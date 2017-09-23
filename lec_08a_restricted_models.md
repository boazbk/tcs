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
In this lecture we will discuss several such examples.


## Turing completeness as a bug

We have seen that seemingly simple formalisms can turn out to be Turing complete.
The [following webpage](http://beza1e1.tuxen.de/articles/accidentally_turing_complete.html) lists several examples of formalisms that "accidentally" turned out to Turing complete, including supposedly limited languages such as the C preprocessor, CCS, SQL, sendmail configuration, as well as games such as Minecraft, Super Mario, and  the card game "Magic: The gathering".
This is not always a good thing, as it means that such formalisms can give rise to arbitrarily complex behavior.
For example, the postscript format (a precursor of PDF) is a Turing-complete programming language meant to describe documents for printing.
The expressive power of postscript can allow for short description of very complex images.
But it also gives rise to some nasty surprises, such as the attacks described in  [this page](http://hacking-printers.net/wiki/index.php/PostScript) ranging from using infinite loops as a denial of service attack, to accessing the printer's file system.

An interesting recent example of the pitfalls of Turing-completeness arose in the context of the cryptocurrency [Ethereum](https://www.ethereum.org/).
The distinguishing feature of this currency is the ability to design "smart contract" using an expressive (and in particular Turing-complete) language.  
Whereas in our "human operated" economy, Alice and Bob might pool their funds together sign a contract to create a joint venture and agree that if condition X happens then they will invest in Charlie's company, Ethereum allows Alice and Bob to create a joint venture where Alice and Bob pool their funds together into an account that will be governed by some program $P$ that would decide under what conditions it disburses funds from it.
For example, one could imagine some code that interacts between Alice, Bob, and some program running on Bob's car that would allow Alice to rent out Bob's car without any human intervention or overhead.


Specifically Ethereum uses the Turing-complete programming  [solidity](https://solidity.readthedocs.io/en/develop/index.html) which has a syntax similar to Javascript.
The flagship of Ethereum was an experiment known as  The "Decentralized Autonomous Organization" or [The DAO](https://en.wikipedia.org/wiki/The_DAO_(organization)).
The idea was to create a smart contract that would create an autonomously run decentralized venture capital fund, without human managers, were shareholders could decide on investment opportunities.
The DAO was  the biggest crowdfunding success in history and at its height was worth 150 million dollars, which was more than ten percent of the total Ethereum market.
Investing in the DAO (or entering any other "smart contract") amounts to providing your funds to be run by a computer program. i.e., "code is law", or to use the words the DAO described itself: "The DAO is borne from immutable, unstoppable, and irrefutable computer code".
Unfortunately, it turns out that (as we'll see in the next lecture) understanding the behavior of Turing-complete computer programs is quite a hard thing to do.
A hacker (or perhaps, some would say, a savvy investor) was able to fashion an input that would cause the DAO code to essentially enter into an infinite recursive loop in which it continuously transferred funds into their account, thereby [cleaning out about 60 million dollars](https://www.bloomberg.com/features/2017-the-ether-thief/) out of the DAO.
While this transaction was "legal" in the sense that it complied with the code of the smart contract, it was obviously not what the humans who wrote this code had in mind.
There was a lot of debate in the Ethereum community how to handle this, including some partially successful "Robin Hood" attempts to use the same loophole to drain the DAO funds into a secure account.
Eventually it turned out that the code is mutable, stoppable, and refutable after all, and the Ethereum community decided to do a "hard fork" (also known as a "bailout") to revert history to before this transaction.
Some elements of the community strongly opposed this decision, and so an alternative currency called [Ethereum Classic](https://ethereumclassic.github.io/)  was created that preserved the original history.



## Regular expressions


If you have ever used an advanced text editor, a command line shell, you might have come across the notion of searching for files or objects using _wildcards_ and more generally _regular expression_.
At its heart, the _search problem_ is quite simple.
The user gives out a function $F:\{0,1\}^* \rightarrow \{0,1\}$, and the system applies this function to a set of candidates $\{ x_0, \ldots, x_k \}$, returning all the $x_i$'s such that $F(x_i)=1$.
However, we typically do not want the system to get into an infinite loop just trying to evaluate this function!
For this reason, such systems often do not allow the user to specify an _arbitrary_ function using some Turing-complete formalism, but rather a function that is described by a restricted computational model, and in particular one in which all functions halt.
One of the most popular models for this application is the model of  _regular expressions_.


A _regular expression_ over some alphabet $\Sigma$ is obtained by combining elements of $\Sigma$ with the operations $|$ (corresponding to _or_) and $*$ (corresponding to repetition zero or more times).
For example, the following regular expression over the alphabet $\{0,1\}$  corresponds to the set of all even length strings $x\in \{0,1\}^*$ such that $x_{2i}=x_{2i+1}$ for every $i\in \{0,\ldots, |x|/2-1 \}$:

$$
(00|11)*
$$

You have probably come across regular expressions in the context of searching for a file, doing search-and-replace in an editor,  or text manipulations in programming languages or tools such as `grep`.^[Standard implementations of regular expressions typically include some extra "syntactic sugar", but they can all be implemented using   the operators $|$ and $*$.]
Formally, regular expressions are defined by the following recursive definition:^[Just like recursive functions, we can define a concept recursively. A definition of some class $\mathcal{C}$ of objects can be thought of as defining a function that maps an object $o$ to either $0$ or $1$ depending on whether $o \in \mathcal{C}$. Thus we can think of   [regexp](){.ref} as defining a recursive function that maps a string $exp$ over $\Sigma \cup \{ "(",")","|", "*" \}$ to $0$ or $1$ depending on whether $exp$ describes a valid regular expression.]

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
However, it turns out that there is a much more efficient algorithm to match regular expressions.
One way to obtain such an algorithm is to replace this recursive algorithm with a dynamic program, using the technique of [memoization](https://en.wikipedia.org/wiki/Memoization).
It turns out that the resulting dynamic program only requires maintaining a finite (independent of the input length) amount of state, and hence it can be viewed as a [finite state machine](https://en.wikipedia.org/wiki/Finite-state_machine) or finite automata.
The relation of regular expressions with finite automate is a beautiful topic, and one we may return to later in this course.


The fact that functions computed by regular expressions always halt is of course one of the reason why they are so useful.
When you make a regular expression search, you are guaranteed that you will get a result.
This is   why operating systems, for example, restrict you for searching a file via regular expressions and don't allow searching by specifying an arbitrary function via a general-purpose programming language.
But this always-halting property comes at a cost.
Regular expressions cannot compute every function that is computable by NAND++ programs.
In fact there are some very simple (and useful!) functions that they cannot compute, such as the following:

> # {.theorem title="Matching parenthesis" #regexpparn}
Let $\Sigma = \{"(",")"\}$ and  $MATCHPAREN:\Sigma^* \rightarrow \{0,1\}$ be the function that given a string of parenthesis, outputs $1$ if and only if every opening parenthesis is matched by a corresponding closed one.
Then there is no regular expression over $\Sigma$ that computes $MATCHPAREN$.

[regexpparn](){.ref} is a consequence of the following result known as the _pumping lemma_:

> # {.theorem title="Pumping Lemma" #pumping}
Let $exp$ be a regular expression. Then there is some number $n_0$ such that for every $w\in \{0,1\}^*$ with $|w|>n_0$ and $\Phi_{exp}(w)=1$, it holds that we can write $w=xyz$ where  $|y| \geq 1$, $|xy| \leq n_0$ and such that $\Phi_{exp}(xy^nz)=1$ for every $n\in \N$.

![To prove the "pumping lemma" we look at a word $w$ that is much larger than the regular expression $exp$ that matches it. In such a case, part of $w$ must be matched by some sub-expression of the form $(exp')^*$, since this is the only operator that allows matching words longer than the expression. If we look at the "leftmost" such sub-expression and define $y^k$ to be the string that is matched by it, we obtain the partition needed for the pumping lemma.](../figure/pumpinglemma.png){#pumpinglemmafig .class width=300px height=300px}

> # {.proof data-ref="pumping"}
The idea behind the proof is simple (see [pumpinglemmafig](){.ref}). If we let $n_0$ be one plus the twice the number of symbols that are used in the expression $exp$, then the only way that there is some $w$ with $|w|>n_0$ and $\Phi_{exp}(w)=1$ is that $exp$ contains the $*$ (i.e. star) operator and that there is a nonempty substring $y$ of $w$ that was matched by $(exp')^*$ for some sub-expression $exp'$ of $exp$. Take the left  such expression $exp'$ (and so there is no star expression with a non-emptry match before it), and also the "innermost" (and so it does not contain a sub-expression that uses the star operator and matches a non-empty string). Then we know that the string $w$ has the form $xy^kz'$ where $y$ is a non-emptry string satisfying $\Phi_{exp'}(y)=1$, $k$ is a positive integer, and (since $exp$ does not contain a star before $exp'$ and $exp'$ does not contain a star), $|x|,|y| < n_0/2$.
Hence if we set $z = y^{k-1}z'$ then we get the conditions $|xy| \leq n_0$ and $|y|\geq 1$, and moreover, by the definition of the star operator, $\Phi_{exp}(xy^{n+k-1}z')=\Phi_{exp}(xy^nz)=1$ for every $n\in \N$.


> # {.proof data-ref="regexpparn"}
Given the pumping lemma, we can easily prove [regexpparn](){.ref}. Suppose, towards the sake of contradiction, that there is an expression $exp$ such that $\Phi_{exp}= MATCHPAREN$. Let $n_0$ be the number from [regexpparn](){.ref} and let
$w =(^{n_0})^{n_0}$. Then we see that if we write $w=xyz$ as in [regexpparn](){.ref}, the condition $|xy| \leq n_0$ implies that $y$ consists solely of left parenthesis. Hence the string $xy^2z$ will contain more left parenthesis than right parenthesis.


> # {.remark title="Regular expressions beyond searching" #netkat}
Regular expressions are widely used beyond just searching. First, they are typically used to define _tokens_ in various formalisms such as programming data description languages. But they are also used beyond it. One nice example is the recent work on the [NetKAT network programming language](http://www.cs.cornell.edu/~jnfoster/papers/frenetic-netkat.pdf). In recent years, the world of networking moved from fixed topologies to  "software defined networks", that are run by programmable switches that can implement policies such as "if packet is SSL then forward it to A, otherwise forward it to B". By its nature, one would want to use a formalism for such policies that is guaranteed to always halt (and quickly!) and that where it is possible to answer semantic questions such as "does C see the packets moved from A to B" etc. The NetKAT language uses a variant of regular expressions to achieve that.



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
