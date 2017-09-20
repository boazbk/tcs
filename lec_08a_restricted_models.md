# Restricted computational models


>_"Happy families are all alike; every unhappy family is unhappy in its own way"_,  Leo Tolstoy (opening of  the book "Anna Karenina").

Many natural computational models turn out to be _equivalent_ to one another, in the sense that we can transform a "program" of that other model (such as a $\lambda$ expression, or a game-of-life configurations) into a NAND++ program.
This equivalence implies that we can translate the uncomputability of the Halting problem for NAND++ programs into uncomputability for Halting in other models.
For example:

> # {.theorem title="Turing Machine Halting" #halt-tm}
Let $TMHALT:\{0,1\}^* \rightarrow \{0,1\}$ be the function that on input  strings $M\in\{0,1\}^*$ and $x\in \{0,1\}^*$ outputs $1$ if the Turing machine described by $M$ halts on the input $x$ and outputs $0$ otherwise. Then $TMHALT$ is uncomputable.

> # {.proof }
We have seen that for every NAND++ program $P$ there is an equivalent Turing machine $M(P)$ such that for every $x$, $M(P)$ halts on $x$ if and only $P$ halts on $x$ (and moreover if they both halt, they produce the same output).
The transformation of $P$ to $M(P)$ was completely algorithmic and hence it can be thought of as a computable function $M:\{0,1\}^* \rightarrow \{0,1\}^*$.
We see that $HALT(P,x)=TMHALT(M(P),x)$ and hence if we assume (towards the sake of a contradiction) that $TMHALT$ is computable then we get that $HALT$ is computable, hence contradicting [halt-thm](){.ref}.

The same proof carries over to other computational models such as the _$\lambda$ calculus_, _two dimensional_ (or even one-dimensional) _automata_ etc.
Hence for example, there is no algorithm to decide if a $\lambda$ expression evaluates the identity function, and no algorithm to decide whether an initial configuration of the game of life will result in eventually coloring the cell $(0,0)$ black or not.


The uncomputability of  halting and other semantic specification problems motivates coming up with __restricted computational models__ that are __(a)__ powerful enough to capture a set of functions useful for certain applications but __(b)__ weak enough that we can still solve semantic specification problems on them.
Here are some examples:

### Regular expressions

A _regular expression_ over some alphabet $\Sigma$ is obtained by combining elements of $\Sigma$ with the operations $|$ (corresponding to _or_) and $*$ (corresponding to repetition zero or more times).
For example, the following regular expression over the alphabet $\{0,1\}$  corresponds to the set of all even length strings $x\in \{0,1\}^*$ such that $x_{2i}=x_{2i+1}$ for every $i\in \{0,\ldots, |x|/2-1 \}$:

$$
(00|11)*
$$

You have probably come across regular expressions in the context of searching for a file, doing search-and-replace in an editor,  or text manipulations in programming languages or tools such as `grep`.^[Standard implementations of regular expressions typically include more "syntactic sugar" including shorthands such as $[a-d]$ for $(a|b|c|d)$ and others, but they can all be implemented using   the operators $|$ and $*$.]
Formally, regular expressions are defined by the following recursive definition:^[Just like recursive functions, we can define a concept recursively. Indeed, a definition of some class $\mathcal{C}$ of objects can be thought of as defining a function that maps an object $o$ to either $0$ or $1$ depending on whether $o \in \mathcal{C}$. Thus we can think of   the definition as defining a recursive function that maps a string $exp$ over $\Sigma \cup \{ "(",")","|", "*" \}$ to $0$ or $1$ depending on whether $exp$ describes a valid regular expression.]

