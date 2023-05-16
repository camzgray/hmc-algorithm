# Introduction

In recent years, Harvey Mudd College (HMC) has taken in an overwhelming
number of CS majors, and has had a shortage of CS class spots available
because of it. The normal process for registering for classes as soon as
they become available, called placement or pre-registration, gives every
student a registration time during which they can add classes that
aren’t yet filled. This is effectively a form of serial dictatorship,
where a priority order (the same for all the classes) is chosen for the
students, and they each take their turn in choosing classes. However,
this isn’t ideal, as it can end up with students near the start of the
order obtaining up to four classes, while the ones at the end may obtain
none.

In order to remedy this problem, the Harvey Mudd CS department has a
process called pre-placement, where they use their own mechanism to
decide before placement which of the CS classes that students can be
placed into. One possible solution to this could again be serial
dictatorship, or a modified version running serial dictatorship multiple
times, where each student only chooses one class at a time. However, the
CS department uses a more complicated mechanism involving Integer Linear
Programming (ILP), where for every possible outcome (a student being
pre-placed into a class), an integer cost is assigned based on the
students’ class preferences and their priority. The total cost is then
minimized subject to constraints: that no student gets into more than
two classes, that no student gets into the same class twice, and that no
student gets placed into two classes with conflicting time (a constraint
we’ll ignore here).

# Class-Choice Problems

As defined in , a **school-choice problem** consists of the following
entities:

-   A finite set *I* of **students**;

-   A finite set *S* of **schools**.

Each entity has a preference:

-   The **students’ preferences** consist of linear orders
    ≻<sub>*I*</sub> = (≻<sub>*i*</sub>)<sub>*i* ∈ *I*</sub> over
    *S* ∪ {∅};

-   The **schools’ priorities** consist of complete and transitive
    binary relations
    ≽<sub>*S*</sub> = (≽<sub>*s*</sub>)<sub>*s* ∈ *S*</sub> over *I*.

There are also constraints:

-   The **capacities** are a number *q*<sub>*s*</sub> ∈ ℕ for each
    school *s* ∈ *S*.

A **matching** is defined as a function *μ* : *I* → *S* ∪ {∅} such that
\|*μ*<sup>−1</sup>(*s*)\| ≤ *q*<sub>*s*</sub> for all *s* ∈ *S*, so that
no school has more students than its capacity. A number of useful
properties are defined in for the school-choice problem: whether a
matching *μ* eliminates justified envy, is non-wasteful, is Pareto
efficient for the students, and for a mechanism, if it is
strategy-proof.

However, because of the students being able to get into multiple classes
(up to two in the HMC case), the model in the school-choice isn’t
sufficient. Here I define a **class-choice problem**. The entities again
consist of

-   A finite set *I* of **students**;

-   A finite set *S* of **classes**;

and each entity has a preference:

-   The **students’ preferences** consist of linear orders
    ≻<sub>*I*</sub> = (≻<sub>*i*</sub>)<sub>*i* ∈ *I*</sub> over
    *S* ∪ {∅};

-   The **classes’ priorities** consist of linear orders
    ≻<sub>*S*</sub> = (≻<sub>*s*</sub>)<sub>*s* ∈ *S*</sub> over *I*;

where for our case, the priority order is strict. The constraints are:

-   The **course maximums** are a number *m*<sub>*i*</sub> ∈ ℕ for each
    student *m*<sub>*i*</sub> ∈ *I*;

-   The **capacities** are a number *q*<sub>*s*</sub> ∈ ℕ for each
    school *s* ∈ *S*.

A **matching** is defined as a function *μ* : *I* → 2<sup>*S*</sup> such
that \|*μ*<sup>−1</sup>(*s*)\| ≤ *q*<sub>*s*</sub> for all *s* ∈ *S*, so
that no class has more students than its capacity, and such that
\|*μ*(*i*)\| ≤ *m*<sub>*i*</sub>, so that no student has more than their
course maximum. Here 2<sup>*S*</sup> is the power set of *S*, the
collection of all subsets including the empty set.

