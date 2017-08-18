# Mathematical Background


>_"Young man, in mathematics you don't understand things. You just get used to them."_, John von Neumann

## Mathematical prerequisites



The main notions we will use in this course are the following:

* __Proofs:__ First and foremost, this course will involve a heavy dose of formal mathematical reasoning, which includes mathematical _definitions_, _statements_, and _proofs_.

* __Sets:__ Including notation such as membership ($\in$), containment ($\subseteq$), and set operations such as union, intersection,  subtraction  and Cartesian product ($\cup,\cap,\setminus$ and $\times$).

* __Functions:__ Including the notions of the _domain_ and _range_ of a function, properties such  being  _one-to-one_ or _onto_ functions, and also the   notion of _partial functions_ (that, unlike standard or "total" functions, are not necessarily defined on all elements of their domain).

* __Logical operations:__ The operations AND, OR, and NOT ($\wedge,\vee,\neg$) and the quantifiers "exists" and "forall" ($\exists$,$\forall$).

* __Tuples and strings:__ The notation $\Sigma^k$ and $\Sigma^*$ where $\Sigma$ is some finite set which is called the _alphabet_ (quite often $\Sigma = \{0,1\}$).

* __Basic combinatorics:__ Notions such as $\binom{n}{k}$ (the number of $k$-sized subset of a set of size $n$).

* __Graphs:__ Undirected and directed graphs, degrees, connectivity.

* __Big Oh notation:__ $O,o,\Omega,\omega,Theta$ notation for analyzing asymptotics of functions.

* __Discrete probability:__ Later on in this course we will use _probability theory_, and specifically probability over _finite_ samples spaces such as tossing $n$ coins. We will only use  probability theory in the second half of this course, and will review it  before we use. However,  probabilistic reasoning is a subtle (and extremely useful!) skill, and it's always good to start early in acquiring it.




