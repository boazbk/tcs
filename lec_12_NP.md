---
title: "Polynomial time reductions"
filename: "lec_12_NP"
chapternum: "13"
---

#  Polynomial-time reductions {#reductionchap }

> ### { .objectives }
* Introduce the notion of _polynomial-time reductions_ as a way to relate the complexity of problems to one another. \
* See several examples of such reductions. \
* 3SAT as a basic starting point for reductions.



Consider some of the problems we have encountered before:

* Finding the longest path in a graph

* Finding the maximum cut in a graph

* The 3SAT problem: deciding whether a given 3CNF formula has a satisfying assignment.

* Solving quadratic equations over $n$ variables $x_0,\ldots,x_{n-1} \in \R$.



All of these problems have the following properties:

* These are important problems, and people have spent significant effort on trying to find better algorithms for them.

* Each one of these is a _search_ problem, whereby we search for a solution that is "good" in some easy to define sense (e.g., a long path, a satisfying assignment, etc.).

* Each of these problems has a trivial exponential time algorithm that involve enumerating all possible solutions.

* At the moment, for all these problems the best known algorithm is not much faster than the trivial one in the worst case.


In this chapter and in [cooklevinchap](){.ref} we will see that, despite their apparent differences, we can relate the computational complexity of these and many other problems.
In fact, it turns out that the problem above are _computationally equivalent_, in the sense that solving one of them immediately implies solving the others.
This phenomenon, known as _$\mathbf{NP}$ completeness_, is one of the surprising discoveries of theoretical computer science, and we will see that it has far-reaching ramifications.