For the HMC mechanism *ϕ*<sub>*H**M**C*</sub>, this requires a **cost
function**. This is defined for each student *i* as a function
*c*<sub>*i*</sub> : *S* ∪ {∅} → *C* ⊂ ℕ where *C* is a finite subset of
the natural numbers consisting of the possible costs. This is required
to satisfy two properties: if
*s*<sub>1</sub>≻<sub>*i*</sub>*s*<sub>2</sub>, then
*c*<sub>*i*</sub>(*s*<sub>1</sub>) ≤ *c*<sub>*i*</sub>(*s*<sub>2</sub>);
and if ∅≻<sub>*i*</sub>*s*, then
*c*<sub>*i*</sub>(∅) = *c*<sub>*i*</sub>(*s*). The first property means
that costs increase non-strictly (so that multiple classes can share the
same cost) for less preferred classes, and the second ensures that
getting a class that the student would prefer not getting a class to has
the same cost as the class. Note that these cost functions can depend on
the priority order of the students. The total cost is given by
$$\\begin{aligned}
    c\_{net} &= \\sum\_{i \\in I} \\left( \\sum\_{s \\in \\mu(i)} c_i(s) + (m_i - \|\\mu(i)\|) c_i(\\emptyset) \\right)\\end{aligned}$$
since the cost for an individual student consists of the costs of each
of their classes, plus the cost for each class they did not get towards
their maximum. If we let *x*<sub>*i*, *s*, *k*</sub> = 1 when student
*i* ∈ *I* gets class *s* ∈ *S* ∪ {∅} (or no class) as the *k*th class in
*μ*(*i*) (ordering that set), and zero else, this becomes an ILP
minimizing
$$\\begin{aligned}
    c\_{net} &= \\sum\_{i \\in I}\\sum\_{s \\in S\\cup \\{\\emptyset\\}} \\sum\_{k = 1}^{m_i} c_i(s)x\_{i,s,k}\\end{aligned}$$
subject to our constraints.

# Desirable Properties

Just like the properties for school-choice problems, we can define
similar ones for class-choice problems. However, we run into a
difficulty: when comparing two matchings *μ*(*i*) and *ν*(*i*), how does
*i* choose which one is better, since they are both sets rather than
single classes? An answer is needed in order to define Pareto
efficiency, which asks if at least one student is made better off while
none are made worse. In generality, given some linear order ≻ over a set
*S*, this consists of defining a binary relation we call a **dominance
relation** over 2<sup>*S*</sup>, which may not be transitive, complete,
or anti-symmetric.

Given two subsets *A*, *B* ∈ 2<sup>*S*</sup>, we say that *A* **strongly
dominates** *B*, *A*≽<sup>*s*</sup>*B*, if for all *a* ∈ *A* and for all
*b* ∈ *B*, we have *a* ≽ *b* (unless *A* is empty, in which we say it
never strongly dominates unless *B* is also empty). We say that *A*
strictly strongly dominates *B*, *A*≻<sup>*s*</sup>*B*, if we have
*A*≽<sup>*s*</sup>*B* and if for at least one *a*′ ∈ *A* and at least
one *b*′ ∈ *B*, we have *a*′ ≻ *b*′ (unless *B* is empty in which we say
that strict dominance holds unless *A* is also empty). This means that
*everything* in *A* is preferred over *B*, and in the strict case, at
least one element is strictly preferred.

<div class="prop">

**Proposition 1**. *Both strong dominance and strict strong dominance
are transitive, but are not complete.*

</div>

<div class="proof">

*Proof.* Suppose that *A*≽<sup>*s*</sup>*B* and *B*≽<sup>*s*</sup>*C*.
Then for all *a* ∈ *A*, *b* ∈ *B*, and *c* ∈ *C*, we have *a* ≽ *b* and
*b* ≽ *c*. But linear relations are transitive, so *a* ≽ *c* and so
*A*≽<sup>*s*</sup>*C*. If this is strict strong dominance, then we have
some *a*′ ≻ *b*′ and *b*′ ≻ *c*′, so that *a*′ ≻ *c*′.

However, it is not complete: take *S* = {1, 2, 3} with preference
1 ≻ 2 ≻ 3, and let *A* = {1, 3}, *B* = {2}. We have 1 ≻ 2, so cannot
have *B*≽<sup>*s*</sup>*A*, but also have 2 ≻ 3, so cannot have
*A*≽<sup>*s*</sup>*B*. ◻

</div>

There are other possible transitive binary relations. We say *A*
**weakly dominates** *B*, *A*≽<sup>*w*</sup>*B*, if there exists some
*a* ∈ *A* and if there exists some *b* ∈ *B* such that *a* ≽ *b*, unless
*B* is empty, in which we say that *A* always weakly dominates *B*. This
is strict weak dominance if there are some *a*′ ∈ *A* and some
*b*′ ∈ *B* such that *a*′ ≻ *b*′.

