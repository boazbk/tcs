---
title: "Loops and infinity"
filename: "lec_06_loops"
chapternum: "6"
---

# Loops and infinity { #chaploops }

> ### { .objectives }
* Learn the model of _Turing machines_, which can compute functions of _arbitrary input lengths_.
* See a programming-language description of Turing machines, using
NAND-TM programs, which add _loops_ and _arrays_ to NAND-CIRC.
* See some basic syntactic sugar and equivalence of variants of Turing machines and NAND-TM programs.

>_"The bounds of arithmetic were however outstepped the moment the idea of applying the [punched] cards had occurred; and the Analytical Engine does not occupy common ground with mere "calculating machines."" ... In enabling mechanism to combine together general symbols, in successions of unlimited variety and extent, a uniting link is established between the operations of matter and the abstract mental processes of the most abstract branch of mathematical science. "_, Ada Augusta, countess of Lovelace, 1843^[Translation of  "Sketch of the Analytical Engine" by L. F. Menabrea, Note A.]


>_"What is the difference between a Turing machine and the modern computer? It's the same as that between Hillary's ascent of Everest and the establishment of a Hilton hotel on its peak."_ , Alan Perlis, 1982.




The model of Boolean circuits  (or equivalently, the NAND-CIRC programming language) has one very significant drawback: a Boolean circuit can only compute a _finite_ function $f$, and in particular the number of inputs of $f$ is always smaller than (twice) the number of gates of the circuit.^[Since very NAND gate has two inputs, the number of inputs that an $s$-gate NAND circuit can depend on is at most $2s$. However, the conceptual point of being only able to handle a finite number of inputs holds for any model of circuits or straight-line programming language.]

This does not capture our intuitive notion of an algorithm as a _single recipe_ to compute a potentially infinite function.
For example, the standard elementary school multiplication algorithm is a _single_ algorithm that multiplies numbers of all lengths, but yet we cannot express this algorithm as a single NAND-CIRC program, but rather need a different NAND-CIRC program for every input length (see [multschoolfig](){.ref}).

