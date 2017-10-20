#  NP, NP completeness, and the Cook-Levin Theorem

> # { .objectives }
* Introduce the class $\mathbf{NP}$  capturing a great many important computational problems \
* $\mathbf{NP}$-completness: evidence that a problem might be intractable. \
* The $\mathbf{P}$ vs $\mathbf{NP}$ problem.


>_"In this paper we give theorems that suggest, but do not imply, that these problems, as well as many others, will remain  intractable perpetually"_, Richard Karp, 1972



## The class $\mathbf{NP}$


So far we have shown that 3SAT is no harder than Quadratic Equations, Independent Set, Maximum Cut, and Longest Path.
But to show that they are equivalent we need to give reductions in the other direction, reducing each one of these problems to 3SAT as well.
It turns out we can reduce all three problems to 3SAT in one fell swoop.


In fact, this result extends  far beyond these particular problems.
All of the problems we discussed in the previous lecture, and a great many other problems, share the same  commonality:
they are all _search_ problems, where the goal is to decide, given an instance $x$ whether there exists a _solution_ $y$ that satisfies some condition.
For example, in 3SAT, the instance is a formula and the solution is an assignment to the variable, in Max-Cut the instance is a graph and the solution is a cut in the graph, and so on and so forth.
It turns out that  _every_ such search problem can be reduced to 3SAT.

To make this precise, we need to make the following mathematical definition.
We define the class $\mathbf{NP}$ to  contain all Boolean functions that correspond to a _search problem_ of the form above.
That is, functions that  output $1$ on $x$ if and only if there exists a solution $y$ such that the pair $(x,y)$ satisfies some polynomial-time checkable condition.
Formally, $\mathbf{NP}$ is defined as follows:



> # {.definition title="NP" #NP-def}
We say that $F:\{0,1\}^* \rightarrow \{0,1\}$ is in $\mathbf{NP}$ if there exists some constants $a,b \in \N$ and $G:\{0,1\}^* \rightarrow \{0,1\}$ such that $G\in \mathbf{P}$ and for every $x\in \{0,1\}^n$
$$
F(x)=1 \Leftrightarrow \exists_{y \in \{0,1\}^{an^b}} \text{ s.t. } G(x,y)=1 \label{NP:eq}
$$

The name $\mathbf{NP}$ stands for "nondeterministic polynomial time" and is used for historical reasons, see the bibiographical notes.


### Examples:

* $3SAT$ is in $\mathbf{NP}$ since for every $\ell$-variable formula $\varphi$, $3SAT(\varphi)=1$ if and only if there exists a satisfying assignment $x \in \{0,1\}^\ell$ such that $\varphi(x)=1$, and we can check this condition in polynomial time.^[Note that an $\ell$ variable formula $\varphi$ is represented by a string of length at least $\ell$, and we can use some "padding" in our encoding so that the assignment to $\varphi$'s variables  is encoded by a string of length exactly $|\varphi|$. We can always use this padding trick, and so one can think of the condition [{NP:eq}](){.eqref} as simply stipulating that the "solution" $y$ to the problem $x$ is of size at most $poly(|x|)$.]


* $QUADEQ$ is in $\mathbf{NP}$ since for every $\ell$ variable instance of quadratic equations $E$, $QUADEQ(E)=1$ if and only if there exists an assignment $x\in \{0,1\}^\ell$ that satisfies $E$ and we can check this condition in polynomial time.

* $ISET$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $ISET(G,k)=1$ if and only if there exists a set $S$ of $k$ vertices that contains no pair of neighbors in $G$.
*
* $LONGPATH$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $LONGPATH(G,k)=1$ if and only if there exists a simple path $P$ in $G$ that is of length at least $k$, and we can check this condition in polynomial time.

* $MAXCUT$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $MAXCUT(G,k)=1$ if and only if there exists a cut $(S,\overline{S})$ in $G$ that cuts at least $k$ edges, and we can check this condition in polynomial time.

### From $\mathbf{NP}$ to 3SAT

There are many, many, _many_, more examples of interesting functions we would like to compute that are easily shown to be in $\mathbf{NP}$. What is quite amazing is that if we can solve 3SAT then we can solve all of them!

The following is one of the most fundamental theorems in Computer Science:

> # {.theorem title="Cook-Levin Theorem" #cooklevin-thm}
For every $F\in \mathbf{NP}$, $F \leq_p 3SAT$.

We will soon show the proof of [cooklevin-thm](){.ref}, but note that it immediately implies that $QUADEQ$, $LONGPATH$, and $MAXCUT$ all reduce to $3SAT$.
In fact, combining it with the reductions we've seen, it implies that all these problems are _equivalent!_
To reduce $QUADEQ$ to $LONGPATH$, we can first reduce $QUADEQ$ to $3SAT$ using [cooklevin-thm](){.ref} and use the reduction we've seen from $3SAT$ to $LONGPATH$.
There is of course nothing special about $QUADEQ$ here- by combining [cooklevin-thm](){.eqref} with the reduction we saw, we see that just like $3SAT$,  _every_ $F\in \mathbf{NP}$ reduces to $LONGPATH$, and the same is true for $QUADEQ$ and $MAXCUT$.
All these problems are in some sense "the hardest in $\mathbf{NP}$" in the sense that an efficient algorithm for one of them would imply an efficient algorithm for _all_ the problems in $\mathbf{NP}$.
This motivates the following definition

> # {.definition title="$\mathbf{NP}$ completeness" #NPC-def}
We say that $G:\{0,1\}^* \rightarrow \{0,1\}$ is _$\mathbf{NP}$ hard_ if for every $F\in \mathbf{NP}$,
$F \leq_p G$. We say that $G$ is _$\mathbf{NP}$ complete_ if $G$ is $\mathbf{NP}$ hard and it is in $\mathbf{NP}$.

[cooklevin-thm](){.ref} and the reductions we've seen in the last lecture show that despite their superficial differences, 3SAT, quadratic equations, longest path, independent set, and maximum cut, are all $\mathbf{NP}$ complete. Thousands more problems have been shown to be $\mathbf{NP}$ complete, arising from all science, mathematics, economics, engineering and many other fields.

### What does this mean?



Clearly $\mathbf{NP} \supseteq \mathbf{P}$, since if we can decide efficiently whether $F(x)=1$, we can simply ignore any "solution" that we are presented with.  Also, $\mathbf{NP} \subseteq \mathbf{EXP}$, since all the problems in $\mathbf{NP}$ can be solved in exponential time by enumerating all the possible solutions.
_The_ most famous conjecture in Computer Science is that $\mathbf{P} \neq \mathbf{NP}$.
One way to refute this conjecture is to give a polynomial-time algorithm for even a single one of the $\mathbf{NP}$-complete problems such as 3SAT, Max Cut, or the thousands of others that have been studied in all fields of human endeavors.
The fact that these problems have been studied by so many people, and yet not a single polynomial-time algorithm for them was found, supports that conjecture that indeed $\mathbf{P} \neq \mathbf{NP}$.
In fact, for many of these problems (including all the ones we mentioned above), we don't even know of a $2^{o(n)}$ time algorithm!
However, to the frustration of computer scientists, we have not yet been able to prove that $\mathbf{P}\neq\mathbf{NP}$ or even rule out the existence of an $O(n)$ time algorithm for 3SAT.


One of the mysteries of computation is that people have observed a  certain empirical "zero one law" or "dichotomy" in the computational complexity of natural problems, in the sense that many natural problems are either in $\mathbf{P}$ (in fact often with a low exponent) or are $\mathbf{NP}$ hard. However, it is believed that there are problems in $\mathbf{NP}$ that are neither in $\mathbf{P}$ not in $\mathbf{NP}$, and in fact a result known as "Ladner's Theorem" shows that if $\mathbf{P} \neq \mathbf{NP}$ then this is the case.




![A rough illustration of the (conjectured) status of problems in exponential time. Darker colors correspond to higher running time, and the circle in the middle is the problems in $\mathbf{P}$. $\mathbf{NP}$ is a (conjectured to be proper) superclass of $\mathbf{P}$ and the NP complete problems (or NPC) for short are the "hardest" problems in NP, in the sense that a solution for one of them implies solution for all other problems problems in NP. It is conjectured that all the NP complete problems require at least $\exp(n^\epsilon)$ time to solve for a constant $\epsilon>0$, and many require  $\exp(\Omega(n))$ time. The _permanent_ is not believed to be contained in $\mathbf{NP}$ though it is $\mathbf{NP}$-hard, which means that a polynomial-time algorithm for it implies that $\mathbf{P}=\mathbf{NP}$.](../figure/PNPmap.png){#figureid .class width=300px height=300px}


^[TODO: maybe add examples of NP hard problems as a barrier to understanding - problems  from economics, physics, etc.. that prevent having a closed-form solutions]

^[TODO: maybe include knots]




## The Cook-Levin Theorem


We will now prove the Cook-Levin Theorem, which  is the underpinning to  a great web of reductions from 3SAT to thousands of problems across great many fields.
Some problems that have been shown NP complete include: minimum-energy protein folding, minimum surface-area foam configuration, map coloring,    optimal Nash equilibrium, quantum state entanglement, minimum supersequence of a genome, minimum codeword problem, shortest vector in a lattice, minimum genus knots, positive Diophantine equations, integer programming, and many many more..
The worst-case complexity of all these problems is (up to polynomial factors) equivalent to that of 3SAT, and through the Cook-Levin Theorem, to all problems in $\mathbf{NP}$.


To prove [cook-levin-thm](){.ref} we need to show that $F \leq_p 3SAT$ for every $F\in \mathbf{NP}$.
We will do so in three stages.
We define two intermediate problems: $NANDSAT$ and $3NAND$.
We will shortly show the definitions of these two problems, but
[cook-levin-thm](){.ref} will follow from the following three lemmas:

> # {.lemma #nand-thm}
$NANDSAT$ is $\mathbf{NP}$-hard.

> # {.lemma  #threenand-thm}
$NANDSAT \leq_p 3NAND$.

> # {.lemma  #threenand-sat-thm}
$3NAND \leq_p 3SAT$.

Together [nand-thm](){.ref}, [threenand-thm](){.ref}, and [threenand-sat-thm](){.ref} immediately imply that $3SAT$ is  $\mathbf{NP}$-hard(can you see why?), hence establishing [cook-levin-thm](){.ref}.
We now prove them one by one, providing the requisite definitions as we go along.

## The $NANDSAT$ Problem, and why it is $\mathbf{NP}$ complete.

We define the $NANDSAT$ problem as follows. On input a string $Q\in \{0,1\}^*$, we define $NANDSAT(Q)=1$ if and only if $Q$ is a valid representation of an $n$-input and single-output NAND program and there exists some $y\in \{0,1\}^n$ such that $Q(y)=1$.
To prove [nand-thm](){.ref}  we need to show that for every $F\in \mathbf{NP}$, $F \leq_p NANDSAT$.
The high level __proof idea__ is that by the definition  of $\mathbf{NP}$, there is some NAND++ program $P_F$ and some polynomial $T(\cdot)$ such that $F(x)=1$ if and only if there exists some $y$ such that $P_F(x,y)$ outputs $1$ within $T(|x|)$ steps.
Now by "unrolling the loop" of the NAND++ $P_F$ we can convert it into a  NAND program $Q$ that on input $y$ will simulate $P_F(x,y)$ for $T(|x|)$ steps.
We will then get that $NANDSAT(Q)=1$ if and only if $F(x)=1$.
We now present the details.

TO BE COMPLETED


Since given $P$ and $x$, we can check in polynomial (in fact $O(|P|^2 \log(|P|))$ time) whether $P(x)=1$, $NANDSAT$ is in $\mathbf{NP}$.
Hence the proof of [nand-thm](){.ref} will follow by showing that $NANDSAT$ is $\mathbf{NP}$ hard, or in other words, that $F \leq_p NAND$ for every $F\in \mathbf{NP}$.

Let $F\in \mathbf{NP}$. Hence there are constants $a,b,c \in \N$ and a  NAND++ program $P_F$ such that for every $x\in \{0,1\}^n$, $F(x)=1$ if and only if there exists some $y\in \{0,1\}^{an^b}$ such that $P_F(xy)$ outputs $1$ within $n^c$ steps.
Recall that we had the following "NAND++ to NAND compiler":

> # {.theorem title="NAND++ to NAND compiler" #nand-compiler}
There is an $\tilde{O}(n)$-time NAND++ program $COMPILE$ such that on input a NAND++ program $P$,  and strings of the form $1^n,1^m,1^T$  outputs a NAND program $Q_P$ of at most $O(T \log T)$ lines with $n$ bits of inputs and $m$ bits of output, such that: \
For every $x\in\bits^n$, if $P$ halts on input $x$ within fewer than $T$ steps and outputs some string $y\in\bits^m$, then $Q_P(x)=y$.  


Therefore, we can transform the NAND++ program $P_F$ into a NAND program $Q_F$ of at most $\tilde{O}(n^c)$ lines taking  $n+an^b$ bits of input and outputting one bit, such that $P_F(xy)=Q_F(xy)$ for every $x\in \{0,1\}^n$ and $y\in \{0,1\}^n$.  

Now if $Q_F$ has $t$ lines, then we can transform $Q_F$ and $x$ into a NAND program $Q_{F,x}$ with $t'+4$  lines that takes $an^b$ bits of inputs, and satisfies  $P_x(y)=Q_{F,x}(x,y)$ for every $y\in \{0,1\}^{an^b}$.
The transformation is very simple.
Recall that by adding four lines to the program, we can ensure that we have variables `zero` and `one` that are equal to $0$ and $1$ respectively.
Now for every $i\in \{0,\ldots,n-1\}$, we can replace any mention of `x_`$i$ in the program with either `zero` or `one` depending on whether $x_i$ is equal to $0$ or $1$ respectively.
Then for $i= n,\ldots, n+an^b-1$, we can replace `x_`$i$ with `x_`$i-n$ so we make the last $an^b$ inputs of $Q_F$ become the first inputs of $Q_{F,x}$.

By our construction, $NAND(Q_{F,x})=1$ if and only if there is $y\in \{0,1\}^{an^b}$ such that  $P_F(xy)=1$, which by definition, happens if and only if $F(x)=1$.
Hence the polynomial-time transformation $x \mapsto Q_{F,x}$ is a reduction from $F$ to $NANDSAT$,
completing the proof of [nand-thm](){.ref}.

## The $3NAND$ problem

The $3NAND$ problem is defined as follows: the input is a logical formula on a set of  variables $z_1,\ldots,z_m$
which is an AND of constraints of the form $z_i = NAND(z_j,z_k)$.
The output is $1$ if and only if there is an  assignment to the $z$'s that satisfies all these constraints.

To prove [threenand-thm](){.ref} we need to give a reduction from $NANDSAT$ to $3NAND$.
Given a NAND program $P$ with $n$ inputs, one outputs, and  $m$ lines, we define a $3NAND$ formula $\psi$ as follows.
The formula $\psi$ will have $m+n$ variables $z_1,\ldots,z_{m+n+1}$.
For every $i\in \{1,\ldots,m \}$, the variable $z_i$ will correspond to the $i^{th}$ line of the program $P$.
The variables $z_{m+1},\ldots,z_{m+n}$ will correspond to the input variables `x_0` ... `x_`$n-1$ of $P$.
The last variable $z_{m+n+1}$ is added for convenience, where we ensure that it is always the negation of $z_{m+n}$ by adding the constraint $z_{m+n+1}=NAND(z_{m+n},z_{m+n})$.

If the $i^{th}$ line in the program $P$ has the form
```
var := var' NAND var''
```
then we add a constraint of the form $z_i = NAND(z_j,z_k)$, where we choose $j$ and $k$ as follows.
If `var'` is an input variable `x_`$\ell$, then we choose $j=n+\ell$.
Similarly, if `var''` is an input variable `x_`$\ell'$, then we choose $k=n+\ell'$.
If `var'` is a workspace variable then we let $j$ be the index of the last line prior to $i$ in which `var'` was assigned.
Similarly, if `var''` is a workspace variable then we let $k$ be the index of the last line prior to $i$ in which `var''` was assigned.

Finally, if $i_0$ is the last line in which the output variable `y_0` was assigned, then we add the constraint $z_{i_0} = NAND(z_{m+n},z_{m+n+1})$, which (since we constrained $z_{m+n+1}=1-z_{m+n}$) is equivalent to constraining $z_{i_0}=1$.

![We reduce $NANDSAT$ to $3NAND$ by mapping a program $P$ to a formula $\psi$ where we have a variable for each line and input variable of $P$, and add a constraint to ensure that the variables are consistent with the program. We also add a constraint that the final output is $1$. One can show that there is an input $x$ such that $P(x)=1$ if and only if there is a satisfying assignment for $\psi$.](../figure/3NANDreduction.png){#figureid .class width=300px height=300px}

We make the following claim

> # {.lemma #temp-lemma-nand }
There is $x\in \{0,1\}^n$ s.t. $P(x)=1$ if and only if there is $z\in \{0,1\}^{m+n+1}$ s.t. $\psi(z)=1$.

> # {.proof data-ref="temp-lemma-nand"}
Suppose that there is such an $x$, and consider the execution of $P$ on $x$.
For $i=1,\ldots,m$ we let $z_i$ be the value that is assigned to a variable in the $i^{th}$ line, for $j=0,\ldots,n-1$, we let $z_{n+1+j}=x_j$, and we let $z_{m+n+1}=1-z_{m+n}$.
By the semantics of the NAND program, the value $z_i$ will correspond to the NAND of the values of the variables corresponding to $z_j$ and $z_k$.
Hence we see that every one of our constraints of the form $z_i = NAND(z_j,z_k)$ is satisfied,
and moreover since the final output is $1$, the last constraint is satisfied as well.
>
In the other direction, suppose that there is an assignment $z\in \{0,1\}^{m+n+1}$ s.t. $\psi(z)=1$, and let $x\in \{0,1\}^n$ s.t. $x_j = z_{n+1+j}$ for every $j\in \{0,\ldots,n-1\}$.
We claim that $P(x)=1$. Indeed note that, because $z$ satisfies all constraints of $\psi$, as we execute the program $P$ on $x$, the value assigned in the $i^{th}$ line is equal to $z_i$.
Hence in particular the value that is finally assigned to the output variable `y_0` will equal to $1$.

This claim means that the polynomial time map $P \mapsto \psi$ that transform a NAND program to a 3NAND formula satisfies that $NANDSAT(P)=3NAND(\psi)$ and hence this  is a reduction demonstrating $NANDSAT \leq_p 3NANT$ and concluding the proof of [threenand-thm](){.ref}.

## Concluding the proof of Cook-Levin

To conclude the proof of [cook-levin-thm](){.ref}, we need to show [threenand-sat-thm](){.ref}.
That is, to reduce $3NAND$ to $3SAT$. The reduction is actually quite simple.
Since $NAND(z,z') = \overline{z \wedge z'} = \overline{z}\vee\overline{z'}$,  the constraint
$$
z_i = NAND(z_j,z_k) \label{eq:NANDconstraint}
$$
is the same as
$$
 z_i \Rightarrow \left( \overline{z_j}\vee\overline{z_k} \right) \;\;\;\wedge\;\;\;  \left(\overline{z_j}\vee\overline{z_k} \right) \Rightarrow z_i
$$
where $\Rightarrow$ is the logical implication operator, defined as $a \Rightarrow b = \overline{a} \vee b$.

Hence [{eq:NANDconstraint}](){.eqref} is the same as
$$
 (\overline{z_i} \vee \overline{z_j} \vee\overline{z_k})  \; \wedge \;  ((z_j           \wedge   z_k)      \vee z_i )
$$
which is the same as
$$
 (\overline{z_i} \vee \overline{z_j} \vee\overline{z_k} ) \wedge          (z_i     \vee z_j )
         \wedge  (z_i     \vee z_k)
$$

Hence by replacing every $3NAND$ constraint of $\psi$ with three $3OR$ constraints as above we can transform a 3NAND formula $\psi$ to an equivalent 3CNF formula $\varphi$, thus completing the proof.^[The resulting forumula will have some of the OR's involving only two variables.  If we wanted to insist on each formula involving three distinct variables we can always add a "dummy variable" $z_{m+n+2}$ and include it in all the OR's involving only two variables. We leave it as an exercise to show that the new formula will be satisfiable if and only if the previous one was.]






## Lecture summary

* Many of the problems which we don't know polynomial-time algorithms for are $\mathbf{NP}$ complete, which means that finding a polynomial-time algorithm for one of them would imply a polynomial-time algorithm for _all_ of them.

* It is conjectured that $\mathbf{NP}\neq \mathbf{P}$ which means that we believe that polynomial-time algorithms  for these  problems are not merely _unknown_ but are _nonexistent_.

* While an $\mathbf{NP}$ hardness result means for example that a full fledged "textbook" solution to a problem such as MAX-CUT that is as clean and general as the algorithm for MIN-CUT probably does not exist, it does not mean that we need to give up whenever we see a MAX-CUT instance.                       Later in this course we will discuss several strategies to deal with $\mathbf{NP}$ hardness, including  _average-case complexity_ and _approximation algorithms_.




## Exercises

^[TODO: add exercises]

## Bibliographical notes

^[TODO: credit surveys of Avi, Madhu]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