<div class="prop">

**Proposition 2**. *Weak dominance is complete, but is not transitive.*

</div>

<div class="proof">

*Proof.* Consider two sets *A* and *B*, and any *a* ∈ *A* and *b* ∈ *B*.
Then either *a* ≽ *b* or *b* ≽ *a* is true since linear relations are
complete, and so at least one of *A*≽<sup>*w*</sup>*B* or
*B*≽<sup>*w*</sup>*A* is true, so it is complete.

However, it is not transitive: take *S* = {1, 2, 3, 4} with preference
1 ≻ 2 ≻ 3 ≻ 4, and let *A* = {3}, *B* = {1, 4}, and *C* = {2}. We have
3 ≻ 4 and so *A*≽<sup>*w*</sup>*B*, and 1 ≻ 2 and so
*B*≽<sup>*w*</sup>*C*. However, 2 ≻ 3, and so it is not true that
*A*≽<sup>*w*</sup>*C*, and so this is not transitive. ◻

</div>

The intuition behind strong dominance is that if everything in *A* is
preferred to *B*, *A* will always be chosen over *B*. This is because if
*A*≽<sup>*s*</sup>*B* and *B*≽<sup>*s*</sup>*A*, then *A* = *B*, as
*a* ≽ *b* and *b* ≽ *a* for all *a* and *b*, so *a* = *b* for all, and
*A* = *B* (though this situation can only occur if each has one or zero
elements). However, with weak dominance which is chosen might depend on
other attributes, for two sets can weakly dominate each other: given
*S* = {1, 2, 3} with preference 1 ≻ 2 ≻ 3, and let *A* = {1, 3},
*B* = {2}, we have both *A*≽<sup>*w*</sup>*B* and *B*≽<sup>*w*</sup>*A*.
One question is if there’s an intuitive binary relation over
2<sup>*S*</sup> that while isn’t as strong as strong dominance, still
satisfies this property. For example, given *S* = {1, 2, 3, 4}, with
preference 1 ≻ 2 ≻ 3 ≻ 4, let *A* = {1, 3}, *B* = {2, 4}. It seems like
*A* should dominate *B*, yet it is not by strong domination.

Taking inspiration from how stochastic domination is defined in , we
define **stochastic dominance**, where here we require a preference ≻ on
*S* ∪ {∅}. Given *A* and *B*, order *A*’s elements by their preferences,
so that *a*<sub>*i*</sub> is the ith favorite element of *A*. Similarly
do the same for *B*. If the two are of different sizes, insert empty set
elements {∅} within the smaller one corresponding to the place that the
empty set is within the preferences until the two are the same size.
Then we say that *A* stochastically dominates *B*,
*A*≻<sup>*d*</sup>*B*, if for all *i*,
*a*<sub>*i*</sub> ≽ *b*<sub>*i*</sub>. This is strict stochastic
dominance if *a*<sub>*j*</sub> ≻ *b*<sub>*j*</sub> for some *j*.

The intuition behind this definition is that if the *i*th ranked element
of *A* is better than the *i*th ranked element of *B* for all *i*, *A*
will always be chosen since each individual element is made better off.
As an example, given *S* = {1, 2, 3, 4}, with preference
1 ≻ 2 ≻ 3 ≻ 4 ≻ ∅, let *A* = {1, 3}, *B* = {2, 4}. We see that since
1 ≻ 2 and 3 ≻ 4, *A*≻<sup>*d*</sup>*B*. For another example, given
*S* = {1, 2, 3}, with preference 1 ≻ 2 ≻ ∅ ≻ 3, let *A* = {1},
*B* = {2, 4}. Since 1 ≻ 2 and ∅ ≻ 4, we have *A*≻<sup>*d*</sup>*B*. We
can see that if *A*≽<sup>*d*</sup>*B* and *B*≽<sup>*d*</sup>*A*, then we
have *a*<sub>*i*</sub> ≽ *b*<sub>*i*</sub> and
*b*<sub>*i*</sub> ≽ *a*<sub>*i*</sub>, so
*a*<sub>*i*</sub> = *b*<sub>*i*</sub> and *A* = *B*.

<div class="prop">

**Proposition 3**. *If both sets are of equal size, strong dominance
implies stochastic dominance, and stochastic dominance implies weak
dominance.*

</div>

<div class="proof">

