#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cvxpy as cp
import cvxopt as cpt


# In[2]:


NUM_OF_STUDENTS = 3
NUM_OF_CLASSES = 3
MAX_CLASSES = 2 # must make lists manually
x1 = cp.Variable((NUM_OF_STUDENTS,(NUM_OF_CLASSES+1)),integer=True)
x2 = cp.Variable((NUM_OF_STUDENTS,(NUM_OF_CLASSES+1)),integer=True)
preferences = np.array([[1,2,3,0],[1,2,3,0],[2,1,3,0]])
# Each row lists the preference for a student
priority = np.array([1,2,3])
max_students = np.array([MAX_CLASSES*NUM_OF_STUDENTS,1,1,1])
# Maximum students for each class

PREFERENCE_MULTIPLIER = 100 # C_1
PRIORITY_MULTIPLIER = 1 # C_2

def cost_func(i,s,pref,prior):
    """Takes in the student, class and their
    preferences and preferences, returns cost"""
    this_pref = pref[i-1]
    school_loc = np.argwhere(this_pref==s).flatten()[0]
    empty_loc = np.argwhere(this_pref==0).flatten()[0]
    c_pref = school_loc*PREFERENCE_MULTIPLIER
    c_prior = (np.argwhere(prior==i).flatten()[0])*PRIORITY_MULTIPLIER
    return c_pref+c_prior

cost = np.fromfunction(np.vectorize(
    lambda a, b: cost_func(a+1,b,preferences,priority)), 
                       (NUM_OF_STUDENTS,NUM_OF_CLASSES+1) ,dtype=int)
print("Cost Matrix:")
print(cost)
diag_wzero = np.diagflat(np.ones(NUM_OF_CLASSES+1,dtype=int))
diag_wzero[0][0] = 0

constraints = [x1>=0,x1<=1,x2>=0,x2<=1,
               cp.sum(x1,axis=1)==1,cp.sum(x2,axis=1)==1,
               # Must be in at least one class or no class
               (x1+x2)@diag_wzero<=1,
               # Cannot be in the same class twice
               # but can be in no class twice
              cp.sum(x1,axis=0) + cp.sum(x2,axis=0)<=max_students]
# Must obey class size limits
obj = cp.Minimize(cp.vec(cost)@cp.vec(x1)+cp.vec(cost)@cp.vec(x2))

# Solving the problem
prob = cp.Problem(obj, constraints)
prob.solve(verbose=False)
print("Status:", prob.status)
print("Total Cost:", prob.value)

def return_text(values):
    classnum = np.argwhere(values==1)[0][0]
    if classnum == 0:
        return "No Class"
    else:
        return "Class " + str(classnum)

for i in range(NUM_OF_STUDENTS):
    print("Student",i+1,"is in",return_text(x1.value[i]),
          "and",return_text(x2.value[i]))

values = np.array(x1.value+x2.value,dtype=int)
print("Values Matrix:")
print(values)


# In[3]:


def compare(a,b,pref):
    """Compares two classes"""
    if np.argwhere(pref==a)[0][0] <= np.argwhere(pref==b)[0][0]:
        return True
    return False

def compare_strict(a,b,pref):
    """Strictly compares two classes"""
    if np.argwhere(pref==a)[0][0] < np.argwhere(pref==b)[0][0]:
        return True
    return False

def strong_domination(A,B,pref):
    """Check if for class lists A and B, 
    A strongly dominates B"""
    for i in range(len(A)):
        if A[i] != 0:
            for j in range(len(B)):
                if B[j] != 0:
                    if compare(i,j,pref)==False:
                        return False
    return True

def weak_domination(A,B,pref):
    """Check if for class lists A and B, 
    A weakly dominates B"""
    for i in range(len(A)):
        if A[i] != 0:
            for j in range(len(B)):
                if B[j] != 0:
                    if compare(i,j,pref)==True:
                        return True
    return False

def ordering(A,pref):
    """From a class list, returns a list of the classes 
    ordered by preferences"""
    element_number = np.sum(A)
    A2 = np.copy(A)
    order_A = np.zeros(element_number,dtype=int)
    for i in range(element_number):
        for j in pref:
            if A2[j] != 0:
                order_A[i] = j
                A2[j] -= 1
                break
    return order_A

def stochastic_domination(A,B,pref):
    """Check if for class lists A and B, A stochastically 
    dominates B. Requires each set to be the same size"""
    if np.sum(A) != np.sum(B):
        raise NotImplementedError(
            "Error: not-same size functionality not implemented")
    element_number = np.sum(A)
    order_A = ordering(A,pref)
    order_B = ordering(B,pref)
    for i in range(element_number):
        if compare(order_A[i],order_B[i],pref) == False:
            return False
    return True

def strong_domination_strict(A,B,pref):
    """Check if for class lists A and B, 
    A strictly strongly dominates B"""
    if strong_domination(A,B,pref) == False:
        return False
    for i in range(len(A)):
        if A[i] != 0:
            for j in range(len(B)):
                if B[j] != 0:
                    if compare_strict(i,j,pref)==True:
                        return True
    return False

def weak_domination_strict(A,B,pref):
    """Check if for class lists A and B, 
    A strictly weakly dominates B"""
    if weak_domination(A,B,pref) == False:
        return False
    for i in range(len(A)):
        if A[i] != 0:
            for j in range(len(B)):
                if B[j] != 0:
                    if compare_strict(i,j,pref)==True:
                        return True
    return False

def stochastic_domination_strict(A,B,pref):
    """Check if for class lists A and B, 
    A strictly stochastically dominates B"""
    if stochastic_domination(A,B,pref) == False:
        return False
    element_number = np.sum(A)
    order_A = ordering(A,pref)
    order_B = ordering(B,pref)
    for i in range(element_number):
        if compare_strict(order_A[i],order_B[i],pref) == True:
            return True
    return False

def lexicon_domination(A,B,pref):
    """Check if for class lists A and B, 
    A lexicon dominates B"""
    n = len(np.delete(pref,np.where(pref==0)))
    order_A = ordering(A,pref)
    order_B = ordering(B,pref)
    for i in range(n-len(order_A)):
        order_A = np.append(order_A,0)
    for i in range(n-len(order_B)):
        order_B = np.append(order_B,0)
    for i in range(n):
        if compare(order_A[i],order_B[i],pref) == False:
            return False
    return True

def lexicon_domination_strict(A,B,pref):
    """Check if for class lists A and B, 
    A strictly lexicon dominates B"""
    n = len(np.delete(pref,np.where(pref==0)))
    order_A = ordering(A,pref)
    order_B = ordering(B,pref)
    for i in range(n-len(order_A)):
        order_A = np.append(order_A,0)
    for i in range(n-len(order_B)):
        order_B = np.append(order_B,0)
    if np.array_equal(order_A,order_B):
        return False
    for i in range(n):
        if compare(order_A[i],order_B[i],pref) == False:
            return False
    return True


# In[9]:


def eliminates_justified_envy(vals,prefs,prios,comparison_strict):
    """Checks if justified envy is eliminated"""
    for i in range(NUM_OF_STUDENTS):
        for j in range(NUM_OF_STUDENTS):
            if (j != i and np.argwhere(prios==i+1)[0][0]
                < np.argwhere(prios==j+1)[0][0] and 
                comparison_strict(vals[j],vals[i],prefs[i]) == True ):
                print("Student",i+1,"envies Student",j+1)
                return False
    print("Eliminates justified envy")
    return True


# In[ ]:




