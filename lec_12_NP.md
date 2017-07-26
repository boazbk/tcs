#  NP and NP completeness

>_"In this paper we give theorems that suggest, but do not imply, that these problems, as well as many others, will remain  intractable perpetually"_, Richard Karp, 1972


Let us consider several of the problems we have encountered before:

* Finding the longest path in a graph
* Finding the maximum cut in a graph
* The 3SAT problem
* Solving quadratic equations

All of these have the following properties:

* These are important problems, and people have spent significant effort on trying to find better algorithms for them.

* They have trivial exponential time algorithms that involve enumerating all possible solutions.

* At the moment the best known algorithms are not much better than the trivial one in the worst-case.

In this lecture we will see that, despite their apparent differences, all these problems are _computationally equivalent_, in the sense that solving one of them immediately implies solving the others.
This phenomenon, known as _$\mathbf{NP}$ completeness_, is one of the surprising discoveries of theoretical computer science, and we will see that it has far-reaching ramifications.

### Decision problems

For reasons of technical conditions rather than anything substantial, we will concern ourselves in this lecture with _decision problems_ or _Boolean functions_.
Thus, we will model all the problems as functions mapping $\{0,1\}^*$ to $\{0,1\}$:

* The _3SAT_ problem corresponds to the function $3SAT$ that maps a 3CNF formula $\varphi$ to $1$ if there exists some assignment $x$ that satisfies it and to $0$ otherwise.

* The _quadratic equations_ problem  corresponds to the function $QUADEQ$ that maps a set of quadratic equations $E$ to $1$ if there is an assignment $x$ that satisfies all equations and to $0$ otherwise.

* The _longest path_ problem corresponds to the function $LONGPATH$ that maps a graph $G$ and a number $k$ to $1$ if there is a simple path in $G$ of length at least $k$ and maps $(G,k)$ to $0$ otherwise.

* The _maximum cut_ problem corresponds to the function $MAXCUT$ that maps a graph $G$ and a number $k$ to $1$ if there is a cut in $G$ that cuts at least $k$ edges and maps $(G,k)$ to $0$ otherwise.


## Reductions

Suppose that $F,G:\{0,1\}^* \rightarrow \{0,1\}$ are two functions.
How can we show that they are "computationally equivalent"?
The idea is that we show that an efficient algorithm for $F$ would imply an efficient algorithm for $G$ and vice versa.
The key to this is the notion of a _reduction_:

> # {.definition title="Reductions" #reduction-def}
Let $F,G:\{0,1\}^* \rightarrow \{0,1\}^*$. We say that _$F$ reduces to $G$_, denoted by $F \leq_p G$ if there is a polynomial-time computable $R:\{0,1\}^* \rightarrow \{0,1\}^*$ such that for every $x\in \{0,1\}^*$,
$$
F(x) = G(R(x)) \;. \label{eq:reduction}
$$
We say that $F$ and $G$ have _equivalent complexity_ if $F \leq_p G$ and $G \leq_p H$.

If $F \leq_p G$ and $G$ is computable in polynomial time, then $F$ is computable in polynomial time as well.
Indeed, [eq:reduction](){.eqref} shows a way how to compute $F$ by applying the polynomial-time reduction $R$ and then the  polynomial-time algorithm  for computing $F$.

## Some example reductions

We will now  use reductions to  show that the  problems above- 3SAT, Quadratic Equations, Maximum Cut, and Longest Path- are indeed computationally equivalent to one another.
We start by  reducing 3SAT to the latter three problems, demonstrating that solving either of them will solve it 3SAT.