*Proof.* Suppose that *A*≽<sup>*s*</sup>*B*. Then for all *a* ∈ *A* and
*b* ∈ *B*, *a* ≽ *b*. Thus after ordering,
*a*<sub>*i*</sub> ≽ *b*<sub>*i*</sub> for all *i* since this is true for
all elements. So *A*≽<sup>*d*</sup>*B*. Suppose that
*A*≽<sup>*d*</sup>*B*. Then after ordering,
*a*<sub>*i*</sub> ≽ *b*<sub>*i*</sub> for all *i*. For *i* = 1 we have
*a*<sub>1</sub> ≽ *b*<sub>1</sub>, so this is true for at least one
pair, and thus *A*≽<sup>*w*</sup>*B*. ◻

</div>

It turns out the stochastic dominance is a more general version of the
leximax ordering defined in , what we call here **leximax dominance**.
This requires that the empty set be the least preferred element of *S*.
First we define ordered sets
*A*′ = (*a*<sub>1</sub>,…,*a*<sub>*n*</sub>,∅,…,∅) and
*B*′ = (*b*<sub>1</sub>,…,*b*<sub>*m*</sub>,∅,…,∅) so that the non-empty
set elements are ordered in decreasing preference, and so that both *A*′
and *B*′ have total size \|*S*\| when the empty sets are added. We say
that *A* leximax dominates *B*, *A*≽<sup>*l*</sup>*B*, if for all
*i* = 1, …, \|*S*\|, *a*′<sub>*i*</sub> ≽ *b*′<sub>*i*</sub>. We say
that two sets are leximax equivalent, *A*∼<sup>*l*</sup>*B*, if both
*A*≽<sup>*l*</sup>*B* and *B*≽<sup>*l*</sup>*A*, and define strict
leximax dominance as *A*≻<sup>*l*</sup>*B* if *A*≽<sup>*l*</sup>*B* and
it is not true that *A*≻<sup>*l*</sup>*B*.

Stochastic dominance reduces to leximax dominance in the case where the
empty set is the least preferred element of *S*, and all the empty sets
are added at the end. In our specific class-choice problem, this is a
reasonable assumption: no one who gets pre-placed is forced to take a
class that they are pre-placed into, and are free to drop it, so there
is no reason why they should prefer not getting pre-placed.

<div class="prop">

**Proposition 4**. **A*∼<sup>*l*</sup>*B* if and only if *A* = *B*.*

</div>

<div class="proof">

*Proof.* Suppose that *A* = *B*. Then *A*′ = *B*′ and thus
*a*′<sub>*i*</sub> ≽ *b*′<sub>*i*</sub> and
*b*′<sub>*i*</sub> ≽ *a*′<sub>*i*</sub>. So *A*≽<sup>*l*</sup>*B* and
*B*≽<sup>*l*</sup>*A*, and thus *A*∼<sup>*l*</sup>*B*. Now suppose that
*A*∼<sup>*l*</sup>*B*. Then *a*′<sub>*i*</sub> ≽ *b*′<sub>*i*</sub> and
*b*′<sub>*i*</sub> ≽ *a*′<sub>*i*</sub>, so that
*a*′<sub>*i*</sub> = *b*′<sub>*i*</sub> and *A*′ = *B*′. Since there are
then an equal number of empty sets, this means that *A* = *B*. ◻

</div>

<div class="prop">

**Proposition 5**. *Leximax dominance is transitive.*

</div>

<div class="proof">

*Proof.* Suppose that *A*≽<sup>*l*</sup>*B* and *B*≽<sup>*l*</sup>*C*.
Then we have that *a*′<sub>*i*</sub> ≽ *b*′<sub>*i*</sub> and
*b*′<sub>*i*</sub> ≽ *c*′<sub>*i*</sub>. Since *B*′ is the same in each
comparison (unlike in the general case for stochastic dominance), we
have *a*′<sub>*i*</sub> ≽ *c*′<sub>*i*</sub>, and so
*A*≽<sup>*l*</sup>*C*. ◻

</div>

There are a number of important properties that leximax dominance
satisfies. These are proved in , and we do not prove them here.

<div class="theo">

**Theorem 1**. *Leximax dominance satisfies **simple dominance**: for
all *a*, *b* ∈ *S*, if *a* ≻ *b*, then {*a*}≻<sup>*l*</sup>{*b*}.*

</div>

This property means that if a student gets a choice between two single
classes, they will choose the result with the class that they prefer.

<div class="theo">

**Theorem 2**. *Leximax dominance satisfies **simple monotonicity**: for
all *a*, *b* ∈ *S* such that *a* ≠ *b*, {*a*, *b*}≻<sup>*l*</sup>{*a*}.*

</div>

This property means that if a student has an option to take one class,
or that one class plus another class, they will choose the latter. This
is only realistic in our case because the students aren’t forced to take
classes and pre-placement is an option: students often times wouldn’t
prefer six classes over five!

<div class="theo">

**Theorem 3**. *Leximax dominance satisfies **independence**: for all
*A*, *B* ∈ 2<sup>*S*</sup>, for all *s* ∈ *S* − (*A*∪*B*) we have that
*A* ∪ {*s*}≽<sup>*l*</sup>*B* ∪ {*s*} if and only if
*A*≽<sup>*l*</sup>*B*.*

</div>

This property means that adding or subtracting the same single class
from two pre-placement results won’t change which result the student
chooses. This may not be satisfied in our case, as often times two
classes may pair well together.

<div class="theo">

**Theorem 4**. *Leximax dominance satisfies **robustness of strict
preference**: for all *A*, *B* ∈ 2<sup>*S*</sup>, for all
*s* ∈ *S* − (*A*∪*B*) we have that if *A*≻<sup>*l*</sup>*B*, *a* ≻ *s*
for all *a* ∈ *A*, and *b* ≻ *s* for all *b* ∈ *B*, then
*A*≻<sup>*l*</sup>*B* ∪ {*s*}.*

</div>

This property means that if a student prefers one class schedule to
another, adding a class that the student likes less than any class in
either of those schedules to the schedule the student prefers less does
not make them prefer it more.

<div class="theo">

**Theorem 5**. *Suppose that ≽<sup>*r*</sup> is a dominance relation on
2<sup>*S*</sup> that is also transitive and reflexive. Then
≽<sup>*r*</sup> satisfies simple dominance, simple monotonicity,
independence, and robustness of strict preference if and only if it is
leximax dominance, ≽<sup>*r*</sup> = ≽<sup>*l*</sup>. (*Theorem 4.1* of
)*

</div>

This result says that leximax ordering is unique in that it is the only
such ordering with these properties.

Returning to our class-choice problem, suppose that we are given a
dominance relation $\\succcurlyeq^r_i$ and a strict dominance relation
$\\succ^r_i$ for each *i*. In our particular problem, each class has the
same priority relation over students, so we assume that
≻<sup>\*</sup> = ≻<sub>*s*</sub> for all *s* ∈ *S*. We also assume that
each student can get at most the same number of classes (2 in the HMC
case), so that *m*<sup>\*</sup> = *m*<sub>*i*</sub> for all *i* ∈ *I*.
We can now define some desired properties that require comparisons
between sets.

We say that a matching *μ* **eliminates justified envy** if there is
*i* ∈ *I* such that, for some *j* ∈ *I* both *i*≻<sup>\*</sup>*j* and
$\\mu(j) \\succ^r_i \\mu(i)$ hold.

We say that a matching *μ* is **non-wasteful** if there is no pair
*i* ∈ *I* and non-empty set of classes *S*′ ⊆ *S*,
\|*S*′\| ≤ *m*<sup>\*</sup> such that both $S' \\succ^r_i \\mu(i)$ and
all classes in *S*′ have an empty seat.

We say that a matching *μ* is **Pareto efficient for students** if there
does not exists some matching *ν* such that for all *i* ∈ *I*,
$\\nu(i) \\succcurlyeq^r_i \\mu(i)$, and for some *j* ∈ *I*,
$\\nu(j) \\succ^r_j \\mu(j)$.