> # {.definition title="Regular expression" #regexp}
A _regular expression_ $exp$ over an alphabet $\Sigma$ is a string over $\Sigma \cup \{ "(",")","|","*" \}$ that has one of the following forms:
1. $exp = \sigma$ where $\sigma \in \Sigma$ \
2. $exp = (exp' | exp'')$ where $exp', exp''$ are regular expressions. \
3. $exp = (exp')(exp'')$ where $exp',exp''$ are regular expressions. \
4. $exp = (exp')*$ where $exp'$ is a regular expression.^[Many texts also allow regular expressions that accept no strings or only the empty string. In the interest of simplicity, we drop these "edge cases" from our definition, though it does not matter much.]
>
Every regular expression $exp$ computes a function $\Phi_{exp}:\Sigma^* \rightarrow \{0,1\}$ defined as follows:
1. If $exp = \sigma$ then $\Phi_{exp}(x)=1$ iff $x=\sigma$ \
2. If $exp = (exp' | exp'')$ then $\Phi_{exp}(x) = \Phi_{exp'}(x) \vee \Phi_{exp''}(x)$ where $\vee$ is the OR operator. \
3. If $exp = (exp')(exp'')$ then $\Phi_{exp}(x) = 1$ iff there is some $x',x'' \in \Sigma^*$ such that $x$ is the concatenation of $x'$ and $x''$ and $\Phi_{exp'}(x')=\Phi_{exp''}(x'')=1$.  \
4. If $exp= (exp')*$ then $\Phi_{exp}(x)=1$ iff there are is $k\in \N$ and some $x_0,\ldots,x_{k-1} \in \Sigma^*$ such that $x$ is the concatenation $x_0 \cdots x_{k-1}$ and $\Phi_{exp'}(x_i)=1$ for every $i\in [k]$.

[regexp](){.ref} might not be easy to grasp in a first read, so you should probably pause here and go over it again   until you understand why it corresponds to our intuitive notion of regular expressions.
This is important not just for understanding regular expressions themselves (which are used time and again in a great many applications) but also for getting better at understanding recursive definitions in general.

By [regexp](){.ref}, regular expressions can be thought of as a "programming language" that defines functions $exp: \Sigma^* \rightarrow \{0,1\}$.
But it turns out that the "halting problem" for these functions is easy: they always halt.

> # {.theorem title="Regular expression always halt" #regularexphalt}
For every set $\Sigma$ and $exp \in (\Sigma \cup \{ "(",")","|","*" \})*$,  if $exp$ is a valid regular expression over $\Sigma$ then $\Phi_{exp}$ is a total function from $\Sigma^*$ to $\{0,1\}$.
Moreover, there is an always halting NAND++ program $P_{exp}$ that computes $\Phi_{exp}$.

> # {.proof data-ref="regularexphalt"}
[regexp](){.ref} gives a way of recursively computing $\Phi_{exp}$.
The key observation is that in our recursive definition of regular expressions, whenever $exp$ is made up of one or two expressions $exp',exp''$ then these two regular expressions are _smaller_ than $exp$, and eventually (when they have size $1$) then they must correspond to the non-recursive case of a single alphabet symbol.
>
Therefore, we can prove the theorem by induction over the length $m$ of $exp$.
For $m=1$, $exp$ is a single alhpabet symbol and the function $\Phi_{exp}$ is trivial.
In the general case, for $m=|exp$ we assume by the induction hypothesis that  we have proven the theorem for $|exp|  = 1,\ldots,m-1$.
Then by the definition of regular expressions, $exp$ is made up of one or two sub-expressions $exp',exp''$ of length smaller than $m$, and hence by the induction hypothesis we assume that $\Phi_{exp'}$ and   $\Phi_{exp''}$ are total computable functions.
But then we can follow the definition for the cases of concatenation, union, or the star operator to compute $\Phi_{exp}$ using $\Phi_{exp'}$ and $\Phi_{exp''}$.

The proof of [regularexphalt](){.ref} gives a recursive algorithm to evaluate whether a given string matches or not a regular expression.
However, it turns out that there is a much more efficient algorithm to match regular expressions, based on their connection to _finite automata_.
We will discuss this other algorithm, and this connection,  later in this course.

The fact that functions computed by regular expressions always halt is one of the reason why they are so useful.
When you make a regular expression search, you are guaranteed that you will get a result.
This is   why operating systems, for example, restrict you for searching a file via regular expressions and don't allow searching by specifying an arbitrary function via a general-purpose programming language.

But this always-halting property comes at a cost.
Regular expressions cannot compute every function that is computable by NAND++ programs.
In fact there are some very simple (and useful!) functions that they cannot compute, such as the following:

> # {.theorem title="Matching parenthesis" #regexpparn}
Let $\Sigma = \{"(",")"\}$ and  $MATCHPAREN:\Sigma^* \rightarrow \{0,1\}$ be the function that given a string of parenthesis, outputs $1$ if and only if every opening parenthesis is matched by a corresponding closed one.
Then there is no regular expression over $\Sigma$ that computes $MATCHPAREN$.

> # {.proof data-ref="regexpparn"}
TO BE COMPLETED



### Context free grammars.



Another example of uncomputable functions arises from the notions of _grammars_.
The idea of a grammar is best illustrated by an example.
Consider the set of all valid arithmetical expressions involving natural numbers, and the operators $+,-,\times,\div$.
We can describe this set recursively as follows:

$$
digit := 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
$$

$$
number := digit | digit number
$$

$$
expression := number | (expression + expression) | (expression - expression) | (expression \times expression) | (expression \div expression)
$$

A valid expression is any string in $\Sigma = \{ 0,1,2,3,4,5,6,7,8,9,0,(,),+,-,\times,\div \}^*$ that can be obtained by repeatedly applying some of these rules to the initial symbol $expression$ until we remain a string that does not contain $number$,$digit$ or $expression$ but  only symbols in $\Sigma$ (and hence cannot be reduced further).

^[TODO: maybe add here more example of context-sensitive grammar and then a proof that grammars are undecidable if there is in fact a simple proof of this (maybe based on lambda calculus?).]

More generally, a _grammar_ over an alphabet $\Sigma$ consists of a set of pairs of strings $(\alpha,\beta)$ where $\alpha,\beta \in (\Sigma \cup N)^*$ and $N$ is some finite set disjoint from $\Sigma$ containing a special symbol we call $start$.
$\Sigma$ is known as the set of _terminals_ and $N$ as the set of _non terminals_.

A grammar defines a subset $L \subseteq \Sigma^*$ (known as a _language_) as follows:
$x$ is in $\Sigma$ if and only if there exists some finite sequence of rules such that if we start from the string $start$ and each time replace a substring of the current string $\alpha$ with the corresponding righthand side of the rule $\beta$, then we eventually end up with $x$.











## Lecture summary

* The uncomputability of the Halting problem for general models motivates the definition of restricted computational models.

* In restricted models we might be able to answer questions such as: does a given program terminate, do two programs compute the same function?


## Exercises

> # {.exercise title="Halting problem" #halting-alt-ex}
Give an alternative, more direct, proof for the uncomputability of the Halting problem.
Let us define $H:\{0,1\}^* \rightarrow \{0,1\}$ to be the function such that $H(P)=1$ if, when we interpret $P$ as a program, then $H(P)$ equals $1$ if  $P(P)$ halts (i.e., invoke $P$ on its own string representation) and $H(P)$ equals $0$ otherwise.
Prove that  there no  program $P^*$ that computes $H$, by building from such a supposed $P^*$ a program $Q$ such  that, under the assumption that $P^*$ computes $H$, $Q(Q)$ halts if and only if it does not halt.^[__Hint:__ See Christopher Strachey's letter in the biographical notes.]





> # {.exercise title="Rice's Theorem (slightly restricted form)" #rice-ex}
1. Generalize the result that $COMPUTES\text{-}PARITY$ is uncomputable as follows. Prove that for every computable function $F:\{0,1\}^* \rightarrow \{0,1\}^*$, the function $COMPUTES\text{-}F$ which on input a NAND++ program $P$, outputs $1$ iff it holds that $P(x)=F(x)$ for every $x$, is uncomputable. \
2. Generalize this even further to show that for  every nontrivial (neither emptry nor the entire set) subset $\mathcal{S}$ of the set $\mathbb{R}$ of the  computable functions from $\{0,1\}^*$ to $\{0,1\}^*$, the function $COMPUTES\text{-}\mathcal{S}$ that outputs $1$ on a program $P$ if and only if $P$ computes some function in $\mathcal{S}$, is uncomputable.^[__Hint:__ Pick some $F\in\mathcal{S}$ and for every Turing machine $Q$ and input $x$, construct a machine $P_{Q,x}$ that either computes $F$ or computes nothing, based on whether $Q$ halts on $x$.]



## Bibliographical notes

^[TODO:  Add letter of Christopher Strachey to the editor of The Computer Journal.
Explain right order of historical achievements.
Talk about intuitionistic, logicist, and formalist approaches for the foudnations of mathematics.
Perhaps analogy to veganism.
State the full Rice's Theorem and say that it follows from the same proof as in the exercise.]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