![Our first stage in showing equivalence is to reduce  3SAT to the  three other problems](../figure/sat_to_others.png){#figureid .class width=300px height=300px}


## Reducing 3SAT to quadratic equations

Let us now see our first example of a reduction.
We will show how to reduce 3SAT to the problem of Quadratic Equations.

> # {.theorem title="Hardness of quadratic equations" #quadeq-thm}
$$3SAT \leq_p QUADEQ$$
where $3SAT$ is the function that maps a 3SAT formula $\varphi$ to $1$ if it is satisfiable and to $0$ otherwise, and $QUADEQ$ is the function that maps a set $E$ of quadratic equations over $\{0,1\}^n$ to $1$ if its satisfiable and to $0$ otherwise.

To do so, we need to give a polynomial-time transformation of every 3SAT formula $\varphi$ into a set of quadratic equations $E$.
Recall that a _3SAT formula_ $\varphi$ is a formula such as $(x_{17} \vee \overline{x}_{101} \vee x_{57}) \wedge ( x_{18} \vee \overline{x}_{19} \vee \overline{x}_{101}) \vee \cdots$.
That is, $\varphi$ is composed of the AND of $m$ _3SAT clauses_ where a 3SAT clause is the OR of three variables or their negation.
A _quadratic equations_  instance $E$, is composed of a list of equations, each of involving a sum of variables or their products, such as $x_{19}x_{52} - x_{12} + 2x_{33} = 2$, etc..
Recall that we restrict attention to $\{0,1\}$ valued variables for simplicity (or, equivalently, assume that the instance contains the equations $x_i^2 - x_i = 0$ for every $i$. )

There is a natural way to map a 3SAT instance into a set of equations, and that is to map a clause such as $(x_{17} \vee \overline{x}_{101} \vee x_{57})$ to the equation $(1-x_{17})x_{101}(1-x_{57})=0$.
We can  map a formula $\varphi$ with $m$ clauses into a set $E$ of $m$ such equations such that there is an $x$ with $\varphi(x)=1$ if and only if there is an assignment to the variables that satisfies all the equations of $E$.
The problem is that the equations in $E$ will not be quadratic but _cubic_: they contain terms of degree three.
So, to finish the reduction it will suffice to show that we can map any set of cubic equations $E$ into a set of _quadratic_ equations $E'$ such that $E$ is satisfiable if and only if $E'$ is.

The idea is that for every two variables $x_i$ and $x_j$, we add an extra variables $y_{i,j}$ and $z_{i,j}$ and a set of quadratic equations  that, if satisfied, guarantee that $y_{i,j} = x_i x_j$.
Once we do that, we can replace cubic terms of the form $x_ix_jx_k$ with the quadratic term $y_{i,j}x_k$ in the new variables. We can do so by adding the following equations

$$
\begin{aligned}
x_iy_{i,j} - y_{i,j} &= 0 \\
x_jy_{i,j} - y_{i,j} &= 0 \\
y_{i,j} + 1 - x_i - x_j - z_{i,j} &= 0
\end{aligned}
$$

Note that this system can be satisfied by setting $y_{i,j} = x_ix_j$ and $z_{i,j}=(1-x_i)(1-x_j)$.
It turns out this is the only solution

> # {.lemma #product-lem}
Every assignment to $\{ x_i,x_j,y_{i,j},z_{i,j} \}$ that satisfies the equations above must satisfy $y_{i,j}=x_ix_j$

We leave proving [product-lem](){.ref} as [product-ex](){.ref}.
Using this lemma, we can transform the cubic system $E$ in the variables $\{ x_i\}_{i \in [n]}$ to an equivalent quadratic system $E'$ in the variables $\{ x_i, y_{i,j}, z_{i,j} \}_{i,j \in [n]}$.
Note that the transformation (which involves a simple translation of every 3SAT clause to a constant number of equations) can be easily carried out in polynomial (in fact linear) time.
Since the original system was equivalent to the 3SAT instance it is not hard to see that we get:

* __(Completeness)__ If $\varphi$ has a satisfying assignment $x$ then $E'$ has a satisfying assignments $(x,y,z)$.
* __(Soundness)__ If $E'$ has a satisfying assignment $(x,y,z)$ then $\varphi$ has a satisfying assignment.

Thus if we define $E' = R(\varphi)$, then we see that for every 3SAT formula $\varphi$, $3SAT(\varphi) = QUADEQ(R(\varphi))$, showing that $3SAT \leq_p QUADEQ$ and completing the proof of [quadeq-thm](){.ref}.


## Reducing 3SAT to Maximum Cut

^[Add reduction here]

## Reducing 3SAT to Longest Path

The two reductions above might not have seemed so surprising, since quadratic equations and max cut are at least somewhat similar to 3SAT in the sense that they are _constraint satisfaction problems_, which are about trying to find an assignment $x\in \{0,1\}^n$ (or equivalently a set $S\subseteq [n]$) that satisfies as many local constraints (such as quadratic equations or cutting edges) as possible.
But we will now show that 3SAT reduces the the _longest path_ problem as well, which seems to be of a different nature.

> # {.theorem title="Hardness of longest path" #longpath-thm}
$$3SAT \leq_p LONGPATH$$

To prove [longpath-thm](){.ref} need to show how to transform a 3CNF formula $\varphi$ into a graph $G$ and two vertices $s,t$ such that $G$ has a path of length at least $k$ if and only if $\varphi$ is satisfiable.
The idea of the reduction is sketched in [longpathfig](){.ref} and [longpathfigtwo](){.ref}.
We build a graph $G$ that "snakes" from $s$ to $t$ as follows.
After $s$ we add a sequence of $n$ long loops.
Each loop has an "upper path" and a "lower path".
A simple path cannot take both the upper path and the lower path, and so it will need to take exactly one of them to reach $s$ from $t$.

Our intention is that a path in the graph will correspond to an assignment $x\in \{0,1\}^n$ in the sense that taking the upper path in the $i^{th}$ loop corresponds to assigning $x_i=1$ and taking the lower path corresponds to assigning $x_i=0$.
When we are done snaking through all the $n$  loops corresponding to the variables to reach $t$ we need to pass through $m$ "obstacles":
for each clause $j$ we will have a small gadget consisting of a pair of vertices $s_j,t_j$ that have three paths between them.
For example, if the $j^{th}$ clause had the form $x_{17} \vee \overline{x}_{55} \vee x_{72}$ then one path  would go through a vertex in the lower loop corresponding to $x_{17}$, one path would go through a vertex in the upper loop corresponding to $x_{55}$ and the third would go through the lower loop corresponding to $x_{72}$.
We see that if we went in the first stage according to a satisfying assignment then we will be able to find a free vertex to travel from $s_j$ to $t_j$.
We link $t_1$ to $s_2$, $t_2$ to $s_3$, etc and link $t_m$ to $t$.
Thus a satisfying assignment would correspond to a path from $s$ to $t$ that goes through one path in each loop corresponding to the variables, and one path in each loop corresponding to the clauses.
We can make the loop corresponding to the variables long enough so that we must take the entire path in each loop in order to have a fighting chance of getting a path as long as the one corresponds to a satisfying assignment.
But if we do that, then the only way if we are able to reach $t$ is if the paths we took corresponded to a satisfying assignment, since otherwise we will have one clause $j$ where we cannot reach $t_j$ from $s_j$ without using a vertex we already used before.



![We can transform a 3SAT formula $\varphi$ into a graph $G$ such that the longest path in the graph $G$ would correspond to a satisfying assignment in $\varphi$. In this graph, the black colored part corresponds to the variables of $\varphi$ and the blue colored part corresponds to the vertices. A sufficiently long path would have to first "snake" through the black part, for each variable choosing either the "upper path" (corresponding to assigning it the value `True`) or the "lower path" (corresponding to assigning it the value `False`). Then to achieve maximum length the path would traverse through the blue part, where to go between two vertices corresponding to a clause such as $x_{17} \vee \overline{x}_{32} \vee x_{57}$, the corresponding vertices would have to have been not traversed before. ](../figure/3sat_longest_path_red_without_path.png){#longpathfig .class width=300px height=300px}


![The graph above with the longest path marked on it, the part of the path corresponding to variables is in green and  part corresponding to the clauses is in pink.](../figure/3sat_to_longest_path_reduction.png){#longpathfigtwo .class width=300px height=300px}





## Reducing to 3SAT from... everything?

So far we have shown that 3SAT is no harder than Quadratic Equations, Maximum Cut, and Longest Path.
But to show that they are equivalent we need to give reductions in the other direction, reducing each one of these problems to 3SAT as well.
It turns out we can reduce all three problems to 3SAT in one fell swoop.
In fact, this result extends  far beyond these particular problems:  _every_ problem that corresponds to finding a solution that can be easily verified can be reduced to 3SAT.
We make the following definition:

> # {.definition title="NP" #NP-def}
We say that $F:\{0,1\}^* \rightarrow \{0,1\}$ is in $\mathbf{NP}$ if there exists some constants $a,b \in \N$ and $G:\{0,1\}^* \rightarrow \{0,1\}$ such that $G\in \mathbf{P}$ and for every $x\in \{0,1\}^n$
$$
F(x)=1 \Leftrightarrow \exists_{y \in \{0,1\}^{an^b}} \text{ s.t. } G(x,y)=1 \label{NP:eq}
$$

The name $\mathbf{NP}$ stands for "nondeterministic polynomial time" and is used for historical reasons, see the bibiographical notes.


### Examples:

* $3SAT$ is in $\mathbf{NP}$ since for every $\ell$-variable formula $\varphi$, $3SAT(\varphi)=1$ if and only if there exists a satisfying assignment $x \in \{0,1\}^\ell$ such that $\varphi(x)=1$, and we can check this condition in polynomial time.^[Note that an $\ell$ variable formula $\varphi$ is represented by a string of length at least $\ell$, and we can use some "padding" in our encoding so that the assignment to $\varphi$'s variables  is encoded by a string of length exactly $|\varphi|$. We can always use this padding trick, and so one can think of the condition [{NP:eq}](){.eqref} as simply stipulating that the "solution" $y$ to the problem $x$ is of size at most $poly(|x|)$.]


* $QUADEQ$ is in $\mathbf{NP}$ since for every $\ell$ variable instance of quadratic equations $E$, $QUADEQ(E)=1$ if and only if there exists an assignment $x\in \{0,1\}^\ell$ that satisfies $E$ and we can check this condition in polynomial time.

* $LONGPATH$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $LONGPATH(G,k)=1$ if and only if there exists a simple path $P$ in $G$ that is of length at least $k$, and we can check this condition in polynomial time.

* $MAXCUT$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $MAXCUT(G,k)=1$ if and only if there exists a cut $(S,\overline{S})$ in $G$ that cuts at least $k$ edges, and we can check this condition in polynomial time.

### From $\mathbf{NP}$ to 3SAT

There are many, many, _many_, more examples of interesting functions we would like to compute that are easily shown to be in $\mathbf{NP}$. What is quite amazing is that if we can solve 3SAT then we can solve all of them!

> # {.theorem title="Cook-Levin Theorem" #cooklevin-thm}
For every $F\in \mathbf{NP}$, $F \leq_p 3SAT$.

We will see the proof of [cooklevin-thm](){.ref} in the next lecture, but note that it immediately implies that $QUADEQ$, $LONGPATH$, and $MAXCUT$ all reduce to $3SAT$.
In fact, combining it with the reductions we've seen, it implies that all these problems are _equivalent!_. To reduce $QUADEQ$ to $LONGPATH$, we can first reduce $QUADEQ$ to $3SAT$ using [cooklevin-thm](){.ref} and use the reduction we've seen from $3SAT$ to $LONGPATH$.
There is of course nothing special about $QUADEQ$ here- by combining [cooklevin-thm](){.eqref} with the reduction we saw, we see that just like $3SAT$,  _every_ $F\in \mathbf{NP}$ reduces to $LONGPATH$, and the same is true for $QUADEQ$ and $MAXCUT$.
All these problems are in some sense "the hardest in $\mathbf{NP}$" in the sense that an efficient algorithm for one of them would imply an efficient algorithm for _all_ the problems in $\mathbf{NP}$.
This motivates the following definition

> # {.definition title="$\mathbf{NP}$ completeness" #NPC-def}
We say that $G:\{0,1\}^* \rightarrow \{0,1\}$ is _$\mathbf{NP}$ hard_ if for every $F\in \mathbf{NP}$,
$F \leq_p G$. We say that $G$ is _$\mathbf{NP}$ complete_ if $G$ is $\mathbf{NP}$ hard and it is in $\mathbf{NP}$.

[cooklevin-thm](){.ref} and the reductions we've seen in this lecture show that despite their superficial differences, 3SAT, quadratic equations, longest path and maximum cut, are all $\mathbf{NP}$ complete. Thousands more problems have been shown to be $\mathbf{NP}$ complete, arising from all science, mathematics, economics, engineering and many other fields.
If (as is widely believed to be the case) there is no polynomial-time (or even $2^{o(n)}$ time) algorithm for 3SAT, then all of these problems cannot be computed  by an efficient algorithm.




## Complexocartography

Clearly $\mathbf{NP} \supseteq \mathbf{P}$, since if we can decide efficiently whether $F(x)=1$, we can simply ignore any "solution" that we are presented with.  Also, $\mathbf{NP} \subseteq \mathbf{EXP}$, since all the problems in $\mathbf{NP}$ can be solved in exponential time by enumerating all the possible solutions.
For the $\mathbf{NP}$ complete ones, we believe that we cannot radically improve upon this trivial algorithm.
Whether or not is true is the most important open question in computer science, commonly phrased as the $\mathbf{P}$ vs $\mathbf{NP}$ question- is it the case that $\mathbf{P}=\mathbf{NP}$?


One of the mysteries of computation is that people have observed a  certain empirical "zero one law" or "dychotomy" in the computational complexity of natural problems, in the sense that they are either in $\mathbf{P}$ (in fact often with a low exponent) or are $\mathbf{NP}$ hard. However, it is believed that there are problems in $\mathbf{NP}$ that are neither in $\mathbf{P}$ not in $\mathbf{NP}$, and in fact a result known as "Ladner's Theorem" shows that if $\mathbf{P} \neq \mathbf{NP}$ then this is the case.




![A rough illustration of the (conjectured) status of problems in exponential time. Darker colors correspond to higher running time, and the circle in the middle is the problems in $\mathbf{P}$. $\mathbf{NP}$ is a (conjectured to be proper) superclass of $\mathbf{P}$ and the NP complete problems (or NPC) for short are the "hardest" problems in NP, in the sense that a solution for one of them implies solution for all other problems problems in NP. It is conjectured that all the NP complete problems require at least $\exp(n^\epsilon)$ time to solve for a constant $\epsilon>0$, and many require  $\exp(\Omega(n))$ time. The _permanent_ is not believed to be contained in $\mathbf{NP}$ though it is $\mathbf{NP}$-hard, which means that a polynomial-time algorithm for it implies that $\mathbf{P}=\mathbf{NP}$.](../figure/PNPmap.png){#figureid .class width=300px height=300px}

## $\mathbf{NP}$ completeness as a barrier to understanding

^[TODO: add examples of NP hard problems from economics, physics, etc.. that prevent having a closed-form solutions]

^[TODO: maybe include knots]

## Lecture summary

* Many of the problems which we don't know polynomial-time algorithms for are $\mathbf{NP}$ complete, which means that finding a polynomial-time algorithm for one of them would imply a polynomial-time algorithm for _all_ of them.

* It is conjectured that $\mathbf{NP}\neq \mathbf{P}$ which means that we believe that polynomial-time algorithms  for these  problems are not merely _unknown_ but are _nonexistent_.

* While an $\mathbf{NP}$ hardness result means for example that a full fledged "textbook" solution to a problem such as MAX-CUT that is as clean and general as the algorithm for MIN-CUT probably does not exist, it does not mean that we need to give up whenever we see a MAX-CUT instance.                       Later in this course we will discuss several strategies to deal with $\mathbf{NP}$ hardness, including  _average-case complexity_ and _approximation algorithms_.

## Exercises

^[TODO: Maybe mention either in exercise or in body of the lecture some NP hard results motivated by science. For example, shortest superstring that is motivated by genome sequencing, protein folding, maybe others.]


> # {.exercise  #product-ex}
Prove [product-lem](){.ref}

> # {.exercise title="Transitivity of reductions" #transitivity-reductions-ex}
Prove that if $F \leq_p G$ and $G \leq_p H$ then $F \leq_p H$.

> # {.exercise title="Poor man's Ladner's Theorem" #ladner-ex}
Prove that if there is no $n^{O(\log^2 n)}$ time algorithm for $3SAT$ then there is some $F\in \mathbf{NP}$ such that $F \not\in \mathbf{P}$ and $F$ is not $\mathbf{NP}$ complete.^[__Hint:__ Use the function $F$ that on input a formula $\varphi$ and a string of the form $1^t$, outputs $1$ if and only if $\varphi$ is satisfiable and $t=|\varphi|^{\log|\varphi|}$.]


## Bibliographical notes

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