We say that a mechanism *ϕ* is **strategy-proof** if for every profile
of preferences (≻<sub>*i*</sub>)<sub>*i* ∈ *I*</sub>, there is no such
preference relation  ≻ ′<sub>*i*</sub> for agent *i* in which
$$\\begin{aligned}
    \\phi\[\\succ'\_i,\\succ\_{-i}\](i) \\succ^r_i \\phi\[\\succ_i,\\succ\_{-i}\](i).\\end{aligned}$$

# HMC Algorithm

In order to run the HMC algorithm, coding it into an ILP solver is
needed. Code for this is given in the appendix, along with code testing
desirable properties under different dominance relations. For the
remainder of this paper, we assume that *m*<sup>\*</sup> = 2, and as
noted for the reasons to do with leximax dominance, that getting no
class is the least preferred class of each student. For our cost
function, we take a linear one of the form
$$\\begin{aligned}
    c^{\\mathrm{linear}}\_i(s) &= c_i^{\\mathrm{preference}}(s) + c_i^{\\mathrm{priority}}(s)\\end{aligned}$$
so that there is cost from both the priority number of the student, and
the preferences of the student. For these we assume
$$\\begin{aligned}
    c_i^{\\mathrm{preference}}(s) &= C_1 (\\mathrm{preference}\_i(s)-1) \\\\
    c_i^{\\mathrm{priority}}(s) &= C_2 (\\mathrm{priority}(i)-1)\\end{aligned}$$
where preference<sub>*i*</sub>(*s*) is the place in which student *i*
ranks class *s*, and priority(*i*) is rank of the student in priority.
The subtraction by one allows it so that the top-priority student
getting their top course has no cost. *C*<sub>1</sub> and
*C*<sub>2</sub> are positive integer constants, and their ratio
determines how much preferences cost in comparison to priority. Since
priority is used primarily as a tie-breaker, in real-world
implementation we likely have *C*<sub>1</sub> ≫ *C*<sub>2</sub>, but we
do not assume that here.

<div class="theo">

**Theorem 6**. *The HMC algorithm does not eliminate justified envy
under strong, weak, stochastic, or leximax dominance.*

</div>

<div class="proof">

*Proof.* Considering a problem with students *I* = {1, 2, 3} and classes
{*s*<sub>1</sub>, *s*<sub>2</sub>, *s*<sub>3</sub>}, each with maximum
one student allowed. Suppose that we have the preferences
$$\\begin{aligned}
    \\succcurlyeq_1 : 1,2,3,\\emptyset \\\\
    \\succcurlyeq_2 : 1,2,3,\\emptyset \\\\
    \\succcurlyeq_3 : 2,1,3,\\emptyset\\end{aligned}$$
and the priority
$$\\begin{aligned}
    \\succcurlyeq^\* 1,2,3.\\end{aligned}$$
We choose the cost constants *C*<sub>1</sub> = 100 and
*C*<sub>2</sub> = 1. The HMC algorithms returns the matching
$$\\begin{aligned}
    \\mu\_{HMC}(1) &= \\{1\\} \\\\
    \\mu\_{HMC}(2) &= \\emptyset \\\\
    \\mu\_{HMC}(3) &= \\{2,3\\}\\end{aligned}$$
with cost 1106.

We can see here that Student 2 has justified envy towards Student 3. We
have $\\mu\_{HMC}(3) \\succ_2^s \\mu\_{HMC}(2)$ and
$\\mu\_{HMC}(3) \\succ_2^w \\mu\_{HMC}(2)$ vacuously. Under
stochastic/leximax dominance, we compare 2≻<sub>2</sub>∅ and
3≻<sub>2</sub>∅, and so $\\mu\_{HMC}(3) \\succ_2^d \\mu\_{HMC}(2)$ and
$\\mu\_{HMC}(3) \\succ_2^l \\mu\_{HMC}(2)$. ◻

</div>

<div class="theo">

**Theorem 7**. *The HMC algorithm is not strategy-proof under strong,
weak, stochastic, or leximax dominance.*

</div>

<div class="proof">

*Proof.* Consider the problem in the previous proof, except that agent 2
reports the preferences
$$\\begin{aligned}
    \\succcurlyeq_2 : 2,3,1,\\emptyset\\end{aligned}$$
The HMC algorithms returns the matching
$$\\begin{aligned}
    \\mu'\_{HMC}(1) &= \\{1\\} \\\\
    \\mu'\_{HMC}(2) &= \\{3\\} \\\\
    \\mu'\_{HMC}(3) &= \\{2\\}\\end{aligned}$$
with cost 1006.

Vacuously again, we have $\\mu'\_{HMC}(2) \\succ_2^s \\mu\_{HMC}(2)$ and
$\\mu'\_{HMC}(2) \\succ_2^w \\mu\_{HMC}(2)$. Under stochastic/leximax
dominance, we have the comparison 3≽<sub>2</sub>∅, and both
$\\mu'\_{HMC}(2) \\succ_2^d \\mu\_{HMC}(2)$ and
$\\mu'\_{HMC}(2) \\succ_2^l \\mu\_{HMC}(2)$. ◻

</div>

We next prove a proposition about lexicon domination and cost.

<div class="prop">

**Proposition 6**. *If for lexicon dominance, $A \\succcurlyeq^l_i B$,
and the cost function *c*<sub>*i*</sub>(*s*) is strictly increasing with
preference<sub>*i*</sub>(*s*), then the (individual) cost for any
*i* ∈ *I* of *A* is less than *B*,
$$\\begin{aligned}
     \\sum\_{s \\in A} c_i(s) + (m^\* - \|A\|) c_i(\\emptyset) \\leq \\sum\_{s \\in B} c_i(s) + (m^\* - \|B\|) c_i(\\emptyset).\\end{aligned}$$
If the lexicon dominance is strict, so is this inequality.*

</div>

<div class="proof">

*Proof.* We can put this in the form
$$\\begin{aligned}
     \\sum\_{s \\in A} c_i(s) + (\|S\| - \|A\|) c_i(\\emptyset) &\\leq \\sum\_{s \\in B} c_i(s) + (\|S\| - \|B\|) c_i(\\emptyset) \\\\
     \\sum\_{s \\in A'} c_i(s)  &\\leq \\sum\_{s \\in B'} c_i(s) \\\\
     \\sum\_{i = 1}^{\|S\|} c_i(a'\_i) &\\leq \\sum\_{i = 1}^{\|S\|} c_i(b'\_i) \\\\
     0 &\\geq \\sum\_{i = 1}^{\|S\|} (c_i(a'\_i) - c_i(b'\_i))\\end{aligned}$$
now since *a*′<sub>*i*</sub>≽<sub>*i*</sub>*b*′<sub>*i*</sub> by
definition of lexicon dominance, we have
*c*<sub>*i*</sub>(*a*′<sub>*i*</sub>) ≤ *c*<sub>*i*</sub>(*b*′<sub>*i*</sub>)
as the cost function strictly increases. If the lexicon dominance is
strict then *a*′<sub>*i*</sub>≻<sub>*i*</sub>*b*′<sub>*i*</sub> for (at
least) one of these, and so one of the summands must be positive. ◻

</div>

Note that our specific cost function *c*<sub>*i*</sub><sup>linear</sup>
is strictly increasing with preference<sub>*i*</sub>(*s*). We have the
following results:

<div class="theo">

**Theorem 8**. *If the cost function *c*<sub>*i*</sub>(*s*) is strictly
increasing under preference<sub>*i*</sub>(*s*), the HMC algorithm is
non-wasteful under leximax dominance.*

</div>

<div class="proof">

*Proof.* Suppose that we have a non-empty set of classes *S*′ ⊂ *S* such
that $S' \\succ^s_l \\mu(i)$, \|*S*′\| ≤ *m*<sup>\*</sup>, and all
classes in *S*′ have an empty seat. Define a matching *ν* so that it
assigns *i* to *S*′ while keeping all other agents in the same matching
as *μ*. The cost for each student other than *i*, and by the previous
proposition, the cost for *i* decreases, so the net cost decreases.
However, this means that the cost was not minimized subject to the
constraints, and so *μ* could not have been given by the HMC algorithm,
a contradiction. ◻

</div>

<div class="theo">

**Theorem 9**. *If the cost function *c*<sub>*i*</sub>(*s*) is strictly
increasing under preference<sub>*i*</sub>(*s*), the HMC algorithm is
Pareto efficient for students under leximax dominance.*

</div>

<div class="proof">

*Proof.* Suppose that is not Pareto efficient under leximax dominance,
then there is some matching *ν* such that for all *i* ∈ *I*,
$\\nu(i) \\succcurlyeq^l_i \\mu(i)$, and for some *j* ∈ *I*,
$\\nu(j) \\succ^l_j \\mu(j)$. Now, for each *i* this means that the cost
for them must decrease or stay the same, and for *j* the cost must
decrease, and so the cost decreases overall. This implies that the cost
decreases for the algorithm, and so we have a contradiction. ◻

</div>

Note however, the one used in practice is not of the form
*c*<sup>linear</sup>(*i*), as there are only four different costs given
for each preference. Consider a more general form of the cost function,
where
$$\\begin{aligned}
    c\_{net} &= \\sum\_{i \\in I} c\_{net,i}(\\mu(i)) \\\\
    c\_{net,i}(\\mu(i)) &= \\sum\_{s \\in S\\cup \\{\\emptyset\\}} \\sum\_{k = 1}^{m_i} c_i(s)x\_{i,s,k} \\\\
    &= \\sum\_{s \\in \\mu(i)} c_i(s) + (m_i - \|\\mu(i)\|) c_i(\\emptyset)\\end{aligned}$$
and we suppose that *c*<sub>*i*</sub>(*s*) is a monotonically increasing
function of preference(*s*) and a strictly increasing function of
priority(*i*). Unfortunately, the proposition proving lexicon dominance
gives an decrease in cost does not hold, as the inequality may not be
strict in the case of strict lexicon dominance. In this case we can have
multiple preferences give the same cost, and the algorithm can choose
the less preferred one. Note that our linear cost function with
*C*<sub>1</sub> = 0 (which we didn’t allow earlier) satisfies
monotonically increasing still, so we use that in the following results.

<div class="theo">

**Theorem 10**. *The HMC algorithm is not non-wasteful nor Pareto
efficient for the students under leximax dominance using a cost function
*c*<sub>*i*</sub>(*s*) only monotonically increasing under
preference<sub>*i*</sub>(*s*).*

</div>

<div class="proof">

*Proof.* Considering a problem with students *I* = {1, 2, 3} and classes
{*s*<sub>1</sub>, *s*<sub>2</sub>, *s*<sub>3</sub>}, each with maximum
one student allowed. Suppose that we have the preferences
$$\\begin{aligned}
    \\succcurlyeq_1 : 1,2,3,\\emptyset \\\\
    \\succcurlyeq_2 : 1,2,3,\\emptyset \\\\
    \\succcurlyeq_3 : 2,1,3,\\emptyset\\end{aligned}$$
and the priority
$$\\begin{aligned}
    \\succcurlyeq^\* 1,2,3.\\end{aligned}$$
We choose the cost constants *C*<sub>1</sub> = 0 and
*C*<sub>2</sub> = 1, which is monotonically increasing. The HMC
algorithms returns the matching
$$\\begin{aligned}
    \\mu\_{HMC}(1) &= \\emptyset \\\\
    \\mu\_{HMC}(2) &= \\emptyset \\\\
    \\mu\_{HMC}(3) &= \\{3\\}\\end{aligned}$$
with cost 6.

We can see here that while Student 1 would prefer to get {1} than ∅
under lexicon dominance and class 1 has available seats. So the
algorithm is not non-wasteful. Similarly, a matching where Student 1 is
assigned to {1} would improve Student 1’s situation without changing
either Student 2 or Student 3, and so this is not a Pareto efficient
matching for the students. ◻

</div>

# Conclusion

In conclusion, the HMC algorithm under lexicon domination satisfies none
of the desired properties of eliminating justified envy, being
non-wasteful, being Pareto efficient for students, and being
strategy-proof. However, this is only because the forces preferences to
be grouped into the categories "Excited about taking it", "Interested in
taking it", "Open to taking it", and "Can’t or won’t take it" , and if
instead the algorithm took in full strict preference rankings for every
of the classes, it would become Pareto efficient for students and
non-wasteful. While ranking like this may take considerably more time on
the students’ parts, ensuring Pareto efficiency for students might be
worth that time.

However, we should note that lexicon domination likely is not the
greatest model for domination. Likely, dominance relations on subsets of
courses depend on the individual student and not just on their
single-course preferences. For example, we could have two students with
the same single-course preferences where one wants to take two similar
courses together, whereas another only wants to take one, and their
dominance relations will be different. One remedy to this could be by
asking the students about their domination relations, however, this will
take $1 + S + \\frac{S(S-1)}{2}$ entries as opposed to just *S* (more
generally, *O*(*S*<sup>*m*<sup>\*</sup></sup>), which for a large number
of courses is infeasible.

Another possibility could be to use a version of deferred acceptance, as
at least for the school-choice problem, this does eliminate justified
envy and is strategyproof. While I do not explore this in the paper,
because the classes all have the same priority over students, it seems
reasonable to suspect that this class of mechanisms may end up with the
same results as one of the versions of serial dictatorship briefly
mentioned earlier. If so, for Harvey Mudd this would mostly mean just
giving CS students priority on CS courses and having the pre-placement
mechanism be the same as placement. If the same results hold as in the
school-choice problem, this won’t lead to a mechanism that is Pareto
efficient for students, though it may not have other mechanisms Pareto
dominating it.

# Appendix: Python Implementation

``` python
```
