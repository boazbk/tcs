---
title: "Computation and Representation"
filename: "lec_02_representation"
chapternum: "2"
---

# Computation and Representation {#chaprepres }

> ### { .objectives }
* _Representing_ an object as a string (often of zeroes and ones).
* Examples of representations for common objects such as numbers, vectors, lists, graphs.
* Prefix-free representations.
* Distinguish between _specification_ and _implementation_, or equivalently between _algorithms/programs_ and _mathematical functions_.


>_"The alphabet was a great invention, which enabled men to store and to learn with little effort what others had learned the hard way -- that is, to learn from books rather than from direct, possibly painful, contact with the real world."_, B.F. Skinner


>_"The name of the song is called `HADDOCK'S EYES.'"_ [said the Knight]
>
>_"Oh, that's the name of the song, is it?"_ Alice said, trying to feel interested.
>
>_"No, you don't understand,"_ the Knight said, looking a little vexed. _"That's what the name is CALLED. The name really is `THE AGED AGED MAN.' "_
>
>_"Then I ought to have said `That's what the SONG is called'?"_ Alice corrected herself.
>
>_"No, you oughtn't: that's quite another thing! The SONG is called `WAYS AND MEANS': but that's only what it's CALLED, you know!"_
>
>_"Well, what IS the song, then?"_ said Alice, who was by this time completely bewildered.
>
>_"I was coming to that,"_ the Knight said. _"The song really IS `A-SITTING ON A GATE': and the tune's my own invention."_
>
>Lewis Carroll, _Through the looking glass_
>


To a first approximation, computation can be thought of as a process that maps an _input_ to an _output_.

