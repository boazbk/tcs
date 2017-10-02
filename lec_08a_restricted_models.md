# Restricted computational models

> # { .objectives }
* See that Turing completeness is not always a good thing
* Two important examples of non-Turing-complete, always-halting formalisms: _regular expressions_ and _context-free grammars_.
* The pumping lemmas for both these formalisms, and examples of non regular and non context-free functions.
* Unrestricted grammars, and another example of an uncomputable function.  

>_"Happy families are all alike; every unhappy family is unhappy in its own way"_,  Leo Tolstoy (opening of  the book "Anna Karenina").

Many natural computational models turn out to be _equivalent_ to one another, in the sense that we can transform a "program" of that other model (such as a $\lambda$ expression, or a game-of-life configurations) into a NAND++ program.
This equivalence implies that we can translate the uncomputability of the Halting problem for NAND++ programs into uncomputability for Halting in other models.
For example:

> # {.theorem title="Turing Machine Halting" #halt-tm}
Let $TMHALT:\{0,1\}^* \rightarrow \{0,1\}$ be the function that on input  strings $M\in\{0,1\}^*$ and $x\in \{0,1\}^*$ outputs $1$ if the Turing machine described by $M$ halts on the input $x$ and outputs $0$ otherwise. Then $TMHALT$ is uncomputable.

> # { .pause }
Once again, this is a good point for you to stop and try to prove the result yourself before reading the proof below.

> # {.proof }
We have seen in [TM-equiv-thm](){.ref} that for every NAND++ program $P$ there is an equivalent Turing machine $M_P$ such that for every $x$, $M_P$ halts on $x$ if and only $P$ halts on $x$ (and moreover if they both halt, they produce the same output).
Going back to the proof of [TM-equiv-thm](){.ref}, we can see that the transformation of the program $P$ to the Turing machine $M(P)$ was described in a _constructive_ way.
Specifically, we gave explicit instructions as to how to obtain a Turing Machine $M'$ that computes the _next step_ function of $P$, and then construct a Turing machine $M_P$ that repeatedly executes the instructions of $M'$ until we reach a halting configuration.
In particular if $P$ does _not_  reach a halting configuration on an input $x$ then neither will $M_P$.
>
Thus, we can view the proof of [TM-equiv-thm](){.ref} as a high level description of an _algorithm_ to obtain $M_P$ from the program $P$, and using our "have your cake and eat it too" paradigm, this means that there exists also a NAND++ program $R$ such  that computes the map $P \mapsto M_P$.
We see that
$$
HALT(P,x)=TMHALT(M_P,x)=TMHALT(R(P),x) \label{eqtmhalt}
$$
and hence if we assume (towards the sake of a contradiction) that $TMHALT$ is computable then [eqtmhalt](){.eqref} implies that $HALT$ is computable, hence contradicting [halt-thm](){.ref}.


The same proof carries over to other computational models such as the _$\lambda$ calculus_, _two dimensional_ (or even one-dimensional) _automata_ etc.
Hence for example, there is no algorithm to decide if a $\lambda$ expression evaluates the identity function, and no algorithm to decide whether an initial configuration of the game of life will result in eventually coloring the cell $(0,0)$ black or not.


The uncomputability of  halting and other semantic specification problems motivates coming up with __restricted computational models__ that are __(a)__ powerful enough to capture a set of functions useful for certain applications but __(b)__ weak enough that we can still solve semantic specification problems on them.
In this lecture we will discuss several such examples.


## Turing completeness as a bug

