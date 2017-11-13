#  Modeling randomized computation

> # { .objectives }
* Formal definition of probabilistic polynomial time: $\mathbf{BPTIME}(T(n))$ and $\mathbf{BPP}$. \
* Proof that that every function in $\mathbf{BPP}$ can be computed by $poly(n)$-sized NAND programs/circuits. \
* Pseudorandom generators


>_"Any one who considers arithmetical methods of producing random digits is, of course, in a state of sin."_, John von Neumann, 1951.



So far we have described randomized algorithms in an informal way, assuming that an operation such as  "pick a string $x\in \{0,1\}^n$" can be done efficiently.
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
Modeling randomized computation is actually quite easy.
We can add the following operations to our NAND, NAND++ and NAND<< programming languages:

~~~~ { .go .numberLines }
var := RAND
~~~~

where `var` is a variable.
The result of applying this operation is that `var` is assigned a random bit in $\{0,1\}$.
(Every time the `RAND` operation is invoked it returns a fresh independent random bit.)
We call the resulting languages RNAND, RNAND++, and RNAND<< respectively.

We can use this to define the notion of a function being computed by a randomized $T(n)$ time algorithm for every nice time bound $T:\N \rightarrow \N$, as well as the notion of a finite function being computed by a size $S$ randomized NAND program (or, equivalently, a randomized circuit with $S$ gates that correspond to either NAND or coin-tossing).
However, for simplicity we we will not define randomized computation in full generality, but simply focus on the class of functions that are computable by randomized algorithms _running in polynomial time_, which by historical convention is known as $\mathbf{BPP}$:


> # {.definition title="BPP" #BPPdef}
Let $F:\in \{0,1\}^*\rightarrow \{0,1\}$.
We say that $F\in \mathbf{BPP}$ if there exist  constants $a,b\in \N$ and an RNAND++ program $P$ such that for every $x\in \{0,1\}^*$, on input $x$, the program $P$ halts within at most $a|x|^b$ steps and
$$
\Pr[ P(x)= F(x)] \geq \tfrac{2}{3}
$$
where this  probability is taken over the result of the RAND operations of $P$.^[$\mathbf{BPP}$ stands for "bounded probability polynomial time", and is used for historical reasons.]


The same polynomial-overhead simulation of NAND<< programs by  NAND++ programs we saw in [NANDpp-thm](){.ref} extends to _randomized_ programs as well.
Hence the class $\mathbf{BPP}$ is the same regardless of whether it is defined via RNAND++ or RNAND<< programs.


### Random coins as an "extra input"

While we presented randomized computation as adding an extra "coin tossing" operation to our programs, we can also model this as being given an additional extra input.
That is, we can think of a randomized algorithm  $A$ as a _deterministic_ algorithm $A'$ that takes _two inputs_ $x$ and $r$ where the second input $r$ is chosen at random from $\{0,1\}^m$ for some $m\in \N$.
The equivalence to the [BPPdef](){.ref} is shown in the following theorem:

> # {.theorem title="Alternative characterization of $\mathbf{BPP}$" #randextrainput}
Let $F:\{0,1\}^*  \rightarrow \{0,1\}$. Then $F\in \mathbf{BPP}$ if and only if there exists $a,b\in \N$ and $G:\{0,1\}^* \rightarrow \{0,1\}$ such that $G$ is in $\mathbf{P}$ and for every $x\in \{0,1\}^*$,
$$
\Pr_{r\sim \{0,1\}^{a|x|^b}} [ G(xr)=F(x)] \geq \tfrac{2}{3}  \label{eqBPPauxiliary}\;.
$$


> # {.proofidea data-ref="randextrainput"}
The idea behind the proof is that we can simply replace sampling a random coin with reading a bit from the extra "random input" $r$ and vice versa. Of course to prove this rigorously we  need to work through some formal notation, and so this might be one of those proofs that is easier for you to work out on your own than to read.

> # {.proof data-ref="randextrainput"}
We start by showing the "only if" direction.
Let $F\in \mathbf{BPP}$ and let $P$ be an RNAND++ program that computes $F$ as per [BPPdef](){.ref}, and let $a,b\in \N$ be such that on every input of length $n$, the program $P$ halts within at most $an^b$ steps.
We will construct a NAND++ polynomial-time program $P'$ that computes a function $G$ satisfying the conditions of [eqBPPauxiliary](){.eqref}.
As usual, we will allow ourselves some "syntactic sugar" in constructing this program, as it can always be eliminated with polynomial overhead as in the proof of [NANDequiv-thm](){.ref}.
The program $P'$ will first copy the bits in  positions $n,n+1,n+2,\ldots,n+an^b-1$ of its input into the variables `r_0`, `r_1`, $\ldots$, `r_`$\expr{an^b-1}$.
We will also assume we have access to an extra index variable `j` which we can increase and decrease (which of course can be simulated via syntactic sugar).
The program $P'$ will run the same operations of $P$ except that it will replace a line of the form
`foo := RAND` with the two lines
`foo := r_j` amd `j   := j + 1`
>
One can easily verify that __(1)__ $P'$ runs in polynomial time and __(2)__  if the last $an^b$ bits of the input of $P'$ are chosen at random then its execution when its first $n$ inputs are $x$ is identical to an execution of $P(x)$.
By __(2)__ we mean that for every $r\in \{0,1\}^{an^b}$ corresponding to the result of the `RAND` operations made by $P$ on its execution on $x$, the output of $P$ on input $x$ and with random choices $r$ is equal to $P'(xr)$.
Hence the distribution of the output  $P(x)$ of the randomized program $P$ on input $x$ is identical to the distribution of $P'(x;r)$  when $r \sim \{0,1\}^{an^b}$.
>
For the other direction, given a function $G\in \mathbf{P}$ satisfying the condition [eqBPPauxiliary](){.eqref} and a NAND++ program $P'$ that computes $G$ in polynomial time, we will construct an RNAND++ program $P$ that computes $F$ in polynomial time.
The idea behind the construction of $P$ is simple: on input a string $x\in \{0,1\}^n$, we will first run for $an^b$ steps and use the `RNAND` operation to create variables `r_0`, `r_1`, $\ldots$,`r_`$\expr{an^b-1}$ each containing the result of a random coin toss.
We will then execute $P'$ on the input $x$ and `r_0`,$\ldots$,`r_`$\expr{an^b-1}$ (i.e., replacing every reference to the variable `x_`$\expr{n+k}$ with the variable `r_`$\expr{k}$).
Once again, it is clear that if $P'$ runs in polynomial time then so will $P$, and for every input $x$ and $r\in \{0,1\}^{an^b}$, the output of $P$ on input $x$ and where the coin tosses outcome is $r$ is equal to $P'(xr)$.

The characterization of $\mathbf{BPP}$ [randextrainput](){.ref} is reminiscent of the characterization of $\mathbf{NP}$  in [NP-def](){.ref}, with the randomness in the case of $\mathbf{BPP}$ playing the role of the solution in the case of $\mathbf{NP}$ but there are important differences between the two:

* The definition of $\mathbf{NP}$ is "one sided": $F(x)=1$ if _there exists_ a solution $w$ such that $G(xw)=1$ and $F(x)=0$ if _for every_ string $w$ of the appropriate length, $G(xw)=0$. In contrast, the characterization of $\mathbf{BPP}$ is symmetric with respect to the cases $F(x)=0$ and $F(x)=1$.

* For this reason the relation between $\mathbf{NP}$ and $\mathbf{BPP}$ is not immediately clear, and indeed is not known whether $\mathbf{BPP} \subseteq \mathbf{NP}$, $\mathbf{NP} \subseteq \mathbf{BPP}$, or these two classes are incomprable. It is however known (with a non-trivial proof) that if $\mathbf{P}=\mathbf{NP}$ then  $\mathbf{BPP}=\mathbf{P}$ (see [BPPvsNP](){.ref}).


* Most importantly,  the definition of $\mathbf{NP}$ is "ineffective", since it does not yield a way of actually finding whether there exists a solution among the exponentially many possiblities. In contrast, the definition of $\mathbf{BPP}$ gives us a way to compute the function in practice by simply choosing the second input at random.

__"Random tapes"__ [randextrainput](){.ref} motivates sometimes considering the randomness of an RNAND++ (or RNAND<<) program  as an extra input, and so if $A$ is a randomized algorithm that on inputs of length $n$ makes at most $p(n)$ coin tosses, we will sometimes use the notation $A(x;r)$ (where $x\in \{0,1\}^n$ and $r\in \{0,1\}^{p(n)}$) to refer to the result of executing $x$ when the coin tosses of $A$ correspond to the coordinates of $r$.
This second or "auxiliary" input is sometimes referred to as a "random tape", with the terminology coming from the model of randomized Turing machines.

### Amplification


The number $2/3$ might seem arbitrary, but as we've seen in the previous lecture it can be amplified to our liking:

> # {.theorem title="Amplification" #amplificationthm}
Let $P$ be an RNAND<< program,  $F\in \{0,1\}^* \rightarrow \{0,1\}$,
and $T:\N \rightarrow \N$ be a nice time bound such that for every $x\in \{0,1\}^*$, on input $x$ the program $P$ runs in at most $T(|x|)$ steps and moreover $\Pr[ P(x)=F(x) ] \geq \tfrac{1}{2}+\epsilon$ for some $\epsilon>0$.
Then for every $k$, there is a program $P'$  taking at most $O(k\cdot T(n)/\epsilon^2)$ steps such that on input $x\in \{0,1\}^*$, $\Pr[ P'(x)= F(x)] > 1 - 2^{-k}$.

> # {.proofidea data-ref="amplificationthm"}
The proof is the same as we've seen before in the maximum cut and other examples.
We use the Chernoff bound to argue that if we run the program $O(k/\epsilon^2)$ times, each time using fresh and independent random coins, then the probability that the majority of the answers will not be correct will be less than $2^{-k}$.

> # {.proof data-ref="amplificationthm"}
We can run $P$ on input $x$ for $t=10k/\epsilon^2$ times, using fresh randomness each one, to compute outputs $y_0,\ldots,y_{t-1}$. We output the value $y$ that appeared the largest number of times.
Let $X_i$ be the random variable that is equal to $1$ if $y_i = F(x)$ and equal to $0$ otherwise.
Then all the random variables $X_0,\ldots,X_{t-1}$ are i.i.d.  and satisfy $\E [X_i] = \Pr[ X_i = 1] \geq 1/2 + \epsilon$.
Hence by the Chernoff bound ([chernoffthm](){.ref}) the probability that the majority value is not correct (i.e., that  $\sum X_i \leq t/2$) is at most $2e^{-2\epsilon^2 t}  < 2^{-k}$ for our choice of $t$.

There is nothing special about NAND<< in [amplificationthm](){.ref}. The same proof can be used to amplify randomized NAND or NAND++ programs as well.

## $\mathbf{BPP}$ and $\mathbf{NP}$ completeness

Since "noisy processes" abound in nature, randomized algorithms can be realized physically, and so it is reasonable to propose $\mathbf{BPP}$ rather than $\mathbf{P}$ as our mathematical model for "feasible" or "tractable" computation.
One might wonder if this makes all the previous lectures irrelevant, and in particular does the theory of $\mathbf{NP}$ completeness still apply to probabilistic algorithms.
Fortunately, the answer is _Yes_:

> # {.theorem title="NP hardness and  BPP" #NPCandBPP}
Suppose that $F$ is $\mathbf{NP}$-hard and $F\in \mathbf{BPP}$ then $\mathbf{NP} \subseteq \mathbf{BPP}$.

Before seeing the proof note that [NPCandBPP](){.ref} in particular implies that if there was a randomized polynomial time algorithm for any $\mathbf{NP}$-complete problem such as $3SAT$, $ISET$ etc.. then there will be such an algorithm for _every_ problem in $\mathbf{NP}$.
Thus, regardless of whether our model of computation is deterministic or randomized algorithms, $\mathbf{NP}$ complete problems retain their status as the "hardest problems in $\mathbf{NP}$".

> # {.proofidea data-ref="NPCandBPP"}
The idea is to simply run the reduction as usual, and plug it into the randomized algorithm instead of a deterministic one. It would be an excellent exercise, and a way to reinforce the definitions of $\mathbf{NP}$-hardness and randomized algorithms, for you to work out the proof for yourself. However for the sake of completeness, we include this proof below.

> # {.proof data-ref="NPCandBPP"}
Suppose that $F$ is $\mathbf{NP}$-hard and $F\in \mathbf{BPP}$.
We will now show that this implies that $\mathbf{NP} \subseteq \mathbf{BPP}$.
Let $G \in \mathbf{NP}$.
By the definition of $\mathbf{NP}$-hardness, it follows that $G \leq_p F$, or that in other words there exists a polynomial-time computable function $R:\{0,1\}^* \rightarrow \{0,1\}^*$ such that $G(x)=F(R(x))$ for every $x\in \{0,1\}^*$.
Now if $F$ is in $\mathbf{BPP}$ then there is a polynomial-time RNAND++ program  $P$ such that
$$
\Pr[ P(y)= F(y) ] \geq 2/3 \label{FinBPPeq}
$$  
for _every_ $y\in \{0,1\}^*$ (where the probability is taken over the random coin tosses of $P$).
Hence we can get a polynomial-time  RNAND++ program $P'$ to compute $G$ by setting $P'(x)=P(R(x))$.
By [FinBPPeq](){.eqref} $\Pr[ P'(x) = F(R(x))] \geq 2/3$ and since $F(R(x))=G(x)$ this implies that $\Pr[ P'(x) = G(x)] \geq 2/3$, which proves that $G \in \mathbf{BPP}$.