![Our basic notion of _computation_ is some process that maps an input to an output](../figure/input_output.png){#figureid .margin  }

When discussing computation, it is important to separate the question of  __what__ is the task we need to perform (i.e., the _specification_) from the question of __how__ we achieve this task (i.e., the _implementation_).
For example, as we've seen, there is more than one way to achieve the computational task of computing the product of two integers.

In this chapter we  focus on the **what** part, namely defining  computational tasks.
For starters, we need to define the inputs and outputs.
A priori this seems nontrivial, since computation today is applied to a huge variety  of objects.
We do not compute  merely on numbers, but also on texts, images, videos, connection graphs of social networks, MRI scans, gene data, and even other programs.
We will represent all these objects as __strings of zeroes and ones__, that is objects such as $0011101$ or $1011$ or any other finite list of $1$'s and $0$'s.

![We represent numbers, texts, images, networks and many other objects using strings of zeroes and ones. Writing the zeroes and ones themselves in green font over a black background is optional.](../figure/zeroes-ones.jpg){#figureid .margin  }

Today, we are so used to the notion of digital representation that we are not surprised by the existence of such an encoding.
Indeed, at the time of writing, the full contents of the English Wikipedia, including all the text and media, can be encoded in a string in $\{0,1\}^n$ for $n \sim 10^{12}$ (i.e., about 100 Gigabytes).
However, this is actually  a deep insight with significant implications.
Many animals can convey a particular fear or desire, but what's unique about humans is  _language_:  we use a  finite collection of basic symbols to describe a potentially unlimited range of experiences.
Language allows transmission of information over both time and space, and enables societies that span a  great many people and accumulate a body of shared knowledge over time.

Over the last several decades, we've seen a revolution in what we are able to represent and convey in digital form.
We can capture experiences with almost perfect fidelity, and disseminate it essentially instantaneously to an unlimited audience.
What's more, once information is in digital form, we can _compute_ over it, and gain insights from data that were not accessible in prior times.
At the heart of this revolution is this simple but profound observation that we can represent an unbounded variety of objects using a finite set of symbols (and in fact  using only the two symbols ```0``` and ```1```).^[There is nothing "holy" about using zero and one as the basic symbols, and we can (indeed sometimes people do) use any other finite set of two or more symbols as the fundamental "alphabet". We use zero and one in this course mainly because it simplifies notation.]

In later lectures, we will often fall back on taking this  representation for granted, and hence write something like "program $P$ takes $x$ as input" when $x$ might be a number, a vector, a graph, or any other objects,  when we really mean that $P$ takes as input the _representation_ of $x$ as a binary string.
However, in this chapter, let us dwell a little bit on how such representations can be devised.

## Defining representation

Every time we store numbers, images, sounds, data bases, in the memory of a computer, what  is actually stored is the _representation_ of these objects.
Moreover, the idea of representation is not restricted to digital computers.
When we write down text or a music sheet, we are _representing_ ideas or experiences as sequences of symbols (which might might as well be simply strings of zeroes and ones).
Even our brain does not store the actual sensory inputs we experience, but rather only our _representation_ of them.

To use objects such as numbers, images, graphs, etc. as inputs for  computation, we need to precisely define how these objects are represented as binary strings.
A _representation scheme_ is a way to map an object $x$ to a binary string $E(x) \in \{0,1\}^*$.
For example, a representation scheme for natural numbers is a function $E:\N \rightarrow \{0,1\}^*$.
Of course we can't simply represent all numbers as the string "$0011$" (for example).
A minimal requirement is that if two numbers $x$ and $x'$ are different then they would be represented by different strings.
That is, $E$ is _one to one_ (later on in this book we might need representations with additional properties, such as being easy to compute).


### Representing natural numbers.

We start with the most simple setting of a representation scheme, which is the task of representing natural numbers.
Over the years people have represented numbers in a variety of ways, including Roman numerals, the decimal system, as well as many other ways.


![Representing each one the digits $0,1,2,\ldots,9$ as a $12\times 8$ bitmap image, which can be thought of as a string in $\{0,1\}^{96}$. Using this scheme we can represent a natural number $x$ of $n$ decimal digits as a string in $\{0,1\}^{96n}$. Image taken from [blog post of A. C. Andersen](http://blog.andersen.im/2010/12/autonomous-neural-development-and-pruning/).](../figure/digitsbitmap.png){#bitmapdigitsfig .margin  }

There are great many ways to represent natural numbers as binary strings.
For example, we could represent a number $x$ by breaking it apart to its decimal digits, and represent each one as a binary string corresponding to its graphical representation (see [bitmapdigitsfig](){.ref}).
However, to fix a concrete and simple scheme, we will use as our default representation the _binary basis_.
For example, will represent the number six as the string $y=110$, which satisfies $y_0\cdot 2^{2} + y_1 \cdot 2^1 + y_2 \cdot 2^0 = 6$, and similarly we represent the number thirty-five as the string $y'= 100011$ which satisfies $\sum_{i=0}^5 y_i \cdot 2^{|y|-i} = 35$.^[We could have equally well reversed the order so as to represent $35$ by the string $y=110001$ satisfying $\sum_i y_i\cdot 2^i = 35$. Such low level choices will not make a difference in this course.
A related, but not identical, distinction is the [Big Endian vs Little Endian](https://betterexplained.com/articles/understanding-big-and-little-endian-byte-order/) representation for integers in computing architectures.]

| **Number (decimal representation)** | **Number (binary representation)** |
|-------------------------------------|------------------------------------|
| 503                                 | 111110111                          |
| 53                                  | 110101                             |
| 40                                  | 101000                             |
| 16                                  | 10000                              |
| 40                                  | 101000                             |
| 801                                 | 1100100001                         |
| 111                                 | 1101111                            |
| 389                                 | 110000101                          |
| 3750                                | 111010100110                       |
| 506                                 | 111111010                          |

Table: Representing numbers in the binary basis. The lefthand column contains representations of natural numbers in the decimal basis, while the righthand column contains representations of the same numbers in the binary basis. Note that in both representations the leftmost (i.e., most significant) digit is never equal to zero (unless we represent the natural number zero).

Formally,  our representation is given by the following theorem:

> ### {.theorem title="Binary representation of natural numbers" #binaryrepthm}
There exists a one-to-one function $NtS:\N \rightarrow \{0,1\}^*$.^[$NtS$ stands for "numbers to strings".]

> ### {.proofidea data-ref="binaryrepthm"}
We use the standard binary representation mentioned above. If you find the proof below confusing, there are many sources online which describe this representation fully with examples.

::: {.proof data-ref="binaryrepthm"}
If $x$ is even then the least significant binary digit of $x$ is zero, while if $x$ is odd then the least significant binary digit is one.
In either case, $\floor{x/2}$ corresponds to the number obtained when we "chop off" the least significant digit.
Hence we can define  $NtS$ recursively as follows:

$$NtS(x) = \begin{cases}
            \text{""}    &  x=0 \\
            NTS(\floor{x/2}) parity(x) & x>0
\end{cases}$$
where $parity(x)$ is defined to equal $1$ if $x$ is odd and to equal $0$ if $x$ is even. (The function $NtS$ is well defined since for every $x>0$, $\floor{x/2} < x$.)
If $\alpha$ and $\beta$ are two strings, then $\alpha\beta$ corresponds to the string obtained by _concatenating_ $\alpha$ and $\beta$ (that is, the string $\gamma$ of length $|\alpha|+|\beta|$ obtained by writing $\alpha$ first and then writing $\beta$).
Thus in the definition above $NTS(\floor{x/2}) parity(x)$ corresponds to the _concetenation_ of the string $NTS(\floor{x/2})$ with the (one bit long) string $parity(x)$.

It can be shown (though we omit the proof since it is slightly tedious, and  can be easily found in many online resources) that if $y = NtS(x)$ then $x = \sum_{i=0}^n y_i \cdot 2^{n-i}$ where $n=|y|-1$.
In particular this gives a way to recover (or _decode_) the original  $x$ from the output $y=NtS(x)$ which means that $NtS$ is one to one.

The above representation uses the empty string $\text{""}$ to represent the number $0$. However, we can also represent this number using the string $0$ as well. This choice will not make any difference for our purposes.
:::

### Implementing the representation in python:

In the _Python_ programming language, we can compute the above encoding and decoding functions as follows:



```python
from math import floor, log
def NtS(x):
    if x<1: return ""
    return NtS(floor(x/2))+str(x % 2)

print(NtS(236))
# 11101100

print(int2bits(19))
# 10011

def StN(y):
    x = 0
    n = len(y)-1
    for i in range(n+1):
        x += int(y[i])*(2**(n-i))
    return x

print(StN(NtS(246)))
# 236
```


We can also implement  $NtS$ non recursively as follows:

```python
def NtS(x):
    def list2string(L): return "".join([str(e) for e in L])
    n = floor(log2(x))  # largest power of two smaller than x
    return list2string([ floor(x / 2**(n-i)) % 2 for i in range(n+1)])
```

::: {.remark title="Programming examples" #programmingrem}
In this book, we will often illustrate our points by using programming languages  to
present certain computations.
Our examples will be fairly short, and our point will always be to emphasize that certain computations can be done concretely,
rather than focus on a particular language feature.
We often use Python, but that choice is rather arbitrary.
Indeed, one of the messages of this course is that all programming language are in some sense _equivalent_ to one another, and hence we could have just as well used JavaScript, C, COBOL, Visual Basic or even [BrainF*ck](https://goo.gl/LKKNFK).

This is _not_ a programming course, and it is absolutely fine if you are not familiar with Python and don't follow the fine points of code  examples such as the above.
Still you might find it instructive to try to parse them, with the help of websites such as Google or Stackoverflow.
In particular, the non-recursive implementation of the function `NtS` above uses the fact that the  binary representation of a natural number $x$ is the list  $(\floor{\tfrac{x}{2^i}} \mod 2)_{i=0,\ldots,\floor{\log_2 x}}$, which in Python-speak is written as `[ floor(x / 2**i ) % 2 for i in range(floor(log2(x))+1)]`.
:::



### Meaning of representation

It is natural for us to think of $236$ as a the "actual" number, and of $11101100$ as "merely" its representation.
However, for most Europeans in the middle ages `CCXXXVI` would be the "actual" number and $236$ (if they have even heard about it) would be the weird Hindu-Arabic positional representation.^[While the Babylonians already invented a positional system much earlier, the decimal  positional system we use today was invented by Indian mathematicians around the third century. It was taken up by Arab mathematicians in the 8th century. It was mainly introduced to Europe in the 1202 book _"Liber Abaci"_ by  Leonardo of Pisa, also known as Fibonacci, but did not displace Roman numerals in common usage until the 15th century.]
When our AI robot overlords materialize, they will probably think of $11101100$ as the "actual" number and of $236$ as "merely" a representation that they need to use when they give commands to humans.

So what is the "actual" number? This is a question that philosophers of mathematics have pondered over the generations.
Plato argued that mathematical objects exist in some ideal sphere of existence (that to a certain extent is more "real" than the world we perceive via our senses, as this latter world is  merely the shadow of this ideal sphere).
Thus in Plato's vision  the symbols $236$ are merely notation for some ideal object, that, in homage to the [late musician](https://goo.gl/b93h83), we can refer to as  "the number commonly represented by $236$".

The Austrian philosopher Ludwig Wittgenstein, on the other hand, argued that mathematical objects don't exist at all, and the only thing that exists are the actual splotches on paper that make up $236$, $00110111$ or `CCXXXVI`.
In Wittgenstein's view mathematics is merely about formal manipulation of symbols that don't have any inherent meaning.
You can  think of the "actual" number as (somewhat recursively) "that thing which is common to $236$, $00110111$  and `CCXXXVI` and all other past and future representations that are meant to capture the same object".
(Some mathematicians would say that the actual number can be thought of as an _equivalence class_ of these representations.)

You are free to choose your own philosophy of mathematics, as long as you maintain the distinction between the mathematical objects themselves and the particular choice of representing them, whether as splotches of ink, pixels on a screen, zeroes and one, or any other form.

## Representing more objects

We now discuss how we can represent many other objects as strings, going far beyond natural numbers.
In many instances, choosing the "right" string representation for a piece of data is highly nontrivial, and finding the "best" one (e.g., most compact, best fidelity,  most efficiently manipulable, robust to errors, most informative features, etc..) is the object of intense research.
But for now, we focus on presenting some simple representations for various objects that we would like to use as inputs and outputs for computation.


### Representing (potentially negative) integers

Now that we can represent natural numbers, we can represent the full set of _integers_ (i.e., members of the set $\Z=\{ \ldots, -3 , -2 , -1 , 0 , +1, +2, +3,\ldots \}$ ) by adding one more bit that represents the sign.
If $x\in \Z$, then we can represent it by the string $NtS(|x|)\sigma$ where $\sigma$ equals to $0$ is $x \geq 0$ and $\sigma$ equals to $1$ if $x<0$.

Thus the string $y \in \{0,1\}^*$ will represent the number
$$
x = (-1)^{y_{n+1}} \left(  \sum_{i=0}^{n-1} y_i \cdot 2^{n-i}\right)
$$
where $n=|y|-2$.
Formally, the above can be shown to give a one to one function $ZtS:\Z \rightarrow \{0,1\}^*$ that maps the integers into strings.


The decoding function of a representation should always be _onto_, since every object must be represented by some string.
However, it does not always have to be one to one.
For example, in this particular representation the two strings $1$ and $0$ both represent the number zero (since they can be thought of as representing $-0$ and $+0$ respectively, can you see why?).
We can also allow a _partial_ decoding function for representations.
For example,   in the representation above there is no number that is represented by the empty string.
But this is still a fine representation, since the decoding partial function is onto and the encoding function is the one-to-one total function $E:\Z \rightarrow \{0,1\}^*$ which maps an integer of the form $a\times k$, where $a\in \{\pm 1 \}$ and $k\in \N$ to the bit $(-1)^a$ concatenated with  the binary representation of $k$.
That is, every integer can be represented as a string, and every two distinct integers have distinct representations.


> ### {.remark title="Interpretation and context" #contextreprem}
Given a string $y\in \{0,1\}^*$, how do we know if it's "supposed" to represent a (nonnegative) natural number  or a (potentially negative) integer?
For that matter, even if we know $y$ is "supposed" to be an integer, how do we know what representation scheme it uses?
The short answer is that we don't necessarily know this information, unless it is supplied from the context.^[In  programming language, the compiler or interpreter determines the representation of the sequence of bits corresponding to a variable based on the variable's _type_.]
We can treat the same string $y$ as representing a natural number, an integer, a piece of text, an image, or a green gremlin.
Whenever we say a sentence such as "let $n$ be the number represented by the string $y$", we will assume that we are fixing some canonical representation scheme such as the ones above.
The choice of the particular representation scheme will almost never matter, except that we want to make sure to stick with the same one for consistency.

### Representing rational numbers

We can represent a rational number of the form $a/b$ by representing the two numbers $a$ and $b$ (again, this is not a unique representation but this is fine).
However, simply concatenating the representations of $a$ and $b$ will not work.^[Recall that the _concatenation_ of two strings $x$ and $y$ is  the string of length $|x|+|y|$ obtained by writing $y$ after $x$.]
For example, recall that we represent $4$ as $100$ and  $43$ as $101011$, but the concatenation  $100101011$ of these strings is also the concatenation of the representation $10010$ of $18$ and the representation $1011$ of $11$.
Hence, if we used such simple concatenation then we would not be able to tell if the string $100101011$ is supposed to represent $4/43$ or  $18/11$.^[The above assumes we use the simple binary representation of natural numbers as strings. If we want to handle negative numbers then we should add the sign bit as well, though it would not make any qualitative difference to this discussion.]

The way to tackle this is to find a general representation for _pairs_ of numbers.
If we were using a pen and paper, we would simply use a separator such as the  symbol $\|$ to represent, for example, the pair consisting of the numbers represented by $(0,1)$ and $(1,1,0,0,0,1)$ as the length-$9$ string $s$ "$01\|110001$".
This is just like people add spaces and punctuation to separate words in English.
By adding a little redundancy, we can do just that in the digital domain.
The idea is that we can map the three element set $\Sigma = \{0,1,\|\}$  to the four element set $\{0,1\}^2$ via the one-to-one map that takes $0$ to $00$, $1$ to $11$ and $\|$ to $01$.

::: {.example title="Representing a rational number as a string" #represnumberbypairs}
Consider the rational number $r=19/236$. In our convention, we represent $19$ as the string $10011$ and $236$ as the string $11101100$, and so we could represent $r$ as the _pair_ of strings $(10011,11101100)$.
We can then represent this pair as the length $14$ string $10011\|11101100$ over the alphabet $\{0,1,\|\}$.
Now, applying the map $0 \mapsto 00$, $1\mapsto 11$, $\| \mapsto 01$, we can represent the latter string as the length $28$ string  $s=1100001111011111110011110000$ over the alphabet $\{0,1\}$.
So we represent the rational number $r=19/36$ be the binary string $s=1100001111011111110011110000$.
:::


More generally, we obtained a representation of the non-negative rational numbers as binary strings by composing the following representations:

1. Representing a non-negative rational number as a pair of natural numbers.

2. Representing a natural number by a string via the binary representation. (We can use the representation of integers to handle rational numbers that can be negative. )

3. Combining 1 and 2 to obtain representation of a rational number as a pair of strings.

4. Representing a pair of strings over $\{0,1\}$ as a single string over $\Sigma = \{0,1,\|\}$.

5. Representing a string over $\Sigma$ as a longer string over $\{0,1\}$.


The same idea can be used to represent triples, quadruples, and generally all tuples of strings as a single string (can you see why?).
Indeed, this is one instance of a very general principle that we use time and again in both the theory and practice of computer science (for example, in Object Oriented programming):



::: { .bigidea #representtuplesidea }
If we can represent objects of type T as strings, then we can also represent more complex objects built out of T as strings (such as pairs or lists of elements in T, nested lists and so on and so forth).
:::

We will come back to this point when we discuss  _prefix free encoding_ in [prefixfreesec](){.ref}.

## Representing real numbers

The set of  _real numbers_ $\R$ contains all numbers including positive, negative, and fractional, as well as _irrational_ numbers such as $\pi$ or $e$.
Every real number can be approximated by a rational number, and so up to a small error we can represent every real number $x$ by a rational number $a/b$ that is very close to $x$.
For example, we can represent $\pi$ by $22/7$ with an  error of about $10^{-3}$ and if we wanted smaller error (e.g., about $10^{-4}$) then we can use $311/99$ and so on and so forth.


The above representation of real numbers via rational numbers that approximate them is a fine choice of a representation.
However, typically in computing it is more common to use the _floating point representation scheme_   to represent real numbers.
In the floating point representation scheme we represent $x$ by the pair $(a,b)$ of (positive or negative) integers of some prescribed sizes (determined by the desired accuracy) such that $a \times 2^{b}$ is closest to $x$.^[The floating point representation is the base-two version of  [scientific notation](https://goo.gl/MUJnVE). In scientific notation we represent a number $y$ as $a \times 10^b$ for  $a,b$.
Often this is written as  $y=a \text{\texttt{E}} b$. For example, in many programming languages `1.21E2` is the same as `121.0`.]


The reader might be (rightly) worried about this issue of approximation. In many (though not all) computational applications, one can make the accuracy tight enough so that this does not affect the final result, though sometimes we do need to be careful.
This representation is called "floating point" because we can think of the number $a$ as specifying a sequence of binary digits, and $b$ as describing the location of the "binary point" within this sequence.
The use of floating  representation is the reason why in many programming systems  printing the expression `0.1+0.2` will result in `0.30000000000000004` and not `0.3`, see [here](http://floating-point-gui.de/), [here](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) and [here](https://randomascii.wordpress.com/2012/04/05/floating-point-complexities/) for more (see also [xkcdfloatingfig](){.ref}).

![XKCD cartoon on floating-point arithmetic.](../figure/e_to_the_pi_minus_pi.png){#xkcdfloatingfig .margin  }


Floating-point bugs can sometimes be no joking matter.
A floating point error  has been implicated in the [explosion](http://sunnyday.mit.edu/accidents/Ariane5accidentreport.html) of the Ariane 5 rocket, a bug that cost more than 370 million dollars, and the [failure](http://embeddedgurus.com/barr-code/2014/03/lethal-software-defects-patriot-missile-failure/) of a U.S. Patriot missile to intercept an Iraqi Scud missile, costing 28 lives.
Floating point is [often problematic](http://www.theregister.co.uk/2006/08/12/floating_point_approximation/) in financial applications as well.




### Can we represent reals _exactly_? {#cantorsec }

Given the issues with floating point representation, we could ask whether we could represent real numbers _exactly_ as strings.
Unfortunately, the following theorem shows that this cannot be done:

> ### {.theorem title="Reals are uncountable" #cantorthm}
There is no one-to-one function $RtS:\R \rightarrow \{0,1\}^*$.^[$RtS$ stands for "reals to strings".]

[cantorthm](){.ref} was proven by [Georg Cantor](https://en.wikipedia.org/wiki/Georg_Cantor) in 1874.^[Cantor used the set $\N$ rather than $\{0,1\}^*$, but one can show that these two result are equivalent using the one-to-one maps between those two sets, see [naturalsstringsmapex](){.ref}. Saying that there is no one-to-one map from $\R$ to $\N$ is equivalent to saying that there is no onto map $NtR:\N \rightarrow \R$ or, in other words, that there is no way to "count" all the real numbers as $NtR(0),NtR(1),NtR(2),\ldots$. For this reason [cantorthm](){.ref} is known as the _uncountability of the reals_.]
This result (and the theory around it) was quite shocking to mathematicians at the time.
By showing that there is no one-to-one map from $\R$ to $\{0,1\}^*$ (or $\N$), Cantor showed that these two infinite sets have "different forms of infinity" and that the set of real numbers $\R$ is in some sense "bigger"  than the infinite set $\{0,1\}^*$.
The notion that there are "shades of infinity" was deeply disturbing to mathematicians and philosophers at the time.
The philosopher Ludwig Wittgenstein (whom we mentioned before) called Cantor's results "utter nonsense" and "laughable".
Others thought they were even worse than that.
Leopold Kronecker called Cantor a "corrupter of youth", while Henri Poincaré said that Cantor's ideas "should be banished from mathematics once and for all".
The tide eventually turned, and these days Cantor's work is universally accepted as the cornerstone of set theory and the foundations of mathematics.
As David Hilbert said in 1925, _"No one shall expel us from the paradise which Cantor has created for us."_
As we will see later in this book, Cantor's ideas also play a huge role in the theory of computation.

Now that we discussed the theorem's importance, let us see the proof.
The idea behind the proof is to do the following::

1. Define some infinite set $\mathcal{X}$ for which it is easier for us to prove that $\mathcal{X}$ is not countable: that is there is no one-to-one function from  $\mathcal{X}$ to $\{0,1\}^*$.

2. Prove that there _is_ a one-to-one function $G$ mapping $\mathcal{X}$ to $\mathbb{R}$.

These two facts together imply Cantor's Theorem. The reason is using a "proof by contradiction". If we assume (towards the sake of contradiction) that there exists some one-to-one $F$ mapping $\mathbb{R}$ to $\{0,1\}^*$
then the function $x \mapsto F(G(x))$ obtained by composing $F$ with the function $G$ from Step 2 above would be a  one-to-one function from $\mathcal{X}$ to $\{0,1\}^*$, which contradicts what we proved in Step 1!

To turn this idea into a proof of [cantorthm](){.ref} we need to:

* Define the set $\mathcal{X}$.

* Prove that there is no one-to-one function from $\mathcal{X}$ to $\{0,1\}^*$

* Prove that there _is_ a one-to-one function from $\mathcal{X}$ to $\R$.

We now proceed to do exactly that. Namely, we will give a definition for a set and two lemmas that show that this set satisfies the two properties we desire.

> ### { .definition title = "The set $\{0,1\}^\infty$" }
We define $\{0,1\}^\infty$ to be the set  $\{ f \;|\; f:\N \rightarrow \{0,1\} \}$.

That is, $\{0,1\}^\infty$ is a set of _functions_, and a function $f$ is in $\{0,1\}^infty$ iff its domain is $\N$ and its codomain is $\{0,1\}$.^[We can also think of $\{0,1\}^\infty$ as the set of all infinite _sequences_ of bits, since a function $f:\N \rightarrow \{0,1\}$ can be identified with the sequence $(f(0),f(1),f(2),\ldots )$.]
The set $\{0,1\}^\infty$ will play the role of $\mathcal{X}$ above.
Namely, we will prove the following two results about it:

> ### {.lemma #sequencestostrings}
There does not exist a  one-to-one map $FtS:\{0,1\}^\infty \rightarrow \{0,1\}^*$.^[$FtS$ stands for "functions to strings".]

> ### {.lemma #sequencestoreals}
There _does_ exist a one-to-one map $FtR:\{0,1\}^\infty \rightarrow \R$.^[$FtR$ stands for "functions to reals."]

As we've seen above, [sequencestostrings](){.ref} and [sequencestoreals](){.ref} together  imply [cantorthm](){.ref}.
To repeat the argument more formally, suppose, for the sake of contradiction, that there did exist a one-to-one function $RtS:\R \rightarrow \{0,1\}^*$.
By [sequencestoreals](){.ref}, there exists a one-to-one function $FtR:\{0,1\}^\infty \rightarrow \R$.
Thus, under this assumption, since the composition of two one-to-one functions is one-to-one (see [onetoonecompex](){.ref}), the function $FtS:\{0,1\}^\infty \rightarrow \{0,1\}^*$ defined as $FtS(f)=RtS(FtR(f))$ will be one to one, contradicting [sequencestostrings](){.ref}.
See [proofofcantorfig](){.ref} for a graphical illustration of this argument.

![We prove [cantorthm](){.ref} by combining [sequencestostrings](){.ref} and [sequencestoreals](){.ref}.  [sequencestoreals](){.ref}, which uses standard calculus tools, shows the existence of a one-to-one map $FtR$ from the set $\{0,1\}^\infty$ to the real numbers. So, if a hypothetical one-to-one map $RtS:\R \rightarrow \{0,1\}^*$ existed, then we could compose them to get a one-to-one map $FtS:\{0,1\}^\infty \rightarrow \{0,1\}^*$. Yet this contradicts [sequencestostrings](){.ref}- the heart of the proof- which rules out the existence of such a map.](../figure/proofofcantor.png){#proofofcantorfig .margin  }

Now all that is left is to prove these two lemmas.
We start by proving  [sequencestostrings](){.ref} which is really the heart of [cantorthm](){.ref}.

::: {.proof data-ref="sequencestoreals"}
We will prove that there does not exist an _onto_ function $StF:\{0,1\}^* \rightarrow \{0,1\}^\infty$.
This will imply the lemma since for every two sets $A$ and $B$, there exists an onto function from $A$ to $B$ if and only if there exists a one-to-one function from $B$ to $A$  (see [onetooneimpliesonto](){.ref}).



Let $StF:\{0,1\}^* \rightarrow \{0,1\}^\infty$ be any function mapping $\{0,1\}^*$ to $\{0,1\}^\infty$.
We will prove tha $StF$ is _not_ onto by showing that there exists some $f^* \in \{0,1\}^\infty$ that is _not_ in the image of the function $StF$.
Namely, $StF(x) \neq f^*$ for every $x\in \{0,1\}^*$.


The construction of $f^*$ is short but subtle.
For every number $n\in \N$, we let $x(n)$ be the string obtained by representing $n$ in the binary basis and "chopping off" its  most significant digit.
We define $f^*(n)$ as follows:
$$
f^*(n) = 1 - StF(x(n))(n) \label{eqcantordiagreals}
$$

As computer scientists, let's first verify that [eqcantordiagreals](){.eqref}  "type checks".
First of all, $f^*$ is a member of  $\{0,1\}^\infty$ and so for every $n\in \N$, $f^*(n)$ should be a bit in $\{0,1\}$, and so for [eqcantordiagreals](){.eqref} to "type check" we need its right-hand side to also be a bit.
For every $n$, $x(n)$ is a string in $\{0,1\}^*$ and so $StF(x(n))$ is a function $g\in \{0,1\}^infty$.
If we apply the function $g=StF(x(n))$ to $n$ we get a bit $b \in \{0,1\}$ and so $1-b$ is indeed also a bit as we needed it to be.

Now we want to prove that for every $x\in \{0,1\}^*$, $StF(x) \neq f^*$. Indeed, suppose (towards a contradiction) that there did exist some $x\in \{0,1\}^*$ such that 
$$StF(x) = f^* \label{eqcantordiagrealstwo} \;.$$

Then, if we let $n$ be the number whose binary representation is $1x$, we see that one the one hand by [eqcantordiagrealstwo](){.eqref} $f^*(n)=StF(x)(n)$ but on the other hand (since $x(n)=x$) by [eqcantordiagreals](){.eqref}
$$
f^*(n) = 1 - StF(x)(n) \;.
$$
We obtained that $f^*(n)$ is equal to both $StF(x)(n)$ and to one minus the same quantity which is clearly a contradiction!
:::

::: {.pause}
The proof of [sequencestoreals](){.ref} is rather subtle, and worth re-reading a second or third time.
It is known as the "diagonal" argument, as the construction of $f^*$  can be thought of as going over the diagonal elements of a table that in the $n$-th row and $m$-column contains $StF(x)(m)$ where $x$ is the string such that $n(x)=n$, see [diagrealsfig](){.ref}.
We will use  the diagonal argument again several times later on in this book.
:::

![We construct a function $f^*$ such that $f^* \neq StF(x)$ for every $x\in \{0,1\}^*$ by ensuring that $f^*(n(x)) \neq StF(x)(n(x))$ for every $x\in \{0,1\}^*$. We can think of this as building a table where the columns correspond to numbers $m\in \N$ and the rows correspond to $x\in \{0,1\}^*$ (sorted according to $n(x)$). If the entry in the $x$-th row and the $m$-th column corresponds to $g(m))$ where $g=StF(x)$ then $f^*$ is obtained by going over the "diagonal" elements in this table (the entries corresponding to the $x$-th row  and $n(x)$-th column) and enduring that $f^*(x)(n(x)) \neq StF(x)(n(x))$. ](../figure/diagreals2.png){#diagrealsfig .margin  }


::: {.remark title="Generalizing beyond strings and reals" #generalizepowerset}
[sequencestostrings](){.ref} doesn't really have much to do with the natural numbers or the strings.
An examination of the proof shows that it really shows that for _every_ set $S$, there is no one-to-one map $F:\{0,1\}^S \rightarrow S$ where $\{0,1\}^S$ denotes the set $\{ f \;|\; f:S \rightarrow \{0,1\} \}$ of all Boolean functions with domain $S$.
Since we can identify a subset $V \subseteq S$ with its characteristic function $f=1_V$ (i.e., $1_V(x)=1$ iff $x\in V$), we can think of $\{0,1\}^S$ also as the set of all _subsets_ of $S$.
This subset is sometimes called the _power set_ of $S$.

The proof of [sequencestostrings](){.ref} can be generalized to show that there is no one-to-one map between a set and its power set.
In particular, it means that the set $\{0,1\}^\R$ is "even bigger" than $\R$.
Cantor used these ideas to construct an infinite hierarchy of shades of infinity.
The number of such shades turn out to be much larger than $|\N|$ or even $|\R|$.
He denoted the cardinality of $\N$ by  $\aleph_0$, where $\aleph$ is the first letter in the Hebrew alphabet, and called the the next largest infinite number by $\aleph_1$.
Cantor also made the [continuum hypothesis](https://en.wikipedia.org/wiki/Continuum_hypothesis) that $|\R|=\aleph_1$.
We will come back to the very interesting story of this hypothesis later on in this book.
[This lecture of Aaronson](https://www.scottaaronson.com/democritus/lec2.html) mentions some of these issues (see also [this Berkeley CS 70 lecture](http://www.eecs70.org/static/notes/n10.pdf)).
:::






To complete the proof of [cantorthm](){.ref}, we need to show [sequencestoreals](){.ref}.
This requires some calculus background, but is otherwise straightforward.
The idea is that we can construct a one-to-one map from $\{0,1\}^\infty$ to the real numbers by mapping the function $f:\N \rightarrow \{0,1\}$ to the number that has the infinite decimal expansion $f(0).f(1)f(2)f(3)f(4)f(5)\ldots$ (i.e., the number between $0$ and $2$ that is $\sum_{i=0}^\infty f(i)10^{-i}$).
We will now do this  more formally.
If you have not had much experience with limits of a real series before, then the formal proof below might be a little hard to follow.
This part is not the core of Cantor's argument, nor are such limits important to the remainder of this book, so feel free to also just take [sequencestoreals](){.ref} on faith and skip the proof.


::: {.proofidea data-ref="sequencestoreals"}
As discussed above, we define $FtR(f)$ to be the number between $0$ and $2$ whose decimal expansion is $f(0).f(1) f(2) \ldots$, or in other words  $FtR(f) = \sum_{i=0}^{\infty} f(i) \cdot 10^{-i}$. 
To prove that $FtR$ is one to one, we need to show that if $f \neq g$ then $FtR(f) \neq FtR(g)$.
To do that we let $k\in \N$ be the first input on which $f$ and $g$ disagree.
Then the numbers $FtR(f)$ and $FtR(g)$ agree in the first $k-2$ digits following the decimal point and disagree in the $k-1$-th digit. One can then calculate and verify that this means that $|FtR(f)-FtR(g)| > 0.5 \cdot 10^{-k}$ which in particular means that these two numbers are distinct from one another.^[You could wonder why we don't deduce automatically that two numbers that differ in a digit are not the same. The issue is that we have to be a little more careful when talking about infinite expansions. For example the number half has two decimal expansions $0.5$ and $0.49999\cdots$. However, this issue does not come up if (as in our case) we restrict attention only to numbers with decimal expansions that do not involve the digit $9$.]
:::

::: {.proof data-ref="sequencestoreals"}
For every $f\in \{0,1\}^\infty$ and $n\in \N$, we define $S(f)_n = \sum_{i=0}^n f(i)10^{-i}$.
It is a known result in calculus (whose proof  we won't repeat here) that for every $f:\N \rightarrow \{0,1\}$, the sequence $( S(f)_n )_{n=0}^\infty$ has a _limit_.
In other words, for every $f$ there is a value $\alpha(f) \in \R$ such that for every $\epsilon>0$, if $n$ is sufficiently large then $|S(f)_n - \alpha|<\epsilon$.
The value $\alpha(f)$ is denoted by $\sum_{i=0}^\infty f(i) \cdot 10^{-i}$.
We define the function $FtR$ by setting $FtR(f) = \alpha(f)$. 


We define $FtR(f)$ to be this value $x(f)$.
In other words, we define
$$
FtR(f) = \sum_{i=0}^\infty f(i)\cdot 10^{-i}
$$
which will be a number between $0$ and $2$.

To show that $FtR$ is one to one, we need to show that $FtR(f) \neq FtR(g)$ for every distinct $f,g:\N \rightarrow \{0,1\}$.
Let $f \neq g$ be such functions.
Since $f$ and $g$ are distinct, there must be some input on which they differ, we define $k$ to be the smallest such input.
That is, $k\in \N$ is the smallest number for which $f(k) \neq g(k)$.
We will show that $|FtR(f)-FtR(g)| > 0.5\cdot 10^{-k}$.
This will complete the proof since  in particular it implies that  $FtR(f) \neq FtR(g)$.

Since $f(k) \neq g(k)$, we can assume without loss of generality that $f(k)=0$ and $g(k)=1$ (otherwise, if $f(k)=1$ and $g(k)=1$, then we can simply switch the roles of $f$ and $g$).
Define  $S = \sum_{i=0}^{k-1} 10^{-i}f(i) = \sum_{i=0}^{k-1} 10^{-i}g(i)$ (the equality holds since $f$ and $g$ agree up to $k-1$).
Now, since $g(k)=1$,
$$FtR(g) = \sum_{i=0}^\infty g(i)10^{-i} \geq \sum_{i=0}^k g(i)10^{-i} = S + 10^{-k} \;.$$

On the other hand, since $f(k)=0$ and $f(k+1+j) \leq 1$ for every $j\geq 0$,
$$FtR(f) = \sum_{i=0}^\infty f(i)10^{-i} = S + \sum_{i=k+1}^\infty f(i) 10^{-i} \leq S + 10^{-(k-1)}\sum_{j=0}^\infty 10^{-j}\;.$$

Now $\sum_{j=0}^\infty 10^{-j}$ is simply the number $1.11111\ldots =  11/9$, and hence we get that
$$
FtR(f) \leq S + 11/9 \cdot 10^{-k-1} = S + \tfrac{11}{90} \cdot 10^{-k} < S + 0.2 \cdot 10^{-k}
$$
while $FtR(g) \geq S + 10^{-k}$ which means the difference between them is larger than $0.5 \cdot 10^{-k}$.
:::




## Beyond numbers

We can of course represent objects other than numbers as binary strings.
Let us give a general definition for a  _representation scheme_.
Such a scheme for representing objects from some set $\mathcal{O}$ consists of an _encoding_ function that maps an object in $\mathcal{O}$ to a string, and a _decoding_ function that decodes a string back to an object in $\mathcal{O}$.
Formally, we make the following definition:

> ### {.definition title="String representation" #binaryrepdef}
Let $\mathcal{O}$ be some set. A _representation scheme_ for $\mathcal{O}$ is a pair of functions $E,D$  where  $E:\mathcal{O} \rightarrow \{0,1\}^*$ is a total one-to-one function, $D:\{0,1\}^* \rightarrow_p \mathcal{O}$ is a (possibly partial)  function,
and such that  $D$ and $E$ satisfy that $D(E(o))=o$ for every $o\in \mathcal{O}$.
$E$ is known as the _encoding_ function and $D$ is known as the _decoding_ function.

Note that the condition $D(E(o))=o$ for every $o\in\mathcal{O}$ implies that $D$ is _onto_ (can you see why?).
It turns out that to construct a representation scheme we only need to find an _encoding_ function.
That is, every one-to-one encoding function has a corresponding decoding function, as shown in the following lemma:

> ### {.lemma #decodelem}
Suppose that $E: \mathcal{O} \rightarrow \{0,1\}^*$ is one-to-one. Then there exists a function $D:\{0,1\}^* \rightarrow \mathcal{O}$ such that $D(E(o))=o$ for every $o\in \mathcal{O}$.

> ### {.proof data-ref="decodelem"}
Let $o_0$ be some arbitrary element of $O$.
For every $x \in \{0,1\}^*$, there exists either zero or a single $o\in \mathcal{O}$ such that $E(o)=x$ (otherwise $E$ would not be one-to-one).
We will define $D(x)$ to equal $o_0$ in the first case and this single object $o$ in the second case.
By definition $D(E(o))=o$ for every $o\in \mathcal{O}$.


Note that, while in general we allowed the decoding function to be _partial_.
This proof shows that we can always obtain a _total_ decoding function if we need to.
This observation can sometimes be useful.

### Finite representations

If $\mathcal{O}$ is _finite_, then we can represent every object in $o$ as a string of length at most some number $n$.
What is the value of $n$?
Let us denote by  $\{0,1\}^{\leq n}$ the set $\{ x\in \{0,1\}^* : |x| \leq n \}$ of strings of length at most $n$.
The size of $\{0,1\}^{\leq n}$ is equal to
$$
|\{0,1\}^0| + |\{0,1\}^1| + |\{0,1\}^2| + \cdots + |\{0,1\}^n| = \sum_{i=0}^n 2^i = 2^{n+1}-1 \;.
$$
using the standard formula for summing a [geometric progression](https://en.wikipedia.org/wiki/Geometric_progression).

To obtain a representation of objects in $\mathcal{O}$ as strings of length at most $n$ we need to come up with a one-to-one function from $\mathcal{O}$ to $\{0,1\}^{\leq n}$.
We can do so, if and only if $|\mathcal{O}| \leq 2^{n+1}-1$ as is implied by the following lemma:

> ### {.lemma #onetoone}
For every two finite sets $S,T$, there exists a one-to-one $E:S \rightarrow T$ if and only if $|S| \leq |T|$.

> ### {.proof data-ref="onetoone"}
Let $k=|S|$ and $m=|T|$ and so write the elements of $S$ and $T$ as $S = \{ s_0 , s_1, \ldots, s_{k-1} \}$ and $T= \{ t_0 , t_1, \ldots, t_{m-1} \}$. We need to show that there is a one-to-one function $E: S \rightarrow T$ iff $k \leq m$.
For the "if" direction, if $k \leq m$ we can simply define $E(s_i)=t_i$ for every $i\in [k]$.
Clearly for $i \neq j$, $t_i = E(s_i) \neq E(s_j) = t_j$, and hence this function is one-to-one.
In the other direction, suppose that $k>m$ and  $E: S \rightarrow T$ is some function. Then $E$ cannot be one-to-one.
Indeed, for $i=0,1,\ldots,m-1$ let us "mark" the element $t_j=E(s_i)$ in $T$. If $t_j$ was marked before, then we have found two objects in $S$ mapping to the same element $t_j$. Otherwise, since $T$ has $m$ elements,  when we get to $i=m-1$ we mark all the objects in $T$. Hence, in this case $E(s_m)$ must map to an element that was already marked before.^[This direction is sometimes known as the "Pigeon Hole Principle": the principle that if you have a pigeon coop with $m$ holes, and $k>m$ pigeons, then there must be two pigeons in the same hole. ]


### Prefix-free encoding { #prefixfreesec }

In our discussion of the representation of rational numbers, we used the "hack" of encoding the alphabet $\{ 0,1, \|\}$  to represent tuples of strings as a single string.
This turns out to be a special case of the  general paradigm of _prefix-free_ encoding.
The idea is the following: if we have a representation of objects in $\mathcal{O}$ such that it will never be the case that the string representing some object $o$ is the _prefix_ (i.e., an initial substring) of the string that represents an object $o'$, then we can also represent _lists_ of objects in $\mathcal{O}$ by simply concatenating the representation of all the list members.
For example, because in English every sentence ends with a punctuation mark such as a period, exclamation, or question mark, we can represent a list of sentences (i.e., a paragraph) by simply concatenating the sentences one after the other.

It turns out that we can always transform a representation to a prefix-free form.
This provides a justification for [representtuplesidea](){.ref}, and allows us to transform a representation for objects of a certain type to a representation of _lists_ of objects of the same type.
By using this idea again, we can even represent lists of lists and so on and so forth.
But first let us formally define prefix-freeness:

::: {.definition title="Prefix free encoding" #prefixfreedef}
For two strings $y,y'$, we say that $y$ is a _prefix_ of $y'$ if $|y| \leq |y'|$ and for every $i<|y'|$, $y'_i = y_i$.

Let $E:\mathcal{O} \rightarrow \{0,1\}^*$ be a function.
We say that $E$ _prefix-free_ if there does not exist a distinct pair of  objects $o, o' \in \mathcal{O}$ such that  $E(o)$  is a prefix of $E(o')$.
:::

Recall that for every set $\mathcal{O}$, the set $\mathcal{O}^*$ consists of all finite length tuples (i.e., _lists_) of elements in $\mathcal{O}$.
The following theorem shows that if $E$ is a prefix-free encoding of $\mathcal{O}$ then by concatenating encodings we can obtain a valid (i.e., one-to-one) representation of $\mathcal{O}^*$:



::: {.theorem title="Prefix-free implies tuple encoding" #prefixfreethm}
Suppose that $E:\mathcal{O} \rightarrow \{0,1\}^*$ is prefix-free.
Then the following map $\overline{E}:\mathcal{O}^* \rightarrow \{0,1\}^*$ is one to one, for every $o_0,\ldots,o_{k-1} \in \mathcal{O}^*$, we define
$$
\overline{E}(o_0,\ldots,o_{k-1}) = E(o_0)E(o_1) \cdots E(o_{k-1}) \;.
$$
:::


> ### { .pause }
[prefixfreethm](){.ref} is one of those  statements that are a little hard to parse, but in fact are fairly straightforward to prove  once you understand what they mean.
Thus I highly recommend that you pause here, make sure you understand  statement of the theorem, and try to prove it yourself before proceeding further.




![If we have a prefix-free representation of each object then we can concatenate the representations of $k$ objects to obtain a representation for the tuple $(o_0,\ldots,o_{k-1})$.](../figure/repres_list.png){#figureid .margin  }

> ### {.proofidea data-ref="prefixfreethm"}
The idea behind the proof is simple.
Suppose that for example we want to decode a triple $(o_0,o_1,o_2)$ from its representation $x= E'(o_0,o_1,o_2)=E(o_0)E(o_1)E(o_2)$.
We will do so by first finding the first prefix $x_0$ of $x$ such is a representation of some object.
Then we will decode this object, remove $x_0$ from $x$ to obtain a new string $x'$,  and continue onwards to find the first prefix $x_1$ of $x'$ and so on and so forth  (see [prefix-free-tuples-ex](){.ref}).
The prefix-freeness property of $E$ will ensure that $x_0$ will in fact be $E(o_0)$,  $x_1$ will be $E(o_1)$ etc.








::: {.proof data-ref="prefixfreethm"}
We now show the formal proof.
Suppose, towards the sake of contradiction that there exist two distinct tuples $(o_0,\ldots,o_{k-1})$ and $(o'_0,\ldots,o'_{k'-1})$ such that

$$
\overline{E}(o_0,\ldots,o_{k-1})= \overline{E}(o'_0,\ldots,o'_{k'-1}) \;. \label{prefixfreeassump}
$$
We will denote the string $\overline{E}(o_0,\ldots,o_{k-1})$ by $\overline{x}$.

Let $i$ be the first coordinate such that $o_i \neq o'_i$.
(If $o_i=o'_i$ for all $i$ then, since we assume the two tuples are distinct, one of them must be larger than the other. In this case we assume without loss of generality that $k'>k$ and let $i=k$.)
In the case that $i<k$, we see that the string $\overline{x}$ can be written in two different ways:

$$
\overline{x} = \overline{E}(o_0,\ldots,o_{k-1}) = x_0\cdots x_{i-1} E(o_i) E(o_{i+1}) \cdots E(o_{k-1})
$$

and

$$
\overline{x} = \overline{E}(o'_0,\ldots,o'_{k'-1}) = x_0\cdots x_{i-1} E(o'_i) E(o'_{i+1}) \cdots E(o'_{k-1})
$$

where $x_j = E(o_j) = E(o'_j)$ for all $j<i$.
Let $\overline{y}$ be the string obtained after removing  the  prefix $x_0 \cdots x_{i-i}$ from $\overline{x}$.
We see that $\overline{y}$ can be written as both $\overline{y}= E(o_i)s$ for some string $s\in \{0,1\}^*$ and as $\overline{y} = E(o'_i)s'$ for some $s'\in \{0,1\}^*$.
But this means that one of $E(o_i)$ and $E(o'_i)$ must be a prefix of the other, contradicting the prefix-freeness of $E$.

In the case that $i=k$ and $k'>k$ we get a contradiction in a the following way. In this case

$$\overline{x} = E(o_0)\cdots E(o_{k-1}) = E(o_0) \cdots E(o_{k-1}) E(o'_k) \cdots E(o'_{k'-1})$$

which means that $E(o'_k) \cdots E(o'_{k'-1})$ must correspond to the empty string $\text{""}$. But in such a case $E(o'_k)$ must be the empty string, which in particular is the prefix of any other string, contradicting the prefix-freeness of $E$.
:::

::: {.remark title="Prefix freeness of list representation" #prefixfreelistsrem}
Even if the representation $E$ of objects in $\mathcal{O}$ is prefix free, this does not mean that our representation $\overline{E}$ of _lists_ of such objects will be prefix free as well.
In fact, it won't be: for every three objects $o,o',o''$ the representation of the list $(o,o')$ will be a prefix of the representation of the list $(o,o',o'')$.
However, as we see in [prefixfreetransformationlem](){.ref} below, we can transform _every_ representation into prefix free form, and so will be able to use that transformation if needed to represent lists of lists, lists of lists of lists, and so on and so forth.
:::


### Making representations prefix-free

Some natural representations are prefix-free.
For example, every _fixed output length_ representation (i.e., one-to-one function $E:\mathcal{O} \rightarrow \{0,1\}^n$) is automatically prefix-free, since a string $x$ can only be a prefix of an equal-length $x'$ if $x$ and $x'$ are identical.
Moreover, the approach we used for representing rational numbers can be used to show the following:

> ### {.lemma #prefixfreetransformationlem}
Let $E:\mathcal{O} \rightarrow \{0,1\}^*$ be a one-to-one function.
Then there is a one-to-one prefix-free encoding $\overline{E}$ such that $|\overline{E}(o)| \leq 2|E(o)|+2$ for every $o\in \mathcal{O}$.

> ### { .pause }
For the sake of completeness, we will include the proof below, but it is a good idea for you to pause here and try to prove it yourself, using the same technique we used for representing rational numbers.

::: {.proof data-ref="prefixfreetransformationlem"}
Define the function $PF:\{0,1\}^* \rightarrow \{0,1\}^*$ as follows $PF(x)=x_0 x_0 x_1 x_1 \ldots x_{n-1}x_{n-1}01$ for every $x\in \{0,1\}^*$. If $E:\mathcal{O} \rightarrow \{0,1\}^*$ is the (potentially not prefix-free) representation for $\mathcal{O}$, then we transform it into a prefix-free representation $\overline{E}:\mathcal{O} \rightarrow \{0,1\}^*$ by defining $\overline{E}(o)=PF(E(o))$.

To prove the lemma we need to show that __(1)__ $\overline{E}$ is one-to-one and __(2)__ $\overline{E}$ is prefix-free.
In fact __(2)__ implies __(1)__, since if $\overline{E}(o)$ is never a prefix of $\overline{E}(o')$ for every $o \neq o'$ then in particular  $\overline{E}$ is one-to-one.
Now suppose, toward a contradiction, that there are $o \neq o'$ in $\mathcal{O}$ such that $\overline{E}(o)$ is  a prefix of $\overline{E}(o')$. (That is, if $y=\overline{E}(o)$ and $y'=\overline{E}(o')$, then  $y_j = y'_j$ for every $j<|y|$.)

Define $x = E(o)$ and $x'=E(o')$.
Note that since $E$ is one-to-one, $x \neq x'$.
(Recall that two strings $x,x'$ are distinct if they either differ in length or have at least one distinct coordinate.)
Under our assumption, $|PF(x)| \leq |PF(x')|$, and since by construction $|PF(x)|=2|x|+2$, it follows that $|x| \leq |x'|$.
If $|x|=|x'|$ then, since $x \neq x'$, there must be a coordinate $i\in \{0,\ldots, |x|-1\}$ such that $x_i \neq x'_i$. But since $PF(x)_{2i}=x_i$, we get that $PF(x)_{2i} \neq PF(x')_{2i}$ and hence $\overline{E}(o)=PF(x)$ is _not_ a prefix of $\overline{E}(o')=PF(x')$.
Otherwise (if $|x| \neq |x'|$) then it must be that $|x| < |x'|$, and hence if $n=|x|$, then $PF(x)_{2n}=0$ and $PF(x)_{2n+1}=1$. But since $n<|x'|$, $PF(x')_{2n},PF(x')_{2n+1}$ is equal to either $00$ or $11$, and in any case we get that $\overline{E}(o)=PF(x)$ is not a prefix of $\overline{E}(o')=PF(x')$.
:::

The proof of [prefixfreetransformationlem](){.ref} is not the only or even the best way to transform an arbitrary representation into prefix-free form.
In fact, we can even obtain a more efficient transformation satisfying $|E'(o)| \leq |o| + O(\log |o|)$.
We leave proving this as an exercise (see [prefix-free-ex](){.ref}).

### "Proof by Python" (optional)

The proofs of [prefixfreethm](){.ref} and [prefixfreetransformationlem](){.ref} are _constructive_ in the sense that they give us:

* A way to transform the encoding and decoding functions of any representation of an object $O$ to a encoding and decoding functions that are prefix free;

* A way to extend prefix-free encoding and decoding of single objects to encoding and decoding of _lists_ of objects by concatenation.


Specifically, we could transform any pair of Python functions `encode` and `decode` to functions `pfencode` and `pfdecode` that correspond to a prefix-free encoding and decoding.
Similarly, given `pfencode` and `pfdecode` for single objects, we can extend them to encoding of lists.
Let us show how this works for the case of the `NtS` and `StN` functions we defined above.

We start with the "Python proof" of [prefixfreetransformationlem](){.ref}: a way to transform an arbitrary representation into one that is _prefix free_.
The function `prefixfree` below takes as input an encoding and decoding functions, and returns a triple of function implementing a prefix free encoding functions, as well as a function that checks whether a string is a valid encoding of an object.

```python
# takes functions encode and decode mapping
# objects to lists of bits and vice versa,
# and returns functions pfencode and pfdecode that
# maps objects to lists of bits and vice versa
# in a prefix-free way.
# Also returns a function pfvalid that says
# whether a list is a valid encoding
def prefixfree(encode, decode):
    def pfencode(o):
        L = encode(o)
        return [L[i//2] for i in range(2*len(L))]+[0,1]
    def pfdecode(L):
        return decode([L[j] for j in range(0,len(L)-2,2)])
    def pfvalid(L):
        return (len(L) % 2 == 0 ) and L[-2:]==[0,1]

    return pfencode, pfdecode, pfvalid

pfNtS, pfStN , pfvalidN = prefixfree(NtS,StN)

NtS(234)
# 11101010
pfNtS(234)
# 111111001100110001
pfStN(pfNtS(234))
# 234
pfvalidM(pfNtS(234))
# true
```

> ### { .pause }
Note that Python function `prefixfree` above takes two _Python functions_ as input and outputs three Python functions as output.^[When it's not too awkward, we use the term "Python function" or "subroutine" to distinguish between such snippets of python programs and mathematical functions. However, in comments in python source we use "functions" to denote python functions, just as we use "integers" to denote python int objects.]
You don't have to know Python in this course, but you do need to get comfortable with the idea of functions as mathematical objects in their own right, that can be used as inputs and outputs of other functions.

We now show a "Python proof" of [prefixfreethm](){.ref}. Namely, we show a function `represlists` that takes as input a prefix-free representation scheme (implmented via  encoding, decoding, and validity testing functions) and outputs a representation scheme for _lists_ of such objects. If we want to make this representation prefix-free then we could fit it into the function `prefixfree` above.

```python
# Takes functions pfencode, pfdecode and pfvalid,
# and returns functions encodelists, decodelists
# that can encode and decode
# lists of the objects respectively
def represlists(pfencode,pfdecode,pfvalid):

    def encodelist(L):
        """Gets list of objects, encodes it as list of bits"""
        return "".join([pfencode(obj) for obj in L])

    def decodelist(S):
        """Gets lists of bits, returns lists of objects"""
        i=0; j=1 ; res = []
        while j<=len(S):
            if pfvalid(S[i:j]):
                res += [pfdecode(S[i:j])]
                i=j
            j+= 1
        return res

    return encodelist,decodelist


LtS , StL = represlists(pfNtS,pfStN,pfvalidN)

LtS([234,12,5])
# 111111001100110001111100000111001101
StL(LtS([234,12,5]))
# [234, 12, 5]
```

### Representing letters and text

We can represent a letter or symbol by a string, and then if this representation is prefix-free, we can represent a sequence of symbols by simply concatenating the representation of each symbol.
One such representation is the [ASCII](https://en.wikipedia.org/wiki/ASCII) that represents $128$ letters and symbols as strings of $7$ bits.
Since the ASCII representation  is  fixed-length, it is automatically prefix-free (can you see why?).
[Unicode](https://en.wikipedia.org/wiki/Unicode) is  representation of (at the time of this writing) about 128,000 symbols as numbers (known as _code points_) between $0$ and  $1,114,111$.
There are several types of prefix-free representations of the code points, a popular one being [UTF-8](https://en.wikipedia.org/wiki/UTF-8) that encodes every codepoint into a string of length between $8$ and $32$.
<!-- (For example, the UTF-8 encoding for the "confused face" emoji 😕 is `11110000100111111001100010010101`) -->

![The word "Binary" in "Grade 1" or "uncontracted" Unified English Braille. There are seven symbols since the first one is a modifier indicating that the first letter is capitalized.](../figure/braille.png){#braillefig .class .margin }


::: {.example title="The Braille representation" #braille}
The _Braille system_ is another way to encode letters and other symbols as binary strings. Specifically, in Braille every letter is encoded as a string  in $\{0,1\}^6$, which is written using indented dots arranged in two columns and three rows, see [braillefig](){.ref}.
(Some symbols require more than one six-bit string to encode, and so Braille uses a more general prefix-free encoding.)

The Braille system was invented in 1821 by [Louis Braille](https://goo.gl/Y2BkEe) when he was just 12 years old (though he continued working on it and improving it throughout his life). Braille was a French boy that lost his eyesight at the age of 5 as the result of an accident.
:::

::: {.example title="Representing objects in C (optional)" #Crepresentation}

We can use programming languages to probe how our computing environment represents various values.
This is easiest to do in "unsafe" programming languages such as `C` that allow direct access to the memory.

Using a simple `C` program we have produced the following representations of various values.
One can see that for integers, multiplying by 2 corresponds to a "left shift" inside each byte.
In contrast, for floating point numbers, multiplying by two corresponds to adding one to the exponent part of the representation.
A negative number is represented using the [two's complement](https://goo.gl/wov5fa) approach.
Strings are represented in a prefix-free form by ensuring that a zero byte is at their end.

```c
int      2    : 00000010 00000000 00000000 00000000
int      4    : 00000100 00000000 00000000 00000000
int      513  : 00000001 00000010 00000000 00000000
long     513  : 00000001 00000010 00000000 00000000 00000000 00000000 00000000 00000000
int      -1   : 11111111 11111111 11111111 11111111
int      -2   : 11111110 11111111 11111111 11111111
string   Hello: 01001000 01100101 01101100 01101100 01101111 00000000
string   abcd : 01100001 01100010 01100011 01100100 00000000
float    33.0 : 00000000 00000000 00000100 01000010
float    66.0 : 00000000 00000000 10000100 01000010
float    132.0: 00000000 00000000 00000100 01000011
double   132.0: 00000000 00000000 00000000 00000000 00000000 10000000 01100000 01000000
```

If you are curious, the code for this program (which you can run [here](https://goo.gl/L8oMzn)) is the following:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *bytes(void *p,int n){
  int i;
  int j;
  char *a = (char *) p;
  char *s = malloc(9*n+2);
  s[9*n] = '\n';
  s[9*n+1] = 0;


  j = 0;
  for(i=0;i< n*8;i++){
    s[j] = a[i/8] & (128 >> (i % 8)) ? '1' : '0';
    if (i% 8 == 7) { s[++j] = ' '; }
    ++j;
  }
  return s;
}

void printint(int a) {
  printf("%-8s %-5d: %s", "int", a, bytes(&a,sizeof(int)));
}

void printlong(long a) {
  printf("%-8s %-5d: %s", "long", a, bytes(&a,sizeof(long)));
}


void printstring(char *s) {
  printf("%-8s %-5s: %s", "string", s, bytes(s,strlen(s)+1));
}


void printfloat(float f) {
  printf("%-8s %-5.1f: %s", "float", f, bytes(&f,sizeof(float)));
}

void printdouble(double f) {
  printf("%-8s %-5.1f: %s", "double", f, bytes(&f,sizeof(double)));
}



int main(void) {

  printint(2);
  printint(4);
  printint(513);
  printlong(513);


  printint(-1);

  printint(-2);

  printstring("Hello");

  printstring("abcd");

  printfloat(33);
  printfloat(66);
  printfloat(132);
  printdouble(132);


  return 0;
}
```

:::



### Representing vectors, matrices, images

Once we can represent numbers, and lists of numbers, then we can obviously represent _vectors_ (which are just lists of numbers).
Similarly, we can represent lists of lists, and thus in particular  can represent _matrices_.
To represent an image, we can represent the color at each pixel by a list of three numbers corresponding to the intensity of Red, Green and Blue.^[We can restrict to three basic colors since ([most](https://en.wikipedia.org/wiki/Tetrachromacy)) humans only have three types of cones in their retinas. We would have needed 16 basic colors to represent colors visible to the [Mantis Shrimp](https://goo.gl/t7JBfC).]
Thus an image of $n$ pixels would be represented by a list of $n$ such length-three lists.
A video can be represented as a list of images.^[Of course these representations are rather wasteful and [much](https://en.wikipedia.org/wiki/JPEG) [more](https://goo.gl/Vs8UhU) compact representations are typically used for images and videos, though this will not be our concern in this book.]

### Representing graphs

A _graph_ on $n$ vertices can be represented as an $n\times n$ _adjacency_ matrix whose $(i,j)^{th}$ entry is equal to $1$ if the edge $(i,j)$ is present and is equal to $0$ otherwise.
That is, we can represent an $n$ vertex directed graph $G=(V,E)$ as a string  $A\in \{0,1\}^{n^2}$ such that $A_{i,j}=1$ iff the edge $\overrightarrow{i\;j}\in E$.
We can transform an undirected graph to a directed graph by replacing every edge $\{i,j\}$ with both edges $\overrightarrow{i\; j}$ and $\overleftarrow{i\;j}$

Another representation for graphs is the _adjacency list_ representation. That is, we identify the vertex set $V$ of a graph with the set $[n]$ where $n=|V|$, and  represent the graph $G=(V,E)$ a a list of $n$ lists, where the $i$-th list consists of the out-neighbors of vertex $i$.
The difference between these representations can be important for some applications, though for us would typically be immaterial.

![Representing the graph $G=(\{0,1,2,3,4\},\{ (1,0),(4,0),(1,4),(4,1),(2,1),(3,2),(4,3) \})$ in the adjacency matrix and adjacency list representations.](../figure/representing_graphs.png){#representinggraphsfig .margin  }

Once again, we can also define these encoding and decoding functions in python:



```python
from graphviz import Graph

# get n by n matrix (as list of n lists)
# return graph corresponding to it
def matrix2graph(M):
    G = Graph(); n = len(M)
    for i in range(n):
        G.node(str(i)) # add vertex i
        for j in range(n):
            G.node(str(j))
            if M[i][j]: G.edge(str(i),str(j))
            # if M[i][j] is nonzero then add edge between i and j
    return G

matrix2graph([[0,1,0],[0,0,1],[1,0,0]])
```

![Output of `matrix2graph` on the matrix `[[0,1,0],[0,0,1],[1,0,0]]`](../figure/graphfrommat.png){#figid .margin  } \

<!---
import warnings
warnings.filterwarnings("ignore")

def nxgraph(G):
    P = pydotplus.graph_from_dot_data(G.source)
    return nx.drawing.nx_pydot.from_pydot(P)
--->

### Representing lists

If we have a way of representing objects from a set $\mathcal{O}$ as  binary strings, then we can represent lists of these objects by applying a prefix-free transformation.
Moreover, we can use a trick similar to the above to handle  _nested_ lists.
The idea is that if we have some representation $E:\mathcal{O} \rightarrow \{0,1\}^*$, then we can represent nested lists of items from $\mathcal{O}$ using strings over the five element alphabet $\Sigma = \{$ `0`,`1`,`[` , `]` , `,` $\}$.
For example, if $o_1$ is represented by `0011`, $o_2$ is represented by `10011`, and $o_3$ is represented by `00111`, then we can represent the nested list $(o_1,(o_2,o_3))$ as the string `"[0011,[10011,00111]]"` over the alphabet $\Sigma$.
By encoding every element of $\Sigma$ itself as a three-bit string,
we can transform any representation for objects $\mathcal{O}$ into a representation that allows to represent (potentially nested) lists of these objects.



### Notation

We will typically identify an object with its representation as a string. For example, if $F:\{0,1\}^* \rightarrow  \{0,1\}^*$ is some function that maps strings to strings and $x$ is an integer, we might make statements such as "$F(x)+1$ is prime" to mean that if we represent $x$ as a string $\underline{x}$ and let $\underline{y}=F(\underline{x})$, then the integer $y$ represented by the string $\underline{y}$ satisfies that $y+1$ is prime. (You can see how this convention of identifying objects with their representation can save us a lot of cumbersome formalism.)
Similarly, if $x,y$ are some objects and $F$ is a function that takes strings as inputs, then by $F(x,y)$ we will mean the result of applying $F$ to the representation of the ordered pair $(x,y)$.
We will use the same notation to invoke functions on $k$-tuples of objects for every $k$.

This convention of identifying an object with its representation as a string is one that we humans follow all the time. For example, when people say a statement such as "$17$ is a prime number", what they really mean is that the integer whose decimal representation is the string "`17`", is prime.


::: {.quote}
When we say

_$A$ is an algorithm that computes the multiplication function on natural numbers._

what we really mean is that

_$A$ is an algorithm that computes the function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ such that for every pair $a,b \in \N$, if $x\in \{0,1\}^*$ is a string representing the pair $(a,b)$ then $F(x)$ will be a string representing their product $a\cdot b$._
:::


## Defining computational tasks

Abstractly, a _computational process_ is some process that takes an input which is a string of bits, and produces an output which is a string of bits.
This transformation of input to output can be done using a modern computer, a person following instructions, the evolution of some natural system, or any other means.


![A computational process](../figure/computation.png){#figureid .margin  }

In future chapters, we will turn to mathematically defining  computational process, but, as we discussed above for now we want to focus on _computational tasks_; i.e., focus on the __specification__ and not the __implementation__.
Again, at an abstract level, a computational task can specify any relation that the output needs to have with the input.
But for most of this course, we will focus on the simplest and most common task of _computing a  function_.
Here are some examples:

* Given (a representation) of two integers $x,y$, compute the product $x\times y$. Using our representation above, this corresponds to computing a function from $\{0,1\}^*$ to $\{0,1\}^*$. We've seen that there is more than one way to solve this computational task, and in fact, we still don't know the best algorithm for this problem.

* Given (a representation of) an integer $z$, compute its _factorization_; i.e., the list of primes $p_1 \leq \cdots \leq p_k$ such that $z = p_1\cdots p_k$.  This again corresponds to computing a function from $\{0,1\}^*$ to $\{0,1\}^*$. The gaps in our knowledge of the complexity of this problem are even longer.

* Given (a representation of) a graph $G$ and two vertices $s$ and $t$, compute the length of the shortest path in $G$ between $s$ and $t$, or do the same for the _longest_ path (with no repeated vertices) between $s$ and $t$. Both these tasks correspond to computing a function from $\{0,1\}^*$ to $\{0,1\}^*$, though it turns out that there is a huge difference in their computational difficulty.

* Given the code of a Python program, determine whether there is an input that would force it into an infinite loop. This corresponds to computing a _partial_ function from $\{0,1\}^*$ to $\{0,1\}$ since not every string corresponds to a syntactically valid Python program. We will see that we _do_ understand the computational status of this problem, but the answer is quite surprising.

*  Given (a representation of) an image $I$, decide if $I$ is a photo of a cat or a dog. This correspond to computing  some (partial) function from $\{0,1\}^*$ to $\{0,1\}$.


> ### {.remark title="Boolean functions and languages" #booleanrem}
An important special case of computational tasks corresponds to computing _Boolean_ functions, whose output is a single bit $\{0,1\}$.
Computing such functions corresponds to answering a YES/NO question, and hence this task is also known as a _decision problem_.
Given any function $F:\{0,1\}^* \rightarrow \{0,1\}$ and $x\in \{0,1\}^*$, the task of computing $F(x)$ corresponds to the task of deciding whether or not $x\in L$ where $L = \{ x : F(x)=1 \}$ is known as the _language_ that corresponds to the function $F$.^[The language terminology is due to historical connections between the theory of computation and formal linguistics as developed by Noam Chomsky.]
Hence many texts refer to such as computational task as _deciding a language_.

![A subset $L \subseteq \{0,1\}^*$ can be identified with the function $F:\{0,1\}^* \rightarrow \{0,1\}$ such that $F(x)=1$ if $x\in L$ and $F(x)=0$ if $x\not\in L$. Functions with a single bit of output are called _Boolean functions_, while subsets of strings are called _languages_. The above shows that the two are essentially the same object, and we can identify the task of deciding membership in $L$ (known as _deciding a language_ in the literature) with the task of computing the function $F$.](../figure/booleanfunc.png){#booleanlangfig .margin  }





For every particular  function $F$, there can be several possible _algorithms_ to compute $F$.
We will be interested in questions such as:

* For a given function $F$, can it be the case that _there is no algorithm_ to compute $F$?

* If there is an algorithm, what is the best one? Could it be that $F$ is "effectively uncomputable" in the sense that every algorithm for computing $F$ requires a prohibitively large amount of resources?

* If we can't answer this question, can we show equivalence between different functions $F$ and $F'$ in the sense that either they are both easy (i.e., have fast algorithms) or they are both hard?

* Can a function being hard to compute ever be a _good thing_? Can we use it for applications in areas such as cryptography?

In order to do that, we will need to mathematically define the notion of an _algorithm_, which is what we'll do in [compchap](){.ref}.

### Distinguish functions from programs!

You should always watch out for potential confusions between **specifications** and **implementations** or equivalently between **mathematical functions**  and **algorithms/programs**.
It does not help that programming languages (Python included) use the term _"functions"_ to denote (parts of) _programs_.
This confusion also stems from thousands of years of mathematical history, where people typically defined functions by means of a way to compute them.

For example, consider the  multiplication function on natural numbers.
This is the function $MULT:\N\times \N \rightarrow \N$ that maps a pair $(x,y)$ of natural numbers to the number $x \cdot y$.
As we mentioned, it can be implemented in more than one way:

```python
def mult1(x,y):
    res = 0
    while y>0:
        res += x
        y   -= 1
    return res

def mult2(x,y):
    a = NtS(x)
    b = NtS(y)
    res = 0
    res = [0]*(len(a)+len(b))
    for i in range(len(a)):
        for j in range(len(b)):
            res += int(a[len(a)-i])*int(b[len(b)-j])*(10**(i+j))
    return res

print(mult1(12,7))
# 84
print(mult2(12,7))
# 84
```

Both `mult1` and `mult2` produce the same output given the same pair of inputs.
(Though `mult1` will take far longer to do so when the numbers become large.)
Hence, even though these are two different _programs_, they compute the same _mathematical function_.
This distinction between a _program_ or _algorithm_ $A$, and the _function_ $F$ that $A$ _computes_ will be absolutely crucial for us in this course (see also [functionornotfig](){.ref}).

![A _function_ is a mapping of inputs to outputs. A _program_ is a set of instructions of how to obtain an output given an input. A program _computes_ a function, but it is not the same as a function, popular programming language terminology notwithstanding.](../figure/functionornot.png){#functionornotfig .margin  }

::: { .bigidea #functionprogramidea }
A _function_ is not the same as  a _program_. A program _computes_ a function.
:::

Distinguishing _functions_ from _programs_ (or other ways for computing, including _circuits_ and _machines_) is a crucial theme for this course.
For this reason, this is often a running theme in questions that I (and many other instructors) assign in homeworks and exams (hint, hint..).


::: {.remark title="Computation beyond functions (advanced, optional)" #beyonfdunc}
Functions capture quite a lot of computational tasks, but one can consider more general settings as well.
For starters, we can and will talk about _partial_ functions, that are not defined on all inputs.
When computing a partial function, we only need to worry about the inputs on which the function is defined.
Another way to say it is that we can design an algorithm for a partial function $F$ under the assumption that someone "promised" us that all inputs $x$ would be such that $F(x)$ is defined (as otherwise we don't care about the result).
Hence such tasks are also known as _promise problems_.


Another generalization is to consider _relations_ that may have more than one possible admissible output.
For example, consider the task of finding any solution for a given set of equations.
A _relation_ $R$ maps a string $x\in \{0,1\}^*$ into a _set of strings_ $R(x)$ (for example, $x$ might describe a set of equations, in which case  $R(x)$ would correspond to  the set of all solutions to $x$).
We can also identify a relation $R$ with the set of pairs of strings $(x,y)$ where $y\in R(x)$.
A computational process solves a relation if for every $x\in \{0,1\}^*$, it outputs some string $y\in R(x)$.


Later on in this course we will consider even more general tasks, including  _interactive_  tasks, such as finding good strategy in a game, tasks defined using probabilistic notions, and others.
However, for much of this course we will focus on the task of computing a function, and often even a _Boolean_ function, that has only a single bit of output.
It turns out that a great deal of the theory of computation can be studied in the context of this task, and the insights  learned are applicable in the more general settings.
:::



> ### { .recap }
* We can represent essentially every object we want to compute on using binary strings.
* A representation scheme for a set of objects $\mathcal{O}$ is a one-to-one map  from $\mathcal{O}$ to $\{0,1\}^*$.
* A basic computational task is the task of _computing a function_ $F:\{0,1\}^* \rightarrow \{0,1\}^*$. This encompasses not just arithmetical computations such as multiplication, factoring, etc. but a great many other tasks arising in areas as diverse as scientific computing, artificial intelligence, image processing, data mining and many many more.
* We will study the question of finding (or at least giving bounds on) what is the _best_ algorithm for  computing $F$ for various interesting functions $F$.


## Exercises


::: {.exercise}
Which one of these objects can be represented by a binary string?

a. An integer $x$

b. An undirected graph $G$.

c. A directed graph $H$

d. All of the above.
:::



::: {.exercise title="More compact than ASCII representation" #compactrepletters}
The ASCII encoding can be used to encode a string of $n$ English letters as an $7n$ bit binary string, but in this program we ask about finding a more compact representation for  strings of English lowercase letters.


1. Prove that there exists a representation scheme $(E,D)$ for strings over the 26-letter alphabet $\{ a, b,c,\ldots,z \}$ as binary strings such that for every $n>0$ and length-$n$ string $x \in \{ a,b,\ldots,z \}^n$, the representation $E(x)$ is a binary string of length at most  $4.8n+1000$. In other words, prove that for every $n$, there exists a one-to-one function $E:\{a,b,\ldots, z\}^n \rightarrow \{0,1\}^{\lfloor 4.8n +1000 \rfloor}$.

2. Prove that there exists _no_ representation scheme for strings over the alphabet $\{ a, b,\ldots,z \}$ as binary strings such that for every length-$n$ string $x \in \{ a,b,\ldots, z\}^n$, the representation $E(x)$ is a binary string of length  $\lfloor 4.6n+1000 \rfloor$. In other words, prove that there exists some $n>0$ such that there is no one-to-one function $E:\{a,b,\ldots,z \}^n \rightarrow \{0,1\}^{\lfloor 4.6n + 1000 \rfloor}$

3. Python's `bz2.compress` function is mapping from strings to strings,  which uses the _lossless_ (and hence _one to one_) [bzip2](https://en.wikipedia.org/wiki/Bzip2) algorithm for compression.  After converting to lowercase, and truncating  spaces and numbers, the text of Tolstoy's "War and Peace" contains $n=2,517,262$. Yet, if we run `bz2.compress` on the string of the text of "War and Peace" we get a string of length $k=6,274,768$ bits, which is only $2.49n$ (and in particular much smaller than $4.6n$). Explain why this does not contradict your answer to the previous question.

4. Interestingly, if we try to apply `bz2.compress` on a _random_ string, we get much worse performance. In my experiments, I got a ratio of about $4.78$ between the number of bits in the output and the number of characters in the input.  However, one could imagine that one could do better and that there exists a company called "Pied Piper" with an algorithm that can losslessly compress a string of $n$ random lowercase letters to fewer than $4.6n$ bits.^[Actually that particular fictional company uses a metric that focuses more on compression _speed_ then _ratio_, see [here](https://blogs.dropbox.com/tech/2016/06/lossless-compression-with-brotli/) and [here](https://www.jefftk.com/p/weissman-scores-useful).] Show that this is not the case by proving that for _every_ $n>100$ and one to one function $Encode:\{a,\ldots,z\}^{n} \rightarrow \{0,1\}^*$, if we let $Z$ be the random variable  $|Encode(x)|$ (i.e., the length of $Encode(x)$) for $x$ chosen uniformly at random from the set $\{a,\ldots,z\}^n$, then the expected value of $Z$ is at least $4.6n$.
:::






::: {.exercise title="Representing graphs: upper bound" #representinggraphsex}
Show that there is a string representation of directed graphs with vertex set $[n]$ and degree at most $10$ that uses at most $1000 n\log n$ bits. More formally, show the following. Suppose we  define for every $n\in\mathbb{N}$, the set $G_n$ as the set containing all directed graphs (with no self loops) over the vertex set $[n]$ where every vertex has degree at most $10$. Then, prove that  for every sufficiently large $n$, there exists a one-to-one  function $E:G_n \rightarrow \{0,1\}^{\lfloor 1000 n \log n \rfloor}$.
:::


::: {.exercise title="Representing graphs: lower bound" #represgraphlbex}
1. Define $S_n$ to be the set of one-to-one and onto functions mapping $[n]$ to $[n]$. Prove that there is a one-to-one mapping from $S_n$ to $G_{2n}$, where $G_{2n}$ is the set defined in [representinggraphsex](){.ref} above.

2. In this question you will show that one cannot improve the representation of [representinggraphsex](){.ref} to length $o(n \log n)$. Specifically, prove for every sufficiently large  $n\in \mathbb{N}$ there is _no_ one-to-one function $E:G_n \rightarrow \{0,1\}^{\lfloor 0.001 n \log n \rfloor +1000}$.
:::






::: {.exercise title="Multiplying in different representation" #multrepres }
Recall that the grade-school algorithm for multiplying two numbers requires $O(n^2)$ operations. Suppose that instead of using decimal representation, we use one of the following representations $R(x)$ to represent a number $x$ between $0$ and $10^n-1$. For which one of these representations you can still multiply the numbers in $O(n^2)$ operations?

a. The standard binary representation: $B(x)=(x_0,\ldots,x_{k})$ where $x = \sum_{i=0}^{k} x_i 2^i$ and $k$ is the largest number s.t. $x \geq 2^k$.

b. The reverse binary representation: $B(x) = (x_{k},\ldots,x_0)$ where $x_i$ is defined as above for $i=0,\ldots,k-1$. \

c. Binary coded decimal representation: $B(x)=(y_0,\ldots,y_{n-1})$ where $y_i \in \{0,1\}^4$ represents the $i^{th}$ decimal digit of $x$ mapping $0$ to $0000$, $1$ to $0001$, $2$ to $0010$, etc. (i.e. $9$ maps to $1001$)

d.  All of the above.
:::


> ### {.exercise }
Suppose that $R:\N \rightarrow \{0,1\}^*$ corresponds to  representing a number $x$ as a string of $x$ $1$'s, (e.g., $R(4)=1111$, $R(7)=1111111$, etc.).
If $x,y$ are numbers between $0$ and $10^n -1$, can we still multiply $x$ and $y$ using $O(n^2)$ operations if we are given them in the representation $R(\cdot)$?



::: {.exercise }
Recall that if $F$ is a one-to-one and onto function mapping elements of a finite set $U$ into a finite set $V$ then the sizes of $U$ and $V$ are the same. Let $B:\N\rightarrow\{0,1\}^*$ be the function such that for every $x\in\N$, $B(x)$ is the binary representation of $x$.

a. Prove that $x < 2^k$ if and only if $|B(x)| \leq k$.

b. Use a. to compute the size of the set $\{ y \in \{0,1\}^* : |y| \leq k \}$ where $|y|$ denotes the length of the string $y$.

c. Use a. and b. to prove that $2^k-1 = 1 + 2 + 4+ \cdots + 2^{k-1}$.
:::


::: {.exercise  title="Prefix-free encoding of tuples" #prefix-free-tuples-ex}
Suppose that $F:\N\rightarrow\{0,1\}^*$ is a one-to-one function that is _prefix-free_ in the sense that there is no $a\neq b$ s.t.  $F(a)$ is a prefix of $F(b)$.

a. Prove that $F_2:\N\times \N \rightarrow \{0,1\}^*$, defined as $F_2(a,b) = F(a)F(b)$ (i.e., the concatenation of $F(a)$ and $F(b)$) is a one-to-one function.

b. Prove that $F_*:\N^*\rightarrow\{0,1\}^*$ defined as $F_*(a_1,\ldots,a_k) = F(a_1)\cdots F(a_k)$ is a one-to-one function, where $\N^*$ denotes the set of all finite-length lists of natural numbers.
:::

::: {.exercise title="More efficient prefix-free transformation" #prefix-free-ex}
Suppose that $F:O\rightarrow\{0,1\}^*$ is some (not necessarily prefix-free) representation of the objects in the set $O$, and $G:\N\rightarrow\{0,1\}^*$ is a prefix-free representation of the natural numbers.  Define $F'(o)=G(|F(o)|)F(o)$ (i.e., the concatenation of the representation of the length $F(o)$ and $F(o)$).

a. Prove that $F'$ is a prefix-free representation of $O$.

b. Show that we can transform any representation to a prefix-free one by a modification that takes a $k$ bit string into a string of length at most $k+O(\log k)$.

c. Show that we can transform any representation to a prefix-free one by a modification that takes a $k$ bit string into a string of length at most $k+ \log k + O(\log\log k)$.^[Hint: Think recursively how to represent the length of the string.]
:::


::: {.exercise title="Kraft's Inequality" #prefix-free-lb}
Suppose that $S \subseteq \{0,1\}^n$ is some finite prefix-free set.

a. For every $k \leq n$ and length-$k$ string $x\in S$, let $L(x) \subseteq \{0,1\}^n$ denote all the length-$n$ strings whose first $k$ bits are $x_0,\ldots,x_{k-1}$. Prove that __(1)__ $|L(x)|=2^{n-|x|}$ and __(2)__ If $x \neq x'$ then $L(x)$ is disjoint from $L(x')$.

b. Prove that $\sum_{x\in S}2^{-|x|} \leq 1$.

c. Prove that there is no prefix-free encoding of strings with less than logarithmic overhead. That is, prove that there is no function $PF:\{0,1\}^* \rightarrow \{0,1\}^*$ s.t. $|PF(x)| \leq |x|+0.9\log |x|$ for every $x\in \{0,1\}^*$ and such that the set $\{ PF(x) : x\in \{0,1\}^* \}$ is prefix-free. The factor $0.9$ is arbitrary; all that matters is that it is less than $1$.
:::

> ### {.exercise title="Composition of one-to-one functions" #onetoonecompex}
Prove that for every two one-to-one functions $F:S \rightarrow T$ and $G:T \rightarrow U$, the function $H:S \rightarrow U$ defined as $H(x)=G(F(x))$ is one to one.


::: {.exercise title="Natural numbers and strings" #naturalsstringsmapex}
1. We have shown that the natural numbers can be represented as strings. Prove that the other direction holds as well: that there is a one-to-one map $StN:\{0,1\}^* \rightarrow \N$. ($StN$ stands for "strings to numbers".)

2. Recall that Cantor proved that there is no one-to-one map $RtN:\R \rightarrow \N$. Show that Cantor's result implies [cantorthm](){.ref}.
:::

::: {.exercise title="Map lists of integers to a number" #listsinttonumex}
Recall that for every set $S$, the set $S^*$ is defined as the set of all finite sequences of members of $S$ (i.e., $S^* = \{ (x_0,\ldots,x_{n-1}) \;|\; n\in\mathbb{N} \;,\; \forall_{i\in [n]} x_i \in S \}$ ). Prove that there is a one-one-map from $\mathbb{Z}^*$ to $\mathbb{N}$ where $\mathbb{Z}$ is the set of $\{ \ldots, -3 , -2 , -1,0,+1,+2,+3,\ldots \}$ of all integers.
:::




## Bibliographical notes


The study of representing data as strings mostly follows under the purview of _information theory_, as covered in the classic textbook of Cover and Thomas [@CoverThomas06].
Representations are also studied in the field of  of _data structures design_, as covered in texts such as  [@CLRS].



The idea that we should separate the _definition_ or _specification_ of a function from its _implementation_ or _computation_ might seem "obvious", but it took quite a lot of time for mathematicians to arrive at this viewpoint.
Historically, a function $F$ was  identified by  rules or formulas showing  how to derive the output from the input.
As we discuss in greater  depth in  [chapcomputable](){.ref}, in the 1800's this somewhat informal notion of a function started "breaking at the seams" and eventually mathematicians arrived at the more rigorous definition of  a function as an arbitrary assignment of input to outputs.
While many  functions may be described (or computed) by one or more  formulas, today we do not consider that to be an essential property of functions, and also allow functions that do not correspond to any "nice" formula.

We've mentioned that all  representations of the real numbers are inherently _approximate_. Thus an important endeavor is to understand what guarantees we can offer on the approximation quality of the output of an algorithm, as a function of the approximation quality of the inputs. This is known as the question of [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability).
The  [Floating Points Guide website](https://floating-point-gui.de/) contains extensive description of the floating point representation, as well the ways in which it could subtly fail, see also the website [0.30000000000000004.com](http://0.30000000000000004.com/).

Dauben [@Dauben90cantor] gives a biography of Cantor  with emphasis on the development of his mathematical ideas. [@halmos1960naive] is a  classic textbook on set theory, including also Cantor's theorem. Cantor's Theorem is also covered in many texts on discrete mathematics, including  [@LehmanLeightonMeyer , @LewisZax19].

The adjacency matrix representation of graphs is not merely a convenient way to map a graph into a binary string, but it turns out that many natural notions and operations on matrices are useful for graphs as well. (For example, Google's PageRank algorithm relies on this viewpoint.)  The notes of [Spielman's course](http://www.cs.yale.edu/homes/spielman/561/) are an excellent source for this area, known as _spectral graph theory_. We will return to this view much later in this book when we talk about _random walks_.


Gromov's and Pomerantz's quotes are taken from [Doron Zeilberger's page](http://sites.math.rutgers.edu/~zeilberg/quotes.html).
