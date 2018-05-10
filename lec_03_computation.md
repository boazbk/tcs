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
This gives us hope for a _technology independent_ way of defining computation, which is what we will do in this chapter.

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


> # {.example title="Computing $XOR$ from $AND$,$OR$,$NOT$" #XORandornotexample}
Let us see how we can obtain a different function from these building blocks:
Define $XOR:\{0,1\}^2 \rightarrow \{0,1\}$ to be the function $XOR(a,b)= a + b \mod 2$. That is, $XOR(0,0)=XOR(1,1)=0$ and $XOR(1,0)=XOR(0,1)=1$.
We claim that we can construct $XOR$ using only $AND$, $OR$, and $NOT$.
>
Here is an algorithm to compute $XOR(a,b)$ using $AND,NOT,OR$ as basic operations:
>
1. Compute $w1 = AND(a,b)$ \
2. Compute $w2 = NOT(w1)$ \
3. Compute $w3 = OR(a,b)$ \
4. Output $AND(w2,w3)$ \
>
We can also express this algorithm graphically, see [andornotcircxorfig](){.ref}. Such diagrams are often known as _Boolean circuits_, and each basic operation is known as a _gate_. This is a point of view that we will revisit often in this course.
>
Last but not least, we can also express it in Python code (see below).


```python
def XOR(a,b):
    w1 = a & b
    w2 = ~w1
    w3 = a | b
    return w2 & w3

print([(a,b,XOR(a,b)) for a in [0,1] for b in [0,1]])
# [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
```


