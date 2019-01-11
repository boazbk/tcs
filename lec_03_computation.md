% Defining computation
% Boaz Barak


# Defining computation {#compchap }

># {.objectives  }
* See that computation can be precisely modeled. \
* Learn the computational model of _Boolean circuits_ / _straightline programs_.
* See the NAND operation and also why the specific choice of NAND is not important. \
* Examples of computing in the physical world. \
* Equivalence of circuits and programs.


>_"there is no reason why mental as well as bodily labor should not be economized by the aid of machinery"_, Charles Babbage, 1852


>_"If, unwarned by my example, any man shall undertake and shall succeed in constructing an engine embodying in itself the whole of the executive department of mathematical analysis upon different principles or by simpler mechanical means, I have no fear of leaving my reputation in his charge, for he alone will be fully able to appreciate the nature of my efforts and the value of their results."_, Charles Babbage, 1864

>_"To understand a program you must become both the machine and the program."_, Alan Perlis, 1982



People have been computing for thousands of years, with aids that include not just  pen and paper, but also abacus, slide rulers, various mechanical devices, and modern electronic computers.
A priori, the notion of computation seems to be tied to the particular mechanism that you use.
You might think that the "best"  algorithm for multiplying numbers will differ if you  implement it in _Python_ on a modern laptop than if you use pen and paper.
However, as we saw in the introduction ([chapintro](){.ref}), an algorithm that is asymptotically better would eventually beat a worse one regardless of the underlying technology.
This gives us hope for a _technology independent_ way of defining computation, which is what we will do in this chapter.