![In this chapter we show that if the $3SAT$ problem cannot be solved in polynomial time, then neither can the $QUADEQ$, $LONGESTPATH$, $ISET$ and $MAXCUT$ problems.  We do this by using the _reduction paradigm_ showing for example  "if pigs could whistle" (i.e., if we had an efficient algorithm for $QUADEQ$) then "horses could fly" (i.e., we would have an efficient algorithm for $3SAT$.)](../figure/reductionsoverview.png){#reductionsoverviewfig}





__Decision problems.__ For reasons of technical conditions rather than anything substantial, we will concern ourselves with _decision problems_ (i.e., Yes/No questions) or in other words _Boolean_  (i.e., one-bit output) functions.
We model the problems above as functions mapping $\{0,1\}^*$ to $\{0,1\}$ in the following way:

* The _3SAT_ problem can be phrased as the function $3SAT:\{0,1\}^* \rightarrow \{0,1\}$ that maps a 3CNF formula $\varphi$ to $1$ if there exists some assignment $x$ that satisfies it, and to $0$ otherwise. (We assume some representation of formulas as strings, and define the function to output $0$ if its input is not a valid representation; We will use the same convention for all the other functions below.)

* The _quadratic equations_ problem corresponds to the function $QUADEQ:\{0,1\}^* \rightarrow \{0,1\}$ that maps a set of quadratic equations $E$ to $1$ if there is an assignment $x$ that satisfies all equations, and to $0$ otherwise.

* The _longest path_ problem corresponds to the function $LONGPATH:\{0,1\}^* \rightarrow \{0,1\}$ that maps a graph $G$ and a number $k$ to $1$ if there is a simple path in $G$ of length at least $k$, and maps $(G,k)$ to $0$ otherwise. The longest path problem is a generalization of the well-known [Hamiltonian Path Problem](https://en.wikipedia.org/wiki/Hamiltonian_path_problem) of determining whether a path of length $n$ exists in a given $n$ vertex graph.

* The _maximum cut_ problem corresponds to the function $MAXCUT:\{0,1\}^* \rightarrow \{0,1\}$ that maps a graph $G$ and a number $k$ to $1$ if there is a cut in $G$ that cuts at least $k$ edges, and maps $(G,k)$ to $0$ otherwise.


Some other problems we  consider in this chapter include:

* The _independent set_ problem corresponds to the function $ISET:\{0,1\}^* \rightarrow \{0,1\}$ that on input a string representing a pair $(G,k)$ of a graph $G=(V,E)$ and a number $k$, outputs $1$ iff there exists a set $S \subseteq V$ such that $|V| = k$ and there are is no edge $\{u,v\} \in E$ with both $u$ and $v$ in $S$.

* The _zero-one equations_ problem corresponds to the function $01EQ:\{0,1\}^* \rightarrow \{0,1\}$ that gets a string representing  a set $E$ of linear equations with integer coefficients in variables $x_0, \ldots, x_{n-1}$ and outputs $1$ iff there is a Boolean assignment $x_0,\ldots,x_{n-1} \in \{0,1\}$ that satisfies all equations in $E$.

* The _subset sum_ problem corresponds to the function $SUBSETSUM : \{0,1\}^* \rightarrow \{0,1\}$ that gets a string representing a sequence $(A_0,\ldots,A_{n-1},T)$ of $n+1$ natural numbers, and outputs $1$ if and only if there exists a set $S \subseteq [n]$ such that $\sum_{i\in S} A_i = T$.




## Reductions

Suppose that $F,G:\{0,1\}^* \rightarrow \{0,1\}$ are two functions.
How can we show that they are "computationally equivalent"?
The idea is that we show that an efficient algorithm for $F$ would imply an efficient algorithm for $G$ and vice versa.
The key to this is the notion of a _reduction_.
Roughly speaking, we will say that _$F$ reduces to $G$_ (denoted as $F \leq_p G$) if $F$ is "no harder" than $G$, in the sense that a polynomial-time algorithm for $G$ implies a polynomial-time algorithm for $F$.
The formal definition is as follows:

> ### {.definition title="Reductions" #reduction-def}
Let $F,G:\{0,1\}^* \rightarrow \{0,1\}^*$. We say that _$F$ reduces to $G$_, denoted by $F \leq_p G$ if there is a polynomial-time computable $R:\{0,1\}^* \rightarrow \{0,1\}^*$ such that for every $x\in \{0,1\}^*$,
$$
F(x) = G(R(x)) \;. \label{eq:reduction}
$$
We say that $F$ and $G$ have _equivalent complexity_ if $F \leq_p G$ and $G \leq_p F$.

![If $F \leq_p G$ then we can transform a polynomial-time algorithm $B$  that computes $G$ into a polynomial-time algorithm $A$ that computes $F$. To compute $F(x)$ we can run the reduction $R$ guaranteed by the fact that $F \leq_p G$ to obtain $y=F(x)$ and then run our algorithm $B$ for $G$ to compute $G(y)$. ](../figure/reductiondescription.png){#reductionsfig .margin  }

::: {.solvedexercise title="Reductions and $\mathbf{P}$" #reductionsandP}
Prove that if $F \leq_p G$ and $G \in \mathbf{P}$ then $F\in \mathbf{P}$.
:::

::: { .pause }
As usual, solving this exercise on your own is an excellent way to make sure you understand [reduction-def](){.ref}. This exercise justifies the informal description of $F \leq_p G$ as saying that "$F$ is no harder than $G$."
:::

::: {.solution data-ref="reductionsandP"}
Suppose there was an algorithm $B$ that compute $F$ in time $p(n)$ where $p$ is its input size. Then, [eq:reduction](){.eqref} directly gives an algorithm  $A$ to compute $F$ (see [reductionsfig](){.ref}).
Indeed, on input $x\in \{0,1\}^*$, Algorithm $A$ will run the polynomial-time reduction $R$ to obtain $y=R(x)$ and then return $B(y)$.
By [eq:reduction](){.eqref}, $G(R(x)) = F(x)$ and hence Algorithm $A$ will indeed compute $F$.

We now show that $A$ runs in polynomial time.
By assumption, $R$ can be computed in time $q(n)$ for some polynomial $q$.
In particular, this means that  $|y| \leq q(|x|)$ (as just writing down $y$ takes $|y|$ steps).
This, computing $B(y)$  will take at most $p(|y|) \leq p(q(|x|))$ steps.
Thus the total running time of $A$ on inputs of length $n$ is at most the time to compute $y$, which is bounded by $q(n)$, and the time to compute $B(y)$, which is bounded by $p(q(n))$, and since the composition of two polynomials is a polynomial, $A$ runs in polynomial time.
:::

Since we think of  $F \leq_p G$ as saying that (as far as polynomial-time computation is concerned) $F$ is "easier or equal in difficulty to" $G$, we would expect that if $F \leq_p G$ and $G \leq_p H$, then it would hold that $F \leq_p H$. Indeed this is the case:

> ### {.lemma #transitivitylem}
For every $F,G,H :\{0,1\}^* \rightarrow \{0,1\}$, if $F \leq_p G$ and $G \leq_p H$ then $F \leq_p H$.

> ### { .pause }
We leave the proof of [transitivitylem](){.ref} as [transitivity-reductions-ex](){.ref}. Pausing now and doing this exercise is an excellent way to verify that you understood the definition of reductions.


::: {.remark title="Polynomial reductions, completeness and soundness" #polynomialred}
We have seen reductions before in the context of proving the uncomputability of problems such as $HALTONZERO$ and others.
The most crucial difference between the notion in [reduction-def](){.ref} and previously occuring notions is that in the context of relating the time complexity of problems, we need the reduction to be computable in _polynomial time_, as opposed to merely computable.
[reduction-def](){.ref} also restricts reductions to have a very specific format. That is, to show that $F \leq_p G$, rather than allowing a general algorithm for $F$ that uses a "magic box" that computes $G$, we only allow an algorithm that computes $F(x)$ by outputting $G(R(x))$. This restricted form is convenient for us, but people have defined and used more general reductions as well.

Since both $F$ and $G$ are Boolean functions, the condition $F(x)=G(R(x))$ in [eq:reduction](){.eqref} is equivalent to the following two implications: __(i)__ if $F(x)=1$ then $G(R(x))=1$, and __(ii)__ if $G(R(x))=1$ then $F(x)=1$.
Traditionally, condition __(i)__ is known as   _completness_ and condition __(ii)__ is known as _soundness_.
We can think of this as saying that the reduction $R$ is _complete_ if every $1$-input of $F$ (i.e. $x$ such that $F(x)=1$)  is mapped by $R$ to a $1$-input of $G$, and that it is _sound_ if no $0$-input of $F$ will ever be mapped to a $1$-input of $G$.
As we will see below, it is often the case that establishing __(ii)__ is the more challenging part.
:::



## Some example reductions

We will now use reductions to relate the computational complexity of the   problems mentioned above $-$ 3SAT, Quadratic Equations, Maximum Cut, and Longest Path.
We start by reducing 3SAT to the latter three problems, demonstrating that solving any one of them will solve 3SAT.
Along the way we will introduce one more problem: the _independent set_ problem.
Like the others, it shares the characteristics that it is an important and well-motivated computational problem, and that the best known algorithm for it takes exponential time.
In  [cooklevinchap](){.ref} we will show the other direction: reducing each one of these problems to 3SAT in one fell swoop.


![Our first stage in showing equivalence is to reduce 3SAT to the three other problems](../figure/sat_to_others.png){#freducesattothreeotherfig .margin  }


### Reducing 3SAT to quadratic equations

Let us now see our first example of a reduction.
Recall that in the _quadratic equation_ problem, the input is a list of $n$-variate polynomials $p_0,\ldots,p_{m-1}:\R^n \rightarrow \R$ that are all of [degree](https://en.wikipedia.org/wiki/Degree_of_a_polynomial) at most two (i.e., they are _quadratic_) and with integer coefficients. (The latter condition is for convenience and can be achieved by scaling.)
The task is to find out whether there is a solution $x\in \R^n$ to the equations $p_0(x)=0$, $p_1(x)=0$, $\ldots$, $p_{m-1}(x)=0$.

For example, the following is a set of quadratic equations over the variables $x_0,x_1,x_2$:
$$
\begin{aligned}
x_0^2 - x_0 &= 0 \\
x_1^2 - x_1 &= 0 \\
x_2^2 - x_2 &= 0 \\
1-x_0-x_1+x_0x_1    &= 0
\end{aligned}
$$
You can verify that $x \in \R^3$ satisfies this set of equations if and only if $x \in \{0,1\}^3$ and $x_0 \vee x_1 = 1$.



We will show how to reduce 3SAT to the problem of Quadratic Equations.

> ### {.theorem title="Hardness of quadratic equations" #quadeq-thm}
$$3SAT \leq_p QUADEQ$$
where $3SAT$ is the function that maps a 3SAT formula $\varphi$ to $1$ if it is satisfiable and to $0$ otherwise, and $QUADEQ$ is the function that maps a set $E$ of quadratic equations over $\{0,1\}^n$ to $1$ it has a solution and to $0$ otherwise.

> ### {.proofidea data-ref="quadeq-thm"}
At the end of the day, a 3SAT formula can be thought of as a list of equations on some variables $x_0,\ldots,x_{n-1}$.
Namely, the equations are that each of the $x_i$'s should be equal to either $0$ or $1$, and that the variables should satisfy some set of constraints which corresponds to the OR of three variables or their negation.
To show that $3SAT \leq_p QUADEQ$ we need to give a polynomial-time reduction that maps a 3SAT formula $\varphi$ into a set of quadratic equations $E$ such that $E$ has a solution if and only if $\varphi$ is satisfiable.
The idea is that we can transform a 3SAT formula $\varphi$ first to a set of _cubic_ equations by mapping every constraint of the form $(x_{12} \vee  \overline{x}_{15} \vee x_{24})$ into an equation of the form $(1-x_{12})x_{15}(1-x_{24})=0$. We can then turn this into a _quadratic equation_ by mapping any cubic equation of the form $x_ix_jx_k =0$ into the two quadratic equations $y_{i,j}=x_ix_j$ and $y_{i,j}x_k=0$.

::: {.proof data-ref="quadeq-thm"}
To prove [quadeq-thm](){.ref} we need to give a   polynomial-time transformation of every 3SAT formula $\varphi$ into a set of quadratic equations $E$, and prove that $3SAT(\varphi)=QUADEQ(E)$.

We now describe the transformation of a formula $\varphi$ to equations $E$ and show the completeness and soundness conditions.
Recall that a _3SAT formula_ $\varphi$ is a formula such as $(x_{17} \vee \overline{x}_{101} \vee x_{57}) \wedge ( x_{18} \vee \overline{x}_{19} \vee \overline{x}_{101}) \wedge \cdots$.
That is, $\varphi$ is composed of the AND of $m$ _3SAT clauses_ where a 3SAT clause is the OR of three variables or their negation.
A _quadratic equations_ instance $E$ is composed of a list of equations, each of involving a sum of variables or their products, such as $x_{19}x_{52} - x_{12} + 2x_{33} = 2$, etc.. We will include the constraints $x_i^2-x_i=0$ for every $i\in [n]$ in our equations, which means that we can restrict attention to assignments where $x_i \in \{0,1\}$ for every $i$.

There is a natural way to map a 3SAT instance into a set of _cubic_ equations $E'$, and that is to map a clause such as $(x_{17} \vee \overline{x}_{101} \vee x_{57})$ (which is equivalent to the negation of $\overline{x}_{17} \wedge x_{101} \wedge \overline{x}_{57}$) to the equation $(1-x_{17})x_{101}(1-x_{57})=0$.
Therefore, we can map a formula $\varphi$  with $n$ variables $m$ clauses into a set $E'$ of $m+n$ cubic equations on $n$ variables (that is, one equation per each clause, plus one equation of the form $x_i^2-x_i=0$ for each variable to ensure that its value is in $\{0,1\}$) such that every assignment $a\in \{0,1\}^n$ to the $n$ variables satisfies the original formula if and only if it satisfies the equations of $E'$.


To make the equations _quadratic_ we introduce for every two distinct $i,j \in [n]$  a variable $y_{i,j}$ and include the constraint $y_{i,j}-x_ix_j=0$ in the equations.
This is a quadratic equation that ensures that $y_{i,j}=x_ix_j$ for every such $i,j\in [n]$.
Now we can turn any cubic equation in the $x$'s into a quadratic equation in the $x$ and $y$ variables.
For example, we can "open up the parentheses" of an equation such as $(1-x_{17})x_{101}(1-x_{57})=0$ to $x_{101} -x_{17}x_{101}-x_{101}x_{57}+x_{17}x_{101}x_{57}=0$.
We can now replace the cubic term $x_{17}x_{101}x_{57}$ with the quadratic term $y_{17,101}x_{57}$.
This can be done for every cubic equation in the same way, replacing any cubic term $x_ix_jx_k$ with the term $y_{i,j}x_k$.
The end result will be a set of $m+n+\binom{n}{2}$ equations (one equation per clause, one equation per variable to ensure $x_i^2-x_i=0$, and one equation per pair $i,j$ to ensure $y_{i,j}=x_ix_j=0$) on the $n + \binom{n}{2}$ variables $x_0,\ldots,x_{n-1}$ and $y_{i,j}$ for all pairs of distinct variables $i,j$.^[$\binom{n}{2} = \tfrac{1}{2}n(n-1)$ is the number of all size two subsets of $[n]$. We consider $\{i,j\}$ to be the same as $\{j,i\}$ since $x_ix_j = x_jx_i$ for every $i,j$.]

To complete the proof we need to show that if we transform $\varphi$ to $E$ in this way then the 3SAT formula $\varphi$ is satisfiable if and only if the equations $E$ have a solution.
This is essentially immediate from the construction, but as this is our first reduction, we spell this out fully:

* __Completeness:__ We claim that if  $\varphi$ is satisfiable then the equations $E$ have a solution. To prove this we need to show how to transform a satisfying assignment $a\in \{0,1\}^n$ to the variables of $\varphi$ (that is, $a_i$ is the value assigned to $x_i$) to a solution to the variables of $E$. Specifically, if $a\in \{0,1\}^n$ is such an assignment then by design $a$ satisfies all the _cubic_ equations $E'$ that we constructed above. But then, if we assign to the $n+\binom{n}{2}$ variables the values $a_0,\ldots,a_{n-1}$ and $\{ a_ia_j \}$ for all $\{i,j\} \subseteq [n]$ then by construction this will satisfy all the quadratic equations of $E$ as well.

* __Soundness:__ We claim that if the equations $E$ have a solution then $\varphi$ is satisfiable. Indeed, suppose that $z \in \R^{n + \binom{n}{2}}$ is a solution to the equations $E$. A priori $z$ could be any vector of $n+ \binom{n}{2}$ numbers, but the fact that $E$ contains the equations $x_i^2 - x_i =0$ and $y_{i,j} - x_ix_j = 0$ means that if $z$ satisfies these equations then the values it assigns to $x_i$ must be in $\{0,1\}$ for every $i$, and the value it assigns to $y_{i,j}$ must be $x_ix_j$ for every $\{i,j\} \subseteq [n]$.
Therefore by the way we constructed our equations, the value assigned $x$ must be a solution of the original cubic equations $E'$ and hence also of the original formula $\varphi$, which in particular implies $\varphi$ is satisfiable.

This reduction can be easily implemented in about a dozen lines of Python or any other programming language, see [sattoqefig](){.ref}.
:::

![Reducing 3SAT to satisfiability of quadratic equations. On the righthand side is Python code implementing the reduction of [quadeq-thm](){.ref} and on the lefthand side is the output of this reduction on an example 3SAT instance. ](../figure/SAT2QE.png){#sattoqefig .margin  }



## The independent set problem

For a graph $G=(V,E)$, an [independent set](https://en.wikipedia.org/wiki/Independent_set_(graph_theory)) (also known as a _stable set_) is a subset $S \subseteq V$ such that there are no edges with both endpoints in $S$ (in other words, $E(S,S)=\emptyset$).
Every "singleton" (set consisting of a single vertex) is trivially an independent set, but finding larger independent sets can be challenging.
The _maximum independent set_ problem (henceforth simply "independent set") is the task of finding the largest independent set in the graph.
The independent set problem is naturally related to _scheduling problems_: if we put an edge between two conflicting tasks,  then an independent set corresponds to a set of tasks that can all be scheduled together without conflicts.
But it also arises in very different settings, including trying to find structure in [protein-protein interaction graphs](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3919085/).




To phrase independent set as a decision problem, we think of it as a function $ISET:\{0,1\}^* \rightarrow \{0,1\}$ that on input a graph $G$ and a number $k$ outputs $1$ if and only if the graph $G$ contains an independent set of size at least $k$.
We will now reduce 3SAT to Independent set.

> ### {.theorem title="Hardness of Independent Set" #isetnpc}
$3SAT \leq_p ISET$.

> ### {.proofidea data-ref="isetnpc"}
The idea is that finding a satisfying assignment to a 3SAT formula corresponds to satisfying many local constraints without creating any conflicts. One can think of "$x_{17}=0$"  and "$x_{17}=1$" as two conflicting events, and of the constraints $x_{17} \vee \overline{x}_5 \vee x_9$ as creating a conflict between the events "$x_{17}=0$", "$x_5=1$" and "$x_9=0$", saying that these three cannot simultaneosly co-occur. Using these ideas, we can we can think of solving a 3SAT problem as trying to schedule non conflicting events, though the devil is, as usual, in the details.

::: {.proof data-ref="isetnpc"}
Given a 3SAT formula $\varphi$ on $n$ variables and with $m$ clauses, we will create a graph $G$ with $3m$ vertices as follows: (see [threesattoisfig](){.ref} for an example)



* A clause $C$ in $\varphi$ has the form $C = y \vee y' \vee y''$  where $y,y',y''$ are _literals_ (variables or their negation). For each such clause $C$, we will add three vertices to $G$, and label them  $(C,y)$, $(C,y')$, and $(C,y'')$ respectively. We will also add the three edges between all pairs of these vertices, so they form a _triangle_. Since there are $m$ clauses in $\varphi$, the graph $G$ will have $3m$ vertices.

* In addition to the above edges, we also add an edge between every pair vertices of the form $(C,y)$ and $(C',y')$ where $y$ and $y'$ are _conflicting_ literals. That is, we add an edge between $(C,y)$ and $(C,y')$  if there is an $i$ such that $y=x_i$ and $y' = \overline{x}_i$ or vice versa.


The above construction of $G$ based on $\varphi$ can clearly be carried out in polynomial time.
Hence to prove the theorem we need to show that  $\varphi$ is satisfiable if and only if $G$ contains an independent set of $m$ vertices. We now show both directions of this equivalence:

__Part 1: Completeness.__ The "completeness" direction is to show that if $\varphi$ has a satisfying assignment $x^*$, then $G$ has an independent set $S^*$ of  $m$ vertices. Let us now show this.

Indeed, suppose that $\varphi$ has a satisfying assignment $x^* \in \{0,1\}^n$.  Then for every clause $C = y \vee y' \vee y''$ of $\varphi$, one of the literals $y,y',y''$ must evaluate to _true_ under the assignment $x^*$ (as otherwise it would not satisfy $\varphi$). We let $S$ be a set of $m$ vertices that is obtained by choosing for every clause $C$ one vertex of the form $(C,y)$ such that $y$ evaluates to true under $x^*$. (If there is more than one such vertex for the same $C$, we arbitrarily choose one of them.)

We claim that $S$ is an independent set. Indeed, suppose otherwise that there was a pair of vertices $(C,y)$ and $(C',y')$ in $S$ that have an edge between them. Since we picked one vertex out of each triangle corresponding to a clause, it must be that $C \neq C'$. Hence the only way that there is an edge between $(C,y)$ and $(C,y')$ is if $y$ and $y'$ are conflicting literals (i.e. $y=x_i$ and $y'=\overline{x}_i$ for some $i$). But that would that they can't both evaluate to _true_ under the assignment $x^*$, which contradicts the way we constructed the set $S$. This completes the proof of the completeness condition.

__Part 2: Soundness.__ The "soundness" direction is to show that if $G$ has an independent set $S^*$ of $m$ vertices, then $\varphi$ has a satisfying assignment $x^* \in \{0,1\}^n$. Let us now show this.

Indeed, suppose that $G$ has an independent set $S*$ with $m$ vertices.
We will define an assignment $x^* \in \{0,1\}^n$  for the variables of $\varphi$ as follows. For every $i\in [n]$, we set $x^*_i$ according to the following rules:

* If $S^*$ contains a vertex of the form $(C,x_i)$ then we set $x^*_i=1$.

* If $S^*$ contains a vertex of the form $(C,\overline{x_i})$ then we set $x^*_i=0$.

* If $S^*$ does not contain a vertex of either of these forms, then it does not matter which value we give to $x^*_i$, but for concreteness we'll set $x^*_i=0$.

The first observation is that $x^*$ is indeed well defined, in the sense that the rules above do not conflict with one another, and ask to set $x^*_i$ to be both $0$ and $1$. This follows from the fact that $S^*$ is an _independent set_ and hence if it contains a vertex of the form $(C,x_i)$ then it cannot contain a vertex of the form $(C',\overline{x_i})$.

We now claim that $x^*$ is a satisfying assignment for $\varphi$. Indeed, since $S^*$ is an independent set, it cannot have more than one vertex inside each one of the $m$ triangles $(C,y),(C,y'),(C,y'')$ corresponding to a clause of $\varphi$.
Hence since $|S^*|=m$, it must have exactly one vertex in each such triangle. For every clause $C$ of $\varphi$, if $(C,y)$ is the vertex in $S^*$ in the triangle corresponding to $C$, then by the way we defined $x^*$, the literal $y$ must evaluate to _true_, which means that $x^*$ satisfies this clause.
Therefore $x^*$ satisfies all clauses of $\varphi$, which is the definition of a satisfying assignment.

This completes the proof of [isetnpc](){.ref}
:::


![The reduction of 3SAT to Independent Set. On the righthand side is _Python_ code that implements this reduction. On the lefthand side is a sample output of the reduction. We use black for the "triangle edges" and red for the "conflict edges". Note that the satisfying assignment $x^* = 0110$ corresponds to the independent set $(0,\neg x_3)$, $(1, \neg x_0)$, $(2,x_2)$.](../figure/3sat2ISreduction.png){#threesattoisfig .margin  }



::: {.solvedexercise title="Clique is equivalent to independent set" #iscliqueex}
The [maximum clique problem](https://en.wikipedia.org/wiki/Clique_problem) corresponds to the function $CLIQUE:\{0,1\}^* \rightarrow \{0,1\}$ such that for a graph $G$ and a number $k$, $CLIQUE(G,k)=1$ iff there is a $S$ subset of $k$ vertices  such that for _every_ distinct $u,v \in S$, the edge $u,v$ is in $G$. Such a set is known as a _clique_.

Prove that $CLIQUE \leq_p ISET$ and $ISET \leq_p CLIQUE$.
:::


::: {.solution data-ref="iscliqueex"}
If $G=(V,E)$ is a graph, we denote by $\overline{G}$ its _complement_  which is the graph on the same vertices $V$ and such that for every distinct $u,v \in V$, the edge $\{u,v\}$ is present in $\overline{G}$ if and only if this edge is _not_ present in $G$.

This means that for every set $S$, $S$ is an independent set in $G$ if and only if $S$ is a _clique_ in $\overline{S}$. Therefore for every $k$, $ISET(G,k)=CLIQUE(\overline{G},k)$.
Since the map $G \mapsto \overline{G}$ can be computed efficiently, this yields a reduction $ISET \leq_p CLIQUE$.
Moreover, since $\overline{\overline{G}}=G$ this yields a reduction in the other direction as well.
:::





## Reducing Independent Set to Maximum Cut

> ### {.theorem title="Hardness of Max Cut" #isettomaxcut}
$ISET \leq_p MAXCUT$

> ### {.proofidea data-ref="isettomaxcut"}
We will map a graph $G$ into a graph $H$ such that a large independent set in $G$ becomes a partition cutting many edges in $H$. We can think of a cut in $H$ as coloring each vertex either "blue" or  "red". We will add a special "source" vertex $s^*$, connect it to all other vertices, and assume without loss of generality that it is colored blue. Hence the more vertices we color red, the more edges from $s^*$ we cut. Now, for every edge $u,v$  in the original graph $G$ we will add a special "gadget" which will be a small subgraph that involves $u$,$v$, the source $s^*$, and two other additional vertices. We design the gadget in a way so that if the red vertices are not an independent set in $G$ then the corresponding cut in $H$ will be "penalized" in the sense that it would not cut as many edges. Once we set for ourselves this objective, it is not hard to find a gadget that achieves it$-$ see the proof below.


::: {.proof data-ref="isettomaxcut"}
We will transform a graph $G$ of $n$ vertices and $m$ edges into a graph $H$ of $n+1+2m$ vertices and $n+5m$ edges in the following way:  the graph $H$ will contain all vertices of $G$ (though not the edges between them!) and in addition to that will contain: \
* A special vertex $s^*$ that is connected to all the vertices of $G$ \
* For every edge $e=\{u,v\} \in E(G)$, two vertices $e_0,e_1$ such that $e_0$ is connected to $u$ and $e_1$ is connected to $v$, and moreover we add the edges $\{e_0,e_1 \},\{ e_0,s^* \},\{e_1,s^*\}$ to $H$.

[isettomaxcut](){.ref} will follow by showing that $G$ contains an independent set of size at least $k$ if and only if $H$ has a cut cutting at least $k+4m$ edges. We now prove both directions of this equivalence:


__Part 1: Completeness.__ If $I$ is an independent $k$-sized set in $G$, then we can define $S$ to be a cut in $H$ of the following form: we let $S$ contain all the vertices of $I$ and for every edge $e=\{u,v \} \in E(G)$, if $u\in I$ and $v\not\in I$ then we add $e_1$ to $S$; if $u\not\in I$ and $v\in I$ then we add $e_0$ to $S$; and if $u\not\in I$ and $v\not\in I$ then we add both $e_0$ and $e_1$ to $S$. (We don't need to worry about the case that both $u$ and $v$ are in $I$ since it is an independent set.) We can verify that in all cases the number of edges from $S$ to its complement in the gadget corresponding to $e$ will be four (see [ISETtoMAXCUTfig](){.ref}). Since $s^*$ is not in $S$, we also have $k$ edges from $s^*$ to $I$, for a total of $k+4m$ edges.


__Part 2: Soundness.__ Suppose that $S$ is a cut in $H$ that cuts at least $C=k+4m$ edges. We can assume that $s^*$ is not in $S$ (otherwise we can "flip" $S$ to its complement $\overline{S}$, since this does not change the size of the cut). Now let $I$ be the set of vertices in $S$ that correspond to the original vertices of $G$. If $I$ was an independent set of size $k$ then would be done. This might not always be the case but we will see that if $I$ is not an independent set then its also larger than $k$. Specifically, we define $m_{in}=|E(I,I)|$ be the set of edges in $G$ that are contained in $I$ and let $m_{out}=m-m_{in}$ (i.e., if $I$ is an independent set then $m_{in}=0$ and $m_{out}=m$). By the properties of our gadget we know that for every edge $\{u,v\}$ of $G$, we can cut at most three edges when both $u$ and $v$ are in $S$, and at most four edges otherwise. Hence the number $C$ of edges cut by $S$   satisfies $C \leq |I| + 3m_{in}+4m_{out} = |I|+ 3m_{in} + 4(m-m_{in})=|I|+4m-m_{in}$. Since $C = k +4m$ we get that $|I|-m_{in} \geq k$. Now we can transform $I$ into an independent set $I'$ by going over every one of the $m_{in}$ edges that are inside $I$ and removing one of the endpoints of the edge from it. The resulting set $I'$ is an independent set in the graph $G$ of size $|I|-m_{in} \geq k$ and so this concludes the proof of the soundness condition.
:::


![In the reduction of independent set to max cut, we have a "gadget" corresponding to every edge $e=\{u,v\}$ in the original graph. If we think of the side of the cut containing the special source vertex $s^*$ as "blue" and the other side as "red", then the leftmost and center figures show that if $u$ and $v$ are not both red then we can cut four edges from the gadget. In contrast, by enumerating all possibilities one can verify that if both $u$ and $v$ are red, then no matter how we color the intermediate vertices $e_0,e_1$, we will cut at most three edges from the gadget.  ](../figure/ISETtoMAXCUT.png){#ISETtoMAXCUTfig .margin  }


![The reduction of independent set to max cut. On the righthand side is Python code implementing the reduction. On the lefthand side is an example output of the reduction where we apply it to the independent set instance that is obtained by running the reduction of [isetnpc](){.ref} on the 3CNF formula $(x_0 \vee \overline{x}_3 \vee x_2) \wedge (\overline{x}_0 \vee x_1 \vee \overline{x}_2) \wedge (\overline{x}_1 \vee x_2 \vee x_3)$.](../figure/is2maxcut.png){#isettomaxcutcodefig .margin  }

## Reducing 3SAT to Longest Path

^[This section is still a little messy, feel free to skip it or just read it without going into the proof details]

One of the most basic algorithms in Computer Science is Dijkstra's algorithm to find the _shortest path_ between two vertices.
We now show that in contrast, an efficient algorithm for the _longest path_ problem would imply a polynomial-time algorithm for 3SAT.

> ### {.theorem title="Hardness of longest path" #longpaththm}
$$3SAT \leq_p LONGPATH$$

> ### {.proofidea data-ref="longpaththm"}
To prove [longpaththm](){.ref} need to show how to transform a 3CNF formula $\varphi$ into a graph $G$ and two vertices $s,t$ such that $G$ has a path of length at least $k$ if and only if $\varphi$ is satisfiable.
The idea of the reduction is sketched in [longpathfig](){.ref} and [longpathfigtwo](){.ref}.
We will construct a graph that contains a potentially long "snaking path" that corresponds to all variables in the formula.
We will add a "gadget" corresponding to each clause of $\varphi$ in a way that we would only be able to use the gadgets if we have a satisfying assignment.


> ### {.proof data-ref="longpaththm"}
We build a graph $G$ that "snakes" from $s$ to $t$ as follows.
After $s$ we add a sequence of $n$ long loops.
Each loop has an "upper path" and a "lower path".
A simple path cannot take both the upper path and the lower path, and so it will need to take exactly one of them to reach $s$ from $t$.
>
Our intention is that a path in the graph will correspond to an assignment $x\in \{0,1\}^n$ in the sense that taking the upper path in the $i^{th}$ loop corresponds to assigning $x_i=1$ and taking the lower path corresponds to assigning $x_i=0$.
When we are done snaking through all the $n$  loops corresponding to the variables to reach $t$ we need to pass through $m$ "obstacles":
for each clause $j$ we will have a small gadget consisting of a pair of vertices $s_j,t_j$ that have three paths between them.
For example, if the $j^{th}$ clause had the form $x_{17} \vee \overline{x}_{55} \vee x_{72}$ then one path would go through a vertex in the lower loop corresponding to $x_{17}$, one path would go through a vertex in the upper loop corresponding to $x_{55}$ and the third would go through the lower loop corresponding to $x_{72}$.
We see that if we went in the first stage according to a satisfying assignment then we will be able to find a free vertex to travel from $s_j$ to $t_j$.
We link $t_1$ to $s_2$, $t_2$ to $s_3$, etc and link $t_m$ to $t$.
Thus a satisfying assignment would correspond to a path from $s$ to $t$ that goes through one path in each loop corresponding to the variables, and one path in each loop corresponding to the clauses.
We can make the loop corresponding to the variables long enough so that we must take the entire path in each loop in order to have a fighting chance of getting a path as long as the one corresponds to a satisfying assignment.
But if we do that, then the only way if we are able to reach $t$ is if the paths we took corresponded to a satisfying assignment, since otherwise we will have one clause $j$ where we cannot reach $t_j$ from $s_j$ without using a vertex we already used before.



![We can transform a 3SAT formula $\varphi$ into a graph $G$ such that the longest path in the graph $G$ would correspond to a satisfying assignment in $\varphi$. In this graph, the black colored part corresponds to the variables of $\varphi$ and the blue colored part corresponds to the vertices. A sufficiently long path would have to first "snake" through the black part, for each variable choosing either the "upper path" (corresponding to assigning it the value `True`) or the "lower path" (corresponding to assigning it the value `False`). Then to achieve maximum length the path would traverse through the blue part, where to go between two vertices corresponding to a clause such as $x_{17} \vee \overline{x}_{32} \vee x_{57}$, the corresponding vertices would have to have been not traversed before. ](../figure/3sat_longest_path_red_without_path.png){#longpathfig .margin  }


![The graph above with the longest path marked on it, the part of the path corresponding to variables is in green and part corresponding to the clauses is in pink.](../figure/3sat_to_longest_path_reduction.png){#longpathfigtwo .margin  }



::: { .recap }
* The computational complexity of many seemingly unrelated computational problems can be related to one another through the use of _reductions_.

* If $F \leq_p G$ then a polynomial-time algorithm for $G$ can be transformed into a polynomial-time algorithm for $F$.

* Equivalently, if $F \leq_p G$ and $F$ does _not_ have a polynomial-time algorithm then neither does $G$.

* We've developed many techniques to show that $3SAT \leq_p F$ for interesting functions $F$.  Sometimes we can do so by using _transitivity_ of reductions: if $3SAT \leq_p G$ and $G \leq_p F$ then $3SAT \leq_p F$.
:::

## Exercises

^[TODO: Maybe mention either in exercise or in body of the lecture some NP hard results motivated by science. For example, shortest superstring that is motivated by genome sequencing, protein folding, maybe others.]


> ### {.exercise  #product-ex}
Prove [product-lem](){.ref}

> ### {.exercise title="Transitivity of reductions" #transitivity-reductions-ex}
Prove that if $F \leq_p G$ and $G \leq_p H$ then $F \leq_p H$.


## Bibliographical notes


Several notions of reductions are defined in the literature. The notion defined in [reduction-def](){.ref}  is often known as a _mapping reduction_, _many to one reduction_ or a _Karp reduction_.

The _maximal_ (as opposed to _maximum_) independent set  is the task of finding a "local maximum" of an independent set: an independent set $S$ such that one cannot add a vertex to it without losing the independence property (such a set is known as a _vertex cover_). Unlike finding a _maximum_ independent set, finding a _maximal_ independent set can be done efficiently by a greedy algorithm, but this local maximum can be much smaller than the global maximum.


Reduction of independent set to max cut taken from [these notes](https://people.engr.ncsu.edu/mfms/Teaching/CSC505/wrap/Lectures/week14.pdf). Image of Hamiltonian Path through Dodecahedron by [Christoph Sommer](https://commons.wikimedia.org/wiki/File:Hamiltonian_path.svg).