There are several excellent freely-available resources for the above material online.
In particular, the [CS 121 webpage](http://www.boazbarak.org/cs121/background/) contains a program for self study of all the needed notions using the lecture notes, videos, and assignments of MIT course [6.042j Mathematics for Computer science](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-fall-2010/) (which is also the text used by Harvard CS 20).
Still, in the rest of this section we briefly review these as well, partially to remind the reader and reinforce material that might not be fresh in your mind, and partially to introduce our notation and conventions which might occasionally differ from those you've encountered before.



## Basic discrete math objects

We now quickly review some of the objects and definitions we use from discrete math in this course.

### Sets

A _set_ is an unordered collection of objects.
For example, when we write $S = \{ 2,4, 7 \}$, we mean that $S$ denotes the set that contains the numbers $2$, $4$, and $7$.
(We use the notation "$2 \in S$" to denote that $2$ is an element of $S$.)
Note that the set $\{ 2, 4, 7 \}$ and $\{ 7 , 4, 2 \}$ are identical, since they contain the same elements.
Also, a set either contains an element or does not contain it -there is no notion of containing it  "twice"- and so we could even write the same set $S$ as  $\{ 2, 2, 4, 7\}$ (though that would be a little weird).
The _cardinality_ of a finite set $S$, denoted by $|S|$, is the number of distinct elements it contained.
So, in the example above, $|S|=3$.
A set $S$ is a _subset_ of a set $T$, denoted by $S \subseteq T$, if every element of $S$ is also an element of $T$. (We can also describe this by saying that  $T$ is a _superset_ of $S$.)
For example, $\{2,7\} \subseteq \{ 2,4,7\}$.
The set that contains no elements is known as the _empty set_ and it is denoted by $\emptyset$.


We can define sets by either listing all their elements or by writing down a rule that they satisfy such as
$$
EVEN = \{ x  \;:\; \text{ $x=2y$ for some non-negative integer $y$} \} \;.
$$

Of course there is more than one way to write the same set, and often we will use intuitive notation listing a few examples that illustrate the rules, and hence we can also define $EVEN$ as
$$
EVEN = \{ 0,2,4, \ldots \} \;.
$$

Note that a set can be either finite  (such as the set $\{2,4,7\}$ ) or infinite (such as the set $EVEN$).
Also, the elements of a set don't have to be numbers.
We can talk about the sets such as the set $\{a,e,o,u \}$ of all the vowels in the English language, or the  set $\{ New York, Los Angeles, Chicago \}$  of all cities in the U.S. with population more than  one million  per the 2010 census.^[TODO: check this and add other cities as needed. Also check that as a non-native speaker, I didn't miss a vowel.]
A set can even have other sets as elements, such as the set $\{ \emptyset, \{1,2\},\{2,3\},\{1,3\} \}$ of all even-sized subsets of $\{1,2,3\}$.

__Operations on sets:__ The _union_ of two sets $S,T$, denoted by $S \cup T$, is the set that contains all elements that are either in $S$ _or_ in $T$. The _intersection_ of $S$ and $T$, denoted by $S \cap T$, is the set of elements that are both in $S$ _and_ in $T$. The _set difference_ of $S$ and $T$, denoted by $S \setminus T$ (and in some texts  also by $S-T$), is the set of elements that are in $S$ but _not_ in $T$.

__Tuples and Cartesian product:__ If $S$ and $T$ are sets, then their _Cartesian product_, denoted by $S \times T$, is the set of all ordered pairs $(s,t)$ where $s\in S$ and $t\in T$.
For example, if $S = \{1,2,3 \}$ and $T = \{10,12 \}$, then $S\times T$ contains the $6$ elements $(1,10),(2,10),(3,10),(1,12),(2,12),(3,12)$.
Similarly if $S,T,U$ are sets then $S\times T \times U$ is the set of all ordered triples $(s,t,u)$ where $s\in S$, $t\in T$, and $u\in U$.
More generally, for every positive integer $n$ and sets $S_0,\ldots,S_{n-1}$, we denote by $S_0 \times S_1 \times \cdots \times S_{n-1}$ the set of ordered $n$-tuples $(s_0,\ldots,s_{n-1})$ where $s_i\in S_i$ for every $i \in \{0,\ldots, n-1\}$.  
For every set $S$, we  denote the set $S\times S$ by $S^2$, $S\times S\times S$ by $S^3$, $S\times S\times S \times S$ by $S^4$, and so on and so forth.



### Special sets

There are several sets that we will use in this course time and again, and so find it useful to introduce notation for them.
For starters we define

$$
\N = \{ 0, 1,2, \ldots \}
$$

to be the set of all _natural numbers_, i.e., non-negative integers.
For any natural number $n$, we define the set $[n]$ as $\{0,\ldots, n-1\} = \{ k\in \N : k < n \}$.
Note that we start our indexing of both $\N$ and $[n]$ from $0$.
Many texts start those from $1$.
Starting from zero or one is simply a convention that doesn't make much difference, as long as one is consistent about it.

We will also occasionally use the set $\Z=\{\ldots,-2,-1,0,+1,+2,\ldots \}$ of (negative and non-negative) _whole numbers_, as well as the set $\R$ of _real_ numbers. (This is the set that includes not just the whole numbers, but also fractional and even irrational numbers; e.g., $\R$ contains numbers  such as $+0.5$, $-\pi$, etc.)
We denote by $\R_+$  the set $\{ x\in \R : x > 0 \}$ of _positive_  real numbers.
This set is sometimes also denoted as $(0,\infty)$.

__Strings:__ Another set we will use time and again is

$$
\{0,1\}^n = \{ (x_0,\ldots,x_{n-1}) \;:\; x_0,\ldots,x_{n-1} \in \{0,1\}  \}
$$

which is the set of all $n$-length binary strings for some natural number $n$.
That is $\{0,1\}^n$ is the set of all length-$n$ lists of zeroes and ones.
Note that this is consistent with our notation above: $\{0,1\}^2$ is the Cartesian product $\{0,1\} \times \{0,1\}$, $\{0,1\}^3$ is the product $\{0,1\} \times \{0,1\} \times \{0,1\}$ and so on.


We  will write the string $(x_0,x_1,\ldots,x_{n-1})$ as simply $x_0x_1\cdots x_{n-1}$ and so for example

$$
\{0,1\}^3 = \{ 000 , 001, 010 , 011, 100, 101, 110, 111 \} \;.
$$

For every string $x\in \{0,1\}^n$ and $i\in [n]$, we write $x_i$ for the $i^{th}$ coordinate of $x$.
If $x$ and $y$ are strings, then $xy$  denotes their _concatenation_.
That is, if $x \in \{0,1\}^n$ and $y\in \{0,1\}^m$, then $xy$ is equal to the string $z\in \{0,1\}^{n+m}$ such that for $i\in [n]$, $z_i=x_i$ and for $i\in \{n,\ldots,n+m-1\}$, $z_i = y_{i-n}$.

We will also often talk about the set of binary strings of _all_ lengths, which is

$$
\{0,1\}^* = \{ (x_0,\ldots,x_{n-1}) \;:\; n\in\N \;,\;, x_0,\ldots,x_{n-1} \in \{0,1\} \} \;.
$$

Another way to write this set is as
$$
\{0,1\}^* = \{0,1\}^0 \cup \{0,1\}^1 \cup \{0,1\}^2 \cup \cdots
$$

or more concisely as

$$
\{0,1\}^* = \cup_{n\in\N} \{0,1\}^n \;.
$$

Note that the  set $\{0,1\}^*$ contains also the "string of length $0$", which we denote by $\emptyset$.
If there is a chance of confusion with the empty set, we will denote this string by `""`.


__Generalizing the star operation:__ For every set $\Sigma$, we define

$$\Sigma^* = \cup_{n\in \N} \Sigma^n \;.$$

For example, if $\Sigma = \{a,b,c,d,\ldots,z \}$ then $\Sigma^*$ denotes the set of all finite length strings over the alphabet a-z.



### Functions

If $S$ and $T$ are sets, a _function_ $F$ mapping $S$ to $T$, denoted by $F:S \rightarrow T$, associates with every element $x\in S$ an element $F(x)\in T$.
Just as with sets, we can write a function either by listing the table of all the values it gives for elements in $S$ or using a rule.
For example if $S = \{0,1,2,3,4,5,6,7,8,9 \}$ and $T = \{0,1 \}$.
Then  the function $F$ defined as

| Input | Output |
|:------|:-------|
| 0     | 0      |
| 1     | 1      |
| 2     | 0      |
| 3     | 1      |
| 4     | 0      |
| 5     | 1      |
| 6     | 0      |
| 7     | 1      |
| 8     | 0      |
| 9     | 1      |

\


Is the same as defining $F(x)= (x \mod 2)$.
If $F:S \rightarrow T$ satisfies that $F(x)\neq F(y)$ for all $x \neq y$ then we say that $F$ is _one-to-one_.  
If $F$ satisfies that for every $y\in T$ there is some $x$ such that $F(x)=y$ then we say that $F$ is _onto_.
A  one-to-one and onto function is called a _bijection_, and when $S=T$ it is also known as a _permutation_.
If  $F:S \rightarrow T$ is a bijection  then  for every $y\in T$ there is a unique $x\in S$ s.t. $F(x)=y$.
We denote this value $x$ by $F^{-1}(y)$.
Note that $F^{-1}$ is itself a bijection from $T$ to $S$ (can you see why?).


Giving a bijection between two sets is often a good way to show they have  the same size.
In fact, the standard mathematical definition of the notion that "$S$ and $T$ have the same cardinality" is that there exists a bijection $f:S \rightarrow T$.
As we will see later in this course, this is a definition that naturally generalizes to comparing the cardinality of _infinite_ sets.


__Partial functions:__ We will sometimes be interested in _partial_ functions from $S$ to $T$.
This is a function $F$ that is not necessarily defined on every element of $S$.
For example, the function $F(x)= \sqrt{x}$ is only defined on non-negative real numbers.
When we want to distinguish between partial functions and  standard (i.e., non-partial) functions, we will call the latter _total_ functions.
(Note that the set of partial functions is a proper superset of the set of total functions; i.e., a partial function is allowed to be defined on all its input elements.)
Also, when we want to emphasize that a function $f$ from $A$ to $B$ might not be total, we will write $f: A \rightarrow_p B$.
We can think of a partial function $F$ from $S$ to $T$ also as a total function from $S$ to $T \cup \{ \bot \}$ where $\bot$ is some special "failure symbol", and so instead of saying that $F$ is undefined at $x$, we can say that $F(x)=\bot$.


### Graphs { #graphsec }

_Graphs_ are ubiquitous in Computer Science, and  many other fields as well.
They are used to model a variety of data types including social networks, road networks, deep nueral nets, gene interactions, correlations between observations, and a great many more.
The formal definitions of graphs are below, but if you have not encountered them before then I urge you to read up on them in one of the sources linked above.
Graphs come in two basic flavors: _undirected_ and _directed_.^[It is possible, and sometimes useful, to think of an undirected graph as simply a  directed graph with  the special property that for every pair $u,v$ either both the edges $\overrightarrow{u v}$ and $\overleftarrow{u v}$ are present or neither of them is. However, in many settings there is  a significant difference between  undirected and directed graphs, and so it's typically best to think of them as separate categories.]

__Undirected graphs.__ An _undirected graph_ $G = (V,E)$ consists of a set $V$ of _vertices_ and a set $E$ of edges.
Every edge is a size two subset of $V$.
We say that two vertices $u,v \in V$ are _neighbors_, denoted by $u \sim v$, if the edge $\{u,v\}$ is in $E$.
The _degree_ of $u$ is the number of neighbors it has.
A _path_ in the graph is a tuple $(u_0,\ldots,u_k) \in V^k$, for some $k>0$ such that $u_{i+1}$ is a neighbor of $u_i$ for every $i\in [k]$.
A _simple path_ is a path $(u_0,\ldots,u_{k-1})$ where all the $u_i$'s are distinct.
A _cycle_ is a path $(u_0,\ldots,u_k)$ where $u_0=u_{k}$.
We say that two vertices $u,v\in V$ are _connected_ if either $u=v$ or there is a path from $(u_0,\ldots,u_k)$ where $u_0=u$ and $u_k=v$.
We say that the graph $G$ is _connected_ if every  pair of vertices in it is connected.

Here are some basic facts about undirected graphs. We give some informal arguments below, but leave the full proofs as exercises. (The proofs can also be found in most basic texts on  graph theory.)

> # {.lemma #degreesegeslem}
In any undirected graph $G=(V,E)$, the sum of the degrees of all vertices is equal to twice the number of edges.

[edgreesegeslem](){.ref} can be shown by seeing that every edge $\{ u,v\}$ contributes twice to the sum of the degrees (once for $u$ and the second time for $v$.)

> # {.lemma #conntranslem}
The connectivity relation is _transitive_, in the sense that if $u$ is connected to $v$, and $v$ is connected to $w$, then $u$ is connected to $w$.

[conntranslem](){.ref} can be shown by simply attaching a path of the form $(u,u_1,u_2,\ldots,u_{k-1},v)$ to a path of the form $(v,u'_1,\ldots,u'_{k'-1},w)$ to obtain the path $(u,u_1,\ldots,u_{k-1},v,u'_1,\ldots,u'_{k'-1},w)$ that connects $u$ to $w$.


> # {.lemma #simplepathlem}
For every undirected graph $G=(V,E)$ and connected pair $u,v$, the shortest path from $u$ to $v$ is simple.
In particular, for every connected pair there exists a simple path that connects them.

[simplepathlem](){.ref} can be shown by "shortcutting" any non simple path of the form $(u,u_1,\ldots,u_{i-1},w,u_{i+1},\ldots,u_{j-1},w,u_{j+1},\ldots,u_{k-1},v)$ where the same vertex $w$ appears in both the $i$-th and $j$-position, to obtain the shorter path $(u,u_1,\ldots,u_{i-1},w,u_{j+1},\ldots,u_{k-1},v)$.

> # { .pause }
If you haven't seen these proofs before, it is indeed a great exercise to transform the above informal exercises into fully rigorous proofs.


__Directed graphs.__ In a _directed graph_ $G=(V,E)$, the set $E$ is a set of _ordered_ pairs, and so each edge is a pair $(u,v)$, which we often denote as $\overrightarrow{u v}$.
If the edge $\overrightarrow{u v}$ is present in the graph then we say that $v$ is an _out-neighbor_ of $u$ and $u$ is an _in-neigbor_ of $v$.
Note that a directed graph might contain both $\overrightarrow{u v}$ and $\overrightarrow{v u}$ in which case $u$ will be both an in-neighbor and an out-neighbor of $v$ and vice versa.
The _in-degree_ of $u$ is the number of in-neighbors it has, and the _out-degree_ of $v$ is the number of out-neighbors it has.
A _path_ in the graph is a tuple $(u_0,\ldots,u_k) \in V^k$, for some $k>0$ such that $u_{i+1}$ is an out-neighbor of $u_i$ for every $i\in [k]$.
As in the undirected case, a _simple path_ is a path $(u_0,\ldots,u_{k-1})$ where all the $u_i$'s are distinct and a  _cycle_ is a path $(u_0,\ldots,u_k)$ where $u_0=u_{k}$.
One type of directed graphs we often care about is _directed acyclic graphs_ or _DAGs_, which, as their name implies, are directed graphs without any cycles.

The lemmas we mentioned above have analogs for directed graphs.
We again leave the proofs (which are essentially identical to their undirected analogs) as exercises for the reader:

> # {.lemma #diredgreesegeslem}
In any directed graph $G=(V,E)$, the sum of the in-degrees  is equal to the sum of the out-degrees, which is equal to the number of edges.


> # {.lemma #dirconntranslem}
In any directed graph $G$, if there is a path from $u$ to $v$ and a path from $v$ to $w$, then there is a path from $u$ to $w$.


> # {.lemma #dirsimplepathlem}
For every directed graph $G=(V,E)$ and a  pair $u,v$ such that there is a path from $u$ to $v$, the _shortest path_ from $u$ to $v$ is simple.



### Logic operators and quantifiers.

If $P$ and $Q$ are some statements that can be true or false, then $P$ AND $Q$ (denoted as $P \wedge Q$) is the statement that is true if and only if both $P$ _and_ $Q$ are true, and $P$ OR $Q$ (denoted as $P \vee Q$) is the statement that is true if and only if either $P$ _or_ $Q$ is true.
The _negation_ of $P$, denoted as $\neg P$ or $\overline{P}$, is the statement that is true if and only if $P$ is false.

Suppose that $P(x)$ is a statement that depends on some _parameter_  $x$ (also sometimes known as an _unbound_ variable) in the sense that for every instantiation of $x$ with a value from some set $S$, $P(x)$ is either true or false.
For example, $x>7$ is a statement that is not a priori true or false, but does become true or false whenever we instantiate $x$ with some real number.
In such case we denote by  $\forall_{x\in S} P(x)$  the statement that is true if and only if $P(x)$ is true _for every_ $x\in S$.
We denote by  $\exists_{x\in S} P(x)$  the statement that is true if and only if _there exists_ some $x\in S$ such that $P(x)$ is true.

For example, the following is a formalization of the true statement that there exists a natural number $n$ larger than $100$ that is not divisble by $3$:

$$
\exists_{n\in \N} (n>100) \wedge \left(\forall_{k\in N} k+k+k \neq n\right) \;.
$$

### Quantifiers for summations and products { #secquantifiers }

The following shorthands for summing up or taking products of several numbers are often convenient.
If $S = \{s_0,\ldots,s_{n-1} \}$ is a finite set and  $f:S \rightarrow \R$ is a function, then we write $\sum_{x\in S} f(x)$ as shorthand for

$$
f(s_0) + f(s_1) + f(s_2) + \ldots + f(s_{n-1}) \;,
$$

and $\prod_{x\in S} f(x)$ as shorthand for

$$
f(s_0) \cdot f(s_1) \cdot f(s_2) \cdot \ldots \cdot f(s_{n-1}) \;.
$$

For example, the sum of the squares of all numbers from $1$ to $100$ can be written as

$$
\sum_{i\in \{1,\ldots,100}} i^2 \;. \label{eqsumsquarehundred}
$$

Since summing up over intervals of integers is so common, there is  a special notation for it, and for every two integers $a \leq b$,  $\sum_{i=a}^b f(i)$ denotes $\sum_{i\in S} f(i)$ where $S =\{ x\in \Z : a \leq x \leq b \}$.
Hence we can write the sum [eqsumsquarehundred](){.eqref} as

$$
\sum_{i=1}^{100} i^2 \;.
$$





### Asymptotics and big-Oh notation

It is often very cumbersome to describe precisely  quantities such as running time and is also not needed, since we are typically mostly interested in the "higher order terms".
That is, in  understanding the _scaling behavior_ of the quantity as the input variable grows.
For example, as far as running time goes, the difference between an $n^5$-time algorithm and an $n^2$-time one is much more significant than the difference between an $100n^2 + 10n$ time algorithm and an $10n^2$
For this purpose, Oh notation is extremely useful as a way to "declutter" our text and focus our attention on what really matters.
For example, using Ph notation, we can say that both $100n^2 + 10n$ and $10n^2$ are simply $\Theta(n^2)$ (which informally means "the same up to constant factors"), while $n^2 = o(n^5)$ (which informally means that $n^2$ is "much smaller than" $n^5$).


Generally (though still informally), if $F,G$ are two functions mapping natural numbers to non-negative reals,  then "$F=O(G)$" means that  $F(n) \leq G(n)$ if we don't care about constant factors, while  "$F=o(G)$" means that $F$ is much smaller than $G$, in the sense that no matter by what constant factor we multiply $F$, if we take $n$ to be large enough then  $G$ will be bigger (for this reason, sometimes $F=o(G)$ is written as $F \ll G$).
We will write $F= \Theta(G)$ if $F=O(G)$ and $G=O(F)$, which one can think of as saying that $F$ is the same as $G$ if we don't care about constant factors.
More formally, we define Big Oh notation as follows:


> # {.definition title="Big Oh notation" #bigohdef}
For $F,G: \N \rightarrow \R_+$, we define $F=O(G)$ if there exist numbers $a,N_0 \in \N$ such that $F(n) \leq a\cdot G(n)$ for every $n>N_0$.
We define $F=\Omega(G)$ if $G=O(F)$.
>
We write $F =o(G)$ if for every $\epsilon>0$ there is some $N_0$ such that $F(n) <\epsilon G(n)$ for every $n>N_0$.
We write $F =\omega(G)$ if $G=o(F)$.
We write $F= \Theta(G)$ if $F=O(G)$ and $G=O(F)$.


We can also use the notion of _limits_ to define big and little oh notation.
You can verify that $F=o(G)$ (or, equivalently, $G=\omega(F)$) if and only if $\lim\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)} = 0$.
Similarly, if the limit $\lim\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)}$ exists and is a finite number then $F=O(G)$.
If you are familiar with the notion of _supremum_, then you can verify that $F=O(G)$ if and only if $\limsup\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)} < \infty$.