Most of the results we've seen about the $\mathbf{NP}$ hardness, including the search to decision reduction of [search-dec-thm](){.ref}, the decision to optimization reduction of [optimizationnp](){.ref}, and the quantifier elimination result of [PH-collapse-thm](){.ref}, all carry over in the same way if we replace $\mathbf{P}$ with $\mathbf{BPP}$ as our model of efficient computation.
Thus if $\mathbf{NP} \subseteq \mathbf{BPP}$ then we'd get essentially all of the strange and wonderful  consequences of $\mathbf{P}=\mathbf{NP}$.
Unsurprisingly, we cannot rule out this possiblity.
In fact, unlike $\mathbf{P}=\mathbf{EXP}$, which is ruled out by the time hierarchy theorem, we don't even know how to rule out the possiblity that $\mathbf{BPP}=\mathbf{EXP}$!
Thus a priori it's possible (though seems highly unlikely) that randomness is a magical tool that allows to speed up arbitrary exponential time computation.^[At the time of this writing, the largest "natural" complexity class which we can't rule out being contained in $\mathbf{BPP}$ is the class $\mathbf{NEXP}$, which we did not define in this course, but  corresponds to non deterministic exponential time. See [this paper](https://people.csail.mit.edu/rrw/nexp-v-bpp.pdf) for a discussion of this question.]
Nevertheless, as we discuss below, it is believed that randomization's power is much weaker and $\mathbf{BPP}$ lies in much more "pedestrian" territory.


## The power of randomization


A major question is whether randomization can add power to computation.
Mathematically, we can phrase this as the following question: does $\mathbf{BPP}=\mathbf{P}$?
Given what we've seen so far about the relations of other complexity classes such as $\mathbf{P}$ and $\mathbf{NP}$, or $\mathbf{NP}$ and $\mathbf{EXP}$, one might guess that:

1. We do not know the answer to this question.

2. But we suspect that $\mathbf{BPP}$ is different than $\mathbf{P}$.

One would be correct about the former, but wrong about the latter.
As we will see, we do in fact have  reasons to believe that $\mathbf{BPP}=\mathbf{P}$.
This can be thought of as supporting the _extended Church Turing hypothesis_ that deterministic polynomial-time NAND++ program (or, equivalently, polynomial-time Turing machines)  capture what can be feasibly computed in the physical world.

We now survey some of the relations that are known between $\mathbf{BPP}$ and other complexity classes we have encountered.

### Solving $\mathbf{BPP}$ in exponential time

It is not hard to see that if $F$ is in $\mathbf{BPP}$ then it can be computed in _exponential_ time.

> # {.theorem title="Simulating randomized algorithm in exponential time" #BPPEXP}
$\mathbf{BPP} \subseteq \mathbf{EXP}$

> # { .pause }
The proof of [BPPEXP](){.ref} readily follows by enumerating over all the (exponentially many) choices for the random coins.
We omit the formal proof, as doing it by yourself is an excellent way to get comfort with [BPPdef](){.ref}




### Simulating randomized algorithms by circuits or straightline programs.

We have seen in [non-uniform-thm](){.ref} that if  $F$ is in $\mathbf{P}$, then there is a polynomial $p:\N \rightarrow \N$ such that for every $n$, the restriction $F_n$ of $F$ to inputs $\{0,1\}^n$ is in $SIZE(p(n))$.
A priori it is not at all clear that the same holds for a function in $\mathbf{BPP}$, but this does turn out to be the case.



> # {.theorem title="Randomness does not help in non uniformity" #rnandthm}
For every $F\in \mathbf{BPP}$, there exist some $a,b\in \N$ such that for every $n>0$, $F_n \in SIZE(an^b)$ where $F_n$ is the restriction
of $F$ to inputs in $\{0,1\}^n$.


> # {.proofidea data-ref="rnandthm"}
The idea behind the proof is that we can first amplify by repetition the probability of success from $2/3$ to $1-0.1 \cdot 2^{-n}$.
This will allow us to show that there exists a single fixed choice of "favorable coins" that would cause the algorithm to output the right answer on _all_ of the possible $2^n$ inputs.
We can then use the standard "unravelling the loop" technique to transform an RNAND++ program to an RNAND program, and  "hardwire" the favorable choice of random coins to  transform the RNAND program into a plain-old deterministic NAND program.

> # {.proof data-ref="rnandthm"}
Suppose that $F\in \mathbf{BPP}$ and let $P$ be a polynomial-time RNAND++ program that computes $F$ as per [BPPdef](){.ref}.
Using [amplificationthm](){.ref} we can  _amplify_ the success probability of $P$ to obtain an RNAND++ program $P'$ that is at most a factor of $O(n)$ slower (and hence still polynomial time)
such that for every $x\in \{0,1\}^n$
$$
\Pr_{r \sim \{0,1\}^m}[ P'(x;r)=F(x)] \geq 1 - 0.1\cdot 2^{-n} \;, \label{ampeq}
$$
where $m$ is the number of coin tosses that $P'$ uses on inputs of length $n$, and we use  the notation $P'(x;r)$ to denote the execution of $P'$ on input $x$ and when the result of the coin tosses corresponds to the string $r$.
>
For every $x\in \{0,1\}^n$, define the "bad" event $B_x$ to hold if $P'(x) \neq F(x)$, where the sample space for this event consists of the coins of $P'$.
Then by [ampeq](){.eqref}, $\Pr[B_x] \leq  0.1\cdot 2^{-n}$ for every $x \in \{0,1\}^n$.
Since there are $2^n$ many such $x$'s, by the union bound we see that the probability that the _union_ of the events $\{ B_x \}_{x\in \{0,1\}^n}$ is at most $0.1$.
This means that if we choose $r \sim \{0,1\}^m$, then with probability at least $0.9$ it will be the case that for _every_ $x\in \{0,1\}^n$, $F(x)=P'(x;r)$.
(Indeed, otherwise the event $B_x$ would hold for some $x$.)
In particular, because of the mere fact that the the probability of $\cup_{x \in \{0,1\}^n} B_x$ is smaller than $1$, this means that _there exists_ a particular $r^* \in \{0,1\}^m$ such that  
$$P'(x;r^*)=F(x) \label{hardwirecorrecteq}
$$
for every $x\in \{0,1\}^n$.
Now let us use the standard "unravelling the loop" the technique and transform $P'$ into a NAND program $Q$ of polynomial in $n$ size, such that $Q(xr)=P'(x;r)$ for every $x\in \{0,1\}^n$ abd $r \in \{0,1\}^m$.
Then by "hardwiring" the values $r^*_0,\ldots,r^*_{m-1}$ in place of the last $m$ inputs of $Q$, we obtain a new NAND program $Q_{r^*}$ that satisfies by [hardwirecorrecteq](){.eqref} that $Q_{r^*}(x)=F(x)$ for every $x\in \{0,1\}^n$.
This demonstrates that $F_n$ has a polynomial sized NAND program, hence completing the proof of [rnandthm](){.ref}

> # {.remark title="Randomness and non uniformity" #nonuniform}
The proof of [rnandthm](){.ref} actually yields more than its statement. We can use the same "unrolling the loop" arguments we've used before to show that the restriction to $\{0,1\}^n$ of every function in $\mathbf{BPP}$ is also computable by a polynomial-size RNAND program (i.e., NAND program with the `RAND` operation), but like in the $\mathbf{P}$ vs $SIZE(poly(n))$ case, there are functions outside $\mathbf{BPP}$ whose restrictions can be  computed  by polynomial-size  RNAND programs.
Nevertheless the proof of [rnandthm](){.ref} shows that even such functions can be computed by polynomial sized NAND programs without using the `rand` operations.
This can be phrased as saying   that $BPSIZE(T(n)) \subseteq SIZE(O(n T(n)))$ (where $BPSIZE$ is defined in the natural way using RNAND progams).
[rnandthm](){.ref} can also be phrased as saying  that $\mathbf{BPP} \subseteq \mathbf{P_{/poly}}$, and the stronger result can be phrased as $\mathbf{BPP_{/poly}} = \mathbf{P_{/poly}}$.





## Derandomization

The proof of [rnandthm](){.ref} can be summarized as follows:  we can replace a $poly(n)$-time algorithm that tosses coins as it runs, with an algorithm that uses a single set of coin tosses $r^* \in \{0,1\}^{poly(n)}$ which will be good enough for all inputs of size $n$.
Another way to say it is that for the purposes of computing functions, we do not need "online" access to random coins and can generate a set of  coins "offline" ahead of time, before we see the actual input.

But this does not really help us with answering the question of whether $\mathbf{BPP}$ equals $\mathbf{P}$, since we still need to find a way to generate these "offline" coins in the first place.
To derandomize an RNAND++ program we will need to come up with a _single_ deterministic algorithm that will work for _all input lengths_.
That is, unlike in the case of RNAND programs, we cannot choose for every input length $n$ some string $r^* \in \{0,1\}^{poly(n)}$ to use as our random coins.



Can we derandomize randomized algorithms, or does randomness add an inherent extra power for computation?
This is a fundamentally interesting question  but is also of practical significance.
Ever since people started to use randomized algorithms during the Manhattan project, they have been trying to remove  the need for randomness and replace it with numbers that are selected through some deterministic process.
Throughout the years this approach has often been used successfully, though there have been a number of failures as well.^[One amusing anecdote is a [recent case](https://www.wired.com/2017/02/russians-engineer-brilliant-slot-machine-cheat-casinos-no-fix/) where scammers managed to predict the imperfect "pseudorandom generator" used by slot machines to cheat casinos. Unfortunately we don't know the details of how they did it, since the case was [sealed](https://www.plainsite.org/dockets/2j3mlaig6/missouri-eastern-district-court/usa-v-bliev-et-al/).]

A common approach people used over the years was to  replace the random coins of the algorithm by a "randomish looking" string that they generated through some arithmetic progress.
For example, one can use the digits of $\pi$ for the random tape.
Using these type of methods corresponds to   what von Neumann referred to as a "state of sin".
(Though   this is a sin that he himself frequently committed, as generating true randomness in sufficient quantity was and still is often too expensive.)
The reason that this is considered a "sin" is that such a  procedure will not work in general.
For example, it is easy to  modify any probabilistic algorithm $A$ such as the ones we have seen in the previous lecture, to an algorithm $A'$ that is _guaranteed to fail_ if the random tape happens to equal the digits of $\pi$.
This means that the procedure  "replace the random tape by the digits of $\pi$" does not yield a _general_ way to transform a probabilistic algorithm to a deterministic one that will solve the same problem.
Of course,  this procedure does not _always_ fail, but we have no good way to determine when it fails and when it succeeds.
This reasoning is not specific to $\pi$ and holds for every deterministically produced string, whether it obtained by  $\pi$,  $e$, the Fibonacci series, or anything else.

<!---


> # {.lemma title="Can't replace tape deterministically" #nodet}
Let $G:\{0,1\}^* \rightarrow \{0,1\}^m$
There is a linear time probabilistic algorithm $A$ such that for  every $x\in \{0,1\}^*$, $\Pr[A(x)=1]< 1/10$ but
for every $n>10$ and fixed string $r\in \{0,1\}^n$, there is some $x\in \{0,1\}^n$ such that $A(x;r)=1$ where $A(x;r)$ denotes the execution of $A$ on input $x$ and where the randomness is supplied from $r$.

> # {.proof data-ref="nodet"}
The algorithm $A$ is very simple. On input $x$ of length $n$, it tosses $n$ random coins $r_1,\ldots,r_n$ and outputs $1$ if and only if $x_0=r_0$, $x_1=r_1$, $\ldots$, $x_{9}=r_{9}$ (if $n<10$ then $A$ always outputs $0$).
Clearly $A$ runs in $O(n)$ steps and for every $x\in \{0,1\}^*$, $\Pr[ A(x)=1] \leq 2^{-10} < 0.1$.
However, by definition, for every fixed string $r$ of length at least $10$, $A(r;r)=1$.

The proof of [nodet](){.ref} might seem quite silly, but refers to a very serious issue.

--->

An algorithm that checks if its random tape is equal to $\pi$ and then fails seems to be quite silly, but this is but the "tip of the iceberg" for a very serious issue.
Time and again people have learned the hard way that one needs to be very careful about producing random bits using deterministic means.
As we will see when we discuss cryptography, many spectacular security failures and break-ins were the result of using "insufficiently random" coins.

### Pseudorandom generators

So, we can't use any _single_ string to "derandomize" a probabilistic algorithm.
It turns out however, that we can use a _collection_ of strings to do so.
Another way to think about it is that rather than trying to _eliminate_ the need for randomness,  we start by focusing on _reducing_  the amount of randomness needed. (Though we will see that if we reduce the randomness sufficiently, we can eventually get rid of it altogether.)

We make the following definition:

> # {.definition title="Pseudorandom generator" #prgdef}
A function $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ is a _$(T,\epsilon)$-pseudorandom generator_ if for every
NAND program $P$ with $m$ inputs and one output of at most $T$ lines,
$$
\left| \Pr_{s\sim \{0,1\}^\ell}[P(G(s))=1] - \Pr_{r \sim \{0,1\}^m}[P(r)=1] \right| < \epsilon \label{eq:prg}
$$

![A pseudorandom generator $G$ maps a short string $s\in \{0,1\}^\ell$ into a long string $r\in \{0,1\}^m$ such that an small program $P$ cannot distinguish between the case that it is provided a random input $r \sim \{0,1\}^m$ and the case that it is provided a "pseudorandom" input of the form $r=G(s)$ where $s \sim \{0,1\}^\ell$. The short string $s$ is sometimes called the _seed_ of the pseudorandom generator, as it is a small  object that can be thought as yielding a large "tree of randomness".](../figure/prg_experiment.png){#figureid .class width=300px height=300px}

> # { .pause }
This is a definition that's worth reading more than once, and spending some time to digest it.
Note that it takes several parameters:
>
* $T$ is the limit on the number of lines of the program $P$  that the generator needs to "fool". The larger $T$ is, the stronger the generator.
>
* $\epsilon$ is how close is the output of the pseudorandom generator to the true uniform distribution over $\{0,1\}^m$. The smaller $\epsilon$ is, the stronger the generator.
>
* $\ell$ is the input length and $m$ is the output length. If $\ell \geq m$ then it is trivial to come up with such a generator: on input $s\in \{0,1\}^\ell$, we can output $s_0,\ldots,s_{m-1}$. In this case $\Pr_{s\sim \{0,1\}^\ell}[ P(G(s))=1]$ will simply equal $\Pr_{r\in \{0,1\}^m}[ P(r)=1]$, no matter how many lines $P$ has. So, the smaller $\ell$ is and the larger $m$ is, the stronger the generator, and to get anything non-trivial, we need $m>\ell$.
>
Furthermore note that although our eventual goal is to fool probabilistic randomized algorithms that take an unbounded number of inputs,  [prgdef](){.ref} refers to _finite_ and _deterministic_ NAND programs.


We can think of a pseudorandom generator as a "randomness amplifier". It takes an input $s$ of $\ell$ bits chosen at random and expands these $\ell$ bits into an output $r$ of $m>\ell$ _pseudorandom_ bits.
If $\epsilon$ is small enough then the pseudorandom bits will "look random" to any NAND program that is not too big.
Still, there are two questions we haven't answered:

* _What reason do we have to believe that pseudorandom generators with non-trivial parameters exist?_

* _Even if they do exist, why would such generators be useful to derandomize randomized algorithms?_ After all, [prgdef](){.ref} does not involve RNAND++ or RNAND<<programs but deterministic NAND programs with no randomness and no loops.

We will now (partially) answer both questions.

For the first question, let us come clean and confess we do not know how to _prove_ that interesting pseudorandom generators exist.
By _interesting_ we mean pseudorandom generators that satisfy that $\epsilon$ is some small constant (say $\epsilon<1/3$), $m>\ell$, and the function $G$ itself can be computed in $poly(m)$ time.
Nevertheless, [prgexist](){.ref} (whose statement and proof is deferred to the end of this chapter) shows that if we only drop the last  condition (poltnomial-time computability), then there do in fact exist pseudorandom generators where $m$ is _exponentially larger_  than $\ell$.

> # { .pause }
At this point you might want to skip ahead and  look at the _statement_ of [prgexist](){.ref}. However, since its _proof_ is somewhat subtle, I recommend you defer reading it until you've finished reading the rest of this lecture.

### From existence to constructivity


The fact that there _exists_ a pseudorandom generator does not mean that there is one that can be efficiently computed.
However, it turns out that we can turn complexity "on its head" and used the assumed _non existence_ of fast algorithms for problems such as 3SAT to obtain pseudorandom generators that can then be used to transform randomized algorithms into deterministic ones.
This is known as the _Hardness vs Randomness_ paradigm.
A number of results along those lines, most of whom are ourside the scope of this course, has led researchers to believe the following conjecture:

>__Optimal PRG conjecture:__ There is a polynomial-time computable function $PRG:\{0,1\}^* \rightarrow \{0,1\}$ that yields an _exponentially secure pseudorandom generator_.
Specifically, there exists a constant  $\delta >0$ such that for every $\ell$ and $m < 2^{\delta \ell}$, if we define $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ as $G(s)_i = PRG(s,i)$ for every $s\in \{0,1\}^\ell$ and $i \in [m]$, then $G$ is a $(2^{\delta \ell},2^{-\delta \ell})$ pseudorandom generator.

> # { .pause }
The "optimal PRG conjecture" is worth while reading more than once. What it posits is that we can obtain $(T,\epsilon)$ pseudorandom generator $G$ such that every output bit of $G$ can be computed in time polynomial in the length $\ell$ of the input, where $T$ is exponentially large in $\ell$ and $\epsilon$ is exponentially small in $\ell$. (Note that we could not hope for the entire output to be computable in $\ell$, as just writing the output down will take too long.)
>
To understand why we call such a pseudorandom generator "optimal", it is a great exercise to convince yourself that there exists no $(T,\epsilon)$ pseudorandom generator unless $T$ is larger than (say) $2^{2\ell}$ and $\epsilon$ is at least (say) $2^{-2\ell}$.
For the former case note that if we allow a NAND program with much more than $2^\ell$ lines then this NAND program could "hardwire" inside it all the outputs of $G$ on all its $2^\ell$ inputs, and use that to distinguish between a string of the form $G(s)$ and a uniformly chosen string in $\{0,1\}^m$.
For the latter case note that by trying to "guess" the input $s$, we can achieve a $2^{-\ell}$ advantage in distinguishing a pseudorandom and uniform input.
But working out these details is a highly recommended exercise.

We emphasize again that the optimal PRG conjecture is, as its name implies, a _conjecture_, and we still do not know how to _prove_ it.
In particular, it is stronger than the conjecture that $\mathbf{P} \neq \mathbf{NP}$.
But we do have some evidence for its truth.
There is a spectrum of different types of pseudorandom generators, and there are weaker assumption than the optimal PRG conjecture that suffice to prove that $\mathbf{BPP}=\mathbf{P}$.
In particular this is known to hold under the assumption that there exists a function $F\in \mathbb{TIME}(2^{O(n)})$ and $\epsilon >0$ such that for every sufficiently large  $n$, $F_n$ is not in $SIZE(2^{\epsilon n})$.
The name "Optimal PRG conjecture" is non standard. This conjecture is sometimes known in the literature as the existence of exponentially strong pseudorandom functions.^[For more on the many interesting results and connections in the study of _pseudorandomness_, see [this monograph of Salil Vadhan](https://people.seas.harvard.edu/~salil/pseudorandomness/).]

### Usefulness of pseudorandom generators

We now show that optimal pseudorandom generators are indeed very useful, by proving the following theorem:

> # {.theorem title="Derandomization of BPP" #derandBPPthm}
Suppose that the optimal PRG conjecture is true. Then $\mathbf{BPP}=\mathbf{P}$.

> # {.proofidea data-ref="derandBPPthm"}
The optimal PRG conjecture tells us that we can achieve _exponential expansion_ of $\ell$ truly random coins into as many as $2^{\delta \ell}$ "pseudorandom coins".
Looked at from the other direction, it allows us to reduce the need for randomness by taking an algorithm that uses $m$ coins and converting it into an algorithm that only uses $O(\log m)$ coins.
Now an algorithm of the latter type by can be made fully deterministic by enumerating over all the $2^{O(\log m)}$ (which is polynomial in $m$) possiblities for its random choices.
We now proceed with the proof details.


> # {.proof data-ref="derandBPPthm"}
Let $F\in \mathbf{BPP}$ and let $P$ be a NAND++ program and $a,b,c,d$ constants such that for every $x\in \{0,1\}^n$, $P(x)$ runs in at most $c\dot n^d$ steps and  $\Pr_{r\sim \{0,1\}^m}[ P(x;r) = F(x) ] \geq 2/3$.
By "unrolling the loop" and hardwiring the input $x$, we can obtain for every input $x\in \{0,1\}^n$ a NAND program $Q_x$ of at most, say, $T=10c\dot n^d$ lines, that takes $m$ bits  of input and such that $Q(r)=P(x;r)$.
>
Now suppose that $G:\{0,1\}^\ell \rightarrow \{0,1\}$ is a $(T,0.1)$ pseudorandom generator.
Then we could deterministically estimate $\Pr_{r\sim \{0,1\}^m}[ Q_x(r) = 1 ]$ up to $0.1$ accuracy (and hence compute $F(x)$) in time  $O(T \cdot 2^\ell \cdot m \cdot cost(G))$ where $cost(G)$ is the time that it takes to compute a single output bit of $G$.
The reason is that we know that $\Pr_{s \sim \{0,1\}^\ell}[ Q_x(G(s)) = 1]$ will give us such an estimate, and we can compute this probability by simply trying all $2^\ell$ possibillites for $s$.
Now, under the optimal PRG conjecture we can set  $T = 2^{\delta \ell}$ or equivalently $\ell = \tfrac{1}{\delta}\log T$, and our total computation time is polynomial in $2^\ell = T^{1/\delta}$, and since $T \leq 10c \dot n^d$, this running time will be polynomial in $n$.


##  $\mathbf{P}=\mathbf{NP}$ and $\mathbf{BPP}$ vs $\mathbf{P}$

Two computational complexity questions that we cannot settle are:

* Is $\mathbf{P}=\mathbf{NP}$? Where we believe the answer  is _negative_.

* If $\mathbf{BPP}=\mathbf{P}$? Where we believe the answer is _positive_.

However we can say that the "conventional wisdom" is correct on at least one of these questions.
Namely, if we're wrong on the first count, then we'll be right on the second one:

> # {.theorem title="Sipser–Gács Theorem" #BPPvsNP}
If $\mathbf{P}=\mathbf{NP}$ then $\mathbf{BPP}=\mathbf{P}$.

> # {.proofidea data-ref="BPPvsNP"}
TO BE COMPLETED

> # {.proof data-ref="BPPvsNP"}
TO BE COMPLETED

## Non-constructive existence of pseudorandom generators

We now show that, if we don't insist on _constructivity_ of pseudorandom generators, then we can show that there exists  pseudorandom generators with output that  _exponentially larger_   in the input length.


> # {.lemma title="Existence of inefficient pseudorandom generators" #prgexist}
There is some absolute constant $C$ such that for every $\epsilon,T$, if $\ell > C (\log T + \log (1/\epsilon))$ and $m \leq T$,  then there is an $(T,\epsilon)$ pseudorandom generator $G: \{0,1\}^\ell \rightarrow \{0,1\}^m$.


> # {.proofidea data-ref="prgexist"}
The proof uses an extremely useful technique known  as the "probabilistic method" which is not too hard mathematically but can be confusing at first.^[There is a whole (highly recommended) [book by Alon and Spencer](https://www.amazon.com/Probabilistic-Method-Discrete-Mathematics-Optimization/dp/1119061954/ref=dp_ob_title_bk)  devoted to this method.]
The idea is to give a "non constructive" proof of existence of the pseudorandom generator $G$ by showing that if $G$ was chosen at random, then the probability that it would be a valid $(T,\epsilon)$ pseudorandom generator is positive.
In  particular this means that there _exists_ a single $G$ that is a valid $(T,\epsilon)$ pseudorandom generator.
The probabilistic method is just a _proof technique_ to demonstrate the existence of such a function.
Ultimately, our goal is to show the existence of  a _deterministic_ function $G$ that satisfies

The above discussion might be rather abstract at this point, but would become clearer after seeing the proof.



> # {.proof data-ref="prgexist"}
Let $\epsilon,T,\ell,m$ be as in the lemma's statement. We need to show that there exists a function $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ that "fools" every $T$ line program $P$ in the sense of [eq:prg](){.eqref}.
We will show that this follows from the following claim:
>
__Claim I:__ For every fixed NAND program $P$, if we pick $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ _at random_ then the probability that [eq:prg](){.eqref} is violated is at most $2^{-T^2}$.
>
Before proving Claim I, let us see why it implies [prgexist](){.ref}.
We can identify a function $G:\{0,1\}^\ell \rightarrow \{0,1\}^m$ with its "truth table" or simply the list of evaluations on all its possible $2^\ell$ inputs. Since each output is an $m$ bit string,
we can also think of $G$ as a string in $\{0,1\}^{m\cdot 2^\ell}$. We define $\mathcal{G}^m_\ell$ to be the set of all functions from $\{0,1\}^\ell$ to $\{0,1\}^\ell$. As discussed above we can identify $\mathcal{F}_\ell^m$ with $\{0,1\}^{m\cdot 2^\ell}$ and choosing a random function $G \sim \mathcal{F}_\ell^m$ corresponds to choosing a random $m\cdot 2^\ell$-long bit string.
>
For every NAND program $P$ let $B_P$ be the event that, if we choose $G$ at random from $\mathcal{F}_\ell^m$ then  [eq:prg](){.eqref} is violated with respect to the program $P$.
It is important to understand what is the sample space that the event $B_P$ is defined over, namely this event depends on the choice of $G$ and so $B_P$ is a subset of $\mathcal{F}_\ell^m$. An equivalent way to define the  event $B_P$ is that it is the subset of  all functions  mapping $\{0,1\}^\ell$ to $\{0,1\}^m$  that violate [eq:prg](){.eqref}, or in other words:
$$
B_P = \bigl\{ G \in \mathcal{F}_\ell^m  \; \big| \; \left| \tfrac{1}{2^\ell}\sum_{s\in \{0,1\}^\ell} P(G(s)) - \tfrac{1}{2^m}\sum_{r \in \{0,1\}^m}P(r)  \right| < \epsilon  \bigr\} \;\;. \label{eq:eventdefine}
$$
(We've replaced here the probability statements in [eq:prg](){.eqref} with the equivalent sums so as to reduce confusion as to what is the sample space that $B_P$ is defined over.)
>
To understand this proof it is crucial that you pause here and see how  the definition of $B_P$ above corresponds to [eq:eventdefine](){.eqref}. This may well take re-reading the above text once or twice, but it is a good exercise at parsing probabilistic statements and learning how to identify the _sample space_ that these statements correspond to.
>
Now, we've shown in [program-count](){.ref} that up to renaming variables (which makes no difference to program's functionality) there are $2^{O(T\log T)}$ NAND programs of at most $T$ lines.
Since $T\log T < T^2$ for sufficiently large $T$, this means that if the Claim I  is true, then by the union bound it holds that the probability of the union of $B_P$ over _all_ NAND programs of at most $T$ lines is at most $2^{O(T\log T)}2^{-T^2} < 0.1$ for sufficiently large $T$.
What is important for us about the number $0.1$ is that it is smaller than $1$.
In particular this means that there _exists_ a single $G^* \in \mathcal{F}_\ell^m$ such that $G^*$ _does not_ violate [eq:prg](){.eqref} with respect to any NAND program of at most $T$ lines, but that precisely means that $G^*$ is a $(T,\epsilon)$ pseudorandom generator.
>
Hence  conclude the proof of [prgexist](){.ref}, it suffices to prove Claim I.
Choosing a random $G: \{0,1\}^\ell \rightarrow \{0,1\}^m$ amounts to choosing $L=2^\ell$ random strings $y_0,\ldots,y_{L-1} \in \{0,1\}^m$ and letting $G(x)=y_x$ (identifying $\{0,1\}^\ell$ and $[L]$ via the binary representation).
Hence the claim amounts to showing that for every fixed function $P:\{0,1\}^m \rightarrow \{0,1\}$,
if $L >  2^{C (\log T + \log \epsilon)}$ (which by setting $C>4$, we can ensure is larger than $10 T^2/\epsilon^2$) then the probability that
$$
\left| \tfrac{1}{L}\sum_{i=0}^{L-1} P(y_s)  -  \Pr_{s \sim \{0,1\}^m}[P(s)=1] \right| > \epsilon \label{eq:prgchernoff}
$$
is at most $2^{-T^2}$.
[{eq:prgchernoff}](){.eqref} follows directly from the Chernoff bound.
If we let for every $i\in  [L]$  the random variable $X_i$ denote $P(y_i)$, then since $y_0,\ldots,y_{L-1}$ is chosen independently at random, these are independently and identically distributed random variables with mean $\E_{y \sim \{0,1\}^m}[P(y)]= \Pr_{y\sim \{0,1\}^m}[ P(y)=1]$ and hence the probability that they deviate from their expectation by $\epsilon$ is at most $2\cdot 2^{-\epsilon^2 L/2}$.


## Lecture summary


## Exercises




## Bibliographical notes


## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)



## Acknowledgements
