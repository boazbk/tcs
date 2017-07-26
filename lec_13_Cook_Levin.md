#  The Cook-Levin Theorem

In this lecture we prove one of the most important theorems in Computer Science:

> # {.theorem title="Cook-Levin Theorem" #cook-levin-thm}
$3SAT$ is $\mathbf{NP}$-complete.

The Cook-Levin Theorem is the underpinning to  a great web of reductions from 3SAT to thousands of problems across great many fields. Some problems that have been shown NP complete include: minimum-energy protein folding, minimum surface-area foam configuration, map coloring,    optimal Nash equilibrium, quantum state entanglement, minimum supersequence of a genome, minimum codeword problem, shortest vector in a lattice, minimum genus knots, positive Diophantine equations, integer programming, and many many more..
The worst-case complexity of all these problems is (up to polynomial factors) equivalent to that of 3SAT, and through the Cook-Levin Theorem, to all problems in $\mathbf{NP}$.

Since (as we have already observed before) $3SAT$ is obviously in $\mathbf{NP}$, to prove [cook-levin-thm](){.ref} we need to show that $F \leq_p 3SAT$ for every $F\in \mathbf{NP}$.
We will do so in three stages.
We define two intermediate problems: $NANDSAT$ and $3NAND$.
We will shortly show the definitions of these two problems, but
[cook-levin-thm](){.ref} will follow from the following three theorems:

> # {.theorem  #nand-thm}
$NANDSAT$ is $\mathbf{NP}$-complete.

> # {.theorem  #threenand-thm}
$NANDSAT \leq_p 3NAND$.

> # {.theorem  #threenand-sat-thm}
$3NAND \leq_p 3SAT$.

Together [nand-thm](){.ref}, [threenand-thm](){.ref}, and [threenand-sat-thm](){.ref} immediately imply that $3SAT$ is  $\mathbf{NP}$ complete (can you see why?), hence establishing [cook-levin-thm](){.ref}.
We now prove them one by one, providing the requisite definitions as we go along.

## The $NANDSAT$ Problem, and why it is $\mathbf{NP}$ complete.

We define the $NANDSAT$ problem as follows: its input is a NAND program $P$ (represented as a string as usual),
and we define $NANDSAT(P)=1$ if and only there is some input $x$ such that $P(x)=1$.
Since given $P$ and $x$, we can check in polynomial (in fact $\tilde{O}(|P|)$ time) whether $P(x)=1$, $NANDSAT$ is in $\mathbf{NP}$.
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

^[TODO: Add summary]


## Exercises

^[TODO: add exercises]

## Bibliographical notes

^[TODO: credit surveys of Avi, Madhu]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
