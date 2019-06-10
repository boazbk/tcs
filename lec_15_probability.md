---
title: "Probability theory 101"
filename: "lec_15_probability"
chapternum: "17"
---

#  Probability Theory 101 {#probabilitychap }

> ### { .objectives }
* Review the basic notion of probability theory that we will use. \
* Sample spaces, and in particular the space $\{0,1\}^n$ \
* Events, probabilities of unions and intersections. \
* Random variables and their expectation, variance, and standard deviation. \
* Independence and correlation for both events and random variables. \
* Markov, Chebyshev and Chernoff tail bounds (bounding the probability that a random variable will deviate from its expectation).



>_"God doesn't play dice with the universe"_, Albert Einstein

>_"Einstein was doubly wrong ... not only does God definitely play dice, but He sometimes confuses us by throwing them where they can't be seen."_, Stephen Hawking

>_"'The probability of winning a battle' has no place in our theory because it does not belong to any [random experiment]. Probability cannot be applied to this problem any more than the physical concept of work can be applied to the 'work' done by an actor reciting his part."_, Richard Von Mises, 1928 (paraphrased)

>_"I am unable to see why 'objectivity' requires us to interpret every probability as a frequency in some random experiment; particularly when in most problems probabilities are frequencies only in an imaginary universe invented just for the purpose of allowing a frequency interpretation."_, E.T. Jaynes, 1976


Before we show how to use randomness in algorithms, let us do a quick review of some basic notions in probability theory.
This is not meant to replace a course on probability theory, and if you have not seen this material before, I highly recommend you look at additional resources to get up to speed.^[Harvard's [STAT 110](http://projects.iq.harvard.edu/stat110/home) class (whose lectures are available on [youtube](http://projects.iq.harvard.edu/stat110/youtube) ) is a highly recommended introduction to probability. See also these [lecture notes](https://goo.gl/4SoqJk) from MIT's "Mathematics for Computer Science" course.]
Fortunately, we will not need many of the advanced notions of probability theory, but, as we will see, even the so-called "simple" setting of tossing $n$ coins can lead to very subtle and interesting issues.




## Random coins


The nature of randomness and probability is a topic of great philosophical, scientific and mathematical depth.
Is there actual randomness in the world, or does it proceed in a deterministic clockwork fashion from some initial conditions set at the beginning of time?
Does probability refer to our uncertainty of beliefs, or to the frequency of occurrences in repeated experiments?
How can we define probability over infinite sets?

These are all important questions that have been studied and debated by scientists, mathematicians, statisticians and philosophers.
Fortunately, we will not need to deal directly with these questions here.
We will be mostly interested in the setting of tossing $n$ random, unbiased and independent coins.
Below we define the basic probabilistic objects of _events_ and _random variables_ when restricted to this setting.
These can be defined for much more general probabilistic experiments or _sample spaces_, and later on we will briefly discuss how this can be done. However, the $n$-coin case is sufficient for almost everything we'll need in this course.

If instead of "heads" and "tails" we encode the sides of each coin by "zero" and "one", we can encode the result of tossing $n$ coins as a string in $\{0,1\}^n$.
Each particular outcome $x\in \{0,1\}^n$ is obtained with probability $2^{-n}$.
For example, if we toss three coins, then we obtain each of the 8 outcomes $000,001,010,011,100,101,110,111$ with probability $2^{-3}=1/8$ (see also [coinexperimentfig](){.ref}).
We can describe the experiment of tossing $n$ coins as choosing a string $x$ uniformly at random from $\{0,1\}^n$, and hence we'll use the shorthand $x\sim \{0,1\}^n$ for $x$ that is chosen according to this experiment.

