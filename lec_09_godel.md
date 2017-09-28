# Is every theorem provable?

>_"Take any definite unsolved problem, such as ... the existence of an infinite number of prime numbers of the form $2^n + 1$. However unapproachable these problems may seem to us and however helpless we stand before them, we have, nevertheless, the firm conviction that their solution must follow by a finite number of purely logical processes..."_ \
>_"...This conviction of the solvability of every mathematical problem is a powerful incentive to the worker. We hear within us the perpetual call: There is the problem. Seek its solution. You can find it by pure reason, for in mathematics there is no ignorabimus."_, David Hilbert, 1900.





## Unsolvability of Diophantine equations

The problems of the previous lecture, while natural and important, still  intimately involved NAND++ programs or other computing mechanisms in their definitions.
One could perhaps hope that as long as we steer clear of functions whose inputs are themselves programs, we can avoid the "curse of uncomputability".
Alas, we have no such luck.



Many of the functions people wanted to compute over the years involved solving equations.
These have a much longer history than mechanical computers.
The Babilonians already knew how to solve some quadratic equations in 2000BC, and the formula for all quadratics appears in the [Bakshali Manuscript](https://en.wikipedia.org/wiki/Bakhshali_manuscript) that was composed in India around the 3rd century.
During the Renaissance, Italian mathematicians discovered generalization of these formulas for cubic and quartic (degrees $3$ and $4$) equations.
Many of the greatest minds of the 17th and 18th century, including Euler, Lagrange, Leibnitz and Gauss worked on the problem of finding such a formula  for _quintic_ equations to no avail, until in the 19th century Ruffini, Abel and Galois  showed that no such formula exists, along the way giving birth to _group theory_.


However, the fact that there is no closed-form formula does not mean we can not solve such equations.
People have been solving higher degree equations numerically for ages.
The Chinese manuscript [Jiuzhang Suanshu](https://en.wikipedia.org/wiki/The_Nine_Chapters_on_the_Mathematical_Art) from the first century mentions such approaches.
Solving polynomial equations is by no means restricted only to ancient history or to students' homeworks.
The [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) method is the workhorse powering many of the machine learning tools that have revolutionized Computer Science over the last several years.

But there are some equations that we simply do not know how to solve _by any means_.
For example, it took more than 200 years until people succeeded in proving that the equation  $a^{11} + b^{11} = c^{11}$ has no solution in integers.^[This is a special case of what's known as  "Fermat's Last Theorem" which states that $a^n + b^n = c^n$ has no solution in integers for $n>2$. This was conjectured in 1637 by Pierre de Fermat but only proven by Andrew Wiles in 1991. The case $n=11$ (along with all other so called "regular prime exponents") was established by Kummer in 1850.]
The notorious difficulty of so called _Diophantine equations_ (i.e., finding _integer_ roots of a polynomial) motivated the mathematician David Hilbert in 1900 to include the question of finding a general procedure for solving such equations  in his famous list of twenty-three open problems for mathematics of the 20th century.
I  don't think Hilbert  doubted that such a procedure exists.
After all, the whole history of mathematics up to this point involved the discovery of ever more powerful methods, and even impossibility results such as the inability to trisect an angle with a straightedge and compass, or the non-existence of an algebraic formula for qunitic equations, merely pointed out to the need to use more general methods.

Alas, this turned out not to be the case for Diophantine equations: in 1970, Yuri Matiyasevich, building on a decades long line of work by  Martin Davis,  Hilary Putnam and Julia Robinson, showed that there is simply _no method_ to solve such equations in general:

> # {.theorem title="MRDP Theorem" #MRDP-thm}
Let  $SOLVE:\{0,1\}^* \rightarrow \{0,1\}^*$ be the function that takes as input a multivariate polynomial with integer coefficients $P:\R^k \rightarrow \R$ for $k \leq 100$ and outputs either $(x_1,\ldots,x_k) \in \N^k$ s.t.  $P(x_1,\ldots,x_k)=0$  or the string ```no solution``` if no $P$ does not have non-negative integer roots.^[As usual, we assume some standard way to express numbers and text as binary strings.]
Then $SOLVE$ is uncomputable.
Moreover, this holds even for the easier function $HASSOL:\{0,1\}^* \rightarrow \{0,1\}$ that given such a polynomial $P$ outputs $1$ if there are $x_1,\ldots,x_k \in \N$ s.t. $P(x_1,\ldots,x_k)=0$ and $0$ otherwise.


The difficulty in finding a way to distinguish between "code" such as NAND++ programs, and "static content" such as polynomials is just another manifestation of the phenomenon that _code_ is the same as _data_.
While a fool-proof solution for distinguishing between the two is inherently impossible, finding heuristics that do a reasonable job keeps many firewall and anti-virus manufacturers very busy
(and finding ways to bypass these tools keeps many hackers busy as well).

### "Baby" MRDP Theorem: hardness of quantified Diophantine equations

Computing the function $HASSOL$ is equivalent to determining the truth of a logical statement of the following form:^[Recall  that $\exists$ denotes the _existential quantifier_; that is, a statement of the form $\exists_x \varphi(x)$ is true if there is _some_ assignment for $x$ that makes the Boolean function $\varphi(x)$ true.
The dual quantifier is the _universal quantifier_, denoted by $\forall$, where a statement $\forall_x \varphi(x)$ is true if  _every_ assignement for $x$ makes the Boolean function $\varphi(x)$ true.
Logical statements where all variables are _bound_ to some quantifier (and hence have no parameters) can be either true or false, but determining which is the case is sometimes highly nontrivial.
If you could use a review of quantifiers, section 3.6 of the text by [Lehman, Leighton and Meyer](http://www.boazbarak.org/cs121/MIT6_042Notes.pdf) is an excellent source for this material.]

$$
\exists_{x_1,\ldots,x_k \in \N} \text{ s.t.} P(x_1,\ldots,x_k)=0 \;. \label{eq:diophantine}
$$


[MRDP-thm](){.ref} states that there is no NAND++ program that can determine the truth of every statements of the form [eq:diophantine](){.eqref}.
The proof is highly involved and we will not see it here.
Rather  we will prove the following weaker result that there is no NAND++ program that can the truth of more general statements that mix together the existential ($\exists$) and universal ($\forall$) quantifiers.
The reason this  result is weaker than [MRDP-thm](){.ref} is  because deciding the truth of  more general  statements (that involve both quantifier) is a potentially harder problem than only existential statements, and so it is potentially easier to prove that this problem is uncomputable. (If you find the last sentence confusing, it is worthwhile to reread it until you are sure you follow its logic; we are so used to trying to find solution for problems that it can be quite confusing to follow the arguments showing that problems are _uncomputable_.)

> # {.definition title="Quantified integer statements" #QIS-def}
A _quantified integer statement_ is a well-formed statement with no unbound variables involving integers, variables, the operators $>,<\times,+,-,=$, the logical operations $\neg$ (NOT), $\wedge$ (AND), and $\vee$ (OR), as well as quantifiers of the form $\exists_{x\in\N}$ and $\forall_{y\in\N}$ where $x,y$ are variable names.

[QIS-def](){.ref} is interesting in its own right and not just as a "toy version" of [MRDP-thm](){.ref}.
We often care deeply about determining the truth of quantified integer statements.
For example, the statement that Fermat's Last Theorem is true for $n=3$ can be phrased as the quantified integer statement
$$
\neg \exists_{a\in\N} \exists_{b\in\N} \exists_{c\in\N} a\times a \times a  + b \times b \times b = c\times c \times c \;.
$$

The _twin prime hypothesis_, that states that there is an infinite number of numbers $p$ such that both $p$ and $p+2$ are primes  can be phrased as the quantified integer statement
$$
\forall_{n\in\N} \exists_{p\in\N} (p>n) \wedge PRIME(p) \wedge PRIME(p+2)
$$
where we replace an instance of $PRIME(q)$ with the statement $(q>1) \wedge \forall_{a\in \N} \forall_{b\in\N} (a=1) \vee (a=q) \vee \neg (a\times b =q)$.

The claim (mentioned in Hilbert's quote above) that are infinitely many _Fermat primes_ of the form $p=2^n+1$ can be phrased as follows:

$$
\begin{split}
\forall_{n\in\N}\exists_{p\in\N} (p>n) \wedge PRIME(p) \wedge \\
\left(\forall_{k\in\N}  (k = 2) \vee \neg PRIME(k) \vee \neg DIVIDES(k,p-1)\right)
\end{split}
$$

where $DIVIDES(a,b)$ is the statement $\exists_{c\in\N} b\times c = a$.
In English, this corresponds to the claim that for every $n$ there is some $p>n$ such that all of $p-1$'s prime factors are equal to $2$.


Much of number theory is concerned with determining the truth of quantified integer statements.
Since our experience has been that, given enough time (which could sometimes be several centuries)  humanity has  managed to do so for the statements that she cared enough about, one could (as Hilbert did) hope that eventually we will discover a _general procedure_ to determine the truth of such statements.
The following theorem shows that this is not the case:

> # {.theorem title="Uncomputability of quantified integer statements" #QIS-thm}
Let $QIS:\{0,1\}^* \rightarrow \{0,1\}$ be the function that given a (string representation of) a quantified integer statement outputs $1$ if it is true and $0$ if it is false.^[Since a quantified integer statement is simply a sequence of symbols, we can easily represent it as a string. We will assume that _every_ string represents some  quantified integer statement, by mapping strings that do not correspond to such a statement to an arbitrary statement such as $\exists_{x\in \N} x=1$.] Then $QIS$ is uncomputable.

Note that [QIS-thm](){.ref} is an immediate corollary of [MRDP-thm](){.ref}.
Indeed,   if you can compute $QIS$ then you can compute $HASSOL$ and hence if you _can't_ compute $HASSOL$ then you can't compute $QIS$ either.
But [QIS-thm](){.ref} is easier (though not trivial) to prove, and we will provide the proof in the following section.

## Proving the unsolvability of quantified integer statements.

In this section we will prove [QIS-thm](){.ref}.
The proof will, as usual, go by reduction from the Halting problem, but we will do so in two steps:

1. We will first use a reduction from the Halting problem to show that a deciding  _quantified mixed statements_ is uncomputable. Unquantified mixed statements involve both strings and integers.

2. We will then reduce the problem of quantified mixed statements to quantifier integer statements.



### Quantified mixed statements and computation traces

As mentioned above, before proving [QIS-thm](){.ref}, we will give an easier result showing the uncomputability of deciding the truth of an even more general class of statements- one that involves not just integer-valued variables but also string-valued ones.

> # {.definition title="Quantified mixed statements" #QMS-def}
A _quantified mixed statement_ is a well-formed statement with no unbound variables involving integers, variables, the operators $>,<\times,+,-,=$, the logical operations $\neg$ (NOT), $\wedge$ (AND), and $\vee$ (OR), as well as quantifiers of the form $\exists_{x\in\N}$, $\exists_{a\in\bits^*}$,  $\forall_{y\in\N}$, $\forall_{b\in\{0,1\}^*}$ where $x,y,a,b$ are variable names. These also include the operator $|a|$ which returns the length of a string valued variable $a$, as well as the operator $a_i$ where $a$ is a string-valued variable and $i$ is an integer valued expression which is true if $i$ is smaller than the length of $a$ and the $i^{th}$ coordinate of $a$ is $1$, and is false otherwise.

For example, the true statement that for every string $a$ there is a string $b$ that correspond to $a$ in reverse order can be phrased as the following quantified mixed statement
$$
\forall_{a\in\{0,1\}^*} \exists_{b\in \{0,1\}^*}  (|a|=|b|)
\wedge (\forall_{i\in\N} (i>|a|) \vee (a_i \wedge b_{|a|-i}) \vee (\neg a_i \wedge \neg b_{|a|-i}) )) \;.
$$

Quantified mixed statements are a more general than quantified integer statements, and so the following theorem is potentially easier to prove than [QIS-thm](){.ref}:


> # {.theorem title="Uncomputability of quantified mixed statements" #QMS-thm}
Let $QMS:\{0,1\}^* \rightarrow \{0,1\}$ be the function that given a (string representation of) a quantified mixed  statement outputs $1$ if it is true and $0$ if it is false. Then $QMS$ is uncomputable.


### "Unraveling" NAND++ programs and  quantified mixed integer statements

We will first prove [QMS-thm](){.ref} and then use it to prove [QIS-thm](){.ref}.
The proof is again by reduction to $HALT$ (see [QMS:reduction:fig](){.ref}).
That is, we do so by giving a program that transforms any NAND++ program $P$ and input $x$ into a quantified mixed statement $\varphi_{P,x}$ such that $\varphi_{P,x}$  is true if and only if $P$ halts on input $x$.
This sill complete  the proof, since it will imply that if $QMS$ is computable then so is the $HALT$ problem, which we have already shown is uncomputable.

![We prove that $QMS$ is uncomputable by giving a reduction that maps every pair $(P,x)$ into a quantified mixed statements $\varphi_{P,x}$ that is true if and only if $P$ halts on $x$.](../figure/QMS_reduction.png){#QMS:reduction:fig .class width=300px height=300px}


The idea behind the construction of the statement $\varphi_{P,x}$ is the following.
The statement will be true if and only if there exists a string $L\in \{0,1\}^*$ which corresponds to an _execution trace_ that proves that $P$ halts on input $x$.
At a high level, the crucial insight  is that unlike when we actually run the computation, to verify the correctness of a execution trace  we only need to verify _local consistency_ between pairs of lines.


We have seen execution traces before, but now we  define them more precisely.
Informally, an _execution trace_ of a program $P$ on an input $x$ is a string that represents a "log" of all the lines executed and variables assigned in the course of the execution.
For example, if we execute the parity program

~~~~ { .go .numberLines }
tmp1  := seen_i NAND seen_i
tmp2  := x_i NAND notseen_i
val   :=  tmp2 NAND tmp2
ns   := s   NAND s
y_0  := ns  NAND ns
u    := val NAND s
v    := s   NAND u
w    := val NAND u
s    := v   NAND w
seen_i := zero NAND zero  
stop := validx_i NAND validx_i
loop := stop     NAND stop
~~~~


on the input `01`, the trace will be

```
... add trace here...
```

More formally, given a NAND++ program $P$ and an input $x\in \{0,1\}^n$, if $P$ takes $T$ steps to halt on $x$, then the _execution trace_ of $P$ on $x$ will be a string $L\in \{0,1\}^{T+n}$ such that $(L_0,\ldots,L_{n-1})=x$ and for every $i\in \{n,\ldots,n+T-1\}$, $L_i$ correspond to the value that is assigned to a variable in the $(i-n)^{th}$ step of $P$'s execution on $x$.
Note that such an execution trace $L\in \{0,1\}^{n+T}$ satisfies that for every $i\in \{n,\ldots,n+T-1\}$, $L_i$ is the NAND of $L_j$ and $L_k$ where $j$ and $k$ are the last lines in which the two variables referred to in the corresponding line are assigned a value.

We can compute $j$ and $k$ as an arithmetic function of $i$ as follows:

* If $P$ has $L$ lines then  line $\ell$ of $P$ that is executed in the $j^{th}$ step is $j (\mod L)$ and the value of the program counter $pc$ is $\floor{j/L}$.

* The value of the index variable `i` at this point is $INDEX(pc)$ where $INDEX$ is the explicit function that we computed in Lecture 6.

* The variables that a referred to in the $\ell$-th line are computed by a constant size function since there is only a constant number of lines in $P$.

### Completing the proof


The idea of the reduction is that given a NAND++ program $P$ and an input $x$, we can come up with a mixed quantifier statement $\Psi_{P,x}(L)$ such that for every $L\in \{0,1\}^*$,  $\Psi_{P,x}(L)$ is true if and only if $L$ is a consistent execution trace of $P$ on input $x$ that ends in a halting state (with the `loop` variable set to $0$).
The full details are rather tedious,  but the crucial points are the following:

* We can come up with a quantified integer statement $INDEX(t,i)$ that will be true if and only if the value of `i` when the program executes step $t$ equals $i$.

* We can come up with quantified integer statements $PREV_1(t,s)$  and $PREV_2(t,r)$ that will satisfy the following. If at step $t$ the operation invokved is `foo := bar NAND baz` then $PREV_1(t,s)$ is true if and only if $s$ is the last step before $t$ in which `bar` was written to  and $PREV_2(t,r)$ is true if and only if $r$ is the last step before $t$ in which `baz` was written to. Note that these statements will themselves use $INDEX$ because if `bar` and/or `baz` are indexed by `i` then part of the condition for $PREV_1(t,s)$ and $PREV_2(t,r)$ will be to ensure that $INDEX(t)=INDEX(s)$ and/or $INDEX(t)=INDEX(r)$.

* We can come up with a quantified integer statement $LOOP(t)$ that will be true if and only if the variable written to  at step $t$ in the execution is equal to `loop`


Given a construction of such a formula $\Psi_{P,x}(L)$ we can see that $HALT(P,x)=1$ if and only if the following quantified mixed statement $\varphi_{P,x}$ is true
$$
\varphi_{P,x} = \exists_{L\in \{0,1\}^*} \Psi_{P,x}(L) \label{eq:QMSHALT}
$$
and hence we can write $HALT(P,x)= QMS(\varphi_{P,x})$.
Since we can compute from $P,x$ the statement $\varphi_{P,x}$, we see that if $QMS$ is computable then so would have been $HALT$, yielding a proof by contradiction of [QMS-thm](){.ref}.





### Reducing mixed statements to integer statements

We now show how to prove [QIS-thm](){.ref} using [QMS-thm](){.ref}.
The idea is again a proof by reduction.
We will show a transformation of every quantifier mixed statement $\varphi$ into a quantified _integer_ statement $\xi$ that does not use string-valued variables such that $\varphi$ is true if and only if $\xi$ is true.

To remove string-valued variables from a  statement, we  encode them by integers.
We will show  that we can encode a string $x\in \{0,1\}^*$ by a pair  of numbers $(X,n)\in \N$ s.t.

* $n=|x|$
* There is a quantified integer statement $INDEX(X,i)$ that for every $i<n$, will be true  if $x_i=1$ and will be false otherwise.


This will mean that we can replace a quantifier such as $\forall_{x\in \{0,1\}^*}$ with $\forall_{X\in \N}\forall_{n\in\N}$  (and similarly replace existential quantifiers over strings). We can  later replace all calls to $|x|$ by $n$ and all calls to $x_i$ by $INDEX(X,i)$.
Hence an encoding of the form above yields a proof of [QIS-thm](){.ref}, since we can use it to map every mixed quantified statement $\varphi$ to quantified integer statement $\xi$ such that $QMS(\varphi)=QIS(\xi)$.
Hence if $QIS$ was computable then $QMS$ would be computable as well, leading to a contradiction.

To achieve our encoding we use the following technical result :

> # {.lemma title="Constructible prime sequence" #primeseq}
There is a sequence of prime numbers $p_0 < p_1 < p_3 < \cdots$ such that there is  a quantified integer statement $PINDEX(p,i)$ that is true if and only if $p=p_i$.

Using [primeseq](){.ref} we can encode a $x\in\bits^*$ by the numbers $(X,n)$ where  $X = \prod_{x_i=1} p_i$ and $n=|x|$.
We can then define the statement $INDEX(X,i)$ as
$$
\forall_{p\in\N} \neg PINDEX(p,i) \vee DIVIDES(p,X)
$$
where  $DIVIDES(a,b)$, as before, is defined as $\exists_{c\in\N} a\times c = b$.
Note that indeed if $X,n$ encodes the string $x\in \{0,1\}^*$, then for every $i<n$, $INDEX(X,i)=x_i$, since $p_i$ divides $X$ if and only if $x_i=1$.  

Thus all that is left to conclude the proof of [QIS-thm](){.ref} is to prove [primeseq](){.ref}, which we now proceed to do.

> # {.proof data-ref="primeseq"}
 The sequence of prime numbers we consider is the following:
we define $p_i$ to be the smallest prime number that is in the interval $[i+1,2i+1]$.
It is known by [Bertrand's postulate](https://en.wikipedia.org/wiki/Bertrand's_postulate) that there exists such a prime number for every $i\in\N$.
Given this, the  definition of $PINDEX(p,i)$ is simple:
$$
(p > i) \wedge (p < 2\times i+1)\wedge
\left(\forall_{p'} \neg PRIME(p') \vee (p' \leq i) \vee (p' \geq p) \right) \;,
$$
We leave it to the reader to verify that $PINDEX(p,i)$ is true iff $p=p_i$.



## Hilbert's Program and Gödel's Incompleteness Theorem

>_"And what are these …vanishing increments? They are neither finite
quantities, nor quantities infinitely small, nor yet nothing. May we not call them the ghosts of
departed quantities?"_, George Berkeley, Bishop of Cloyne, 1734.

The 1700's and  1800's were a time of great discoveries in mathematics but also of several crises.
The discovery of calculus by Newton and Leibnitz in the late 1600's ushered a golden age of problem solving.
Many longstanding challenges succumbed to the new tools that were discovered, and mathematicians got ever better at doing some truly impressive calculations.
However, the rigorous foundations behind these calculations left much to be desired.
Mathematicians manipulated infinitsemal quantities and infinite series cavalierly, and while most of the time they  ended up with the correct results, there were a few strange examples (such as trying to calculate the value of the infinite series $1-1+1-1+1+\ldots$) which seemed to give out different answers depending on the method of calculation.
This led to a growing sense of unease in the foundations of the subject which was  addressed in works of mathematicians such as Cauchy, Weierstrass, and Reimann, who eventually  placed analysis on firmer foundations, giving rise to the $\epsilon$'s and $\delta$'s that students taking honors calculus grapple with to this day.

In the beginning of the 20th century, there was an effort to replicate this effort,  in greater rigor, to all parts of mathematics.
The hope was to show that all the true results of mathematics can be obtained by starting with a number of axioms, and deriving theorems from them using logical rules of inference.
This effort was known as the _Hilbert program_, named after the very same David Hilbert we mentioned above.
Alas, [MRDP-thm](){.ref}  yields a devastating blow to this program, as it implies that for _any_ valid set of axioms and inference laws, there will be unsatisfiable Diophantine equations that cannot be proven unsatisfiable using these axioms and laws.
To formalize that, we make the following definition:

> # {.definition title="Proof systems for diophantine equations" #proofdef}
A proof system for Diophantine equations is defined by a finite subset $A \subseteq \{0,1\}^*$ of _axioms_ and a finite set of functions $I_1,\ldots, I_m$ (known as _inference rules_) where each $I_j:(\{0,1\}^*)^{k_j} \rightarrow \{0,1\}^*$ is a function mapping a tuple of $k_j$ strings to a string.
>
A _valid proof_ in the system $(A,I_1,\ldots,I_m)$ of the unsatisfiability of a diophantine equation $P(x_1,\ldots,x_t)=0$  consists of a sequence $p_1,\ldots,p_n$ of strings such that for every $i$, either $p_i \in A$ or there exists $j\in [m]$ and $i_1,\ldots,i_{k_j} < i$ such that $p_i = I_j(p_{i_1},\ldots,p_{i_j})$ and $p_n$ is a string representing the statement "$\forall_{x_1,\ldots,x_t \in \N} P(x) \neq 0$."
>
A proof system $(A,I_1,\ldots,I_m)$ is _sound_ if there is no valid proof of a false statement. That is, for every diophantine equation $P(x_1,\ldots,x_t)=0$, if there is a proof $(p_1,\ldots,p_n)$ that the equation is unsatisfiable then it is indeed unsatisfiable.

The formal definition is a bit of a mouthful, but what it states the natural notion of a logical proof for the unsatisfiability of an equation.
Namely, that such a proof will consist of $n$ lines, where each line is either an axiom or is derived from the previous lines by some rule of inference.
We do not make any restriction on what the axioms or rules should be, except that they should not allow us to prove false statements.
Hilbert believed that for all of mathematics, and in particular for settling diophantine equations, it should be possible to find some set of axioms and rules of inference that would allow to derive all true statements.
However, he was wrong:


> # {.theorem title="Gödel's Incompleteness Theorem" #godelthm}
For every valid proof system $(A,I_1,\ldots,I_m)$, there exists a diophantine equation $P(x_1,\ldots,x_t)=0$ such that there is no $x_1,\ldots,x_t \in \N$ that satisfy it, but yet there is no proof in the system $(A,I_1,\ldots,I_m)$ for the statement "$\forall_{x_1\in\N} \cdots \forall_{x_t\in \N} P(x_1,\ldots,x_t)\neq 0$".

> # {.proof data-ref="godelthm"}
Suppose otherwise, that there exists such a system.
Then we can define the following algorithm $S$ that computes the function $HASSOL:\{0,1\}^* \rightarrow \{0,1\}$ described in [MRDP-thm](){.ref}.
The algorithm will work as follows:
>
* On input a Diophantine equation $P(x_1,\ldots,x_t)=0$, for $k=1,2,\ldots$ do the following:
   >1. Check for all $x_1,\ldots,x_t \in \{0,\ldots, k\}$ whether $x_1,\ldots,x_t$  satisfies the equation. If so then halt and output $1$.
   >2. For all  $n \in \{1,\ldots,k\}$ and all strings $p_1,\ldots,p_n$ of length at most $k$, check whether $(p_1,\ldots,p_n)$ is a valid proof of "$\forall_{x_1\in\N} \cdots \forall_{x_t\in \N} P(x_1,\ldots,x_t)\neq 0$". If so then halt and output $0$.
>
Note that checking if a list $(p_1,\ldots,p_n)$ is a valid proof can be done in finite time since there is only a finite number of axioms and inference rules. Under the assumption that for _every_ diophantine equation that is unsatisfiable, there is a proof that certifies it, this algorithm will always halt and output $0$ or $1$, and moreover, the answer will be correct. Hence we reach a contradiction to [MRDP-thm](){.ref}

Note that if we considered proof systems for more general quantified integer statements, then  the existence of a true but yet unprovable statement would follow from [QIS-thm](){.ref}.
Indeed, that was the content of Gödel's original incompleteness theorem which was proven in 1931 way before the MRDP Theorem (and initiated the line of research which resulted in the latter theorem).
Another way to state the result is that every proof system that is rich enough to express quantified integer statements  is either inconsistent (can prove both a statement and its negation) or incomplete (cannot prove all true statements).


Examining the proof of [godelthm](){.ref} shows that it yields a more general statement (see [godelthemex](){.ref}): for every uncomputable function $F:\{0,1\}^* \rightarrow \{0,1\}$ and every sound axiomatic proof system $S$ (that is characterized by a finite number of axioms and inference rules), there is some input $x$ for which the proof system $S$ is not able to prove neither that $F(x)=0$ nor that $F(x) \neq 0$ (see [godelthemex](){.ref}).

Also, the  proof of  [godelthm](){.ref} can be extended to yield Gödel's second incompleteness theorem which, informally speaking, says for that every proof system $S$ rich enough to express quantified integer statements, the following holds:

* There is a quantified integer statement $\varphi$ that is true if and only if $S$ is consistent.

* There is no proof in $S$ for $\varphi$.


Thus once we pass a sufficient level of expressiveness, we cannot find a proof system that is strong enough to prove its own consistency.
This in particular showed that Hilbert's second problem (which was about finding an axiomatic provably-consistent basis for arithmetic) was also unsolvable.






## Lecture summary

* Uncomputable functions include also functions that seem to have nothing to do with NAND++ programs or other computational models such as determining the satisfiability of diophantine equations.

* This also implies that for any finite axiomatic system $S$,  there are interesting statements $X$ (namely of the form "$F(x)=0$" for an uncomputable function $F$) such that $S$ is not able to prove either $X$ or its negation.  

## Exercises


> # {.exercise title="title" #godelthemex}
For every representation of logical statements as strings, we can define as in [proofdef](){.ref} an axiomatic proof system to consist of a finite set of strings $A$ and a finite set of rules $I_0,\ldots,I_{m-1}$ with $I_j: (\{0,1\}^*)^{k_j} \rightarrow \{0,1\}^*$ such that a proof $(s_1,\ldots,s_n)$ that $s_n$ is true is valid if for every $i$, either $s_i \in A$ or is some $j\in [m]$ and  are $i_1,\ldots,i_{k_j} < i$ such that $s_i = I_j(s_{i_1},\ldots,i_{k_j})$.
A system is _sound_  if whenever there is no false $s$ such that there is  a proof that $s$ is true
Prove that for every uncomputable function $F:\{0,1\}^* \rightarrow \{0,1\}$ and every sound axiomatic proof system $S$ (that is characterized by a finite number of axioms and inference rules), there is some input $x$ for which the proof system $S$ is not able to prove neither that $F(x)=0$ nor that $F(x) \neq 0$.

^[TODO: Maybe add an exercise to give a MIS that corresponds to any regular expression.]


## Bibliographical notes

^[TODO:  Add letter of Christopher Strachey to the editor of The Computer Journal.
Explain right order of historical achievements.
Talk about intuitionistic, logicist, and formalist approaches for the foudnations of mathematics.
Perhaps analogy to veganism.
State the full Rice's Theorem and say that it follows from the same proof as in the exercise.]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements

Thanks to Alex Lombardi for pointing out  an embarrassing mistake in the description of Fermat's Last Theorem. (I  said that it was open for exponent 11 before Wiles' work.)