![Once you know how to multiply multi-digit numbers, you can do so for every number $n$ of digits, but if you had to describe multiplication using NAND-CIRC programs or Boolean circuits, you would need a different program/circuit for every length $n$ of the input.](../figure/multiplicationschool.png){#multschoolfig .margin  }

Let us consider the case of the simple _parity_ or _XOR_ function  $XOR:\{0,1\}^* \rightarrow \{0,1\}$, where $XOR(x)$ equals $1$ iff the number of $1$'s in $x$ is odd.
As simple as it is, the $XOR$ function cannot be computed by a NAND-CIRC program.
Rather, for every $n$, we can compute $XOR_n$ (the restriction of $XOR$ to $\{0,1\}^n$) using a different NAND-CIRC program. For example, here is the NAND-CIRC program to compute $XOR_5$: (see also [XOR5fig](){.ref})

```python
Temp[0] = NAND(X[0],X[1])
Temp[1] = NAND(X[0],Temp[0])
Temp[2] = NAND(X[1],Temp[0])
Temp[3] = NAND(Temp[1],Temp[2])
Temp[4] = NAND(X[2],Temp[3])
Temp[5] = NAND(X[2],Temp[4])
Temp[6] = NAND(Temp[3],Temp[4])
Temp[7] = NAND(Temp[5],Temp[6])
Temp[8] = NAND(Temp[7],X[3])
Temp[9] = NAND(Temp[7],Temp[8])
Temp[10] = NAND(X[3],Temp[8])
Temp[11] = NAND(Temp[9],Temp[10])
Temp[12] = NAND(Temp[11],X[4])
Temp[13] = NAND(Temp[11],Temp[12])
Temp[14] = NAND(X[4],Temp[12])
Y[0] = NAND(Temp[13],Temp[14])
```

![The circuit for computing the XOR of $5$ bits. Note how it merely repeats four times the circuit to compute the XOR of $2$ bits.](../figure/XOR5circuit.png){#XOR5fig .margin  }


This is rather repetitive, and more importantly, does not capture the fact that there is a _single_ algorithm to compute the parity on all inputs.
Typical programming language use the notion of _loops_ to express such an algorithm, and so we might have wanted to use code such as:

```python
# s is the "running parity", initialized to 0
while i<len(X):
    u = NAND(s,X[i])
    v = NAND(s,u)
    w = NAND(X[i],u)
    s = NAND(v,w)
    i+= 1
Y[0] = s
```

In this chapter we will show how we can extend the   NAND-CIRC programming language so that it can capture these kinds of constructs.
We will see two ways to do so:


* _Turing machines_, invented by Alan Turing in 1936, are an hypothetical abstract device that can yields a finite description of an algorithm that can handle arbitrarily long inputs.


* The _NAND-TM Programming language_ extends   NAND-CIRC with the notion of _loops_ and _arrays_ to allow a finite program that can compute a function with arbitrarily long inputs.

It turns out that these two models are _equivalent_, and in fact they are equivalent to a great many other computational models including programming languages you may be familiar with such as C, Java, Python, Javascript, OCaml, and so on and so forth. This notion, known as _Turing equivalence_ or _Turing completeness_, will be discussed in [chapequivalentmodels](){.ref}.
We start off by presenting Turing machines and then show their equivalence to NAND-TM, though it is also possible to present these in the opposite order.



## Turing Machines


>_"Computing is normally done by writing certain symbols on paper. We may suppose that this paper is divided into squares like a child's arithmetic book.. The behavior of the \[human\] computer at any moment is determined by the symbols which he is observing, and of his 'state of mind' at that moment... We may suppose that in a simple operation not more than one symbol is altered."_, \
>_"We compare a man in the process of computing ... to a machine which is only capable of a finite number of configurations... The machine is supplied with a 'tape' (the analogue of paper) ... divided into sections (called 'squares') each capable of bearing a 'symbol' "_, Alan Turing, 1936



![Aside from his many other achievements, Alan Turing was an excellent long distance runner who just fell shy of making England's olympic team. A fellow runner once asked him why he punished himself so much in training. Alan said "I have such a stressful job that the only way I can get it out of my mind is by running hard; it’s the only way I can get some release."](../figure/alan-turing-running.jpg){#turingrunning .margin  }


The "granddaddy" of all models of computation is the _Turing Machine_, which is the standard model of computation in most textbooks.^[This definitional choice does not make much difference since, as we show here, NAND-TM programs are equivalent to Turing machines in their computing power.]
Turing machines were defined in 1936 by Alan Turing in an attempt to formally capture all the functions that can be computed by human "computers" (see [humancomputersfig](){.ref}) that follow a well-defined set of rules, such as the standard algorithms for addition or multiplication.

![Until the advent of electronic computers, the word "computer" was used to describe a person that performed calculations. These human computers were absolutely essential to many achievements including mapping the stars, breaking the Enigma cipher, and the NASA space mission. Photo taken from from [@sobel2017the].](../figure/HumanComputers.jpg){#humancomputersfig .margin  }

Turing thought of such a person as having access to as much "scratch paper" as they need.
For simplicity we can think of this scratch paper as a one dimensional piece of graph paper (or _tape_, as it is commonly referred to),  which is divided to "cells", where each "cell" can hold a single symbol (e.g., one digit or letter, and more generally some element of a finite _alphabet_).
At any point in time, the person can read from and write to a single cell of the paper, and based on the contents can update his/her finite mental state, and/or move to the cell immediately to the left or right of the current one.


![Steam-powered Turing Machine mural, painted by CSE grad students at the University of Washington on the night before spring qualifying examinations, 1987. Image from [https://www.cs.washington.edu/building/art/SPTM](https://www.cs.washington.edu/building/art/SPTM). ](../figure/SPTM.jpg){#steamturingmachine .margin  }



Thus, Turing modeled such a computation by a "machine" that maintains one of $k$ states, and at each point can read and write a single symbol from some alphabet $\Sigma$ (containing $\{0,1\}$) from its "work tape" (see [turing-machine-fig](){.ref}).
To perform computation using this machine, we write the input $x\in \{0,1\}^n$ on the tape, and the goal of the machine is to ensure that at the end of the computation, the value $F(x)$ will be written on the tape.
Specifically, a computation of a Turing Machine $M$ with $k$ states and alphabet $\Sigma$ on input $x\in \{0,1\}^*$ proceeds as follows:

* Initially the machine is at state $0$ (known as the "starting state") and the tape is initialized to $\triangleright,x_0,\ldots,x_{n-1},\varnothing,\varnothing,\ldots$.^[We use the symbol $\triangleright$ to denote the beginning of the tape, and the symbol $\varnothing$ to denote an empty cell. Hence we will assume that $\Sigma$ contains these symbols, along with $0$ and $1$.]

* The location $i$ to which the machine points to is set to $0$.

* At each step, the machine reads the symbol $\sigma = T[i]$ that is in the $i^{th}$ location of the tape, and based on this symbol and its state $s$ decides on:
  - What symbol $\sigma'$ to write on the tape \
  - Whether to move **L**eft (i.e., $i \leftarrow i-1$), **R**ight  (i.e., $i \leftarrow i+1$), **S**tay in place, or **H**alt the computation.
  - What is going to be the new state $s \in [k]$

* The set of rules the Turing machine follows is known as its _transition function_.

* When the machine halts then its output is obtained by reading off the tape from the second location (just after the $\triangleright$) onwards, stopping at the first point where the symbol is not $0$ or $1$.


![A Turing machine has access to a _tape_ of unbounded length. At each point in the execution, the machine can read a single symbol of the tape, and based on that and its current state, write a new symbol, update the tape, decide whether to move left, right, stay, or halt.](../figure/turingmachine.png){#turing-machine-fig   }


### Example:  A Turing machine for palindromes  { #turingmachinepalindrome }

Let $PAL$ (for _palindromes_) be the function that on input $x\in \{0,1\}^*$, outputs $1$ if and only if $x$ is an (even length) _palindrome_, in the sense that $x = w_0 \cdots w_{n-1}w_{n-1}w_{n-2}\cdots w_0$ for some $n\in \N$ and $w\in \{0,1\}^n$.

We now show a Turing Machine $M$ that computes $PAL$. To specify $M$ we need to specify __(i)__ $M$'s tape alphabet $\Sigma$ which should contain at least the symboles $0$,$1$, $\triangleright$ and $\varnothing$, and __(ii)__ $M$'s _transition function_ which determines what action $M$ takes when it reads a given symbol while it is in a particular state.

In our case, $M$ will use the alphabet $\{ 0,1,\triangleright, \varnothing, \times \}$ and will have $k=14$ states. Though the states are simply numbers between $0$ and $k-1$, for convenience we will give them the following labels:

```table
---
caption: ''
alignment: ''
table-width: ''
id: ''
---
State, Label
0, `START`
1,`RIGHT_0`
2,`RIGHT_1`
3,`LOOK_FOR_0`
4,`LOOK_FOR_1`
5,`RETURN`
6,`REJECT`
7,`ACCEPT`
8,`OUTPUT_0`
9,`OUTPUT_1`
10,`0_AND_BLANK`
11,`1_AND_BLANK`
12,`BLANK_AND_STOP`
```



We describe the operation of our Turing Machine $M$ in words:

* $M$ starts in state `START` and will go right, looking for the first symbol that is $0$ or $1$. If we find $\varnothing$ before we hit such a symbol then we will move to the `OUTPUT_1` state that we describe below.

* Once $M$ found such a symbol $b \in \{0,1\}$, $M$ deletes $b$ from the tape by writing the $\times$ symbol, it enters either the `RIGHT_0` or `RIGHT_1` mode according to the value of $b$ and starts moving rightwards until it hits the first $\varnothing$ or $\times$ symbol.

* Once we found this symbol we
 into the state `LOOK_FOR_0` or `LOOK_FOR_1` depending on whether we were in the state `RIGHT_0` or `RIGHT_1` and make one left move.

* In the state `LOOK_FOR_`$b$, we check whether the value on the tape is $b$. If it is, then we delete it by changing its value to $\times$, and move to the state `RETURN`. Otherwise, we change to the `OUTPUT_0` state.

* The `RETURN` state means we go back to the beginning. Specifically, we move leftward until we hit the first symbol that is not $0$ or $1$, in which case we change our state to `START`.

* The `OUTPUT_`$b$ states mean that we are going to output the value $b$. In both these states we go left until we hit $\triangleright$. Once we do so, we make a right step, and change to the `1_AND_BLANK` or `0_AND_BLANK` states respectively. In the latter states, we write the corresponding value, and then move right and change to the `BLANK_AND_STOP` state, in which we write $\varnothing$ to the tape and halt.

The above description can be turned into a table describing for each one of the $13\cdot 5$ combination of state and symbol, what the Turing machine will do when it is in that state and it reads that symbol. This table is known as the _transition function_ of the Turing machine.


### Turing machines: a formal definition



The formal definition of Turing machines is as follows:

:::  {.definition title="Turing Machine" #TM-def}
A (one tape) _Turing machine_ with $k$ states and alphabet $\Sigma \supseteq \{0,1, \triangleright, \varnothing \}$ is represented by a _transition function_
$\delta_M:[k]\times \Sigma \rightarrow [k] \times \Sigma  \times \{\mathsf{L},\mathsf{R}, \mathsf{S}, \mathsf{H} \}$.

For every $x\in \{0,1\}^*$, the _output_ of $M$ on input $x$, denoted by $M(x)$, is the result of the following process:

* We initialize  $T$ to be the sequence $\triangleright,x_0,x_1,\ldots,x_{n-1},\varnothing,\varnothing,\ldots$, where $n=|x|$. (That is, $T[0]=\triangleright$, $T[i+1]=x_{i}$ for $i\in [n]$, and $T[i]=\varnothing$ for $i>n$.)

* We also initialize $i=0$ and $s=0$.

* We then repeat the following process:

   1. Let $(s',\sigma',D) = \delta_M(s,T[i])$.
   2. Set $s \rightarrow s'$, $T[i] \rightarrow \sigma'$.
   3. If $D=\mathsf{R}$ then set $i \rightarrow i+1$, if $D=\mathsf{L}$ then set $i \rightarrow \max\{i-1,0\}$. (If $D = \mathsf{S}$ then we keep $i$ the same.)
   4. If $D=\mathsf{H}$ then halt.

* The _result_ of the process, which we denote by $M(x)$, is the string $T[1],\ldots,T[m]$ where $m>0$ is the smallest integer such that $T[m+1] \not\in \{0,1\}$.  If the process never ends then we denote the result by $\bot$.
:::



::: { .pause }
You should make sure you see why this formal definition corresponds to our informal description of a Turing Machine.
To get more intuition on Turing Machines, you can play with some of the online available simulators such as [Martin Ugarte's](https://turingmachinesimulator.com/), [Anthony Morphett's](http://morphett.info/turing/turing.html), or [Paul Rendell's](http://rendell-attic.org/gol/TMapplet/index.htm).
:::

::: {.remark title="Transition functions vs computed functions, comparison to Sipser" #transitionfunc}
One should not confuse the _transition function_ of a Turing machine $M$ with the function that the machine computes. The transition function is a _finite_ function, with $k|\Sigma|$ inputs and $4k|\Sigma|$ outputs. (Can you see why?)
The machine can compute an _infinite_ function $F$ that takes as input a string $x\in \{0,1\}^*$ of arbitrary length and might also produce an arbitrary length string as output.

In our formal definition, we identified the machine with its transition function since the transition function tells us everything we need to know about the Turing machine, and hence serves as a good mathematical representation of it. This choice of representation is somewhat arbitrary, and is based on our convention that the state space is always the numbers $\{0,\ldots,k-1\}$, where we use $0$ as our starting.
Other texts use different conventions and so their mathematical definition of a Turing machine might look superficially different, but these definitions describe the same computational process and has the same computational powers.

For example, Sipser's text [@SipserBook] allows a more general set of states $Q$ and allow to designate arbitrary elements of $Q$ as starting and halting states, though by simple relabeling of the states one can see that this has no effect on the computational power of the model.
Sipser also restricts attention to Turing machines that output only a single bit. In such cases, it is convenient to have _two halting states_:  one of them is designated as the "$0$ halting state" (often known as the _rejecting state_) and the other as the "$1$ halting state" (often known as the _accepting state_).
Thus instead of writing $0$ or $1$, the machine will enter into one of these states and halt.
This again makes no difference to the computational power, though we prefer to consider the more general model of multi-bit outputs.

Sipser considers also functions with input in $\Sigma^*$ for an arbitrary alphabet $\Sigma$ (and hence distiguishes between the _input alphabet_ which he denotes as $\Sigma$ and the _tape alphabet_ which he denotes as $\Gamma$), while we restrict attention to functions with binary strings as input. Finally (and this is a very minor point) Sipser requires the machine to either move left or right in every step, without the $\mathsf{S}$tay operation, but again staying in place is very easy to emulate by simply moving right and then back left.

The bottom line is that Sipser defines Turing machines as a _seven tuple_ consisting of the state space, input alphabet, tape alphabet, transition function, starting state, accpeting state, and rejecting state. Yet, this is simply a different representation of the same concept, just as a graph can be represented in either adjacency list or adjacency matrix form.
:::

### Computable functions


We now turn to making one of the most important definitions in this book, that of _computable functions_.

::: {.definition title="Computable functions" #computablefuncdef}
Let $F:\{0,1\}^* \rightarrow \{0,1\}^*$ be a (total) function and let $M$ be a Turing machine.  We say that $M$ _computes_ $F$ if for every $x\in \{0,1\}^*$, $M(x)=F(x)$.

We say that a function $F$ is _computable_ if there exists a Turing machine $M$ that computes it.
:::

Defining a function "computable" if and only if it can be computed by a Turing machine might seem "reckless" but, as we'll see in [chapequivalentmodels](){.ref}, it turns out that being computable in the sense of [computablefuncdef](){.ref} is equivalent to being computable in essentially any reasonable model of computation.
This is known as the _Church Turing Thesis_.^[Unlike the _extended_ Church Turing Thesis which we discussed in [PECTTsec](){.ref}, the Church-Turing thesis itself is widely believed and there are no candidate devices that attack it.]


::: { .pause }
[computablefuncdef](){.ref} is, as we mentioned above, one of the most important definitions in this book. Please re-read it (and [TM-def](){.ref}, which it relies upon).
:::






This is a good point to remind the reader of the distinction between _functions_ and _programs_:

$$ \text{Functions} \;\neq\; \text{Programs} $$

A program (or Turing machine) $P$  can _compute_ some function  $F$, but it is not the same as $F$.
In particular there can be more than one program to compute the same function.
Being computable is a property of _functions_, not of machines.

We will often pay special attention to functions $F:\{0,1\}^* \rightarrow \{0,1\}$ that have a single bit of output.
Hence we give a special name for the set of functions of this form that are computable.


> ### {.definition title="The class $\mathbf{R}$" #classRdef}
We define $\mathbf{R}$ be the set of all _computable_ functions $F:\{0,1\}^* \rightarrow \{0,1\}$.



::: {.remark title="Decidable languages" #decidablelanguages}
Many texts use the term _decidable languages_ instead of _computable functions_.
Another term that is often used is _recursive languages_ (which is the reason that the letter $\mathbf{R}$ is often used to denote the set of computable Boolean functions / decidable languages defined in [classRdef](){.ref}).

The name "language"  has its roots in _formal language theory_ as pursued by linguists such as Noam Chomsky.
A _formal language_ is simply a subset $L \subseteq \{0,1\}^*$ (or more generally $L \subseteq \Sigma^*$ for some finite alphabet $\Sigma$).
The _membership_ or _decision_ problem for a language $L$, is the task of determining, given $x\in \{0,1\}^*$, whether or not $x\in L$.
One can see that this task is equivalent to computing the Boolean function  $F:\{0,1\}^* \rightarrow \{0,1\}$ which is defined as $F(x)=1$ iff $x\in L$.
Thus saying that the function $F$ is computable is equivalent to saying that the corresponding language $L$ is decidable.
:::


### Infinite loops and partial functions

One crucial difference between circuits/straight-line programs and Turing machines is the following.
Looking at a NAND-CIRC program $P$, we can always tell how many inputs and how many outputs it has (by simply looking at the `X` and `Y` variables).
Furthermore, we are guaranteed that if we invoke $P$ on any input then _some_ output will be produced.

In contrast, given any Turing machine $M$, we cannot determine a priori the length of the output.
In fact, we don't even know if an output would be produced at all!
For example, it is very easy to come up with a Turing machine whose transition function never outouts $\mathsf{H}$ and hence never halts.


If a machine  $M$ fails to stop and produce an output on some an input $x$, then it cannot compute any total function $F$, since clearly on input $x$, $M$  will fail to output $F(x)$. However, $P$ can still compute a _partial_ function.^[A _partial function_ $F$ from a set $A$ to a set $B$ is a function that is only defined on a _subset_ of $A$, (see [functionsec](){.ref}). We can also think of such a function as mapping $A$ to $B \cup \{ \bot \}$ where $\bot$ is a special "failure" symbol such that $F(a)=\bot$  indicates the function $F$ is not defined on $a$.]

For example, consider the partial function $DIV$ that on input a pair $(a,b)$ of natural numbers, outputs $\ceil{a/b}$ if $b > 0$, and is undefined otherwise.
We can define a turing machine $M$ that computes $DIV$ on input $a,b$ by outputting the first $c=0,1,2,\ldots$ such that $cb \geq a$. If $a>0$ and $b=0$ then the machine $M$ will never halt, but this is OK, since $DIV$ is undefined on such inputs. If $a=0$ and $b=0$, the machine  $M$ will output $0$, which is also OK, since we don't care about what the program outputs on inputs on which $DIV$ is undefined. Formally, we define computability of partial functions as follows:

::: {.definition title="Computable (partial or total) functions" #computablepartialfuncdef}
Let $F$ be either a total or partial function mapping $\{0,1\}^*$ to $\{0,1\}^*$ and let $M$ be a Turing machine.
We say that $M$ _computes_ $F$ if for every $x\in \{0,1\}^*$ on which $F$ is defined, $M(x)=F(x)$.^[Note that if $F$ is a total function, then it is defined on every $x\in \{0,1\}^*$ and hence in this case, this definition is identical to [computablefuncdef](){.ref}.]

We say that a (partial or total) function $F$ is _computable_ if there is a Turing machine that computes it.
:::



## Turing machines as programming languages

The name "Turing machine", with its "tape" and "head" evokes a physical object, while in contrast we think of a _program_ as a piece of text.
But we can think of a Turing machine as a program as well.
For example, consider the Turing Machine $M$ of [turingmachinepalindrome](){.ref} that computes the function $PAL$ such that $PAL(x)=1$ iff $x$ is a palindrome.
We can also describe this machine as a _program_ using the Python-like pseudocode of the form below

```python
# Gets an array Tape that is initialized to [">", x_0 , x_1 , .... , x_(n-1), "∅", "∅", ...]
# At the end of the execution, Tape[1] is equal to 1 if x is a palindrome and is equal to 0 otherwise
def PAL(Tape):
    head = 0
    state = 0 # START
    while (state != 12):
        if (state == 0 && Tape[head]=='0'):
            state = 3 # LOOK_FOR_0
            Tape[head] = 'x'
            head += 1 # move right
        if (state==0 && Tape[head]=='1')
            state = 4 # LOOK_FOR_1
            Tape[head] = 'x'
            head += 1 # move right
        ... # more if statements here
```

The particular details of this program are not important. What is important is that we can describe Turing machines as _programs_.
Moreover, note that when translating a Turing machine into a program, the _tape_ becomes a _list_ or _array_ that can hold values from the finite set $\Sigma$.^[Most programming languages use arrays of fixed size, while a Turing machine's tape is unbounded, though of course there is no need to store an infinite number of $\varnothing$ symbols. If you want, you can think of the tape as a list that starts off at some a length that is just long enough to store the input, but is dynamically grown in size as the Turing machine's head explores new positions.]
The _head position_ can be thought of as an integer valued variable that can hold integers of unbounded size.
The _state_ is a _local register_ that can hold one of a fixed number of values in $[k]$.

More generally we can think of every Turing Machine $M$ as equivalent to a program of the following form:

```python
# Gets an array Tape that is initialized to [">", x_0 , x_1 , .... , x_(n-1), "∅", "∅", ...]
def M(Tape):
    state = 0
    i     = 0
    while (True):
        if Head[i]=="0" and state==7:
            i += 1
            Head[i]="1"
            state = 19
        elif Head[i]==">" and state == 13:
            Head[i]="0"
            state = 15
        elif ...
        ...
        elif Head[i]==">1" and state == 29:
            break
```

Note that if our programming language has only _Boolean_ (i.e., $0$/$1$-valued) variables, then we could replace the variable `state` with $\ceil{\log k}$ Boolean variables.
Similarly, we can represent each element of the alphabet $\Sigma$ using $\ceil{\log |\Sigma|}$ bits.
Hence if our programming language had only Boolean-valued arrays, we could replace the $\Sigma$-valued array `Tape[]` with $\ceil{\log |\Sigma|}$ Boolean-valued arrays `Tape0[]`,$\ldots$, `Tape`$\ell$`[]` for $\ell = \ceil{\log|\Sigma|}$.


### The NAND-TM Programming language

We now introduce the _NAND-TM programming language_, which aims to capture the power of a Turing machine in a programming language formalism.
The main difference between NAND-TM and NAND-CIRC is that NAND-TM will need to model a _single uniform algorithm_ that can compute a function that takes inputs of _arbitrary lengths_.
To do so, we extend the NAND-CIRC programming language with two constructs:

* _Loops_: NAND-CIRC is a _straight-line_ programming language- a NAND-CIRC program of $s$ lines takes exactly $s$ steps of computation and hence in particular cannot even touch more than $3s$ variables. _Loops_ allow us to capture in a short program the instructions for a computation that can take an arbitrary amount of time.

* _Arrays_: A NAND-CIRC program of $s$ lines touches at most $3s$ variables. While we can use variables with names such as  `Foo_17` or `Bar[22]`, they are not true arrays, since the number in the identifier is a constant that is "hardwired" into the program.


Thus a good way to remember NAND-TM is using the following informal equation:

$$
\text{NAND-TM} \;=\; \text{NAND-CIRC} \;+\; \text{loops} \;+\; \text{arrays} \label{eqnandloops}
$$

> ### {.remark title="NAND-CIRC + loops + arrays = everything." #otherpl}
As we will see, adding loops and arrays to NAND-CIRC is enough to capture the full power of all programming languages! Hence we could replace "NAND-TM" with any of _Python_, _C_, _Javascript_, _OCaml_,  etc... in the lefthand side of  [eqnandloops](){.eqref}.
But we're getting ahead of ourselves: this issue will be discussed in [chapequivalentmodels](){.ref}.


Concretely, the NAND-TM programming language adds the following features on top of NANC-CIRC:

* We add a special _integer valued_ variable `i`. All other variables in NAND-TM will be _Boolean valued_ (as in NAND-CIRC).

* We add _arrays_ to the language by allowing variable identifiers to have the form `Foo[i]` with `i` being the special integer-valued variable mentioned above.  `Foo` is an array of Boolean values, and `Foo[i]` refers to the value of this array at location equal to the current value of the variable `i`.

* We use the convention that _arrays_ always start with a capital letter, and _scalar variables_ (which are never indexed with `i`) start with lowercase letters. Hence `Foo` is an array and `bar` is a scalar variable.

* The input and output `X` and `Y` are now considered _arrays_ with values of zeroes and ones.

* We add a special `MODANDJUMP` instruction that takes two boolean variables $a,b$ as input and does the following:
  - If $a=1$ and $b=1$ then `MODANDJUMP(`$a,b$`)` increments `i` by one and jumps to the first line of the program.
  - If $a=0$ and $b=1$ then `MODANDJUMP(`$a,b$`)` decrements `i` by one and jumps to the first line of the program. (If `i` is already equal to $0$ then it tays at $0$.)
  - If $a=1$ and $b=0$ then `MODANDJUMP(`$a,b$`)` jumps to the first line of the program without modifying `i`.
  - If $a=b=0$ then `MODANDJUMP(`$a,b$`)` halts execution of the program.


* Note that since `MODANDJUMP` always either jumps to the first line of the program or halts the computation, the instructions following it will never get executed. Hence in NAND-TM programs the `MODANDJUMP` instruction appears in the last line of the program and nowhere else.

::: {.remark title="Default values and conventions" #defaultvalues}
We also need one more convention to handle "default values". In a Turing machine the tape could contain in addition to $0$ and $1$ (and possibly other values) also the special symbol $\varnothing$ to indicate that this location is "blank".
All our variables, including our arrays, will be Boolean, and so they can contain either the value $0$ or $1$.
However, we can achieve the same effect by adding to every array `Foo` a "companion array" `Foo_nonblank` that encodes this information.

Specifically, for every $i$ and array `Foo`, if the value `Foo[`$i$`]` has not been written to, then it defaults to $0$.
However, we will establish the convention that for every array `Foo` there is a "companion array" `Foo_nonblank` such that  `Foo_nonblank[`$i$`]`$=1$ if the value `Foo[`$i$`]` has been written to.
In particular we will use this convention for the input and output arrays `X` and `Y`. Hence the input corresponds to the values `X[`$0$`]`, $\ldots$, `X[`$n-1$`]` where $n$ is the smallest integer such that `X_nonblank[`$n$`]`$=0$, and the output will be the values `Y[`$0$`]`, $\ldots$, `Y[`$m-1$`]` where $m$ is the smallest integer such that `Y_nonblank[`$m$`]`$=0$. A NAND-TM program gets called with `X` and `X_nonblank` initialized to contain the input, and writes to `Y` and `Y_nonblank` to produce the output.
:::

### Sneak peak: NAND-TM vs Turing machines

As the name implies, NAND-TM programs are a direct implementation of Turing machines in programming language form.
we will show the equivalence below but you can already see how the components of Turing machines and NAND-TM programs correspond to one another:


```table
---
caption: 'Turing Machine and NAND-TM analogs'
alignment: 'LL'
table-width: '1/1'
id: TMvsNANDTMtable
---
**Turing Machine** | **NAND-TM program**
*State:* single register that takes values in $[k]$ | *Scalar variables:* Several variables such as `foo`, `bar` etc.. each taking values in $\{0,1\}$.
*Tape:* One tape containing values in a finite set $\Sigma$. Potentially infinite but $T[t]$ defaults to $\varnothing$ for all locations $t$ that have not been accessed. | *Arrays:* Several arrays such as `Foo`, `Bar` etc.. for each such array `Arr` and index $j$, the value of `Arr` at position $j$ is either $0$ or $1$. The value defaults to $0$ for position that have not been written to.
*Head location:* A number $i\in \mathbb{N}$ that encodes the position of the head. | *Index variable:* The variable `i` that can be used to access the arrays.
*Accessing memory:* At every step the Turing machine has access to its local state, but can only access the tape at the position of the current head location. | *Accessing memory:* At every step a NAND-TM program has access to all the scalar variables, but can only access the arrays at the location `i` of the index variable
*Control of location:* In each step the machine can move the head location by at most one position. | *Control of index variable:* In each iteration of its main loop the program can modify the index `i` by at most one.
```


### Examples

We now present some examples of NAND-TM programs

:::  {.example title="XOR in NAND-TM" #XORENANDPP}
The following is a NAND-TM program to compute the XOR function
on inputs of arbitrary length.
That is $XOR:\{0,1\}^* \rightarrow \{0,1\}$ such that $XOR(x) = \sum_{i=0}^{|x|-1} x_i \mod 2$ for every $x\in \{0,1\}^*$.

```python
temp_0 = NAND(X[0],X[0])
Y_nonblank[0] = NAND(X[0],temp_0)
temp_2 = NAND(X[i],Y[0])
temp_3 = NAND(X[i],temp_2)
temp_4 = NAND(Y[0],temp_2)
Y[0] = NAND(temp_3,temp_4)
MODANDJUMP(X_nonblank[i],X_nonblank[i])
```
:::

::: {.example title="Increment in Enhanced NAND-TM" #INCENANDPP}
We now present enhanced NAND-TM program to compute the _increment function_.
That is, $INC:\{0,1\}^* \rightarrow \{0,1\}^*$ such that for every $x\in \{0,1\}^n$, $INC(x)$ is the $n+1$ bit long string $y$ such that if $X = \sum_{i=0}^{n-1}x_i \cdot 2^i$ is the number represented by $x$, then $y$ is the (least-significant digit first) binary representation of the number $X+1$.

We start by showing the program using the "syntactic sugar" we've seen before of using shorthand for some NAND-CIRC programs we have seen before to compute simple functions such as `IF`, `XOR` and `AND` (as well as the constant `one` function as well as the function `COPY` that just maps a bit to itself).

```python
carry = IF(started,carry,one(started))
started = one(started)
Y[i] = XOR(X[i],carry)
carry = AND(X[i],carry)
Y_nonblank[i] = one(started)
MODANDJUMP(X_nonblank[i],X_nonblank[i])
```

The above is not, strictly speaking, a valid enhanced NAND-TM program.
If we "open up" all of the syntactic sugar, we get the following valid program to compute this syntactic sugar.

```python
temp_0 = NAND(started,started)
temp_1 = NAND(started,temp_0)
temp_2 = NAND(started,started)
temp_3 = NAND(temp_1,temp_2)
temp_4 = NAND(carry,started)
carry = NAND(temp_3,temp_4)
temp_6 = NAND(started,started)
started = NAND(started,temp_6)
temp_8 = NAND(X[i],carry)
temp_9 = NAND(X[i],temp_8)
temp_10 = NAND(carry,temp_8)
Y[i] = NAND(temp_9,temp_10)
temp_12 = NAND(X[i],carry)
carry = NAND(temp_12,temp_12)
temp_14 = NAND(started,started)
Y_nonblank[i] = NAND(started,temp_14)
MODANDJUMP(X_nonblank[i],X_nonblank[i])
```
:::

::: { .pause }
Working out the above two example can go a long way towards understanding the NAND-TM language.
See the appendix and our [GitHub repository](https://github.com/boazbk/tcscode] for a full specification of the NAND-TM language.
:::



## Equivalence of Turing machines and NAND-TM programs

Given the above discussion, it might not be surprising that Turing machines turn out to be equivalent to NAND-TM programs.
Indeed, we designed the NAND-TM language to have this property.
Nevertheless, this is an important result, and the first of many other such equivalence results we will see in this book.

> ### {.theorem title="Turing machines and NAND-TM programs are equivalent" #TM-equiv-thm}
For every $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable by a NAND-TM program $P$ if and only if there is a Turing Machine $M$ that computes $F$.

::: {.proofidea data-ref="TM-equiv-thm"}
To prove such an equivalence theorem, we need to show two directions. We need to be able to __(1)__ transform a Turing machine $M$ to a NAND-TM program $P$ that computes the same function as $P$  and __(2)__ transform a NAND-TM program $P$ into a Turing machine $M$ that computes the same function as $P$.

The idea of the proof is illustrated in [tmvsnandppfig](){.ref}.
To show __(1)__, given a Turing machine $M$, we will create a NAND-TM program $P$ that will have an array `Tape` for the tape of $M$ and scalar (i.e., non array) variable(s) `state` for the state of $M$.
Specifically, since the state of a Turing machine is not in $\{0,1\}$ but rather in a larger set $[k]$, we will use $\ceil{\log k}$ variables `state_`$0$ , $\ldots$, `state_`$\ceil{\log k}-1$ variables to store the representation of the state.
Similarly, to encode the larger alphabet $\Sigma$ of the tape, we will use $\ceil{\log |\Sigma|}$ arrays `Tape_`$0$ , $\ldots$, `Tape_`$\ceil{\log |\Sigma|}-1$, such that the $i^{th}$ location of these arrays encodes the $i^{th}$ symbol in the tape for every tape.
Using the fact that _every_ function can be computed by a NAND-CIRC program, we will be able to compute the transition function of $M$, replacing moving left and right by decrementing and incrementing `i` respectively.

We show __(2)__ using very similar ideas. Given a program $P$ that uses $a$ array variables and $b$ scalar variables, we will create a Turing machine with about $2^b$ states to encode the values of scalar variables, and an alphabet of about $2^a$ so we can encode the arrays using our tape. (The reason the sizes are only "about" $2^a$ and $2^b$ is that we will need to add some symbols and steps for bookkeeping purposes.) The Turing Machine $M$ will simulate each iteration of the program $P$ by updating its state and tape accordingly.
:::

![Comparing a Turing Machine to a NAND-TM program. Both have an unbounded memory component (the _tape_ for a Turing machine, and the _arrays_ for a NAND-TM program), as well as a constant local memory (_state_ for a Turing machine, and _scalar variables_ for a NAND-TM program). Both can only access at each step one location of the unbounded memory, this is the "head" location for a Turing machine, and the value of the index variable `i` for a NAND-TM program.  ](../figure/tmvsnandpp.png){#tmvsnandppfig   }

:::  {.proof data-ref="TM-equiv-thm"}
We start by proving the "if" direction of [TM-equiv-thm](){.ref}. Namely we show that given a Turing machine $M$, we can find a NAND-TM program $P_M$ such that for every input $x$, if $M$ halts on input $x$ with output $y$ then $P_M(x)=y$.
Since our goal is just to show such a program $P_M$ _exists_, we don't need to write out the full code of $P_M$ line by line, and can take advantage of our various "syntactic sugar" in describing it.

The key observation is that by [NAND-univ-thm](){.ref} we can compute _every_ finite function using a NAND-CIRC program.
In particular, consider the transition function  $\delta_M:[k]\times \Sigma \rightarrow [k] \times \Sigma  \times \{\mathsf{L},\mathsf{R} \}$ of our Turing Machine.
We can encode the its components as follows:

* We encode  $[k]$ using $\{0,1\}^\ell$ and  $\Sigma$ using $\{0,1\}^{\ell'}$,  where $\ell = \ceil{\log k}$ and $\ell' = \ceil{\log |\Sigma|}$.

* We encode the set  $\{\mathsf{L},\mathsf{R}, \mathsf{S},\mathsf{H} \}$ using $\{0,1\}^2$. We will choose the encode $\mathsf{L} \mapsto 01$, $\mathsf{R} \mapsto 11$, $\mathsf{S} \mapsto 10$, $\mathsf{H} \mapsto 00$. (This conveniently corresponds to the semantics of the `MODANDJUMP` operation.)


Hence we can identify $\delta_M$ with a function $\overline{M}:\{0,1\}^{\ell+\ell'}  \rightarrow \{0,1\}^{\ell+\ell'+2}$, mapping strings of length $\ell+\ell'$ to strings of length $\ell+\ell'+2$.
By [NAND-univ-thm](){.ref} there exists a finite length NAND-CIRC program `ComputeM` that computes this function $\overline{M}$.
The NAND-TM program to simulate $M$ will essentially be the following:

```python
state, Tape[i], dir0, dir1  = ComputeM(state, Tape[i])
MODANDJUMP(dir0,dir1)
```

where we use `state` as shorthand for the tuple of variables `state_`$0$, $\ldots$, `state_`$\ell-1$ and `Tape[i]` as shorthand for `Tape_`$0$`[i]` ,$\ldots$, `Tape_`$\ell'-1$`[i]`.
(We need to add a little "book keeping" to translate the output and the input from the tape to the `X` and `Y` variables, but the above is basically it.)
Since every step of the main loop of the above program perfectly mimics the computation of the Turing Machine $M$ as `ComputeM` computes the transition of the Turing Machine, and the program carries out exactly the definition of computation by a Turing Machine as per [TM-def](){.ref}.

For the other direction, suppose that $P$ is a NAND-TM program with $s$ lines, $\ell$ scalar variables, and $\ell'$ array variables. We will show that there exists a Turing machine $M_P$ with $2^\ell+C$ states and alphabet $\Sigma$ of size $C' + 2^{\ell'}$ that computes the same functions as $P$ (where $C$, $C'$ are some constants to be determined later).

Specifically, consider the function $\overline{P}:\{0,1\}^\ell \times \{0,1\}^{\ell'} \rightarrow \{0,1\}^\ell \times \{0,1\}^{\ell'}$ that on input the contents of $P$'s scalar variables and the contents of the array variables at location `i` in the beginning of an iteration, outputs all the new values of these variables at the last line of the iteration, right before the `MODANDJUMP` instruction is executed.

If `foo` and `bar` are the two variables that are used as input to the `MODANDJUMP` instruction, then this means that based on the values of these variables we can compute whether `i` will increase, decrease or stay the same, and whether the program will halt or jump back to the beginning.
Hence a Turing machine can simulate an execution of $P$ in one iteration using a finite function applied to its alphabet.
The overall operation of the Turing machine will be as follows:

1. The machine $M_P$ encodes the contents of the array variables of $P$ in its tape, and the contents of the scalar variables in (part of) its state.

2. Initially, the machine $M_P$ will scan the input and copy the result to the parts of the tape corresponding to the `X` and `X_nonblank` variables of $P$. (We use some extra states and alphabet symbols to achieve this.)

3. The machine will $M_P$  then simulates each iterations of $P$ by applying the constant function to update the state and the location of the head, as long as the `loop` variable of $P$ equals $1$.

4. When the loop variable equals $0$, the machine $M_P$ will scan the output arrays and copy them to the beginning of the tape. (Again we can add some states and alphabet symbols to achieve this.)

5. At the end of this scan the machine $M_P$ will enter its halting state.

The above is not a full formal description of a Turing Machine, but our goal is just to show that such a machine exists. One can see that $M_P$ simulates every step of $P$, and hence computes the same function as $P$.
:::


::: {.remark title="Running time equivalence (optional)" #polyequivrem}
If we examine the proof of [TM-equiv-thm](){.ref} then we can see that the every iteration of the loop of a NAND-TM program corresponds to one step in the execution of the Turing machine.
We will come back to this question of measuring number of computation steps later in this course.
For now the main take away point is that NAND-TM programs and Turing Machines are essentially equivalent in power even when taking running time into account.
:::

### Specification vs implementation (again)

Once you understand the definitions of both NAND-TM programs and Turing Machines, [TM-equiv-thm](){.ref} is fairly straightforward.
Indeed, NAND-TM programs are not as much a different model from Turing Machines as they are simply a reformulation of the same model using programming language notation.
You can think of the difference between a Turing machine and a NAND-TM program as the difference between representing a number using decimal or binary notation.
In contrast, the difference between a _function_ $F$ and a Turing machine that computes $F$ is much more profound: it is like the difference between an equation $E$ and a number that is a solution for $E$.
For this reason, while we take special care in distinguishing _functions_ from _programs_ or _machines_, we will often identify the two latter concepts.
We will move freely between describing an algorithm as a Turing machine or as a NAND-TM program (as well as some of the other equivalent computational models we will see in [chapequivalentmodels](){.ref} and beyond).


```table
---
caption: 'Specification vs Implementation formalisms'
alignment: 'LL'
table-width: ''
id: specvsimp
---
*Specification* ; *Implementation*
__Functions__ mapping $\{0,1\}^*$ to $\{0,1\}$ or to $\{0,1\}^*$. ; __Algorithms__, __Turing Machines__, __Programs__
```


## NAND-TM syntactic sugar

Just like we did with NAND-CIRC in [finiteuniversalchap](){.ref}, we can use "syntactic sugar" to make NAND-TM programs easier to write.
For starters, we can use all of the syntactic sugar of NAND-CIRC, and so have access to macro definitions and conditionals (i.e., if/then).
But we can go beyond that and also implement more advanced _looping constructs_ than the simple `MODANDJUMP`.


For staters, we can implement `GOTO`. A `GOTO` statement corresponds to jumping to a certain line in the execution. For example, if we have code of the form

```python
"line1":  do foo
   GOTO("line2")
"line2": do bar
"line3": do blah
```

then the program will only do `foo` and `blah` as when it reaches the line `GOTO("gohere")` it will jump to the line labeled with "gohere".
We can achieve the effect of `GOTO` in NAND-TM using conditionals.
In the code below, we assume that we have variables that can encode strings of finite length (which will be our labels).
Each such variable can be emulated using a constant number of scalar boolean variables.
We also assume that we have access to conditional (i.e., `if` statements), which we can emulate in the same way as NAND.

To emulate a GOTO statement, we will first modify a program P of the form

```python
do foo
do bar
do blah
```

to have the following form (using syntactic sugar for `if` and variables taking finite length string)

```python
pc = "line1"
if (pc=="line1"):
    do foo
    pc = "line2"
if (pc=="line2"):
    do bar
    pc = "line3"
if (pc=="line3"):
    do blah
```

The two programs do the same thing.
The variable `pc` corresponds to the "program counter" and tells the program which line to execute next.
We can see that if we wanted to emulate a `GOTO("line3")` then we could simply modify the instruction `pc = "line2"` to be `pc = "line3"`.

In NAND-CIRC we could only have `GOTO`s that go forward in the code, but since in NAND-TM everything is encompassed within a large outer loop, we can use the same ideas to implement `GOTO`'s that can go backwards, as well as conditional loops.
Using this, we can emulate all the standard loop constructs such as `while`, `do .. until` or `for` in NAND-TM as well.












::: {.remark title="GOTO's in programming languages" #gotorem}
The `GOTO` statement was a staple of most early programming languages, but has largely fallen out of favor and is not included in many modern languages such as _Python_, _Java_,  _Javascript_.
In 1968, Edsger Dijsktra wrote a famous letter titled "[Go to statement considered harmful.](https://goo.gl/bnNsjo)" (see also [xkcdgotofig](){.ref}).
The main trouble with `GOTO` is that it makes analysis of programs more difficult by making it harder to argue about _invariants_ of the program.

When a program contains a loop of the form:

```python
for j in range(100):
    do something

do blah
```


you know that the line of code `do blah` can only be reached if the loop ended, in which case you know that `j` is equal to $100$, and might also be able to argue other properties of the state of the program.
In contrast, if the program might jump to `do blah` from any other point in the code, then it's very hard for you as the programmer to know what you can rely upon in this code.
As Dijkstra said, such invariants are important because _"our intellectual powers are rather geared to master static relations and .. our powers to visualize processes evolving in time are relatively poorly developed"_ and so _"we should ... do ...our utmost best to shorten the conceptual gap between the static program and the dynamic process."_

That said, `GOTO` is still a major part of lower level languages where it is used to implement higher level looping constructs such as `while` and `for` loops.
For example, even though _Java_ doesn't have a `GOTO` statement, the Java Bytecode (which is a lower level representation of Java) does have such a statement.
Similarly, Python bytecode has instructions such as  `POP_JUMP_IF_TRUE` that implement the `GOTO` functionality, and similar instructions are included in many assembly languages.
The way we use `GOTO` to implement a higher level functionality in NAND-TM is reminiscent of the way these various jump instructions are used to implement higher level looping constructs.
:::

![XKCD's take on the `GOTO` statement.](../figure/xkcdgoto.png){#xkcdgotofig .margin  }

### Well formed programs: The NAND-TM style manual

The notion of passing between different variants of programs can be extremely useful, as often, given a program $P$ that we want to analyze, it would be simpler for us to first modify it to an equivalent program $P'$ that has some convenient properties.
You can think of this as the NAND-TM equivalent of enforcing "coding conventions" that are often used for programming languages.
For example, while this is not part of the Python language, Google's  [Python style guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) stipulates that variables that are initialized to a value and never changed (i.e., constants) are typed with all capital letters. (Similar requirements are used in other [style guides](https://www.kernel.org/doc/html/v4.10/process/coding-style.html).)
Of course this does not really restrict the power of Google-conforming Python programs, since every Python program can be transformed to an equivalent one that satisfies this requirement.
In fact, many programming languages have automatic programs known as [linters](https://www.pylint.org/)  that can detect and sometimes modify the program to fit certain standards.

The following solved exercise is an example of that. We will define the notion of a _well-formed program_ and show that every NAND-TM program can be transformed into an equivalent one that is well formed.

::: {.definition title="Well-formed programs" #wellformeddef}
We say that a NAND-TM program $P$ is _well formed_ if it satisfies the following properties:

* Every reference to a variable in $P$ either has the form `foo` or `foo_123` (a _scalar variable:_ alphanumerical string starting with a lowercase letter and no brackets) or the form `Bar[i]` or `Bar_12[i]` (an _array variable_ alphanumerical string starting with a capital letter and ending with `[i]`).

* $P$ contains the scalar variables `zero`, `one`, `dir0`, and `dir1`  such that `zero` and `one` are always the constants $0$ and $1$ respectively, and `MODANDJUMP` is always invoked with the variables `dir0` and `dir1`.

* $P$ contains the array variables `Visited` and `Atstart` and code to ensure that `Atstart[` $i$ `]` equals $1$ if and only if $i=0$, and `Visited[`$i$`]` equals $1$ for all the positions $i$ such that the program finished an iteration with the index variable `i` equalling $i$.
:::

The following exercise shows that we can transform every NAND-TM program $P$ into a well-formed program $P'$ that is equivalent to it. Hence if we are given a NAND-TM program $P$, we can (and will) often assume without loss of generality that it is well-formed.

> ### {.lemma #wellformedlem}
For every   NAND-TM program $P$, there exists an    NAND-TM program $P'$ equivalent to $P$ that is _well formed_ as pre [wellformeddef](){.ref}.
That is, for every input $x\in \{0,1\}^*$, either both $P$ and $P'$ do not halt on $x$, or both $P$ and $P'$ halt on $x$ and produce the same output $y\in \{0,1\}^*$.





::: {.solvedexercise title="Making an NAND-TM program well formed." #wellformedex}
Prove [wellformedlem](){.ref}
:::

::: { .pause }
As usual, I would recommend you try to solve this exercise yourself before looking up the solution.
:::

::: {.solution data-ref="wellformednandpp"}
Since variable identifiers on their own have no meaning in (enhanced) NAND-TM (other than the special ones `X`, `X_nonblank`, `Y`, `Y_nonblank` that already have the desired properties), we can easily achieve the property that scalars variables start with lowercase and arrays with uppercase   using "search and replace".
We just have to take care that we don't make two distinct identifiers become the same.
For example, we can do so by changing all scalar variable identifiers to lower case, and adding to them the prefix `scalar_`, and adding the prefix `Array_` to all array variable identifiers.

The property that an array variable is never references with a numerical index is more challenging.
We need to remove all references to an array variable with an actual numerical index rather than `i`.
One thought might be to simply convert a a reference of the form `Arr[17]` to the scalar variable `arr_17`.
However, this will not necessarily preserve the functionality of the program.
The reason is that we want to ensure that when `i`$=17$ then `Arr[i]` would give us the same value as `arr_17`.

Nevertheless, we can use the approach above with a slight twist. We will demonstrate the solution in a concrete case.(Needless to say, if you needed to solve this question in a problem set or an exam, such a demonstration of a special case would not be sufficient; but this example should be good enough for you to extrapolate a full solution.) Suppose that there are only three references to array variables with numerical indices in the program: `Foo[5]`, `Bar[12]` and `Blah[22]`.
We will include three scalar variables `foo_5`, `bar_12` and `blah_22` which will serve as a _cache_ for the values of these arrays.
We will change all references to `Foo[5]` to `foo_5`, `Bar[12]` to `bar_12` and so on and so forth.
But in addition to that, whenever in the code we refer to `Foo[i]` we will check if `i`$=5$ and if so use the value `foo_5` instead, and similarly with  `Bar[i]`  or `Blah[i]`.

Specifically, we will change our program as follows.
We will create an array `Is_5` such that `Is_5[i]`$=1$ if and only `i`$=5$, and similarly create arrays `Is_12`, `Is_22`.

We can then change code of the following form

```python
Foo[i] = something
```

to

```python
temp = something
foo_5 = IF(Is_5[i],temp,foo_5)
Foo[i] = temp
```

and similarly code of the form

```python
blah = NAND(Bar[i],baz)
```

to

```python
temp = If(Is_22[i],bar_22,Bar[i])
blah = NAND(temp,baz)
```

To create the arrays we can add code of the following form in the beginning of the program (here we're using enhanced NAND-TM syntax, `GOTO`, and the constant `one` but this syntactic sugar can of course be avoided):

```python
# initialization of arrays
GOTO("program body",init_done)
i += one
i += one
i += one
i += one
i += one
Is_5[i] = one
i += one
... # repeat i += one 6 more times
Is_12[i] = one
i += one
... # repeat i += one 9 more times
Is_22[i] = one
i -= one
... # repeat i -= one 21 more times
init_done = one

LABEL("program body")
original code of program..
```

Using `IF` statements (which can easily be replaced with syntactic sugar) we can handle the conditions that `loop`, `Y`, and `Y_nonblank` are not written to once `loop` is set to $0$.
We leave completing all the details as an exercise to the reader (see [standardnoabsoluteindexex](){.ref}).
:::








## Uniformity, and NAND vs NAND-TM (discussion)


While NAND-TM adds extra operations over NAND-CIRC, it is not exactly accurate to say that NAND-TM programs or Turing machines are "more powerful" than NAND-CIRC programs.
NAND-CIRC programs, having no loops, are simply not applicable for computing functions with an bounded number of inputs.
Thus, to compute a function $F:\{0,1\}^* :\rightarrow \{0,1\}^*$ using NAND-CIRC (or equivalently, Boolean circuits) we need a _collection_ of programs/circuits: one for every input length.



The key difference between NAND-CIRC and NAND-TM is that NAND-TM allows us to express the fact that the algorithm for computing parities of length-$100$ strings is really the same one as the algorithm for computing parities of length-$5$ strings (or similarly the fact that the algorithm for adding $n$-bit numbers is the same for every $n$, etc.).
That is, one can think of the NAND-TM program for general parity as the "seed" out of which we can grow NAND-CIRC programs for length $10$, length $100$, or length $1000$ parities as needed.


This notion of a single algorithm that can compute functions of all input lengths is known as _uniformity_ of computation and hence we think of Turing machines / NAND-TM as _uniform_ model of computation, as opposed to Boolean circuits or NAND-CIRC which is a _nonuniform_ model, where we have to specify a different program for every input length.


Looking ahead, we will see that this uniformity leads to another crucial difference between Turing machines and circuits.
Turing machines can have inputs and outputs that are longer than the description of the machine as a string and in particular there exists a Turing machine that can  "self replicate" in the sense that it can print its own code.
This notion of "self replication", and the related notion of "self reference" is crucial to many aspects of computation, as well of course to life itself, whether in the form of digital or biological programs.

For now, what you ought to remember is the following differences between _uniform_ and _non uniform_ computational models:

* __Non uniform computational models:__ Examples are _NAND-CIRC programs_ and _Boolean circuits_. These are models where each individual program/circuit can compute a _finite_ function $f:\{0,1\}^n \rightarrow \{0,1\}^m$. We have seen that _every_ finite function can be computed by _some_ program/circuit.
To discuss computation of an _infinite_ function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ we need to allow a _sequence_ $\{ P_n \}_{n\in \N}$ of programs/circuits (one for every input length), but this does not capture the notion of a _single algorithm_ to compute the function $F$.

* __Uniform computational models:__ Examples are _Turing machines_ and _NAND-TM programs_. These are model where a single program/machine can take inputs of _arbitrary length_ and hence compute an _infinite_ function $F:\{0,1\}^* \rightarrow \{0,1\}^*$.
The number of steps that a program/machine takes on some input is not a priori bounded in advance and in particular there is a chance that it will enter into an _infinite loop_.
Unlike the nonuniform case, we have _not_ shown that every infinite function can be computed by some NAND-TM program/Turing Machine. We will come back to this point in [chapcomputable](){.ref}.



> ### { .recap }
* _Turing machines_ capture the notion of a single algorithm that can evaluate functions of every input length.
* They are equivalent to _NAND-TM programs_, which add loops and arrays to NAND-CIRC.
* Unlike NAND-CIRC or Boolean circuits, the number of steps that a Turing machine takes on a given input is not fixed in advance. In fact, a Turing machine or a NAND-TM program can enter into an _infinite loop_ on certain inputs, and not halt at all.


## Exercises


::: {.exercise title="Explicit NAND TM programming" #majoritynandtm}
Produce the code of a (syntactic-sugar free) NAND-TM program $P$ that computes the (unbounded input length) _Majority_ function $Maj:\{0,1\}^* \rightarrow \{0,1\}$ where for every $x\in \{0,1\}^*$, $Maj(x)=1$ if and only if $\sum_{i=0}^{|x|} x_i > |x|/2$.   We say "produce" rather than "write" because you do not have to write the code of $P$ by hand, but rather can use the programming language of your choice to compute this code.
:::


::: {.exercise}
Prove the following closure properties of the set $\mathbf{R}$ defined in [classRdef](){.ref}:

1. If $F \in \mathbf{R}$ then the function $G(x) = 1 - F(x)$  is in $\mathbf{R}$.

2. If $F,G \in \mathbf{R}$ then the function $H(x) = F(x) \vee G(x)$ is in $\mathbf{R}$.

3. If $F \in \mathbf{R}$ then the function $F^*$  in in $\mathbf{R}$ where $F^*$ is defined as follows: $F^*(x)=1$ iff there exist some strings $w_0,\ldots,w_{k-1}$ such that $x = w_0 w_1 \cdots w_{k-1}$ and $F(w_i)=1$ for every $i\in [k]$.

4. If $F \in \mathbf{R}$ then the function
$$
G(x) = \begin{cases}  \exists_{y \in \{0,1\}^{|x|}} F(xy) = 1 \\
0 & \text{otherwise}
\end{cases}
$$
is in $\mathbf{R}$.
:::




> ### {.exercise title="Single vs multiple bit" #singlebit-ex}
Prove that for every $F:\{0,1\}^* \rightarrow \{0,1\}^*$, the function $F$ is computable if and only if the following function $G:\{0,1\}^* \rightarrow \{0,1\}$ is computable, where $G$ is defined as follows:
$G(x,i,\sigma) = \begin{cases} F(x)_i & i < |F(x)|, \sigma =0 \\ 1 & i < |F(x)|, \sigma = 1 \\ 0 & i \geq |F(x)| \end{cases}$

::: {.exercise title="Uncomputability via counting" #uncomputabilityviacountingex}
Recall that  $\mathbf{R}$ is the set of all total functions from $\{0,1\}^*$ to $\{0,1\}$ that are computable by a Turing machine (see [classRdef](){.ref}). Prove that $\mathbf{R}$ is _countable_.
That is, prove that there exists a one-to-one map $DtN:\mathbf{R} \rightarrow \mathbb{N}$.
You can use the equivalence between Turing machines and NAND-TM programs.
:::


::: {.exercise title="Not every function is computable" #uncountablefuncex}
Prove that the set of _all_ total functions from $\{0,1\}^* \rightarrow \{0,1\}$ is _not_ countable. You can use the results of [cantorsec](){.ref}.
(We will see an _explicit_ uncomputable function in [chapcomputable](){.ref}.)
:::



## Bibliographical notes

Augusta Ada Byron, countess of Lovelace (1815-1852) lived a short but turbulent life, though is today most well known for her collaboration with Charles Babbage
(see [@stein1987ada] for a biography).
Ada took an immense interest in Babbage's _analytical engine_, which we mentioned in [compchap](){.ref}.
In 1842-3, she translated from Italian a paper of Menabrea on the engine,  adding copious notes (longer than the paper itself) including some examples of programs.
Because of these programs, some call Ada "the first computer programmer" though recent evidence shows they were likely written by Babbage himself [@holt2001ada].
Regardless, Ada was clearly one of very few people (perhaps the only one outside of Babbage himself) to fully appreciate how significant and revolutionary the idea of mechanizing computation truly is.


The books of Shetterly [@shetterly2016hidden] and Sobel [@sobel2017the] discuss the history of human computers (which were more often than not women) and their important contributions to scientific discoveries.


Alan Turing was one of the intellectual giants of the 20th century. He was not only the first person to define the notion of computation, but also invented and used some of the world's earliest computational devices as part of the effort to break the _Enigma_ cipher during World War II, saving [millions of lives](https://goo.gl/KY1bJN).
Tragically, Turing committed suicide in 1954, following his conviction in 1952 for homosexual acts and a court-mandated hormonal treatment.
In 2009, British prime minister Gordon Brown made an official public apology to Turing, and in 2013 Queen Elizabeth II granted Turing a posthumous pardon.
Turing's life is the subject of a [great book](https://goo.gl/3GdFdp) and a [mediocre movie](https://goo.gl/EtQvSu).

One of the first programming-language formulations of Turing machines was given by Wang [@Wang1957]. Our formulation is aimed at making the connection with circuits more direct, with the eventual goal of using it for the Cook-Levin Theorem, as well as results such as $\mathbf{P} \subseteq \mathbf{P_{/poly}}$ and  $\mathbf{BPP} \subseteq \mathbf{P_{/poly}}$.
The website [esolangs.org](https://esolangs.org) features a large variety of esoteric Turing-complete programming languages.
One of the most famous of them is [Brainf*ck](https://esolangs.org/wiki/Brainfuck).

In this book, we use the terminology of _functions_ as opposed to _languages_.
These are easily related by identifying a language $L \subseteq \{0,1\}^*$ with its characteristic function $1_L:\{0,1\}^* \rightarrow \{0,1\}$ defined as $1_L(x)=1$ iff $x\in L$.
The characteristic function of a language is always a total function.
The language-like object that corresponds to a _partial function_ is known as a [promise problem](https://goo.gl/sBczFM).
