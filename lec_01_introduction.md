% Introduction chapter
% Boaz Barak


# Introduction { #chapintro }



> # { .objectives }
* Introduce and motivate the study of computation for its own sake, irrespective of particular implementations.
* The notion of an _algorithm_ and some of its history.
* Algorithms as not just  _tools_, but also _ways of thinking and understanding_.
* Taste of Big Oh analysis and surprising creativity in efficient algorithms.

>_"Computer Science is no more about computers than astronomy is about telescopes"_,  attributed to Edsger Dijkstra.^[This quote is typically read as disparaging the importance of actual physical computers in Computer Science, but note that telescopes are absolutely essential to astronomy as they provide us with the means to connect  theoretical predictions with actual experimental observations.]


>_"Hackers need to understand the theory of computation about as much as painters need to understand paint chemistry."_ , Paul Graham 2003.^[To be fair, in the following sentence Graham says "you need to know how to calculate time and space complexity and about Turing completeness". Apparently, NP-hardness, randomization, cryptography, and quantum computing are not essential to a hacker's education.]



>_"The subject of my talk is perhaps most directly indicated by simply
asking two questions: first, is it harder to multiply than to
add? and second, why?...I (would like to) show that there is no
algorithm for multiplication computationally as simple as that for
addition, and this proves something of a stumbling block."_,  Alan Cobham, 1964


The origin of much of science and medicine can be traced back to the ancient Babylonians.
But perhaps their greatest contribution to humanity was the invention of the _place-value number system_.
This is the idea that we can represent any number using a fixed number of digits, whereby the _position_ of the digit is used to determine the corresponding value, as opposed to system such as  Roman numerals, where every symbol has a fixed numerical value regardless of position.
For example, the distance to the moon is 238,900 of our miles or 259,956 Roman miles.
The latter quantity, expressed in standard Roman numerals is

```
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMDCCCCLVI
```

Writing the distance to the sun in Roman numerals would require about 100,000 symbols: a 50 page book just containing this single number!

This means that for someone who thinks of numbers in an additive  system like Roman numerals, quantities like the distance to the moon or sun are not merely large- they are _unspeakable_: cannot be expressed or even grasped.
It's no wonder that Eratosthene, who was the first person to calculate the earth's diameter (up to about ten percent error) and Hipparchus who was the first to calculate the distance to the moon, did not use a Roman-numeral type system but rather  the Babylonian sexadecimal (i.e., base 60) place-value system.

The Babylonians also invented the precursors of "standard algorithms" that we were all taught in elementary school for adding and multiplying numbers.^[For more on the actual algorithms the Babylonians used, see [Knuth's paper](http://steiner.math.nthu.edu.tw/disk5/js/computer/1.pdf) and Neugebauer's [classic book](https://www.amazon.com/Exact-Sciences-Antiquity-Neugebauer/dp/0486223329).]
These algorithms and their variants have  been  of course essential to people throughout history  working with abaci, papyrus, or pencil and paper, but in our computer age, do they really serve any purpose beyond torturing third graders?


To answer this question, let us try to see in what sense is the standard digit by digit multiplication algorithm "better" than the straightforward implementation of multiplication as iterated addition.
Let's start by more formally describing both algorithms:

>__Naive multiplication algorithm:__ \
>__Input:__ Non-negative integers $x,y$ \
>__Operation:__ \
>1. Let  $result \leftarrow 0$. \
>2. For $i=1,\ldots,y$: set $result \leftarrow result + x$ \
>3. Output $result$



>__Standard grade multiplication algorithm:__ \
>__Input:__ Non-negative integers $x,y$ \
>__Operation:__ \
>1. Let $n$ be number of digits of $y$, and set $result \leftarrow 0$. \
>2. For $i=0,\ldots,n-1$: set $result \leftarrow result + 10^i\times y_i \times x$, where $y_i$ is the $i$-th digit of $y$ (i.e. $y= 10^0 y_0 + 10^1y_1 + \cdots + y_{n-1}10^{n-1}$) \
>3. Output $result$

Both algorithms assume that we already know how to add numbers, and the second one also assumes that we can multiply a number by a power of $10$ (which is after all a simple shift) as well as multiply by a single-digit (which like addition, is done by multiplying each digit and propagating carries).
Now suppose that $x$ and $y$ are two numbers of $n$ decimal digits each.
Adding two such numbers takes at least $n$  single-digit additions (depending on how many times we need to use a "carry"), and so adding $x$ to itself $y$ times will take at least  $n\cdot y$ single-digit additions.
In contrast, the standard grade algorithm reduces this problem to taking $n$ products of $x$ with a single-digit (which require up to $2n$ single-digit operations each, depending on carries) and then adding all of those together (total of $n$ additions, which, again depending on carries, would cost at most $2n^2$ single-digit operations) for a total of at most $4n^2$ single-digit operations.
How much faster would $4n^2$ operations be than $n\cdot y$? And would this make any difference in a modern computer?

Let us consider the case of multiplying 64 bit or 20 digit numbers.^[This is a common size in several programming languages; for example the `long` data type in the Java programming language, and (depending on architecture) the `long` or `long long` types in C.]
That is, the task of multiplying two numbers $x,y$ that are between $10^{19}$ and $10^{20}$.
Since in this case $n=20$, the standard algorithm would use at most  $4n^2=1600$ single-digit operations, while repeated addition would require at least $n\cdot y \geq 20\cdot 10^{19}$ single-digit operations.
To understand the difference, consider that a human being might do a single-digit operation in about 2 seconds, requiring just under an hour to complete the calculation of $x\times y$ using the grade algorithm.
In contrast, even though it is more than a billion times faster, a modern PC that computes $x\times y$ using  naïve iterated addition would require about $10^{20}/10^9 = 10^{11}$ seconds (which is more than three millenia!) to compute the same result.

::: { .pause }
It is important to distinguish between the _value_ of a number, and the _length of its representation_ (i.e.,  the number of digits it has).
There is a big difference between the two: having \$1,000,000,000 is not the same as having \$10!
When talking about running time of algorithms, "less is more", and so an algorithm that runs in time proportional to the _number of digits_ of an input number (or even the number of digit squared) is much preferred to an algorithm that runs in time proportional to the _value_ of the input number.
:::

We see that computers have not made algorithms obsolete.
On the contrary, the vast increase in our ability to measure, store, and communicate data has led to a much higher demand for developing better and more sophisticated algorithms that can allow us to make better decisions based on these data.
We also see that to a large extent the notion of _algorithm_ is independent of the actual computing device that will execute it.
The digit-by-digit multiplication algorithm is vastly better than iterated addition, regardless whether the technology we use to implement it is a silicon based  chip, or a third grader with pen and paper.


Theoretical computer science is concerned with  the _inherent_ properties of algorithms and computation; namely, those properties that are _independent_ of current technology.
We ask some questions that were already pondered by the Babylonians, such as "what is the best way to multiply two numbers?", but also questions that rely on cutting-edge science such as "could we use the effects of quantum entanglement to factor numbers faster?".

In Computer Science parlance, a scheme such as the decimal (or sexadecimal) positional representation for numbers is known as a _data structure_, while the operations on this representations are known as _algorithms_.
Data structures and algorithms have enabled amazing applications, but their importance goes beyond  their practical utility.
Structures from computer science, such as bits, strings, graphs, and even the notion of a program itself, as well as concepts such as universality and replication, have not just found (many) practical uses but contributed a new language and a new way to view the world.

## Extended Example: A faster way to multiply {#karatsubasec }

Once you think of the standard digit-by-digit multiplication algorithm, it seems like obviously the "right" way to multiply numbers.
Indeed, in 1960, the famous mathematician Andrey Kolmogorov organized a seminar at Moscow State University in which he conjectured that every algorithm for multiplying two $n$ digit numbers would require a number of basic operations that is proportional to $n^2$.^[That is, he conjectured that the number of operations would be at least some $n^2/C$ operations for some constant $C$ or, using "Big Oh notation", $\Omega(n^2)$ operations. See the _mathematical background_ chapter for a precise definition of big Oh notation.]
Another way to say it, is that he conjectured that in any multiplication algorithm, doubling the number of digits would _quadruple_ the number of basic operations required.

A young student named Anatoly Karatsuba was in the audience, and within a week he found an algorithm that requires only about $Cn^{1.6}$ operations for some constant $C$.
Such a  number becomes  much smaller than $n^2$ as $n$ grows.^[At the time of this writing, the [standard Python multiplication implementation](https://svn.python.org/projects/python/trunk/Objects/longobject.c) switches from the elementary school algorithm to  Karatsuba's algorithm when multiplying numbers larger than 1000 bits long.]
Amazingly,  Karatsuba's algorithm is based on a faster way to multiply _two-digit_ numbers.

Suppose that $x,y \in [100]=\{0,\ldots, 99 \}$ are a pair of two-digit numbers.
Let's write $\overline{x}$ for the "tens" digit of $x$, and $\underline{x}$ for the "ones" digit, so that $x = 10\overline{x} + \underline{x}$, and write similarly $y = 10\overline{y} + \underline{y}$ for $\overline{y},\underline{y} \in [10]$.
The grade school algorithm for multiplying $x$ and $y$ is illustrated in [gradeschoolmult](){.ref}.

![The grade school multiplication algorithm illustrated for multiplying $x=10\overline{x}+\underline{x}$ and $y=10\overline{y}+\underline{y}$. It uses the formula $(10\overline{x}+\underline{x}) \times (10 \overline{y}+\underline{y}) = 100\overline{x}\overline{y}+10(\overline{x}\underline{y} + \underline{x}\overline{y}) + \underline{x}\underline{y}$.](../figure/gradeschoolmult.png){#gradeschoolmult .class width=300px height=300px}

The grade school algorithm  works by transforming the task of multiplying a pair of two-digit number into _four_ single-digit multiplications via the formula

$$
(10\overline{x}+\underline{x}) \times (10 \overline{y}+\underline{y}) = 100\overline{x}\overline{y}+10(\overline{x}\underline{y} + \underline{x}\overline{y}) + \underline{x}\underline{y} \label{eq:gradeschooltwodigit}
$$


Karatsuba's algorithm is based on the observation that we can express this also as

$$
(10\overline{x}+\underline{x}) \times (10 \overline{y}+\underline{y}) = (100-10)\overline{x}\overline{y}+10\left[(\overline{x}+\underline{x})(\overline{y}+\underline{y})\right]  -(10-1)\underline{x}\underline{y} \label{eq:karatsubatwodigit}
$$

which reduces multiplying the two-digit number $x$ and $y$ to computing the following three "simple" products:  $\overline{x}\overline{y}$, $\underline{x}\underline{y}$ and $(\overline{x}+\underline{x})(\overline{y}+\underline{y})$.^[The  term $(\overline{x}+\underline{x})(\overline{y}+\underline{y})$ is not exactly a single-digit multiplication as $\overline{x}+\underline{x}$ and $\overline{y}+\underline{y}$ are numbers between $0$ and $18$ and not between $0$ and $9$. As we'll see, it turns out that this  does not make much of a difference, since when we  use this algorithm recursively on $n$-digit numbers, this term will have at most $\ceil{n/2}+1$ digits, which is  essentially half the number of digits as the original input.]


![Karatsuba's multiplication algorithm illustrated for multiplying $x=10\overline{x}+\underline{x}$ and $y=10\overline{y}+\underline{y}$. We compute the three orange, green and purple products $\underline{x}\underline{y}$, $\overline{x}\overline{y}$ and $(\overline{x}+\underline{x})(\overline{y}+\underline{y})$ and then add and subtract them to obtain the result.](../figure/karatsubatwodigit.png){#karatsubafig .class width=300px height=300px}


Of course if all we wanted to was to multiply two digit numbers, we wouldn't really need any clever algorithms.
It turns out that we can repeatedly apply the same idea, and use them to multiply $4$-digit numbers, $8$-digit numbers, $16$-digit numbers, and so on and so forth.
If we used the grade school  approach then our cost for doubling the number of digits would be to _quadruple_ the number of multiplications, which for $n=2^\ell$ digits would result in about $4^\ell=n^2$ operations.
In contrast, in Karatsuba's approach doubling the number of digits  only  _triples_ the number of operations,  which means that for $n=2^\ell$ digits we require about $3^\ell = n^{\log_2 3} \sim n^{1.58}$ operations.

Specifically, we use a  _recursive_ strategy as follows:

>__Karatsuba Multiplication:__ \
>__Input:__ nonnegative integers $x,y$ each of at most $n$ digits \
>__Operation:__ \
>1. If $n \leq 2$ then return $x\cdot y$ (using a constant number of single-digit multiplications) \
>2. Otherwise, let $m = \floor{n/2}$, and write $x= 10^{m}\overline{x} + \underline{x}$ and $y= 10^{m}\overline{y}+ \underline{y}$.^[Recall that for a number $x$, $\floor{x}$ is obtained by "rounding down" $x$ to the largest integer smaller or equal to  $x$.]  \
>2. Use _recursion_ to compute  $A=\overline{x}\overline{y}$, $B=\underline{y}\underline{y}$ and $C=(\overline{x}+\underline{x})(\overline{y}+\underline{y})$. Note that all the numbers will have at most $m+1$ digits.  \
>3. Return $(10^n-10^m)\cdot A  + 10^m \cdot B +(1-10^m)\cdot C$

To understand why the output will be correct, first note that for $n>2$, it will always hold that  $m<n-1$, and hence the recursive calls will always be for multiplying numbers with a smaller number of digits, and (since eventually we will get to single or double digit numbers)  the algorithm will indeed terminate.
Now, since $x= 10^{m}\overline{x} + \underline{x}$ and $y= 10^{m}\overline{y}+ \underline{y}$,

$$
x \times y = 10^n \overline{x}\cdot \overline{y} + 10^{m}(\overline{x}\overline{y} +\underline{x}\underline{y}) + \underline{x}\underline{y}  \;. \label{eqkarastubaone}
$$

Rearranging the terms we see that

$$
x\times y =   10^n\overline{x}\cdot \overline{y} + 10^{m}\left[ (\overline{x}+\underline{x})(\overline{y}+\underline{y}) - \underline{x}\underline{y}  - \overline{x}\overline{y} \right]  + \underline{x}\underline{y} \;,
 \label{eqkarastubatwo}
$$

which equals to the value $(10^n-10^m)\cdot A  + 10^m \cdot B +(1-10^m)\cdot C$ returned by the algorithm.


The key observation is that  [eqkarastubatwo](){.eqref} reduces the task of computing the product of two $n$-digit numbers to computing _three_ products of  $\ceil{n/2}$-digit numbers.
Specifically, we can compute $x\times y$ from the three products $\overline{x}\overline{y}$, $\underline{y}\underline{y}$ and $(\overline{x}+\underline{x})(\overline{y}+\underline{y})$), using a constant number (in fact eight) of additions, subtractions, and multiplications by $10^n$ or $10^{\floor{n/2}}$.
(Multiplication by a power of ten can be done very efficiently as it corresponds to simply shifting the digits.)
Intuitively this means that as the number of digits _doubles_, the cost of performing a multiplication via Karatsuba's algorithm _triples_  instead of quadrupling, as happens in the naive algorithm.
This implies that multiplying numbers of $n=2^\ell$ digits costs about $3^\ell = n^{\log_2 3} \sim n^{1.585}$ operations.
In a [karatsuba-ex](){.ref}, you will formally show that the number of single-digit operations that Karatsuba's algorithm uses for multiplying $n$ digit integers is at most $O(n^{\log_2 3})$ (see also [karatsubafig](){.ref}).

![Running time of Karatsuba's algorithm vs. the Grade school algorithm. (Python implementation available [online](https://goo.gl/zwzpYe).) Note the existence of a "cutoff" length, where for sufficiently large inputs Karatsuba becomes more efficient than the grade algorithm. The precise cutoff location varies by implementation and platform details, but will always occur eventually.](../figure/karastubavsgschoolv2.png){#karatsubaruntimefig .class width=300px height=300px}

![Karatsuba's algorithm reduces an $n$-bit multiplication to three $n/2$-bit multiplications, which in turn are reduced to nine $n/4$-bit multiplications and so on. We can represent the computational cost of all these multiplications in a $3$-ary tree of depth $\log_2 n$, where at the root the extra cost is $cn$ operations, at the first level the extra cost is $c(n/2)$ operations, and at each of the $3^i$ nodes of  level $i$, the extra cost is $c(n/2^i)$. The total cost is $cn\sum_{i=0}^{\log_2 n} (3/2)^i \leq 2cn^{\log_2 3}$ by the formula for summing a geometric series.](../figure/karatsuba_analysis.png){#karatsuba-fig .class width=300px height=300px}


::: {.remark title="Ceilings, floors, and rounding" #remfloors}
One of the benefits of using big Oh notation is that we can allow ourselves to be a little looser with issues such as rounding numbers etc..
For example, the natural way to describe Karatsuba's algorithm's running time is via the   following  recursive equation

$$T(n)= 3T(n/2)+O(n)$$

but of course if $n$ is not even then we cannot recursively invoke the algorithm on $n/2$-digit integers.
Rather, the true recursion is $T(n) = 3T(\floor{n/2}+1)+ O(n)$.
However, this will not make much difference when we don't worry about constant factors, since it's not hard to show that $T(n+O(1)) \leq T(n)+ o(T(n))$ for the functions we care about.
Another way to show that this doesn't hurt us is to note that for every number $n$, we can find a number $n' \leq 2n$, such that $n'$ is a power of two.
Thus we can always "pad" the input by adding some input bits to make sure the number of digits is a power of two, in which case we will never run into these rounding issues.
These kind of tricks work not just in the context of multiplication algorithms but in many other cases as well.
Thus most of the time we can safely ignore these kinds of "rounding issues".
:::




### Beyond Karatsuba's algorithm

It turns out that the ideas of Karatsuba can be further extended to yield asymptotically faster multiplication algorithms, as was shown by Toom and Cook in the 1960s.
But this was not the end of the line.
In 1971, Schönhage and Strassen gave an even faster algorithm using the _Fast Fourier Transform_; their idea was to somehow treat integers as "signals" and do the multiplication more efficiently by moving to the Fourier domain.^[The _Fourier transform_ is a central tool in mathematics and engineering, used in a great number of applications. If you have not seen it yet, you will hopefully encounter it at some point in your studies.]
The latest asymptotic improvement was given by Fürer in 2007 (though it only starts beating  the Schönhage-Strassen algorithm for truly astronomical numbers).
And yet, despite all this progress, we still don't know whether or not there is an $O(n)$ time algorithm for multiplying two $n$ digit numbers!





:::  {.remark title="Matrix Multiplication (advanced note)" #matrixmult}
(We will  have several such "advanced" or "optional" notes and sections throughout this book. These may assume background that not every student has, and  can be safely skipped over as none of the future parts will depend on them.)

It turns out that a  similar idea as Karatsuba's can be used to speed up _matrix_ multiplications as well.
Matrices are a powerful way to represent linear equations and operations, widely used in a great many applications of scientific computing, graphics, machine learning, and many many more.

One of the basic operations one can do with two matrices is to _multiply_ them.
For example, if $x =   \begin{pmatrix} x_{0,0} & x_{0,1}\\ x_{1,0}& x_{1,1} \end{pmatrix}$ and $y =  \begin{pmatrix} y_{0,0} & y_{0,1}\\ y_{1,0}& y_{1,1} \end{pmatrix}$ then the product of $x$ and $y$ is the matrix $\begin{pmatrix} x_{0,0}y_{0,0} + x_{0,1}y_{1,01} & x_{0,0}y_{1,0} + x_{0,1}y_{1,1}\\ x_{1,0}y_{0,0}+x_{1,1}y_{1,0}  & x_{1,0}y_{0,1}+x_{1,1}y_{1,1} \end{pmatrix}$.
You can see that we can compute this matrix by _eight_ products of numbers.

Now suppose that $n$ is even and $x$ and $y$ are a pair of  $n\times n$ matrices which we can think of as each composed of four $(n/2)\times (n/2)$ blocks $x_{0,0},x_{0,1},x_{1,0},x_{1,1}$ and $y_{0,0},y_{0,1},y_{1,0},y_{1,1}$.
Then the formula for the matrix product of $x$ and $y$ can be expressed in the same way as above, just replacing products $x_{a,b}y_{c,d}$ with _matrix_ products, and addition with matrix addition.
This means that we can use the formula above to give an algorithm that _doubles_ the dimension of the matrices at the expense of increasing the number of operation by a factor of $8$, which for $n=2^\ell$ will result in $8^\ell = n^3$ operations.


In 1969 Volker Strassen noted that we can compute the product of a pair of two-by-two matrices  using only _seven_ products of numbers by observing that each entry of the matrix $xy$ can be computed by adding and subtracting the following seven terms: $t_1 = (x_{0,0}+x_{1,1})(y_{0,0}+y_{1,1})$, $t_2 = (x_{0,0}+x_{1,1})y_{0,0}$, $t_3 = x_{0,0}(y_{0,1}-y_{1,1})$, $t_4 = x_{1,1}(y_{0,1}-y_{0,0})$, $t_5 = (x_{0,0}+x_{0,1})y_{1,1}$, $t_6 = (x_{1,0}-x_{0,0})(y_{0,0}+y_{0,1})$,
$t_7 = (x_{0,1}-x_{1,1})(y_{1,0}+y_{1,1})$.
Indeed, one can verify that $xy = \begin{pmatrix}   t_1 + t_4 - t_5 + t_7 & t_3 + t_5 \\ t_2 +t_4 & t_1 + t_3 - t_2 + t_6 \end{pmatrix}$.


Using this observation, we can obtain an algorithm such that doubling the dimension of the matrices results in increasing the number of operations by a factor of  $7$, which means that for $n=2^\ell$ the cost is $7^\ell = n^{\log_2 7} \sim n^{2.807}$.
A long sequence of works has since improved this algorithm, and the [current record](https://en.wikipedia.org/wiki/Matrix_multiplication_algorithm#Sub-cubic_algorithms) has running time about $O(n^{2.373})$.
However, unlike the case of integer multiplication, at the moment we don't know of any algorithm for matrix multiplication that runs in time linear or even close to linear in the size of the input matrices (e.g., an $O(n^2 polylog(n))$ time algorithm).
People have tried to use [group representations](https://en.wikipedia.org/wiki/Group_representation), which can be thought of as generalizations of the Fourier transform, to obtain faster algorithms, but this effort [has not yet succeeded](http://discreteanalysisjournal.com/article/1245-on-cap-sets-and-the-group-theoretic-approach-to-matrix-multiplication).
:::


## Algorithms beyond arithmetic

The quest for better algorithms is by no means restricted to arithmetical tasks such as adding, multiplying or solving equations.
Many _graph algorithms_, including algorithms for finding paths, matchings, spanning tress, cuts, and flows, have been discovered in the last several decades, and this is still an intensive area of research.
(For example,  the last few years saw many advances in algorithms for the _maximum flow_ problem, borne out of surprising connections with electrical circuits and linear equation solvers.)
These algorithms are being used not just for the "natural" applications of routing network traffic or GPS-based navigation, but also for applications as varied as drug discovery through searching for structures in  gene-interaction graphs to computing risks from correlations in financial investments.


Google was founded based on the _PageRank_ algorithm, which is an efficient algorithm to approximate the "principal eigenvector" of (a dampened version of) the adjacency matrix of web graph.
The _Akamai_ company was founded based on a new data structure, known as _consistent hashing_, for a hash table where buckets are stored at different servers.
The _backpropagation algorithm_, which computes partial derivatives of a neural network in $O(n)$ instead of $O(n^2)$ time, underlies many of the recent phenomenal successes of  learning deep neural networks.
Algorithms for solving  linear equations under sparsity constraints, a concept known as _compressed sensing_, have been used to drastically reduce the amount and quality of data needed to analyze MRI images.
This is absolutely crucial for MRI imaging of cancer tumors in children, where previously doctors needed to use anesthesia to suspend breath during the MRI exam, sometimes with dire consequences.

Even for classical questions, studied through the ages, new discoveries are still being made.
For example, for the question of determining whether a given integer is  prime or composite, which has been studied since the days of  Pythagoras, efficient probabilistic algorithms were only discovered in the 1970s, while the first [deterministic polynomial-time algorithm](https://en.wikipedia.org/wiki/AKS_primality_test) was only found in 2002.
For the related problem of actually finding the factors of a composite number, new algorithms were found in the 1980s, and (as we'll see later in this course) discoveries in the 1990s  raised the tantalizing prospect of obtaining faster algorithms through the use of quantum mechanical effects.

Despite all this progress, there are still many more questions than answers in the world of algorithms.
For almost all natural problems, we do not know whether the current algorithm is the "best", or whether a significantly  better one is still waiting to be discovered.
As we already saw, even for the classical problem of multiplying numbers we have not yet answered the age-old question of __"is multiplication harder than addition?"__ .

But at least we now know the right way to _ask_ it.



## On the importance of negative results.

Finding better multiplication algorithms is undoubtedly a worthwhile endeavor.
But why is it important  to prove that such algorithms _don't_ exist?
What useful applications could possibly arise from an impossibility result?


One motivation is pure intellectual curiosity.
After all, this is a question even Archimedes could have been excited about.
Another reason to study impossibility results is that they correspond to the fundamental limits of our world.
In other words, they are _laws of nature_.
In physics, the impossibility of building a _perpetual motion machine_ corresponds to the _law of conservation of energy_.
The impossibility of building  a heat engine beating Carnot's bound corresponds to the second law of thermodynamics, while the impossibility of faster-than-light information transmission is a cornerstone of  special relativity.

In mathematics, while we all learned the solution for quadratic equations in high school, the impossibility of generalizing this to equations of degree five or more gave  birth to _group theory_.
Another example of an impossibility result comes from geometry.
For two millennia, mathematicians tried to show that Euclid's fifth axiom or "postulate" could be derived from the first four.
(This fifth postulate was known a the  "parallel postulate", and roughly speaking it states that every line has a unique parallel line of each distance.)
It was shown to be impossible using constructions of so called "non-Euclidean geometries", which turn out to be crucial  for the theory of general relativity.

::: {.remark title="" #id}
It is fine if you have not yet encountered many of the above examples.
I hope however that they spark your curiosity!
:::

In an analogous way, impossibility results for computation correspond to "computational laws of nature" that tell us about the fundamental limits of any information processing apparatus, whether based on silicon, neurons, or quantum particles.^[Indeed,  some [exciting recent research](http://www.scottaaronson.com/barbados-2016.pdf) is focused on  trying to use computational complexity to shed light on fundamental questions in physics such understanding black holes and reconciling general relativity with quantum mechanics.]
Moreover, computer scientists have recently been finding creative approaches to _apply_ computational limitations to achieve certain useful tasks.
For example, much of modern Internet traffic is encrypted using the RSA encryption scheme, which relies on its security on the (conjectured) impossibility of efficiently  factoring large integers.
More recently, the [Bitcoin](https://en.wikipedia.org/wiki/Bitcoin) system uses a digital analog of the "gold standard" where, instead of using a  precious metal,  new currency is obtained by "mining"  solutions for computationally difficult problems.



> # { .recap }
* The history of algorithms goes back thousands of years;  they have been essential much of human progress and these days form the basis of multi-billion dollar industries, as well as life-saving technologies.
* There is often more than one algorithm to achieve the same computational task. Finding a faster algorithm can often make a much bigger difference than improving computing hardware.
* Better algorithms and data structures don't just speed up calculations, but can yield  new qualitative insights.
* One question we will study is to find out what  is  the _most efficient_ algorithm for a given  problem.
* To show that an algorithm is the most efficient one for a given problem,  we need to be able to _prove_ that it is _impossible_ to solve the  problem using a smaller amount of computational resources.

## Roadmap to the rest of this course {#roadmapsec }

Often, when we try to solve a computational problem, whether it is solving a system of  linear equations, finding the top eigenvector of a matrix, or trying to rank Internet search results, it is enough to use the "I know it when I see it" standard for describing algorithms.
As long as we find some way to solve the problem, we are happy and  don't care so much about  formal descriptions of the algorithm.
But when we want to answer a question such as "does there _exist_ an algorithm to solve the problem $P$?" we need to be much more precise.

In particular, we will  need to __(1)__  define exactly what  it means to solve $P$, and __(2)__  define exactly what  an algorithm is.
Even __(1)__ can sometimes be non-trivial but __(2)__ is particularly challenging; it is not at all clear how (and even whether) we can encompass all potential ways to design algorithms.
We will consider several simple _models of computation_, and argue that, despite their simplicity, they do capture all "reasonable" approaches to achieve computing, including all those that are currently used in modern computing devices.

Once we have these formal models of computation, we can try to obtain _impossibility results_ for computational tasks, showing that some problems _can not be solved_ (or perhaps can not be solved within the resources of our universe).
Archimedes once said that given a fulcrum and a long enough lever, he could move the world.
We will see how _reductions_ allow us  to leverage one hardness result into a slew of a great many others, illuminating the boundaries between the computable and uncomputable (or tractable and intractable) problems.

Later in this course we will go back to examining our models of computation, and see how resources such as randomness or quantum entanglement could potentially change the power of our model.
In the context of  probabilistic algorithms, we will see a glimpse of how randomness  has become an indispensable tool for understanding computation, information, and communication.
We will also see how  computational difficulty can be an asset rather than a hindrance, and be used for the   "derandomization" of probabilistic algorithms.
The same ideas also show up in _cryptography_, which has undergone not just a technological but also an intellectual revolution in the last few decades, much of it building on the foundations that we explore in this course.

Theoretical Computer Science is a vast topic, branching out and touching upon many scientific and engineering disciplines.
This course only provides a very partial (and biased) sample of this area.
More than anything, I hope I will manage to "infect" you with at least some of my love for this field, which is inspired and enriched by the connection to practice, but which I find to be  deep and  beautiful regardless of   applications.

### Dependencies between chapters

This book is divided into the following parts:

* __Preliminaries:__ Introduction, mathematical background, and representing objects as strings.

* __Part I: Finite computation:__ Boolean circuits / straightline  programs. Universal gatesets, counting lower bound, representing programs as string and universality.

* __Part II: Uniform computation:__ Turing machines / programs with loops. Equivalence of models (including RAM machines and $\lambda$ calculus), universality, uncomputability,  Gödel's incompleteness theorem, restricted models (regular and context free languages).

* __Part III: Efficient computation:__ Definition of running time, time hierarchy theorem, $\mathbf{P}$ and $\mathbf{NP}$, $\mathbf{NP}$ completeness, space bounded computation.

* __Part IV: Randomized computation:__ Probability, randomized algorithms, $\mathbf{BPP}$, amplification, $\mathbf{BPP} \subseteq \mathbf{P}_{/poly}$, pseudrandom generators and derandomization.

* __Part V: Advanced topics:__ Cryptography, proofs and algorithms (interactive and zero knowledge proofs, Curry-Howard correspondence), quantum computing.

The book proceeds in linear order, with each chapter building on the previous one, with the following exceptions:


* All chapters in [advancedpart](){.ref} (Advanced topics) are independent of one another, and you can choose which one of them to read.

* [godelchap](){.ref} (Gödel's incompleteness theorem), [restrictedchap](){.ref} (Restricted computational models),  and [spacechap](){.ref} (Space bounded computation), are not used in following  chapters. Hence you can choose to skip them.

A course based on this book can use all of Parts I, II, and III  (possibly skipping over some or all of [godelchap](){.ref}, [restrictedchap](){.ref} or [spacechap](){.ref}), and then either cover all or some of Part IV, and add a "sprinkling" of advanced topics from Part V based on student or instructor interest.







## Exercises

::: {.remark title="Disclaimer" #disclaimerrem}
Most of the exercises have been written in the summer of 2018 and haven't yet been fully debugged. While I would prefer people do not post online solutions to the exercises, I would greatly appreciate if you let me know of any bugs. You can do so by posting a [GitHub issue](https://github.com/boazbk/tcs/issues) about the exercise, and optionally complement this with an email to me with more details about the attempted solution.
:::


::: {.exercise }
Rank the significance of the  following inventions in speeding up multiplication of large (that is 100 digit or more) numbers. That is, use "back of the envelope" estimates to order them in terms of the speedup factor they offered over the previous state of affairs.

a. Discovery of the grade style digit by digit algorithm (improving upon repeated addition)

b. Discovery of Karatsuba's algorithm (improving upon the digit by digit algorithm)

c.  Invention of modern electronic computers (improving upon calculations with pen and paper).
:::

::: {.exercise}
The 1977  Apple II personal computer had a processor speed of 1.023 Mhz or about $10^6$ operations per seconds. At the time of this writing the world's fastest supercomputer performs 93 "petaflops" ($10^{15}$ floating point operations per second) or about $10^{18}$ basic steps per second. For each one of the following running times (as a function of the input length $n$), compute for both computers how large an input  they could handle in a week of computation, if they run an algorithm that has this running time:

a. $n$ operations.

b. $n^2$ operations.

c. $n\log n$ operations.

d. $2^n$ operations.

e. $n!$ operations.
:::

::: {.exercise title="Analysis of Karatsuba's Algorithm" #karatsuba-ex}

a. Suppose that $T_1,T_2,T_3,\ldots$ is a sequence of numbers such that $T_2 \leq 10$ and for every $n$, $T_n \leq 3T_{\lceil n/2 \rceil} + Cn$. Prove that $T_n \leq 10Cn^{\log_2 3}$ for every $n$.^[__Hint:__ Use a proof by induction - suppose that this is true for all $n$'s from $1$ to $m$, prove that this is true also for $m+1$.] \

b. Prove that the number of single-digit operations that Karatsuba's algorithm takes to multiply two $n$ digit numbers is at most $1000n^{\log_2 3}$.

:::

> # {.exercise }
Implement in the programming language of your choice functions ```Gradeschool_multiply(x,y)``` and ```Karatsuba_multiply(x,y)``` that take two arrays of digits ```x``` and ```y``` and return an array representing the product of ```x``` and ```y``` (where ```x``` is identified with the number ```x[0]+10*x[1]+100*x[2]+...``` etc..) using the grade algorithm and the Karatsuba algorithm respectively. At what number of digits does the Karatsuba algorithm beat the grade one?


::: {.exercise title="Matrix Multiplication (optional, advanced)" #matrixex}
In this exercise, we show that if  for some $\omega>2$, we can write the product of two $k\times k$ real-valued matrices $A,B$ using at most $k^\omega$ multiplications, then we can multiply two $n\times n$ matrices in roughly $n^\omega$ time for every large enough $n$.

To make this precise, we need to make some notation that is unfortunately somewhat cumbersome. Assume that there is some $k\in \N$ and $m \leq k^\omega$ such that for every $k\times k$ matrices $A,B,C$ such that $C=AB$, we can write for every $i,j \in [k]$:
$$
C_{i,j} = \sum_{\ell=0}^m \alpha_{i,j}^\ell f_\ell(A)g_\ell(B)
$$
for some linear functions $f_0,\ldots,f_{m-1},g_0,\ldots,g_{m-1}:\mathbb{R}^{n^2} \rightarrow \mathbb{R}$ and coefficients $\{ \alpha_{i,j}^\ell \}_{i,j \in [k],\ell \in [m]}$.
Prove that under this assumption  for every $\epsilon>0$, if $n$ is sufficiently large, then there is an algorithm that computes the product of two $n\times n$ matrices using at most $O(n^{\omega+\epsilon})$ arithmetic operations.^[_Hint:_ Start by showing this for the case that $n=k^t$ for some natural number $t$, in which case you can do so recursively by breaking the matrices into $k\times k$ blocks.]
:::

## Bibliographical notes

For an overview of what we'll see in this course, you could do far worse than read [Bernard Chazelle's wonderful essay on the Algorithm as an Idiom of modern science](https://www.cs.princeton.edu/~chazelle/pubs/algorithm.html).

## Further explorations

Some topics related to this chapter that might be accessible to advanced students include:

* The _Fourier transform_, the _Fast_ Fourier transform algorithm and how to use it multiply polynomials and integers. [This lecture of Jeff Erickson](http://jeffe.cs.illinois.edu/teaching/algorithms/notes/02-fft.pdf) (taken from his [collection of notes](http://jeffe.cs.illinois.edu/teaching/algorithms/) ) is a very good starting point.  See also this [MIT lecture](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2012/lecture-notes/MIT6_046JS12_lec05.pdf) and this [popular article](http://www.ams.org/samplings/feature-column/fcarc-multiplication).

* Fast matrix multiplication algorithms, and the approach of obtaining exponent two via group representations.

* The proofs of some of the classical impossibility results in mathematics we mentioned, including the impossibility of proving Euclid's fifth postulate from the other four, impossibility of trisecting an angle with a straightedge and compass and the impossibility of solving a quintic equation via radicals. A geometric proof of the impossibility of angle trisection (one of the three [geometric problems of antiquity](http://mathworld.wolfram.com/GeometricProblemsofAntiquity.html), going back to the ancient greeks) is given in this [blog post of Tao](https://terrytao.wordpress.com/2011/08/10/a-geometric-proof-of-the-impossibility-of-angle-trisection-by-straightedge-and-compass/). [This book of Mario Livio](https://www.amazon.com/dp/B000FCKGVQ/) covers some of the background and ideas behind these impossibility results.
