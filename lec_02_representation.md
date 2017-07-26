# Computation and Representation


>_"The alphabet was a great invention, which enabled men to store and to learn with little effort what others had learned the hard way-that is, to learn from books rather than from direct, possibly painful, contact with the real world."_, B.F. Skinner

>_"I found that every number, which may be expressed from one to ten, surpasses the preceding by one unit: afterwards the ten is doubled or tripled  ...  until a hundred; then the hundred is doubled and tripled in the same manner as the units and the tens ... and so forth to the utmost limit of numeration."_,  Muhammad ibn Mūsā al-Khwārizmī, 820, translation by Fredric Rosen, 1831.


To a first approximation, computation can be thought of as a process that maps an _input_ to an _output_.

![Our basic notion of _computation_ is some process that maps and input to an output](../figure/input_output.png){#figureid .class width=300px height=300px}

When discussing computation, it is important to separate the question of  __what__ is the task we need to perform (i.e., the _specification_) from the question of __how__ we achieve this task (i.e., the _implementation_).
For example, as we've seen, there is more than one way to achieve the computational task of computing the product of two integers.

In this lecture we  discuss the first question - how do we define a computational task.
For starters, we need to define the inputs and outputs.
A priori this seems nontrivial, since computation today is applied to a huge variety  of objects.
We do not compute  merely on numbers, but also on texts, images, videos, connection graphs of social networks, MRI scans, gene data, and even other programs.  
We will represent all these objects as __strings of zeroes and ones__, that is objects such as $0011101$ or $1011$ or any other finite list of $1$'s and $0$'s.

![We represent numbers, texts, images, networks and many other objects using strings of zeroes and ones. Writing the zeroes and ones themselves in green font over a black background is optional.](../figure/zeroes-ones.jpg){#figureid .class width=300px height=300px}

Today, we are so used to the notion of digital representation that we do not find this surprising.
But it is  a deep insight with significant implications.
Many animals can convey a particular fear or desire, but what's unique about humans'  _language_ is that we use a  finite collection of basic symbols to describe a potentially unlimited range of experiences.
Language allows transmission of information over both time and space, and enables societies that span a  great many people and accumulate a body of shared knowledge over time.

Over the last several decades, we've seen a revolution in what we are able to represent and convey.
We can capture experiences with almost perfect fidelity, and disseminate it essentially instantaneously to an unlimited audience.
What's more, once information is in digital form, we can _compute_ over it, and gain insights that were simply not accessible in prior times.
At the heart of this revolution is this simple but profound observation that we can represent an unbounded variety of objects using a finite set of symbols (and in fact  using only the two symbols ```0``` and ```1```).^[There is nothing "holy" about using zero and one as the basic symbols, and we can (indeed sometimes people do) use any other finite set of two or more symbols as the fundamental "alphabet". We use zero and one in this course mainly because it simplifies notation.]

In later lectures, we will often fall back on taking this  representation for granted, and hence write something like "program $P$ takes $x$ as input" when $x$ could be a number, a vector, a graph, etc..,  when we really mean that $P$ takes as input the _representation_ of $x$ as a binary string.
However, in this lecture, let us dwell a little bit on how such representations can be devised.
We note that in many instances, choosing the "right" string representation for a piece of data is highly nontrivial, and finding the "best" one (e.g., most compact, best fidelity,  most efficiently manipulable, robust to errors, most informative features, etc..) is the object of intense research.
But for now, we will  focus on describing some simple representations for various natural objects.


### Representing natural numbers

Perhaps the simplest object we want to represent is a _natural number_.
That is, a member $x$ of the set $\N = \{0,1,2,3,\ldots \}$. We can represent a number $x\in\N$ as a string using the _binary basis_.
That is, we can write $x$ in a unique way as $x = x_02^0 + x_12^1 + \cdots + x_n2^n$  (or $\sum_{i=0}^n x_i 2^i$ for short) where $x_0,\ldots,x_n$ are zero/one and $n$ is the largest number such that $2^n \leq x$. We can then represent $x$ as the string $(x_0,x_1,\ldots,x_n)$.
For example, the number 35 will be represented as the string $(1,1,0,0,0,1)$ which we often also write as $110001$.^[Note that this is the reverse of the typical way we write numbers with the least significant digit as the rightmost one. Representing the number $x$ as $(x_n,x_{n-1},\ldots,x_0)$ will of course work just as well (in some contexts this is known as "Big Endian" vs. "Little Endian" representation). We chose the particular representation above for the sake of concreteness but such low level choices will not make a difference in this course.]

We can think of a representation as consisting of    _encoding_ and _decoding_ functions.
In the case of the _binary representation_ for integers, the _encoding_ function $E:\N \rightarrow \{0,1\}^*$ maps a natural number to the string representing it, and the _decoding_ function $D:\{0,1\}^* \rightarrow \N$ maps a string into the number it represents (i.e., $D(x_0,\ldots,x_{n-1})= 2^0x_0 + 2^1x_1 +\ldots + 2^{n-1}x_{n-1}$ for every $x_0,\ldots,x_n \in \{0,1\}$).


In the case of the binary representation, both the encoding and decoding functions are _one-to-one and onto functions_,^[Recall that a function $f$ mapping a set $U$ to a set $V$ is _one-to-one_ if $f(x)\neq f(x')$ for every $x\neq x'$ in $U$, and is _onto_ if for every $y\in V$ there is some $x$ s.t. $f(x)=y$.]   also known as _bijections_.^[Note that since in our convention $\N$ includes zero, the set $\{0,1\}^*$ includes the empty (i.e., length zero) string which will represent the number zero.]

### Representing (potentially negative) integers

Now that we can represent natural numbers, we can represent _whole numbers_ (i.e., members of the set $\Z=\{ \ldots, -3 , -2 , -1 , 0 , +1, +2, +3,\ldots \}$ ) by adding one more bit that represents the sign. So, the string $(\sigma,x_0,\ldots,x_n) \in \{0,1\}^{n+1}$ will represent the number
$$
(-1)^\sigma \left[ x_0 2^0 + \cdots x_n 2^n \right]
$$


For this representation, the decoding function is not one-to-one anymore: the two strings $1$ and $0$ both represent the number zero (since they can be thought of as representing $-0$ and $+0$ respectively, can you see why?).
The decoding function is also only a _partial_ function, since there is no number that is represented by the empty string.

But this is still a fine representation, since the encoding function still corresponds  the one-to-one total function $E:\Z \rightarrow \{0,1\}^*$ which maps an integer of the form $a\times k$, where $a\in \{\pm 1 \}$ and $k\in \N$ to the bit $(-1)^a$ concatenated with  the binary representation of $k$).
That is, every integer can be represented as a string, and two distinct integers have distinct representations.


__Interpretation:__  Given a string $x\in \{0,1\}^*$, how do we know if it's "supposed" to represent a (nonnegative) natural number  or a (potentially negative) integer?
For that matter, even if we know $x$ is "supposed" to be an integer, how do we know what representation scheme it uses?
The short answer is that we don't necessarily know this information, unless it is supplied from the context.^[In  programming language, the compiler or interpreter determines the representation of the sequence of bits corresponding to a variable based on the variable's _type_.]
We can treat the same string $x$ as representing a natural number, an integer, a piece of text, an image, or a green gremlin.
Whenever we say a sentence such as "let $n$ be the number represented by the string $x$", we will assume that we are fixing some canonical representation scheme such as the ones above.
The choice of the particular representation scheme will almost never matter, except that we want to make sure to stick with the same one for consistency.

### Representing rational numbers and prefix freeness

We can represent a rational number of the form $a/b$ by representing the two numbers $a$ and $b$ (again, this is not a unique representation but this is fine).
However, simply concatenating the representations of $a$ and $b$ will not work.
For example, recall that we   represent $4$ as $01$ and  $35$ as $110001$, but the concatenation  $01110001$ of these strings is also the concatenation of the representation $011$ of $6$ and the representation $10001$ of $17$.
Hence, if we used such simple concatenation then we would not be able to tell if the string $01110001$ is supposed to represent $4/35$ or  $6/17$.

The solution is to use a _prefix free_ encoding for the numbers.
An encoding of a set of objects into strings is _prefix free_ if for there are no two objects $o,o'$ such that the representation $x$ of $o$ is a _prefix_ of the representation $x'$ of $o'$. (The definition of prefix is as you would expect: a length $n$ string $x$ is a prefix of a length $n' \geq n$ string $x'$ if $x_i=x'_i$ for every $1 \leq i \leq n$.)
If we have a prefix free encoding for some set $\mathcal{O}$ then we can encode pairs or tuples of objects in $\mathcal{O}$ by simply concatenating the underlying representation.
That is, if $x_1,\ldots,x_k$ represent $o_1,\ldots,o_k$ then we can represent the tuple $(o_1,\ldots,o_k)$ simply by $x_1\cdots x_k$.
We can recover the list of original objects from their  representation as a string $x$ by finding the first prefix of $x$ that is a valid representation, decoding this prefix, and then removing it from $x$ and continuing onwards (see [prefix-free-tuples-ex](){.ref}).