![The probabilistic experiment of tossing three coins corresponds to making $2\times 2 \times 2 = 8$ choices, each with equal probability. In this example, the blue set corresponds to the event $A = \{ x\in \{0,1\}^3 \;|\; x_0 = 0 \}$ where the first coin toss is equal to $0$,  and the pink set corresponds to the event $B = \{ x\in \{0,1\}^3 \;|\; x_1 = 1 \}$ where the second coin toss is equal to $1$ (with their intersection having a purplish color). As we can see, each of these events contains $4$ elements (out of $8$ total) and so has probability $1/2$. The intersection of $A$ and $B$ contains two elements, and so the probability that both of these events occur is $2/8 = 1/4$.](../figure/coinexperiment.png){#coinexperimentfig .margin  }

An _event_ is simply a subset $A$ of $\{0,1\}^n$.
The _probability of $A$_, denoted by $\Pr_{x\sim \{0,1\}^n}[A]$ (or $\Pr[A]$ for short, when the sample space is understood from the context), is the probability that an $x$ chosen uniformly at random will be contained in $A$.
Note that this is the same as $|A|/2^n$ (where $|A|$ as usual denotes the number of elements in the set $A$).
For example, the probability that $x$ has an even number of ones is $\Pr[A]$ where $A=\{ x : \sum_{i=0}^{n-1} x_i \;= 0 \mod 2 \}$.
In the case $n=3$, $A=\{ 000,011,101,110 \}$, and hence $\Pr[A]=\tfrac{4}{8}=\tfrac{1}{2}$.
It turns out this is true for every $n$:

> ### {.lemma #evenprob}
$$\Pr_{x\sim \{0,1\}^n}[ \text{$\sum_{i=0}^{n-1} x_i$ is even }] = 1/2$$

> ### { .pause }
To test your intuition on probability, try to stop here and prove the lemma on your own.

> ### {.proof data-ref="evenprob"}
Let $A = \{ x \in \{0,1\}^n :  \sum_{i=0}^{n-1} x_i = 0 \mod 2 \}$.
Since every $x$ is obtained with probability $2^{-n}$, to show this we need to show that $|A|=2^n/2=2^{n-1}$.
For every $x_0,\ldots,x_{n-2}$, if $\sum_{i=0}^{n-2} x_i$ is even then $(x_0,\ldots,x_{n-1},0)\in A$ and $(x_0,\ldots,x_{n-1},1) \not\in A$.
Similarly, if $\sum_{i=0}^{n-2} x_i$ is odd then $(x_0,\ldots,x_{n-1},1) \in A$ and  $(x_0,\ldots,x_{n-1},0)\not\in A$.
Hence, for every one of the $2^{n-1}$ prefixes $(x_0,\ldots,x_{n-2})$, there is exactly a single continuation of $(x_0,\ldots,x_{n-2})$ that places it in $A$.

We can also use the _intersection_ ($\cap$) and _union_ ($\cup$) operators to talk about the probability of both event $A$ _and_ event $B$ happening, or the probability of event $A$ _or_ event $B$ happening.
For example, the probability $p$ that $x$ has an _even_ number of ones _and_ $x_0=1$ is the same as
$\Pr[A\cap B]$ where $A=\{ x\in \{0,1\}^n : \sum_{i=0}^{n-1} x_i =0 \mod 2 \}$ and $B=\{ x\in \{0,1\}^n : x_0 = 1 \}$.
This probability is equal to $1/4$ for $n > 1$. (It is a great exercise for you to pause here and verify that you understand why this is the case.)


Because intersection corresponds to considering the logical AND of the conditions that two events happen, while union corresponds to considering the logical OR, we will sometimes use the $\wedge$ and $\vee$ operators instead of $\cap$ and $\cup$, and so write this probability $p=\Pr[A \cap B]$ defined above also as
$$
\Pr_{x\sim \{0,1\}^n} \left[ \sum_i x_i =0 \mod 2 \; \wedge \; x_0 = 1 \right] \;.
$$

If $A \subseteq \{0,1\}^n$ is an event, then $\overline{A} = \{0,1\}^n \setminus A$ corresponds to the event that $A$ does _not_ happen.
Since $|\overline{A}|=2^n-|A|$, we get that
$$\Pr[\overline{A}] = \tfrac{|\overline{A}|}{2^n} = \tfrac{2^n-|A|}{2^n}=1-\tfrac{|A|}{2^n} = 1- \Pr[A]
$$
This makes sense: since $A$ happens if and only if $\overline{A}$ does _not_ happen, the probability of $\overline{A}$ should be one minus the probability of $A$.

> ### {.remark title="Remember the sample space" #samplespace}
While the above definition might seem very simple and almost trivial,  the human mind seems not to have evolved for probabilistic reasoning, and it is surprising how often people can get even the simplest settings of probability wrong.
One way to make sure you don't get confused when trying to calculate probability statements is to always ask yourself the following two questions: __(1)__ Do I understand what is the __sample space__ that this probability is taken over?, and __(2)__ Do I understand what is the definition of the __event__ that we are analyzing?.
>
For example, suppose that I were to randomize seating in my course, and then it turned out that students sitting in row 7 performed better on the final: how surprising should we find this? If we started out with the hypothesis that there is something special about the number 7 and chose it ahead of time, then the event that we are discussing is the event $A$  that students sitting in number 7 had better performance on the final, and we might find it surprising. However, if we first looked at the results and then chose the row whose average performance is best, then the event we are discussing is the event $B$ that there exists _some_ row where the performance is higher than the overall average. $B$ is a superset of $A$, and its probability (even if there is no correlation between sitting and performance) can be quite significant.



### Random variables

_Events_ correspond to Yes/No questions, but often we want to analyze finer questions.
For example, if we make a bet at the roulette wheel, we don't want to just analyze whether we won or lost, but also _how much_ we've gained.
A (real valued) _random variable_ is simply a way to associate a number with the result of a probabilistic experiment.
Formally, a random variable is simply a function $X:\{0,1\}^n \rightarrow \R$ that maps every outcome $x\in \{0,1\}^n$ to a real number $X(x)$.^[In many probability texts a random variable is always defined to have values in the set $\R$ of real numbers, and this will be our default option as well. However, in some contexts in theoretical computer science we can consider random variables mapping to other sets such as $\{0,1\}^*$.]
For example, the function $sum:\{0,1\}^n \rightarrow \R$ that maps $x$ to the sum of its coordinates (i.e., to $\sum_{i=0}^{n-1} x_i$) is a random variable.


The _expectation_ of a random variable $X$, denoted by $\E[X]$, is the average value that that this number takes, taken over all draws from the probabilistic experiment.
In other words, the expectation of $X$ is defined as follows:
$$
\E[X] = \sum_{x\in \{0,1\}^n} 2^{-n}X(x) \;.
$$



If $X$ and $Y$ are random variables, then we can define $X+Y$ as simply the random variable that maps a point $x\in \{0,1\}^n$ to $X(x)+Y(x)$.
One basic and very useful property of the expectation is that it is _linear_:

> ### {.lemma title="Linearity of expectation" #linearityexp}
$$ \E[ X+Y ] = \E[X] + \E[Y] $$

> ### {.proof data-ref="linearityexp"}
$$
\begin{gathered}
\E [X+Y] = \sum_{x\in \{0,1\}^n}2^{-n}\left(X(x)+Y(x)\right) =  \\
\sum_{x\in \{0,1\}^b} 2^{-n}X(x) + \sum_{x\in \{0,1\}^b} 2^{-n}Y(x) = \\
\E[X] + \E[Y]
\end{gathered}
$$

Similarly, $\E[kX] = k\E[X]$ for every $k \in \R$.
For example, using the linearity of expectation, it is very easy to show that the expectation of the sum of the $x_i$'s for $x \sim \{0,1\}^n$ is equal to $n/2$.
Indeed, if we write $X= \sum_{i=0}^{n-1} x_i$ then $X= X_0 + \cdots + X_{n-1}$ where $X_i$ is the random variable $x_i$. Since for every $i$, $\Pr[X_i=0] = 1/2$ and $\Pr[X_i=1]=1/2$, we get that $\E[X_i] = (1/2)\cdot 0 + (1/2)\cdot 1 = 1/2$ and hence $\E[X] = \sum_{i=0}^{n-1}\E[X_i] = n\cdot(1/2) = n/2$.


> ### { .pause }
If you have not seen discrete probability before, please go over this argument again until you are sure you follow it; it is a prototypical simple example of the type of reasoning we will employ again and again in this course.

If $A$ is an event, then $1_A$ is the random variable such that $1_A(x)$ equals $1$ if $x\in A$, and $1_A(x)=0$ otherwise.
Note that $\Pr[A] = \E[1_A]$ (can you see why?).
Using this and the linearity of expectation, we can show one of the most useful bounds in probability theory:

> ### {.lemma title="Union bound" #unionbound}
For every two events $A,B$, $\Pr[ A \cup B] \leq \Pr[A]+\Pr[B]$

> ### { .pause }
Before looking at the proof, try to see why the union bound makes intuitive sense. We can also prove it directly from the definition of probabilities and the cardinality of sets, together with the equation $|A \cup B| \leq |A|+|B|$. Can you see why the latter equation is true? (See also [unionboundfig](){.ref}.)

> ### {.proof data-ref="unionbound"}
For every $x$, the variable $1_{A\cup B}(x) \leq 1_A(x)+1_B(x)$.
Hence, $\Pr[A\cup B] = \E[ 1_{A \cup B} ] \leq \E[1_A+1_B] = \E[1_A]+\E[1_B] = \Pr[A]+\Pr[B]$.

The way we often use this in theoretical computer science is to argue that, for example, if there is a list of 100 bad events that can happen, and each one of them happens with probability at most $1/10000$, then with probability at least $1-100/10000 = 0.99$, no bad event happens.

![The _union bound_ tells us that the probability of $A$ or $B$ happening is at most the sum of the individual probabilities. We can see it by noting that for every two sets $|A\cup B| \leq |A|+|B|$ (with equality only if $A$ and $B$ have no intersection).](../figure/unionbound.png){#unionboundfig .margin  }

### Distributions over strings

While most of the time we think of random variables as having as output a _real number_, we sometimes consider random variables whose output is a _string_.
That is, we can think of a map $Y:\{0,1\}^n \rightarrow \{0,1\}^*$ and consider the "random variable" $Y$ such that for every $y\in \{0,1\}^*$, the probability that $Y$ outputs $y$ is equal to $\tfrac{1}{2^n}\left| \{ x \in \{0,1\}^n \;|\; Y(x)=y \}\right|$.
To avoid confusion, we will typically refer to such string-valued random variables as _distributions_ over strings.
So, a _distribution_ $Y$ over strings $\{0,1\}^*$ can be thought of as a finite collection of strings $y_0,\ldots,y_{M-1} \in \{0,1\}^*$ and probabilities $p_0,\ldots,p_{M-1}$ (which are non-negative numbers summing up to one), so that $\Pr[ Y = y_i ] = p_i$.

Two distributions $Y$ and $Y'$ are _identical_ if they assign the same probability to every string.
For example, consider the following two functions $Y,Y':\{0,1\}^2 \rightarrow \{0,1\}^2$.
For every $x \in \{0,1\}^2$, we define $Y(x)=x$ and $Y'(x)=x_0(x_0\oplus x_1)$ where $\oplus$ is the XOR operations.
Although these are two different functions, they induce the same distribution over $\{0,1\}^2$ when invoked on a uniform input.
The distribution $Y(x)$ for $x\sim \{0,1\}^2$ is of course the uniform distribution over $\{0,1\}^2$.
On the other hand $Y'$ is simply the map $00 \mapsto 00$, $01 \mapsto 01$, $10 \mapsto 11$, $11 \mapsto 10$ which is a permutation over
the map $F:\{0,1\}^2 \rightarrow \{0,1\}^2$ defined as $F(x_0x_1)=x_0x_1$ and the map $G:\{0,1\}^2 \rightarrow \{0,1\}^2$  defined as $G(x_0x_1)=x_0(x_0 \oplus x_1)$

### More general sample spaces.

While in this chapter we assume that the underlying probabilistic experiment   corresponds to tossing $n$ independent coins, everything we say easily generalizes to sampling $x$ from a more general finite or countable set $S$ (and not-so-easily generalizes to uncountable sets $S$ as well).
A _probability distribution_ over a finite set $S$ is simply a function $\mu : S \rightarrow [0,1]$ such that
$\sum_{x\in S}\mu(s)=1$.
We think of this as the experiment where we obtain every $x\in S$ with probability $\mu(s)$, and sometimes denote this as $x\sim \mu$.
An _event_ $A$ is a subset of $S$, and the probability of $A$, which we denote by $\Pr_\mu[A]$, is $\sum_{x\in A} \mu(x)$.
A _random variable_ is a function $X:S \rightarrow \R$, where the probability that $X=y$ is equal to $\sum_{x\in S \text{ s.t. } X(x)=y} \mu(x)$.


^[TODO: add exercise on simulating die tosses and choosing a random number in $[m]$ by coin tosses]


## Correlations and independence

One of the most delicate but important concepts in probability is the notion of _independence_ (and the opposing notion of _correlations_).
Subtle correlations are often behind surprises and errors in probability and statistical analysis, and several mistaken predictions have been blamed on miscalculating the correlations between, say, housing prices in Florida and Arizona, or voter preferences in Ohio and Michigan. See also Joe Blitzstein's aptly named talk ["Conditioning is the Soul of Statistics"](https://youtu.be/dzFf3r1yph8).^[Another thorny issue is of course the difference between _correlation_ and _causation_. Luckily, this is another point we don't need to worry about in our clean setting of tossing $n$ coins.]

Two events $A$ and $B$ are _independent_ if the fact that $A$ happens makes $B$ neither more nor less likely to happen.
For example, if we think of the experiment of tossing $3$ random coins $x\in \{0,1\}^3$, and we let $A$ be the event that $x_0=1$ and $B$ the event that $x_0 + x_1 + x_2 \geq 2$, then if $A$ happens it is more likely that $B$ happens, and hence these events are _not_ independent.
On the other hand, if we let $C$ be the event that $x_1=1$, then because the second coin toss is not affected by the result of the first one, the events $A$ and $C$ are independent.

The formal definition is that events $A$ and $B$ are _independent_ if $\Pr[A \cap B]=\Pr[A] \cdot \Pr[B]$.
If $\Pr[A \cap B] > \Pr[A]\cdot \Pr[B]$ then we say that $A$ and $B$ are _positively correlated_, while if $\Pr[ A \cap B] < \Pr[A] \cdot \Pr[B]$ then we say that $A$ and $B$ are _negatively correlated_ (see [coinexperimentfig](){.ref}).


![Two events $A$ and $B$ are _independent_ if $\Pr[A \cap B]=\Pr[A]\cdot \Pr[B]$. In the two figures above, the empty $x\times x$ square is the sample space, and $A$ and $B$ are two events in this sample space. In the left figure, $A$ and $B$ are independent, while in the right figure they are negatively correlated, since $B$ is less likely to occur if we condition on $A$ (and vice versa). Mathematically, one can see this by noticing that in the left figure the areas of $A$ and $B$ respectively are $a\cdot x$ and $b\cdot x$, and so their probabilities are $\tfrac{a\cdot x}{x^2}=\tfrac{a}{x}$ and
$\tfrac{b\cdot x}{x^2}=\tfrac{b}{x}$ respectively, while the area of $A \cap B$ is $a\cdot b$ which corresponds to the probability $\tfrac{a\cdot b}{x^2}$. In the right figure, the area of the triangle $B$ is $\tfrac{b\cdot x}{2}$ which corresponds to a probability of  $\tfrac{b}{2x}$, but the area of $A \cap B$ is $\tfrac{b' \cdot a}{2}$ for some $b'<b$. This means that the probability of $A \cap B$ is $\tfrac{b'\cdot a}{2x^2} < \tfrac{b}{2x} \cdot \tfrac{a}{x}$, or in other words $\Pr[A \cap B ] < \Pr[A] \cdot \Pr[B]$.](../figure/independence.png){#independencefig .margin  }


If we consider the above examples on the experiment of choosing $x\in \{0,1\}^3$ then we can see that

$$
\begin{aligned}
\Pr[x_0=1] &= \tfrac{1}{2} \\
\Pr[x_0+x_1+x_2 \geq 2] = \Pr[\{ 011,101,110,111 \}] &= \tfrac{4}{8} = \tfrac{1}{2}
\end{aligned}
$$

but

$$
\Pr[x_0 =1 \; \wedge \; x_0+x_1+x_2 \geq 2 ] = \Pr[ \{101,110,111 \} ] = \tfrac{3}{8} > \tfrac{1}{2} \cdot \tfrac{1}{2}
$$

and hence, as we already observed, the events $\{ x_0 = 1 \}$ and $\{ x_0+x_1+x_2 \geq 2 \}$ are not independent and in fact are positively correlated.
On the other hand, $\Pr[ x_0 = 1 \wedge x_1 = 1 ] = \Pr[ \{110,111 \}] = \tfrac{2}{8} = \tfrac{1}{2} \cdot \tfrac{1}{2}$ and hence the events $\{x_0 = 1 \}$ and $\{ x_1 = 1 \}$ are indeed independent.

> ### {.remark title="Disjointness vs independence" #disjoint}
People sometimes confuse the notion of _disjointness_ and _independence_, but these are actually quite different.
Two events $A$ and $B$ are _disjoint_ if $A \cap B = \emptyset$, which means that if $A$ happens then $B$ definitely does not happen. They are _independent_ if $\Pr[A \cap B]=\Pr[A]\Pr[B]$ which means that knowing that $A$ happens gives us no information about whether $B$ happened or not. If $A$ and $B$ have nonzero probability, then being disjoint implies that they are _not_ independent, since in particular it means that they are negatively correlated.



__Conditional probability:__ If $A$ and $B$ are events, and $A$ happens with nonzero probability then we define the probability that $B$ happens _conditioned on $A$_ to be $\Pr[B|A] = \Pr[A \cap B]/\Pr[A]$.
This corresponds to calculating the probability that $B$ happens if we already know that $A$ happened.
Note that $A$ and $B$ are independent if and only if $\Pr[B|A]=\Pr[B]$.

__More than two events:__ We can generalize this definition to more than two events.
We say that events $A_1,\ldots,A_k$ are _mutually independent_ if knowing that any set of them occurred or didn't occur does not change the probability that an event outside the set occurs.
Formally, the condition is that for every subset $I \subseteq [k]$,
$$
\Pr[ \wedge_{i\in I} A_i] =\prod_{i\in I} \Pr[A_i].
$$

For example, if $x\sim \{0,1\}^3$, then the events $\{ x_0=1 \}$, $\{ x_1 = 1\}$ and $\{x_2 = 1 \}$ are mutually independent.
On the other hand, the events $\{x_0 = 1 \}$, $\{x_1 = 1\}$ and $\{ x_0 + x_1 = 0 \mod 2 \}$ are _not_ mutually independent, even though every pair of these events is independent (can you see why? see also [independencecoinsfig](){.ref}).


![Consider the sample space $\{0,1\}^n$ and the events $A,B,C,D,E$ corresponding to $A$: $x_0=1$, $B$: $x_1=1$, $C$: $x_0+x_1+x_2 \geq 2$, $D$: $x_0+x_1+x_2 = 0 mod 2$ and $D$: $x_0+x_1 = 0 mod 2$. We can see that $A$ and $B$ are independent, $C$ is positively correlated with $A$ and positively correlated with $B$, the three events $A,B,D$ are mutually independent, and while every pair out of $A,B,E$ is independent, the three events $A,B,E$ are not mutually independent since their intersection has probability $\tfrac{2}{8}=\tfrac{1}{4}$ instead of $\tfrac{1}{2}\cdot \tfrac{1}{2} \cdot \tfrac{1}{2} = \tfrac{1}{8}$.](../figure/independencecoins.png){#independencecoinsfig .margin  }

### Independent random variables

We say that two random variables $X:\{0,1\}^n \rightarrow \R$ and $Y:\{0,1\}^n \rightarrow \R$ are independent if for every $u,v \in \R$, the events $\{ X=u \}$ and $\{ Y=v \}$ are independent.^[We use $\{ X=u \}$ as shorthand for $\{ x \;|\; X(x)=u \}$.]
In other words, $X$ and $Y$ are independent if $\Pr[ X=u \wedge Y=v]=\Pr[X=u]\Pr[Y=v]$ for every $u,v \in \R$.
For example, if two random variables depend on the result of tossing different coins then they are independent:

> ### {.lemma  #indcoins}
Suppose that $S=\{ s_0,\ldots, s_{k-1} \}$ and $T=\{ t_0 ,\ldots, t_{m-1} \}$ are disjoint subsets of $\{0,\ldots,n-1\}$ and let
$X,Y:\{0,1\}^n \rightarrow \R$ be random variables such that $X=F(x_{s_0},\ldots,x_{s_{k-1}})$ and $Y=G(x_{t_0},\ldots,x_{t_{m-1}})$ for some functions $F: \{0,1\}^k \rightarrow \R$ and $G: \{0,1\}^m \rightarrow \R$.
Then $X$ and $Y$ are independent.

> ### { .pause }
The notation in the lemma's statement is a bit cumbersome, but at the end of the day, it simply says that if $X$ and $Y$ are random variables that depend on two disjoint sets $S$ and $T$ of coins (for example, $X$ might be the sum of the first $n/2$ coins, and $Y$ might be the largest consecutive stretch of zeroes in the second $n/2$ coins), then they are independent.

> ### {.proof data-ref="indcoins"}
Let $a,b\in \R$, and let $A = \{ x \in \{0,1\}^k : F(x)=a \}$ and $B=\{ x\in \{0,1\}^m : F(x)=b \}$.
Since $S$ and $T$ are disjoint, we can reorder the indices so that $S = \{0,\ldots,k-1\}$ and $T=\{k,\ldots,k+m-1\}$ without affecting any of the probabilities.
Hence we can write $\Pr[X=a \wedge X=b] = |C|/2^n$ where $C= \{ x_0,\ldots,x_{n-1} : (x_0,\ldots,x_{k-1}) \in A \wedge (x_k,\ldots,x_{k+m-1}) \in B \}$.
Another way to write this using string concatenation is that $C = \{ xyz : x\in A, y\in B, z\in \{0,1\}^{n-k-m} \}$, and hence $|C|=|A||B|2^{n-k-m}$, which means that
$$
\tfrac{|C|}{2^n} = \tfrac{|A|}{2^k}\tfrac{|B|}{2^m}\tfrac{2^{n-k-m}}{2^{n-k-m}}=\Pr[X=a]\Pr[Y=b] .
$$



Note that if $X$ and $Y$ are independent random variables then (if we let $S_X,S_Y$ denote all the numbers that have positive probability of being the output of $X$ and $Y$, respectively) it holds that:
$$
\begin{gathered}
\E[ XY ] = \sum_{a \in S_X,b \in S_Y} {\textstyle\Pr[X=a \wedge Y=b]}\cdot ab \; =^{(1)} \; \sum_{a \in S_X,b \in S_Y} {\textstyle \Pr[X=a]\Pr[Y=b]}\cdot ab =^{(2)} \\
\left(\sum_{a \in S_X} {\textstyle \Pr[X=a]}\cdot a\right)\left(\sum_{b \in S_Y} {\textstyle \Pr[Y=b]}b\right) =^{(3)} \\
\E[X] \E[Y]
\end{gathered}
$$
where the first equality  ($=^{(1)}$) follows from the independence of $X$ and $Y$, the second equality ($=^{(2)}$) follows by "opening the parentheses" of the righthand side, and the third inequality ($=^{(3)}$) follows from the definition of expectation.
(This is not an "if and only if"; see [noindnocorex](){.ref}.)

Another useful fact is that if $X$ and $Y$ are independent random variables, then so are $F(X)$ and $G(Y)$ for all functions $F,G:\R \rightarrow R$.
This is intuitively true since learning $F(X)$ can only provide us with less information than does learning $X$ itself.
Hence, if learning $X$ does not teach us anything about $Y$ (and so also about $F(Y)$) then neither will learning $F(X)$.
Indeed, to prove this we can write for every $a,b \in \R$:

$$
\begin{gathered}
\Pr[ F(X)=a \wedge G(Y)=b ] = \sum_{x \text{ s.t.} F(x)=a, y \text{ s.t. } G(y)=b} \Pr[ X=x \wedge Y=y ] = \\
\sum_{x \text{ s.t.} F(x)=a, y \text{ s.t. } G(y)=b} \Pr[ X=x ] \Pr[  Y=y ]  = \\
\left( \sum_{x \text{ s.t.} F(x)=a } \Pr[X=x ] \right) \cdot \left( \sum_{y \text{ s.t.} G(y)=b } \Pr[Y=y ] \right) = \\
\Pr[ F(X)=a] \Pr[G(Y)=b] .
\end{gathered}
$$

### Collections of independent random variables.

We can extend the notions of independence to more than two random variables:
we say that the random variables $X_0,\ldots,X_{n-1}$ are _mutually independent_ if for every $a_0,\ldots,a_{n-1} \in \R$,
$$
\Pr\left[X_0=a_0 \wedge \cdots \wedge X_{n-1}=a_{n-1}\right]=\Pr[X_0=a_0]\cdots \Pr[X_{n-1}=a_{n-1}] .
$$
And similarly, we have that

> ### {.lemma title="Expectation of product of independent random variables" #expprod}
If $X_0,\ldots,X_{n-1}$ are mutually independent then
$$
\E[ \prod_{i=0}^{n-1} X_i ] = \prod_{i=0}^{n-1} \E[X_i] .
$$

> ### {.lemma title="Functions preserve independence" #indeplem}
If $X_0,\ldots,X_{n-1}$ are mutually independent, and $Y_0,\ldots,Y_{n-1}$ are defined as $Y_i = F_i(X_i)$ for some functions $F_0,\ldots,F_{n-1}:\R \rightarrow \R$, then $Y_0,\ldots,Y_{n-1}$ are mutually independent as well.

> ### { .pause }
We leave proving [expprod](){.ref} and [indeplem](){.ref} as [expprodex](){.ref} [indeplemex](){.ref}.
It is good idea for you stop now and do these exercises to make sure you are comfortable with the notion of independence, as we will use it heavily later on in this course.



## Concentration

The name "expectation" is somewhat misleading.
For example, suppose that you and I place a bet on the outcome of 10 coin tosses, where if they all come out to be $1$'s then I pay you 100,000 dollars and otherwise you pay me 10 dollars.
If we let $X:\{0,1\}^{10} \rightarrow \R$ be the random variable denoting your gain, then we see that

$$
\E[X] = 2^{-10}\cdot 100000 - (1-2^{-10})10 \sim 90 .
$$

But we don't really "expect" the result of this experiment to be for you to gain 90 dollars.
Rather, 99.9\% of the time you will pay me 10 dollars, and you will hit the jackpot 0.01\% of the times.

However, if we repeat this experiment again and again (with fresh and hence _independent_ coins), then in the long run we do expect your average earning to be 90 dollars, which is the reason why casinos can make money in a predictable way even though every individual bet is random.
For example, if we toss $n$ coins, then as $n$ grows, the number of coins that come up ones will be more and more _concentrated_ around $n/2$ according to the famous "bell curve" (see [bellfig](){.ref}).

![The probabilities that we obtain a particular sum when we toss $n=10,20,100,1000$ coins converge quickly to the Gaussian/normal distribution.](../figure/binomial.png){#bellfig .margin  }

Much of probability theory is concerned with so called _concentration_ or _tail_ bounds, which are upper bounds on the probability that a random variable $X$ deviates too much from its expectation.
The first and simplest one of them is Markov's inequality:

> ### {.theorem title="Markov's inequality" #markovthm}
If $X$ is a non-negative random variable then $\Pr[ X \geq k \E[X] ] \leq 1/k$.

> ### { .pause }
Markov's Inequality is actually a very natural statement (see also [markovfig](){.ref}). For example, if you know that the average (not the median!) household income in the US is 70,000 dollars, then in particular you can deduce that at most 25 percent of households make more than 280,000 dollars, since otherwise, even if the remaining 75 percent had zero income, the top 25 percent alone would cause the average income to be larger than 70,000. From this example you can already see that in many situations, Markov's inequality will not be _tight_ and the probability of deviating from expectation will be much smaller: see the Chebyshev and Chernoff inequalities below.

> ### {.proof data-ref="markovthm"}
Let $\mu = \E[X]$ and define $Y=1_{X \geq k \mu}$. That is, $Y(x)=1$ if $X(x) \geq k \mu$ and $Y(x)=0$ otherwise.
Note that by definition, for every $x$, $Y(x) \leq X/(k\mu)$.
We need to show $\E[Y] \leq 1/k$.
But this follows since  $\E[Y] \leq \E[X/k(\mu)] = \E[X]/(k\mu) = \mu/(k\mu)=1/k$.

![Markov's Inequality tells us that a non-negative random variable $X$ cannot be much larger than its expectation, with high probability. For example, if the expectation of $X$ is $\mu$, then the probability that $X>4\mu$ must be at most $1/4$, as otherwise just the contribution from this part of the sample space will be too large.](../figure/markovineq.png){#markovfig .margin  }


__Going beyond Markov's Inequality:__
Markov's inequality says that a (non-negative) random variable $X$ can't go too crazy and be, say, a million times its expectation, with significant probability.
But ideally we would like to say that with high probability, $X$ should be very close to its expectation, e.g., in the range $[0.99 \mu, 1.01 \mu]$ where $\mu = \E[X]$.
This is not generally true, but does turn out to hold when $X$ is obtained by combining (e.g., adding)  many independent random variables.
This phenomenon, variants of which are known as  "law of large numbers", "central limit theorem", "invariance principles" and "Chernoff bounds", is one of the most fundamental in probability and statistics, and is one that we heavily use in computer science as well.

### Chebyshev's Inequality

A standard way to measure the deviation of a random variable from its expectation is by using its _standard deviation_.
For a random variable $X$, we define the _variance_ of $X$ as  $\mathrm{Var}[X] = \E[(X-\mu)^2]$ where $\mu = \E[X]$; i.e., the variance is the average squared distance of $X$ from its expectation.
The _standard deviation_ of $X$ is defined as $\sigma[X] = \sqrt{\mathrm{Var}[X]}$.
(This is well-defined since the variance, being an average of a square, is always a non-negative number.)

Using Chebyshev's inequality, we can control the probability that a random variable is too many standard deviations away from its expectation.

> ### {.theorem title="Chebyshev's inequality" #chebychevthm}
Suppose that $\mu=\E[X]$ and $\sigma^2 = \mathrm{Var}[X]$.
Then for every $k>0$, $\Pr[ |X-\mu | \geq k \sigma ] \leq 1/k^2$.

> ### {.proof data-ref="chebychevthm"}
The proof follows from Markov's inequality.
We define the random variable $Y = (X-\mu)^2$.
Then $\E[Y] = \mathrm{Var}[X] = \sigma^2$, and hence by Markov the probability that $Y > k^2\sigma^2$ is at most $1/k^2$.
But clearly $(X-\mu)^2 \geq k^2\sigma^2$ if and only if $|X-\mu| \geq k\sigma$.



One example of how to use Chebyshev's inequality is the setting when $X = X_1 + \cdots + X_n$ where $X_i$'s are _independent and identically distributed_ (i.i.d for short) variables with values in $[0,1]$ where each has expectation $1/2$.
Since $\E[X] = \sum_i \E[X_i] = n/2$, we would like to say that $X$ is very likely to be in, say, the interval  $[0.499n,0.501n]$.
Using Markov's inequality directly will not help us, since it will only tell us that $X$ is very likely to be at most $100n$ (which we already knew, since it always lies between $0$ and $n$).
However,  since $X_1,\ldots,X_n$ are independent,
$$
\mathrm{Var}[X_1+\cdots +X_n] = \mathrm{Var}[X_1]+\cdots + \mathrm{Var}[X_n]  \label{varianceeq}\;.
$$
(We leave showing this to the reader as  [varianceex](){.ref}.)

For every random variable $X_i$ in $[0,1]$, $\mathrm{Var}[X_i] \leq 1$ (if the variable is always in $[0,1]$, it can't be more than $1$ away from its expectation), and hence [varianceeq](){.eqref} implies that $\mathrm{Var}[X]\leq n$ and hence $\sigma[X] \leq \sqrt{n}$.
For large $n$, $\sqrt{n} \ll 0.001n$, and in particular if $\sqrt{n} \leq 0.001n/k$,  we can use Chebyshev's inequality to bound the probability that $X$ is not in $[0.499n,0.501n]$ by $1/k^2$.


### The Chernoff bound

Chebyshev's inequality already shows a connection between independence and concentration, but in many cases we can hope for a quantitatively much stronger result.
If, as in the example above, $X= X_1+\ldots+X_n$ where the $X_i$'s are bounded i.i.d random variables of mean $1/2$, then as $n$ grows, the distribution of $X$ would be roughly the _normal_ or _Gaussian_ distribution$-$ that is, distributed according to the _bell curve_ (see [bellfig](){.ref} and [empiricalbellfig](){.ref}).
This distribution has the property of being _very_ concentrated in the sense that the probability of deviating $k$ standard deviations from the mean is not merely $1/k^2$ as is guaranteed by Chebyshev, but rather is roughly $e^{-k^2}$.^[Specifically, for a normal random variable $X$ of expectation $\mu$ and standard deviation $\sigma$, the probability that $|X-\mu| \geq k\sigma$ is at most $2e^{-k^2/2}$.]
That is, we have an _exponential decay_ of the probability of deviation.



![In the _normal distribution_ or the Bell curve, the probability of deviating $k$ standard deviations from the expectation shrinks _exponentially_ in $k^2$, and specifically with probability at least $1-2e^{-k^2/2}$,  a random variable $X$ of expectation $\mu$ and standard deviation $\sigma$ satisfies $\mu -k\sigma \leq X \leq \mu+k\sigma$. This figure gives more precise bounds for $k=1,2,3,4,5,6$. (Image credit:Imran Baghirov)](../figure/sixsigma.jpg){#empiricalbellfig   .margin  }


The following extremely useful theorem shows that such exponential decay occurs every time we have a sum of independent and bounded variables. This theorem is known under many names in different communities, though it is mostly called the [Chernoff bound](https://en.wikipedia.org/wiki/Chernoff_bound) in the computer science literature:



> ### {.theorem title="Chernoff/Hoeffding bound" #chernoffthm}
If $X_1,\ldots,X_n$ are i.i.d random variables such that $X_i \in [0,1]$ and $\E[X_i]=p$ for every $i$,
then for every $\epsilon >0$
$$
\Pr[ \left| \sum_{i=0}^{n-1} X_i - pn \right| > \epsilon n ] \leq 2\cdot e^{-2\epsilon^2 n} .
$$

We omit the proof, which appears in many texts, and uses Markov's inequality on i.i.d random variables $Y_0,\ldots,Y_n$ that are of the form $Y_i = e^{\lambda X_i}$ for some carefully chosen parameter $\lambda$.
See [chernoffstirlingex](){.ref}  for a proof of the    simple (but highly useful and representative) case where each $X_i$ is $\{0,1\}$ valued and $p=1/2$.
(See also [poorchernoff](){.ref} for a generalization.)

^[TODO: maybe add an example application of Chernoff. Perhaps a probabilistic method proof using Chernoff+Union bound.]

## Lecture summary

* A basic probabilistic experiment corresponds to tossing $n$ coins or choosing $x$ uniformly at random from $\{0,1\}^n$.
* _Random variables_ assign a real number to every result of a coin toss. The _expectation_ of a random variable $X$ is its average value, and there are several _concentration_ results showing that under certain conditions,  random variables deviate significantly from their expectation only with small probability.

## Exercises



> ### {.exercise }
Suppose that we toss three independent fair coins $a,b,c \in \{0,1\}$. What is the probability that the XOR of $a$,$b$, and $c$ is equal to $1$? What is the probability that the AND of these three values is equal to $1$? Are these two events independent?


> ### {.exercise }
Give an example of random variables $X,Y: \{0,1\}^3 \rightarrow \R$ such that
$\E[XY] \neq \E[X]\E[Y]$.


> ### {.exercise #noindnocorex }
Give an example of random variables $X,Y: \{0,1\}^3 \rightarrow \R$ such that $X$ and $Y$ are _not_ independent but $\E[XY] =\E[X]\E[Y]$.



> ### {.exercise title="Product of expectations" #expprodex}
Prove [expprod](){.ref}

> ### {.exercise title="Transformations preserve independence" #indeplemex}
Prove [indeplem](){.ref}


> ### {.exercise title="Variance of independent random variables" #varianceex}
Prove that if $X_0,\ldots,X_{n-1}$ are independent random variables then $\mathrm{Var}[X_0+\cdots+X_{n-1}]=\sum_{i=0}^{n-1} \mathrm{Var}[X_i]$.


> ### {.exercise title="Entropy (challenge)" #entropyex}
Recall the definition of a distribution $\mu$ over some finite set $S$.
Shannon defined the _entropy_ of a distribution $\mu$, denoted by $H(\mu)$, to be $\sum_{x\in S} \mu(x)\log(1/\mu(x))$.
The idea is that if $\mu$ is a distribution of entropy $k$, then encoding members of $\mu$ will require $k$ bits, in an amortized sense.
In this exercise we justify this definition. Let  $\mu$ be such that $H(\mu)=k$. \
1. Prove that for every one to one function $F:S \rightarrow \{0,1\}^*$, $\E_{x \sim \mu} |F(x)| \geq k$. \
2. Prove that for every $\epsilon$, there is some $n$ and a one-to-one function $F:S^n \rightarrow \{0,1\}^*$, such that $\E_{x\sim \mu^n} |F(x)| \leq n(k+\epsilon)$,
where $x \sim \mu$ denotes the experiments of choosing $x_0,\ldots,x_{n-1}$ each independently from $S$ using the distribution $\mu$.

> ### {.exercise title="Entropy approximation to binomial" #entropybinomex}
Let $H(p) = p \log(1/p)+(1-p)\log(1/(1-p))$.^[While you don't need this to solve this exercise, this is the function that maps $p$ to the entropy (as defined in [entropyex](){.ref}) of the $p$-biased coin distribution over $\{0,1\}$, which is the function $\mu:\{0,1\}\rightarrow [0,1]$ s.y. $\mu(0)=1-p$ and $\mu(1)=p$.]
Prove that for every $p \in (0,1)$ and $\epsilon>0$, if $n$ is large enough then^[__Hint:__ Use Stirling's formula for approximating the factorial function.]
$$
2^{(H(p)-\epsilon)n }\binom{n}{pn} \leq 2^{(H(p)+\epsilon)n}
$$
where $\binom{n}{k}$ is the binomial coefficient $\tfrac{n!}{k!(n-k)!}$ which is equal to the number of $k$-size subsets of $\{0,\ldots,n-1\}$.


> ### {.exercise title="Chernoff using Stirling" #chernoffstirlingex}
1. Prove that $\Pr_{x\sim \{0,1\}^n}[ \sum x_i = k ] = \binom{n}{k}2^{-n}$.\
2. Use this and [entropybinomex](){.ref} to prove the Chernoff bound for the case that $X_0,\ldots,X_n$ are i.i.d. random variables over $\{0,1\}$ each equaling $0$ and $1$ with probability $1/2$.

> ### {.exercise title="Poor man's Chernoff" #poorchernoff}
Let $X_0,\ldots,X_n$ be i.i.d random variables with $\E X_i = p$ and $\Pr [ 0 \leq X_i \leq 1 ]=1$.
Define $Y_i = X_i - p$.  \
1. Prove that for every $j_1,\ldots,j_n \in \N$, if there exists one $i$ such that $j_i$ is odd then $\E [\prod_{i=0}^{n-1} Y_i^{j_i}] = 0$. \
2. Prove that for every $k$, $\E[ (\sum_{i=0}^{n-1} Y_i)^k ] \leq (10kn)^{k/2}$.^[__Hint:__ Bound the number of tuples $j_0,\ldots,j_{n-1}$ such that every $j_i$ is even and $\sum j_i = k$.] \
3. Prove that for every $\epsilon>0$, $\Pr[ |\sum_i Y_i| \geq \epsilon n ] \geq 2^{-\epsilon^2 n / (10000\log 1/\epsilon)}$.^[__Hint:__ Set $k=2\lceil \epsilon^2 n /1000 \rceil$ and then show that if the event $|\sum Y_i | \geq \epsilon n$ happens then the random variable $(\sum Y_i)^k$ is a factor of $\epsilon^{-k}$ larger than its expectation.]



> ### {.exercise title="Simulating distributions using coins" #coindistex}
Our model for probability involves tossing $n$ coins, but sometimes algorithms require sampling from other distributions, such as selecting a uniform number in $\{0,\ldots,M-1\}$ for some $M$.
Fortunately,  we can simulate this with an exponentially small probability of error: prove that for every $M$, if $n>k\lceil \log M \rceil$, then there is a function $F:\{0,1\}^n \rightarrow \{0,\ldots,M-1\} \cup \{ \bot \}$ such that __(1)__ The probability that $F(x)=\bot$ is at most $2^{-k}$ and __(2)__ the distribution of $F(x)$ conditioned on $F(x) \neq \bot$ is equal to the uniform distribution over $\{0,\ldots,M-1\}$.^[__Hint:__ Think of $x\in \{0,1\}^n$ as choosing $k$ numbers $y_1,\ldots,y_k \in \{0,\ldots, 2^{\lceil \log M \rceil}-1 \}$. Output the first such number that is in $\{0,\ldots,M-1\}$. ]

::: {.exercise title="Sampling" #samplingex}
Suppose that a country has 300,000,000 citizens, 52 percent of which prefer the color "green" and 48 percent of which prefer the color "orange". Suppose we sample $n$ random citizens and ask them their favorite color (assume they will answer truthfully). What is the smallest value $n$ among the following choices so that the probability that the majority of the sample answers "green" is at most $0.05$?

a. 1,000

b. 10,000

c. 100,000
d. 1,000,000
:::

> ### {.exercise  #exid}
Would the answer to [samplingex](){.ref}  change if the country had 300,000,000,000 citizens?

::: {.exercise title="Sampling (2)" #exidtwo}
Under the same assumptions as [samplingex](){.ref}, what   is the smallest value $n$ among the following choices so that the probability that the majority of the sample answers "green" is at most $2^{-100}$?

a. 1,000

b. 10,000

c. 100,000

d. 1,000,000

e. It is impossible to get such low probability since there are fewer than $2^{100}$ citizens.
:::

^[TODO: add some exercise about the probabilistic method]

## Bibliographical notes
