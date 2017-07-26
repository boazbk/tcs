#  Efficient computation

>_"The problem of distinguishing prime numbers from composite and of resolving the latter into their prime factors is ... one of the most important and useful in arithmetic ... Nevertheless we must confess that all methods ... are either restricted to very special cases or are so laborious ... they try the patience of even the practiced calculator ... and do not apply at all to larger numbers."_, Carl Friedrich Gauss, 1798

>_"For practical purposes, the difference between algebraic and exponential order is often more crucial than the difference between finite and non-finite."_, Jack Edmunds, "Paths, Trees, and Flowers", 1963

>_"Sad to say, but it will be many more years, if ever before we really understand the Mystical Power of Twoness... 2-SAT is easy, 3-SAT is hard, 2-dimensional matching is easy, 3-dimensional matching is hard. Why? oh, Why?"_ Eugene Lawler


So far we were concerned with which functions are computable and which ones are not.
But now we return to _quantitative considerations_ and study the time that it takes to compute functions mapping strings to strings, as a function of the input length.
One of the interesting phenomenona of computing is that there is often a kind of "zero one law" for running time, where for many natural problems, they either can be solved in _polynomial_ running time (e.s., something like $O(n^2)$ or $O(n^3)$), or require _exponential_ (e.g., at least $2^{\Omega(n)}$ or $2^{\Omega(\sqrt{n})}$) running time.
The reasons for this phenomenon are still not fully understood, but some light on this is shed by the concept of _NP completeness_, which we will encounter later.

In this lecture we will survey some examples of computational problems, for some of which we know efficient (e.g., $n^c$-time for a small constant $c$) algorithms, and for others the best known algorithms are exponential.
We want to get a feel as to the kinds of problems that lie on each side of this divide and also see how some seemingly minor changes in formulation can make the (known) complexity of a problem "jump" from polynomial to exponential.

In this lecture, we will not formally define the notion of running time, and so use the same notion of an $O(n)$ or $O(n^2)$ time algorithms as the one you've seen in an intro to CS course: "I know it when I see it".
In the next lecture, we will define this notion precisely, using our NAND++ and NAND<< programming languages.
One of the nice things about the theory of computation is that it turns out that, like in the context of computability, the details of the precise computational model or programming language don't matter that much, especially if you mostly care about the distinction between polynomial and exponential time.

## Some computational problems

Let us start with a few examples of computational problems that we might want to solve.
Many of the problems will involve _graphs_.
We have already encountered graphs in the context of Boolean circuits, but let us now quickly recall the basic notation.
A  graph  $G$ consists of a set of _vertices_ $V$ and _edges_ $E$ where each edge is a pair of vertices.
In a _directed_ graph, an edge is an ordered pair $(u,v)$, which we sometimes denote as $\overrightarrow{u\;v}$.
In an _undirected_ graph, an edge is an unordered pair (or simply a set) $\{ u,v \}$.^[An equivalent viewpoint is that an undirected graph is like a directed graph with the property that whenever the edge $\overrightarrow{u\; v}$ is present then so is the edge $\overrightarrow{v\; u}$.]
We will assume graphs are undirected and _simple_ (i.e., containing no parallel edges or self-loops) unless stated otherwise.
We typically will think of the set of vertices as simply the set  $[n]$ of the numbers from $0$ till $n-1$.
Graphs can be represented either in the _adjacency list_ representation, which is a list of $n$ lists, with the $i^{th}$ list corresponding to the neighbors of the $i^{th}$ vertex, or the _adjacency matrix_ representation, which is an $n\times n$ matrix $A$ with $A_{i,j}$ equalling $1$ if the edge $\overrightarrow{u\; v}$ is present and equalling $0$ otherwise.^[In an undirected graph, the adjacency matrix $A$ is _symmetric_, in the sense that it satisfies $A_{i,j}=A_{j,i}$.]
We can transform between these two representations using $O(n^2)$ operations, and hence for our purposes we will mostly consider them as equivalent.
We will sometimes consider _labeled_ or _weighted_ graphs, where we assign a label or a number to the edges or vertices of the graph, but mostly we will try to keep things simple and stick to the basic notion of an unlabeled, unweighted, simple undirected graph.