Using the equality sign for Oh notation is extremely common, but is somewhat of a misnomer, since a statement such as $F = O(G)$ really means that $F$ is in the set $\{ G' : \exists_{N,c} \text{ s.t. } \forall_{n>N} G'(n) \leq c G(n) \}$.
For this reason, some texts write $F \in O(G)$ instead of $F = O(G)$.
If anything, it would have made more sense use _inequalities_ and  write $F \leq O(G)$ and $F \geq \Omega(G)$, reserving equality for $F = \Theta(G)$,  but by now the equality notation is quite firmly entrenched.
Nevertheless, you should remember that a statement such as $F = O(G)$ means that $F$ is "at most" $G$ in some rough sense when we ignore constants, and a statement such as $F = \Omega(G)$ means that $F$ is "at least" $G$ in the same rough sense.

It's often convenient to use "anonymous functions" when using Oh notation and to emphasize the input parameter to the function.
For example, when we write a statement such as $F(n) = O(n^3)$, we mean that  $F=O(G)$ where $G$ is the function defined by $G(n)=n^3$.


__Some "rules of thumbs" for big Oh notation:__
There are some simple heuristics that can help when trying to compare two functions $F$ and $G$:

* Multiplicative constants don't matter in Oh notation, and so if $F(n)=O(G(n))$ then $100F(n)=O(G(n))$.