![A circuit with $AND$, $OR$ and $NOT$ gates (denoted as $\wedge,\vee,\neg$ respectively) for computing the $XOR$ function.](../figure/andornotcircforxor.png){#andornotcircxorfig  .class width=300px height=300px}




> # {.example title="Computing $XOR$ on three bits" #xorthree}
Extending the same ideas, we can use these basic operations to compute the function $XOR_3:\{0,1\}^3 \rightarrow \{0,1\}$ defined as $XOR_3(a,b,c) = a + b + c (\mod 2)$  by computing first $d=XOR(a,b)$ and then outputting $XOR(d,c)$.
In Python this is done as follows:
>
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


> # {.solvedexercise title="Compute majority with NAND" #majbynandex}
Let $MAJ_3: \{0,1\}^3 \rightarrow \{0,1\}$ be the function that on input $a,b,c$ outputs $1$ iff $a+b+c \geq 2$. Show how to compute $MAJ_3$ using a composition of $NAND$'s.

> # {.solution data-ref="majbynandex"}
To solve this problem, we will first express  $MAJ_3$  using $AND$, $OR$, $NOT$, and then use
[univnandonethm](){.ref}  to replace those with only $NAND$.
We can very naturally express the statement "At least two of $a,b,c$ are equal to $1$" using OR's and AND's. Specifically, this is true if at least one of the values $AND(a,b)$, $AND(a,c)$, $AND(b,c)$ is true.
So we can write
$$MAJ_3(a,b,c) = OR(OR(AND(a,b),AND(a,c)),AND(b,c)) \label{eqmajusingandor} \;.$$
>
Now we can use the equivalence $AND(a,b)=NOT(NAND(a,b))$, $OR(a,b)=NAND(NOT(a),NOT(b))$, and $NOT(a)=NAND(a,a)$ to replace the righthand side of [{eqmajusingandor}](){.eqref} with an expression involving only $NAND$, yielding
$$
MAJ_3(a,b,c) = NAND(NAND(NAND(a,b),NAND(a,c)),NAND(b,c))
$$



### Informally defining "basic operations" and "algorithms"

[univnandonethm](){.ref} tells us that we can use applications of the single function $NAND$ to obtain $AND$, $OR$, $NOT$, and so by extension all the other functions that can be built up from them.
This suggests making $NAND$ our notion of a "basic operation", and hence coming up with the following definition of an "algorithm":

>__Informal definition for an algorithm:__ An _algorithm_  consists of a sequence of steps of the form "store the NAND of variables `foo` and `bar` in variable `blah`". \
>
An algorithm $A$ _computes_ a function $F$ if for every input $x$ to $F$, if we feed $x$ as input to the algorithm, the value computed in its last step is $F(x)$.

There are questions that are raised by this definition:

1. First and foremost, it is indeed too informal. We do not specify exactly what each step does, nor what it means to "feed $x$ as input".

2. Second, the choice of $NAND$ as a basic operation seems arbitrary. Why just $NAND$? Why not $AND$, $OR$ or $NOT$? Why not allow operations like addition and multiplication? What about any other logical constructions such `if`/`then` or `while`?

3. Third, do we even know that this definition has anything to do with actual computing? If someone gave us a description of such an algorithm, could we use it to actually compute the function the real world?


A large part of this course will be devoted to answering questions 1,2 and 3 above. We will see that:

1. We can make the definition of an algorithm fully formal, and so give a precise mathematical meaning to statements such as "Algorithm $A$ computes function $F$".

2. While the choice of $NAND$ is arbitrary, and we could just as well chose some other functions, we will also see this choice does not matter muchh. Our notion of an algorithm is not more restrictive because we only think of $NAND$ as a basic step. We have already seen that allowing $AND$,$OR$, $NOT$ as basic operations will not add any power (because we can compute them from $NAND$'s via [univnandonethm](){.ref}). We will see that the same is true for addition, multiplication, and essentially every other operation that could be reasonably thought of as a basic step.

3. It turns out that we can and do compute such "$NAND$ based algorithms" in the real world. First of all, such an algorithm is clearly well specified, and so can be executed by a human with a pen and paper. Second, there are a variety of ways to _mechanize_ this computation. We've already seen that we can write Python code that corresponds to following such a list of instructions. But in fact we can directly implement operations such as $NAND$, $AND$, $OR$, $NOT$ etc.. via electronic signals using components known as _transistors_. This is how modern electronic computers operate.

We will see fully formal definitions of computation in future chapters. In the remainder of this chapter, we will focus on giving some partial answers to Questions 2 and 3.
We will see more example of the power of simple operations like $NAND$ (or equivalently, $AND$/$OR$/$NOT$, as well as many other choices) to compute more complex operations including addition, multiplication, sorting and more.
We will then discuss how to _physically implement_ simple operations such as NAND using a variety of technologies.

## From NAND to infinity and beyond..

We have seen that using $NAND$, we can compute $AND$, $OR$, $NOT$ and $XOR$.
But this still seems a far cry from being able to add and multiply numbers, not to mention more complex programs such as sorting and searching, solving equations, manipulating images, and so on.
We now give a few examples demonstrating how we can use these simple operations to do some more complicated tasks.
While we will not go as far as implementing   [Call of Duty](https://goo.gl/DdJZFF), we will at least show how we can compose $NAND$ operations to obtain tasks such as addition, multiplications, and comparisons.

__NAND Circuits.__ We can describe the computation of a  function $F:\{0,1\}^n \rightarrow \{0,1\}$ via a composition of $NAND$ operations in terms of a _circuit_, as was done in [andornotcircxorfig](){.ref}.
Since in our case, all the gates are the same function (i.e., $NAND$), the description of the circuit is even simpler.
We can think of the circuit as a directed graph.
It has a vertex for every one of the input bits, and also for every intermediate  value  we use in our computation.
If we compute a value $u$ by applying $NAND$ to $v$ and $w$ then we put a directed edges from $v$ to $u$ and from $w$ to $u$.
We will follow the convention of using  "$x$" for inputs and "$y$" for outputs, and hence write $x_0,x_1,\ldots$ for our inputs and $y_0,y_1,\ldots$ for our outputs. (We will sometimes also write these as `x[0]`,`x[1]`,$\ldots$ and  `y[0]`,`y[1]`,$\ldots$ respectively.)

We now present some examples of $NAND$ circuits for various natural problems:


> # {.example title="$NAND$ circuit for $XOR$" #xornandexample}
Recall the $XOR$ function which maps $x_0,x_1 \in \{0,1\}$ to $x_0 + x_1 \mod 2$.
We have seen in [XORandornotexample](){.ref} that we can compute this function using $AND$, $OR$, and $NOT$, and so by [univnandonethm](){.ref} we can compute it using only $NAND$'s.
However, the following is a direct construction of computing $XOR$ by a sequence of NAND operations:
>
1. Let $u = NAND(x_0,x_1)$.  \
2. Let $v = NAND(x_0,u)$  \
3. Let $w = NAND(x_1,u)$. \
4. The $XOR$ of $x_0$ and $x_1$ is $y_0 = NAND(v,w)$.
>
(We leave it to you to verify that this algorithm does indeed compute $XOR$.)
>
We can also represent this algorithm graphically as a circuit:
>
![](../figure/xornandcirc.png){#figid .class width=300px height=300px} \


We now present a few more examples of computing natural functions by a sequence of $NAND$ operations.

> # {.example title="$NAND$ circuit for incrementing" #incrementnandexample}
Consider the task of computing, given as input a string $x\in \{0,1\}^n$ that represents a natural number $X\in \N$, the representation of $X+1$.
That is, we want to compute the function $INC_n:\{0,1\}^n \rightarrow \{0,1\}^{n+1}$ such that for every $x_0,\ldots,x_{n-1}$, $INC_n(x)=y$  which satisfies $\sum_{i=0}^n y_i 2^i = \left( \sum_{i=0}^{n-1} x_i 2^i \right)+1$.
>
The increment operation can be very informally described as follows: _"Add $1$ to the most significant bit and propagate the carry"_.
A little more precisely, in the case of the binary representation, to obtain the increment of $x$, we scan $x$ from the least significant bit onwards, and flip all $1$'s to $0$'s until we encounter a bit equal to $0$, in which case we flip it to $1$ and stop.
(Please verify you understand why this is the case.)
>
Thus we can compute the increment of $x_0,\ldots,x_{n-1}$ by doing the following:
>
1. Set $c_0=1$ (we pretend we have a "carry" of $1$ initially)
2. For $i=0,\ldots, n-1$ do the following:
   a. Let $y_i = XOR(x_i,c_i)$.
   b. If $y_i=x_i=1$ then $c_{i+1}=1$, else $c_{i+1}=0$.
3. Set $y_n = c_n$.
>
The above is a very precise description of an algorithm to compute the increment operation, and can be easily transformed into _Python_ code that performs the same computation, but it does not seem to directly yield a NAND circuit to compute this.
However, we can transform this algorithm line by line to a NAND circuit.
For example, since for every $a$, $NAND(a,NOT(a))=1$, we can replace the initial statement $c_0=1$ with $c_0 = NAND(x_0,NAND(x_0,x_0))$.
We already know how to compute $XOR$ using NAND, so line 2.a can be replaced by some NAND operations.
Next, we can write line 2.b as simply saying $c_{i+1} = AND(y_i,x_i)$,  or in other words $c_{i+1}=NAND(NAND(y_i,x_i),NAND(y_i,x_i))$.
Finally, the assignment $y_n = c_n$ can be written as $y_n = NAND(NAND(c_n,c_n),NAND(c_n,c_n))$.
Combining these observations yields for every $n\in \N$, a $NAND$ circuit to compute $INC_n$.
For example, this is how this circuit looks like for $n=4$.
>
![](../figure/incrementnandcirc.png){#figid .class width=100px height=300px} \


> # {.example title="Addition using NANDs" #additionnandcirc}
Once we have the increment operation, we can certainly compute addition by repeatedly incrementing (i.e., compute $x+y$ by performing $INC(x)$ $y$ times).
However, that would be quite inefficient and unnecessary.
With the same idea of keeping track of carries we can implement the "gradeschool" algorithm for addition to compute the function $ADD_n:\{0,1\}^{2n} \rightarrow \{0,1\}^{n+1}$ that on input $x\in \{0,1\}^{2n}$ outputs the binary representation of the sum of the numbers represented by $x_0,\ldots,x_{n-1}$ and $x_{n+1},\ldots,x_n$:
>
1. Set $c_0=0$.
2. For $i=0,\ldots,n-1$:
   a. Let $y_i = x_i + x_{n+i} + c_i (\mod 2)$.
   b. If $x_i + x_{n+i} + c_i \geq 2$ then $c_{i+1}=1$.
3. Let $y_n = c_n$
>
Once again, this can be translated into a NAND circuit.
To transform Step 2.b to a NAND circuit we use the fact (shown in [majbynandex](){.ref}) that the function $MAJ_3:\{0,1\}^3 \rightarrow \{0,1\}$ can be computed  using $NAND$s.


## Physical implementations of computing devices.


_Computation_ is an abstract notion, that is distinct from its physical _implementations_.
While most modern computing devices are obtained by mapping logical gates to semi-conductor based transistors, over history people have computed using a huge variety of mechanisms,  including mechanical systems, gas and liquid (known as _fluidics_), biological and chemical processes, and even living creatures (e.g., see [crabfig](){.ref} or  [this video](https://www.youtube.com/watch?v=czk4xgdhdY4) for how crabs or slime mold can be used to do computations).


In the rest of this  chapter we review some of these implementations, both so  you can get an appreciation of how it is possible to directly translate NAND programs to the physical world, without going through the entire stack of architecture, operating systems, compilers, etc... as well as to emphasize that silicon-based processors are by no means the only way to perform computation.
Indeed, as we will see much later in this course, a very exciting recent line of works involves using different media for computation that would allow us to take advantage of _quantum mechanical effects_ to enable different types of algorithms.

![Crab-based logic gates from the paper "Robust soldier-crab ball gate" by Gunji, Nishiyama and Adamatzky. This is an example of an AND gate that relies on the tendency of two swarms of crabs arriving from different directions to combine to a single swarm that continues in the average of the directions.](../figure/crab-gate.jpg){#crabfig .class width=200px height=200px}



### Transistors and physical logic gates

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




### NAND gates from transistors

We can use transistors to implement a _NAND gate_, which would be a system with two input wires $x,y$ and one output wire $z$, such that if we identify high voltage with "$1$" and low voltage with "$0$", then the wire  $z$ will equal to "$1$" if and only if the NAND of the values of the wires $x$ and $y$ is $1$ (see [transistor-nand-fig](){.ref}).

![Implementing a NAND gate using transistors.](../figure/nand_transistor.png){#transistor-nand-fig .class width=300px height=300px}

This means that there exists a NAND circuit to  compute a function $F:\{0,1\}^n \rightarrow \{0,1\}^m$, then we can compute $F$ in the physical world using transistors as well.


## Basing computing on other media

Electronic transistors are in no way the only technology that can implement computation.
There are many mechanical, chemical, biological,  or even social systems that can be thought of as  computing devices.
We now discuss some of these examples.




### Biological computing

Computation can be based on [biological  or chemical systems]((http://www.nature.com/nrg/journal/v13/n7/full/nrg3197.html)).
For example the [_lac_ operon](https://en.wikipedia.org/wiki/Lac_operon) produces the enzymes needed to digest lactose only if the conditions $x \wedge (\neg y)$ hold where $x$ is "lactose is present" and $y$ is "glucose is present".
Researchers have managed to [create transistors](http://science.sciencemag.org/content/340/6132/554?iss=6132), and from them the NAND function and other logic gates, based on DNA molecules (see also [transcriptorfig](){.ref}).
One motivation for DNA computing is to achieve  increased parallelism or storage density; another is to create "smart biological agents" that could perhaps be injected into bodies, replicate themselves, and fix or kill cells that were damaged by a disease such as cancer.
Computing in biological systems is not restricted of course to DNA.
Even larger systems such as [flocks of birds](https://www.cs.princeton.edu/~chazelle/pubs/cacm12-natalg.pdf) can be considered as computational processes.

![Performance of DNA-based logic gates. Figure taken from paper of [Bonnet et al](http://science.sciencemag.org/content/early/2013/03/27/science.1232758.full), Science, 2013.](../figure/transcriptor.jpg){#transcriptorfig .class width=300px height=300px}

### Cellular automata and the game of life

_Cellular automata_ is a model of a system composed of a sequence of _cells_, which of which can have a finite state.
At each step, a cell updates its state based on the states of its _neighboring cells_ and some simple rules.
As we will discuss later in this course, cellular automata such as Conway's "Game of Life" can be used to simulate computation gates, see [gameoflifefig](){.ref}.

![An AND gate using a "Game of Life" configuration. Figure taken from [Jean-Philippe Rennard's paper](http://www.rennard.org/alife/CollisionBasedRennard.pdf).](../figure/game_of_life_and.png){#gameoflifefig .class width=300px height=300px}


### Neural networks

One particular basis we can use are _threshold gates_.
For every vector $w= (w_0,\ldots,w_{k-1})$ of integers  and  integer $t$ (some or all of whom  could be negative),
the _threshold function corresponding to $w,t$_ is the function
$T_{w,t}:\{0,1\}^k \rightarrow \{0,1\}$ that maps $x\in \{0,1\}^k$ to $1$ if and only if $\sum_{i=0}^{k-1} w_i x_i \geq t$.
For example, the threshold function $T_{w,t}$ corresponding to $w=(1,1,1,1,1)$ and $t=3$ is simply the majority function $MAJ_5$ on $\{0,1\}^5$.
The function $NAND:\{0,1\}^2 \rightarrow \{0,1\}$  is the threshold function corresponding to $w=(-1,-1)$ and $t=-1$, since $NAND(x_0,x_1)=1$ if and only if $x_0 + x_1 \leq 1$ or equivalently, $-x_0 - x_1 \geq -1$.



Threshold gates can be thought of as an approximation for    _neuron cells_ that make up the core of human and animal brains. To a first approximation, a neuron has $k$ inputs and a single output and the neurons  "fires" or "turns on" its output when those signals pass some threshold.^[Typically we think of an input to neurons as being a real number rather than a binary string, but  we can reduce to the binary case by  representing a real number in the binary basis, and multiplying the weight of the bit corresponding to the $i^{th}$ digit by $2^i$.]
Hence circuits with threshold gates are sometimes known as _neural networks_.
Unlike the cases above, when we considered $k$ to be a small constant, in such  neural networks we often do not put any bound on the number of inputs.
However, since any threshold function on $k$ inputs can be computed by a NAND program of $poly(k)$  lines (see [threshold-nand-ex](){.ref}), the  power of NAND programs and neural networks is not very different.

### The marble computer

TO BE COMPLETED