We have seen that seemingly simple computational models or systems  can turn out to be Turing complete.
The [following webpage](http://beza1e1.tuxen.de/articles/accidentally_turing_complete.html) lists several examples of formalisms that "accidentally" turned out to Turing complete, including supposedly limited languages such as the C preprocessor, CCS, SQL, sendmail configuration, as well as games such as Minecraft, Super Mario, and  the card game "Magic: The gathering".
This is not always a good thing, as it means that such formalisms can give rise to arbitrarily complex behavior.
For example, the postscript format (a precursor of PDF) is a Turing-complete programming language meant to describe documents for printing.
The expressive power of postscript can allow for short description of very complex images.
But it also gives rise to some nasty surprises, such as the attacks described in  [this page](http://hacking-printers.net/wiki/index.php/PostScript) ranging from using infinite loops as a denial of service attack, to accessing the printer's file system.

An interesting recent example of the pitfalls of Turing-completeness arose in the context of the cryptocurrency [Ethereum](https://www.ethereum.org/).
The distinguishing feature of this currency is the ability to design "smart contracts" using an expressive (and in particular Turing-complete) language.  
In our current "human operated" economy, Alice and Bob might  sign a contract to  agree that if condition X happens then they will jointly invest in Charlie's company. Ethereum allows Alice and Bob to create a joint venture where Alice and Bob pool their funds together into an account that will be governed by some program $P$ that  decides under what conditions it disburses funds from it.
For example, one could imagine a piece of code that interacts between Alice, Bob, and some program running on Bob's car that allows Alice to rent out Bob's car without any human intervention or overhead.


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


One of the most common tasks in computing is to _search_ for a piece of text.
At its heart, the _search problem_ is quite simple.
The user gives out a function $F:\{0,1\}^* \rightarrow \{0,1\}$, and the system applies this function to a set of candidates $\{ x_0, \ldots, x_k \}$, returning all the $x_i$'s such that $F(x_i)=1$.
However, we typically do not want the system to get into an infinite loop just trying to evaluate this function!
For this reason, such systems often do not allow the user to specify an _arbitrary_ function using some Turing-complete formalism, but rather a function that is described by a restricted computational model, and in particular one in which all functions halt.
One of the most popular models for this application is the model of  [regular expressions](https://en.wikipedia.org/wiki/Regular_expression).
You have probably come across regular expresions if you  ever used an advanced text editor, a command line shell, or have done any kind of manipulations of text files.^[Sections 1.3 and 1.4 in [Sipser's book](https://www.google.com/search?q=introduction+to+the+theory+of+computation) are excellent resources for regular expressions. Sipser's book also discusses the equivalence of regular expressions with _finite automata_.]


A _regular expression_ over some alphabet $\Sigma$ is obtained by combining elements of $\Sigma$ with the operations $|$ (corresponding to _or_) and $*$ (corresponding to repetition zero or more times).^[Common implementations of regular expressions in programming languages and shells typically include some extra  operations on top of $|$ and $*$, but these can all be implemented as "syntactic sugar" using   the operators $|$ and $*$.]
For example, the following regular expression over the alphabet $\{0,1\}$  corresponds to the set of all even length strings $x\in \{0,1\}^*$ such that $x_{2i}=x_{2i+1}$ for every $i\in \{0,\ldots, |x|/2-1 \}$:

$$
(00|11)*
$$

Formally, regular expressions are defined by the following recursive definition:^[Just like recursive functions, we can define a concept recursively. A definition of some class $\mathcal{C}$ of objects can be thought of as defining a function that maps an object $o$ to either $0$ or $1$ depending on whether $o \in \mathcal{C}$. Thus we can think of   [regexp](){.ref} as defining a recursive function that maps a string $exp$ over $\Sigma \cup \{ "(",")","|", "*" \}$ to $0$ or $1$ depending on whether $exp$ describes a valid regular expression.]

> # {.definition title="Regular expression" #regexp}
A _regular expression_ $exp$ over an alphabet $\Sigma$ is a string over $\Sigma \cup \{ "(",")","|","*" \}$ that has one of the following forms:
1. $exp = \sigma$ where $\sigma \in \Sigma$ \
2. $exp = (exp' | exp'')$ where $exp', exp''$ are regular expressions. \
3. $exp = (exp')(exp'')$ where $exp',exp''$ are regular expressions. \
4. $exp = (exp')*$ where $exp'$ is a regular expression.^[The standard definition of regular expressions  adds some additional syntax to allow a regular expressions that accepts only the empty string, as well as a regular expression accepts no strings. In the interest of simplicity, we drop this "edge cases" from the  definition we use in these notes, though it does not matter much.]
>
Every regular expression $exp$ computes a function $\Phi_{exp}:\Sigma^* \rightarrow \{0,1\}$ defined as follows:
1. If $exp = \sigma$ then $\Phi_{exp}(x)=1$ iff $x=\sigma$ \
2. If $exp = (exp' | exp'')$ then $\Phi_{exp}(x) = \Phi_{exp'}(x) \vee \Phi_{exp''}(x)$ where $\vee$ is the OR operator. \
3. If $exp = (exp')(exp'')$ then $\Phi_{exp}(x) = 1$ iff there is some $x',x'' \in \Sigma^*$ such that $x$ is the concatenation of $x'$ and $x''$ and $\Phi_{exp'}(x')=\Phi_{exp''}(x'')=1$.  \
4. If $exp= (exp')*$ then $\Phi_{exp}(x)=1$ iff there are is $k\in \N$ and some $x_0,\ldots,x_{k-1} \in \Sigma^*$ such that $x$ is the concatenation $x_0 \cdots x_{k-1}$ and $\Phi_{exp'}(x_i)=1$ for every $i\in [k]$.
>
We say that a function $F:\Sigma^* \rightarrow \{0,1\}$ is _regular_ if $F=\Phi_{exp}$ for some regular expression $exp$. We say that a set $L \subseteq \Sigma^*$ (also known as a _language_) is _regular_ if the function $F$ s.t. $F(x)=1$ iff $x\in L$ is regular.

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



## Context free grammars.

If you have ever written a program, you've  experienced  a _syntax error_.
You might have had also the experience of your program entering into an _infinite loop_.
What is less likely is that the compiler or interpreter entered an infinite loop when trying to figure out if your program has a syntax error.
When a person designs a programming language, they need to come up with a function $VALID:\{0,1\}^* \rightarrow \{0,1\}$ that determines the strings that correspond to valid programs in this language.
The compiler or interpreter computes $VALID$ on the string corresponding to your source code to determine if there is a syntax error.
To ensure that the compiler will always halt in this computation, language designers  typically _don't_ use a general Turing-complete mechanism to express the function $VALID$, but rather a restricted computational model.
One of the most popular choices for such a model is _context free grammar_.

To explain context free grammars, let's begin with a canonical example.
Let us try to define a function $ARITH:\Sigma^* \rightarrow \{0,1\}$ that takes as input a string $x$ over the alphabet $\Sigma = \{ (,),+,-,\times,\div,0,1,2,3,4,5,6,7,8,9\}$ and returns $1$ if and only if the string $x$ represents a valid arithmetic expression.
Intuitively, we build expressions by applying an operation to smaller expressions, or enclosing them in parenthesis, where the "base case" corresponds to expressions that are simply numbers.
A bit more precisely, we can make the following definitions:

* A _number_ is either $0$ or a sequence of digits not starting with $0$.

* An _operation_ is one of $+,-,\times,\div$

* An _expression_ has either the form "_number_" or the form  "_subexpression1 operation subexpression2_" or "(_subexpression_)".

A context free grammar is a formal way of specifying such conditions.^[Sections 2.1 and 2.3 in [Sipser's book](https://www.google.com/search?q=introduction+to+the+theory+of+computation) are excellent resources for context free grammars.]

> # {.definition title="Context Free Grammar" #defcfg}
Let $\Sigma$ be some finite set. A _context free grammar (CFG) over $\Sigma$_ is a triple $(V,R,s)$ where $V$ is a set disjoint from $\Sigma$ of _variables_, $R$ is a set of _rules_, which are pairs $(v,z)$ where $v\in V$ and $z\in (\Sigma \cup V)^*$, and $s\in V$ is the starting rule. We require that for every rule $(v,z)\in R$, if $z$ contains an element in $V$ then it must also contain at least one element in $\Sigma$.
>  
IF $G=(V,R,s)$ is a context-free grammar over $\Sigma$, then for two strings $\alpha,\beta \in (\Sigma \cup V)^*$ we say that $\beta$ _can be derived in one step_ from $\alpha$, denoted by  $\alpha \rightarrow_G \beta$, if there exist a rule $(v,z) \in R$ and strings $\alpha',\alpha'' \in (\Sigma \cup V)^*$ such that $\alpha = \alpha'v\alpha''$ and $\beta=\alpha'z\alpha''$.
We say that $\beta$ can be derived from $\alpha$, denoted by $\alpha \rightsquigarrow_G \beta$ if there exist $k\in \N$. $\alpha_1,\alpha_2,\ldots,\alpha_{k-1}$ such that $\alpha \rightarrow_G \alpha_1 \rightarrow_G \alpha_2 \rightarrow_G \cdots \rightarrow_G \alpha_{k-1} \rightarrow_G \beta$.
>
We define the _function computed by_ $(V,R,s)$ to be the map $\Phi_{V,R,s}:\Sigma^* \rightarrow \{0,1\}$ such that $\Phi_{V,R,s}(x)=1$ iff  $s \rightsquigarrow_G x$.
We say that $F:\Sigma^* \rightarrow \{0,1\}$ is _context free_ if $F = \Phi_{V,R,s}$ for some CFG $(V,R,s)$ we say that a set $L \subseteq \Sigma^*$ (also knoan as a _language_) is _context free_ if the function $F$ such that $F(x)=1$ iff $x\in L$ is context free.


that is recursively defined as follows:
>
* For every $x\in \Sigma^*$, $\Phi_{V,R,s}(x)=1$ if there exists some $k\in \N$ and some strings $a_0,\ldots,a_{k},w_1,\ldots,w_{k} \in \Sigma^*$ and variables $v_1,\ldots,v_k \in V$ such that:
   - $x= a_0w_1a_1w_2a_2 \cdots w_ka_k$
   - The rule $(s,a_0v_1w_1a_2w_2 \cdots v_ka_k)$ is in $R$.
   - For every $i\in \{1,\ldots,k\}$, $\Phi_{V,R,v_i}(w_i)=1$.



A priori it might not be clear that the function $\Phi_{V,R,s}$ above is well defined, but since the second member of every rule either contains no element of $v$ or contains at least one element of $\Sigma$, we get that if $k>0$, $|w_1|+\cdots+|w_k| < |x|$. and hence this recursive definition always involves calls to $\Phi_{V,R,v}$ on inputs $w_i$ that are smaller than $x$.
By the same reasoning, for every context-free grammar $(V,R,s)$ there is a recursive algorithm to compute the function $\Phi_{V,R,s}$ that always terminates.
In particular the "halting problem" for context free grammars is trivial, or in other words, we have the following theorem:

> # {.theorem title="Context-free grammars always halt" #CFGhalt}
For every CFG $(V,R,s)$ over $\Sigma$, the function $\Phi_{V,R,s}:\Sigma^* \rightarrow \{0,1\}$ is computable.^[While formally we only defined computability of functions over $\{0,1\}^*$, we can extend the definition to functions over any finite $\Sigma^*$ by using any one-to-one encoding of $\Sigma$ into $\{0,1\}^k$ for some finite $k$. It is a (good!) exercise to verify that if a function is computable with respect to one such encoding, then it is computable with respect to them all.]

> # { .pause }
[CFGhalt](){.ref} can be proven via the recursive algorithm sketched above, but it would be a great exercise for you to work out both the details of the algorithm, as well as the proof that it always halts with the correct answer. As a hint, such a proof is easiest done by induction on the length of the input, since all of our recursive calls always involve innputs of shorter length than the original one.


The example above of well-formed arithmetic expressions can be captured formally by the following context free grammar:

* The alphabet $\Sigma$ is  $\{ (,),+,-,\times,\div,0,1,2,3,4,5,6,7,8,9\}$
* The variables are $V = \{ expression, operation \}$.
* The rules  are the  set $R$ containing the following pairs:^[For the sake of clarify, we use quotation marks $".."$ to enclose the string which is the second pair of each rule. Also, note that our rules below,  slightly differ from those illustrated above. The two sets of rules compute the same function, but the description below has been modified to be an equivalent form of the reulsts above that doesn't have a rule whose righthand side is only variables. We could have also relaxed the condition of containing an alphabet symbol by only requiring that rules with no alphabet symbols induce a _directed acyclic graph_ over the variables.]
   - $(number,"0")$ and $(number,"1number")$,$\ldots$, $(number,"9number")$
   - $(expression,"(expression)")$,$(expression,"expression+expression")$,$(expression,"expression-expression")$,$(expression,"expression \times expression")$,$(expression,expression \div expression)$, $(expression,"0")$,$(expression,"1number")$,$\ldots$,$(expression,"9number")$.

* The starting variable is $expression$

For clarity, we will often write a rule of the form $(v,\alpha)$ as $v \mapsto \alpha$.
There are various notations to write context free grammars in the literature, with one of the most common being [Backus–Naur form](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) where we write a rule of the form $v\mapsto a$ (where $v$ is a variable and $a$ is a string) in the form  `<v> := a`.
If we have several rules of the form $v \mapsto a$, $v \mapsto b$, and $v \mapsto c$ then we can combine them as `<v> := a|b|c` (and this similarly extends for the case of more rules).



While we can (and people do) talk about context free grammars over any alphabet $\Sigma$, in the following we will restrict ourselves to $\Sigma=\{0,1\}$. This is of course not a big restriction, as any finite alphabet $\Sigma$ can be encoded as strings of some finite size.
It turns out that context free grammars can capture every regular expression:

> # {.theorem title="Context free grammars and regular expressions" #CFGreg}
Let $exp$ be a regular expression over $\{0,1\}$, then there is a CFG $(V,R,s)$ over $\{0,1\}$ such that $\Phi_{V,R,s}=\Phi_{exp}$.

> # {.proof data-ref="CFGreg"}
We will prove this by induction on the length of $exp$. If $exp$ is an expression of one bit length, then $exp=0$ or $exp=1$, in which case we leave it to the reader to verify that there is a (trivial) CFG that computes it.
Otherwise, we fall into one of the following case: __case 1:__ $exp = exp'exp''$, __case 2:__ $exp = exp'|exp''$ or __case 3:__ $exp=(exp')^*$ where in all cases $exp',exp''$ are shorter regular expressions. By the induction hypothesis have grammars $(V',R',s')$ and $(V'',R'',s'')$ that compute $\Phi_{exp'}$ and $\Phi_{exp''}$ respectively. By renaming of variables, we can also assume without loss of generality that $V'$ and $V''$ are disjoint.
>
In case 1, we can define the new grammar as follows: we add a new starting variable $s \not\in V \cup V'$ and the rule $s \mapsto  s's''$.
In case 2, we can define the new grammar as follows: we add a new starting variable $s \not\in V \cup V'$ and the rules $s \mapsto s'$ and $s \mapsto s''$.
Case 3 will be the only one that uses _recursion_. As before  we add a new starting variable $s \not\in V \cup V'$, but now add the rules $s \mapsto ""$ (i.e., the empty string) and also add for every rule of the form $(s',\alpha) \in R'$ the rule $s \mapsto s\alpha$ to $R$.
>
We leave it to the reader as (again a very good!) exercise to verify that in all three cases the grammars we produce  capture the same function as the original expression.

It turns out that CFG's are strictly more powerful than regular expressions. In particular, the "matching parenthesis" function can be computed by a context free grammar.
Specifically, consider the grammar $(V,R,s)$ where $V=\{s\}$ and $R$ is $s \mapsto ""$, $s \mapsto (s)s$, and $s \mapsto s(s)$. It is not hard to see that it captures exactly the set of strings over $\{ (,)\}$ that correspond to matching parenthesis.
However, there are some simple languages that are _not_ captured by context free grammars, as can be shown via the following version of [pumping](){.ref}

> # {.theorem title="Context-free pumping lemma" #cfgpumping}
Let $(V,R,s)$ be a CFG over $\Sigma$, then there is some $n_0\in \N$ such that for every $x \in \Sigma^*$ with $|\sigma|>n_0$, if $\Phi_{V,R,s}(x)=1$ then $x=abcde$ such that $|b|+|c|+|d| \leq n_1$, $|b|+|d| \geq 1$, and $\Phi_{V,R,s}(ab^kcd^ke)=1$ for every $k\in \N$.

> # {.proof data-ref="cfgpumping"}
We only sketch the proof. The idea is that if the total number of symbols in the rules $R$ is $k_0$, then the only way to get $|x|>k_0$ with $\Phi_{V,R,s}(x)=1$ is to use _recursion_.
That is there must be some $v \in V$ such that by a sequence of rules we are able to derive from $v$ the value $bvd$ for some strings $b,d \in \Sigma^*$ and then further on derive from $v$ the string $c\in \Sigma^*$ such that $bcd$ is a substring of $x$. If try to take the minimal such $v$ then we can ensure that $|bcd|$ is at most some constant depending on $k_0$ and we can set $n_0$ to be that constant ($n_0=10|R|k_0$ will do, since we will not need more than $|R|$ applications of rules, and each such application can grow the string by at most $k_0$ symbols).
Thus by the definition of the grammar, we can repeat the derivation to replace the substring $bcd$ in $x$ with $b^kcd^k$ for every $k\in \N$ while retaining the property that the output of $\Phi_{V,R,s}$ is still one.

Using [cfgpumping](){.ref} one can show that even the simple function $F(x)=1$ iff $x =  ww$ for some $w\in \{0,1\}^*$ is not context free. (In contrast, the function $F(x)=1$ iff $x=ww^R$ for $w\in \{0,1\}^*$ where for $w\in \{0,1\}^n$, $w^R=w_{n-1}w_{n-2}\cdots w_0$ is context free, can you see why?.)



> # {.remark title="Parse trees" #parsetreesrem}
While we present CFGs as merely _deciding_ whether the syntax is correct or not, the algorithm to compute $\Phi_{V,R,s}$ actually gives more information than that. That is, on input a string $x$, if $\Phi_{V,R,s}(x)=1$ then the algorithm yields the sequence of rules that one can apply from the starting vertex $s$ to obtain the final string $x$. We can think of these rules as determining a connected directed acylic graph (i.e., a _tree_) with $s$ being a source (or _root_) vertex and the sinks (or _leaves_)  corresponding to the substrings of $x$ that are obtained by the rules that do not have a variable in their second element. This tree is known as the _parse tree_ of $x$, and often yields very useful information about the structure of $x$.
Often the first step in a compiler or interpreter for a programming language is a _parser_ that transforms the source into the parse tree (often known in this context as the [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree)). There are also tools that can automatically convert a description of a context-free grammars into a _parser_ algorithm that computes the parse tree of a given string. (Indeed, the above recursive algorithm can be used to achieve this, but there are much more efficient versions, especially for grammars that have [particular forms](https://en.wikipedia.org/wiki/LR_parser), and programming language designers often try to ensure their languages have these more efficient grammars.)

## Unrestricted grammars

The reason we call context free grammars "context free" is because if we have a rule of the form $v \mapsto a$ it means that we can always replace $v$ with the string $a$, no matter the _context_ in which $v$ appears.
More generally, we want to consider cases where our replacement rules depend on the context.^[TODO: add example]
This gives rise to the notion of _general grammars_ that allow rules of the form $(a,b)$ where both $a$ and $b$ are strings over $(V \cup \Sigma)^*$.
The idea is that if, for example, we wanted to enforce the condition that we only apply some rule such as $v \mapsto 0w1$  when $v$ is surrounded by three zeroes on both sides, then we could do so by adding a rule of the form $000v000 \mapsto 0000w1000$ (and of course we can add much more general conditions).
Formally we make the following definition

> # {.definition title="General Grammar" #defcfg}
Let $\Sigma$ be some finite set. A  _grammar_ (also known as a _general_ or _unrestricted_ grammar) over $\Sigma$ is a triple $(V,R,s)$ where $V$ is a set disjoint from $\Sigma$ of _variables_, $R$ is a set of _rules_, which are pairs $(z',z)$ where  $z,z'\in (\Sigma \cup V)^*$, and $s\in (\Sigma \cup V)^*$ is the starting string.
>
Ig $(V,R,s)$ is a grammar over $\Sigma$, then the function computed by $(V,R,s)$ is the map $\Phi_{V,R,s}:\Sigma^* \rightarrow \{0,1\}$ that is recursively defined as follows:
>
* For every $x\in \Sigma^*$, $\Phi_{V,R,s}(x)=1$ if there exists some $k\in \N$ and some strings $a_0,\ldots,a_{k},w_1,\ldots,w_{k} \in \Sigma^*$ and variables $v_1,\ldots,v_k \in V$ such that:
   - $x= a_0w_1a_1w_2a_2 \cdots w_ka_k$
   - The rule $(s,a_0v_1w_1a_2w_2 \cdots v_ka_k)$ is in $R$.
   - For every $i\in \{1,\ldots,k\}$, $\Phi_{V,R,v_i}(w_i)=1$.
>
We say that $F:\Sigma^* \rightarrow \{0,1\}$ is _context free_ if $F = \Phi_{V,R,s}$ for some CFG $(V,R,s)$ we say that a set $L \subseteq \Sigma^*$ (also known as a _language_) is _context free_ if the function $F$ such that $F(x)=1$ iff $x\in L$ is context free.

Like context free grammars, this definition yields a natural recursive algorithm for computing $\Phi_{V,R,s}$.
However, unlike the case of CFGs, we are not necessarily guaranteed that the algorithm will terminate, as the recursive calls are not guaranteed to use inputs shorter than the original input.^[This does not mean that the algorithm will necessarily _not_ terminate, but it does mean that we can't use the same argument we used above]
However, we can still make the function above well defined by stating that $\Phi_{V,R,s}(x)$ defaults to $0$ unless it is set to $1$ by the definition above.
That is, we can think of $\Phi_{V,R,s}$ as being defined by a process that starts with the all zeroes function, then sets $\Phi_{V,R,z'}(z)=1$ for every $z\in \Sigma^*$ such that $(z,z')\in R$, and then continues to set $\Phi_{V,R,s}(x)=1$ for every $x$ that can be demonstrated to equal $1$ via the recursive definition above.


^[TO BE CONTINUED]




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
