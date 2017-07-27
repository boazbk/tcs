# Introduction

>_"Computer Science is no more about computers than astronomy is about telescopes"_,  attributed to Edsger Dijkstra.^[This quote is typically read as disparaging the importance of actual physical computers in Computer Science, but note that telescopes are absolutely essential to astronomy and are our only means of connecting theoretical speculations with actual experimental observations.]

>_"Hackers need to understand the theory of computation about as much as painters need to understand paint chemistry."_ , Paul Graham 2003.^[To be fair, in the following sentence Graham says "you need to know how to calculate time and space complexity and about Turing completeness", which will be taught in this course. Apparently, NP-hardness, randomization, cryptography, and quantum computing are not essential to a hacker's education.]

>_"The subject of my talk is perhaps most directly indicated by simply
asking two questions: first, is it harder to multiply than to
add? and second, why?...I (would like to) show that there is no
algorithm for multiplication computationally as simple as that for
addition, and this proves something of a stumbling block."_,  Alan Cobham, 1964


The origin of much of science and medicine can be traced back to the ancient Babylonians.
But perhaps their greatest contribution to society was the invention of the _place-value number system_.
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

Writing the distance to the sun in Roman numerals would require about 100,000 symbols.

This means that for someone that thinks of numbers in an additive  system like Roman numerals, quantities like the distance to the moon or sun are not merely large- they are _unspeakable_: cannot be expressed or even grasped.
It's no wonder that Eratosthene, who was the first person to calculate the earth's diameter (up to about ten percent error) and Hipparchus who was the first to calculate the distance to the moon, did not use a Roman-numeral type system but rather  the Babylonian sexadecimal (i.e., base 60) place-value system.

The Babylonians also invented the precursors of "standard algorithms" that we were all taught in elementary school for adding and multiplying numbers.^[For more on the actual algorithms the Babylonians used, see [Knuth's paper](http://steiner.math.nthu.edu.tw/disk5/js/computer/1.pdf) and Neugebauer's [classic book](https://www.amazon.com/Exact-Sciences-Antiquity-Neugebauer/dp/0486223329).]
These algorithms and their variants have  been  of course essential to people throughout history  working with abaci, papyrus, or pencil and paper, but in our computer age, do they really serve any purpose beyond torturing third graders?

To answer this question, let us try to see in what sense is the standard digit by digit multiplication algorithm "better" than the straightforward implementation of multiplication as iterated addition. Suppose that $x$ and $y$ are two numbers of $n$ decimal digits each. Adding two such numbers takes between $n$ to $2n$ single digit additions (depending on how many times we need to use a "carry"), and so adding $x$ to itself $y$ times will take between $n\cdot y$ to $2n\cdot y$ single digit additions.^[Actually the number of single digit additions might grow up to $3n\cdot y$ since as we add $x$ to itself the number of digits in our running sum could reach $2n$.] In contrast, the standard algorithm reduces this problem to taking $n$ products of $x$ with a single digit (which require up to $2n$ single digit operations each, depending on carries) and then adding all of those together (total of $n$ additions, which would cost at most $2n\cdot n$ single digit operations) for a total of at most $4n^2$ single digit operations. How much faster would $4n^2$ operations be than $n\cdot y$? and would this make any difference in a modern computer?

Let us consider the case of multiplying so called "double precision"  64 bit or 20 digit numbers.
That is, the task of multiplying two numbers $x,y$ that are between $10^{19}$ and $10^{20}$.
Since in this case $n=20$, the standard algorithm would use at most  $4n^2=1600$ single digit operations, while repeated addition would require at least $n\cdot y \geq 20\cdot 10^{19}$ single digit operations. To understand the difference, a human being might do a single digit operation in about 2 seconds, requiring just under an hour to complete the calculation, while a modern 4Ghz processor might be able to do $10^{10}$ single digit calculations in one second, and hence would take about $10^{10}$ seconds or $317$ years to do the same calculations using naïve iterated addition.

We see that computers have not made algorithms obsolete.
On the contrary, the vast increase in our ability to measure, store, and communicate data has led to a much higher demand on developing better and more sophisticated algorithms that can allow us to compute and these data and make better decisions based on them.
We also see that to a large extent the notion of _algorithm_ is independent of the actual computing device that will execute it.
The digit by digit standard algorithm is vastly better than iterated addition regardless if the technology to implement it is a silicon based computer chip or a third grader with pen and paper.


Theoretical computer science is largely about studying the _inherent_ properties of algorithms and computation, that are independent of current technology.
We ask questions that already pondered by the Babylonians, such as "what is the best way to multiply two numbers?" as well as those that rely on cutting-edge science such as "could we use the effects of quantum entanglement to factor numbers faster" and many in between.
These types of questions are the topic of this course.

In Computer Science parlance, a scheme such as the decimal (or sexadecimal) positional representation for numbers is known as a _data structure_, while the operations on this representations are known as _algorithms_.
As we can see from this example, data structures and algorithm are useful beyond  just allowing us to do some things a little quicker.
They  expand our vocabulary  and allow us to grasp concepts that otherwise would be beyond our comprehension.  
Structures from computer science, such as bits, strings, graphs, and even the notion of a program itself, as well as concepts such as universality and replication, have not just found practical uses but contributed a new language and a new way to view the world.

### Example: A faster way to multiply

Once you think of the standard digit-by-digit multiplication algorithm, it seems like obviously the "right" way to multiply numbers.
Indeed, in 1960, the famous mathematician Andrey Kolmogorov organized a seminar at Moscow State University in which he conjectured that every algorithm for multiplying two $n$ digit numbers would require a number of basic operations that is proportional to $n^2$.^[That is at least some $n^2/C$ operations for some constant $C$ or, using "Big Oh notation", $\Omega(n^2)$ operations.]
Another way to say it, is that he conjectured that in any multiplication algorithm, doubling the number of digits would _quadruple_ the number of basic operations required.

A young student named Anatoly Karatsuba was in the audience, and within a week he found an algorithm that requires only about $Cn^{1.6}$ operations for some constant $C$.
Such a  number becomes  much smaller than $n^2$ as $n$ grows.^[At the time of this writing, the [standard Python multiplication implementation](https://svn.python.org/projects/python/trunk/Objects/longobject.c) switches from the elementary school algorithm to  Karatsuba's algorithm when multiplying numbers larger than 70 bits long.]
Karatsuba's algorithm is based on the following observation:

We can write two $n$ digit numbers $x$ and $y$ as $10^{n/2}x' + x''$ and $10^{n/2}y'+ y''$ where $x',x'',y',y''$ are $n/2$ digit numbers.
Then
$$
x\cdot y = 10^nx'\cdot y' + 10^{n/2}(x'\cdot y''+x''\cdot y') + x''\cdot y'' \label{eqkarastubaone}
$$

But we can also write the same expression as
$$
x\cdot y = 10^nx' \cdot y' + 10^{n/2}[(x'+x'')\cdot (y'+y'')-x'\cdot y'-x''\cdot y''] + x''\cdot y'' \label{eqkarastubatwo}
$$

The key observation is that the formula [eqkarastubatwo](){.eqref} reduces computing the product of two $n$ digit numbers to computing _three_ products of $n/2$ digit numbers (namely $x'\cdot y'$, $x''\cdot y''$ and $(x'+x'')\cdot (y'+y'')$) as well as performing a constant number (in fact eight) additions, subtractions, and multiplications by $10^n$ or $10^{n/2}$ (the latter corresponding to simple shifts).
Intuitively this means that as the number of digits _doubles_, the cost of multiplying _triples_  instead of quadrupling, as happens in the naive algorithm.
This implies that multiplying numbers of $n=2^\ell$ digits costs about $3^\ell = n^{\log_2 3} \sim n^{1.585}$ operations.
In a [karatsuba-ex](){.ref}, you will formally show that the number of single digit operations that Karatsuba's algorithm uses for multiplying $n$ digit integers is at most $1000 n^{\log_2 3}$ (see also [karatsubafig](){.ref}).

![Running time of Karatsuba's algorithm vs. the Gradeschool algorithm. Figure by [Marina Mele](http://www.marinamele.com/third-grade-karatsuba-multiplication-algorithms).](../figure/karatsuba-vs-third-grade-order-768x600.png){#karatsubafig .class width=300px height=300px}


![Karatsuba's algorithm reduces an $n$-bit multiplication to three $n/2$-bit multiplications, which in turn are reduced to nine $n/4$-bit multiplications and so on. We can represent the computational cost of all these multiplications in a $3$-ary tree of depth $\log_2 n$, where at the root the extra cost is $cn$ operations, at the first level the extra cost is $c(n/2)$ operations, and at each of the $3^i$ nodes of  level $i$, the extra cost is $c(n/2^i)$. The total cost is $cn\sum_{i=0}^{\log_2 n} (3/2)^i \leq 2cn^{\log_2 3}$ by the formula for summing a gemoetric series.](../figure/karatsuba_analysis.png){#karatsuba-fig .class width=300px height=300px}

>__Remark on Big Oh notation:__ It can be quite an headache to keep track of the various constants, and so typically in theoretical computer science we use asymptotic or "Big Oh" notation for quantities such as running time of an algorithm. So, we will write $f(n)=O(g(n))$ if there is some constant $C$ such that $f(n) \leq C g(n)$ for all $n$ and $f(n)=\Omega(g(n))$ if $g(n)=O(f(n))$. Most of the time, when you see a statement such as "running time is  $O(n^3)$" you can think of it as saying  that the algorithm takes at most $1000\cdot n^3$ steps and similarly when a statement such as "running time is  $\Omega(n^2)$" can be thought of as saying that the algorithm takes at least  $0.001\cdot n^2$ steps.
A fuller review Big Oh notation and asymptotics of running time appears in the "mathematical background" section.

### Beyond Karatsuba's algorithm

It turns out that the ideas of Karatsuba can be further extended to yield asymptotically faster multiplication algorithms, as was shown by Toom and Cook in the 1960s.
But this was not the end of the line.
In 1971, Schönhage and Strassen gave an even faster algorithm using the _Fast Fourier Transform_; their idea was to somehow treat integers as "signals" and do the multiplication more efficiently by moving to the Fourier domain.
The latest asymptotic improvement was given by Fürer in 2007 (though it only starts beating  the Schönhage-Strassen algorithm for truly astronomical numbers).

### Algorithms beyond arithmetic

The quest for better algorithms is by no means restricted to arithmetical tasks such as adding, multiplying or solving equations.
Many _graph algorithms_, including algorithms for finding paths, matchings, spanning tress, cuts, and flows, have been discovered in the last several decades, and this is still an intensive area of research.
(For example,  the last few years saw many advances in algorithms for the _maximum flow_ problem, borne out of surprising connections with electrical circuits and linear equation solvers.)   
These algorithms are being used not just for the "natural" applications of routing network traffic or GPS-based navigation, but also for applications as varied as drug discovery through searching for structures in  gene-interaction graphs to computing risks from correlations in financial investments.


Google was founded based on the _PageRank_ algorithm, which is an efficient algorithm to approximate the top eigenvector of (a dampened version of) the adjacency matrix of web graph.
The _Akamai_ company was founded based on a new data structure, known as _consistent hashing_, for a hash table where buckets are stored at different servers.  
The _backpropagation algorithm_, that computes partial derivatives of a neural network in $O(n)$ instead of $O(n^2)$ time, underlies many of the recent phenomenal successes of  learning deep neural networks.
Algorithms for solving  linear equations under sparsity constraints, a concept known as _compressed sensing_, have been used to drastically reduce the amount and quality of data needed to analyze MRI images.
This is absolutely crucial for MRI imaging of cancer tumors in children, where previously doctors needed to use anesthesia to suspend breath during the MRI exam, sometimes with dire consequences.

Even for classical questions, studied through the ages, new discoveries are still being made.
For the basic task, already of importance to the Greeks, of discovering whether an integer is prime or composite, efficient probabilistic algorithms were only discovered in the 1970s, while the first [deterministic polynomial-time algorithm](https://en.wikipedia.org/wiki/AKS_primality_test) was only found in 2002.
For the related problem of actually finding the factors of a composite number, new algorithms were found in the 1980s, and (as we'll see later in this course) discoveries in the 1990s  raised the tantalizing prospect of obtaining faster algorithms through the use of quantum mechanical effects.

Despite all this progress, there are still many more questions than answers in the world of algorithms.
For almost all natural problems, we do not know whether the current algorithm is the "best", or whether a significantly  better one is still waiting to be discovered.
Even for the classical problem of multiplying numbers, we have not yet answered the age-old question of __"is multiplication harder than addition?"__ .  But at least, as we will see in this course, we now know the right way to _ask_ it.



### On the importance of negative results.

Finding better multiplication algorithms is undoubtedly a worthwhile endeavor.
But why is it important  to prove that such algorithms _don't_ exist?
What useful applications could possibly arise from an impossibility result?


One motivation is pure intellectual curiosity.
After all, this is a question even Archimedes could have been excited about.
Another reason to study impossibility results is that they correspond to the fundamental limits of our world or in other words to _laws of nature_.
The impossibility of building a perpetual motion machine corresponds to the law of conservation of energy, the impossibility of building  a heat engine beating Carnot's bound corresponds to the second law of thermodynamics, while the impossibility of faster-than-light information transmission corresponds to special relativity.
Within mathematics, the impossibility of solving a quintic equation with radicals gave  birth to group theory, while the impossibility of proving Euclid's fifth postulate from the first four gave rise to alternative geometries.

Similarly, impossibility results for computation correspond to "computational laws of nature" that tell us about the fundamental limits of any information processing apparatus, whether based on silicon, neurons, or quantum particles.
Indeed,  some [exciting recent research](http://www.scottaaronson.com/barbados-2016.pdf)  has been trying to use computational complexity to shed light on fundamental questions in physics such as the "firewall paradox" for black holes and the "AdS/CFT correspondence".

Moreover, computer scientists have recently been finding creative approaches to _apply_ computational limitations to achieve certain useful tasks.
For example, much of modern Internet traffic is encrypted using the RSA encryption scheme, which relies on its security on the (conjectured) _non existence_ of an efficient algorithm to perform the inverse operation for multiplication--- namely, factor large integers.
More recently, the [Bitcoin](https://en.wikipedia.org/wiki/Bitcoin) system uses a digital analog of the "gold standard" where, instead of being based on a  precious metal, minting new currency corresponds to "mining"  solutions for computationally difficult problems.


## Lecture summary

( _The notes for every lecture will end in such a "lecture summary" section that contains a few of the "take home messages" of the lecture. It is not meant to be a comprehensive summary of all the main points covered in the lecture._ )


* There can be several different algorithms to achieve the same computational task. Finding a faster algorithm can make a much bigger difference than better technology.
* Better algorithms and data structures don't just speed up calculations, but can yield  new qualitative insights.
* One of the main topics of this course is studying the question of what is  the _most efficient_ algorithm for a given  problem.
* To answer such a question we need to find ways to _prove lower bounds_ on the computational resources needed to solve certain problems. That is, show an _impossiblity result_ ruling out the existence of "too good" algorithms.

### Roadmap to the rest of this course

Often, when we try to solve a computational problem, whether it is solving a system of  linear equations, finding the top eigenvector of a matrix, or trying to rank Internet search results, it is enough to use the "I know it when I see it" standard for describing algorithms.
As long as we find some way to solve the problem, we are happy and  don't care so much about  formal descriptions of the algorithm.
But when we want to answer a question such as "does there _exist_ an algorithm to solve the problem $P$?" we need to be much more precise.

In particular, we will  need to __(1)__  define exactly what does it mean to solve $P$, and __(2)__  define exactly what is an algorithm.
Even __(1)__ can sometimes be non-trivial but __(2)__ is particularly challenging; it is not at all clear how (and even whether) we can encompass all potential ways to design algorithms.
We will consider several simple _models of computation_, and argue that, despite their simplicity, they do capture many "reasonable" approache for computing, including all those that are currently used in modern computing devices.

Once we have these formal models of computation, we can try to obtain _impossibility results_ for computational tasks, showing that some problems _can not be solved_ (or perhaps can not be solved within the resources of our universe).
Archimedes one said that given a fulcrum and a long enough lever, he could move the world.
We will see how _reductions_ allow us  to leverage one hardness result into a slew of a great many others, illuminating the boundaries between the computable and uncomputable (or tractable and intractable) problems.

Later in this course we will go back to examining our models of computation, and see how resources such as randomness or quantum entanglement could potentially change the power of our model.
In the context of  probabilistic algorithms, we will see how randomness, and related notions such as _entropy_ and _mutual information_, has become an indispensable tool for understanding computation, information, and communication.   
We will also see how  computational difficulty can be an asset rather than a hindrance, and be used for the   "derandomization" of probabilistic algorithms.
The same ideas also show up in _cryptography_, which has undergone not just a technological but also an intellectual revolution in the last few decades, much of it building on the foundations that we explore in this course.

Theoretical Computer Science is a vast topic, branching out and touching upon many scientific and engineering disciplines.
This course only provides a very partial (and biased) sample of this area.
More than anything, I hope I will manage to "infect" you with at least some of my love for this field, which is inspired and enriched by the connection to practice, but which I find to be  deep and  beautiful regardless of   applications.


## Exercises


> # {.exercise }
Rank the significance of the  following inventions in speeding up multiplication of large (that is 100 digit or more) numbers. That is, use "back of the envelope" estimates to order them in terms of the speedup factor they offered over the previous state of affairs.  \
   >a. Discovery of the gradeschool style digit by digit algorithm (improving upon repeated addition) \
   >b. Discovery of Karatsuba's algorithm (improving upon the digit by digit algorithm) \
   >c. Invention of modern electronic computers (improving upon calculations with pen and paper)

> # {.exercise}
The 1977  Apple II personal computer had a processor speed of 1.023Mhz or about $10^6$ operations per seconds. At the time of this writing the world's fastest supercomputer performs 93 "petaflops" ($10^{15}$ floating point operations per second) or about $10^{18}$ basic steps per second. Compute the size of input that each one of those computers can handle in a week of computation, if the algorithm they run takes on input of length $n$: \
   >a. $n$ operations. \
   >b. $n^2$ operations. \
   >c. $n\log n$ operations. \
   >d. $2^n$ operations. \
   >e. $n!$ operations.


> # {.exercise title="Analysis of Karatsuba's Algorithm" #karatsuba-ex}
>  \
   >a. Suppose that $T_1,T_2,T_3,\ldots$ is a sequence of numbers such that $T_2 \leq 10$ and for every $n$, $T_n \leq 3T_{\lceil n/2 \rceil} + Cn$. Prove that $T_n \leq 10Cn^{\log_2 3}$ for every $n$.^[__Hint:__ Use a proof by induction - suppose that this is true for all $n$'s from $1$ to $m$, prove that this is true also for $m+1$.] \
   >b. Prove that the number of single digit operations that Karatsuba's algorithm takes to multiply two $n$ digit numbers is at most $1000n^{\log_2 3}$.


> # {.exercise }
Implement in the programming language of your choice functions ```Gradeschool_multiply(x,y)``` and ```Karatsuba_multiply(x,y)``` that take two arrays of digits ```x``` and ```y``` and return an array representing the product of ```x``` and ```y``` (where ```x``` is identified with the number ```x[0]+10*x[1]+100*x[2]+...``` etc..) using the gradeschool algorithm and the Karatsuba algorithm respectively. At what number of digits does the Karatsuba algorithm beat the gradeschool one?


## Bibliographical notes

For an overview of what we'll see in this course, you could do far worse than read [Bernard Chazelle's wonderful essay on the Algorithm as an Idiom of modern science](https://www.cs.princeton.edu/~chazelle/pubs/algorithm.html).

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

* The _Fourier transform_, the _Fast_ Fourier transform algorithm and how to use it multiply polynomials and integers. [This lecture of Jeff Erickson](http://jeffe.cs.illinois.edu/teaching/algorithms/notes/02-fft.pdf) (taken from his [collection of notes](http://jeffe.cs.illinois.edu/teaching/algorithms/) ) is a very good starting point.  See also this [MIT lecture](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2012/lecture-notes/MIT6_046JS12_lec05.pdf) and this [popular article](http://www.ams.org/samplings/feature-column/fcarc-multiplication).

* The proofs of some of the classical impossibility results in mathematics we mentioned, including the impossibility of proving Euclid's fifth postulate from the other four, impossibility of trisecting an angle with a straightedge and compass and the impossibility of solving a quintic equation via radicals. A geometric proof of the impossibility of angle trisection (one of the three [geometric problems of antiquity](http://mathworld.wolfram.com/GeometricProblemsofAntiquity.html), going back to the ancient greeks) is given in this [blog post of Tao](https://terrytao.wordpress.com/2011/08/10/a-geometric-proof-of-the-impossibility-of-angle-trisection-by-straightedge-and-compass/). [This book of Mario Livio](https://www.amazon.com/dp/B000FCKGVQ/) covers some of the background and ideas behind these impossibility results.



## Acknowledgements