* When adding two functions, we only care about the larger one. For example, for the purpose of Oh notation, $n^3+100n^2$ is the same as $n^3$, and in general in any polynomial, we only care about the larger exponent.

* For every two constants $a,b>0$, $n^a = O(n^b)$ if and only if $a \leq b$, and $n^a = o(n^b)$ if and only if $a<b$. For example, combining the two observations above, $100n^2 + 10n + 100 = o(n^3)$.

* Polynomial is always smaller than exponential: $n^a = o(2^{n^\epsilon})$ for every two constants $a>0$ and $\epsilon>0$ even if $\epsilon$ is much smaller than $a$. For example, $100n^{100} = o(2^{\sqrt{n}})$.

* Similarly, logarithmic is always smaller than polynomial: $(\log n)^a$ (which we write as $\log^a n$) is $o(n^\epsilon)$ for every two constants $a,\epsilon>0$. For example, combining the observations above, $100n^2\log^100 n = o(n^3)$.

In most (though not all!) cases we use Oh notation, the constants hidden by it are not too huge and so on an intuitive level, you can think of $F=O(G)$ as saying something like $F(n) \leq 1000 G(n)$ and $F=\Omega(G)$ as saying something $F(n) \geq 0.001 G(n)$.


## Proofs


In this course we will be interested in understanding the truth of assertions such as _"there is no efficient algorithm to find the prime factors of a given number"_.^[Actually, scientists currently do not know if this assertion is true or false, but we will see that settling it in either direction has very interesting applications touching on areas as far apart as Internet security and quantum mechanics.]

