# Defining computation


># {.objectives  }
* See that computation can be precisely modeled. \
* Learn the NAND computational model. \


>_"there is no reason why mental as well as bodily labor should not be economized by the aid of machinery"_, Charles Babbage, 1852


>_"If, unwarned by my example, any man shall undertake and shall succeed in constructing an engine embodying in itself the whole of the executive department of mathematical analysis upon different principles or by simpler mechanical means, I have no fear of leaving my reputation in his charge, for he alone will be fully able to appreciate the nature of my efforts and the value of their results."_, Charles Babbage, 1864

>_"To understand a program you must become both the machine and the program."_, Alan Perlis, 1982





People have been computing for thousands of years, with aids that include not just  pen and paper, but also abacus, slide rulers, various mechanical devices, and modern electronic computers.
A priori, the notion of computation seems to be tied to the particular mechanism that you use.
You might think that the "best"  algorithm for multiplying numbers will differ if you  implement it in _Python_ on a modern laptop than if you use pen and paper.
However, as we saw in the introduction, an algorithm that is asymptotically better would eventually beat a worse one regardless of the underlying technology.
This gives us hope for a _technology independent_ way of defining computation, which is what we will do in this lecture.

![Calculating wheels by Charles Babbage. Image taken from the Mark I 'operating manual'](../figure/wheels_babbage.png){#babbagewheels .class width=300px height=300px}



![A 1944 _Popular Mechanics_ article on the [Harvard Mark I computer](http://sites.harvard.edu/~chsi/markone/about.html).](../figure/PopularMechanics1944smaller.jpg){#markIcomp .class width=300px height=300px}


## Defining computation


The name "algorithm" is derived from the Latin transliteration of  Muhammad ibn Musa al-Khwarizmi, who was a Persian scholar during the 9th century whose books introduced the western world to the decimal positional numeral system, as well as the solutions of linear and quadratic equations (see [alKhwarizmi](){.ref}).
Still his description of the algorithms were rather informal by today's standards.
Rather than use "variables" such as $x,y$, he used concrete numbers such as 10 and 39, and trusted the reader to be able to extrapolate from these examples.^[Indeed, extrapolation from examples is still the way most of us first learn algorithms such as addition and multiplication, see [childrenalg](){.ref})]

Here is how al-Khwarizmi described how to solve an equation of the form $x^2 +bx = c$:^[Translation from "The Algebra of Ben-Musa", Fredric Rosen, 1831.]

>_[How to solve an equation of the form ] "roots and squares are equal to numbers": For instance "one square , and ten roots of the same, amount to thirty-nine dirhems" that is to say, what must be the square which, when increased by ten of its own root, amounts to thirty-nine? The solution is this: you halve the number of the roots, which in the present instance yields five. This you multiply by itself; the product is twenty-five. Add this to thirty-nine' the sum is sixty-four. Now take the root of this, which is eight, and subtract from it half the number of roots, which is five; the remainder is three. This is the root of the square which you sought for; the square itself is nine._


![An explanation for children of the two digit addition algorithm](../figure/addition_regrouping.jpg){#childrenalg .class width=300px height=300px}


![Text pages from Algebra manuscript with geometrical solutions to two quadratic equations. Shelfmark: MS. Huntington 214 fol. 004v-005r](../figure/alKhwarizmi.jpg){#alKhwarizmi .class width=300px height=300px}

For the purposes of this course, we will need a much more precise way to define algorithms.
Fortunately (or is it unfortunately?), at least at the moment, computers lag far behind school-age children in learning from examples.
Hence in the 20th century people have come up with  exact formalisms for describing algorithms, namely _programming languages_.
Here is al-Khwarizmi's quadratic equation solving  algorithm described in the Python programming language:^[For concreteness we often  include code of actual programming languages in these notes. However, these will be simple enough to be understandable even by people that are not familiar with these languages.]


```python
from math import sqrt

def solve_eq(b,c):
    # return solution of x^2 + bx = c using Al Khwarizmi's instructions
    val1 = b/2.0 # halve the number of the roots
    val2 = val1*val1 # this you multiply by itself
    val3 = val2 + c # Add this to thirty-nine (c)
    val4 = sqrt(val3) # take the root of this
    val5 = val4 - val1 # subtract from it half the number of roots
    return val5  # This is the root of the square which you sought for

print(solve_eq(2,35))
# 5.0
```


### Defining "elementary operations"

An _algorithm_ breaks down a complex calculation into a series of simpler steps.
These steps can be executed by:

* Writing down symbols on a piece of paper

* Modifying the current flowing on electrical wires.

* Binding a protein to a strand of DNA

* Response to a stimulus by a member of a collection (e.g., a bee in a colony, a trader in a market).

Let us try to "err on the side of simplicity" and model computation in the simplest possible way.
We will think of the most basic of computational steps.
Here are some very simple functions:

* $OR:\{0,1\}^2 \rightarrow \{0,1\}$ defined as

$$OR(a,b) = \begin{cases} 0 & a=b=0 \\ 1 & \text{otherwise} \end{cases}$$

* $AND:\{0,1\}^2 \rightarrow \{0,1\}$ defined as

$$AND(a,b) = \begin{cases} 1 & a=b=1 \\ 0 & \text{otherwise} \end{cases}$$

* $NOT:\{0,1\} \rightarrow \{0,1\}$ defind as $NOT(a) = 1-a$.


Each one of these functions takes either one or two single bits as input, and produces a single bit as output. Clearly, it cannot get much more basic than these.
However, the power of computation comes from _composing_ simple building blocks together.
Let us see how we can obtain a different function from these building blocks:

Define $XOR:\{0,1\}^2 \rightarrow \{0,1\}$ to be the function $XOR(a,b)= a + b \mod 2$. That is, $XOR(0,0)=XOR(1,1)=0$ and $XOR(1,0)=XOR(0,1)=1$.
We claim that we can construct $XOR$ using only $AND$, $OR$, and $NOT$.

> # { .pause }
You should stop here and try to construct $XOR$ yourself from $AND,OR,NOT$. Try to think of other functions as well. For example, can you construct the function $MAJ:\{0,1\}^5  \rightarrow \{0,1\}$ that output $1$ on $x\in \{0,1\}^5$ if the majority of $x$'s coordinates are equal to $1$?

Here is an algorithm to compute $XOR(a,b)$ using $AND,NOT,OR$ as basic operations:

1. Compute $w1 = AND(a,b)$
2. Compute $w2 = NOT(w1)$
3. Compute $w3 = OR(a,b)$
4. Output $AND(w2,w3)$


We can also express this algorithm graphically, see [andornotcircxorfig](){.ref}. Such diagrams are often known as _Boolean circuits_, and each basic operation is known as a _gate_. This is a point of view that we will revisit often in this course.
Last but not least, we can also express it in Python code.

![A circuit with $AND$, $OR$ and $NOT$ gates (denoted as $\wedge,\vee,\neg$ respectively) for computing the $XOR$ function.](../figure/andornotcircforxor.png){#andornotcircxorfig  .class width=300px height=300px}



```python
def XOR(a,b):
    w1 = a & b
    w2 = ~w1
    w3 = a | b
    return w2 & w3

print([(a,b,XOR(a,b)) for a in [0,1] for b in [0,1]])
# [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
```


Extending the same ideas, we can use these basic operations to compute the function $XOR_3:\{0,1\}^3 \rightarrow \{0,1\}$ defined as $XOR_3(a,b,c) = a + b + c (\mod 2)$  by computing first $d=XOR(a,b)$ and then outputting $XOR(d,c)$.
In Python this is done as follows:

```python
def XOR3(a,b,c):
    w1 = a & b
    w2 = ~w1
    w3 = a | b
    w4 = w2 & w3
    w5 = w4 & c
    w6 = ~w5
    w7 = w4 | c
    return w6 & w7

print([(a,b,c,XOR3(a,b,c)) for a in [0,1] for b in [0,1] for c in [0,1]])
# [(0, 0, 0, 0), (0, 0, 1, 1), (0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 1, 0, 0), (1, 1, 1, 1)]
```

> # { .pause }
Make sure you see how to generalize this and obtain a way to compute $XOR_n:\{0,1\}^n \rightarrow \{0,1\}$ for every $n$ using at most $4n$ basic steps involving applications of a function in $\{ AND, OR , NOT \}$ to omputs or previously computed values.


### The NAND function

Here is another function we can compute using $AND,OR,NOT$. The $NAND$ function maps $\{0,1\}^2$ to $\{0,1\}$ and is defined as

$$NAND(a,b) = \begin{cases} 0 & a=b=1 \\ 1 & \text{otherwise} \end{cases}$$

As its name implies, $NAND$ is the NOT  of AND (i.e., $NAND(a,b)= NOT(AND(a,b))$), and so we can clearly compute $NAND$ using $AND,OR,NOT$. Interestingly, the opposite direction also holds:

> # {.theorem title="NAND computes AND,OR,NOT." #univnandonethm}
We can compute $AND$, $OR$, and $NOT$ by composing only the $NAND$ function.

> # {.proof data-ref="univnandonethm"}
We start with the following observation. For every $a\in \{0,1\}$, $AND(a,a)=a$. Hence, $NAND(a,a)=NOT(AND(a,a))=NOT(a)$.
This means that $NAND$ can compute $NOT$, and since by the principle of "double negation",  $AND(a,b)=NOT(NOT(AND(a,b)))$ this means that we can use $NAND$ to compute $AND$ as well.
Once we can compute $AND$ and $NOT$, we can compute $OR$ using the so called ["De Morgan's Law"](https://goo.gl/TH86dH): $OR(a,b)=NOT(AND(NOT(a),NOT(b)))$ for every $a,b \in \{0,1\}$.

> # { .pause }
[univnandonethm](){.ref}'s proof is very simple, but you should make sure that __(i)__ you understand the statement of the theorem, and __(ii)__ you follow its proof completely. In particular, you should make sure you understand why De Morgan's law is true.


[univnandonethm](){.ref} tells us that we can use applications of the single function $NAND$ to obtain $AND$, $OR$, $NOT$, and so by extension all the other functions that can be built up from them.
This suggests making $NAND$ our notion of a "basic operation", and hence coming up with the following definition of an "algorithm":

>__Informal definition for an algorithm:__ An _algorithm_  consists of a sequence of steps of the form "store the NAND of variables `foo` and `bar` in variable `blah`". \
>
An algorithm $A$ _computes_ a function $F$ if for every input $x$ to $F$, if we feed $x$ as input to the algorithm, the value computed in its last step is $F(x)$.

There are several things that are wrong with this definition:

1. First and foremost, it is indeed too informal. We do not specify exactly what each step does, nor what it means to "feed $x$ as input".

2. Second, the choice of $NAND$ as a basic operation seems arbitrary. Why just $NAND$? Why not $AND$, $OR$ or $NOT$? Why not allow operations like addition and multiplication? What about any other logical constructions such `if`/`then` or `while`?

3. Third, do we even know that this definition has anything to do with actual computing? If someone gave us a description of such an algorithm, could we use it to actually compute the function the real world?


A large part of this course will be devoted to answering questions 1,2 and 3 above. We will see that:

1. We can make the definition of an algorithm fully formal, and so give a precise mathematical meaning to statements such as "Algorithm $A$ computes function $F$".

2. While the choice of $NAND$ is arbitrary, and we could just as well chose some other functions, we will also see this choice does not matter muchh. Our notion of an algorithm is not more restrictive because we only think of $NAND$ as a basic step. We have already seen that allowing $AND$,$OR$, $NOT$ as basic operations will not add any power (because we can compute them from $NAND$'s via [univnandonethm](){.ref}). We will see that the same is true for addition, multiplication, and essentially every other operation that could be reasonably thought of as a basic step.

3. It turns out that we can and do compute such "$NAND$ based algorithms" in the real world. First of all, such an algorithm is clearly well specified, and so can be executed by a human with a pen and paper. Second, there are a variety of ways to _mechanize_ this computation. We've already seen that we can write Python code that corresponds to following such a list of instructions. But in fact we can directly implement operations such as $NAND$, $AND$, $OR$, $NOT$ etc.. via electronic signals using components known as _transistors_. This is how modern electronic computers operate.


## Physical implementations of computing devices.


_Computation_ is an abstract notion, that is distinct from its physical _implementations_.
While most modern computing devices are obtained by mapping logical gates to semi-conductor based transistors, over history people have computed using a huge variety of mechanisms,  including mechanical systems, gas and liquid (known as _fluidics_), biological and chemical processes, and even living creatures (e.g., see [crabfig](){.ref} or  [this video](https://www.youtube.com/watch?v=czk4xgdhdY4) for how crabs or slime mold can be used to do computations).


In the rest of this  lecture we review some of these implementations, both so  you can get an appreciation of how it is possible to directly translate NAND programs to the physical world, without going through the entire stack of architecture, operating systems, compilers, etc... as well as to emphasize that silicon-based processors are by no means the only way to perform computation.
Indeed, as we will see much later in this course, a very exciting recent line of works involves using different media for computation that would allow us to take advantage of _quantum mechanical effects_ to enable different types of algorithms.

![Crab-based logic gates from the paper "Robust soldier-crab ball gate" by Gunji, Nishiyama and Adamatzky. This is an example of an AND gate that relies on the tendency of two swarms of crabs arriving from different directions to combine to a single swarm that continues in the average of the directions.](../figure/crab-gate.jpg){#crabfig .class width=200px height=200px}



## Transistors and physical logic gates

A _transistor_ can be thought of as an electric circuit with two inputs, known as _source_ and _gate_ and an output, known as the _sink_.
The gate controls whether current flows from the source to the sink.
In a _standard transistor_, if the gate is "ON" then current can flow from the source to the sink and if it is "OFF" then it can't.
In a _complementary transistor_ this is reversed: if the gate is "OFF" then current can flow from the source to the sink and if it is "ON" then it can't.

![We can implement the logic of transistors using water. The water pressure from the gate closes or opens a faucet between the source and the sink.](../figure/transistor_water.png){#transistor-water-fig .class width=300px height=300px}

There are several ways to implement the logic of a transistor.
For example, we can use faucets to implement it using water pressure (e.g. [transistor-water-fig](){.ref}).^[This might seem as curiosity but there is a field known as [fluidics](https://en.wikipedia.org/wiki/Fluidics) concerned with implementing logical operations using liquids or gasses. Some of the motivations include operating in extreme environmental conditions such as in space or  a battlefield, where standard electronic equipment would not survive.]
However, the standard implementation uses electrical current.
One of the original implementations used   _vacuum tubes_.
As its name implies, a vacuum tube is a tube containing nothing (i.e., vacuum) and where a priori electrons could freely flow from source (a wire) to the sink (a plate). However, there is a gate (a grid)  between the two, where modulating its voltage  can block the  flow of electrons.

Early vacuum tubes were roughly the size of lightbulbs (and looked very much like them too).
In the 1950's they were supplanted by _transistors_, which implement the same logic using _semiconductors_ which are materials that normally do not conduct electricity but whose conductivity can be modified and controlled by inserting impurities ("doping") and an external electric field (this is known as the _field effect_).
In the 1960's computers were started to be implemented using _integrated circuits_ which enabled much greater density.
In 1965, Gordon Moore predicted that the number of transistors per circuit would double every  year (see [moorefig](){.ref}), and that this would lead to "such wonders as home computers —or at least terminals connected to a central computer— automatic controls for automobiles, and personal portable communications equipment".
Since then, (adjusted versions of) this so-called "Moore's law" has been running strong, though exponential growth cannot be sustained forever, and some physical limitations are already [becoming apparent](http://www.nature.com/news/the-chips-are-down-for-moore-s-law-1.19338).

![The number of transistors per integrated circuits from 1959 till 1965 and a prediction that exponential growth will continue at least another decade. Figure taken from "Cramming More Components onto Integrated Circuits", Gordon Moore, 1965](../figure/gordon_moore.png){#moorefig .class width=300px height=300px}

![Gordon Moore's cartoon "predicting" the implications of radically improving transistor density.](../figure/moore_cartoon.png){#moore-cartoon-fig .class width=300px height=300px}

![The exponential growth in computing power over the last 120 years. Graph by Steve Jurvetson, extending a prior graph of Ray Kurzweil.](../figure/1200px-Moore's_Law_over_120_Years.png){#kurzweil-fig .class width=300px height=300px}