![If we have a prefix-free representation of each object then we can concatenate the representations of $k$ objects to obtain a representation for the tuple $(o_1,\ldots,o_k)$.](../figure/repres_list.png){#figureid .class width=300px height=300px}

One simple way to transform every representation to a prefix-free representation is to include a special "end representation mark".
That is, suppose we modify every $0$ symbol to $00$ and every $1$ symbol to $11$ and append the two symbols $01$ to the end of the representation.
This would make the representation prefix-free (can you see why?) at the cost of roughly doubling its size (i.e., if the original representation had length $k$ then the new representation will have  length $2k+2$).
It is actually possible to have a more efficient prefix-free representation that encodes a $k$ bit string by a string of length at most $k+O(\log k)$, see [prefix-free-ex](){.ref}.

### Representing letters and text

We can represent a letter or symbol by a string, and then if this representation is prefix free, we can represent a sequence of symbols by simply concatenating the representation of each symbol.
One such representation is the [ASCII](https://en.wikipedia.org/wiki/ASCII) that represents $128$ letters and symbols as strings of $7$ bits.
Since it is a fixed-length representation it is automatically prefix free (can you see why?). [Unicode](https://en.wikipedia.org/wiki/Unicode) is a representation of (at the time of this writing) about 128,000 symbols into numbers (known as _code points_) between $0$ and  $1,114,111$.
There are several types of prefix-free representations of the code points, a popular one being [UTF-8](https://en.wikipedia.org/wiki/UTF-8) that encodes every codepoint into a string of length between $8$ and $32$.
<!-- (For example, the UTF-8 encoding for the "confused face" emoji 😕 is `11110000100111111001100010010101`) -->


### Representing real numbers

The _real numbers_ contain all numbers including positive, negative, and fractional, as well as _irrational_ numbers such as $\pi$ or $e$.
Every real number can be approximated by a rational number, and so up to a small error we can represent every real number $x$ by a rational number $a/b$ that is very close to $x$.
This is a fine representation though a more common choice to represent real numbers is the _floating point_ representation, where we represent $x$ by the pair $(a,b)$ of integers of some prescribed sizes (determined by the desired accuracy) such that $a2^{-b}$ is closest to $x$.
The reader might be (rightly) worried about this issue of approximation, but in many (thuogh not all) computational applications, one can make the accuracy tight enough so that this does not effect the final result.^[This is called "floating point" because we can think of the number $a$ as specifying a sequence of binary digits, and $b$ as describing the location of the "binary point" within this sequence. This internal representation is the reason why, for example, in   Python  typing `0.1+0.2` will result in `0.30000000000000004` and not `0.3`, see [here](http://floating-point-gui.de/), [here](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) and [here](https://randomascii.wordpress.com/2012/04/05/floating-point-complexities/) for more. A floating point error  has been implicated in the [explosion](http://sunnyday.mit.edu/accidents/Ariane5accidentreport.html) of the Ariane 5 rocket, a bug that cost more than 370 million dollars, and the [failure](http://embeddedgurus.com/barr-code/2014/03/lethal-software-defects-patriot-missile-failure/) of a U.S. Patriot missile to intercept an Iraqi Scud missile, costing 28 lives. Floating point is [often problematic](http://www.theregister.co.uk/2006/08/12/floating_point_approximation/) in financial applications as well.]
Also, some error in representing real numbers is _unavoidable_: there is no exact representation of real numbers as strings; see [cantor-ex](){.ref}.



### Representing vectors, matrices, images, graphs

Once we can represent numbers, and lists of numbers, then we can obviously represent _vectors_ (which are just lists of numbers).
Similarly, we can represent lists of lists and so in particular _matrices_.
To represent an image, we can represent the color at each pixel by a list of three numbers corresponding to the intensity of Red, Green and Blue.^[We can restrict to three basic colors since ([most](https://en.wikipedia.org/wiki/Tetrachromacy)) humans only have three types of cones in their retinas. We would have needed 16 basic colors to represent colors visible to the [Mantis Shrimp](https://en.wikipedia.org/wiki/Mantis_shrimp).]
Thus an image of $n$ pixels would be represented of a list of $n$ such length-three lists.
A video can be represented as a list of images.^[Of course these representations are rather wasteful and [much](https://en.wikipedia.org/wiki/JPEG) [more](https://en.wikipedia.org/wiki/H.264/MPEG-4_AVC) compact representations are typically used for images and videos, though this will not be our concern in this course.]

A _graph_ on $n$ vertices can be represented as an $n\times n$ matrix whose $(i,j)^{th}$ entry is equal to $1$ if the edge $(i,j)$ is present and is equal to $0$ otherwise. (We can also represent a graph using the so-called "adjacency list" representation, though the difference between these two representations will almost never matter for this course.)

## General definitions for representations

Generally, a _representation_ of set of objects $\mathcal{O}$ consists of a pair of _encoding_ and _decoding_ functions $E:\mathcal{O} \rightarrow \{0,1\}^*$ and $D:\{0,1\}^* \rightarrow \mathcal{O}$.
We require that $E$ is one-to-one   $D(G(o))=o$ for every $o\in \mathcal{O}$.

As mentioned, the decoding function $D$ might be a _partial_ function if not every string is a valid representation.
Often however we will ensure for the sake of convenience that $D$ is total by picking some fixed object $o_0 \in \mathcal{O}$ and  stipulating that $D(x)=o_0$ for every $x$ where $D$ would not otherwise be defined.

### Representing lists:

If we have a way of represent objects from a set $\mathcal{O}$ as  binary strings, then we can easily represent lists of these objects.
For starters, as mentoned above, we can convert any representation to a _prefix free_ representation.
Given a prefix-free encoding $E:\mathcal{O} \rightarrow  \{0,1\}^*$, we can encode a list such as $(o_1,o_2,o_3)$ simply as the concatenation of $o_1$,$o_2$ and $o_3$.

But we can also use a different approach, that doesn't require prefix-free-ness, and  can also handle _nested_ lists.
The idea is that if we have some representation $E:\mathcal{O} \rightarrow \{0,1\}^*$, then we can represent nested lists of items from $\mathcal{O}$ using strings over the five element alphabet $\Sigma = \{0,1,$`[` $,$ `]` $,$ `,` $\}$.
For example, if $o_1$ is represented by `0011`, $o_2$ is represented by `10011`, and $o_3$ is represented by `00111`, then we can represent the nested list $(o_1,(o_2,o_3))$ as the string `"[0011,[1011,00111]]"` over the alphabet $\Sigma$.
By encoding every element of $\Sigma$ itself as a three-bit string,
we can transform any representation for objects $\mathcal{O}$ into a representation that allows to represent (potentially nested) lists of these objects.
If we do not specify another representation scheme for lists, then we will assume that we use this method.



### Notation

We will typically identify an object with its representation as a string. For example, if $F:\{0,1\}^* \rightarrow  \{0,1\}^*$ is some function that maps strings to strings and $x$ is an integer, we might make statements such as "$F(x)+1$ is prime" to mean that if we represent $x$ as a string $\underline{x}$ and let $\underline{y}=F(\underline{x})$, then the integer $y$ represented by the string $\underline{y}$ satisfies that $y+1$ is prime. (You can see how this convention of identifying objects with their representation can save us a lot of cumbersome formalism.)
Similarly, if $x,y$ are some objects and $F$ is a function that takes strings as inputs, then by $F(x,y)$ we will mean the result of applying $F$ to the representation of the tuple $(x,y)$.

Note that this convention of identifying an object with its representation as a string is one that we humans follow all the time. For example, when people say a statement such as "$17$ is a prime number", what they really mean is that the integer whose representation in the decimal basis is the string "`17`", is prime.

## Defining computational tasks

Given the above, we will define a computational process as an object that takes an input which is a string of bits, and produces an output which is a string of bits.

![A computational process](../figure/computation.png){#figureid .class width=300px height=300px}

A _computational task_ defines the relation that the output needs to have with the input.
The simplest and most common task is simply _computing a function_.
That is, computing some deterministic map $F$ of $\{0,1\}^*$ to $\{0,1\}^*$.
A computational process $P$ computes a  function $F$ if for every input $x\in \{0,1\}^*$, the output of $P$ on input $x$, which we denote by $P(x)$, is equal to $F(x)$. ^[We will sometimes consider also _partial functions_, which are functions $F$ that are only defined on a subset of $\{0,1\}^*$.
In this case, we say that $P$ computes $F$ if $P(x)=F(x)$ for every $x$ on which $F$ is defined, where we don't care what is the output of $P$ on $x$'s  where $F$ is undefined.]
An important special case is when the function's output is a single bit $\{0,1\}$.
Computing such functions corresponds to answering a YES/NO question, and hence this task is also known as a _decision problem_.^[Computing a single-bit output _partial_ function $F$ corresponds to answering a YES/NO question on inputs that are promised to be in the set on which $F$ is defined. Hence this task is also known as solving a _promise problem_. See our note on terminology below.]


Computing functions or partial functions captures a very wide variety of computational tasks including:

* Given (a representation of) an integer $x$, decide if $x$ is prime or composite. (This corresponds to computing a function from $\{0,1\}^*$ to $\{0,1\}$, can you see why?)

* Given (a representation of) an integer $x$, compute its _factorization_; i.e., the list of primes $p_1 \leq \cdots \leq p_k$ such that $x = p_1\cdots p_k$. (This corresponds to computing a function from $\{0,1\}^*$ to $\{0,1\}^*$.)

* Given (a representation of) a logical true or false statement about the integers such as the Reimann Hypothesis, the twin prime conjecture, etc.., decide whether it is true or fale. (This corresponds to computing a partial function from $\{0,1\}^*$ to $\{0,1\}$; we can also make this a total function by arbitrarily assigning some trivial statement such as `1+1=2` to strings that do not correspond to a valid statement.)

* Given (a representation of) a graph $G$ and two vertices $s$ and $t$, compute the length of the shortest simple (i.e., non intersecting) path in $G$ between $s$ and $t$, or do the same for the _longest_ simple path between $s$ and $t$. (Both correspond to computing a function from $\{0,1\}^*$ to $\{0,1\}^*$, though it turns out that there is a huge difference in their computational difficulty.)

*  Given (a representation of) an image $I$, decide if $I$ is a photo of a cat or a dog. (This corresponds to a partial function from $\{0,1\}^*$ to $\{0,1\}$, though of course there is more than one partial function that would correspond to this task.)

etc.. etc..

Given every particular (partial) function $F$, there can be several possible _algorithms_ to compute this function.
We will be interested in questions such as:

* For a given function $F$, can it be the case that _there is no algorithm_ to compute $F$?

* If there is an algorithm, what is the best one? Could it be that $F$ is "effectively uncomputable" in the sense that every algorithm for computing $F$ requires an prohibitively large amount of resources?

* If we can't answer this question, can we show equivalence between different functions $F$ and $F'$ in the sense that either they are both easy or they are both hard?

* Can a function being hard to compute every be a _good thing_? Can we use it for applications in areas such as cryptography?

In order to do that, we will need to mathematically define the notion of an _algorithm_, which is what we'll do in the next lecture.

### Advanced note: beyond computing functions

Functions capture quite a lot of computational tasks, but one can consider more general settings as well.
One generalization is to consider _relations_ that may have more than one possible admissible output.
For example, a set of equations might have more than one solution.  
A _relation_ $R$ maps a string $x\in \{0,1\}^*$ into a _set of strings_ $R(x)$ (for example, $x$ might be description of a set of equations and $R(x)$ will be the set of all solution).
We can also identify a relation $R$ with the set of pairs of strings $(x,y)$ where $y\in R(x)$.
A computational process solves a relation if for every $x\in \{0,1\}^*$, it outputs some string $y\in R(x)$.
We can also consider _interactive_ computational tasks, such as finding good strategy in a game, etc..

Last but not least, our focus on the moment is on finding algorithms that correctly compute a function $F$ on _every_ input $x$.
This is sometimes known as _worst case analysis_.
We can also try to study algorithms that succeed on "typical" or "most" inputs, which is sometimes known as _average case complexity_.
This is often a more appropriate model in various data analysis and machine learning applications, though formalizing the notion of "typical" is highly non trivial.

We will consider various such generalizations later on in this course.
However, in the first several few lectures we will focus on the task of computing a function, and often even a _Boolean_ function, that has only a single bit of output.
It turns out that a great deal of the theory of computation can be studied in the context of this task, and the insights  learned are applicable in the more general settings.

### Terminology

Different texts on the theory of computation use somewhat different terminology to describe computational tasks.
As mentioned above, computing a _Boolean_ (i.e., with $0/1$ output) function $F:\{0,1\}^* \rightarrow \{0,1\}$ amounts to solving a YES/NO problem of whether $F(x)=0$ or $F(x)=1$.
Hence this task is also known as a _decision problem_.
We can identify a Boolean function $F$ with the set $L =  \{ x : F(x)=1 \}$ of the inputs on which it outputs $1$.
For historical reasons, such sets are often known as _languages_, and hence some texts use the term "deciding a language" for the task of computing a Boolean function.
We will not use this terminology in this course.

If $F$ is a _partial_ function, then computing $F$ amounts to solving the decision problem only on the inputs $x$ for which $F$ is defined. One way to think of this is that the algorithm is "promised" that its input $x$ is such that $F$ is defined on it (and if the promise is violated then the algorithm need not provide any guarantees on the output).
For this reason, computing a partial function $F$ is sometimes known as solving a _promise problem_.


## Lecture summary

* We can represent essentially every object we want to compute on using binary strings.
* A representation scheme for a set of objects $\mathcal{O}$ is a one-to-one map  from $\mathcal{O}$ to $\{0,1\}^*$.
* A basic computational task is the task of _computing a function_ $F:\{0,1\}^* \rightarrow \{0,1\}^*$. This encompasses not just arithmetical computations such as multiplication, factoring, etc.. but a great many other tasks arising in areas as diverse as scientific computing, artificial intelligence, image processing, data mining and many many more.
* We will study the question of finding (or at least giving bounds on) what is the _best_ algorithm for  computing $F$ for various interesting functions $F$.

## Exercises

> # {.exercise}
Which one of these objects can be represented by a binary string? \
   >a. An integer $x$  \
   >b. An undirected graph $G$. \
   >c. A directed graph $H$ \
   >d. All of the above.


> # {.exercise title="Multiplying in different representation" #multrepres }
Recall that the gradeschool algorithm for multiplying two numbers requires $O(n^2)$ operations. Suppose that instead of using decimal representation, we use one of the following representations $R(x)$ to represent a number $x$ between $0$ and $10^n-1$. For which one of these representations you can still multiply the numbers in $O(n^2)$ operations? \
   >a. The standard binary representation: $B(x)=(x_0,\ldots,x_{k})$ where $x = \sum_{i=0}^{k} x_i 2^i$ and $k$ is the largest number s.t. $x \geq 2^k$.  \
   >b. The reverse binary representation: $B(x) = (x_{k},\ldots,x_0)$ where $x_i$ is defined as above for $i=0,\ldots,n-1$. \
   >c. Binary coded decimal representation: $B(x)=(y_0,\ldots,y_{n-1})$ where $y_i \in \{0,1\}^4$ represents the $i^{th}$ decimal digit of $x$ mapping $0$ to $0000$, $1$ to $0001$, $2$ to $0010$, etc.. (i.e. $9$ maps to $1001$) \
   >d. All of the above.

> # {.exercise }
Suppose that $R:\N \rightarrow \{0,1\}^*$ corresponds to  representing a number $x$ as a string of $x$ $1$'s, (e.g., $R(4)=1111$, $R(7)=1111111$, etc..).
If $x,y$ are number between $0$ and $10^n -1$, can we still multiply $x$ and $y$ using $O(n^2)$ operations if we are given them in the representation $R(\cdot)$?

> # {.exercise }
Recall that if $F$ is a one-to-one and onto function mapping elements of a finite set $U$ into a finite set $V$ then the sizes of $U$ and $V$ are the same. Let $B:\N\rightarrow\{0,1\}^*$ be the function such that for every $x\in\N$, $B(x)$ is the binary representation of $x$. \
   >a. Prove that $x < 2^k$ if and only if $|B(x)| \leq k$. \
   >b. Use a. to compute the size of the set $\{ y \in \{0,1\}^* : |y| \leq k \}$ where $|y|$ denotes the length of the string $y$. \
   >c. Use a. and b. to prove that $2^k-1 = 1 + 2 + 4+ \cdots + 2^{k-1}$.

> # {.exercise  title="Prefix free encoding of tuples" #prefix-free-tuples-ex}
Suppose that $F:\N\rightarrow\{0,1\}^*$ is a one-to-one function that is _prefix free_ in the sense that there is no $a\neq b$ s.t.  $F(a)$ is a prefix of $F(b)$. \
   >a. Prove that $F_2:\N\times \N \rightarrow \{0,1\}^*$, defined as $F_2(a,b) = F(a)F(b)$ (i.e., the concatenation of $F(a)$ and $F(b)$) is a one-to-one function. \
   >b. Prove that $F_*:\N^*\rightarrow\{0,1\}^*$ defined as $F_*(a_1,\ldots,a_k) = F(a_1)\cdots F(a_k)$ is a one-to-one function, where $\N^*$ denotes the set of all finite-length lists of natural numbers.

> # {.exercise title="More efficient prefix-free transformation" #prefix-free-ex}
Suppose that $F:O\rightarrow\{0,1\}^*$ is some (not necessarily prefix free) representation of the objects in the set $O$, and $G:\N\rightarrow\{0,1\}^*$ is a prefix-free representation of the natural numbers.  Define $F'(o)=G(|F(o)|)F(o)$ (i.e., the concatenation of the representation of the length $F(o)$ and $F(o)$). \
   >a. Prove that $F'$ is a prefix-free representation of $O$. \
   >b. Show that we can transform any representation to a prefix-free one by a modification that takes a $k$ bit string into a string of length at most $k+O(\log k)$.
   >c. Show that we can transform any representation to a prefix-free one by a modification that takes a $k$ bit string into a string of length at most $k+ \log k + O(\log\log k)$.^[Hint: Think recursively how to represent the length of the string.]

> # {.exercise title="Kraft's Inequality" #prefix-free-lb}
Suppose that $S \subseteq \{0,1\}^n$ is some finite prefix free set. \
a. For every $k \leq n$ and length-$k$ string $x\in S$, let $L(x) \subseteq \{0,1\}^n$ denote all the length-$n$ strings whose first $k$ bits are $x_0,\ldots,x_{k-1}$. Prove that __(1)__ $|L(x)|=2^{n-|x|}$ and __(2)__ If $x \neq x'$ then $L(x)$ is disjoint from $L(x')$. \
b. Prove that $\sum_{x\in S}2^{-|x|} \leq 1$. \
c. Prove that there is no prefix-free encoding of strings with less than logarithmic overhead. That is, prove that there is no function $PF:\{0,1\}^* \rightarrow \{0,1\}^*$ s.t. $|PF(x)| \leq |x|+0.9\log |x|$ for every $x\in \{0,1\}^*$ and such that the set $\{ PF(x) : x\in \{0,1\}^* \}$ is prefix-free.


> # {.exercise title="No lossless representation of reals (challenge)" #cantor-ex}
In this exercise we will prove that there is no "lossless" representation of real numbers as stings. That is, that there is no one-to-one function $F$ mapping the real numbers $\R$ to the set of finite strings $\{0,1\}^*$. \
a. Suppose, towards the sake of contradiction, that there exists such a function $F: \R \rightarrow \{0,1\}^*$. Prove that there exists an onto function $G:\{0,1\}^* \rightarrow \R$. \
b. Prove that there is an onto function $G': \N \rightarrow \{0,1\}^*$. Conclude that  if there is an onto function $G:\{0,1\}^* \rightarrow \R$ then there exists an onto function $H: \N \rightarrow \R$.
c. For any real number $x$ and $i>0$,  define $D(x,i) \in \{0,\ldots, 9\}$ to be the $i^{th}$ decimal digit following the decimal point of $x$. That is, $D(x,i)$ is the remainder when we divide $\lfloor x 10^i \rfloor$ by $10$. For example $D(1/4,1)=2$, $D(1/4,2)=5$ and $D(1/4,i)=0$ for every $i>2$. Similarly,  $D(1/3,i)=3$ for every $i$.
Prove that if $x$ is between $0$ and $1$ then $x = \sum_{i=1}^{\infty} 10^{-i}D(x,i)$.^[__Hint:__ If you have not taken honors calculus, start by showing that this is true for the case where $x$ has finite decimal expansion, namely that there is some $n$ such that $D(x,i)=0$ for all $i>n$. Formally, what you need to prove for the infinite case is that for every $\epsilon>0$, there is some $n$ such that $|x-\sum_{i=1}^n 10^{-i}D(x,i)|<\epsilon$.] \
d. Let $S$ be the set of all functions from $\N$ to $\{0,1\}$ prove that the map $D:\R \rightarrow S$ that maps a number $x$ to the function $i \mapsto D(x,i) (\mod 2)$ is onto.^[__Hint:__ Show that for every function $f:\N \rightarrow \{0,1\}$, the number $x = \sum_{i=0}^\infty 10^{-i-1}f(i)$ satisfies $D(x)=f$.]
e. Prove that there is no onto map from $\N$  to $S$.^[__Hint:__ Suppose that there was such a map $O$, the we can define the function $f \in S$ such that $f(i)=1-O(i)(i)$ and show that it is not in the image of $O$.]
f. Combine a-e to get a contradiction to the assumption that there is one-to-one map from $\R$ to $\{0,1\}^*$.
^[TODO: can we have a proof that doesn't need people to know limits?]

## Bibliographical notes

The idea that we should separate the _definition_ or _specification_ of a function from its _implementation_ or _computation_ might seem "obvious", but it took some time for mathematicians to arrive at this viewpoint.
Historically, a function $F$ was  identified by  rules or formulas showing  how to derive the output from the input.
As we discuss in greater  depth in our lecture on uncomputability, in the 1800's this somewhat informal notion of a function started "breaking at the seams" and eventually mathematicians arrived at more rigorous notion that a function is simply any arbitrary assignment of input to outputs, and while many  functions may be described (or computed) by one or more  formulas, one can also have functions that do not correspond to any "nice" formula.

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

* _Succinct_ data structures. These are representations that map objects from some set $\mathcal{O}$ into strings of length not much larger than the minimum of $\log_2 |\mathcal{O}|$ but still enable fast access to certain queries, see for example [this paper](https://people.csail.mit.edu/mip/papers/succinct/succinct.pdf).

* We've mentioned that all  representations of the real numbers are inherently _approximate_. Thus an important endeavor is to understand what guarantees we can offer on the approximation quality of the output of an algorithm, as a function of the approximation quality of the inputs. This is known as the question of [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability).

* The linear algebraic view of graphs. The adjacency matrix representation of graphs is not merely a convenient way to map a graph into a binary string, but it turns out that many natural notions and operations on matrices are useful for graphs as well. (For example, Google's PageRank algorithm relies on this viewpoint.)  The notes of [this course](http://www.cs.yale.edu/homes/spielman/561/) are an excellent source for this area, known as _spectral graph theory_. We will discuss this view much later in this course when we talk about _random walks_.



## Acknowledgements

Thanks to Jarosław Błasiok for comments on the exercise on Cantor's Theorem.