You cannot run experiments to prove the _non existence_ of an algorithm.
Thus, our only way to show that an assertion such as the above is true is to use _mathematical proofs_.
In fact, even before asking if this assertion is true, we will need to use _mathematical definitions_ to make this a precise statement that is either true or false.
So you see that our main tools in this course will be mathematical proofs and definitions.^[The [CS 121 website](http://www.boazbarak.org/cs121/background/) contains links to various resources which can help students catch up on this material.]

Many people think of mathematical proofs as a sequence of logical deductions that starts from some axioms and ultimately arrives at a conclusion.
In fact, some dictionaries [define](http://www.thefreedictionary.com/mathematical+proof) proofs that way.
This is not entirely wrong, but in reality a mathematical proof of a statement X is simply an argument that convinces the reader that X is true beyond a shadow of a doubt.
To produce such a proof you need to:

1. Understand precisely what X means.

2. Convince  _yourself_ that X is true.

3. Write your reasoning down in plain, precise and concise English (using formulas or notation only when they help clarity).

In many cases, Step 1 is the most important one. Understanding what a statement means is often more than halfway towards understanding why it is true.
In Step 3, to convince the reader beyond a shadow of a doubt, we will often want to  break down the reasoning to "basic steps", each of which is simple enough to be "self evident" and the combination of all steps yields the desired statement.
(This "breaking down" can indeed be often thought of as proceeding in a sequence of  logical deduction from some axioms.)

### Proofs and programs

There is a great deal of similarity between the process of writing _proofs_ and that of writing _programs_, and doing both well requires a similar set of skills.  
Writing a _program_ involves:

1. Understanding what is the _task_ we want the program to achieve.

2. Convincing _yourself_ that the task can be achieved by a computer, perhaps by planning on a whiteboard or notepad how you will break it up to simpler tasks.

3. Converting this plan into code that a compiler or interpreter can understand, by breaking up each task into a sequence of the basic operations of some programming language.

In programs as in proofs, step 1 is often the most important one.
A key difference is that the reader for proofs is a human being and for programs is a compiler.^[This difference might be eroding with time, as more proofs are being written in a _machine verifiable form_ and progress in artificial intelligence allows expressing programs in more human friendly ways, such as "programming by example". Interestingly, much of the progress in automatic proof verification and proof assistants relies on a much deeper correspondence between _proofs_ and _programs_. We _might_ see this correspondence later in this course.]
Thus our emphasis is on _readability_ and having a _clear logical flow_ for the proof (which is not a bad idea for programs as well..).
For the purposes of this course, you can think of the human reader as an intelligent but highly skeptical reader, that will "call foul" at every step that is not well justified.


## Extended example: graph connectivity

To illustrate these ideas, let us consider the following example of a true theorem:

> # {.theorem title="Minimum edges for connected graphs" #graphconthm}
Every connected undirected graph of $n$ vertices has at least $n-1$ edges.


We are going to take our time to understand how one would come up with a  proof for [graphconthm](){.ref}, and how to write such a proof down.
This will not be the shortest way to prove this theorem, but hopefully following this process will give you some general insights on  reading, writing, and discovering mathematical proofs.

Before trying to prove [graphconthm](){.ref},  we need to understand what it means.
Let's start with the terms in the theorems.
We defined undirected graphs and the notion of connectivity in [graphsec](){.ref} above.
In particular, an undirected graph $G=(V,E)$ is _connected_ if for every pair $u,v \in V$, there is a path $(u_0,u_1,\ldots,u_k) \in  V^{k+1}$ such that $u_0=u$, $u_k=v$, and $\{ u_i,u_{i+1} \} \in E$ for every $i\in [k]$.

> # { .pause }
It is crucial that at this point you pause and verify that you completely understand the definition of connectivity. Indeed, you should make a habit of pausing after any statement of a theorem, even before looking at the proof, and verifying that you  understand all the terms that the theorem refers to.

To prove [graphconthm](){.ref} we need to show that there is no $2$-vertex connected graph with fewer than $1$ edges, $3$-vertex connected graph with fewer than $2$ edges, and so on and so forth.
One of the best ways to prove a theorem is to first try to _disprove it_.
By trying to come up with a counterexample, we often understand why it could not be false.
For example, if you try to draw a $4$-vertex graph with only two edges, you can see that there are basically only two  choices for such a graph as depicted in [figurefourvertexgraph](){.ref}, and in both  there will remain a vertex that is not connected.


![In a four vertex graph with two edges, either both edges have a shared vertex or they don't. In both cases the graph will not be connected.](../figure/4graph2edge.png){#figurefourvertexgraph .class width=300px height=300px}

In fact, we can see that if we have a budget of $2$ edges and we choose some vertex $u$, we will not be able to connect to $u$ more than two other vertices, and similarly with a budget of $3$ edges we will not be able to connect to $u$ more than three other vertices.
We can keep trying to draw such examples until we convince ourselves that the theorem is probably true, at which point we want to see how we can _prove_ it.


> # { .pause }
If you have not seen the proof of this theorem before (or don't remember it), this would be an excellent point to pause and try to prove it yourself.

There are several ways to approach this proof, but one version is to start by proving it for small graphs, such as graphs with 2,3 or 4 edges, for which we can check all the cases, and then try to extend the proof for larger graphs.
The technical term for this proof approach is _proof by induction_.

__Mathematical induction.__
_Induction_ is simply an application of the self-evident  [Modus Ponens](https://en.wikipedia.org/wiki/Modus_ponens) rule that says that if: \

 __(a)__ $P$ implies $Q$ \

and \

__(b)__ $P$ is true \
then $Q$ is true.

In the setting of proofs by induction we typically have a statement $Q(k)$ about an integer $k$, and we prove that: \

__(a)__ For every $k>0$, if $Q(0),\ldots,Q(k-1)$ are all true then $Q(k)$ is true \

 and \

 __(b)__ $Q(0)$ is true. \

(Usually proving __(a)__ is the hard part, though there are examples where the "base case" __(b)__ is quite subtle.)
By repeatedly applying Modus Ponens, we can see that $Q(1)$ is true, $Q(2)$ is true, etc.. and this implies that  $Q(k)$ is true for every $k$.

There are several ways to use induction to prove  [graphconthm](){.ref}.
One possibility is to follow our intuition above that with a budget of $k$ edges, we cannot connect to a vertex more than $k-1$ other vertices.
That is, we will define the statement $Q(k)$ as follows: "For every graph $G=(V,E)$ with at most $k$ edges and every $u\in V$, the number of vertices that are connected to $u$ is at most $k+1$". (Recall that $u$ is always connected to itself.)
Note that $Q(n-2)$ implies our theorem, since it means that in an $n$ vertex graph of $n-2$ edges, there would be at most $n-1$ vertices  that are connected to $u$, and hence in particular there would be _some_ vertex that is not connected to $u$.
More formally, if we define, given any undirected graph $G$ and vertex $u$ of $G$, the set $C_G(u)$ to contain all  vertices connected to $u$, then the statement $Q(k)$ is that for every undirected graph $G=(V,E)$ with $|E|=k$ and $u\in V$,  $|C_G(u)| \leq k+1$.

To prove that $Q(k)$ is true for every $k$ by induction, we will first prove __(a)__ that $Q(0)$ is true, and then prove __(b)__ that if $Q(0),\ldots,Q(k-1)$ are true then $Q(k)$ is true as well.
In fact, we will prove the stronger statement __(b')__ that if $Q(k-1)$ is true then $Q(k)$ is true as well.
(This is a stronger statement because we prove the same conclusion from a weaker assumption.)
Thus, if we show both __(a)__ and __(b')__ then we complete the proof of [graphconthm](){.ref}.


Proving __(a)__  (i.e., the "base case") is actually quite easy. The statement $Q(0)$ says that if $G$ has zero edges, then $|C_G(u)|=1$, but this is clear because in a graph  with zero edges, $u$ is only connected to itself.
The heart of the proof is, as typical with induction proofs, is in proving a statement such as __(b')__ (or even the weaker statement __(b)__).
Since we are trying to prove an _implication_, we can _assume_ the so-called "inductive hypothesis" that $Q(k-1)$ is true  and need to prove from this assumption that $Q(k)$ is true.
So, suppose that $G=(V,E)$ is a graph of $k$ edges, and $u\in V$.
Since we can use induction, a natural approach would be to remove an edge $e\in E$ from the graph to create a new graph $G'$ of $k-1$ edges.
We can use the induction hypothesis to argue that $|C_{G'}(u)| \leq k$.
Now if we could only argue that removing the edge $e$ reduced the connected component of $u$ by at most a single vertex,  then we would be done, as we could argue that $|C_G(u)| \leq |C_{G'}(u)|+1 \leq k+1$.

Alas, this might not be the case.
It could be that removing  a single edge $e$ will greatly reduce the size of $C_{G}(u)$.
For example that edge might be a "bridge" between two large connected components; such a situation is illustrated in  [effectofoneedgefig](){.ref}.

![Removing a single edge $e$ can greatly decrease the number of vertices that are connected to a vertex $u$.](../figure/effectofoneedge.png){#effectofoneedgefig .class width=300px height=300px}

This might seem as a real stumbling block, and at this point we might go back to the drawing board to see if perhaps the theorem is false after all.
However, if we look at various concrete examples, we see that in any concrete example, there is always a "good" choice of an edge,  adding which will  increase the component connect to $u$ by at most one vertex.
The crucial observation is that this always holds if we choose an edge  $e = \{ s, w\}$ where $w \in C_G(u)$ has degree one in the graph $G$, see [degoneconnectivityfig](){.ref}.
The reason is simple.
Since every path from $u$ to $w$ must pass through $s$ (which is $w$'s only neighbor), removing the edge $\{ s,w \}$ merely has the effect of disconnecting $w$ from $u$, and hence $C_{G'}(u) = C_G(u) \setminus \{ w \}$ and in particular $|C_{G'}(u)|=|C_G(u)|-1$, which is exactly the condition we needed.


![Removing an edge $e=\{s,w\}$ where $w\in C_G(u)$ has degree one removes only $w$ from $C_G(u)$. ](../figure/addingdegreeone.png){#addingdegreeonefig .class width=300px height=300px}


Now the question is whether there will always be a degree one vertex in $C_G(u) \setminus \{u \}$.
Of course generally we are not guaranteed that a graph would have a degree one vertex, but we are not dealing with a general graph here but rather a graph with a small number of edges.
We can assume that $|C_G(u)| > k+1$ (otherwise we're done) and each vertex in $C_G(u)$ must have degree at least one (as otherwise it would not be connected to $u$).
Thus, the only case where there is no vertex $w\in C_G(u) \setminus \{u\}$  of degree one, is when the degrees of all vertices in $C_G(u)$ are at least $2$.
But then by [degreesegeslem](){.ref} the number of edges in the graph is at least $\tfrac{1}{2}\cdot 2 \cdot (k+1)>k$, which contradicts our assumption that the graph $G$ has at most $k$ edges.
Thus we can conclude that either $|C_G(u)| \leq k+1$  (in which case we're done) or there is a degree one vertex $w\neq u$ that is connected to $u$.
By removing the single edge $e$ that touches $w$, we obtain a $k-1$ edge graph $G'$ which (by the inductive hypothesis) satisfies $|C_{G'}(u)| \leq k$, and hence $|C_G(u)|=|C_{G'}(u) \cup \{ w \}| \leq k+1$.


### Writing down the proof

All of the above was a discussion of how we _discover_ the proof, and convince _ourselves_ that the statement is true.
However, once we do that, we still need to write it down.
When writing the proof,   we use the benefit of hindsight, and try to streamline what was a messy journey into a linear and easy-to-follow flow of logic that starts with the word __Proof:__ and ends with __QED__.
All our discussions, examples and digressions can be very insightful, but we keep them outside the space delimited between these two words, where (to use the words of this [excellend handout](http://web.stanford.edu/class/cs103/handouts/110%20Proofwriting%20Checklist.pdf)) "every sentence must be load bearing".
Just like we do in programming, we can break the proof into little "subroutines" or "functions" (known as _lemmas_ or _claims_ in math language), which will be smaller statements that help us prove the main result.
However, it should always be crystal-clear to the reader in what stage we are of the proof.
That is, just like it should always be clear to which function a line of code belongs to, it should always be clear whether a sentence in the overall proof is part of the proof of an intermediate result, or part of the argument showing that this intermediate result implies the theorem.
Sometimes we highlight this partition by noting after each occurence of  __QED__ to which lemma or claim it belongs.


Let us see how the proof of [graphconthm](){.ref} looks in this streamlined fashion.
We start by repeating the theorem statement

> # {.theorem title="Minimum edges for connected graphs (restated)" #graphconthmpf}
Every connected undirected graph of $n$ vertices has at least $n-1$ edges.

> # {.proof data-ref="graphconthmpf"}
The proof will follow from the following lemma:
>
>> # {.lemma #graphcontlem}
>For every $k\in \N$, undirected graph $G=(V,E)$ of at most $k$ edges, and $u\in V$, the number of vertices connected to $u$ in $G$ is at most $k+1$.
>
>We start by showing that [graphcontlem](){.ref} implies the theorem:
>
>>__Proof of [graphconthmpf](){.ref} from [graphcontlem](){.ref}:__ We will show that for undirected graph $G=(V,E)$ of $n$ vertices and at most $n-2$ edges, there is a pair $u,v$ of vertices that are disconnected in $G$. let $G$ be such a graph and $u$ be some vertex of $G$. By [graphcontlem](){.ref}, the number of vertices connected to $u$ is at most $n-1$, and hence (since $|V|=n$) there is a vertex $v\in V$ that is not connected to $u$, thus completing the proof. __QED (Proof of [graphconthm](){.ref} from [graphcontlem](){.ref})__
>
>We now turn to proving [graphcontlem](){.ref}. Let $G=(V,E)$ be an undirected graph of $k$ vertices and $u\in V$. We define $C_G(u)$ to be the set of vertices connected to $u$. To complete the proof of  [graphcontlem](){.ref}, we need to prove that $|C_G(u)| \leq k+1$. We will do so by induction on $k$.
>
>The _base_ case that $k=0$ follows since in a graph with zero edges, $u$ is only connected to itself.
>
>Now suppose that [graphcontlem](){.ref} is true for $k-1$ and we will prove it for $k$.
>Let $G=(V,E)$ and $u\in V$ be as above, where $|E|=k$, and suppose (towards a contradiction) that $|C_G(u)| \geq k+2$. Let $S = C_G(u) \setminus \{u \}$.
Denote by $deg(v)$ the degree of any vertex $v$.
By [degreesegeslem](){.ref}, $\sum_{v\in S} deg(v) \leq \sum_{v\in V} deg(v) = 2|E|=2k$.
Hence in particular, under our assumption that $|S|+1=|C_G(u)| \geq k+2$, we get that $\tfrac{1}{|S|}\sum_{v\in S} deg(v) \leq 2k/(k+2)< 2$.
In other words, the _average_ degree of a vertex in $S$ is smaller than $2$, and hence in particular there is some vertex $w\in S$ with degree smaller than $2$.
Since $w$ is connected to $u$, it must have degree at least one, and hence (since $w$'s degree is smaller than two) degree exactly one, or in other words, $w$ has a single neighbor which we denote by $s$.
Let $G'$ be the graph obtained by removing the edge $\{ s, w\}$.
Since $G'$ has at most $k-1$ edges, by the inductive hypothesis we can assume that $|C_{G'}(u)| \leq k$.
The proof of the lemma will be concluded by showing the following claim:
>
>>__Claim:__ Under the above assumptions, $|C_G(u)| \leq |C_{G'}(u)|+1$.
>
>>__Proof of claim:__ This will follow by showing that $C_{G'}(u) \supseteq C_G(u) \setminus \{ w \}$. Indeed, if $v \neq w$ is connected to $u$, then by [simplepathlem](){.ref} there must be some _simple_ path $(t_0,t_1,\ldots,t_{i-1},t_i)$ in the graph $G$ where $t_0=u$ and $t_i=v$. But $w$ cannot belong to this path, since $w \neq \{u,v \}$, and $w$ cannot equal one of the $t_j$'s for $0 < j < i$ since $w$ has only a single neighbor $s$, and hence if $w=t_j$ then it would have to hold that $s=t_{j-1}=t_{j+1}$, contradicting the simplicity of the path.
Hence the path from $u$ to $v$ is also a path in the graph $G'$, which means that $v \in C_{G'}(u)$, which is what we wanted to prove. __QED (claim)__
>
>The claim implies [graphcontlem](){.ref} since by the inductive assumption, $|C_{G'}(u)| \leq k$, and hence by the claim $|C_G(u)| \leq k$, which is what we wanted to prove. This concludes the proof of [graphcontlem](){.ref} and hence also of [graphconthmpf](){.ref}. __QED ([graphcontlem](){.ref})__, __QED ([[graphconthmpf](){.ref}](){.ref})__

> # { .pause }
Reading a proof is no less of an important skill than producing one.
In fact, just like understanding code, it is a highly non-trivial skill in itself.
Therefore I strongly suggest that you re-read the above proof, asking yourself at every sentence whether the assumption it makes are justified, and whether this sentence truly demonstrates what it purports to achieve.

The proof above used the observation that if the _average_ of some $n$ numbers $x_0,\ldots,x_{n-1}$ is at most $X$, then there must _exists_ at least a single number $x_i \leq X$. (In the proof the numbers were the degrees of vertices in $S$.)
This is known as the _averaging principle_, and despite its simplicity, it is often extremely useful.



## Proof writing style

A mathematical proof is a piece of writing, but it is a specific genre of writing with certain conventions and preferred styles.
As in any writing, practice makes perfect, and it is also important to revise your drafts for clarity.

In a proof for the statement $X$, all the text between the words __"Proof:"__ and __"QED"__ should be focused on establishing that $X$ is true.
Digressions, examples, or ruminations should be kept outside these two words, so they do not confuse the reader.
The proof should have a clear logical flow in the sense that every sentence or equation in it should have some purpose and it should be crystal-clear to the reader what this purpose is.
When you write a proof, for every equation or sentence you include, ask yourself:

1. Is this sentence or equation stating that some statement is true?

2. If so, does this statement   follow from the previous steps,  or are we going to establish it in the next step?

3. What is the _role_ of this sentence  or equation? Is it one step towards proving the original statement, or is it a step towards proving some intermediate claim that you have stated before?

4. Finally, would the answers to questions 1-3 be clear to the reader? If not, then you should reorder, rephrase or add explanations.


Some helpful resources on mathematical writing include [this handout by Lee](https://sites.math.washington.edu/~lee/Writing/writing-proofs.pdf), [this handout by Hutching](https://math.berkeley.edu/~hutching/teach/proofs.pdf), as well as several of the excellent handouts in [Stanford's CS 103 class](http://web.stanford.edu/class/cs103/).


### Patterns in proofs

Just like in programming, there are several common patterns of proofs that occur time and again.
Here are some examples:

__Proofs by contradiction:__ One way to prove that $X$ is true, is to show that if $X$ was false then we would get a contradiction as a result. Such proofs often start with a sentence such as "Suppose, towards a contradiction, that $X$ is false" and end with deriving some contradiction (such as a violation of one of the assumptions in the theorem statement).
Our proof of [inf-primes-thm](){.ref}  was obtained by assuming, toward a contradiction, that there are finitely many primes, and deriving from this assumption an equality of the form $A= B$ where $A$ is a whole number and $B$ has a fractional component.

__Proofs of a universal statement:__ Often we want to prove a statement $X$ of the form "Every object of type $O$ has property $P$." Such proofs often start with a sentence such as "Let $o$ be an object of type $O$" and end by showing that $o$ has the property $P$.
Here is a simple example:

> # {.lemma }
For every natural number $n\in N$, either $n$ or $n+1$ is even.


> # {.proof}
Let $n\in N$ be some number.
If $n/2$ is a whole number then we are done, since then $n=2(n/2)$ and hence it is even.
Otherwise, $n/2+1/2$ is a whole number, and hence $2(n/2+1/2)=n+1$ is even.

__Proofs of an implication:__ Another common case is that the statement $X$ has the form "$A$ implies $B$". Such proofs often start with a sentence such as "Assume that $A$ is true" and end with a derivation of $B$ from $A$.
Here is a simple example:

> # {.lemma }
If $b^2 \geq 4ac$ then there is a solution to the quadratic equation $ax^2 + bx + c =0$.

> # {.proof }
Suppose that $b^2 \geq 4ac$.
Then $d = b^2 - 4ac$ is a non-negative number and hence it has a square root $s$.
Thus $x = (-b+s)/(2a)$ satisfies
$$
ax^2 + bx + c = a(-b+s)^2/(4a^2) + b(-b+s)/(2a) + c = (b^2-2bs+s^2)/(4a)+(-b^2+bs)/(2a)+c \;. \label{eq:quadeq}
$$
Rearranging the terms of [eq:quadeq](){.eqref} we get
$$
s^2/(4a)+c- b^2/(4a) = (b^2-4ac)/(4a) + c - b^2/(4a) = 0
$$

If a statement has the form "$A$ holds if and only if $B$ holds" then we need to prove both that $A$ implies $B$ and that $B$ implies $A$.

__Proofs by combining intermediate claims:__
When a proof is more complex, it is often helpful to break it apart into several steps.
That is, to prove the statement $X$, we might first prove statements $X_1$,$X_2$, and $X_3$ and then prove that $X_1 \wedge X_2 \wedge X_3$ implies $X$.^[As mentioned below, $\wedge$ denotes the logical AND operator.]
Our proof of [graphconthm](){.ref} had this form.

__Proofs by induction:__ We can think of such proofs as a variant of the above, where we have an unbounded number of intermediate claims $X_0,X_2,\ldots,X_k$, and we prove that $X_0$ is true, as well that $X_0$ implies $X_1$, and that $X_0  \wedge X_1$ implies $X_2$, and so on and so forth.
The website for CMU course 15-251 contains a [useful handout](http://www.cs.cmu.edu/~./15251/notes/induction-pitfalls.pdf) on potential pitfalls when making proofs by induction.


## Non-standard notation

Most of the notation we discussed above is standard and is used in most mathematical texts.
The main points where we diverge are:

* We index the natural numbers $\N$ starting with $0$ (though many other texts, especially in computer science, do the same).

* We also index the set $[n]$ starting with $0$, and hence define it as $\{0,\ldots,n-1\}$. In most texts it is defined as $\{1,\ldots, n \}$. Similarly, we index coordinates of our strings starting with $0$, and hence a string $x\in \{0,1\}^n$ is written as $x_0x_1\cdots x_{n-1}$.

* We use _partial_ functions which are functions that are not necessarily  defined on all inputs. When we write $f:A \rightarrow B$ this will refer to a _total_ function unless we say otherwise. When we want to emphasize that $f$ can be  a partial function, we will sometimes write $f: A \rightarrow_p B$.

* As we will see later on in the course, we will mostly describe our computational problems in the terms of computing a _Boolean function_ $f: \{0,1\}^* \rightarrow \{0,1\}$. In contrast, most textbooks will refer to this as the task of _deciding a language_ $L \subseteq \{0,1\}^*$. These two viewpoints are equivalent, sicne for every set $L\subseteq \{0,1\}^*$ there is a corresponding  function $f = 1_L$ such that $f(x)=1$ if and only if $x\in L$. Computing _partial functions_ corresponds to the task known in the literature as a solving a _promise problem_.^[Because the language notation is so prevalent in textbooks, we will occasionally remind the reader of this correspondence.]

## Exercises

># {.exercise title="Inclusion Exclusion" #inclex }
a. Let $A,B$ be finite sets. Prove that $|A\cup B| = |A|+|B|-|A\cap B|$. \
b. Let $A_0,\ldots,A_{k-1}$ be finite sets. Prove that $|A_1 \cup \cdots \cup A_k| \geq \sum_{i=0}^{k-1} |A_i| - \sum_{0 \leq i < j < k} |A_i \cap A_j|$. \
c. Let $A_0,\ldots,A_{k-1}$ be finite subsets of $\{1,\ldots, n\}$, such that $|A_i|=m$ for every $i\in [k]$. Prove that if $k>100n$, then there exist two distinct sets $A_i,A_j$ s.t. $|A_i \cap A_j| \geq m^2/(10n)$.


> # {.exercise }
Prove that if $S,T$ are finite and $F:S \rightarrow T$ is one to one then $|S| \leq |T|$.

> # {.exercise }
Prove that if $S,T$ are finite and $F:S \rightarrow T$ is onto then $|S| \geq |T|$.


> # {.exercise }
Prove that for every finite $S,T$, there are $(|T|+1)^{|S|}$ partial functions from $S$ to $T$.




> # {.exercise }
Suppose that $\{ S_n \}_{n\in \N}$ is a sequence such that $S_0 \leq 10$ and for $n>1$ $n \leq 5 S_{\lfloor \tfrac{n}{5} \rfloor} + 2n$.
Prove by induction that  $S_n \leq 100 n \log n$ for every $n$.

> # {.exercise }
Describe the following statement in English words: $\forall_{n\in\N} \exists_{p>n} \forall{a,b \in \N} (a\times b \neq p) \vee (a=1)$.

> # {.exercise }
Prove that for every undirected graph $G$ of $100$ vertices, if every vertex has degree at most $4$, then there exists a subset $S$ of at $20$ vertices such that no two vertices in $S$ are neighbors of one another.


> # {.exercise }
Suppose that we toss three independent fair coins $a,b,c \in \{0,1\}$. What is the probability that the XOR of $a$,$b$, and $c$ is equal to $1$? What is the probability that the AND of these three values is equal to $1$? Are these two events independent?

> # {.exercise}
For every pair of functions $F,G$ below, determine which of the following relations holds: $F=O(G)$, $F=\Omega(G)$, $F=o(G)$ or $F=\omega(G)$. \
a. $F(n)=n$, $G(n)=100n$. \
b. $F(n)=n$, $G(n)=\sqrt{n}$.\
c. $F(n)=n$, $G(n)=2^{(\log (n))^2}$.\
d. $F(n)=n$, $G(n)=2^{\sqrt{\log n}}$

> # {.exercise}
Give an example of a pair of functions $F,G:\N \rightarrow \N$ such that neither $F=O(G)$ nor $G=O(F)$ holds.


## Acknowledgements
