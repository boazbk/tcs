# Mathematical Background


__Note:__ In this section we briefly review some of the mathematical content we will use in this course. We will assume that students either encountered these notions before, in a discrete math or other course, or can pick them up via self study. There are several excellent freely-available resources for this material online. In particular, the [CS 121 webpage](http://www.boazbarak.org/cs121/background/) contains a program for self study of all the needed notions using the lecture notes, videos, and assignments of MIT course [6.042j Mathematics for Computer science](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-fall-2010/).





>_"Young man, in mathematics you don't understand things. You just get used to them."_, John von Neumann


In this course we will be interested in understanding the truth of assertions such as _"there is no efficient algorithm to find the prime factors of a given number"_.^[Actually, scientists currently do not know if this assertion is true or false, but we will see that settling it in either direction has very interesting applications touching on areas as far apart as Internet security and quantum mechanics.]

You cannot run experiments to prove the _non existence_ of an algorithm.
Thus, our only way to show that an assertion such as the above is true is to use _mathematical proofs_.
In fact, even before asking if this assertion is true, we will need to use _mathematical definitions_ to make this a precise statement that is either true or false.
So you see that our main tools in this course will be mathematical proofs and definitions.^[The [CS 121 website](http://www.boazbarak.org/cs121/background/) contains links to various resources which can help students catch up on this material.]

Many people think of mathematical proofs as a sequence of logical deductions that starts from some axioms and ultimately arrives at a conclusion.
In fact, some dictionaries [define](http://www.thefreedictionary.com/mathematical+proof) proofs that way.
But in reality a mathematical proof of a statement X is simply an argument that convinces the reader that X is true beyond a shadow of a doubt.
To produce such a proof you need to:

1. Understand precisely what X means.
2. Convince  _yourself_ that X is true.
3. Write your reasoning down in plain, precise and concise English (using formulas or notation only when they help clarity).

In many cases, Step 1 is the most important one. Understanding what a statement means is often more than halfway towards understanding why it is true.

## Example: There are infinitely many primes

A classical example for a proof is Euclid's proof that there are infinitely many prime numbers.
The first step is to understand what this statement means.
One way to state this statement is that there is no largest prime number: for every number $N$, there is always a prime number $p$ that is larger than $N$.
Now that we understand the statement, we can try to prove it.

We can start by thinking why think this statement should be true or, equivalently, why it couldn't be false.
If this statement was false, then there would be some number $N$ such that every number $M>N$ is _composite_: $M$ always has some divisors different than $1$ and itself.
If any of the  divisors  is itself larger than $N$ then it must be composite as well, and hence we can decompose it further.
Thus we can conclude that if we assume our original statement is false then every number $M>N$ has a divisor $K$ that is between $2$ and $N$.
But consider the number $M$ defined as $N!+1 = (1\cdot 2 \cdots N) + 1$.
If we divide $M$ by any number $K$  between $2$ and $N$, the remainder is $1$ and so in particular $M$ is not evenly divisible by $K$, contradicting our claim above that $M$ must have a divisor in that range.
Hence the assumption that all primes are at most $N$ led to a contradiction, and so our original statement must have been true.

The above is a perfectly valid proof, but just like it is often helpful to break down a computer  program to several functions, it is often useful to break proofs into simpler claims.
Let us start by stating the statement as theorem:

> # {.theorem  title="Infinitude of primes" #inf-primes-thm}
For every natural number $N$, there exists a prime $p>N$.


To prove [inf-primes-thm](){.ref}, we use the following intermediate statement (called a "lemma" in mathspeak):

> # {.lemma title="Factoring" #inter-claim}
Every integer $M \geq 2$ can be written as a product $M=P\cdot A$ where $P$ is prime and $A$ is a positive natural number.


>#{.proof data-ref="inter-claim"}
We prove the lemma  by induction on $M$.^[We discuss proofs by induction below, and the [CS 121 website](http://www.boazbarak.org/cs121/background/) contains more links to resources.]
It is clearly true when $M=2$ since when $2$ is a prime and so we can write $2=2\cdot 1$.
To prove the claim we need to show that if it   is true for all numbers between $2$ and $M-1$ then it is true for $M$ as well.
If $M$ is prime, then since $M = M \cdot 1$, the claim is true for $M$ as well.
Otherwise, we can write $M=B\cdot C$ where both $B$ and $C$ are between $2$ and $M-1$.
Hence by the induction hypothesis we can write $B=P\cdot A'$ for prime $P$, which means that $M=P \cdot (A'\cdot C)$ hence proving the claim for $M$.^[Notice the similarity between proofs and code in how we "define" variables such as $P,A'$ which we can think of as being the values that are "returned" to us from a "recursive call" to the induction hypothesis. However, if you find this viewpoint more confusing than helpul, feel free to ignore it.]


We now use [inter-claim](){.ref} to prove [inf-primes-thm](){.ref}:

> # {.proof data-ref="inf-primes-thm"}
Suppose toward the sake of contradiction that there exists some $N$ s.t. all primes are between $2$ and $N$, and let $M$ be the number $N!+1 = (1\cdot 2 \cdot 3 \cdots N)+1$. By the claim, we can write $M = P\cdot A$ for a prime $P$, and so we get the equation
$$
PA =  (1 \cdots N) + 1  \;. \label{eqprimes}
$$
Divide both sides of [eqprimes](){.eqref} by $P$ to get
$$
A = (1\cdots N)/P + 1/P \;, \label{eqprimestwo}
$$
the lefthand side of [eqprimestwo](){.eqref} is a natural number, while, since $P$ is prime, under our assumption it is between $2$ and $N$, and hence the righthand side is equal to the natural number
$$
2 \times 3 \times \cdots \times (P-1) \times (P+1) \times \cdots \times N = \prod_{B \in \{2,\ldots,N\} \setminus \{P \}} B
$$
plus the fraction $1/P$, yielding a contradiction.^[We discuss below mathematical notation, including the shorthands $\sum$ and $\prod$ for sums and products.]


When you first start writing proofs, it is good to err on the side of being a little more rigorous and formal, but like in coding, you should always make sure that you are not adding _unnecessary_ formalism, and trying to obfuscate invalid reasoning by using formal symbols.
So (again like in programming) before you start writing down a proof formally, you want to make sure that you understand _what_ is the statement that you are trying to prove and _why_ it is in fact true.

> # {.exercise title="Irrationality of the square root of 3" #sqrt3irrat}
Write a proof that $\sqrt{3}$ is irrational in the following stages: \
a. Write a statement X that of the form "there are no integers $a$, $b$ that satisfy 'blah' " such that X will be  equivalent to the statement  "$\sqrt{3}$ is irrational". \
b. Convince _yourself_ that X is true. \
c. Write down an informal argument to convince a friend of yours that X is true. \
d. Write down a formal proof that X is true.

> # {.exercise title="Irrationality of square roots of primes" #sqrtPirrat}
Prove that for every prime number $p$,  $\sqrt{p}$ is irrational.
Is it possible to extend this to show that this is true even for numbers that are prime powers? In particular, can you show that if $n=p^4$ for a prime number $p$, then $\sqrt{n}$ is irrational?

### Writing proofs

Once you have convinced yourself that a statement $X$ is true, and you understand the logical argument that proves it, it is time to write down the proof.
A mathematical proof is a piece of writing, but it is a specific genre of writing with certain conventions and style.
As in any writing, practice makes perfect, and it is also important to revise your drafts for clarity.

In a proof for the statement $X$, all the text between the words "Proof:" and "QED" should be focused on establishing that $X$ is true.
Digressions, examples, or ruminations will just confuse the reader.
The proof should have a clear logical flow in the sense that every sentence or equation in it should have some purpose and it should be crystal-clear to the reader what this purpose is.
When you write a proof, for every equation or sentence you include, ask yourself:

1. Is this sentence or equation stating that some proposition is true?
2. If so, does this proposition follow from the previous steps,  or are we going to establish it in the next step?
3. What is the _role_ of this sentence or equation? Is it one step towards proving the original statement, or is it a step towards proving some intermediate claim that you have statebed before?
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
Every linear equation in one variable has a solution

> # {.proof}
Let $ax+b=0$ be a linear equation in the single variable $x$.
Since the equation involves the variable $x$, it must be that $a \neq 0$.
Hence $x = -b/a$ is a solution for the equation.

__Proofs of an implication:__ Another common case is that the statement $X$ has the form "$A$ implies $B$". Such proofs often start with a sentence such as "Assume that $A$ is true" and end with a derivation of $B$ from $A$.
Here is a simple example:

> # {.lemma }
If $b^2 \geq 4ac$ then there is a solution to the quadratic equation $ax^2 + bx + c =0$.

> # {.proof }
Suppose that $b^2 \geq 4ac$.
Then $d = b^2 - 4ac$ is a non-negative number and hence it has a square root $s$.
Then $x = (-b+s)/(2a)$ satisfies
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
We've seen an example of such a proof in [inf-primes-thm](){.ref}.

__Proofs by induction:__ We can think of such proofs as a variant of the above, where we have an unbounded number of intermediate claims $X_1,X_2,\ldots,X_n$, and we prove that $X_1$ is true, as well as that if $X_1 \wedge \ldots \wedge X_i$  is true then then $X_{i+1}$ is true. We discuss proofs by inductions below.





## Some discrete mathematics notions

We  now review some basic notions that we will use.
This is not meant to be a substitute for a course on discrete mathematics, and, as mentioned above, there are  excellent online resources to catch up on this material if needed.


## Sets

One of the most basic notation in mathematics is the notion of _sets_.
For example, when we write $S = \{ 2,4, 7 \}$, we mean that $S$ denotes the set that contains the numbers $2$, $4$, and $7$.
(We use the notation "$2 \in S$" to denote that $2$ is an element of $S$.)
Note that the set $\{ 2, 4, 7 \}$ and $\{ 7 , 4, 2 \}$ are identical, since they contain the same elements.
Also, a set either contains an element or does not contain it -there is no notion of containing it  "twice"- and so we could even write the same set $S$ as  $\{ 2, 2, 4, 7\}$ (though that would be a little weird).
The _cardinality_ of a finite set $S$, denoted by $|S|$, is the number of elements it contained.
So, in the example above, $|S|=3$.
A set $S$ is a _subset_ of a set $T$, denoted by $S \subseteq T$, if every element of $S$ is also an element of $T$.
For example, $\{2,7\} \subseteq \{ 2,4,7\}$.


We can define sets by either listing all their elements or by writing down a rule that they satisfy such as
$$
EVEN = \{ x\in \N \;:\; \text{ $x=2y$ for some non-negative integer $y$} \}
$$
where $\N=\{0,1,2,\ldots \}$ is the set of natural numbers.

Of course there is more than one way to write the same set, and often we will use intuitive notation listing a few examples that illustrate the rules, and hence we can also define $EVEN$ as
$$
EVEN = \{ 0,2,4, \ldots \} \;.
$$




Note that a set can be either finite  (such as the set $\{2,4,7\}$ ) or infinite (such as the set $EVEN$).
There are two sets that we will encounter time and again:
$$
\N = \{ 0, 1,2, \ldots \}
$$
is (as we've seen) the set of all natural numbers,^[Some texts define the natural numbers as the set $\{1,2,3,\ldots \}$. Like the style of bracing in a computer program, it doesn't make much difference which convention you choose, as long as you are consistent. In this course we will start the natural numbers from zero.]
and
$$
\{0,1\}^n = \{ (x_0,\ldots,x_{n-1}) \;:\; x_0,\ldots,x_{n-1} \in \{0,1\}  \}
$$
is the set of all $n$-length binary strings for some natural number $n$.
That is $\{0,1\}^n$ is the set of all length-$n$ lists of zeroes and ones.
We often write the string $(x_0,x_1,\ldots,x_{n-1})$ as simply $x_0x_1\cdots x_{n-1}$ and so we can write
$$
\{0,1\}^3 = \{ 000 , 001, 010 , 011, 100, 101, 110, 111 \} \;.
$$

We will use the notation $[n]$ for the set $\{0,\ldots, n-1\}$.
For every string $x\in \{0,1\}^n$ and $i\in [n]$, we write $x_i$ for the $i^{th}$ coordinate of $x$.
If $x$ and $y$ are strings, then $xy$  denotes their _concatenation_.
That is, if $x \in \{0,1\}^n$ and $y\in \{0,1\}^m$, then $xy$ is equal to the string $z\in \{0,1\}^{n+m}$ such that for $i\in [n]$, $z_i=x_i$ and for $i\in \{n,\ldots,n+m-1\}$, $z_i = y_{i-n}$.


Another set we will encounter is the set $\{0,1\}^*$ of binary strings of _all_ lengths $n$.
We can write it as
$$
\{0,1\}^* = \{ (x_0,\ldots,x_{n-1}) \;:\; n\in\N \;,\;, x_0,\ldots,x_{n-1} \in \{0,1\} \} \;.
$$
Another way to write it is as
$$
\{0,1\}^* = \{0,1\}^0 \cup \{0,1\}^1 \cup \{0,1\}^2 \cup \cdots
$$
or more concisely as
$$
\{0,1\}^* = \cup_{n\in\N} \{0,1\}^n \;,
$$
where $\cup$ denotes the _set union_ operation.
That is,  for sets $S$ and $T$, $S \cup T$ is the set that contains all elements that are either in $S$ or in $T$.^[One minor technicality is, that as we mentioned, the set $\{0,1\}^*$ contains also the "string of length $0$", which we denote by $\emptyset$.
This is just a technical convention, like starting the natural numbers from zero, and will not make any difference in almost all cases in this course, and so you can safely ignore this zero-length string 99.9\% of the time.]

The notions of lists/tuples and the $*$ operator extend  beyond the setting of binary strings. See any discrete mathematics text for their definitions, as well as the standard operators on sets which include not just union ($\cup$) but also intersection ($\cap$) and set difference ($\setminus$).



># {.exercise title="Inclusion Exclusion" #inclex }
a. Let $A,B$ be finite sets. Prove that $|A\cup B| = |A|+|B|-|A\cap B|$. \
b. Let $A_0,\ldots,A_{k-1}$ be finite sets. Prove that $|A_1 \cup \cdots \cup A_k| \geq \sum_{i=0}^{k-1} |A_i| - \sum_{0 \leq i < j < k} |A_i \cap A_j|$. \
c. Let $A_0,\ldots,A_{k-1}$ be finite subsets of $\{1,\ldots, n\}$, such that $|A_i|=m$ for every $i\in [k]$. Prove that if $k>100n$, then there exist two distinct sets $A_i,A_j$ s.t. $|A_i \cap A_j| \geq m^2/(10n)$.






## Functions

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
The following claims are left as exercises:

> # {.exercise }
Prove that if $S,T$ are finite and $F:S \rightarrow T$ is one to one then $|S| \leq |T|$.

> # {.exercise }
Prove that if $S,T$ are finite and $F:S \rightarrow T$ is onto then $|S| \geq |T|$.

If  $F:S \rightarrow T$ is both one-to-one and onto then by the claims above $|S|=|T|$ and for every $y\in T$ there is a unique $x\in S$ s.t. $F(x)=y$. We denote this value $x$ by $F^{-1}(y)$.
A  one-to-one and onto function is called a _bijection_.
Giving a bijection between two sets is often a good way to show they have  the same size, as in the following lemma.
(Making sure you understand both the statement and the proof of this lemma is a good way to verify that you are sufficiently comfortable with the notions of both sets and functions.)

> # {.lemma title="Power set" #powerset-lem}
For every finite $S$ and $T$, there are $|T|^{|S|}$ functions from $S$ to $T$

Before reading the proof it is good to verify the lemma for a few small examples.
For example, if $S$ is the set $\{0,1,2,3 \}$ and $T = \{0,1\}$, then a  function $F$ mapping  $S$ to $T$ can be described in a table with four rows, where in the second cell of the  $i^{th}$ row we can we write either $0$ or $1$ depending on $F(i)$.
So, for example the function $F$ where $F(x) = 3x/2 - x^2/2$ can be described by the table:


| Input | Output |
|:------|:-------|
| 0     | 0      |
| 1     | 1      |
| 2     | 1      |
| 3     | 0      |

   \


\


To specify a function $F: \{0,1,2,3 \} \rightarrow \{0,1\}$ we need to specify these four values that appear in the output column.
Since we have two choices for each one of these columns, the total number of functions is exactly $2^4$.
We now prove the lemma in general:



> # {.proof data-ref="powerset-lem"}
Let $S$ and $T$ be some finite sets of cardinalities $n$ and $m$ respectively.
To prove the lemma, we need to show that there are $m^n$ functions mapping $S$ to $T$.
Define $A$ to be the set $\{ 0,\ldots, m^n - 1\}$ and
define  $B$ to be the set $\{ F \;:\; F:S \rightarrow T \}$ of such functions.
We will prove the lemma by giving a bijection $G$ from $A$ to $B$.
Let us give some arbitrary ordering $s_0,\ldots,s_{n-1}$ to the elements of $S$ and another arbitrary ordering $t_0,\ldots,t_{m-1}$ to the elements of $T$.
Given some number $X\in A$, we  can write $X$ in the $m$ basis as $X=\sum_{i=0}^{n-1}X_im^i$ where for every $i\in\{0,\ldots,n-1\}$, $X_i \in \{0,\ldots,m-1\}$.
Now we define $G(X)$ to be the function $F_X:S \rightarrow T$ such that for every $i\in\{0,\ldots,n-1\}$, $F_X(s_i)= t_{X_i}$.
Because for every $X \neq X'$ there will be some digit $i$ on which $X_i \neq X'_i$, for this digit it will hold  $F_X(s_i) \neq F_{X'}(s_i)$  and hence $F_X \neq F_{X'}$ which means that the map $G$ is one-to-one.
Moreover, it is onto as well, since for every function $F:S \rightarrow T$, we can define $X=\sum_{i=0}^{n-1}X_i m^i$ where $X_i$ is equal to the $j\in \{0,\ldots,m-1\}$ such that $F(s_i)=t_j$.
By construction $F_X = X$ which demonstrates that $G(X)=F$ and hence $G$ is onto.


We will sometimes be interested in _partial_ functions from $S$ to $T$.
This is a function $F$ that is not necessarily defined on every element of $S$.
For example, the function $F(x)= \sqrt{x}$ is only defined on non-negative real numbers.
When we want to distinguish between partial functions and  standard (i.e., non-partial) functions, we will call the latter _total_ functions.
We can think of a partial function $F$ from $S$ to $T$ also as a total function from $S$ to $T \cup \{ \bot \}$ where $\bot$ is some special "failure symbol", and so instead of saying that $F$ is undefined at $x$, we can say that $F(x)=\bot$.


> # {.exercise }
Prove that for every finite $S,T$, there are $(|T|+1)^{|S|}$ partial functions from $S$ to $T$.

## Asymptotics and big-Oh notation

It is often very cumbersome to describe precisely  quantities such as running time, whereas we are typically only interested in the "higher order terms" or understanding the scaling of the quantity as the input variable grows.
For example, as far as running time goes, the difference between an $n^5$-time algorithm and an $n^2$-time one is much more significant than the difference between an $100n^2 + 10n$ time algorithm and an $10n^2$
For this purpose, Oh notation is extremely useful as a way to "declutter" our text,
so for example, we can say that both $100n^2 + 10n$ and $10n^2$ are simply $O(n^2)$ (which we call  "Big Oh" of $n^2$), while $n^2 = o(n^5)$ (which we call "little Oh" of $n^5$).


Intuitively, if $F,G$ are two functions mapping natural numbers to natural numbers,  you can think of "$F=O(G)$" as meaning that  $F(n) \leq G(n)$ if we don't care about constant factors, while you can think of "$F=o(G)$" as meaning that $F(n) < G(n)$ even if we mutliply $F$ by an arbitrary large constant factor (sometimes $F=o(G)$ is written as $F \ll G$).
More formally, we define Big Oh notation as follows:


> # {.definition title="Big Oh notation" #bigohdef}
For $F,G: \N \rightarrow \N$, we define $F=O(G)$ if there exist numbers $a,N_0 \in \N$ such that $F(n) \leq a\cdot G(n)$ for every $n>N_0$.
We define $F=\Omega(G)$ if $G=O(F)$.
>
We write $F =o(G)$ if for every $\epsilon>0$ there is some $N_0$ such that $F(n) <\epsilon G(n)$ for every $n>N_0$.
We write $F =\omega(G)$ if $G=o(F)$.


In most cases you can safely  interpret $F=O(G)$ as $F(n) \leq 100 G(n)$ and $F=\Omega(G)$ as $F(n) \geq 0.01 G(n)$. Similarly, in most cases you can pretend that $F=o(G)$ means that $F(n) \leq G(n)/\log G(n)$ and you will not lose much  in understanding.

We can also use the notion of _limits_ to define big and little oh notation.
You can verify that $F=o(G)$ (or, equivalently, $G=\omega(F)$) if and if $\lim\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)} = 0$.
Similarly, if the limit $\lim\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)}$ exists and is a finite number then $F(n)=O(G(n))$.
If you are familiar with the notion of _supremum_, then you can verify that $F=O(G)$ if and only if $\limsup\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)} < \infty$.