![Calculating wheels by Charles Babbage. Image taken from the Mark I 'operating manual'](../figure/wheels_babbage.png){#babbagewheels .class width=300px height=300px}



![A 1944 _Popular Mechanics_ article on the [Harvard Mark I computer](http://sites.harvard.edu/~chsi/markone/about.html).](../figure/PopularMechanics1944smaller.jpg){#markIcomp .class width=300px height=300px}


## Defining computation


The name "algorithm" is derived from the Latin transliteration of  Muhammad ibn Musa al-Khwarizmi's name.
Al-Khwarizmi was a Persian scholar during the 9th century whose books introduced the western world to the decimal positional numeral system, as well as to the solutions of linear and quadratic equations (see [alKhwarizmi](){.ref}).
However Al-Khwarizmi's descriptions of algorithms were rather informal by today's standards.
Rather than use "variables" such as $x,y$, he used concrete numbers such as 10 and 39, and trusted the reader to be able to extrapolate from these examples.^[Indeed, extrapolation from examples is still the way most of us first learn algorithms such as addition and multiplication, see [childrenalg](){.ref})]

Here is how al-Khwarizmi described the algorithm for solving an equation of the form $x^2 +bx = c$:^[Translation from "The Algebra of Ben-Musa", Fredric Rosen, 1831.]

>_[How to solve an equation of the form ] "roots and squares are equal to numbers": For instance "one square , and ten roots of the same, amount to thirty-nine dirhems" that is to say, what must be the square which, when increased by ten of its own root, amounts to thirty-nine? The solution is this: you halve the number of the roots, which in the present instance yields five. This you multiply by itself; the product is twenty-five. Add this to thirty-nine' the sum is sixty-four. Now take the root of this, which is eight, and subtract from it half the number of roots, which is five; the remainder is three. This is the root of the square which you sought for; the square itself is nine._




![Text pages from Algebra manuscript with geometrical solutions to two quadratic equations. Shelfmark: MS. Huntington 214 fol. 004v-005r](../figure/alKhwarizmi.jpg){#alKhwarizmi .class width=300px height=300px}

![An explanation for children of the two digit addition algorithm](../figure/addition_regrouping.jpg){#childrenalg .class width=300px height=300px}


For the purposes of this book, we will need a much more precise way to describe algorithms.
Fortunately (or is it unfortunately?), at least at the moment, computers lag far behind school-age children in learning from examples.
Hence in the 20th century people have come up with  exact formalisms for describing algorithms, namely _programming languages_.
Here is al-Khwarizmi's quadratic equation solving  algorithm described in the _Python_ programming language:^[This is not a programming textbook, and it is absolutely fine if you don't know Python. Still the code below should be fairly self-explanatory.]

```python
from math import sqrt
#Pythonspeak to enable use of the sqrt function to compute square roots.

def solve_eq(b,c):
    # return solution of x^2 + bx = c following Al Khwarizmi's instructions
    # Al Kwarizmi demonstrates this for the case b=10 and c= 39

    val1 = b/2.0 # "halve the number of the roots"
    val2 = val1*val1 # "this you multiply by itself"
    val3 = val2 + c # "Add this to thirty-nine"
    val4 = sqrt(val3) # "take the root of this"
    val5 = val4 - val1 # "subtract from it half the number of roots"
    return val5  # "This is the root of the square which you sought for"

# Test: solve x^2 + 10*x = 39
print(solve_eq(10,39))
# 3.0
```


We can define algorithms informally as follows:

::: {.quote }
__Informal definition of an algorithm:__ An _Algorithm_ is a set of instructions of how to compute an output from an input by following a sequence of "elementary steps".

An algorithm $A$ _computes_ a function $F$ if for every input $x$, if we follow the instructions of $A$ on the input $x$, we obtain the output $F(x)$.
:::



In this chapter we will use an ultra-simple "programming language" to give a _formal_ (that is, _precise_) definition of  algorithms. (In fact, our programming language will be so  simple that it is hardly worthy of this name.)
However, it will take us some time to get there.
We will start by discussing what are "elementary operations" and also how do we map a description of an algorithm into an actual physical process that produces an output from an input in the real world.




### Boolean formulas with AND, OR, and NOT.



An algorithm breaks down a complex calculation into a series of simpler steps.
These steps can be executed in a variety of different ways, including:

* Writing down symbols on a piece of paper

* Modifying the current flowing on electrical wires.

* Binding a protein to a strand of DNA

* Response to a stimulus by a member of a collection (e.g., a bee in a colony, a trader in a market).


To formally define algorithms, let us try to "err on the side of simplicity" and model our "basic steps" as truly minimal.
For example, here are some very simple functions:

* $OR:\{0,1\}^2 \rightarrow \{0,1\}$ defined as

$$OR(a,b) = \begin{cases} 0 & a=b=0 \\ 1 & \text{otherwise} \end{cases}$$

* $AND:\{0,1\}^2 \rightarrow \{0,1\}$ defined as

$$AND(a,b) = \begin{cases} 1 & a=b=1 \\ 0 & \text{otherwise} \end{cases}$$

* $NOT:\{0,1\} \rightarrow \{0,1\}$ defined as $NOT(a) = 1-a$.

The $AND$, $OR$ and $NOT$  functions are the basic logical operators  used in logic and many computer system.
Each one of these functions takes either one or two single bits as input, and produces a single bit as output.
Clearly, it cannot get much more basic than that.
However, the power of computation comes from _composing_ simple building blocks together.

Here is an example. Consider the function $MAJ:\{0,1\}^3 \rightarrow \{0,1\}$ that is defined as follows:

$$MAJ(x) = \begin{cases}1 & x_0 + x_1 + x_2 \geq 2 \\ 0 & \text{otherwise}\end{cases} \;.$$
That is, for every $x\in \{0,1\}^3$, $MAJ(x)=1$ if and only if the majority (i.e., at least two out of the three) of $x$'s coordinates are equal to $1$.
Can you come up with a formula involving $AND$, $OR$ and $NOT$ to compute $MAJ$?

::: { .pause }
It is useful for you to pause at this point and work out the formula for yourself. As a hint, although it is needed to compute some functions, you will not need to use the $NOT$ operator to compute $MAJ$.
:::

Let us first try to rephrase $MAJ(x)$ in words: "$MAJ(x)=1$ if and only if there exists some pair of distinct coordinates $i,j$ such that both $x_i$ and $x_j$ are equal to $1$." In other words it means that $MAJ(x)=1$ iff   _either_ both $x_0=1$ _and_ $x_1=1$,  _or_ both $x_1=1$ _and_ $x_2=1$, _or_ both $x_0=1$ _and_ $x_2=1$.
Since the $OR$ of three conditions $c_0,c_1,c_2$ can be written as $OR(c_0,OR(c_1,c_2))$, we can now translate this into a formula as follows:

$$
MAJ(x_0,x_1,x_2) = OR\left(\, AND(x_0,x_1)\;,\; OR \bigl( AND(x_1,x_2) \;,\; AND(x_0,x_2) \bigr) \, \right) \;. \label{eqmajandornot}
$$

It is common to use $a \vee b$ for $OR(a,b)$ and $a \wedge b$ for $AND(a,b)$, as well as write $a \vee b \vee c$ as shorthand for $(a \vee b) \vee c$. ($NOT(a)$ is often written as either $\neg a$ or $\overline{a}$; we will use both notations in this book.) With this notation,
[eqmajandornot](){.eqref}  can also be written as

$$MAJ(x_0,x_1,x_2) = (x_0 \wedge x_1) \vee (x_1 \wedge x_2) \vee (x_0 \wedge x_3)\;.$$



We can also write  [eqmajandornot](){.eqref} in a   "programming language" format, expressing it as a set of instructions for computing $MAJ$ given the basic operations $AND,OR,NOT$:

```python
def MAJ(X[0],X[1],X[2]):
    firstpair  = AND(X[0],X[1])
    secondpair = AND(X[1],X[2])
    thirdpair  = AND(X[0],X[2])
    temp       = OR(secondpair,thirdpair)
    return OR(firstpair,temp)
```

Yet a third way to describe the same computation is by a _Boolean circuit_.
Think of having _wires_ that can carry a signal that is either the value $0$ or $1$. ^[In practice, this is [often  implemented](https://goo.gl/gntTQE) by electric potential or _voltage_ on a wire, where for example voltage above a certain level is interpreted as a logical value of $1$, and below a certain level is interpreted as a logical value of $0$.]
An _OR gate_ is a gadget that has two incoming wires and one outgoing wires, and is designed so that if the signals on the incoming wires are $a$ and $b$ respectively (for $a,b \in \{0,1\}$), then the signal on the outgoing wire will be $OR(a,b)$.
AND and NOT gates are defined similarly.
Using this, we can express [eqmajandornot](){.eqref} as a circuit as well:

![](../figure/majandorcirc.pnj){#figid .class width=300px height=300px} \

::: {.example title="Computing $XOR$ from $AND$,$OR$,$NOT$" #XORandornotexample}
Let us see how we can obtain a different function from these building blocks.
Define $XOR:\{0,1\}^2 \rightarrow \{0,1\}$ to be the function $XOR(a,b)= a + b \mod 2$. That is, $XOR(0,0)=XOR(1,1)=0$ and $XOR(1,0)=XOR(0,1)=1$.
We claim that we can construct $XOR$ using only $AND$, $OR$, and $NOT$.

Here is an algorithm to compute $XOR(a,b)$ using $AND,NOT,OR$ as basic operations:

1. Compute $w1 = AND(a,b)$ \
2. Compute $w2 = NOT(w1)$ \
3. Compute $w3 = OR(a,b)$ \
4. Output $AND(w2,w3)$ \

We can also express this algorithm as a circuit:

![A circuit with $AND$, $OR$ and $NOT$ gates (denoted as $\wedge,\vee,\neg$ respectively) for computing the $XOR$ function.](../figure/xorandornotcirc.png){#andornotcircxorfig  .class width=300px height=300px} \

Last but not least, we can also express it in a programming language.
Specifically, the following is a _Python_ program that computes the $XOR$ function:

```python
def AND(a,b): return a*b
def OR(a,b):  return 1-(1-a)*(1-b)
def NOT(a): return 1-a

def XOR(a,b):
    w1 = AND(a,b)
    w2 = NOT(w1)
    w3 = OR(a,b)
    return AND(w2,w3)

print([f"XOR({a},{b})={XOR(a,b)}" for a in [0,1] for b in [0,1]])
# ['XOR(0,0)=0', 'XOR(0,1)=1', 'XOR(1,0)=1', 'XOR(1,1)=0']
```
:::






::: {.example title="Computing $XOR$ on three bits" #xorthree}
Extending the same ideas, we can use these basic operations to compute the function $XOR_3:\{0,1\}^3 \rightarrow \{0,1\}$ defined as $XOR_3(a,b,c) = a + b + c (\mod 2)$  by computing first $d=XOR(a,b)$ and then outputting $XOR(d,c)$.
In Python this is done as follows:

```python
def XOR3(a,b,c):
    w1 = AND(a,b)
    w2 = NOT(w1)
    w3 = OR(a,b)
    w4 = AND(w2,w3)
    w5 = AND(w4,c)
    w6 = NOT(w5)
    w7 = OR(w4,c)
    return AND(w6,w7)

print([f"XOR3({a},{b},{c})={XOR3(a,b,c)}" for a in [0,1] for b in [0,1] for c in [0,1]])
# ['XOR3(0,0,0)=0', 'XOR3(0,0,1)=1', 'XOR3(0,1,0)=1', 'XOR3(0,1,1)=0', 'XOR3(1,0,0)=1', 'XOR3(1,0,1)=0', 'XOR3(1,1,0)=0', 'XOR3(1,1,1)=1']
```
:::


> # { .pause }
Try to generalize the above examples to  obtain a way to compute $XOR_n:\{0,1\}^n \rightarrow \{0,1\}$ for every $n$ using at most $4n$ basic steps involving applications of a function in $\{ AND, OR , NOT \}$ to outputs or previously computed values.



### The NAND function

Here is another function we can compute using $AND,OR,NOT$.
The $NAND$ function maps $\{0,1\}^2$ to $\{0,1\}$ and is defined as

$$NAND(a,b) = \begin{cases} 0 & a=b=1 \\ 1 & \text{otherwise} \end{cases}$$

As its name implies, $NAND$ is the NOT  of AND (i.e., $NAND(a,b)= NOT(AND(a,b))$), and so we can clearly compute $NAND$ using $AND$  and $NOT$. Interestingly, the opposite direction also holds:

> # {.theorem title="NAND computes AND,OR,NOT" #univnandonethm}
We can compute $AND$, $OR$, and $NOT$ by composing only the $NAND$ function.

> # {.proof data-ref="univnandonethm"}
We start with the following observation. For every $a\in \{0,1\}$, $AND(a,a)=a$. Hence, $NAND(a,a)=NOT(AND(a,a))=NOT(a)$.
This means that $NAND$ can compute $NOT$, and since by the principle of "double negation",  $AND(a,b)=NOT(NOT(AND(a,b)))$ this means that we can use $NAND$ to compute $AND$ as well.
Once we can compute $AND$ and $NOT$, we can compute $OR$ using the so called ["De Morgan's Law"](https://goo.gl/TH86dH):  $OR(a,b)=NOT(AND(NOT(a),NOT(b)))$ (which can also be written as $a \vee b = \overline{\overline{a} \wedge \overline{b}}$) for every $a,b \in \{0,1\}$.

> # { .pause }
[univnandonethm](){.ref}'s proof is very simple, but you should make sure that __(i)__ you understand the statement of the theorem, and __(ii)__ you follow its proof completely. In particular, you should make sure you understand why De Morgan's law is true.


::: {.remark title="Verify NAND's universality by Python (optional)" #verifynanduniversalitybyptyon}
If you are so inclined, you can also verify the proof of [univnandonethm](){.ref} by Python:

```python
def NAND(a,b): return 1-a*b

def ORwithNAND(a,b):
    return NAND(NAND(a,a),NAND(b,b))

print([f"Test {a},{b}: {ORwithNAND(a,b)==OR(a,b)}" for a in [0,1] for b in [0,1]])
# ['Test 0,0: True', 'Test 0,1: True', 'Test 1,0: True', 'Test 1,1: True']
```
:::


> # {.solvedexercise title="Compute majority with NAND" #majbynandex}
Let $MAJ: \{0,1\}^3 \rightarrow \{0,1\}$ be the function that on input $a,b,c$ outputs $1$ iff $a+b+c \geq 2$. Show how to compute $MAJ$ using a composition of $NAND$'s.

::: {.solution data-ref="majbynandex"}
Recall that [eqmajandornot](){.eqref} stated that

$$
MAJ(x_0,x_1,x_2) = OR\left(\, AND(x_0,x_1)\;,\; OR \bigl( AND(x_1,x_2) \;,\; AND(x_0,x_2) \bigr) \, \right) \;. \label{eqmajandornotrestated}
$$

We we can use [univnandonethm](){.ref}  to replace all the occurrences of $AND$ and $OR$   with $NAND$'s.
Specifically, we can use the equivalence $AND(a,b)=NOT(NAND(a,b))$, $OR(a,b)=NAND(NOT(a),NOT(b))$, and $NOT(a)=NAND(a,a)$ to replace the righthand side of
[eqmajandornotrestated](){.eqref} with an expression involving only $NAND$, yielding that $MAJ(a,b,c)$ is equivalent the (somewhat unwieldy) expression

$$
\begin{gathered}
NAND \biggl(\, NAND\Bigl(\, NAND\bigl(NAND(a,b),NAND(a,c)\bigr), \\
NAND\bigl(NAND(a,b),NAND(a,c)\bigr)\, \Bigr),\\
NAND(b,c) \, \biggr)
\end{gathered}
$$


This corresponds to the following circuit with $NAND$ gates:

![](../figure/majcircnand.png){#figid .class width=300px height=300px}  \
:::


<!--
```python
def MAJ(a,b,c): return 1 if a+b+c >=2 else 0


print([MAJ(a,b,c)==NAND(NAND(NAND(NAND(a,b),NAND(a,c)),NAND(NAND(a,b),NAND(a,c))),NAND(b,c)) for a in [0,1] for b in [0,1] for c in [0,1]])
```
-->


## Informally defining "basic operations" and "algorithms"

[univnandonethm](){.ref} tells us that we can use applications of the single function $NAND$ to obtain $AND$, $OR$, $NOT$, and so by extension all the other functions that can be built up from them.
So, if we wanted to decide on a "basic operation", we might as well choose $NAND$, as we'll get "for free" the three other operations $AND$, $OR$ and $NOT$.
This suggests  the following definition of an "algorithm":


::: {.quote}
__Semi-formal definition of an algorithm:__ An _algorithm_  consists of a sequence of steps of the form "store the NAND of variables `bar` and `blah` in variable `foo`".


An algorithm $A$ _computes_ a function $F$ if for every input $x$ to $F$, if we feed $x$ as input to the algorithm, the value computed in its last step is $F(x)$.
:::


There are several concerns that are raised by this definition:

1. First and foremost, this definition is indeed too informal. We do not specify exactly what each step does, nor what it means to "feed $x$ as input".

2. Second, the choice of $NAND$ as a basic operation seems arbitrary. Why just $NAND$? Why not $AND$, $OR$ or $NOT$? Why not allow operations like addition and multiplication? What about any other logical constructions such `if`/`then` or `while`?

3. Third, do we even know that this definition has anything to do with actual computing? If someone gave us a description of such an algorithm, could we use it to actually compute the function in the real world?


> # { .pause }
These concerns will to a large extent guide us in the upcoming chapters. Thus you would be well advised to re-read the above informal definition and see what you think about these issues.


A large part of this course will be devoted to addressing the above issues.
We will see that:

1. We can make the definition of an algorithm fully formal, and so give a precise mathematical meaning to statements such as "Algorithm $A$ computes function $F$".

2. While the choice of $NAND$ is arbitrary, and we could just as well chose some other functions, we will also see this choice does not matter much. Our notion of an algorithm is not more restrictive because we only think of $NAND$ as a basic step. We have already seen that allowing $AND$, $OR$, $NOT$ as basic operations will not add any power (because we can compute them from $NAND$'s via [univnandonethm](){.ref}). We will see that the same is true for addition, multiplication, and essentially every other operation that could be reasonably thought of as a basic step.

3. It turns out that we can and do compute such "$NAND$ based algorithms" in the real world. First of all, such an algorithm is clearly well specified, and so can be executed by a human with a pen and paper. Second, there are a variety of ways to _mechanize_ this computation. We've already seen that we can write Python code that corresponds to following such a list of instructions. But in fact we can directly implement operations such as $NAND$, $AND$, $OR$, $NOT$ etc.. via electronic signals using components known as _transistors_. This is how modern electronic computers operate.

In the remainder of this chapter, we will begin to answer some of these questions.
We will see more examples of the power of simple operations like $NAND$ (or equivalently, $AND$, $OR$, $NOT$, as well as many other choices) to compute more complex operations including addition, multiplication, sorting and more.
We will then discuss how to _physically implement_ simple operations such as NAND using a variety of technologies.
Finally we will define the _NAND programming language_ that will be our formal model of computation.


## From NAND to infinity and beyond...

We have seen that using $NAND$, we can compute $AND$, $OR$, $NOT$ and $XOR$.
But this still seems a far cry from being able to add and multiply numbers, not to mention more complex programs such as sorting and searching, solving equations, manipulating images, and so on.
We now give a few examples demonstrating how we can use these simple operations to do some more complicated tasks.
While we will not go as far as implementing   [Call of Duty](https://goo.gl/DdJZFF) using $NAND$, we will at least show how we can compose $NAND$ operations to obtain tasks such as addition, multiplications, and comparisons.

### NAND Circuits

We can describe the computation of a  function $F:\{0,1\}^n \rightarrow \{0,1\}$ via a composition of $NAND$ operations in terms of a _circuit_, as was done in [XORandornotexample](){.ref}.
Since in our case, all the gates are the same function (i.e., $NAND$), the description of the circuit is even simpler.
We can think of the circuit as a directed graph.
It has a vertex for every one of the input bits, and also for every intermediate  value  we use in our computation.
If we compute a value $u$ by applying $NAND$ to $v$ and $w$ then we put a directed edges from $v$ to $u$ and from $w$ to $u$.
We will follow the convention of using  "$x$" for inputs and "$y$" for outputs, and hence write $x_0,x_1,\ldots$ for our inputs and $y_0,y_1,\ldots$ for our outputs. (We will sometimes also write these as `X[0]`,`X[1]`,$\ldots$ and  `Y[0]`,`Y[1]`,$\ldots$ respectively.)
Here is a more formal definition:

> # { .pause }
Before reading the formal definition, it would be an extremely good exercise  for you to pause here and try to think how _you_ would formally define the notion of a NAND circuit.
Sometimes working out the definition for yourself is easier than parsing its text.

> # {.definition title="NAND circuits" #nandcircdef}
Let $n,m,s > 0$. A NAND circuit $C$ with $n$ inputs, $m$ outputs, and $s$ gates is a labeled directed acyclic graph (DAG)
with $n+s$ vertices such that:
>
* $C$ has $n$ vertices with no incoming edges, which are called  the _input vertices_ and are labeled with `X[`$0$`]`,$\ldots$, `X[`$n-1$`]`. \
* $C$ has $s$ vertices each with exactly two (possibly parallel) incoming edges, which are called the _gates_.  \
* $C$ has $m$  gates which are called the _output vertices_ and are labeled with `Y[`$0$`]`,$\ldots$,`Y[`$m-1$`]`. The output vertices have no outgoing edges.
>
For $x\in \{0,1\}^n$, the _output_ of $C$ on input $x$, denoted by $C(X)$, is computed in the natural way.
For every $i\in [n]$, we assign to the  input vertex `X[`$i$`]` the value $x_i$, and then continuously assign to every gate the value which is the NAND of the values assigned to its two incoming neighbors. The output is the string $y\in \{0,1\}^m$ such that for every $j \in [m]$, $y_j$ is the value assigned to the output gate labeled with `Y[`$j$`]`.


> # { .pause }
[nandcircdef](){.ref} is perhaps our first encounter with a somewhat complicated definition.
When you are faced with such a definition, there are several strategies to try to understand it:
>
1. First, as we suggested above, you might want to see how _you_ would formalize the intuitive notion that the definitions tries to capture. If we made different choices than you would, try to think why is that the case. \
2. Then, you should read the definition carefully, making sure you understand all the terms that it uses, and all the conditions it imposes. \
3. Finally, try to  how the definition corresponds  to  simple examples such as the NAND circuit presented in [eqmajusingandor](){.ref}, as well as the examples illustrated below.



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
The increment operation can be very informally described as follows: _"Add $1$ to the least significant bit and propagate the carry"_.
A little more precisely, in the case of the binary representation, to obtain the increment of $x$, we scan $x$ from the least significant bit onwards, and flip all $1$'s to $0$'s until we encounter a bit equal to $0$, in which case we flip it to $1$ and stop.
(Please verify you understand why this is the case.)
>
Thus we can compute the increment of $x_0,\ldots,x_{n-1}$ by doing the following:
>
1. Set $c_0=1$ (we pretend we have a "carry" of $1$ initially)
2. For $i=0,\ldots, n-1$ do the following:
  a. Let $y_i = XOR(x_i,c_i)$.
   b. If $c_i=x_i=1$ then $c_{i+1}=1$, else $c_{i+1}=0$.
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



:::  {.example title="Addition using NANDs" #additionnandcirc}
Once we have the increment operation, we can certainly compute addition by repeatedly incrementing (i.e., compute $x+y$ by performing $INC(x)$ $y$ times).
However, that would be quite inefficient and unnecessary.
With the same idea of keeping track of carries we can implement the "grade-school" algorithm for addition to compute the function $ADD_n:\{0,1\}^{2n} \rightarrow \{0,1\}^{n+1}$ that on input $x\in \{0,1\}^{2n}$ outputs the binary representation of the sum of the numbers represented by $x_0,\ldots,x_{n-1}$ and $x_{n+1},\ldots,x_n$:

1. Set $c_0=0$.
2. For $i=0,\ldots,n-1$:
   i. Let $y_i = x_i + x_{n+i} + c_i (\mod 2)$.
   ii. If $x_i + x_{n+i} + c_i \geq 2$ then $c_{i+1}=1$.
3. Let $y_n = c_n$

Once again, this can be translated into a NAND circuit.
To transform Step 2.b to a NAND circuit we use the fact (shown in [majbynandex](){.ref}) that the function $MAJ_3:\{0,1\}^3 \rightarrow \{0,1\}$ can be computed  using $NAND$s.
:::


## Physical implementations of computing devices.


_Computation_ is an abstract notion, that is distinct from its physical _implementations_.
While most modern computing devices are obtained by mapping logical gates to semi-conductor based transistors, over history people have computed using a huge variety of mechanisms,  including mechanical systems, gas and liquid (known as _fluidics_), biological and chemical processes, and even living creatures (e.g., see [crabfig](){.ref} or  [this video](https://www.youtube.com/watch?v=czk4xgdhdY4) for how crabs or slime mold can be used to do computations).


In this section we will  review some of these implementations, both so  you can get an appreciation of how it is possible to directly translate NAND programs to the physical world, without going through the entire stack of architecture, operating systems, compilers, etc. as well as to emphasize that silicon-based processors are by no means the only way to perform computation.
Indeed, as we will see much later in this course, a very exciting recent line of works involves using different media for computation that would allow us to take advantage of _quantum mechanical effects_ to enable different types of algorithms.

![Crab-based logic gates from the paper "Robust soldier-crab ball gate" by Gunji, Nishiyama and Adamatzky. This is an example of an AND gate that relies on the tendency of two swarms of crabs arriving from different directions to combine to a single swarm that continues in the average of the directions.](../figure/crab-gate.jpg){#crabfig .class width=200px height=200px}



### Transistors and physical logic gates

A _transistor_ can be thought of as an electric circuit with two inputs, known as _source_ and _gate_ and an output, known as the _sink_.
The gate controls whether current flows from the source to the sink.
In a _standard transistor_, if the gate is "ON" then current can flow from the source to the sink and if it is "OFF" then it can't.
In a _complementary transistor_ this is reversed: if the gate is "OFF" then current can flow from the source to the sink and if it is "ON" then it can't.

![We can implement the logic of transistors using water. The water pressure from the gate closes or opens a faucet between the source and the sink.](../figure/transistor_water.png){#transistor-water-fig .class width=300px height=300px}

There are several ways to implement the logic of a transistor.
For example, we can use faucets to implement it using water pressure (e.g. [transistor-water-fig](){.ref}).^[This might seem as merely a  curiosity but there is a field known as [fluidics](https://en.wikipedia.org/wiki/Fluidics) concerned with implementing logical operations using liquids or gasses. Some of the motivations include operating in extreme environmental conditions such as in space or  a battlefield, where standard electronic equipment would not survive.]
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


## Basing computing on other media (optional)

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
As we will discuss later in this course, cellular automata such as Conway's "Game of Life" can be used to simulate computation gates (see [gameoflifefig](){.ref}).

![An AND gate using a "Game of Life" configuration. Figure taken from [Jean-Philippe Rennard's paper](http://www.rennard.org/alife/CollisionBasedRennard.pdf).](../figure/game_of_life_and.png){#gameoflifefig .class width=300px height=300px}


### Neural networks

One computation device that we all carry with us is our own _brain_.
Brains have served humanity throughout history, doing computations  that range from  distinguishing prey from predators, through making scientific discoveries and artistic masterpieces, to composing witty 280 character  messages.
The exact working of the brain is still not fully understood, but it seems that to a first approximation it can be modeled by a (very large) _neural network_.

A neural network is a Boolean circuit that instead of $NAND$ (or even $AND$/$OR$/$NOT$) uses some other gates as the basic basis.
For example, one particular basis we can use are _threshold gates_.
For every vector $w= (w_0,\ldots,w_{k-1})$ of integers  and  integer $t$ (some or all of whom  could be negative),
the _threshold function corresponding to $w,t$_ is the function
$T_{w,t}:\{0,1\}^k \rightarrow \{0,1\}$ that maps $x\in \{0,1\}^k$ to $1$ if and only if $\sum_{i=0}^{k-1} w_i x_i \geq t$.
For example, the threshold function $T_{w,t}$ corresponding to $w=(1,1,1,1,1)$ and $t=3$ is simply the majority function $MAJ_5$ on $\{0,1\}^5$.
The function $NAND:\{0,1\}^2 \rightarrow \{0,1\}$  is the threshold function corresponding to $w=(-1,-1)$ and $t=-1$, since $NAND(x_0,x_1)=1$ if and only if $x_0 + x_1 \leq 1$ or equivalently, $-x_0 - x_1 \geq -1$.^[Threshold is just one example of gates that can  used by neural networks. More generally, a neural network is often described as operating on signals that are real numbers, rather than $0/1$ values, and where the output of a gate on inputs $x_0,\ldots,x_{k-1}$ is obtained by applying $f(\sum_i w_i x_i)$ where $f:\R \rightarrow \R$ is an an [activation function](https://goo.gl/p9izfA) such as rectified linear unit (ReLU), Sigmoid, or many others. However, for the purpose of our discussion, all of the above are equivalent. In particular we can reduce the real case to the binary case by a real number in the binary basis, and multiplying the weight of the bit corresponding to the $i^{th}$ digit by $2^i$.]



Threshold gates can be thought of as an approximation for    _neuron cells_ that make up the core of human and animal brains. To a first approximation, a neuron has $k$ inputs and a single output and the neurons  "fires" or "turns on" its output when those signals pass some threshold.
Unlike the cases above, when we considered the number of inputs to a gate $k$ to be a small constant, in such  neural networks we often do not put any bound on the number of inputs.
However, since any threshold function on $k$ inputs can be computed by a NAND circuit of at most $poly(k)$  gates (see [threshold-nand-ex](){.ref}),  NAND circuits are no less powerful than  neural networks.

### The marble computer

We can implement computation using many other physical media, without need for any electronic, biological, or chemical components. Many suggestions for _mechanical_ computers have been put forward, starting with Charles Babbage's  1837 plan for a mechanical ["Analytical Engine"](https://en.wikipedia.org/wiki/Analytical_Engine).

As one example, [marblefig](){.ref} shows a simple implementation of a NAND gate using marbles going through pipes. We represent a logical value in $\{0,1\}$ by a pair of pipes, such that there is a marble flowing through exactly one of the pipes.
We call one of the pipes the "$0$ pipe" and the other the "$1$ pipe", and so the identity of the pipe containing the marble determines the logical value.
A NAND gate would correspond to some mechanical object with two pairs of incoming pipes and one pair of outgoing pipes, such that for every $a,b \in \{0,1\}$, if two marble are rolling toward the object  in the $a$ pipe of the first pair  and the $b$ pipe of the second pair, then a marble will roll out of the object in the $NAND(a,b)$-pipe of the outgoing pair.

As shown in [marblefig](){.ref}, we  can achieve such a NAND gate in a fairly straightforward way, together with a gadget that ensures that at most one marble flows in each wire. Such NAND gates can be combined together to form for every $n$-input NAND circuit $P$ a physical computer that simulates $P$ in the sense that if the marbles are placed in its ingoing pipes according to some input
$x\in \{0,1\}^n$, then eventually marbles will come out of its outgoing pipes according to the output $P(x)$.^[If our circuit uses the same value as input to more than one gate then we will need also a "copying gadget", that given input $a\in \{0,1\}$ outputs two copies of $a$. However, such a gadget is easy to construct using the same ideas, and we leave doing so as an exercise for the reader.]


![A physical implementation of a NAND gate using marbles. Each  wire in a Boolean circuit is modeled by a pair of pipes representing the values $0$ and $1$ respectively, and hence a gate has four input pipes (two for each logical input) and two output pipes. If one of the input pipes representing the value $0$ has a marble in it then that marble will flow to the output pipe representing the value $1$. (The dashed line represent a gadget that will ensure that at most one marble is allowed to flow onward in the pipe.) If both the input pipes representing the value $1$ have marbles in them, then the first marble will be stuck but the second one will flow onwards to the output pipe representing the value $0$.](../figure/marble.png){#marblefig .class width=300px height=300px}

![A "gadget" in a pipe that ensures that at most one marble can pass through it. The first marble that passes causes the barrier to lift and block new ones.](../figure/gadget.png){#gadgetfig .class width=300px height=300px}


## The NAND Programming language { #nandsec }

We now turn to formally defining the notion of algorithm.
We use a _programming language_ to do so.
We define the _NAND Programming Language_ to be a programming language where every line has the following  form:

```python
foo = NAND(bar,blah)
```

where `foo`, `bar` and `blah` are variable identifiers.^[We follow the common [programming languages convention](https://goo.gl/QyHa3b)  of using names such as `foo`, `bar`, `baz`, `blah` as stand-ins for generic identifiers. Generally a variable identifier in the NAND programming language can be any combination of letters and numbers, and we will also sometimes have identifiers such as `Foo[12]`  that end with a number inside square brackets. Later in the course we will introduce programming languages where such identifiers  carry special meaning as _arrays_. At the moment you can treat them as simply any other identifier. The appendix contains a full formal specification of the NAND programming language.]

> # {.example title="Our first NAND program" #NANDprogramexample}
Here is an example of a NAND program: \
>
`u = NAND(X[0],X[1])` \
`v = NAND(X[0],u)` \
`w = NAND(X[1],u)` \
`Y[0] = NAND(v,w)`


> # { .pause }
Do you know what function this program computes? Hint: you have seen it before.


As you might have guessed from this example, we  have two special types of variables in the NAND language: _input variables_ have the form `X[` $i$ `]` where $i$ is a natural number, and _output variables_ have the form `Y[`$j$ `]` where $j$ is a natural number. When a NAND program is _executed_ on input $x \in \{0,1\}^n$, the variable `X[`$i$ `]` is assigned the value $x_i$ for all $i\in [n]$. The _output_ of the program is the list of $m$ values  `Y[0]`$\ldots$ `Y[`$m-1$ `]`, where $m-1$ is the largest index for which the variable `Y[`$m-1$ `]` is assigned a value in the program.
If a line of the form `foo = NAND(bar,blah)` appears in the program, then if `bar` is _not_ an input variable of the form `X[`$i$ `]`, then it must have been assigned a value in a previous line, and the same holds for `blah`.
We also forbid assigning a value to an input variable, and applying the NAND operation to an output variable.

We can now formally define the notion of a function being computed by a NAND program:

> # {.definition title="Computing by a NAND program" #NANDcomp}
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$ be some function, and let $P$ be a NAND program. We say that $P$ _computes_ the function $F$ if:
>
1. $P$ has $n$ input variables `X[`$0$`]`$,\ldots,$`X[`$n-1$`]` and $m$ output variables `Y[`$0$`]`,$\ldots$,`Y[`$m-1$`]`. \
2. For every $x\in \{0,1\}^n$, if we execute $P$ when we assign to `X[`$0$`]`$,\ldots,$`X[`$n-1$`]` the values $x_0,\ldots,x_{n-1}$, then at the end of the execution, the output variables `Y[`$0$`]`,$\ldots$,`Y[`$m-1$`]` have the values $y_0,\ldots,y_{m-1}$ where $y=F(x)$.

> # { .pause }
[NANDcomp](){.ref} is one of the most important definitions in this book. Please make sure to read it time and again until you are sure that you understand it. A full formal specification of the execution model of NAND programs appears in the appendix.


> # {.remark title="Is the NAND programming language Turing Complete? (optional note)" #NANDturingcompleteness}
You might have heard of a term called "Turing Complete" to describe programming languages. (If you haven't, feel free to ignore the rest of this remark: we will encounter this term later in this course and define it properly.)
If so, you might wonder if the NAND programming language has this property.
The answer is no, or perhaps more accurately, the term is not really applicable for the NAND programming language.
The reason is that, by design, the NAND programming language can only compute _finite_ functions $F:\{0,1\}^n \rightarrow \{0,1\}^m$ that take a fixed number of input bits and produce a fixed number of outputs bits.
The term "Turing Complete" is really only applicable to programming languages for _infinite_ functions that can take inputs of arbitrary length.
We will come back to this distinction later on in the course.



### NAND programs and NAND circuits

So far we have described two models of computation:

* _NAND circuits_, which are obtained by applying NAND gates to inputs.

* _NAND programs_, which are obtained by repeatedly applying operations of the form `foo = NAND(bar,blah)`.

A central result is that these two models are actually equivalent:

> # {.theorem title="Circuit and straightline program equivalence" #nandcircuitthm}
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $s\in \N$. Then $F$ is computable by a NAND program of $s$ lines if and only if it is computable by a NAND circuit of $s$ gates.

> # {.proofidea data-ref="nandcircuitthm"}
To understand the proof, you can first work out for yourself the equivalence between the NAND program of [NANDprogramexample](){.ref} and the circuit we have seen in [xornandexample](){.ref}, see also [progandcircfig](){.ref}.
Generally, if we have a NAND program, we can transform it into a circuit by mapping every line `foo = NAND(bar,blah)` of the program into a gate `foo` that is applied to the result of the previous gates `bar` and `blah`. (Since we always assign a variable to variables that have been assigned before or are input variables, we can assume that `bar` and `blah` are either gates we already constructed or are inputs to the circuit.)
In the reverse direction, to map a circuit $C$ into a program $P$ we use [topological sorting](https://goo.gl/QvLE3K) to sort the vertices of the graph of $C$ into an order $v_0,v_1,\ldots,v_{s-1}$ such that if there is an edge from $v_i$ to $v_j$ then $j>i$.
Thus we can transform every gate (i.e. non input vertex) of the circuit into a line in a program in an analogous way: if $v$ is a gate that has two incoming edges from $u$ and $w$, then we add a variable `foo` corresonding to $v$ and a line `foo = NAND(bar,blah)` where `bar` and `blah` are the variables corresponding to $u$ and $w$.

![The NAND code and the corresponding circuit for a program to compute the _increment_ function that maps a string $x\in \{0,1\}^3$ (which we think of as a number in $[7]$) to the string $y\in \{0,1\}^4$ that represents $x+1$. Note how every line in the program corresponds to a gate in the circuit.](../figure/progandcircinc3.png){#progandcircfig .class width=300px height=300px}

> # {.proof data-ref="nandcircuitthm"}
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$ be a function. Suppose that there exists a program $P$ of $s$ lines that computes $F$. We construct a NAND circuit $C$ to compute $F$ as follows: the circuit will include $n$ input vertices, and will include $s$ gates, one for each of the lines of $P$.
We let $I(0),\ldots,I(n-1)$ denotes the vertices corresponding to the inputs and $G(0),\ldots,G(s-1)$ denote the vertices corresponding to the lines.
We connect our gates in the natural way as follows:
>
If the $\ell$-th line of $P$ has the form `foo  = NAND(bar,blah)` where `bar` and `blah` are variables _not_ of the form `X[`$i$`]`, then `bar` and `blah` must have been assigned a value before. We let $j$ and $k$ be the last lines before the $\ell$-th line in which the variables `bar` and `blah` respectively were assigned a value.
In such a case, we will add the edges $\overrightarrow{G(j)\;G(\ell)}$ and $\overrightarrow{G(k)\;G(\ell)}$ to our circuit $C$.
That is, we will apply the gate $G(\ell)$ to the outputs of the gates $G(j)$ and $G(k)$. If `bar` is an input variable of  the form `X[`$i$`]` then we connect $G(\ell)$ to the corresponding input vertex $I(i)$, and do the analogous step if `blah` is an input variable.
Finally, for every $j\in [m]$, if $\ell(j)$ is the last line which assigns a value to `Y[`$j$`]`, then we mark the gate $G(j)$ as the $j$-th output gate of the circuit $C$.
>
We claim that the circuit $C$ computes the same function as the program $P$. Indeed, one can show by induction on $\ell$ that  for every input $x\in \{0,1\}^n$, if we execute $P$ on input $x$, then the value assigned to the variable in the $\ell$-th line is the same as the value output by the gate $G(\ell)$ in the circuit $C$.
(To see this note that by the induction hypothesis, this is true for the values that the $\ell$-th line uses, as they were assigned a value in earlier lines or are inputs, and both the gate and the line compute the NAND function on these values.)
Hence in particular the output variables of the program will have the same value as the output gates of the circuits.
>
In the other direction, given a circuit $C$ of $s$ gates that computes $F$, we can construct a program of $s$ lines that computes the same function. We use a topological sort to ensure that the $n+s$ vertices of the graph of $C$ are sorted so that all edges go from earlier vertices to later ones, and ensure the first $n$ vertices $0,1,\ldots,n-1$ correspond to the $n$ inputs. (This can be ensured as input vertices have no incoming edges.) Then for every $\ell \in [s]$, the $\ell$-th line of the program $P$ will correspond to the vertex $n+\ell$ of the circuit.
If  vertex $n+\ell$'s incoming neighbors are $j$ and $k$, then the $\ell$-th line will be of the form `Temp[`$\ell$`] = NAND(Temp[`$j-n$`],Temp[`$k-n$`])` (if $j$ and/or $k$ are one of the first $n$ vertices, then we will use the corresponding input variable `X[`$j$`]` and/or `X[`$j$`]` instead).
If vertex $n+\ell$ is the $j$-th output gate, then we use `Y[`$j$`]` as the variable on the righthand side of the $\ell$-th line.
Once again by a similar inductive proof we can show that the program $P$ we constructed computes the same function as the circuit $C$.


> # {.remark title="Constructive proof" #circbypython}
The proof of [nandcircuitthm](){.ref} is _constructive_, in the sense that it yields an explicit transformation from a program to a circuit and vice versa.
The appendix contains code of a _Python_ function that outputs the circuit corresponding to a program.

### Circuits with other gate sets (optional)

There is nothing special about NAND. For every set of functions $\mathcal{G} = \{ G_0,\ldots,G_{k-1} \}$, we can define a notion of circuits that use elements of  $\mathcal{G}$ as gates, and a notion of a "$\mathcal{G}$ programming language" where every line involves assigning to a variable `foo` the result of applying some $G_i \in \mathcal{G}$ to previously defined or input variables.
Specifically, we can make the following definition:

> # {.definition title="General straightline programs" #genstraightlineprogs}
Let $\mathcal{F} = \{ f_0,\ldots, f_{t-1} \}$ be a finite  collection of Boolean functions, such that
$f_i:\{0,1\}^{k_i} \rightarrow \{0,1\}$ for some $k_i \in \N$.
An _$\mathcal{F}$ program_ is a sequence of lines, each of which assigns to some  variable  the result of applying some $f_i \in \mathcal{F}$ to $k_i$ other variables. As above, we use `X[`$i$`]` and `Y[`$j$`]` to denote the input and output variables.


_NAND programs_ corresponds to $\mathcal{F}$ programs for the set  $\mathcal{F}$ that only contains the $NAND$ function, but we can can talk about $\{ AND, OR , NOT \}$ programs, $\{ XOR,0,1\}$ programs, or use any other set.
We can also define _$\mathcal{F}$ circuits_, which will be directed graphs in which the _gates_ corresponds to applying a function $f_i \in \mathcal{F}$, and will each have $k_i$ incoming wires and a single outgoing wire.^[There is a minor technical complication when using gates corresponding to _non symmetric_ functions. A function $f:\{0,1\}^k \rightarrow \{0,1\}$ is _symmetric_ if re-oredring its inputs does not make a difference to the output. For example, the functions $NAND$, $AND$, $OR$ are symmetric. If we consider circuits with gates that are non-symmetric functions, then we need to label each wire entering a gate as to which parameter of the function it correspond to.]
As in [nandcircuitthm](){.ref}, we can show  that $\mathcal{F}$ circuits and $\mathcal{F}$ programs are equivalent.
We have seen that for $\mathcal{F} = \{ AND,OR, NOT\}$, the resulting  circuits/programs  are equivalent in power to the NAND programming language, as we can compute $NAND$ using $AND$/$OR$/$NOT$ and vice versa.
This turns out to be a special case of a general phenomena— the _universality_ of $NAND$ and other gate sets — that we will explore more in depth later in this course.
However, there are some sets $\mathcal{F}$ that are _not_ equivalent in power to $NAND$: see [universalbasisex](){.ref} for more.



> # { .recap }
* An _algorithm_ is a recipe for performing a computation as a sequence of "elementary" or "simple" operations.
* One candidate definition for an "elementary" operation is the $NAND$ operation. It is an operation that is easily implementable in the physical world in a variety of methods including by electronic transistors.
* We can use $NAND$ to compute many other functions, including majority, increment, and others.
* There are other equivalent choices, including the set $\{AND,OR,NOT\}$.
* We can formally define the notion of a function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ being computable using the _NAND Programming language_.
* The notions of being computable by a $NAND$ circuit and being computable by a $NAND$ program are equivalent.

## Exercises

::: {.remark title="Disclaimer" #disclaimerrem}
Most of the exercises have been written in the summer of 2018 and haven't yet been fully debugged. While I would prefer people do not post online solutions to the exercises, I would greatly appreciate if you let me know of any bugs. You can do so by posting a [GitHub issue](https://github.com/boazbk/tcs/issues) about the exercise, and optionally complement this with an email to me with more details about the attempted solution.
:::

::: {.exercise title="Universal basis" #universalbasisex}
Define a set $\mathcal{F}$ of functions to be a _universal basis_ if we can compute $NAND$ using $\mathcal{F}$. For every one of the following sets, either prove that it is a universal basis or prove that it is not.

1. $\mathcal{F} = \{ AND, OR , NOT \}$.

2. $\mathcal{F} = \{ AND, OR  \}$.

3. $\mathcal{F} = \{ OR, NOT  \}$.

4. $\mathcal{F} = \{ NOR   \}$ where $NOR(a,b) = NOT(OR(a,b))$.

5. $\mathcal{F} =  \{ XOR,0,1 \}$ where $0$ and $1$ are the constant functions that take no input and output $0$ and $1$.

6. $\mathcal{F} = \{ LOOKUP_1,0,1 \}$ where $0$ and $1$ are the constant functions as above and  $LOOKUP_1:\{0,1\}^3 \rightarrow \{0,1\}$ satisfies $LOOKUP_1(a,b,c)$ equals $a$ if $c=0$ and equals $b$ if $c=1$.
:::


> # {.exercise title="Bound on universal basis size (challenge)" #universal-bound}
Prove that for every subset $B$ of the functions from $\{0,1\}^k$ to $\{0,1\}$,
if $B$ is universal then there is a $B$-circuit of at most $O(k)$ gates to compute the $NAND$ function (you can start by showing that there is a $B$ circuit of at most $O(k^{16})$ gates).^[Thanks to Alec Sun for solving this problem.]

> # {.exercise title="Threshold using NANDs" #threshold-nand-ex}
Prove that for every $w,t$, the function $T_{w,t}$ can be computed by a NAND program of at most $O(k^3)$ lines.^[TODO: check the right bound, and give it as a challenge program. Also say the conditions under which this can be improved to $O(k)$ or $\tilde{O}(k)$.]


## Biographical notes


## Further explorations

Some topics related to this chapter that might be accessible to advanced students include:

* Efficient constructions of circuits: finding  circuits of minimal size that compute certain functions.

TBC
