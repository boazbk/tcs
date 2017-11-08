#  Modeling randomized computation

> # { .objectives }
* Formal definition of probabilistic polynomial time: $\mathbf{BPTIME}(T(n))$ and $\mathbf{BPP}$. \
* Proof that that every function in $\mathbf{BPP}$ can be computed by $poly(n)$-sized NAND programs/circuits. \
* Pseudorandom generators


>_"Any one who considers arithmetical methods of producing random digits is, of course, in a state of sin."_, John von Neumann, 1951.



So far we have descrined randomized algorithms in an informal way, assuming that an operation such as  "pick a string $x\in \{0,1\}^n$" can be done efficiently.
We have neglected to address two questions:

1. How do we actually efficiently obtain random strings in the physical world?

2. What is the  mathematical model for randomized computations, and is it more powerful than deterministic computation?

The first  question is of both practical and theoretical importance,  but for now let's just say that there are various random physical sources.
User's mouse movements, (non solid state) hard drive and network latency, thermal noise, and radioactive decay, have all been used as sources for randomness.
For example, new Intel chips  come with a random number generator [built in](http://spectrum.ieee.org/computing/hardware/behind-intels-new-randomnumber-generator).
One can even build mechanical  coin tossing machines (see [coinfig](){.ref}).^[The output of  processes such as above can be thought of  as a binary string sampled from some distribution $\mu$ that might have significant unpredictablity (or _entropy_) but is  not necessarily the _uniform_ distribution over $\{0,1\}^n$. Indeed, as [this paper](http://statweb.stanford.edu/~susan/papers/headswithJ.pdf) shows, even (real-world) coin tosses do not have exactly the distribution of a uniformly random string.
Therefore, to use the resulting measurements for randomized algorithms, one typically needs to apply a "distillation" or _randomness extraction_ process to the raw measurements to transform them to the uniform distribution.]

![A mechanical coin tosser built for Percy Diaconis by  Harvard technicians Steve Sansone and Rick Haggerty](../figure/coin_tosser.jpg){#coinfig .class width=300px height=300px}

In this lecture we focus on the second point - formally modeling probabilistic computation and studying its power.
The first part is very easy.
We can define the RNAND programming language to include all the operations of   NAND  plus  the following additional operation:

~~~~ { .go .numberLines }
var := RAND
~~~~

where `var` is a variable.
The result of applying this operation is that `var` is assigned a random bit in $\{0,1\}$.
Similarly RNAND++ and RNAND<< will corresponds to NAND++ and NAND<< augmented with the same operation.
(Every time the `RAND` operation is involved it returns a fresh independent random bit.)
We can now define what it means to compute both finite and infinite  functions with randomized algorithm:

> # {.definition title="Randomized circuits and algorithms" #rnandcomp}
Let $F$ be a  function mapping $\{0,1\}^n$ to $\{0,1\}^m$ and $T\in \N$. We say that $F \in \mathbf{BPSIZE}(T)$ if there is an $n$-input $m$-output RNAND program $P$ of at most $T$ lines so that for every $x\in \{0,1\}^n$, $\Pr[ P(x)= F(x)] \geq 2/3$ where this probability is taken over the random choices in the `RAND` operations.
>
Let $F:\{0,1\}^* \rightarrow \{0,1\}$. We say that $F\in \mathbf{BPTIME}_{<<}(T(n))$ if there is an RNAND<< program $P$  such that   for every $x\in \{0,1\}^*$, $P$ always halts with an output $P(x)$ within at most $T(|x|)$ steps and $\Pr[ P(x)=F(x)] \geq 2/3$, where again this probability is taken over the random choices in the `RAND` operations.
We define the condition $F\in \mathbf{BPTIME}_{++}(T(n))$ analogously using NAND++ programs, and use $\mathbf{BPTIME}$ as shorthand for $\mathbf{BPTIME}_{<<}$.^[The prefix BP stands for "bounded probability", and is used for historical reasons.]

We are mostly interested in understanding which functions can be computed by randomized algorithms running in _polynomial_ time, which motivates the following definition:

> # {.definition title="BPP" #bppdef}
The class $\mathbf{BPP}$ is equal to the union over all $c\in\N$ of $\mathbf{BPTIME}(n^c)$.

The same polynomial-overhead simulation of NAND<< programs by  NAND++ programs we saw in [NANDpp-thm](){.ref} extends to _randomized_ programs as well.
Hence the class $\mathbf{BPP}$ is the same regardless of whether it is defined via RNAND++ or RNAND<< programs.


## Amplification


The number $2/3$ might seem arbitrary, but as we've seen in the previous lecture it can be amplified to our liking:

> # {.theorem title="Amplification" #amplificationthm}
Let $P$ be an RNAND<< program,  $F\in \{0,1\}^* \rightarrow \{0,1\}$,
and $T:\N \rightarrow \N$ be a nice time bound such that for every $x\in \{0,1\}^*$, on input $x$ the program $P$ runs in at most $T(|x|)$ steps and moreover $\Pr[ P(x)=F(x) ] \geq \tfrac{1}{2}+\epsilon$ for some $\epsilon>0$.
Then for every $k$, there is a program $P'$  taking at most $O(k\cdot T(n)/\epsilon^2)$ steps such that on input $x\in \{0,1\}^*$, $\Pr[ P'(x)= F(x)] > 1 - 2^{-k}$.

> # {.proofidea data-ref="amplificationthm"}
The proof is the same as we've seen before in the maximum cut and other examples.
We use the Chernoff bound to argue that if we run the program $O(k/\epsilon^2)$ times, each time using fresh and independent random coins, then the probability that the majority of the answers will not be correct will be less than $2^{-k}$.

> # {.proof data-ref="amplificationthm"}
The proof is the same as we've seen in the maximum cut example.
We can run $P$ on input $x$ for $t=10k/\epsilon^2$ times, using fresh randomness each one, to compute outputs $y_0,\ldots,y_{t-1}$. We output the value $y$ that appeared the largest number of times.
Let $X_0$ be the random variable that is equal to $1$ if $y_i = F(x)$ and equal to $0$ otherwise.
Then all the random variables $X_0,\ldots,X_{t-1}$ are i.i.d.  and satisfy $\E [X_i] = \Pr[ X_i = 1] \geq 1/2 + \epsilon$.
Hence by the Chernoff bound ([chernoffthm](){.ref}) the probability that the majority value is not correct (i.e., that  $\sum X_i \leq t/2$) is at most $\exp(-\epsilon^2 t/4) \leq 2^{-m}$.

There is nothing special about NAND<< in [amplificationthm](){.ref}. The same proof can be used to amplify randomized NAND or NAND++ programs as well.



## The power of randomization


A major question is whether randomization can add power to computation.
For _finite_ functions, we can formalize this as asking  whether RNAND programs can be simulated by NAND programs with at most a polynomially larger number of lines.
For _infinite_ functions, we can formalize this as asking whether  RNAND<<  programs can be simulated by NAND<< programs with at most a polynomially larger number of steps.
(Due to their polynomial equivalence, the question remains the same if we replace RNAND<< or NAND<< with RNAND++ or NAND++).

Mathematically, we can also formulate both questions as follows:

1. If there a constant $c\in \N$, $\mathbf{BPSIZE}(T) \subseteq SIZE(T^c)$ for every $t\in \N$?

2. Is there a constant $c\in \N$ such that $\mathbf{BPTIME}(T(n)) \subseteq \mathbf{TIME}(T(n)^c)$ for every nice time bound $T:\N \rightarrow \N$? In particular, is $\mathbf{BPP}=\mathbf{P}$?
3.

### Simulating RNAND programs by NAND programs

It turns out that question 1 is much easier to answer than question 2: RNAND is not really more powerful than NAND.

> # {.theorem title="Simulating RNAND with NAND" #rnandthm}
For every $T\in \N$ and  $F: \{0,1\}^n \rightarrow \{0,1\}^m$, if $F\in RSIZE(T)$ then $F \in SIZE(100nT)$.

> # {.proof data-ref="rnandthm"}
Suppose that $P$ is a $T$-line  RNAND program such that $\Pr[ P(x)=F(x)] \geq 2/3$.
We use [amplificationthm](){.ref} to obtain an $50n T$ line program $P'$ such that
$$
\Pr[ P'(x)=F(x)] \geq 1 - 0.9\cdot 2^{-n} \;. \label{ampeq}
$$
>
Let $R \leq T$ be the number of lines using the `RAND` operations in $P'$.
For every $r\in \{0,1\}^R$, let $P'_r(x)$ be the result of executing $P'$ on $x$ where we use $r_i$ for the result of the $i^{th}$ `RAND` operation for every $i\in \{0,\ldots,R-1\}$.
For every $r\in \{0,1\}^R$ and $x\in \{0,1\}^n$, define a matrix $B$ whose rows are indexed by elements in $\{0,1\}^R$ and whose columns are indexed by elements in $\{0,1\}^n$ such that for every $r\in \{0,1\}^R$ and $x\in \{0,1\}^n$, $B_{r,x}$ equals $1$ if $P'_r(x) \neq F(x)$ and $B_{r,x} = 0$ otherwise.
We can rewrite [ampeq](){.eqref} as follows: for every $x\in \{0,1\}^n$
$$
\sum_{r\in \{0,1\}^R} B_{x,r} \leq 0.1 \cdot 2^{R-n} \;.
$$
>
It follows that the total number of $1$'s in this matrix is at most $0.1 2^R$, which means that there is at least one row $r^*$ in this matrix such that $B_{r^*,x}=0$ for every $x$. (Indeed, otherwise the matrix would have at least $2^R$ $1$'s.)^[In fact, the same reasoning shows that at least a $0.9$ fraction of the rows have this property.]
Let $P^*$ be  the following NAND program which is obtained by taking $P'$ and replacing  the $i^{th}$ line of the form `var := RAND` with the line `var := `$\expr{r^*_i}$.
That is, we replace this with `var := one NAND one` or `var := zero NAND zero` based on whether $r^*_i$ is equal  to $0$ or $1$ respectively, where we add as usual a couple of lines to initialize `zero` and `one` to $0$ and $1$.
By construction, for every $x$, $P^*(x)=P'_r(x)$ and hence, since $B_{r^*,x}=0$ for every  $x\in \{0,1\}^n$, it follows that $P^*(x)= F(x)$ for every $x\in \{0,1\}^n$.

__Note:__ [rnandthm](){.ref} can also be proven using the _Union Bound_. That is, once we show that the probability of an error is smaller than $2^{-n}$, we can take a union bound over all $x$'s and so show that if we choose some random coins $r^*$ and fix them once and for all, then with high probability they will work for _every_ $x\in \{0,1\}^n$.

## Derandomizing uniform computation

The proof of [rnandthm](){.ref} can be summarized as follows:  we can replace a $poly(n)$-time algorithm that tosses coins as it runs, with an algorithm that uses a single set of coin tosses $r^* \in \{0,1\}^{poly(n)}$ which will be good enough for all inputs of size $n$.
Another way to say it is that for the purposes of computing functions, we do not need "online" access to random coins and can generate a set of  coins "offline" ahead of time, before we see the actual input.

But the question of derandomizing _uniform_ computation, or equivalently, NAND++ programs, is a whole different matter.
For a NAND++ program we need to come up with a _single_ deterministic algorithm that will work for _all input lengths_.
That is, unlike the nonuniform NAND case, we cannot choose for every input length $n$ some string $r^* \in \{0,1\}^{poly(n)}$ to use as our random coins.
Can we still do this, or does randomness add an inherent extra power for computation?
This is a fundamentally interesting question  but is also of practical significance.
Ever since people started to use randomized algorithms during the Manhattan project, they have been trying to remove  the need for randomness and replace it with numbers that are selected through some deterministic process.
Throughout the years this approach has often been used successfully, though there have been a number of failures as well.^[One amusing anecdote is a [recent case](https://www.wired.com/2017/02/russians-engineer-brilliant-slot-machine-cheat-casinos-no-fix/) where scammers managed to predict the imperfect "pseudorandom generator" used by slot machines to cheat casinos. Unfortunately we don't know the details of how they did it, since the case was [sealed](https://www.plainsite.org/dockets/2j3mlaig6/missouri-eastern-district-court/usa-v-bliev-et-al/).]

A common approach people used over the years was to  replace the random coins of the algorithm by a "randomish looking" string that they generated through some arithmetic progress.
For example, one can use the digits of $\pi$ for the random tape.
Using these type of methods corresponds to   what von Neumann referred to as a "state of sin".
(Though   this is a sin that he himself frequently committed, as generating true randomness in sufficient quantity was and still is often too expensive.)
The reason that this is considered a "sin" is that such a  procedure will not work in general.
For example, it is easy to modify any probabilistic algorithm $A$ such as the ones we have seen in the previous lecture, to an algorithm $A'$ that is guaranteed to fail if the random tape happens to equal the digits of $\pi$.
This means that the procedure of "replacing the random tape by the digits of $\pi$" does not yield a general way to transform a probabilistic algorithm to a deterministic one that will solve the same problem.
It does not mean that it _always_ fails, but we have no good way to determine when this will work out.

This reasoning is not specific to $\pi$ and holds for every deterministically produced string, whether it obtained by  $\pi$,  $e$, the Fibonacci series, or anything else, as shown in the following result:


> # {.lemma title="Can't replace tape deterministically" #nodet}
There is a linear time probabilistic algorithm $A$ such that for  every $x\in \{0,1\}^*$, $\Pr[A(x)=1]< 1/10$ but
for every $n>10$ and fixed string $r\in \{0,1\}^n$, there is some $x\in \{0,1\}^n$ such that $A(x;r)=1$ where $A(x;r)$ denotes the execution of $A$ on input $x$ and where the randomness is supplied from $r$.

> # {.proof data-ref="nodet"}
The algorithm $A$ is very simple. On input $x$ of length $n$, it tosses $n$ random coins $r_1,\ldots,r_n$ and outputs $1$ if and only if $x_0=r_0$, $x_1=r_1$, $\ldots$, $x_{9}=r_{9}$ (if $n<10$ then $A$ always outputs $0$).
Clearly $A$ runs in $O(n)$ steps and for every $x\in \{0,1\}^*$, $\Pr[ A(x)=1] \leq 2^{-10} < 0.1$.
However, by definition, for every fixed string $r$ of length at least $10$, $A(r;r)=1$.

The proof of [nodet](){.ref} might seem quite silly, but refers to a very serious issue.
Time and again people have learned the hard way that one needs to be very careful about producing random bits using deterministic means.
As we will see when we discuss cryptography, many spectacular security failures and break-ins were the result of using "insufficiently random" coins.

## Pseudorandom generators

So, we can't use any _single_ string to "derandomize" a probabilistic algorithm.
It turns out however, that we can use a _collection_ of strings to do so.
Another way to think about it is that we start by focusing on _reducing_ (as opposed to _eliminating_) the amount of randomness needed. (Though we will see that if we reduce the randomness sufficiently, we can eventually get rid of it altogether.)

We make the following definition:

> # {.definition title="Pseudorandom generator" #prg}
A function $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ is a _$(T,\epsilon)$-pseudorandom generator_ if for every
NAND program $P$ with $m$ inputs and one output of at most $T$ lines,
\begin{equation}
\left| \Pr_{s\sim \{0,1\}^\ell}[P(G(s))=1] - \Pr_{r \sim \{0,1\}^m}[P(r)=1] \right| < \epsilon \label{eq:prg}
\end{equation}

![A pseudorandom generator $G$ maps a short string $s\in \{0,1\}^\ell$ into a long string $r\in \{0,1\}^m$ such that an small program $P$ cannot distinguish between the case that it is provided a random input $r \sim \{0,1\}^m$ and the case that it is provided a "pseudorandom" input of the form $r=G(s)$ where $s \sim \{0,1\}^\ell$. The short string $s$ is sometimes called the _seed_ of the pseudorandom generator, as it is a small  object that can be thought as yielding a large "tree of randomness".](../figure/prg_experiment.png){#figureid .class width=300px height=300px}

This is a definition that's worth reading more than once, and spending some time to digest it.
First of all note that it takes several parameters:

* $T$ is the limit on the number of lines of the program $P$  that the generator needs to "fool". The larger $T$ is, the stronger the generator.

* $\epsilon$ is how close is the output of the pseudorandom generator to the true uniform distribution over $\{0,1\}^m$. The smaller $\epsilon$ is, the stronger the generator.

* $\ell$ is the input length and $m$ is the output length. If $\ell \geq m$ then it is trivial to come up with such a generator: on input $s\in \{0,1\}^\ell$, we can output $s_0,\ldots,s_{m-1}$. In this case $\Pr_{s\sim \{0,1\}^\ell}[ P(G(s))=1]$ will simply equal $\Pr_{r\in \{0,1\}^m}[ P(r)=1]$, no matter how many lines $P$ has. So, the smaller $\ell$ is and the larger $m$ is, the stronger the generator, and to get anything non-trivial, we need $m>\ell$.

We can think of a pseudorandom generator as a "randomness amplifier". It takes an input $s$ of $\ell$ bits, which we can assume per [{eq:prg}](){.eqref} that are _truly random_, and expands this into an output $r$ of $m>\ell$ _pseudorandom_ bits.
If $\epsilon$ is small enough (even $\epsilon=0.1$ might be enough) then the pseudorandom bits will "look random" to any NAND program that is not too big.
Still, there are two questions we haven't answered:

* _What reason do we have to believe that pseudorandom generators with non-trivial parameters exist?_

* _Even if they do exist, why would such generators be useful to derandomize randomized algorithms?_ After all, [prg](){.ref} does not involve RNAND++ programs but deterministic NAND programs with no randomness and no loops.

We will now (partially) answer both questions.

### Existence of pseudorandom generators

For the first question, let us come clean and confess we do not know how to _prove_ that interesting pseudorandom generators exist.
By _interesting_ we mean pseudorandom generators that satisfy that $\epsilon$ is some small constant (say $\epsilon<1/3$), $m>\ell$, and the function $G$ itself can be computed in $poly(m)$ time.
If we drop the last  condition, then as shown in [prgexist](){.ref}, there are pseudorandom generators where $m$ is _exponentially larger_  than $\ell$.


> # {.lemma title="Existence of inefficient pseudorandom generators" #prgexist}
There is some absolute constant $C$ such that for every $\epsilon,T$, if $\ell > C (\log T + \log (1/\epsilon))$ and $m \leq T$,  then there is an $(T,\epsilon)$ pseudorandom generator $G: \{0,1\}^\ell \rightarrow \{0,1\}^m$.

The proof uses an extremely useful technique known  as the "probabilistic method" which is not too hard technically but can be confusing at first.^[There is a whole (highly recommended) [book](https://www.amazon.com/Probabilistic-Method-Discrete-Mathematics-Optimization/dp/1119061954/ref=dp_ob_title_bk) by Alon and Spencer devoted to this method.]
The idea is to give a "non constructive" proof of existence of the pseudorandom generator $G$ by showing that if $G$ was chosen at random, then the probability that it would be a valid $(T,\epsilon)$ pseudorandom generator is positive.
In  particular this means that there _exists_ a single $G$ that is a valid $(T,\epsilon)$ pseudorandom generator.
The probabilistic method is doubly-confusing in the current setting, since eventually $G$ is a _deterministic_ function $G$  (as its whole point is to reduce the need for randomness).
The probabilistic method is just a _proof technique_ to demonstrate the existence of such a function.
The above discussion might be rather abstract at this point, but would become clearer after seeing the proof.

^[TODO: if we end up discussing the probabilistic method before this proof, then move this discussion to that point.]




> # {.proof data-ref="prgexist"}
Let $\epsilon,T,\ell,m$ be as in the lemma's statement. We need to show that there exists a function $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ that "fools" every $T$ line program $P$ in the sense of [eq:prg](){.eqref}.
We will show that this follows from the following claim:
>
__CLAIM:__ For every fixed NAND program $P$, if we pick $G$ _at random_ then the probability that [eq:prg](){.eqref} is violated is at most $2^{-T^2}$.
>
Before proving the claim, let us see why it implies the lemma.
Suppose we give some arbitrary ordering $P_1,\ldots,P_M$ for the NAND programs $P$ of at most $T$ lines where $M$ is the number of such programs, which we have seen in lecture 4 to be at most $2^{O(T \log T)}< 2^{T^2}$ (for lare enough $T$).^[Recall that we showed this by arguing that we can translate all variables in a $\leq T$-line program to have the form `x_`$\expr{j}$, `y_`$\expr{j}$ or `work_`$\expr{j}$ (where $j$ is a number between $0$ and $3T$) without changing the function that the program computes and hence without affecting the event [eq:prg](){.eqref}. For programs in this form, every line can be described by at most $4\log T$ ASCII characters which means that the program can be described by at most $10 T \log T$ characters or $12 T \log T$ bits, which means there are at most $2^{12 T \log T}$ of them.]
Thus if we let $E_i$ be the event [eq:prg](){.eqref} is violated for program $P_i$ with respect to the random $G$, then by setting $C$ large enough we can ensure that $\Pr[ E_i ] < 1/(10M)$ which means that by the union bound with probability $0.9$, [eq:prg](){.eqref} holds for _every_ program $P$ of at most $T$ lines.
This means that $G$ is a $(T,\epsilon)$ pseudorandom generators
>
Hence  conclude the proof of [prgexist](){.ref}, it suffices to prove the claim.
Choosing a random $G: \{0,1\}^\ell \rightarrow \{0,1\}^m$ amounts to choosing $L=2^\ell$ random strings $y_0,\ldots,y_{L-1} \in \{0,1\}^m$ and letting $G(x)=y_x$ (identifying $\{0,1\}^\ell$ and $[L]$ via the binary representation).
Hence the claim amounts to showing that for every fixed function $P:\{0,1\}^m \rightarrow \{0,1\}$,
if $L >  2^{C (\log T + \log \epsilon)}$ (which by setting $C>4$, we can ensure is larger than $10 T^2/\epsilon^2$) then the probability that
\begin{equation}
\left| \tfrac{1}{L}\sum_{i=0}^{L-1} P(y_s)  -  \Pr_{s \sim \{0,1\}^m}[P(s)=1] \right| > \epsilon \label{eq:prgchernoff}
\end{equation}
is at most $2^{-T^2}$.
[{eq:prgchernoff}](){.eqref} follows directly from the Chernoff bound. If we let for every $i\in  [L]$  the random variable $X_i$ denote $P(y_i)$, then since $y_0,\ldots,y_{L-1}$ is chosen independently at random, these are independently and identically distributed random variables with mean $\Pr_{s\sim \{0,1\}^m}[ P(s)=1]$ and hence the probability that they deviate from their expectation by $\epsilon$ is at most $2\cdot 2^{-\epsilon^2 L/2}$.

The fact that there _exists_ a pseudorandom generator does not mean that there is one that can be efficiently computed.
However, it turns out that we can turn complexity "on its head" and used the assumed _non existence_ of fast algorithms for problems such as 3SAT to obtain pseudorandom generators that can then be used to transform randomized algorithms into deterministic ones.
This is known as the _Hardness vs Randomness_ paradigm.
We will discuss this in the next lecture, but this set of results led researchers to believe the following conjecture:

>__Optimal PRG conjecture:__ There are some absolute constants  $\delta>0 , c\in \N$  such that for every nice time-complexity  function   $m:\N \rightarrow \N$, satisfying $m(n)  \leq 2^{\delta n}$, there is a function $G:\{0,1\}^* \rightarrow \{0,1\}^*$, in $\overline{TIME}(m(n)^c)$ such that for every $\ell \in \N$, the restriction  of $G$ to length $\ell$ inputs is a function $G_\ell: \{0,1\}^\ell \rightarrow \{0,1\}^{m(\ell)}$ that is a $(2^{\delta \ell},2^{-\delta \ell})$ pseudorandom generator.

TO BE CONTINUED (discussion of what this means)

### Usefulness of pseudorandom generators

TO BE CONTINUED (show that optimal pseudorandom generators imply that $\overline{\mathbb{BPP}}=\overline{\mathbb{P}}$)


## Lecture summary


## Exercises




## Bibliographical notes


## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)



## Acknowledgements