__Some "rules of thumbs" for big Oh notation:__
There are some simple heuristics that can help when trying to compare two functions $f$ and $g$:

* Multiplicative constants don't matter in Oh notation, and so if $f(n)=O(g(n))$ then $100f(n)=O(g(n))$.
* When adding two functions, we only care about the larger one. For example, for the purpose of Oh notation, $n^3+100n^2$ is the same as $n^3$, and in general in any polynomial, we only care about the larger exponent.
* For every two constants $a,b>0$, $n^a = O(n^b)$ if and only if $a \leq b$, and $n^a = o(n^b)$ if and only if $a<b$. For example, combining the two observations above, $100n^2 + 10n + 100 = o(n^3)$.
* Polynomial is always smaller than exponential: $n^a = o(2^{n^\epsilon})$ for every two constants $a>0$ and $\epsilon>0$ even if $\epsilon$ is much smaller than $a$. For example, $100n^{100} = o(2^{\sqrt{n}})$.
* Similarly, logarithmic is always smaller than polynomial: $(\log n)^a$ (which we write as $\log^a n$) is $o(n^\epsilon)$ for every two constants $a,\epsilon>0$. For example, combining the observations above, $100n^2\log^100 n = o(n^3)$.

> # {.exercise}
For every pair of functions $F,G$ below, determine which of the following relations holds: $F=O(G)$, $F=\Omega(G)$, $F=o(G)$ or $F=\omega(G)$. \
a. $F(n)=n$, $G(n)=100n$. \
b. $F(n)=n$, $G(n)=\sqrt{n}$.\
c. $F(n)=n$, $G(n)=2^{(\log (n))^2}$.\
d. $F(n)=n$, $G(n)=2^{\sqrt{\log n}}$