There is a reason that graphs are so ubiquitous in computer science and other sciences.
They can be used to model a great many of the data that we encounter.
These are not just the "obvious" networks such as the road network (which can be thought of as a graph of whose vertices are locations with edges corresponding to road segments), or the web (which can be thought of as a graph whose vertices are web pages with edges corresponding to links), or social networks (which can be thought of as a graph whose vertices are people and the edges correspond to friend relation).
Graphs can also denote correlations in data (e.g., graph of observations of features with edges corresponding to features that tend to appear together), casual relations (e.g., gene regulatory networks, where a gene  is connected to gene products it derives), or the state space of a system (e.g., graph of configurations of a physical system, with edges corresponding to states that can be reached from one another in one step).

![Some examples of graphs found from the Internet.](../figure/graphs.png){#figureid .class width=300px height=300px}


We now give some examples of computational problems on graphs.
As mentioned above, to keep things simple, we will restrict attention to undirected simple graphs.
In all cases the input graph $G=(V,E)$ will have $n$ vertices and $m$ edges.
To avoid trivialities, we will always assume the graph is connected (every two vertices can be reached from one another by traversing edges), which in particular means that $m \geq n-1$ (can you see why?).


### Finding the shortest path in a graph

The _shortest path problem_ is the task of, given a graph $G=(V,E)$ and two vertices $s,t \in V$, to find the length of the  shortest path between $s$ and $t$.
That is, we want to find the smallest number $k$ such that there are vertices $v_0,v_1,\ldots,v_k$ with $v_0=s$, $v_k=t$ and for every $i\in\{0,\ldots,k-1\}$ an edge between $v_i$ and $v_{i+1}$.
If each vertex has at least two neighbors then there can be an _exponential_ number of paths from $s$ to $t$, but fortunately we do not have to enumerate them all to find the shortest path.
We can do so by performing a _breadth first search (BFS)_, enumerating $s$'s neighbors, and then neighbors' neighbors, etc.. in order.
If we maintain the neighbors in a list we can perform a BFS in $O(n^2)$ time, while using  a queue we can do this in $O(m)$ time.^[Since we assume $m \geq n-1$, $O(m)$ is the same as $O(n+m)$. As we mentioned above, we state the running time of BFS as $O(m)$ even though it is typically  thought of as an  $O(m)$ time algorithm, to avoid dependence on the model. [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm) is a well-known generalization of BFS to _weighted_ graphs.]


### Finding the longest path in a graph

The _longest path problem_ is the task of, given a graph $G=(V,E)$ and two vertices $s,t \in V$, to find the length of the _longest_ simple (i.e., non intersecting) path between $s$ and $t$.
While a priori this may seem less motivated than the shortest path, it is a natural optimization problem related to the  [Hamiltonian path problem](https://en.wikipedia.org/wiki/Hamiltonian_path_problem) which asks for  a _maximally long_ simple path (i.e., path that visits all $n$ vertices once) between $s$ and $t$, as well as   the notorious [traveling salesman problem (TSP)](https://en.wikipedia.org/wiki/Travelling_salesman_problem) of finding (in a weighted graph) a maximally long path of cost at most $w$.
TSP is a classical optimization problem, with applications ranging from  planning and logistics to DNA sequencing and astronomy.

A priori it is not clear that  finding the longest path should be harder  than finding the shortest path,
but this turns out to be the case.
While we know how to find the shortest path in $O(n)$ time, for the longest path problem we have not been able to significantly improve upon the trivial brute force algorithm to try all paths,
and the best algorithm takes   $\Omega(c^n)$ time for some constant $c$ which is a little smaller than $2$ but not that much smaller.^[At the moment the best record is $c \sim 1.65$ or so. Even beating the trivial $O(n!)$ bound is not that simple, see [longest-path-ex](){.ref}.]

![A _knight's tour_ can be thought of as a maximally long path on the graph corresponding to a chessboard where we put an edge between any two squares that can be reached by one step via a legal knight move.](../figure/knights_tour.jpg){#knighttourpath .class width=300px height=300px}


### Finding the minimum cut in a graph

Given a graph $G=(V,E)$, a _cut_  is simply a subset $S$ of $V$, and the edges cut by $S$ are those edges where one of their endpoints is in $S$ and the other is in $\overline{S} = V \setminus S$.
If $s,t \in V$ then an _$s,t$ cut_ is a cut such that $s\in S$ and $t\in \overline{S}$.
The _minimum $s,t$ cut problem_ ( is the task of finding, given $s$ and $t$, the minimum number $k$ such that there is an $s,t$ cut cutting $k$ edges.^[We can also define the problem of finding the minimum $s,t$ cut in the graph over all pairs $s,t$. Though note that  if we can solve the minimum $s,t$ cut problem in time $T(n)$ then we can solve the global minimum cut in time   $O(T(n)n^2)$.]

The minimum $s,t$ cut problem appears in many applications.
Minimum cuts often correspond to  _bottlenecks_.
For example, in a communication network the minimum cut between $s$ and $t$ corresponds to the smallest number of edges that, if dropped,  will disconnect $s$ from $t$.
Similar applications arise in scheduling and planning.
There are also other applications as well: for _image segmentation_, we can define a graph whose vertices are pixels and whose edges correspond to neighboring pixels of distinct colors.
If we want to separate the foreground from the background then we can  pick (or guess) a foreground pixel $s$ and background pixel $t$ and ask for a minimum cut between them.

Once again, a priori we might worry that we'd need to enumerate over all the $2^n$ subsets of $S$.
Fortunately, we can solve the minimum $s$-$t$ cut problem efficiently.
There are several algorithms to do so, but many of them rely on the [Max Flow Min Cut](https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem) that says that the minimum cut between $s$ and $t$ equals the maximum amount of _flow_ we can send from $s$ to $t$, if every edge has unit capacity.
For example, this directly implies that the value of the minimum cut problem is the solution for the following [linear program](https://en.wikipedia.org/wiki/Linear_programming):

$$
\begin{split}
\max_{x\in \R^m} F_s(x)-F_t(x) \text{s.t.}\\
\forall_{u \not\in \{s,t\}} F_u(x)=0
\end{split}
$$
where for every vertex $u$ and $x\in \R^m$, $F_u(x) = \sum_{e \in E \text{s.t.} u \in e} x_e$.

Since there is a polynomial-time algorithm for linear programming, the minimum cut (or, equivalently, maximum flow) problem can be solved in polynomial time.
In fact, there are much better algorithms for this problem, with currently the record standing at $O(\min\{ m^{10/7}, m\sqrt{n}\})$.^[TODO: add references in biliographical notes: Madry, Lee-Sidford]


### Finding the maximum cut in a graph

We can also define the _maximum cut_ problem of finding, given a graph $G=(V,E)$ the subset $S\subseteq V$
that _maximizes_ the number of edges cut by $S$.^[We can also consider the variant where one is given $s,t$ and looks for the $s,t$-cut that maximizes the number of edges cut. The two variants are equivalent up to $O(n^2)$ factors in the running time, but the we use the  global max cut forumlation since it  is more common in the literature.]
Like its cousin the minimum cut problem, the maximum cut problem is also very well motivated.
For example, it  arises in VLSI design, and also has some surprising relation to analyzing the
[Ising model](https://en.wikipedia.org/wiki/Ising_model) in statistical physics.

Once again, a priori it might not be clear that the maximum cut problem should be  harder than minimum cut but this turns out to be the case.
We do not know of an algorithm that solves this problem much faster than the trivial  "brute force" algorithm that tries all $2^n$ possibilities for the set $S$.

###  A note on convexity


![In a _convex_ function (right figure) the global minimum is the only local minimum, and we can find it by a local-search algorithm which can be thought of as dropping  a marble and letting it "slide down" until it reaches the global minimum. In contrast, a non-convex function (right figure) might have an exponential number of local minima in which any local-search algorithm could get stuck.](../figure/convexandnon.jpg){#figureid .class width=300px height=300px}

There is an underlying reason for the sometimes radical difference between the difficulty of maximizing and minimizing a function over a domain.
If $D \subseteq \R^n$, then a function $f:D \rightarrow R$ is _convex_ if for every $x,y \in D$ and $p\in [0,1]$
$f(px+(1-p)y) \leq pf(x) + (1-p)f(y)$.
That is, $f$ applied to the $p$-weighted midpoint between $x$ and $y$ is smaller than the $p$-weighted average value of $f$.
If $D$ itself is convex (which means that if $x,y$ are in $D$ then so is the line segment between them), then this means that if $x$ is a _local minimum_ of $f$ then it is also a _global minimum_.
The reason is that if $f(y)<f(x)$ then every point $z=px+(1-p)y$ on the line segment between $x$ and $y$ will satisfy $f(z) \leq p f(x) + (1-p)f(y) < f(x)$ and hence in particular $x$ cannot be a local minimum.
Intuitively, local minima of functions are much easier to find than global ones: after all, any "local search" algorithm that keeps finding a nearby point on which the value is lower, will eventually arrive at a local minima.^[One example of such a local search algorithm is [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) which takes a small step in the direction that would reduce the value by the most amount based on the current derivative. There are also algorithms that take advantage of the _second derivative_ (hence are known as _second order methods_)  to potentially converge faster.]
Indeed, under certain technical conditions, we can often efficiently find the minimum of convex functions, and this underlies the reason problems such as minimum cut and shortest path are easy to solve.
On the other hand, _maximizing_  a convex function (or equivalently, minimizing a _concave_ function) can often be a hard computational task.

The minimum cut problem is not a priori a convex minimization task, because the set of potential cuts is   _discrete_. However, it turns out that we can embed it in a continuous and convex set via the maximum flow problem.
The "max flow min cut" theorem ensuring that this embedding is "tight" in the sense that the minimum "fractional cut" that we obtain through the maximum-flow linear program will be the same as the true minimum cut.
Unfortunately, we don't know of such a tight embedding in the setting of the _maximum_ cut problem.

The issue of convexity arises time and again in the context of computation.
For example, one of the basic tasks in machine learning is _empirical risk minimization_.
That is, given a set of labeled examples $(x_1,y_1),\ldots,(x_m,y_m)$, where each $x_i \in \{0,1\}^n$ and $y_i \in \{0,1\}$, we want to find the function $h:\{0,1\}^n \rightarrow \{0,1\}$ from some class $H$ that minimizes the _error_ in the sense of minimizing the number of $i$'s such that $h(x_i) \neq y_i$.
Like in the minimum cut problem, to make this a better behaved computational problem, we often embed it in a continuous domain, including functions that could output a real number and replacing the condition $h(x_i) \neq y_i$ with minimizing some continuous _loss function_ $\ell(h(x_i),y_i)$.^[We also sometimes replace or enhance the condition that $h$ is in the class $H$ by adding a _regularizing term_ of the form $R(h)$ to the minimization problem, where $R:H \rightarrow \R$ is some measure of  the "complexity" of $h$. As a general rule, the larger or more "complex" functions $h$ we allow, the easier it is to fit the data, but the more danger we have of "overfitting".]
When this embedding is _convex_ then we are guaranteed that the global minimizer is unique and can be found in polynomial time.
When the embedding is _non convex_, we have no such guarantee and in general there can be many global or local minima.
That said, even if we don't find the global (or even a local) minima, this continuous embedding can still help us.
In particular,  when running a local improvement algorithm such as Gradient Descent, we might still find a function $h$ that is  "useful" in the sense of having a   small error on future examples from the same distribution.^[In machine learning parlance, this task is known as _supervised learning_. The set of examples $(x_1,y_1),\ldots,(x_m,y_m)$ is known as the _training set_, and the error on additional samples from the same distribution is known as the _generalization error_, and can be measured by checking $h$ against a _test set_ that was not used in  training it.]


### The 2SAT problem

Not all computational problems arise from graphs.
A _propositional formula_ $\varphi$ involves $n$ variables $x_1,\ldots,x_n$ and the logical operators AND ($\wedge$), OR ($\vee$), and NOT ($\neg$, also denoted as $\overline{\cdot}$).
We say that such a formula is in _conjunctive normal form_ (CNF for short) if it is an OR of ANDs of variables or their negations (we call a term of the form $x_i$ or $\overline{x}_i$ a _literal_).
For example, this is a CNF formula
$$
(x_7 \vee \overline{x}_{22} \vee x_{15} ) \wedge (x_{37} \vee x_{22}) \wedge (x_{55} \vee \overline{x}_7)
$$


We say that a formula is a $k$-CNF it is an AND or ORs where each OR involves exactly $k$ literals.
The 2SAT problem is to find out, given a $2$-CNF formula $\varphi$, whether there is an assignment $x\in \{0,1\}^n$ that _satisfies_ $\varphi$, in the sense that it makes it evaluate to $1$ or "True".

Determining the satisfiability of Boolean formulas arises in many applications and in particular in software and hardware verification, as well as scheduling problems.
The trivial, brute-force, algorithm for 2SAT will enumerate all the $2^n$ assignments $x\in \{0,1\}^n$ but fortunately we can do much better.

The key is that we can think of every constraint of the form $\ell_i \vee \ell_j$ (where $\ell_i,\ell_j$ are _literals_, corresponding to variables or their negations) as an _implication_ $\overline{\ell}_i \Rightarrow \ell_j$, since it corresponds to the constraints that if the literal $\ell'_i = \overline{\ell}_i$ is true then it must be the case that $\ell_j$ is true as well.
Hence we can think of $\varphi$ as a directed graph between the $2n$ literals, with an edge from $\ell_i$ to $\ell_j$ corresponding to an implication from the former to the latter.
It can be shown  that $\varphi$ is unsatisfiable if and only if there is a variable $x_i$ such that there is a directed path from  $x_i$ to $\overline{x}_i$ as well as a directed path from $\overline{x}_i$ to $x_i$ (see [twosat_ex](){.ref}).
This reduces 2SAT to the (efficiently solvable) problem of determining connectivity in directed graphs.

### The 3SAT problem

The 3SAT problem is the task of determining satisfiability  for 3CNFs.
One might think that the difference between two and three would not make that much a difference for complexity.
One would be wrong.
Despite much effort, do not know of a significantly better than brute force algorithm for 3SAT (the best known algorithms take roughy $1.3^n$ steps).

Interestingly, a similar issue arises time and again in computation, where the difference between two and three often corresponds to the difference between tractable and intractable.
As Lawler's quote alludes to, we do not fully understand the reasons for this phenomenon, though the notions of $\mathbf{NP}$ completeness we will see in the next lecture does offer a partial explanation.
It may be related to the fact that optimzing a polynomial often amounts to equations on its derivative. The derivative of a  a quadratic polynomial is linear, while the derivative of a cubic is quadratic, and, as we will see, the difference between solving linear and quadratic equations can be quite profound.


### Solving linear equations

One of the most useful problems that people have been solving time and again is solving
$n$ linear equations in $n$ variables.
That is, solve equations of the form

$$
\begin{split}
a_{0,0}x_0 + a_{0,1}x_1 + \cdots + a_{0,{n-1}}x_{n-1} &= b_0 \\
a_{1,0}x_0 + a_{1,1}x_1 + \cdots + a_{1,{n-1}}x_{n-1} &= b_1 \\
\vdots     + \vdots      +  \vdots + \vdots              &= \vdots \\
a_{n-1,0}x_0 + a_{n-1,1}x_1 + \cdots + a_{n-1,{n-1}}x_{n-1} &= b_{n-1}
\end{split}
$$



where $\{ a_{i,j} \}_{i,j \in [n]}$ and $\{ b_i \}_{i\in [n]}$ are real (or rational) numbers.
More compactly, we can write this as the equations $Ax = b$ where $A$ is an $n\times n$ matrix, and we think of $x,b$ are column vectors in $\R^n$.

The standard Gaussian elimination algorithm can be used to solve such equations in polynomial time (i.e., determine if they have a solution, and if so, to find it).^[To analyze this fully we need to ensure that the bit complexity of the numbers involved does not grow too much, but fortunately we can indeed ensure this using Cramer's rule. Also, as is usually the case when talking about real numbers, we  do not care much for the distinction  between solving equations exactly and solving them to arbitrarily good precision.]
As we discussed above,  if we are willing to allow some loss in precision, we even have algorithms that  handle linear _inequalities_, also known as linear programming.


### Solving quadratic equations

Suppose that the equations involve also _quadratic_ terms of the form $a_{i,j,k}x_jx_k$.
That is, suppose that we are given a set of quadratic polynomials $p_1,\ldots,p_m$ and consider the equations $\{ p_i(x) = 0 \}$.
To avoid issues with bit representations, we will always assume that the equations contain the constraints $\{ x_i^2 - x_i = 0 \}_{i\in [n]}$ and hence the solutions can be assumed to lie in $\{0,1\}^n$.
This is a very well motivated problem which in particular generalizes the classical [quadratic assignment problem](https://www.opt.math.tugraz.at/~cela/papers/qap_bericht.pdf).
Once again, we do not know a much better algorithm for this problem than the one that enumerates over all the $2^n$ possiblities.

### The permanent (mod 2) problem

Given an $n\times n$ matrix $A$, the _permanent_ of $A$ is the sum over all permutations $\pi$ (i.e., $\pi$ is a member of the set $S_n$ of one-to-one and onto functions  from $[n]$ to $[n]$) of the product $\prod_{i=0}^{n-1}A_{i,\pi(i)}$.
The permanent of a matrix is a natural quantity, and has been studied in several contexts including combinatorics and graph theory.
It also arises in physics where it can be used to describe the quantum state of multiple boson particles
(see [here](http://www.cs.huji.ac.il/labs/learning/Papers/perm.pdf) and [here](https://en.wikipedia.org/wiki/Boson_sampling)).

If the entries of $A$ are integers, then we can also define a _Boolean_ function $perm_2(A)$ which will output the result of the permanent modulo $2$.
A priori computing this would seem to require enumerating over all $n!$ possiblities.
However, it turns out we can compute $perm_2(A)$ in polynomial time!
The key is that modulo $2$, $-x$ and $+x$ are the same quantity and hence the permanent  moulo $2$ is the same as taking the following quantity modulo $2$:

$$
\sum_{\pi \in S_n} sign(\pi)\prod_{i=0}^{n-1}A_{i,\pi(i)} \label{eq:det}
$$

where the _sign_  of a permutation $\pi$ is a number in $\{+1,-1\}$ which can be defined in several ways, one of which is that $sign(\pi)$  equals  $+1$ if the number of swaps that "Bubble" sort performs starting an array sorted according to $\pi$ is even, and it equals $-1$ if this number is odd.^[It turns out that this definition is independent of the sorting algorithm, and for example if $sign(\pi)=-1$ then one cannot sort an array ordered according to $\pi$ using an even number of swaps.]

It seems like we replaced one formula involving a sum over $n!$ terms with an even more complicated formula, which does not appear useful for making the problem easier.
But fortunately [eq:det](){.eqref} also has an alternative description: it is simply the [determinant](https://en.wikipedia.org/wiki/Determinant) of the matrix $A$, which can be computed using a process similar to Gaussian elimination.

### The permanent (mod 3) problem

Emboldened by our good fortune above, we might hope to be able to compute the permanent modulo any prime $p$ and perhaps in full generality.
Alas, we have no such luck.
We do not know of a much better than brute force algorithm to even compute the permanent modulo $3$.

### Finding a zero-sum equilibrium

A _zero sum game_ is a game between two players where the payoff for one is the same as the penalty for the other.
That is, whatever the first player gains, the second player loses.
As much as we want to avoid them, zero sum games do arise in life, and the one good thing about them is that at least we can compute the optimal strategy.

A zero sum game can be specified by an $n\times n$ matrix $A$, where if player 1 chooses action $i$ and player 2 chooses action $j$ then player one gets $A_{i,j}$ and player 2 loses the same amount.
The famous "min max" theorem by John von Neumann states that if we allow probabilistic or "mixed" strategies (where a player does not choose a single action but rather a _distribution_ over actions) then it does not matter who plays first and the end result will be the same.
Mathematically the min max theorem is that if we let $\Delta_n$ be the set of probability distributions over $[n]$ (i.e., non-negative columns vectors in $\R^n$ whose entries sum to $1$) then

$$
\max_{p \in \Delta_n} \min_{q\in \Delta_n} p^\top A q =  \min_{q \in \Delta_n} \max_{p\in \Delta_n} p^\top A q \label{eq:minmax}
$$

The min-max theorem turns out to be a corollary of linear programming duality, and indeed the value of [eq:minmax](){.eqref} can be computed efficiently by a linear program.

### Finding a Nash equilibrium

Fortunately, not all real-world games are zero sum, and we do have  more general games, where the payoff of one player is not necessarily the loss of the other.
John Nash won the Nobel prize for showing that there is a notion of _equilibrium_ for such games as well.
In many economic texts it is taken as an article of faith that when actual agents are involved in such a game then they reach a Nash equilibrium.
However, unlike zero sum games, we do not know of an efficient algorithm for finding a Nash equilibrium given the description of a general (non zero sum) game.
In particular this means that, despite economists' intuitions, there are games for which natural stategies will take exponential number of steps to converge to an equilibrium.



### Primality testing

Another classical computational problem that has been of interest since the ancient greeks is to determine whether a given number $N$ is prime or composite.
Clearly we can do so by trying to divide it with all the numbers in $2,\ldots,N-1$, but this would take at least $N$ steps which is _exponential_ in its bit complexity $n = \log N$.
We can reduce these $N$ steps to $\sqrt{N}$ by observing that if $N$ is a composite of the form $N=PQ$ then either $P$ or $Q$ is smaller than $\sqrt{N}$.
However, it turns out we can do radically better.
In the 1970's, Rabin and Miller gave _probabilistic_ algorithms to determine whether a given number $N$ is prime or composite in time $poly(n)$ for $n=\log N$.
We will discuss the probabilistic model of computation later in this course.
In 2002, Agrawal, Kayal, and Saxena found a deterministic $poly(n)$ time algorithm for this problem.
This is surely a development that mathematicians from Archimedes till Gauss would have found exciting.



### Integer factoring

Given that we can efficiently determine whether a number $N$ is prime or composite, we could expect that in the latter case we could also efficiently _find_ the factorization of $N$.
Alas, no such algorithm is known.
In a surprising and exciting turn of events, the _non existence_ of such an algorithm has been used as a basis for encryptions, and indeed it underlies much of the security of the world wide web.
We will return to the factoring problem later in this course.
We remark that we do know much better than brute force algorithms for this problem.
While the brute force algorithms would require $2^{\Omega(n)}$ time to factor an $n$-bit integer, there are known algorithms running in time $2^{O(\sqrt{n})}$ and also algorithms that are widely believed (though not fully rigorously analyzed) to run in time $2^{O(n^{1/3})}$.


## Our current knowledge

![The current computational status of several interesting problems. For all of them we either know a polynomial-time algorithm or the known algorithms require at least $2^{n^c}$ for some $c>0$. In fact for all except the _factoring_ problem, we either know an $O(n^3)$ time algorithm or the best known algorithm require at least $2^{\Omega(n)}$ time where $n$ is a natural parameter such that there is a brute force algorithm taking roughly $2^n$ or $n!$ time. Whether this "cliff" between the easy and hard problem is a real phenomenon or a reflection of our ignorane is still an open question.](../figure/poly_vs_exp.png){#current_status .class width=300px height=300px}

The difference between an  exponential and polynomial time algorithm might seem merely "quantiative" but it is in fact extremely significant.
As we've already seen, the brute force exponential time algorithm runs out of steam very very fast, and as Edmonds says, in practice there might not be much difference between a problem where the best algorithm is exponential and a problem that is not solvable at all.
Thus the efficient algorithms we mention above are widely used and power many computer science applications.
Moreover, a polynomial-time algorithm often arises out of significant insight to the problem at hand, whether it is the "max-flow min-cut" result, the solvability of the determinant, or the group theoretic structure that enables primality testing.
Such insight can be useful regardless of its computational implications.

At the moment we do not know whether the "hard" problems are truly hard, or whether it is merely because we haven't yet found the right algorithms for them.
However, we will now  see  that there are problems that do _inherently require_ exponential time.
We just don't know if any of the examples above fall into that category.

## Lecture summary

* There are many natural problems that have polynomial-time  algorithms, and other natural problems that we'd love to solve, but for which the best known algorithms are exponential.

* Often a polynomial time algorithm relies on discovering some hidden structure in the problem, or finding a surprising  equivalent formulation for it.

* There are many interesting problems where there is an _exponential gap_ between the best known algorithm and the best algorithm that we can rule out. Closing this gap is one of the main open questions of theoretical computer science.

## Exercises

> # {.exercise title="exponential time algorithm for longest path" #longest-path-ex}
Give a $poly(n)2^n$ time algorithm for the longest path problem in $n$ vertex graphs.^[__Hint:__ Use dynamic programming to compute for every $s,t \in [n]$ and $S \subseteq [n]$ the value $P(s,t,S)$ which equals to $1$ if there is a simple path from $s$ to $t$ that uses exactly the vertices in $S$. Do this iteratively for $S$'s of growing sizes.]

> # {.exercise title="2SAT algorithm" #twosat_ex}
For every 2CNF $\varphi$,  define the graph $G_\varphi$ on $2n$ vertices corresponding to the literals $x_1,\ldots,x_n,\overline{x}_1,\ldots,\overline{x}_n$, such that there is an edge $\overrightarrow{\ell_i\; \ell_j}$ iff the constraint $\overline{\ell}_i \vee \ell_j$ is in $\varphi$.
Prove that $\varphi$ is unsatisfiable if and only if there is some $i$ such that there is a path from $x_i$ to $\overline{x}_i$ and from $\overline{x}_i$ to $x_i$ in $G_\varphi$.
Show how to use this to solve 2SAT in polynomial time.

> # {.exercise title="Regular expressions" #regularexp}
A _regular_ expression over the binary alphabet is a string consisting of the symbols $\{ 0 , 1 , \emptyset , ( , ) , * , | \}$.
An expression $exp$ corresponds to a function mapping $\{0,1\}^* \rightarrow \{0,1\}$, where the `0` and `1` expressions correspond to the functions that map only output $1$ on the strings `0` and `1` respectively, and if $exp,exp'$ are expressions corresponnding to the functions, $f'$ then $(exp)|(exp')$ corresponds to the function $f \vee f'$, $(exp)(exp')$ corresponds to the function $g$ such that for $x\in \{0,1\}^n$, $g(x)=1$ if there is some $i \in [n]$ such that $f(x_0,\ldots,x_i)=1$ and $f(x_{i+1},\ldots,x_{n-1})=1$, and $(exp)*$ corresponds to the function $g$ such that $g(x)=1$ if either $x=\emptyset$ or  there are strings $x_1,\ldots,x_k$ such that $x$ is the concatenation of $x_1,\ldots,x_k$ and $f(x_i)=1$ for every $i\in [k]$. \
Prove that for every regular expression $exp$, the function corresponding to $exp$ is computable in polynomial time.
Can you show that it is computable in $O(n)$ time?


## Bibliographical notes

Eugene Lawler's quote on  the "mystical power of twoness"  was taken from the wonderful book "The Nature of Computation" by Moore and Mertens. See also [this memorial essay on Lawler](https://pure.tue.nl/ws/files/1506049/511307.pdf) by Lenstra.

^[TODO: add reference to best algorithm for longest path - probably the Bjorklund algorithm]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)

## Acknowledgements
