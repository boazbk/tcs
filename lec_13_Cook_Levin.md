---
title: "NP, NP completeness, and the Cook-Levin Theorem"
filename: "lec_13_Cook_Levin"
chapternum: "14"
---

#  NP, NP completeness, and the Cook-Levin Theorem {#cooklevinchap }

> ### { .objectives }
* Introduce the class $\mathbf{NP}$  capturing a great many important computational problems \
* $\mathbf{NP}$-completeness: evidence that a problem might be intractable. \
* The $\mathbf{P}$ vs $\mathbf{NP}$ problem.


>_"In this paper we give theorems that suggest, but do not imply, that these problems, as well as many others, will remain intractable perpetually"_, Richard Karp, 1972


>_"Sad to say, but it will be many more years, if ever before we really understand the Mystical Power of Twoness... 2-SAT is easy, 3-SAT is hard, 2-dimensional matching is easy, 3-dimensional matching is hard. Why? oh, Why?"_ Eugene Lawler


## The class $\mathbf{NP}$


So far we have shown that 3SAT is no harder than Quadratic Equations, Independent Set, Maximum Cut, and Longest Path.
But to show that these problems are _computationally equivalent_ we need to give reductions in the other direction, reducing each one of these problems to 3SAT as well.
It turns out we can reduce all three problems to 3SAT in one fell swoop.


In fact, this result extends far beyond these particular problems.
All of the problems we discussed in [reductionchap](){.ref}, and a great many other problems, share the same commonality:
they are all _search_ problems, where the goal is to decide, given an instance $x$, whether there exists a _solution_ $y$ that satisfies some condition that can be verified in polynomial time.
For example, in 3SAT, the instance is a formula and the solution is an assignment to the variable; in Max-Cut the instance is a graph and the solution is a cut in the graph; and so on and so forth.
It turns out that _every_ such search problem can be reduced to 3SAT.

To make this precise, we make the following mathematical definition:
we define the class $\mathbf{NP}$ to contain all Boolean functions that correspond to a _search problem_ of the form above$-$
that is, functions that output $1$ on $x$ if and only if there exists a solution $w$ such that the pair $(x,w)$ satisfies some polynomial-time checkable condition.
Formally, $\mathbf{NP}$ is defined as follows:

![The class $\mathbf{NP}$ corresponds to problems where solutions can be _efficiently verified_.  That is, this is the class of functions $F$ such that $F(x)=1$ if there is a "solution" $w$ of length polynomial in $|x|$ that can be verified by a polynomial-time algorithm $V$. ](../figure/NPdeffig.png){#NPdeffigfig .margin  }

::: {.definition title="NP" #NP-def}
We say that $F:\{0,1\}^* \rightarrow \{0,1\}$ is in $\mathbf{NP}$ if there exists some constants $a,b \in \N$ and $V:\{0,1\}^* \rightarrow \{0,1\}$ such that $V\in \mathbf{P}$ and for every $x\in \{0,1\}^n$,
$$
F(x)=1 \Leftrightarrow \exists_{w \in \{0,1\}^{an^b}} \text{ s.t. } V(xw)=1 \;. \label{NP:eq}
$$

In other words, for $F$ to be in $\mathbf{NP}$, there needs to exist some polynomial-time computable verification function $V$, such that if $F(x)=1$ then there must exist $w$ (of length polynomial in $|x|$) such that $V(xw)=1$, and if $F(x)=0$ then for _every_ such $w$, $V(xw)=0$.
Since the existence of this string $w$ certifies that $F(x)=1$, $w$ is often referred to as a _certificate_, _witness_, or _proof_ that $F(x)=1$.
:::

See also [NPdeffigfig](){.ref} for an illustration of [NP-def](){.ref}.
The name $\mathbf{NP}$ stands for "nondeterministic polynomial time" and is used for historical reasons; see the bibiographical notes.
The string $w$ in [{NP:eq}](){.eqref} is sometimes known as a _solution_, _certificate_, or _witness_ for the instance $x$.

> ### {.remark title="$\mathbf{NP}$ and proof systems" #NPproofs}
The definition of $\mathbf{NP}$ means that for every  $F\in \mathbf{NP}$ and string $x\in \{0,1\}^*$, $F(x)=1$ if and only if there is a _short and efficiently verifiable proof_ of this fact.
That is, we can think of the function $V$ in [NP-def](){.ref} as a _verifier_ algorithm, similar to what we've seen in [godelproofdef](){.ref}.
The verifier checks whether a given string $w\in \{0,1\}^*$ is a valid proof for the statement "$F(x)=1$".
Essentially all proof systems considered in mathematics involve line-by-line checks that can be carried out in polynomial time.
Thus the heart of $\mathbf{NP}$ is asking for statements that have _short_ (i.e., polynomial in the size of the statements) proof.
Indeed, as we will see in [#chappvsnp](){.ref},  Kurt Gödel phrased the question of whether $\mathbf{NP}=\mathbf{P}$ as asking whether "the mental work of a mathematician [in proving theorems]  could be completely replaced by a machine".

> ### { .pause }
[NP-def](){.ref} is _asymmetric_ in the sense that there is a difference between an output of $1$ and an output of $0$.
You should make sure you understand why this definition does _not_ guarantee that if $F \in \mathbf{NP}$ then the function $1-F$ (i.e., the map $x \mapsto 1-F(x)$) is in $\mathbf{NP}$ as well.
In fact, it is believed that there do exist functions $F$ satisfying  $F\in \mathbf{NP}$ but $1-F \not\in \mathbf{NP}$.^[For example, as shown below, $3SAT \in \mathbf{NP}$, but the function $\overline{3SAT}$ that on input a 3CNF formula $\varphi$ outputs $1$ if and only if $\varphi$ is _not_ satisfiable is not known (nor believed) to be in  $\mathbf{NP}$.]
This is in contrast to the class $\mathbf{P}$ which (as you should verify) _does_ satisfy that if $F\in \mathbf{P}$ then $1-F$ is in $\mathbf{P}$ as well.

### Examples of $\mathbf{NP}$ functions

::: {.example title="$3SAT \in \mathbf{NP}$" #threesatinnpex}
$3SAT$ is in $\mathbf{NP}$ since for every $\ell$-variable formula $\varphi$, $3SAT(\varphi)=1$ if and only if there exists a satisfying assignment $x \in \{0,1\}^\ell$ such that $\varphi(x)=1$, and we can check this condition in polynomial time.

The above reasoning explains why $3SAT$ is in $\mathbf{NP}$,  but since this is our first example, we will now belabor the point and expand out in full formality what is the precise representation of the witness $w$ and the algorithm $V$ that demonstrate that  $3SAT$ is in  $\mathbf{NP}$.


Specifically, we can represent a 3CNF formula $\varphi$ with $k$ variables and $m$ clauses as a string of length $n=O(m\log k)$, since every one of the $m$ clauses involves three variables and their negation, and the identity of each variable can be represented using $\lceil \log_2 k \rceil$.
We assume that every variable participates in some clause (as otherwise it can be ignored) and hence that $m \geq k$, which in particular means that $n$ is larger than both $m$ and $k$.

We can represent an assignment to the $k$ variables using a $k$-length string, which, since $n > k$, can be "padded" to a string $w\in \{0,1\}^n$ in some standard way. (For example, if $y\in \{0,1\}^k$ is the assignment, we can let $w=y10^{n-k-1}$; given the string $w$ we can "read off" $y$, by chopping off all the zeroes at the end of $w$ until we encounter the first $1$, which we remove as well.)


Now checking whether a given assignment $y\in \{0,1\}^k$ satisfies a given $k$-variable 3CNF $\varphi$ can be done in polynomial time through the following algorithm $V$:

::: {.quote}

__Algorithm $V$:__

__Input:__

1. 3CNF formula $\varphi$ with $k$ variables and $m$ clauses (encoded as a string of length $n=O(m\log k))$

2. Assignment $y\in \{0,1\}^k$ to the variables of $\varphi$ (encoded using padding as a string $w \in \{0,1\}^n$)

__Output:__ $1$ if and only if $y$ satisfies $\varphi$.

__Operation:__

1. For every clause $C = (\ell_1 \vee \ell_2 \vee \ell_3)$ of $\varphi$ (where $\ell_1,\ell_2,\ell_3$ are literals), if all three literals evaluate to _false_ under the assignment $y$ then halt and output $0$.

2. Output $1$.
:::

Algorithm $V$ runs in time polynomial in the length $n$ of $\varphi$'s description as a string. Indeed there are $m$ clauses, and checking the evaluation of a literal of the form $y_i$ or $\neg y_j$ can be done by scanning the $k$-length string $y$, and hence the running time of Algorithm $V$ is at most $O(mk)=O(n^2)$, as both $k$ and $m$ are smaller than $n$.

By its definition the algorithm outputs $1$ if and only if the assignment $y$ satisfies all the clauses of the 3CNF formula $\varphi$, which means that $3SAT(\varphi)=1$ if and only if there exists some $w\in \{0,1\}^n$ such that $V(\varphi w)=1$ which is precisely the condition needed to show that  $3SAT \in \mathbf{NP}$ per [NP-def](){.ref}.
:::

::: {.remark title="Padding a witness" #padding}
The "padding trick" we used in [threesatinnpex](){.ref}  can always be used to expand a witness of length smaller than $an^b$ to a witness of exactly that length.
Therefore one can think of the condition [{NP:eq}](){.eqref} in [NP-def](){.ref}as simply stipulating that the "solution" $w$ to the problem $x$ is of length _at most_ polynomial in $|x|$.
:::

Here are some more examples for problems in $\mathbf{NP}$. For each one of these problems we merely sketch how the witness is represented and why it is efficiently checkable, but working out the details can be a good way to get more comfortable with [NP-def](){.ref}:

* $QUADEQ$ is in $\mathbf{NP}$ since for every $\ell$-variable instance of quadratic equations $E$, $QUADEQ(E)=1$ if and only if there exists an assignment $x\in \{0,1\}^\ell$ that satisfies $E$. We can check the condition that $x$ satisfies $E$ in polynomial time by enumerating over all the equations in $E$, and for each such equation $e$, plug in the values of $x$ and verify that $e$ is satisfied.

* $ISET$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $ISET(G,k)=1$ if and only if there exists a set $S$ of $k$ vertices that contains no pair of neighbors in $G$. We can check the condition that $S$ is an independent set of size $\geq k$ in polynomial time by first checking that $|S| \geq k$ and then enumerating over all edges $\{u,v \}$ in $G$, and for each such edge verify that either $u\not\in S$ or $v\not\in S$.

* $LONGPATH$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $LONGPATH(G,k)=1$ if and only if there exists a simple path $P$ in $G$ that is of length at least $k$. We can check the condition that $P$ is a simple path of length $k$ in polynomial time by checking that it has the form $(v_0,v_1,\ldots,v_k)$ where each $v_i$ is a vertex in $G$, no $v_i$ is repeated, and for every $i \in [k]$, the edge $\{v_i,v_{i+1}\}$ is present in the graph.

* $MAXCUT$ is in $\mathbf{NP}$ since for every graph $G$ and integer $k$, $MAXCUT(G,k)=1$ if and only if there exists a cut $(S,\overline{S})$ in $G$ that cuts at least $k$ edges. We can check that condition that $(S,\overline{S})$ is a cut of value at least $k$ in polynomial time by checking that $S$ is a subset of $G$'s vertices and enumerating over all the edges $\{u,v\}$ of $G$, counting those edges such that $u\in S$ and $v\not\in S$ or vice versa.


### Basic facts about $\mathbf{NP}$

The definition of $\mathbf{NP}$ is one of the most important definitions of this book, and is worth while taking the time to digest and internalize.
The following solved exercises establish some basic properties of this class.
As usual, I highly recommend that you try to work out the solutions yourself.

::: {.solvedexercise title="Verifying is no harder than solving" #PinNP}
Prove that $\mathbf{P} \subseteq \mathbf{NP}$.
:::

::: {.solution data-ref="PinNP"}
Suppose that $F \in \mathbf{P}$. Define the following function $V$: $V(x0^n)=1$ iff $n=|x|$ and $F(x)=1$. ($V$ outputs $0$ on all other inputs.)
Since $F\in \mathbf{P}$ we can clearly compute $V$ in polynomial time as well.

Let $x\in \{0,1\}^n$ be some string.
If $F(x)=1$ then $V(x0^n)=1$. On the other hand, if $F(x)=0$ then for every $w\in \{0,1\}^n$, $V(xw)=0$.
Therefore, setting $a=b=1$, we see that $V$ satisfies  [{NP:eq}](){.eqref}, and establishes that $F \in \mathbf{NP}$.
:::

::: {.remark title="$\mathbf{NP}$ does not mean non-polynomial!" #NPandNOTPolynomial}
People sometimes think that $\mathbf{NP}$ stands for "non polynomial time".
As [PinNP](){.ref} shows, this is far from the truth, and in fact every polynomial-time computable function is in $\mathbf{NP}$ as well.

If $F$ is in $\mathbf{NP}$ it certainly does _not_ mean that $F$ is hard to compute (though it does not, as far as we know, necessarily mean that it's easy to compute either).
Rather, it means that $F$ is _easy to verify_, in the technical sense of [NP-def](){.ref}.
:::

::: {.solvedexercise title="$\mathbf{NP}$ is in exponential time" #NPinEXP}
Prove that $\mathbf{NP} \subseteq \mathbf{EXP}$.
:::

::: {.solution data-ref="NPinEXP"}
Suppose that $F\in \mathbf{NP}$ and let $V$ be the polynomial-time computable function that satisfies [{NP:eq}](){.eqref} and $a,b$ the corresponding constants. Then the following is an exponential-time algorithm $A$ to compute $F$:

::: {.quote}
__Algorithm $A$:__

__Input:__ $x \in \{0,1\}^*$, let $n=|x|$

__Operation:__

1. For every $w\in \{0,1\}^{an^b}$, if $V(xw)=1$ then halt and output $1$.

2. Output $0$.
:::

Since $V \in \mathbf{P}$, for every $x\in \{0,1\}^n$, Algorithm $A$ runs in time $poly(n)2^{an^b}$.
Moreover by [{NP:eq}](){.eqref}, $A$ will output $1$ on $x$ if and only if $F(x)=1$.
:::

[PinNP](){.ref} and [NPinEXP](){.ref} together imply that

$$\mathbf{P} \subseteq \mathbf{NP} \subseteq \mathbf{EXP}\;.$$

The time hierarchy theorem ([time-hierarchy-thm](){.ref}) implies that $\mathbf{P} \subsetneq \mathbf{EXP}$ and hence at least
one of the two inclusions $\mathbf{P} \subseteq \mathbf{NP}$ or $\mathbf{NP} \subseteq \mathbf{EXP}$ is _strict_.
It is believed that both of them are in fact strict inclusions.
That is, it is believed that there are functions in $\mathbf{NP}$ that cannot be computed in polynomial time (this is the $\mathbf{P} \neq \mathbf{NP}$ conjecture)  and that there are functions $F$ in $\mathbf{EXP}$ for which we cannot even efficiently _certify_ that $F(x)=1$ for a given input $x$.^[One function $F$ that is believed to lie outside $\mathbf{NP}$ is the function $\overline{3SAT}$ defined as  $\overline{3SAT}(\varphi)= 1 - 3SAT(\varphi)$ for every 3CNF formula $\varphi$. The conjecture that $\overline{3SAT}\not\in \mathbf{NP}$ is known as the "$\mathbf{NP} \neq \mathbf{coNP}$" conjecture. It implies the $\mathbf{P} \neq \mathbf{NP}$ conjecture (can you see why?).]


We have previously informally equated the notion of $F \leq_p G$ with $F$ being "no harder than $G$" and in particular have seen in [reductionsandP](){.ref} that if $G \in \mathbf{P}$ and $F \leq_p G$, then $F \in \mathbf{P}$ as well.
The following exercise shows that if $F \leq_p G$ then it is also "no harder to verify" than $G$.
That is, regardless of whether or not it is in $\mathbf{P}$, if $G$  has the property that solutions to it can be efficiently verified, then so does $F$.


::: {.solvedexercise title="Reductions and $\mathbf{NP}$" #reductionnpex}
Let $F,G:\{0,1\}^* \rightarrow \{0,1\}$. Show that if $F \leq_p G$ and $G\in \mathbf{NP}$ then $F \in \mathbf{NP}$.
:::


::: {.solution data-ref="reductionnpex"}
Suppose that $G$ is in $\mathbf{NP}$ and in particular there exists $a,b$ and $V \in \mathbf{P}$ such that for every $y \in \{0,1\}^*$, $G(y)=1 \Leftrightarrow \exists_{w\in \{0,1\}^{a|y|^b}} V(yw)=1$.
Define $V'(x,w)=1$ iff $V(R(x)w)=1$ where $R$ is the polynomial-time reduction demonstrating that $F \leq_p G$.
Then for every $x\in \{0,1\}^*$,

$$F(x)=1 \Leftrightarrow G(R(x)) =1 \Leftrightarrow \exists_{w \in \{0,1\}^{a|R(x)|^b} V(R(x)w) = 1 \Leftrightarrow \exists_{w\in \{0,1\}^{a|R(x)|^b} } V'(x,w)=1 }$$

Since there are some constants $a',b'$ such that $|R(x)| \leq a'|x|^{b'}$ for every $x\in \{0,1\}^*$, by simple padding we can modify $V'$ to an algorithm that certifies that $F \in \mathbf{NP}$.
:::

## From $\mathbf{NP}$ to 3SAT: The Cook-Levin Theorem

We have seen everal example of problems for which we do not know if their best algorithm is polynomial or exponential, but we can show that they are in $\mathbf{NP}$.
That is, we don't know if they are easy to _solve_, but we do know that it is easy to _verify_ a given solution.
There are many, many, _many_, more examples of interesting functions we would like to compute that are easily shown to be in $\mathbf{NP}$. What is quite amazing is that if we can solve 3SAT then we can solve all of them!

The following is one of the most fundamental theorems in Computer Science:



> ### {.theorem title="Cook-Levin Theorem" #cook-levin-thm}
For every $F\in \mathbf{NP}$, $F \leq_p 3SAT$.

We will soon show the proof of [cook-levin-thm](){.ref}, but note that it immediately implies that $QUADEQ$, $LONGPATH$, and $MAXCUT$ all reduce to $3SAT$.
Combining it with the reductions we've seen in [reductionchap](){.ref}, it implies that all these problems are _equivalent!_
For example, to reduce $QUADEQ$ to $LONGPATH$, we can first reduce $QUADEQ$ to $3SAT$ using [cook-levin-thm](){.ref} and use the reduction we've seen in [longpaththm](){.ref} from $3SAT$ to $LONGPATH$.
That is, since $QUADEQ \in \mathbf{NP}$, [cook-levin-thm](){.ref} implies that $QUADEQ \leq_p 3SAT$, and  [longpaththm](){.ref}  implies that $3SAT \leq_p LONGPATH$, which by the transitivity of reductions ([transitivitylem](){.ref}) means that $QUADEQ \leq_p LONGPATH$.
Similarly, since $LONGPATH \in \mathbf{NP}$, we can use [cook-levin-thm](){.ref} and [quadeq-thm](){.ref} to show that $LONGPATH \leq_p 3SAT \leq_p QUADEQ$, concluding that $LONGPATH$ and $QUADEQ$ are computationally equivalent.


There is of course nothing special about $QUADEQ$ and $LONGPATH$ here: by combining [cook-levin-thm](){.eqref} with the reductions we saw, we see that just like $3SAT$,  _every_ $F\in \mathbf{NP}$ reduces to $LONGPATH$, and the same is true for $QUADEQ$ and $MAXCUT$.
All these problems are in some sense "the hardest in $\mathbf{NP}$" since an efficient algorithm for any one of them would imply an efficient algorithm for _all_ the problems in $\mathbf{NP}$.
This motivates the following definition:

> ### {.definition title="$\mathbf{NP}$-hardness and $\mathbf{NP}$-completeness" #NPC-def}
We say that $G:\{0,1\}^* \rightarrow \{0,1\}$ is _$\mathbf{NP}$ hard_ if for every $F\in \mathbf{NP}$,
$F \leq_p G$.
>
We say that $G:\{0,1\}^* \rightarrow \{0,1\}$ is _$\mathbf{NP}$ complete_ if $G$ is $\mathbf{NP}$ hard and $G$ is in $\mathbf{NP}$.

The Cook-Levin Theorem ([cook-levin-thm](){.ref}) can be rephrased as saying that $3SAT$ is $\mathbf{NP}$ hard, and since it is also in $\mathbf{NP}$, this means that $3SAT$ is $\mathbf{NP}$ complete.
Together with the reductions of [reductionchap](){.ref},  [cook-levin-thm](){.ref} shows that despite their superficial differences, 3SAT, quadratic equations, longest path, independent set, and maximum cut, are all $\mathbf{NP}$-complete.
Many thousands of additional problems have been shown to be $\mathbf{NP}$-complete, arising from all the sciences, mathematics, economics, engineering and many other fields.^[For some partial lists, see [this Wikipedia page](https://goo.gl/NomnoU) and [this website](https://goo.gl/nfJHWv).]

### What does this mean?

As we've seen in [PinNP](){.ref}, $\mathbf{P} \subseteq \mathbf{NP}$.
_The_ most famous conjecture in Computer Science is that this containment is _strict_.
That is, it is widely conjectured that $\mathbf{P} \neq \mathbf{NP}$.
One way to refute the conjecture that $\mathbf{P} \neq \mathbf{NP}$ is to give a polynomial-time algorithm for even a single one of the $\mathbf{NP}$-complete problems such as 3SAT, Max Cut, or the thousands of others that have been studied in all fields of human endeavors.
The fact that these problems have been studied by so many people, and yet not a single polynomial-time algorithm for any of them has been found, supports that conjecture that indeed $\mathbf{P} \neq \mathbf{NP}$.
In fact, for many of these problems (including all the ones we mentioned above), we don't even know of a $2^{o(n)}$-time algorithm!
However, to the frustration of computer scientists, we have not yet been able to prove that $\mathbf{P}\neq\mathbf{NP}$ or even rule out the existence of an $O(n)$-time algorithm for 3SAT.
Resolving whether or not $\mathbf{P}=\mathbf{NP}$ is known as the [$\mathbf{P}$ vs $\mathbf{NP}$ problem](https://en.wikipedia.org/wiki/P_versus_NP_problem).
A million-dollar prize has been [offered](http://www.claymath.org/millennium-problems/p-vs-np-problem) for the solution of this problem, a [popular book](https://www.amazon.com/dp/B00BKZYGUY) has been written, and every year a new paper comes out claiming a proof of $\mathbf{P}=\mathbf{NP}$ or $\mathbf{P}\neq\mathbf{NP}$, only to wither under scrutiny.^[The following [web page](https://goo.gl/bFHsd9) keeps a catalog of these failed attempts. At the time of this writing, it lists about 110 papers claiming to resolve the question, of which about 60 claim to prove that $\mathbf{P}=\mathbf{NP}$ and about 50 claim to prove that $\mathbf{P} \neq \mathbf{NP}$.]
The following [120 page survey of Aaronson](https://eccc.weizmann.ac.il/report/2017/004/), as well as [chapter 3 in Wigderson's upcoming book](https://www.math.ias.edu/avi/book) are excellent sources for summarizing what is known about this problem.


![The world if $\mathbf{P}\neq \mathbf{NP}$ (left) and $\mathbf{P}=\mathbf{NP}$ (right). In the former case the set of $\mathbf{NP}$-complete problems is disjoint from $\mathbf{P}$ and Ladner's theorem shows that there exist problems that are neither in $\mathbf{P}$ nor are $\mathbf{NP}$-complete. (There are remarkably few natural candidates for such problems, with some prominent examples being decision variants of problems such as integer factoring, lattice shortest vector, and finding Nash equilibria.) In the latter case that $\mathbf{P}=\mathbf{NP}$ the notion of $\mathbf{NP}$-completeness loses its meaning, as essentially all functions in $\mathbf{P}$ (save for the trivial constant zero and constant one functions) are $\mathbf{NP}$-complete.](../figure/PNPscenarios.png){#PNPscenariosfig .margin  }

One of the mysteries of computation is that people have observed a certain empirical "zero-one law" or "dichotomy" in the computational complexity of natural problems, in the sense that many natural problems are either in $\mathbf{P}$ (often in $TIME(O(n))$ or $TIME(O(n^2))$), or they are are $\mathbf{NP}$ hard.
This is related to the fact that for most natural problems, the best known algorithm is either exponential or polynomial, with not too many examples where the best running time is some strange intermediate complexity such as $2^{2^{\sqrt{\log n}}}$.
However, it is believed that there exist problems in $\mathbf{NP}$ that are neither in $\mathbf{P}$ nor are $\mathbf{NP}$-complete, and in fact a result known as "Ladner's Theorem" shows that if $\mathbf{P} \neq \mathbf{NP}$ then this is indeed the case (see also [ladner-ex](){.ref} and [PNPscenariosfig](){.ref}).




![A rough illustration of the (conjectured) status of problems in exponential time. Darker colors correspond to higher running time, and the circle in the middle is the problems in $\mathbf{P}$. $\mathbf{NP}$ is a (conjectured to be proper) superclass of $\mathbf{P}$ and the $\mathbf{NP}$-complete problems (or $\mathbf{NPC}$ for short) are the "hardest" problems in $\mathbf{NP}$, in the sense that a solution for one of them implies a solution for all other problems in $\mathbf{NP}$. It is conjectured that all the $\mathbf{NP}$-complete problems require at least $\exp(n^\epsilon)$ time to solve for a constant $\epsilon>0$, and many require  $\exp(\Omega(n))$ time. The _permanent_ is not believed to be contained in $\mathbf{NP}$ though it is $\mathbf{NP}$-hard, which means that a polynomial-time algorithm for it implies that $\mathbf{P}=\mathbf{NP}$.](../figure/PNPmap.png){#complexitymapfig .margin  }


^[TODO: maybe add examples of NP hard problems as a barrier to understanding - problems from economics, physics, etc.. that prevent having a closed-form solutions]

^[TODO: maybe include knots]




###  The Cook-Levin Theorem: Proof outline


We will now prove the Cook-Levin Theorem, which is the underpinning to a great web of reductions from 3SAT to thousands of problems across great many fields.
Some problems that have been shown to be $\mathbf{NP}$-complete include: minimum-energy protein folding, minimum surface-area foam configuration, map coloring,    optimal Nash equilibrium, quantum state entanglement, minimum supersequence of a genome, minimum codeword problem, shortest vector in a lattice, minimum genus knots, positive Diophantine equations, integer programming, and many many more.
The worst-case complexity of all these problems is (up to polynomial factors) equivalent to that of 3SAT, and through the Cook-Levin Theorem, to all problems in $\mathbf{NP}$.


To prove [cook-levin-thm](){.ref} we need to show that $F \leq_p 3SAT$ for every $F\in \mathbf{NP}$.
We will do so in three stages.
We define two intermediate problems: $NANDSAT$ and $3NAND$.
We will shortly show the definitions of these two problems, but
[cook-levin-thm](){.ref} will follow from combining the following three results:

1. $NANDSAT$ is $\mathbf{NP}$ hard ([nand-thm](){.ref}).

2. $NANDSAT \leq_p 3NAND$  ([threenand-thm](){.ref}).

3. $3NAND \leq_p 3SAT$   ([threenand-sat-thm](){.ref}).

By the transitivity of reductions, it will follow that for every $F \in \mathbf{NP}$,

$$
F \leq_p NANDSAT \leq_p 3NAND \leq_p 3SAT
$$

hence establishing  [cook-levin-thm](){.ref}.


We will prove these three results [nand-thm](){.ref}, [threenand-thm](){.ref} and  [threenand-sat-thm](){.ref} one by one, providing the requisite definitions as we go along.

## The $NANDSAT$ Problem, and why it is $\mathbf{NP}$ hard.

We define the $NANDSAT$ problem as follows. On input a string $Q\in \{0,1\}^*$, we define $NANDSAT(Q)=1$ if and only if $Q$ is a valid representation of an $n$-input and single-output NAND program and there exists some $w\in \{0,1\}^n$ such that $Q(w)=1$.
While we don't need this to prove [nand-thm](){.ref}, note that $NANDSAT$ is in $\mathbf{NP}$ since we can verify that $Q(w)=1$ using the polyonmial-time algorithm for evaluating NAND-CIRC programs.^[$Q$ is a NAND-CIRC program and not a NAND-TM program, and hence it is only defined on inputs of some particular size $n$. Evaluating $Q$ on any input $w\in \{0,1\}^n$ can be done in time polynomial in the number of lines of $Q$.]
We now prove that $NANDSAT$ is $\mathbf{NP}$ hard.

> ### {.lemma #nand-thm}
$NANDSAT$ is $\mathbf{NP}$ hard.


> ### {.proofidea data-ref="nand-thm"}
To prove [nand-thm](){.ref}  we need to show that for every $F\in \mathbf{NP}$, $F \leq_p NANDSAT$.
The high-level idea is that by the definition of $\mathbf{NP}$, there is some NAND-TM program $P^*$ and some polynomial $T(\cdot)$ such that $F(x)=1$ if and only if there exists some $w \in \{0,1\}^{a|x|^b}$ such that $P^*(xw)$ outputs $1$ within $T(|x|)$ steps.
Now by "unrolling the loop" of the NAND-TM program $P^*$ we can convert it into an $O(T(n))$  NAND-CIRC program $Q'$ with $n + an^b$ inputs and a single output such that for every $x\in \{0,1\}^n$ and $w\in \{0,1\}^{an^b}$, $Q'(xw)=P^*(xw)$. on input $x \in \{0,1\}$  that on input $w$ will simulate $P^*(xw)$ for $T(|x|)$ steps.
The next step is to _hardwire_ the input $x$ to $Q'$ to obtain an $O(T(n))$ line NAND-CIRC program $Q$ with $m=an^b$ inputs such that for every $w\in \{0,1\}^m$, $Q'(w)=Q(xw)$.
By construction it will be the case that for every $x\in \{0,1\}^n$, $F(x)=1$ if and only if there exists $w\in \{0,1\}^{an^b}$ such that $Q(w)=1$, and hence this shows that $F \leq_p NANDSAT$.


> ### { .pause }
The proof is a little bit technical but ultimately follows quite directly from the definition of $\mathbf{NP}$, as well as of NAND and NAND-TM programs. If you find it confusing, try to pause here and work out the proof yourself from these definitions, using the idea of "unrolling the loop" of a NAND-TM program.
It might also be useful for you to think how you would implement in your favorite programming language the function `unroll` which on input a NAND-TM program $P$ and numbers $T,n$ would output an $n$-input NAND-CIRC program $Q$ of $O(|T|)$ lines such that for every input $z\in \{0,1\}^n$, if $P$ halts on $z$ within at most $T$ steps and outputs $y$, then $Q(z)=y$.


::: {.proof data-ref="nand-thm"}
We now present the details.
Let $F \in \mathbf{NP}$.
To prove [nand-thm](){.ref} we need to give a polynomial-time computable function that will map every $x^* \in \{0,1\}^*$ to a NAND-CIRC program $Q$ such that $F(x)=NANDSAT(Q)$.

Let  $x^* \in \{0,1\}^*$ be such a string and let $n=|x^*|$ be its length.
By [NP-def](){.ref} there exists $V \in \mathbf{P}$ and $a,b \in \N$ such that $F(x^*)=1$  if and only if there exists $w\in \{0,1\}^{an^b}$ such that $V(x^*w)=1$.

Let $m=an^b$. Since $V\in \mathbf{P}$ there is some NAND-TM program $P^*$ that computes $V$ on inputs of the form $xw$ with $x\in \{0,1\}^n$ and $w\in \{0,1\}^m$ in at most ${(n+m)}^c$ time for some constant $c$.
Using our "unrolling the loop NAND-TM to NAND compiler" of [nand-compiler](){.ref}, we can obtain a NAND-CIRC program $Q'$ that has $n+m$ inputs and at most $O((n+m)^c)$ lines such that $Q'(xw)= P^*(xw)$ for every $x\in \{0,1\}^n$ and $w \in \{0,1\}^m$.

Now we can use the following simple but useful "hardwiring" technique to obtain a program:

> ### {.lemma title="Hardwiring Lemma" #hardwiringlem}
Given a $T$-line NAND-CIRC program $Q'$ of $n+m$ inputs and $x^* \in \{0,1\}^n$, we can obtain in polynomial a program $Q$ with $m$ inputs of $T+3$ lines such that for ever $w\in \{0,1\}^m$, $Q(w)= Q'(x^*w)$.

::: {.proof data-ref="hardwiringlem"}
To compute $Q$, we simply do a "search and replace" for all references in $Q'$ to `X[`$i$`]` for $i \in [n]$, and transform them to either the variable `zero` or `one` depending on whether $x^*_i$ is equal to $0$ or $1$ respectively.
By adding three lines to the beginning of $Q'$, we can ensure that the `zero` and `one` variables will have the correct value.
The only thing that then remains to do another search and replace to transform all references to the variables `X[`$n$`]`,$\ldots$, `X[`$n+m-1$`]` to the variables `X[`$0$`]`, $\ldots$, `X[`$m-1$`]` so that the $m$ inputs to the new program $Q$ will correspond to last $m$ inputs of the original program $Q'$.
See [hardwiringfig](){.ref} for an implementation of this reduction in Python.
:::

Using [hardwiringlem](){.ref}, we obtain a program $Q$ of $m$ inputs such that $Q(w)=Q'(x^*w)=P^*(x^*w)$ for every $w\in \{0,1\}^m$.
Since we know that $F(x^*)=1$ if and only if there exists $w\in \{0,1\}^m$ such that $P^*(x^*w)=1$, this means that $F(x^*)=1$ if and only if $NANDSAT(Q)=1$, which is what we wanted to prove.
:::


![Given an $T$-line NAND-CIRC program $Q$ that has $n+m$ inputs and some $x^*\in \{0,1\}^n$, we can transform $Q$ into a $T+3$ line NAND-CIRC program $Q'$ that computes the map $w \mapsto Q(x^*w)$ for $w\in \{0,1\}^m$ by simply adding code to compute the `zero` and `one` constants,  replacing all references to `X[`$i$`]` with either `zero` or `one` depending on the value of $x^*_i$, and then replacing the remaining references to `X[`$j$`]` with `X[`$j-n$`]`. Above is Python code that implements this transformation, as well as an example of its execution on a simple program.](../figure/hardwiring.png){#hardwiringfig }




## The $3NAND$ problem

The $3NAND$ problem is defined as follows: the input is a logical formula $\varphi$ on a set of variables $z_0,\ldots,z_{r-1}$
which is an AND of constraints of the form $z_i = NAND(z_j,z_k)$.
For example, the following is a $3NAND$ formula with $5$ variables and $3$ constraints:

$$
\left( z_3 = NAND(z_0,z_2) \right) \wedge \left( z_1 = NAND(z_0,z_2) \right) \wedge \left( z_4 = NAND(z_3,z_1) \right)
$$

The output of $3NAND$ on input $\varphi$ is $1$ if and only if there is an assignment to the variables of $\varphi$ that makes it evaluate to "true"  (that is, there is some assignment $z \in \{0,1\}^r$ satisfying all of the constraints of $\varphi$).
As usual, we can represent $\varphi$ as a string, and so think of $3NAND$ as a function mapping $\{0,1\}^*$ to $\{0,1\}$.
We now prove that $3NAND$ is $\mathbf{NP}$ hard:


> ### {.lemma  #threenand-thm}
$NANDSAT \leq_p 3NAND$.



> ### {.proofidea data-ref="threenand-thm"}
To prove [threenand-thm](){.ref} we need to give a polynomial-time map from every NAND-CIRC program $Q$ to a 3NAND formula $\Psi$ such that there exists $w$ such that $Q(w)=1$ if and only if there exists $z$ satisfying $\Psi$.
For every line $i$ of $Q$, we define a corresponding variable $z_i$ of $\Psi$.
If the line $i$ has the form `foo = NAND(bar,blah)` then we will add the clause $z_i = NAND(z_j,z_k)$ where $j$ and $k$ are the last lines in which `bar` and `blah` were written to. We will also set variables corresponding to the input variables, as well as add a clause to ensure that the final output is $1$.
The resulting reduction can be implemented in about a dozen lines of Python, see [andsattothreenandfig](){.ref}.



![Python code to reduce an instance $Q$ of $NANDSAT$ to an instance $\Psi$ of $3NAND$. In the example above we transform the NAND-CIRC program `xor5` which has $5$ input variables and $16$ lines, into a $3NAND$ formula $\Psi$ that has $24$ variables and $20$ clauses. Since `xor5` outputs $1$ on the input $1,0,0,1,1$, there exists an assignment $z \in \{0,1\}^{24}$ to $\Psi$ such that $(z_0,z_1,z_2,z_3,z_4)=(1,0,0,1,1)$ and $\Psi$ evaluates to _true_ on $z$. ](../figure/nandsatto3nandreduction.png){#nandsattothreenandfig  }


::: {.proof data-ref="threenand-thm"}
To prove [threenand-thm](){.ref} we need to give a reduction from $NANDSAT$ to $3NAND$.
Let  $Q$ be a NAND-CIRC program with $n$ inputs, one output, and  $m$ lines.
We can assume without loss of generality that $Q$ contains the variables `one` and `zero` as usual.


We map $Q$ to a $3NAND$ formula $\Psi$ as follows:

* $\Psi$ has $m+n$ variables $z_0,\ldots,z_{m+n-1}$.

* The first $n$ variables $z_0,\ldots,z_{n-1}$ will corresponds to the inputs of $Q$. The next $m$ variables $z_n,\ldots,z_{n+m-1}$ will correspond to the $m$ lines of $Q$.

* For every $\ell\in \{n,n+1,\ldots,n+m \}$, if the $\ell-n$-th line of the program $Q$ is `foo = NAND(bar,blah)` then we add to $\Psi$  the constraint $z_\ell = NAND(z_j,z_k)$ where $j-n$ and $k-n$ correspond to the last lines in which the variables `bar` and `blah` (respectively) were written to. If one or both of `bar` and `blah` was not written to before then we use $z_{\ell_0}$ instead of the corresponding value $z_j$ or $z_k$  in the constraint, where $\ell_0-n$ is the line in which `zero` is assigned a value.
If one or both of `bar` and `blah` is an input variable `X[i]` then we use $z_i$ in the constraint.


* Let $\ell^*$ be the last line in which the output `y_0` is assigned a value. Then we add the constraint $z_{\ell^*} = NAND(z_{\ell_0},z_{\ell_0})$ where $\ell_0-n$ is as above the last line in which `zero` is assigned a value. Note that this is effectively the constraint $z_{\ell^*}=NAND(0,0)=1$.


To complete the proof we need to show that there exists $w\in \{0,1\}^n$ s.t. $Q(w)=1$ if and only if there exists $z\in \{0,1\}^{n+m}$ that satisfies all constraints in $\Psi$.
We now show both sides of this equivalence.


__Part I: Completeness.__ Suppose that there is $w\in \{0,1\}^n$ s.t. $Q(w)=1$. Let $z\in \{0,1\}^{n+m}$ be defined as follows: for $i\in [n]$, $z_i=w_i$ and for $i\in \{n,n+1,\ldots,n+m\}$ $z_i$ equals the value that is assigned in the $(i-n)$-th line of $Q$ when executed on $w$. Then by construction $z$ satisfies all of the constraints of $\Psi$ (including the constraint that $z_{\ell^*}=NAND(0,0)=1$ since $Q(w)=1$.)

__Part II: Soundness.__ Suppose that there exists $z\in \{0,1\}^{n+m}$ satisfying $\Psi$. Soundness will follow by showing that  $Q(z_0,\ldots,z_{n-1})=1$ (and hence in particular there exists $w\in \{0,1\}^n$, namely $w=z_0\cdots z_{n-1}$, such that $Q(w)=1$). To do this we will prove the following claim $(*)$: for every $\ell \in [m]$, $z_{\ell+n}$ equals the value assigned in the $\ell$-th step of the execution of the program $Q$ on $z_0,\ldots,z_{n-1}$. Note that because $z$ satisfies the constraints of $\Psi$, $(*)$ is sufficient to prove the soundness condition since these constraints imply that the last value assigned to the variable `y_0` in the execution of $Q$ on $z_0\cdots w_{n-1}$  is equal to $1$. To prove $(*)$ suppose, towards a contradiction, that it is false, and let $\ell$ be the smallest number such that $z_{\ell+n}$ is _not_ equal to the value assigned in the $\ell$-th step of the exeuction of $Q$ on $z_0,\ldots,z_{n-1}$. But since $z$ satisfies the constraints of $\Psi$, we get that $z_{\ell+n}=NAND(z_i,z_j)$ where (by the assumption above that $\ell$ is _smallest_ with this property) these values _do_ correspond to the values last assigned to the variables on the righthand side of the assignment operator in the $\ell$-th line of the program. But this means that the value assigned in the $\ell$-th step is indeed simply the NAND of $z_i$ and $z_j$, contradicting our assumption on the choice of $\ell$.
:::




![A $3NAND$ instance that is obtained by taking a NAND-TM program for computing the $AND$ function, unrolling it to obtain a $NANDSAT$ instance, and then composing it with the reduction of [threenand-thm](){.ref}.](../figure/threenandresultreduction.png){#resultreduction .margin  }


## From $3NAND$ to $3SAT$



To conclude the proof of [cook-levin-thm](){.ref}, we need to show [threenand-sat-thm](){.ref} and show that $3NAND \leq_p 3SAT$:

> ### {.lemma  #threenand-sat-thm}
$3NAND \leq_p 3SAT$.


> ### {.proofidea data-ref="threenand-sat-thm"}
To prove [threenand-sat-thm](){.ref} we need to map a 3NAND formula $\varphi$ into a 3SAT formula $\psi$ such that $\varphi$ is satisfiable if and only if $\psi$ is. The idea is that we can transform every NAND constraint of the form $a=NAND(b,c)$ into the AND of ORs involving the variables $a,b,c$ and their negations, where each of the ORs contains at most three terms. The construction is fairly straightforward, and the details are given below.

> ### { .pause }
It is a good exercise for you to try to find a 3CNF formula $\xi$ on three variables $a,b,c$ such that $\xi(a,b,c)$ is true if and only if $a = NAND(b,c)$. Once you do so, try to see why this implies a reduction from $3NAND$ to $3SAT$,  and hence completes the proof of [threenand-sat-thm](){.ref}

![Code and example output for the reduction given in [threenand-sat-thm](){.ref} of $3NAND$ to $3SAT$.](../figure/3nandto3sat.png){#threenandtothreesat   }


::: {.proof data-ref="threenand-sat-thm"}
The constraint
$$
z_i = NAND(z_j,z_k) \label{eq:NANDconstraint}
$$
is satisfied if $z_i=1$ whenever $(z_j,z_k) \neq (1,1)$.
By going through all cases, we can verify that  [eq:NANDconstraint](){.eqref} is equivalent to the constraint

$$
 (\overline{z_i} \vee \overline{z_j} \vee\overline{z_k} ) \wedge          (z_i     \vee z_j )
         \wedge  (z_i     \vee z_k) \;\;. \label{eq:CNFNAND}
$$

Indeed if $z_j=z_k=1$ then the first constraint of [eq:CNFNAND](){.ref} is only true if $z_i=0$.
On the other hand, if either of $z_j$ or $z_k$ equals $0$ then unless $z_i=1$  either the second or third constraints will fail. This means that, given any 3NAND formula $\varphi$ over $n$ variables $z_0,\ldots,z_{n-1}$, we can obtain a 3SAT formula $\psi$ over the same variables by replacing every $3NAND$ constraint of $\varphi$ with three $3OR$ constraints as in [eq:CNFNAND](){.ref}.^[The resulting forumula will have some of the OR's involving only two variables.  If we wanted to insist on each formula involving three distinct variables we can always add a "dummy variable" $z_{n+m}$ and include it in all the OR's involving only two variables, and add a constraint requiring this dummy variable to be zero.]
Because of the equivalence of [eq:NANDconstraint](){.eqref} and [eq:CNFNAND](){.eqref}, the formula $\psi$ satisfies that $\psi(z_0,\ldots,z_{n-1})=\varphi(z_0,\ldots,z_{n-1})$ for every assignment $z_0,\ldots,z_{n-1} \in \{0,1\}^n$ to the variables.
In particular $\psi$ is satisfiable if and only if $\varphi$ is, thus completing the proof.
:::


## Wrapping up

We have shown that for every function $F$ in $\mathbf{NP}$, $F \leq_p NANDSAT \leq_p 3NAND \leq_p 3SAT$, and so $3SAT$ is $\mathbf{NP}$-hard.
Since in [reductionchap](){.ref} we saw that $3SAT \leq_p QUADEQ$, $3SAT \leq_p ISET$, $3SAT \leq_p MAXCUT$ and $3SAT \leq_p LONGPATH$, all these problems are $\mathbf{NP}$-hard as well.
Finally, since all the aforementioned problems are in $\mathbf{NP}$, they are all in fact $\mathbf{NP}$-complete and have equivalent complexity.
There are thousands of other natural problems that are $\mathbf{NP}$-complete as well.
Finding a polynomial-time algorithm for any one of them will imply a polynomial-time algorithm for all of them.



![An instance of the _independent set_ problem obtained by applying the reductions $NANDSAT \leq_p 3NAND \leq_p 3SAT \leq_p ISAT$ starting with the `xor5` NAND-CIRC program.](../figure/indsetfromnandsat.png){#indsetfromnandsatfig   }



> ### { .recap }
* Many of the problems for which we don't know polynomial-time algorithms are $\mathbf{NP}$-complete, which means that finding a polynomial-time algorithm for one of them would imply a polynomial-time algorithm for _all_ of them.
* It is conjectured that $\mathbf{NP}\neq \mathbf{P}$ which means that we believe that polynomial-time algorithms for these problems are not merely _unknown_ but are _nonexistent_.
* While an $\mathbf{NP}$-hardness result means for example that a full-fledged "textbook" solution to a problem such as MAX-CUT that is as clean and general as the algorithm for MIN-CUT probably does not exist, it does not mean that we need to give up whenever we see a MAX-CUT instance. Later in this course we will discuss several strategies to deal with $\mathbf{NP}$-hardness, including _average-case complexity_ and _approximation algorithms_.




## Exercises


> ### {.exercise title="Poor man's Ladner's Theorem" #ladner-ex}
Prove that if there is no $n^{O(\log^2 n)}$ time algorithm for $3SAT$ then there is some $F\in \mathbf{NP}$ such that $F \not\in \mathbf{P}$ and $F$ is not $\mathbf{NP}$ complete.^[__Hint:__ Use the function $F$ that on input a formula $\varphi$ and a string of the form $1^t$, outputs $1$ if and only if $\varphi$ is satisfiable and $t=|\varphi|^{\log|\varphi|}$.]


::: {.exercise  #WSATex}
Define $WSAT$ to be the following function: the input is  a CNF   formula $\varphi$ where each clause is the OR of one to three variables (_without negations_), and a number $k\in \mathbb{N}$.
For example, the following formula can be used for  a valid input to $WSAT$:
$\varphi = (x_5 \vee x_{2} \vee x_1) \wedge (x_1 \vee x_3 \vee x_0) \wedge (x_2 \vee x_4 \vee x_0)$.
The output $WSAT(\varphi,k)=1$ if and only if there exists a satisfying assignment to $\varphi$
in which exactly $k$ of the variables get the value $1$.
For example for the formula above $WSAT(\varphi,2)=1$ since the assignment $(1,1,0,0,0,0)$ satisfies all the clauses. However $WSAT(\varphi,1)=0$ since there is no single variable appearing in all clauses.

Prove that $WSAT$ is $\mathbf{NP}$-complete.
:::

::: {.exercise  #employeerecrutingex}
In the _employee recruiting problem_ we are given a list of potential employees, each of which has some subset of $m$ potential skills, and a number $k$.
We need to assemble a team of $k$ employees such that for every skill there would be one member of the team with this skill.

For example, if Alice has the skills "C programming", "NAND programming" and "Solving Differential Equations", Bob has the skills "C programming" and "Solving Differential Equations", and Charlie has the skills "NAND programming" and "Coffee Brewing", then if we want a team of two people that covers all the four skills, we would hire Alice and Charlie.

Define the function $EMP$ s.t. on input the skills $L$ of all potential employees (in the form of a sequence $L$ of $n$ lists $L_1,\ldots,L_n$, each containing distinct  numbers between $0$ and $m$), and a number $k$, $EMP(L,k)=1$ if and only if there is a subset $S$ of $k$ potential employees such that for every skill $j$ in $[m]$, there is an employee in $S$ that has the skill $j$.

Prove that $EMP$ is $\mathbf{NP}$ complete.
:::

::: {.exercise title="Balanced max cut" #balancedmc}
Prove that the "balanced variant" of the maximum cut problem is $\mathbf{NP}$-complete, where this is defined as $BMC:\{0,1\}^* \rightarrow \{0,1\}$ where for every graph $G=(V,E)$ and $k\in \mathbb{N}$, $BMC(G,k)=1$ if and only if there exists a cut $S$ in $G$ cutting at least $k$ edges such that $|S|=|V|/2$.
:::

::: {.exercise title="Regular expression intersection" #manyregs}
Let $MANYREGS$ be the following function: On input a list  of regular expressions $exp_0,\ldots,\exp_m$ (represented as strings in some standard way), output $1$ if and only if there is a single string $x \in \{0,1\}^*$ that matches all of them. Prove that $MANYREGS$ is $\mathbf{NP}$-hard.
:::



## Bibliographical notes

^[TODO: credit surveys of Avi, Madhu]


Eugene Lawler's quote on the "mystical power of twoness"  was taken from the wonderful book "The Nature of Computation" by Moore and Mertens. See also [this memorial essay on Lawler](https://pure.tue.nl/ws/files/1506049/511307.pdf) by Lenstra.


## Further explorations

Some topics related to this chapter that might be accessible to advanced students include: (to be completed)


## Acknowledgements