> # {.exercise}
Give an example of a pair of functions $F,G:\N \rightarrow \N$ such that neither $F=O(G)$ nor $G=O(F)$ holds.




## Proofs by induction

One common, but often tricky, method of proofs is to use _inductions_.
Induction is simply an application of the basic  [Modus Ponens](https://en.wikipedia.org/wiki/Modus_ponens) rule that says that if: \

 __(a)__ $P$ implies $Q$ \

and \

__(b)__ $P$ is true \
then $Q$ is true.

In the setting of induction we typically have a statement $Q(n)$ about an integer $n$, and we prove that: \

__(a)__ For every $n>0$, if $Q(0),\ldots,Q(n-1)$ are all true then $Q(n)$ is true \

 and \

 __(b)__ $Q(0)$ is true. \

(Usually proving __(a)__ is the hard part, though there are examples where the "base case" __(b)__ is quite subtle.)
By repeatedly applying Modus Ponens, we can see that $Q(1)$ is true, $Q(2)$ is true, etc.. and this implies that  $Q(n)$ is true for every $n$.

For example, to show the classical formula that the sum $S_n = 1+2+3+\cdots+n$ is equal to $(n+1)n/2$, we
first show this for the case $S_0$ in which indeed $0 = S_0 = (0+1)0/2$.
Then we need to show that if for every $i\leq n-1$, $S_i = (i+1)i/2$ then $S_n=(n+1)n/2$.
To do so we simply take $i=n-1$, and then $S_n = S_{n-1}+n = n(n-1)/2 +n = [n(n-1)+2n]/2= n(n+1)/2$.

> # {.exercise }
Suppose that $\{ S_n \}_{n\in \N}$ is a sequence such that $S_0 \leq 10$ and for $n>1$ $n \leq 5 S_{\lfloor \tfrac{n}{5} \rfloor} + 2n$.
Prove by induction that  $S_n \leq 100 n \log n$ for every $n$.

The website for CMU course 15-251 contains a [useful handout](http://www.cs.cmu.edu/~./15251/notes/induction-pitfalls.pdf) on potential pitfalls when making proofs by induction.


## Logic, graphs, discrete probability

Later in this course we will encounter several other topics including:

* Logical operators such as AND ($\wedge$), OR ($\vee$), and NOT ($\neg$), as well as the quantifiers $\forall$ and $\exists$.  

* Graphs: directed, and undirected, including notions such as degree, paths, connectivity, cycles and trees.

* Discrete probability: probabilistic events, random variable, expectation, variance and concentration (a.k.a tail) bounds.

As with the other topics mentioned here, you can review these notions using the  lecture notes of [Lehman, Leighton and Meyer](http://www.boazbarak.org/cs121/LLM_June17.pdf) or the other resources mentioned on the [CS 121 website](http://www.boazbarak.org/cs121/background/).

> # {.exercise }
Describe the following statement in English words: $\forall_{n\in\N} \exists_{p>n} \forall{a,b \in \N} (a\times b \neq p) \vee (a=1)$.

> # {.exercise }
Prove that for every undirected graph $G$ of $100$ vertices, if every vertex has degree at most $4$, then there exists a subset $S$ of at $20$ vertices such that no two vertices in $S$ are neighbors of one another.


> # {.exercise }
Suppose that we toss three independent fair coins $a,b,c \in \{0,1\}$. What is the probability that the XOR of $a$,$b$, and $c$ is equal to $1$? What is the probability that the AND of these three values is equal to $1$? Are these two events independent?

## Mathematical notation

We summarize some of the mathematical notation we use in this course.
Most of it is fairly standard, and can be found in any text on discrete mathematics:

* __Set notation:__ We write a set by either listing its elements (as in $\{1,2,3\}$) or writing some rule that specifies its members. We write $x\in S$ to indicate that $x$ is a member of the set $S$ and $A \subseteq B$ to indicate that $A$ is a subset of $B$.  We write $A \cup B$, $A \cap B$ and $A \setminus B$ for the union, intersection, and set difference operations respectively.
The _cardinality_ of a set is the number of elements it contains.

* __Special sets:__ The set $\{0,1\}^n$ is the set of 0/1 strings of length $n$, the set $\{0,1\}^*$ is the set of 0/1 strings of arbitrary finite length. The set $\N = \{0,1,2,3,\ldots\}$ is the set of natural numbers. We denote by $[n]$ is the set $\{0,1,\ldots,n-1\}$ of numbers between $0$ and $n-1$. We denote the _empty set_ (set with no elements) by $\emptyset$, and use the same symbol to also denote the empty string (string of zero length). If there is possibility for confusion then we will use `""` for the latter.

* __Indexing from zero:__
Note that we start the natural numbers from $0$, as opposed to $1$. Similarly, we use the set $[n]$ for $\{0,1,\ldots,n-1\}$ instead of $\{1,\ldots, n\}$. Also, if $x \in \{0,1\}^*$ is a string of length $k$, then we will index the coordinates of $x$ by $x_0,\ldots,x_{k-1}$.

* __More special sets:__ While the above are the most common ones, we will also use the set $\Z = \{ a\times b : a\in \N, b \in \{ +1,-1\} \} = \{ 0, \pm 1 , \pm 2 , \ldots \}$ of (positive, zero, or negative) _integers_,^[The letter Z stands for the German word "Zahlen" which means "numbers".] and the set $\R$ of _real numbers_ (that have a fractional component). Given any finite set $\Sigma$, we use $\Sigma^n$ to denote the set of length $n$ strings over the alphabet $\Sigma$ and $\Sigma^*$ to denote the set of all finite-length strings over the same alphabet.

* __Functions:__ If $S,T$ are sets, then we write $f:S \rightarrow T$ to indicate the $f$ is a function mapping elements of $S$ to elements of $T$. A _partial function_ is one that might not be defined on all inputs in $S$.

* __Summations, products:__ If $f:A \rightarrow B$ is some function and $C \subseteq A$, then we write $\sum_{x\in C} f(x)$ to denote that result of adding $f(x)$ for all $x$'s in $C$. The most common case is when $f$ is a function on $\N$ and $C = \{ a,a+1,\ldots,b-1,b \}$ in which case we often write this as $\sum_{n=a}^n f(n)$. We can also write $\prod_{x\in C} f(x)$ or $\prod_{n=a}^b f(n)$ to denote the result of taking a product over all these terms.

* __Graphs:__ A graph $G=(V,E)$ consists of a set of _vertices_ $V$ and a set of _edges_ $E$. In an _undirected_ graph, every member of $E$ is a size-two subset of $V$. In a _directed_ graph, every member of $E$ is an ordered pair of elements of $V$.
A vertex $v$ is a _neighbor_ of $u$ if the edge $(u,v)$ is in $E$.
A _path_ in the graph is a sequence $(v_0,v_1,\ldots,v_k)$ of vertices such that $v_{i+1}$ is a neighbor of $v_i$ for every $i\in [k]$.


## Acknowledgements
