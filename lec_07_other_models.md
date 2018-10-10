% Other computational models
% Boaz Barak

# Equivalent models of computation { #chapequivalentmodels }

> # { .objectives }
* Learn about RAM machines and $\lambda$ calculus, which are important models of computation.
* See the equivalence between these models and NAND++ programs.
* See how many other models turn out to be "Turing complete"
* Understand the Church-Turing thesis.


>_"All problems in computer science can be solved by another level of indirection"_,  attributed to David Wheeler.

>_"Because we shall later compute with expressions for functions, we need a distinction between functions and forms and a notation for expressing this distinction. This distinction and a notation for describing it, from which we deviate trivially, is given by Church."_,  John McCarthy, 1960 (in paper describing the LISP programming language)

So far we have defined the notion of computing a  function based on the rather esoteric NAND++ programming language.
While we have shown this is equivalent with Turing machines, the latter also don't correspond closely to the way computation is typically done these days.
In this chapter we justify this choice by showing that the definition of computable functions will remain the same under a wide variety of computational models.
In fact, a widely believed claim known as the _Church-Turing Thesis_ holds that _every_ "reasonable" definition of computable function is equivalent to ours.
We will discuss the Church-Turing Thesis and the potential definitions of "reasonable" in [churchturingdiscussionsec](){.ref}.

## RAM machines and NAND<<

One of the limitations of NAND++ (and Turing machines) is that we can only access one location of our arrays/tape at a time.
If currently `i`$=22$ and we want to access `Foo[`$957$`]` then it will take us at least 923 steps to get there.
In contrast, almost every programming language has a formalism for directly accessing memory locations.
Hardware implementations also provide so called _Random Access Memory (RAM)_ which can be thought of as a large array `Mem`, such that given an index $p$ (i.e., memory address, or a _pointer_), we can read from and write to the $p^{th}$ location of `Mem`.^["Random access memory" is quite a misnomer, since it has nothing to do with probability. Alas at this point the term is quite entrenched. Still, we will try to call use the term _indexed_ access instead.]

The computational model that allows access to such a memory is known as a _RAM machine_ (sometimes also known as the _Word RAM model_).
In this model the memory is an array of unbounded size where each cell can store a single _word_, which we think of as a string in $\{0,1\}^w$ and also as a number in $[2^w]$.
The parameter $w$ is known as the _word size_ and is chosen as some function of the input length $n$.
A typical choice is that $w = c\log n$ for some constant $c$.
This is sometimes known as the "transdichotomous RAM model".
In addition to the memory array, the word RAM model also contains a  constant number of _registers_ $r_1,\ldots,r_k$ that also contain a single word.
The operations in this model include loops, arithmetic on registers, and reading and writing from a memory location addressed by the register.

We will use an extension of NAND++ to capture the RAM model.
Specifically, we define the _NAND<< programming language_ as follows:

* The variables are allowed to be (non negative) _integer valued_ rather than only Boolean. That is, a scalar variable `foo` holds an non negative integer in $\N$ (rather than only a bit in $\{0,1\}$), and an array variable `Bar` holds an array of integers.

* We allow _indexed access_ to arrays. If `foo` is a scalar and `Bar` is an array, then `Bar[foo]` refers to the location of `Bar` indexed by the value of `foo`.

* As is often the case in programming language, we will assume that for Boolean operations such as `NAND`, a zero valued integer is considered as _false_, and a nonzero valued integer is considered as _true_.


* In addition to `NAND` we will also allow the basic arithmetic operations of addition, subtraction, multiplication, (integer) division, as well as comparisons (equal, greater than, less than, etc..)

* We will also include as part of the language basic control flow structures such as `if` and `while`

The full description of the NAND<< programing language is in the appendix.^[One restriction mentioned there is that the integer values in a variable always range between $0$ and $T-1$ where $T$ is the number of steps the program took so far. Hence all the arithmetic operations will "truncate" their results so that the output is in this range. This restriction does not make a difference for any of the discussion in this chapter, but will help us make a more accurate accounting of the running time in the future.] However, the most important fact you need to know about it is the following:

> # {.theorem title="NAND++ (TM's) and NAND<< (RAM) are equivalent" #RAMTMequivalencethm}
For every function $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable by a NAND++ program if and only if $F$ is computable by a NAND<< program.


::: {.proofidea data-ref="RAMTMequivalencethm"}
Clearly NAND<< is only more  powerful  than NAND++, and so if a function $F$ is computable by a NAND++ program then it can be computed by a NAND<< program.
The challenging direction is of course to transform a NAND<< program $P$ to an equivalent NAND++ program $Q$.
To describe the proof in full we will need to cover the full formal specification of the NAND<< language, and show how we can implement every one of its features as syntactic sugar on top of NAND++.

This can be done but going over all the operations in detail is rather tedious. Hence we will focus on describing the main ideas behind this transformation.
The transformation has two steps:

1. _Indexed access of bit arrays:_ NAND<< generalizes NAND++ in two main ways: __(a)__ adding _indexed access_ to the arrays (ie.., `Foo[bar]` syntax) and __(b)__ moving from _Boolean valued_ variables to _integer valued_ ones. We will start by showing how to handle __(a)__.
Namely, we will show how we can implement in NAND++ the operation `Setindex(Bar)` such that if `Bar` is an array that encodes some integer $j$, then after executing `Setindex(Bar)` the value of `i` will equal to $j$. This will allow us to simulate syntax of the form `Foo[Bar]` by `Setindex(Bar)` followed by `Foo[i]`.

2. _Two dimensional bit arrays:_ We will then show how we can use "syntactiv sugar" to  augment NAND++  with _two dimensional arrays_. That is, have _two indices_ `i` and `j` and _two dimensional arrays_, such that we can use the syntax `Foo[i][j]` to access the (`i`,`j`)-th location of `Foo`

3. _Arrays of integers:_ Finally we will encode a one dimensional array `Arr` of _integers_ by a two dimensional `Arrbin` of _bits_. The idea is simple: if $a_{i,0},\ldots,a_{i,\ell}$ is a binary  (prefix free) representation of `Arr[`$i$`]`, then `Arrbin[`$i$`][`$j$`]` will be equal to $a_{i,j}$.

Once we have arrays of integers, we can use our usual syntactic sugar for functions, `GOTO` etc. to implement the arithmetic  and control flow operations of NAND<<.
:::

We do not show the full formal proof of  [RAMTMequivalencethm](){.ref} but focus on the most important parts: implementing indexed access, and simulating two dimensional arrays with one dimensional ones.

### Indexed access in NAND++

Let us choose some prefix free representation for the natural numbers (see [prefixfreesec](){.ref}).
For example, if a natural number $k$ is equal to $\sum_{i=0}^{\ell} k_i \cdot 2^i$ for $\ell=\floor{\log k}$, then we can represent it as the string $(k_0,k_0,k_1,k_1,\ldots,k_\ell,k_\ell,1,0)$.


To implement indexed access in NAND++, we need to be able to do the following.
Given an array `Bar`, implement to operation `Setindex(Bar)` that will set `i` to the value encoded by `Bar`.
This can be achieved as follows:

1. Set `i` to zero, by decrementing it until we reach the point where `Atzero[i]`$=1$ (where `Atzero` is an array that has $1$ only in position $0$).

2. Let `Temp` be an array encoding the number $0$.

3. While the number encoded by `Temp` differs from the number encoded by `Bar`:
   a. Increment `Temp`
   b. Set `i += one`

At the end of the loop, `i` is equal to the value at `Bar`, and so we can use this to read or write to arrays at the location corresponding to this value.
In code, we can implement the above operations as follows:

```python
# set i to 0, assume Atzero, one are initialized
LABEL("zero_idx")
i -= one
GOTO("zero_idx",NOT(Atzero[i]))

...

# zero out temp
#(code below assumes a specific prefix-free encoding in which 10 is the "end marker")
Temp[0] = 1
Temp[1] = 0
# set i to Bar, assume we know how to increment, compare
LABEL("increment_temp")
cond = EQUAL(Temp,Bar)
i += cond
INC(Temp)
GOTO("increment_temp",cond)
# if we reach this point, i is number encoded by Bar

...
```

### Two dimensional arrays in NAND++

To implement two dimensional arrays, we embed want to embed them in a one dimensional array.
The idea is that we come up with a _one to one_ function $embed:\N \times \N \rightarrow \N$, and so embed the location $(i,j)$ of the two dimensional array `Two` in the location $embed(i,j)$ of the array `One`.

Since the set $\N \times \N$ seems "much bigger" than the set $\N$, a priori it might not be clear that such a one to one mapping exists. However, once you think about it more, it is not that hard to construct.
For example, you could ask a child to use scissors and glue to transform a 10" by 10" piece of paper into a  1" by 100" strip.
If you think about it, this is essentially  a one to one map from $[10]\times [10]$ to $[10]$. We can generalize this to obtain a one to one map from $[n]\times [n]$ to $[n^2]$ and more generally a one to one map from $\N \times \N$ to $\N$.
Specifically, the following map $embed$ would do (see [pairingfuncfig](){.ref}):

$$embed(x,y) = \tfrac{1}{2}(x+y)(x+y+1)+x\;\;.$$

We ask you to prove that $embed$ is indeed one to one, as well as computable by a NAND++ program, in [pair-ex](){.ref}.

![Illustration of the map $embed(x,y) = \tfrac{1}{2}(x+y)(x+y+1)+x$ for $x,y \in [10]$, one can see that for every distinct pairs $(x,y)$ and $(x',y')$, $embed(x,y) \neq embed(x',y')$. ](../figure/pairing_function.png){#pairingfuncfig .class width=300px height=300px}

So, we can replace code of the form `Two[Foo][Bar] = something` (i.e., access the two dimensional array `Two` at the integers encoded by the one dimensional arrays `Foo` and `Bar`) by code of the form:

```python
Blah = embed(Foo,Bar)
Setindex(Blah)
Two[i] = something
```

Computing `embed` is left for you the reader as [pair-ex](){.ref}, but let us hint that this can be done by simply following the grade-school algorithms for multiplication, addition, and division.

### All the rest

Once we have two dimensional arrays and indexed access, simulating NAND<< with NAND++ is just a matter of implementing the standard algorithms for arithmetic operations and comparators in NAND++.
While this is cumbersome, it is not difficult, and the end result is to show that every NAND<< program $P$ can be simulated by an equivalent NAND++ program $Q$, thus completing the proof of [RAMTMequivalencethm](){.ref}.


### Turing equivalence (discussion)


![A punched card corresponding to a Fortran statement.](../figure/FortranProg.jpg){#fortranfig .class width=300px height=300px}



Any of the  standard programming language such as `C`, `Java`, `Python`, `Pascal`, `Fortran` have very similar operations to NAND<<.
(Indeed, ultimately they can all be executed by machines which have a fixed number of registers and a large memory array.)
Hence using [RAMTMequivalencethm](){.ref}, we can simulate any program in such a programming language by a NAND++  program.
In the other direction, it is a fairly easy programming exercise to write an interpreter for NAND++ in any of the above programming languages.
Hence we can also simulate NAND++ programs (and so by [TM-equiv-thm](){.ref}, Turing machines) using these programming languages.
This property of being equivalent in power to Turing Machines / NAND++ is called _Turing Equivalent_ (or sometimes _Turing Complete_).
Thus all programming languages we are familiar with are Turing equivalent.^[Some programming language have hardwired fixed (even if extremely large) bounds on the amount of memory they can access, which formally prevent them from being applicable to computing infinite functions and hence simulating Turing machines. We ignore such issues in this discussion and assume access to some storage device without a fixed upper bound on its capacity.]

::: {.remark title="Recursion in NAND<< (advanced)" #recursion}
One concept that appears in some of these languages but we did not include in NAND<< programs is _recursion_.
However, recursion (and function calls in general) can be implemented in NAND<< using the  [stack data structure](https://goo.gl/JweMj).
A _stack_ is a data structure containing a sequence of elements, where we can "push"  elements into it and "pop" them from it in "first in last out" order.
We can implement   a stack  by an array of integers `Stack` and a scalar variable `stackpointer` that will be the number  of items in the stack.
We implement `push(foo)` by

```python
Stack[stackpointer]=foo
stackpointer += one
```

and implement `bar = pop()` by

```python
bar = Stack[stackpointer]
stackpointer -= one
```

We implement a function call to $F$ by pushing the arguments for $F$ into the stack.
The code of $F$ will "pop" the arguments from the stack, perform the computation (which might involve making recursive or non recursive calls) and then "push" its return value into the stack.
Because of the "first in last out" nature of a stack, we do not return control to the calling procedure until all the recursive calls are done.

The fact that we can implement recursion using a non recursive language is not surprising.
Indeed, _machine languages_ typically do not have recursion (or function calls in general), and a compiler implements function calls  using a stack and `GOTO`.
You can find  online  tutorials on how recursion is implemented via stack in your favorite programming language, whether it's [Python](http://interactivepython.org/runestone/static/pythonds/Recursion/StackFramesImplementingRecursion.html) , [JavaScript](https://javascript.info/recursion), or [Lisp/Scheme](https://mitpress.mit.edu/sicp/full-text/sicp/book/node110.html).
:::


## The "Best of both worlds" paradigm (discussion)

The equivalence between NAND++ and NAND<< allows us to choose the most convenient language for the task at hand:

* When we want to give a theorem about all programs, we can use NAND++ because it is simpler and easier to analyze. In particular, if we want to show that a certain function _can not_ be computed, then we will use NAND++.

* When we want to show the existence of a program computing a certain function, we can use NAND<<, because it is higher level and easier to program in. In particular, if we want to show that a function _can_ be computed then we can use NAND<<. In fact, because NAND<< has much of  the features of high level programming languages, we will often describe NAND<< programs in an informal manner, trusting that the reader can fill in the details and translate the high level description to the precise program. (This is just like the way people typically use informal or "pseudocode" descriptions of algorithms, trusting that their  audience will know to translate these descriptions to code if needed.)

Our usage of NAND++ and NAND<< is very similar to the way people use in practice  high and low level programming languages.
When one wants to produce a device that executes programs, it is convenient  to do so for very simple and "low level" programming language. When one wants to describe an algorithm, it is convenient to use as high level a formalism as possible.

![By having the two equivalent languages NAND++ and NAND<<, we can "have our cake and eat it too", using NAND++ when we want to prove that programs _can't_ do something, and using NAND<< or other high level languages when we want to prove that programs _can_ do something.](../figure/have_your_cake_and_eat_it_too-img-intro.png){#cakefig .class width=300px height=300px}





### Let's talk about abstractions.

>"The programmer is in the unique position that ... he has to be able to think in terms of conceptual hierarchies that are much deeper than a single mind ever needed to face before.", Edsger Dijkstra, "On the cruelty of really teaching computing science", 1988.


At some point in any theory of computation course, the instructor and students need to have _the talk_.
That is, we need to discuss the _level of abstraction_ in describing algorithms.
In algorithms courses, one typically describes  algorithms in English, assuming readers can "fill in the details" and would be able to convert such an algorithm into an implementation if needed.
For example, we might describe the [breadth first search](https://goo.gl/ug7Jaj) algorithm to find if two vertices $u,v$ are connected as follows:

1. Put $u$ in  queue $Q$.

2. While $Q$ is not empty:
   * Remove the top vertex $w$ from $Q$
   * If $w=v$ then declare "connected" and exit.
   * Mark $w$ and add all unmarked neighbors of $w$ to $Q$.

3. Declare "unconnected".

We call such a description a _high level description_.


If we wanted to give more details on how to implement  breadth first search in a programming language such as Python or C (or NAND<< /  NAND++ for that matter), we would  describe how we implement the queue data structure using an array, and similarly how we would use arrays to implement the marking.
We call such a "intermediate level" description an _implementation level_ or _pseudocode_ description.
Finally, if we want to describe the implementation precisely, we would give the full code of the program (or another fully precise representation, such as in the form of a list of tuples).
We call this a _formal_ or _low level_ description.

![We can describe an algorithm at different levels of granularity/detail and precision. At the highest level we just write the idea in words, omitting all details on representation and implementation. In the intermediate level (also known as _implementation_ or _pseudocode_) we give enough details of the implementation that would allow someone to derive it, though we still fall short of providing the full code. The lowest level is where the actual code or mathematical description is fully spelled out. These different levels of detail all have their uses, and moving between them is one of the most important skills for a computer scientist. ](../figure/levelsofdescription.png){#levelsdescfig .class width=300px height=300px}


While initially we might have described NAND, NAND++, and NAND<< programs at the full formal level (and the [NAND website](http://www.nandpl.org) contains more such examples), as the course continues we will move to implementation and high level description.
After all, our focus is typically not to use these models for actual computation, but rather to analyze the general phenomenon of  computation.
That said, if you don't understand how the high level description translates to an actual implementation, you should always feel welcome to ask for more details of your teachers and teaching fellows.

A similar distinction applies to the notion of _representation_ of objects as strings.
Sometimes, to be precise, we give a _low level specification_ of exactly how an object maps into a binary string.
For example, we might describe an encoding of $n$ vertex graphs as length $n^2$ binary strings, by saying that we map a graph $G$ over the vertex $[n]$ to a string $x\in \{0,1\}^{n^2}$ such that the $n\cdot i + j$-th coordinate of $x$ is $1$ if and only if the edge $\overrightarrow{i \; j}$  is present in $G$.
We can also use an _intermediate_ or _implementation level_ description, by simply saying that we represent a graph using the adjacency matrix representation.


Finally, because we translating between the various representations of graphs (and objects in general) can be done via a NAND<< (and hence a NAND++) program, when talking in a high level we  also suppress discussion of  representation altogether.
For example, the fact that graph connectivity  is a computable function is true regardless of whether we represent graphs as adjacency lists, adjacency matrices, list of edge-pairs, and so on and so forth.
Hence, in cases where the precise representation doesn't make a difference, we would often talk about our algorithms as taking as input an object $O$ (that can be a graph, a vector, a program, etc.) without specifying how $O$ is encoded as a string.




## Lambda calculus and functional programming languages

The [$\lambda$ calculus](https://goo.gl/B9HwT8) is another way to define computable functions.
It was proposed by Alonzo Church in the 1930's around the same time as Alan Turing's proposal of the Turing Machine.
Interestingly, while Turing Machines are not used for practical computation,  the $\lambda$ calculus has inspired functional programming languages such as LISP, ML and Haskell, and  indirectly the development of many other programming languages as well.
In this section we will present the $\lambda$ calculus and show that its power is equivalent to NAND++ programs (and hence also to Turing machines).
An [online appendix](https://github.com/boazbk/nandnotebooks/blob/master/lambda.ipynb) contains a Jupyter notebook with a Python implementation of the $\lambda$ calculus that you can experiment with to get a better feel for this topic.


__The $\lambda$ operator.__
At the core of the $\lambda$ calculus  is a way to define "anonymous" functions.
For example, instead of defining the squaring function as

$$
square(x) = x\times x
$$

we write it as

$$
\lambda x. x\times x
$$

and so $(\lambda x.x\times x)(7)=49$.

::: {.remark title="Dropping parenthesis" #dropparenrem}
To reduce notational clutter, when writing  $\lambda$ calculus expression we often drop the parenthesis for function evaluation. Hence instead of writing $f(x)$ for the result of applying the function $f$ to the input $x$, we can also write this as simply $f\; x$.
Therefore we can write  $((\lambda x.x\times x) 7)=49$. In this chapter, we will use both the $f(x)$ and $f\; x$ notations for function application.
:::

::: {.remark title="Renaming variables." #renamingvars}
Clearly, the name of the argument to a function doesn't matter, and so $\lambda y.y\times y$ is the same as $\lambda x.x \times x$, as both are ways to write the squaring function.
:::

We can also apply functions on functions.
For example, can you guess what number is the following expression equal to?

$$(((\lambda f.(\lambda y.(f \;(f\; y)))) (\lambda x. x\times x))\; 3) \label{lambdaexampleeq}$$

::: { .pause }
The expression [lambdaexampleeq](){.eqref} might seem daunting, but before you look at the solution below, try to break it apart to its components, and evaluate each component at a time.
Working out this example would go a long way toward understanding the $\lambda$ calculus.
:::


::: {.example title="Working out a $\lambda$ expression." #lambda}
To understand better the $\lambda$ calculus. Let's evaluate [lambdaexampleeq](){.eqref}, one step at a time.
As nice as it is for the $\lambda$ calculus to allow us anonymous functions, for complicated expressions adding names can be very helpful for understanding.
So, let us write $F = \lambda f.(\lambda y.(f (f y)))$ and
$g = \lambda x.x\times  x$.

Therefore [lambdaexampleeq](){.eqref} becomes
$$
((F \; g)\;  3) \;.
$$

On input a function $f$, $F$ outputs the function $\lambda y.(f (f\; y))$, which in more standard notation is the mapping $y \mapsto f(f(y))$.
Our function $g$ is simply $g(x)=x^2$ and so $(F g)$ is the function that maps $y$ to $(y^2)^2$ or in other words to $y^4$.
Hence $((F g) 3) = 3^4 = 81$.
:::


::: {.remark title="Obtaining multi-argument functions via Currying." #curryingrem}
The expression $e$ can itself involve $\lambda$, and so for example the function

$$
\lambda x. (\lambda y. x+y)
$$

maps $x$ to the function $y \mapsto x+y$.

In particular, if we invoke this function on $a$ and then invoke the result on $b$ then we get $a+b$.
We can use this approach to achieve the effect of functions with more than one input and so we will use the shorthand $\lambda x,y. e$ for $\lambda x. (\lambda y. e)$.
Similarly, we will use $f(x,y,z)$ as shorthand for $(((f \; x) \; y) \;  z)$ or equivalently (since function application will associate left to right)  $fxyz$.^[This technique of simulating multiple-input functions with single-input functions is known as [Currying](https://en.wikipedia.org/wiki/Currying) and is named after the logician [Haskell Curry](https://goo.gl/C9hKz1). Curry himself attributed this concept to [Moses Schönfinkel](https://goo.gl/qJqd47), though for some reason the term "Schönfinkeling" never caught on..]
:::

![In the "currying" transformation, we can create the effect of a two parameter function $f(x,y)$ with the $\lambda$ expression $\lambda x.(\lambda y. f(x,y))$ which on input $x$ outputs a one-parameter function $f_x$ that has $x$ "hardwired" into it and such that $f_x(y)=f(x,y)$. This can be illustrated by a circuit diagram; see [Chelsea Voss's site](https://tromp.github.io/cl/diagrams.html).](../figure/currying.png){#currying .class width=300px height=300px}


::: {.example title="Simplfying a $\lambda$ expression" #lambdaexptwo}
Here is another example of a $\lambda$ expression:

$$((\lambda x.(\lambda y.x)) \; 2)\; 9) \;. \label{lambdaexptwo}$$

Let us denote $(\lambda y.x)$ by $F$. Then [lambdaexptwo](){.eqref} has the form

$$((\lambda x. F) \; 2) \; 9)$$

Now $(\lambda x.F) 2$ is equal to $F[x \rightarrow 2]$.
Since $F$ is $\lambda y.x$ this means that $(\lambda x.F) 2$ is the function $\lambda y.2$ that ignores its input and outputs $2$ no matter what it is equal to.
Hence [lambdaexptwo](){.eqref}  is equivalent to $(\lambda y. 2) 9$ which is the result of applying the function $y \mapsto 2$ on the input $9$, which is simply the number $2$.
:::

### Formal description of the λ calculus.

In the $\lambda$ calculus we start with  "basic expressions" that contain a single variable such as $x$ or $y$ and build more complex expressions using the following two rules:

* __Application:__ If $exp$ and $exp'$ are $\lambda$ expressions, then the $\lambda$ expression $(exp\; exp')$ corresponds to applying the function described by $exp$ to the input $exp'$.

* __Abstraction:__ If $exp$ is a  $\lambda$ expression and $x$ is a variable, then the $\lambda$ expression $\lambda x.(exp)$  corresponds to the function that on any input $z$ returns the expression $exp[x \rightarrow z]$ replacing all (free) occurrences of $x$ in $exp$.^[Strictly speaking we should replace only the _free_ and not the ones that are _bound_ by some other $\lambda$ operator. For example, if we have the $\lambda$ expression $\lambda x.(\lambda x. x+1)(x)$ and invoke it on the number $7$ then we get $(\lambda x.x+1)(7)=8$ and not the nonsensical expression $(\lambda 7.7+1)(7)$. To avoid such annoyances, we can adopt the convention that every  instance of $\lambda var.e$ uses a unique variable identifier $var$. See  [boundvarsec](){.ref} for more discussion on bound and free variables.]

We can now formally define $\lambda$ expressions:

::: {.definition title="$\lambda$ expression." #lambdaexpdef}
A _$\lambda$ expression_ is either a single variable identifier or an expression that is built from other expressions using the _application_ and _abstraction_ operations.
:::

[lambdaexpdef](){.ref} is a _recursive_ definition. That is, we define the concept of $\lambda$ expression in terms of itself.
This might seem confusing at first, but in fact you have known recursive definitions since you were an elementary school student. Consider how we define an _arithmetic expression_: it is an expression that is either a number, or is built  from other expressions $exp,exp'$ using $(exp + exp')$, $(exp - exp')$, $(exp \times exp')$, or $(exp \div exp')$.


::: {.remark title="Precedence and parenthesis." #precedencerem}
We will use the following rules to allow us to drop some parenthesis. Function application associates from left to right, and so $fgh$ is the same as $(fg)h$.
Function application has a higher precedence than the $\lambda$ operator, and so $\lambda x.fgx$ is the same as $\lambda x.((fg)x)$.

This is similar to how we use the precedence rules in arithmetic operations to allow us to use fewer parenthesis and so write the expression $(7 \times 3) + 2$ as $7\times 3 + 2$.

As mentioned in [curryingrem](){.ref}, we also use the shorthand $\lambda x,y.e$ for $\lambda x.(\lambda y.e)$ and the shorthand $f(x,y)$ for $(f\; x)\; y$. This plays nicely with the "Currying" transformation of simulating multi-input functions using $\lambda$ expressions.
:::



As we have seen in [lambdaexptwo](){.ref}, the  rule that $(\lambda x. exp) exp'$ is equivalent to $exp[x \rightarrow exp']$ enables us to modify $\lambda$ expressions and obtain simpler _equivalent form_ for them.
Another rule that we can use is that the parameter does not matter and hence for example $\lambda y.y$ is the same as $\lambda z.z$.
Together these rules define the notion of _equivalence_ of $\lambda$ expressions:

::: {.definition title="Equivalence of $\lambda$ expressions" #lambdaequivalence}
Two $\lambda$ expressions are _equivalent_ if they can be made into the same expression by repeated applications of the following rules:^[These two rules are commonly known as "$\beta$ reduction" and "$\alpha$ conversion" in the literature on the $\lambda$ calculus.]

1. __Evaluation (aka $\beta$ reduction):__ The expression $(\lambda x.exp) exp'$ is equivalent to $exp[x \rightarrow exp']$.

2. __Variable renaming (aka $\alpha$ conversion):__ The expression $\lambda x.exp$ is equivalent to $\lambda y.exp[x \rightarrow y]$.
:::

If $exp$ is a $\lambda$ expression of the form $\lambda x.exp'$ then it naturally corresponds to the function that maps any input $z$ to $exp'[x \rightarrow z]$.
Hence the $\lambda$ calculus naturally implies a computational model.
Since in the λ calculus the inputs can themselves be functions, we need to fix how we evaluate an expression such as

$$
(\lambda x.f)(\lambda y.g z) \;. \label{lambdaexpeq}
$$
There are two natural conventions for this:


* _Call by name_: We evaluate [lambdaexpeq](){.eqref} by first plugging in the righthand expression $(\lambda y.g z)$ as input to the lefthand side function, obtaining $f[x \rightarrow (\lambda y.g z)]$ and then continue from there.

* _Call by value_: We evaluate [lambdaexpeq](){.eqref} by first evaluating the righthand side and obtaining $h=g[y \rightarrow z]$, and then plugging this into the lefthandside to obtain $f[x \rightarrow h]$.

Because the λ calculus has only _pure_ functions, that do not have "side effects", in many cases the order does not matter. In fact, it can be shown that if we obtain an definite irreducible expression (for example, a number) in both strategies, then it will be the same one.
However, there could be situations where "call by value" goes into an infinite loop while "call by name" does not.
Hence we will use "call by name" henceforth.^["Call by value" is also sometimes known as  _eager evaluation_, since it means we always evaluate parameters to functions before they are executed, while "call by name" is also known as  _lazy evaluation_, since it means that we hold off on evaluating parameters until we are sure we need them. Most programming languages use eager evaluation, though there are some exceptions (notably Haskell). For programming languages that involve non pure functions, call by value has the advantage that it is much easier to understand when the side effects will take place in the program.]



### Functions as first class objects

The key property of the $\lambda$ calculus (and functional languages in general) is that functions are "first-class citizens" in the sense that they can be used as parameters and return values of other functions.
Thus, we can invoke one $\lambda$ expression on another.
For example if  $DOUBLE$ is the $\lambda$ expression $\lambda f.(\lambda x. f(fx))$, then for every function $f$, $DOUBLE\; f$ corresponds to the function that invokes $f$ twice on $x$ (i.e., first computes $fx$ and then invokes $f$ on the result).
In particular, if  $f=\lambda y.(y+1)$ then  $DOUBLE\; f = \lambda x.(x+2)$.

::: {.remark title="(Lack of) types" #untypedrem}
Unlike most programming languages, the pure $\lambda$-calculus doesn't have the notion of _types_.
Every object in the $\lambda$ calculus can also be thought of as a $\lambda$ expression and hence as a function that takes  one input and returns one output.
All functions take one input and return one output, and if you feed a function an input of a form  it didn't expect, it still evaluates the $\lambda$ expression  via "search and replace", replacing all instances of its parameter with copies of the input expression you fed it.
:::

### "Enhanced" lambda calculus

We now discuss the $\lambda$ calculus as a computational model.
As we did with NAND++, we will start by describing an "enhanced" version of the $\lambda$ calculus that contains some "superfluous objects" but is easier to wrap your head around.
We will later show how we can do without many of those concepts, and that the "enhanced $\lambda$ calculus" is equivalent to the "pure $\lambda$ calculus".

The  _enhanced $\lambda$ calculus_ includes the following set of "basic" objects and operations:

* __Boolean constants:__ $0$ and $1$. We  also have the $IF$ function such that $IF cond\;a\;b$  outputs $a$ if $cond=1$ and $b$ otherwise. (We use _currying_ to implement multi-input functions, so $IF cond$ is the function $\lambda a.\lambda b.a$ if $cond=1$ and is the function $\lambda a. \lambda b. b$ if $cond=0$.) Using $IF$ and the constants $0,1$ we can also compute logical operations such as $AND,OR,NOT,NAND$ etc.: can you see why?


* __Strings/lists:__ The function $PAIR$ where $PAIR\; x\; y$ that creates a pair from $x$ and $y$. We will also have the function $HEAD$ and $TAIL$ to extract the first and second member of the pair. We denote by $NIL$ the empty list, and so can create the list $x,y,z$ by $PAIR\; x\; (PAIR\; y\; (PAIR\; z\; NIL))$, see [lambdalistfig](){.ref}.  The function $ISEMPTY$ will return $0$ on any input that was generated by $PAIR$, but will return $1$ on $NIL$. A _string_ is of course simply a list of bits.^[Note that if $L$ is a list, then $HEAD L$ is its first element, but $TAIL L$ is not the last element but rather all the elements except the first. Since $NIL$ denotes the empty list, $PAIR x NIL$ denotes the list with the single element $x$.]



* __List operations:__ The functions $MAP,REDUCE,FILTER$. Given a list $L=(x_0,\ldots,x_{n-1})$ and a function $f$, $MAP L f$ applies $f$ on every member of the list to obtain $L=(f(x_0),\ldots,f(x_{n-1}))$.
The function $FILTER\; L\; f$ returns the list of $x_i$'s such that $f(x_i)=1$, and $REDUCE \; L \; f$ "combines" the list by  outputting
$$
f(x_0,f(x_1,\cdots f(x_{n-3},f(x_{n-2},f(x_{n-1},NIL))\cdots)
$$
For example $REDUCE \; L \; +$ would output the sum of all the elements of the list $L$.
See [reduceetalfig](){.ref} for an illustration of these three operations.

* __Recursion:__  Finally, we want to be able to execute _recursive functions_.  Since in λ calculus functions are _anonymous_, we can't write a definition of the form $f(x) = blah$  where $blah$ includes calls to $f$.
Instead we will construct functions that take an additional function $me$ as a  parameter.
The operator $RECURSE$ will take a function of the form $\lambda me,x.exp$ as input and will return some function $f$ that has the property that $f = \lambda x.exp[me \rightarrow f]$.

::: {.example title="Computing XOR" #xorusingrecursion}
Let us see how we can compute the XOR of a list in the enhanced $\lambda$ calculus.
First, we note that we can compute XOR of two bits as follows:
$$
NOT = \lambda a. IF(a,0,1) \label{lambdanot}
$$
and
$$
XOR_2 = \lambda a,b. IF(b,NOT(a),a) \label{lambdaxor}
$$

(We are using here a bit of syntactic sugar to describe the functions. To obtain the λ expression for XOR we will simply replace the expression  [lambdanot](){.eqref} in [lambdaxor](){.eqref}.)

Now recursively we can define the XOR of a list as follows:

$$
XOR(L) = \begin{cases} 0 & \text{$L$ is empty} \\
XOR_2(HEAD(L),XOR(TAIL(L))) & \text{otherwise}
\end{cases}
$$

This means that  $XOR$ is equal to

$$
RECURSE \;  \bigl(\lambda me,L. IF(ISEMPTY(L),0,XOR_2(HEAD\;L\;\;,\;\;me(TAIL \; L)))\bigr) \;.
$$

That is, $XOR$ is obtained by applying the $RECURSE$ operator to the function that on inputs $me$, $L$, returns $0$ if $ISEMPTY(L)$ and otherwise returns $XOR_2$ applied to $HEAD(L)$ and to $me(TAIL(L))$.
:::

::: {.solvedexercise title="Compute NAND using λ calculus" #NANDlambdaex}
Give a λ expression $N$ such that  $N\;x\;y = NAND(x,y)$ for every $x,y \in \{0,1\}$.
:::

::: {.solution data-ref="NANDlambdaex"}
This can be done in a similar way to how we computed $XOR_2$. The $NAND$ of $x,y$ is equal to $1$ unless $x=y=1$. Hence we can write

$$
N = \lambda x,y.IF(x,IF(y,0,1),1)
$$
:::

![A list $(x_0,x_1,x_2)$ in the $\lambda$ calculus is constructed from the tail up, building the pair $(x_2,NIL)$, then the pair $(x_1,(x_2,NIL))$ and finally the pair $(x_0,(x_1,(x_2,NIL)))$. That is, a list is a pair where the first element of the pair is the first element of the list and the second element is the rest of the list. The figure on the left renders this "pairs inside pairs" construction, though it is often easier to think of a list as a "chain", as in the figure on the right, where the second element of each pair is thought of as a _link_, _pointer_  or _reference_ to the  remainder of the list.](../figure/lambdalist.png){#lambdalistfig .class width=300px height=300px}

![Illustration of the $MAP$, $FILTER$ and $REDUCE$ operations.](../figure/reducemapfilter.png){#reduceetalfig .class width=300px height=300px}

An _enhanced $\lambda$ expression_ is obtained by composing the objects above with the _application_ and _abstraction_ rules.
We can now define the notion of computing a function using the $\lambda$ calculus.
We will define the _simplification_ of a $\lambda$ expression as the following recursive process:

1. _(Evaluation / $\beta$ reduction.)_ If the expression has the form $(exp_L exp_R)$ then replace the expression with $exp'_L[x \rightarrow exp_R]$.

2. _(Renaming / $\alpha$ conversion.)_ When we cannot simplify any further, rename the variables so that the first bound variable in the expression is $v_0$, the second one is $v_1$, and so on and so forth.

::: { .pause }
Please make sure you understand why this recursive procedure simply corresponds to the "call by name" evaluation strategy.
:::

The result of simplifying a $\lambda$ expression  is an equivalent expression, and hence if two expressions have the same simplification then they are equivalent.

:::  {.definition title="Computing a function via $\lambda$ calculus" #lambdacomputedef   }
Let $F:\{0,1\}^* \rightarrow \{0,1\}^*$ be a function and $exp$ a $\lambda$ expression.
For every $x\in \{0,1\}^n$, we  denote by $LIST(x)$ the  $\lambda$ list $PAIR(x_0, PAIR( x_1 , PAIR(\cdots PAIR(x_{n-1} NIL))))$ that corresponds to $x$.

We say that _$exp$ computes $F$_ if for every $x\in \{0,1\}^*$, the expressions $(exp LIST(x))$ and $LIST(F(x))$ are equivalent, and moreover they have the same simplification.
:::


The basic operations of of the enhanced $\lambda$ calculus more or less amount to the Lisp/Scheme programming language.^[In Lisp, the $PAIR$, $HEAD$ and $TAIL$ functions are [traditionally called](https://goo.gl/BLRd6S) `cons`, `car` and `cdr`.]
Given that, it is perhaps not surprising that the  enhanced $\lambda$-calculus is equivalent to NAND++:

> # {.theorem title="Lambda calculus and NAND++" #lambdaturing-thm}
For every function $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable in the enhanced $\lambda$ calculus if and only if it is computable by a NAND++ program.

::: {.proofidea data-ref="lambdaturing-thm"}
To prove the theorem, we need to show that __(1)__ if $F$ is computable by a $\lambda$ calculus expression then it is computable by a NAND++ program, and __(2)__ if $F$ is computable by a NAND++ program, then it is computable by an enhanced $\lambda$ calculus expression.

Showing __(1)__ is fairly straightforward. Applying the simplification rules to a $\lambda$ expression basically amounts to "search and replace" which we can implement easily in, say, NAND<<, or for that matter Python (both of which are equivalent to NAND++ in power).
Showing __(2)__ essentially amounts to writing a NAND++ interpreter in a functional programming language such as LISP  or Scheme. Showing how this can be done is a good exercise in mastering some functional programming techniques that are useful in their own right.
:::




::: {.proof data-ref="lambdaturing-thm"}
We only sketch the proof. The "if" direction is simple. As mentioned above, evaluating $\lambda$ expressions basically amounts to "search and replace". It is also a fairly straightforward programming exercise to implement all the above basic operations in an imperative language such as Python or C, and using the same ideas we can do so in NAND<< as well, which we can then transform to a NAND++ program.

For the "only if" direction, we need to simulate a NAND++ program using a $\lambda$ expression.
First, by [NANDlambdaex](){.ref} we can compute the $NAND$ function, and hence _every_ finite function, using the $\lambda$ calculus.
Thus the main task boils down to simulating the _arrays_ of NAND++ using the _lists_ of the enhanced λ calculus.

We will encode each array `A` of NAND++ program by a list $L$ of the NAND program.
For the index variable `i`, we will have a special list $I$ that has $1$ only in the location corresponding to the value of `i`.
To simulate moving `i` to the left, we need to remove the first item from the list, while to simulate moving `i` to the right, we add a zero to the head of list.^[In fact, it will be convenient for us to make sure all lists are of the same length, and so at the end of each step we will add a sufficient number of zeroes to the end of each list. This can be done with a simple `REDUCE` operation.]

To extract the `i`-th bit of the array corresponding to $L$, we need to compute the following function $get$ that on input a pair of lists $I$ and $L$ of bits of the same length $n$, $get(I,L)$ outputs $1$ if and only if there is some $j \in [n]$ such that the $j$-th element of both $I$ and $L$ is equal to $1$.
This turns out to be not so hard.
The key is to implement the function $zip$ that on input a pair of lists $I$ and $L$ of the same length $n$, outputs a _list of $n$ pairs_ $M$ such that the $j$-th element of $M$ (which we denote by $M_j$) is the pair $(I_j,L_j)$.
Thus $zip$ "zips together" these two lists of elements into a single list of pairs.
It is a good exercise to give a recursive implementation of $zip$, and so can implement it using the $RECURSE$ operator.
Once we have $zip$, we can implement $get$ by applying an appropriate $REDUCE$ on the list $zip(I,L)$.

Setting the list $L$ at the $i$-th location to a certain value requires computing the function $set(I,L,v)$ that outputs a list $L'$ such that $L'_j = L_j$ if $I_j = 0$ and $L'_j  = v$ otherwise. The function $set$ can be implemented by applying $MAP$ with an appropriate operator to the list $zip(I,L)$.

We omit the full details of implementing $set$, $get$, but the bottom line is that for every NAND++ program $P$, we can obtain a λ expression $NEXT_P$ such that, if we let $\sigma = (loop,foo,bar,\ldots,I,X,Xvalid,Y,Yvalid,Baz,Blah,\ldots)$ be the set of Boolean values and lists that encode the current state of $P$ (with a list for each array and for the index variable `i`), then $NEXT_P \sigma$ will encode the state after performing one iteration of $P$.

Now we can use the following "pseudocode" to simulate the program $P$.
The function $SIM_P$ will obtain an encoding $\sigma_0$ of the initial state of $P$, and output the encoding $\sigma^*$ of the state of $P$ after it halts.
It will be computed as follows:

>__Algorithm $SIM_P(\sigma)$:__ \
>
1. Let $\sigma' = NEXT_P \sigma$. \
>
2. If $loop(\sigma') = 0$ then return $\sigma'$. \
>
3. Otherwise return $SIM_P(\sigma')$.

where $loop(\sigma')$ simply denotes extracting the contents of the variable $loop$ from the tuple $\sigma$.
We can write it as the λ expression

$$
RECURSE \; \bigl(\lambda m,\sigma. IF(loop(NEXT_P \sigma)\;,\; m(NEXT_P \sigma)\;,\;NEXT_P \sigma) \bigr)
$$

Given $SIM_P$, we can compute the function computed by $P$ by  writing expressions for encoding the input as the initial state, and decoding the output from the final state.
We omit the details, though this is fairly straightforward.^[For example, if $X$ is a list representing the input, then we can obtain a list $Xvalid$ of $1$'s of the same length by simply writing $Xvalid = MAP(X,\lambda x.1)$.]
:::

### How basic is "basic"?

While the collection of "basic" functions we allowed for $\lambda$ calculus is smaller than what's provided by most Lisp dialects, coming from NAND++ it still seems a little "bloated".
Can we make do with less?
In other words, can we find a subset of these basic operations that can implement the rest?




::: { .pause  }
This is a good point to pause and think how you would implement these operations yourself. For example, start by thinking how you could implement $MAP$ using $REDUCE$, and then $REDUCE$ using $RECURSE$ combined with  $0,1,IF,PAIR,HEAD,TAIL,NIL,ISEMPTY$ together with the $\lambda$ operations.

Now you can think how you could implement $PAIR$, $HEAD$ and $TAIL$ based on $0,1,IF$.
The idea is that we can represent a  _pair_ as _function_.
:::

It turns out that there is in fact a proper subset of these basic operations that can be used to implement the rest.
That subset is the empty set.
That is, we can implement _all_ the operations above using the $\lambda$ formalism only, even without using $0$'s and $1$'s.
It's $\lambda$'s all the way down!
The idea is that we encode $0$ and $1$  themselves as $\lambda$ expressions, and build things up from there.
This notion is known as [Church encoding](https://goo.gl/QZKM9M), as it was originated by Church in his effort to show that the $\lambda$ calculus can be a basis for all computation.

> # {.theorem title="Enhanced λ calculus equivalent to pure λ calculus." #enhancedvanillalambdathm}
There are λ expressions that implement the functions $0$,$1$,$IF$,$PAIR$, $HEAD$, $TAIL$, $NIL$, $ISEMPTY$, $MAP$, $REDUCE$, and $RECURSE$.

We will not write the full formal proof of [enhancedvanillalambdathm](){.ref} but outline  the ideas involved in it:

* We define $0$ to be the function that on two inputs $x,y$ outputs $y$, and $1$ to be the function that on two inputs $x,y$ outputs $x$. Of course we use Currying to achieve the effect of two inputs and hence $0 = \lambda x. \lambda y.y$ and $1 = \lambda x.\lambda y.x$.^[This representation scheme is the common convention but  there are many other alternative representations for $0$ and $1$ that would have worked just as well.]

* The above implementation makes the $IF$ function trivial: $IF(cond,a,b)$ is simply $cond \; a\; b$ since $0ab = b$ and $1ab = a$. We can write $IF = \lambda x.x$ to achieve $IF(cond,a,b) = (((IF cond) a) b) =  cond \; a \; b$.

* To encode a pair $(x,y)$ we will produce a function $f_{x,y}$ that has $x$ and $y$ "in its belly" and such that $f_{x,y}g = g x y$ for every function $g$. That is, we write $PAIR = \lambda x,y. \lambda g. gxy$. Note that now we can extract the first element of a pair $p$ by writing $p1$ and the second element by writing $p0$, and so $HEAD = \lambda p. p1$ and $TAIL = \lambda p. p0$.

* We define $NIL$ to be the function that ignores its input and always outputs $1$. That is, $NIL = \lambda x.1$. The $ISEMPTY$ function checks, given an input $p$, whether we get $1$ if we apply $p$ to the function $z = \lambda x,y.0$ that ignores both its inputs and always outputs $0$.
For every valid pair of the form $p = PAIR x y$, $p z = p x y = 0$ while $NIL z=1$.
Formally, $ISEMPTY = \lambda p. p (\lambda x,y.0)$.

::: {.remark title="Church numerals (optional)" #Churchnumrem}
There is nothing special about Boolean values. You can use similar tricks to implement _natural numbers_ using $\lambda$ terms.
The standard way to do so is to represent the number $n$ by the function $ITER_n$ that on input a function $f$ outputs the function $x \mapsto f(f(\cdots f(x)))$ ($n$ times).
That is, we represent the natural number $1$ as $\lambda f.f$, the number $2$ as $\lambda f.(\lambda x.f(fx))$,
the number $3$ as $\lambda f.(\lambda x.f(f(fx)))$, and so on and so forth. (Note that this is not the same representation we used for $1$ in the Boolean context: this is fine; we already know that the same object can be represented in more than one way.)
The number $0$ is represented by the function that maps any function $f$ to the identity function $\lambda x.x$.
(That is, $0 = \lambda f.(\lambda x.x)$.)

In this representation, we can compute $PLUS(n,m)$ as $\lambda f.\lambda x.(n f)((m f)x)$ and $TIMES(n,m)$ as $\lambda f.n(m f)$. Subtraction and division are trickier, but can be achieved using recursion. (Working this out  is a great exercise.)
:::

### List processing

Now we come to the big hurdle, which is how to implement $MAP$, $FILTER$, and $REDUCE$ in the $\lambda$ calculus.
It turns out that we can build $MAP$ and $FILTER$ from $REDUCE$.
For example $MAP(L,f)$ is the same as $REDUCE(L,g)$ where $g$ is the operation that on input $x$ and $y$, outputs $PAIR(f(x),NIL)$ if $y$ is NIL and otherwise outputs $PAIR(f(x),y)$.
(I leave checking this as a (recommended!) exercise for you, the reader.)
So, it all boils down to implementing $REDUCE$.
We can define $REDUCE(L,g)$ recursively, by setting $REDUCE(NIL,g)=NIL$ and stipulating that given a non-empty list $L$, which we can think of as a pair $(head,rest)$, $REDUCE(L,g) = g(head, REDUCE(rest,g)))$.
Thus, we might try to write a $\lambda$ expression for $REDUCE$ as follows

$$
REDUCE = \lambda L,g. IF(ISEMPTY(L),NIL,g HEAD(L) REDUCE(TAIL(L),g)) \label{reducereceq} \;.
$$

The only fly in this ointment is that the $\lambda$ calculus does not have the notion of recursion, and so this is an invalid definition.
But of course we can use our $RECURSE$ operator to solve this problem. We will replace the recursive call to "$REDUCE$" with a call to a function $me$ that is given as an extra argument, and then apply $RECURSE$ to this.
Thus $REDUCE = RECURSE\;myREDUCE$ where

$$
myREDUCE = \lambda me,L,g. IF(ISEMPTY(L),NIL,g HEAD(L) me(TAIL(L),g)) \label{myreducereceq} \;.
$$

So everything boils down to implementing the $RECURSE$ operator, which we now deal with.


### Recursion without recursion

How can we implement recursion without recursion?
We will illustrate this using a simple example - the $XOR$ function.
As shown in [xorusingrecursion](){.ref}, we  can write the $XOR$ function of a list recursively as follows:

$$
XOR(L) = \begin{cases} 0 & L \text{ is empty} \\ XOR_2(HEAD(L),XOR(TAIL(L))) & \text{otherwise}
\end{cases}
$$

where $XOR_2:\{0,1\}^2 \rightarrow \{0,1\}$ is the XOR on two bits.
In _Python_ we would write this as

```python
def xor2(a,b): return 1-b if a else b
def head(L): return L[0]
def tail(L): return L[1:]

def xor(L): return xor2(head(L),xor(tail(L))) if L else 0

print(xor([0,1,1,0,0,1]))
# 1
```

Now, how could we eliminate this recursive call?
The main idea is that since functions can take other functions as input, it is perfectly legal in Python (and the λ calculus of course) to give a function _itself_ as input.
So, our idea is to try to come up with a _non recursive_ function `tempxor` that takes _two inputs_: a function and a list, and such that `tempxor(tempxor,L)` will output the XOR of `L`!

::: { .pause }
At this point you might want to stop and try to implement this on your own in Python or any other programming language of your choice (as long as it allows functions as inputs).
:::

Our first attempt might be to simply use the idea of replacing the recursive call by `me`.
Let's define this function as `myxor`

```python
def myxor(me,L): return xor2(head(L),me(tail(L))) if L else 0
```

Let's test this out:

```python
myxor(myxor,[1,0,1])
# TypeError: myxor() missing 1 required positional argument
```

The problem is that `myxor` expects _two_ inputs- a function and a list- while in the call to `me` we only provided a list.
To correct this, we modify the call to also provide the function itself:

```python
def tempxor(me,L): return xor2(head(L),me(me,tail(L))) if L else 0

tempxor(tempxor,[1,0,1])
# 0
tempxor(tempxor,[1,0,1,1])
# 1
```

We see this now works! Note the call `me(me,..)` in the definition of `tempxor`: given a function `me` as input, `tempxor` will actually call the function on itself!
Thus we can now define `xor(L)` as simply `return tempxor(tempxor,L)`.

The approach above is not specific to XOR. Given a recursive function `f` that takes an input `x`, we can obtain a non recursive version as follows:

1. Create the function `myf` that takes a pair of  inputs `me` and `x`, and replaces recursive calls to `f` with calls to `me`.
2. Create the function `tempf` that converts  calls  in `myf` of the form `me(x)` to calls of the form `me(me,x)`.
3. The function `f(x)` will be defined as `tempf(tempf,x)`

Here is the way we implement the `RECURSE` operator in Python. It will take a function `myf` as above, and replace it with a function `g` such that `g(x)=myf(g,x)` for every `x`.

```python
def RECURSE(myf):
    def tempf(me,x): return myf(lambda x: me(me,x),x)
    return lambda x: tempf(tempf,x)

xor = RECURSE(myxor)

print(xor([0,1,1,0,0,1]))
# 1

print(xor([1,1,0,0,1,1,1,1]))
# 0
```
__From Python to the  λ calculus.__ In the λ calculus, a two input function $g$ that takes a pair of inputs $me,x$ is written as $\lambda me.(\lambda x. g)$. So the function $x \mapsto me(me,x)$ is simply written as $me\;me$. (Can you see why?)
So in the λ calculus, the function `tempf` will be `f (me me)` and the function `λ x. tempf(tempf,x)` is the same as `tempf tempf`.
So the `RECURSE` operator in the λ calculus is simply the following:

$$
RECURSE =  \lambda f.\bigl( (\lambda m. f(m\; m))\;\; (\lambda m. f(m \;m)) \bigr)
$$

The [online appendix](https://github.com/boazbk/nandnotebooks/blob/master/lambda.ipynb) contains  an implementation of the λ calculus using Python.
Here is an implementation of the recursive  XOR function from that appendix:^[Because of specific issues of Python syntax, in this implementation we use `f * g` for applying `f` to `g` rather than `fg`, and use `λx(exp)` rather than `λx.exp` for abstraction. We also use `_0` and `_1` for the λ terms for $0$ and $1$ so as not to confuse with the Python constants.]

```python
# XOR of two bits
XOR2 = λ(a,b)(IF(a,IF(b,_0,_1),b))

# Recursive XOR with recursive calls replaced by m parameter
myXOR = λ(m,l)(IF(ISEMPTY(l),_0,XOR2(HEAD(l),m(TAIL(l)))))

# Recurse operator (aka Y combinator)
RECURSE = λf((λm(f(m*m)))(λm(f(m*m))))

# XOR function
XOR = RECURSE(myXOR)

#TESTING:

XOR(PAIR(_1,NIL)) # List [1]
# equals 1

XOR(PAIR(_1,PAIR(_0,PAIR(_1,NIL)))) # List [1,0,1]
# equals 0
```


::: {.remark title="The Y combinator" #Ycombinator}
The $RECURSE$ operator above is better known as the
[Y combinator](https://en.wikipedia.org/wiki/Fixed-point_combinator#Fixed_point_combinators_in_lambda_calculus).

It is one of a family of a _fixed point operators_ that given a lambda expression $F$, find a _fixed point_ $f$ of $F$ such that $f = F f$.
If you think about it, $XOR$ is the fixed point of $myXOR$ above.
$XOR$ is the function such that for every $x$, if plug in  $XOR$ as the first argument of $myXOR$ then we get back $XOR$, or in other words $XOR = myXOR\; XOR$.
Hence finding a _fixed point_ for $myXOR$ is the same as applying $RECURSE$ to it.
:::


::: {.remark title="Infinite loops in the λ calculus" #infiniteloops}
The fact that $\lambda$-expressions can simulate NAND++ programs means that, like them, it can also enter into an infinite loop.
For example, consider the $\lambda$ expression

$$
(\lambda x.xxx)(\lambda x.xxx)
$$

If we try to evaluate it  then the first step is to invoke the lefthand function on the righthand one and then obtain

$$
(\lambda x.xxx)(\lambda x.xxx)(\lambda x.xxx)
$$

To evaluate this, the next step would be to apply the second term on the third term,^[This assumes we use the "call by value" evaluation ordering which states that to evaluate a $\lambda$ expression $fg$ we first evaluate  the righthand expression $g$ and then invoke $f$ on it. The "Call by name" or "lazy evaluation" ordering would first evaluate the lefthand expression $f$ and then invoke it on $g$. In this case both strategies would result in an infinite loop. There are examples though when "call by name" would not enter an infinite loop while "call by value" would. The SML and OCaml programming languages use "call by value" while Haskell uses (a close variant of) "call by name".] which would result in

$$
(\lambda x.xxx)(\lambda x.xxx)(\lambda x.xxx)(\lambda x.xxx)
$$

We can see that continuing in this way we get longer and longer expressions, and this process never concludes.
:::



## Other models

There is a great variety of models that are computationally equivalent to Turing machines (and hence to NAND++/NAND<< program).
Chapter 8 of the book [The Nature of Computation](http://nature-of-computation.org/) is a wonderful resource for some of those models.
We briefly mention a few examples.

### Parallel algorithms and cloud computing

The models of computation we considered so far are inherently sequential, but these days much computation happens in parallel, whether using multi-core processors or in massively parallel distributed computation in data centers or over the Internet.
Parallel computing is important in practice, but it does not really make much difference for the question of what can and can't be computed.
After all, if a computation can be performed using $m$ machines in $t$ time, then it can be computed by a single machine in time $mt$.

### Game of life, tiling and cellular automata

Many physical systems can be described as consisting of a large number of elementary components that interact with one another.
One way to model such systems is using _cellular automata_.
This is a system that consists of a large number (or even infinite) cells.
Each cell only has a constant number of possible states.
At each time step, a cell updates to a new  state by applying some  simple rule to the state of itself and its neighbors.


A canonical example of a cellular automaton is [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
In this automata the cells are arranged in an infinite two dimensional grid.
Each cell has only two states: "dead" (which we can encode as $0$ and identify with $\varnothing$) or "alive" (which we can encode as $1$).
The next state of a cell depends on its previous state and the states of its 8 vertical, horizontal and diagonal neighbors.
A dead cell becomes alive only if exactly three of its neighbors are alive.
A live cell continues to live if it has two or three live neighbors.
Even though the number of cells is potentially infinite, we can have a finite encoding for the state by only keeping track of the live cells.
If we initialize the system in a configuration with a finite number of live cells, then the number of live cells will stay finite in all future steps.



We can think of such a system as encoding a computation by starting it in some initial configuration, and then defining some halting condition (e.g., we halt if the cell at position $(0,0)$ becomes dead) and some way to define an output (e.g., we output the state of the cell at position $(1,1)$).
Clearly, given any starting configuration $x$, we can simulate the game of life starting from $x$ using a NAND<< (or NAND++) program, and hence every "Game-of-Life computable" function is computable by a NAND<< program.
Surprisingly, it turns out that the other direction is true as well: as simple as its rules seem, we can simulate a NAND++ program using the game of life (see [golfig](){.ref}).
The [Wikipedia page](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) for the Game of Life contains some beautiful figures and animations of  configurations that produce some very interesting evolutions.
See also the book [The Nature of Computation](http://nature-of-computation.org/).


![A Game-of-Life configuration simulating a Turing Machine. Figure by [Paul Rendell](http://rendell-attic.org/gol/tm.htm).](../figure/turing_gol.jpg){#golfig .class width=300px height=300px}



### Configurations of NAND++/Turing machines and one dimensional cellular automata


It turns out that even [one dimensional cellular automata](https://en.wikipedia.org/wiki/Rule_110) can be Turing complete (see [onedimautfig](){.ref}).
In a _one dimensional automata_, the cells are laid out in one infinitely long line. The next state of each cell is only a function of its past state and the state of both its neighbors.



::: {.definition title="One dimensional cellular automata" #cellautomatadef}
Let $\Sigma$ be a finite set containing the symbol $\varnothing$. A _one dimensional cellular automation_ over alphabet $\Sigma$ is described by a _transition rule_ $r:\Sigma^3 \rightarrow \Sigma$, which satisfies $r(\varnothing,\varnothing,\varnothing) = \varnothing$.

An _configuration_ of the automaton is specified by a string $\alpha \in \Sigma^*$.  We can also think of $\alpha$ as the infinite sequence $(\alpha_0,\alpha_1,\ldots,\alpha_{n-1},\varnothing,\varnothing,\varnothing,\ldots)$, where $n=|\alpha|$.
If $\alpha$ is a configuration and $r$ is a transition rule, then the _next step configuration_, denoted by $\alpha' = NEXT_r(\alpha)$ is defined as follows:
$$alpha'_i = NEXT_r(\alpha_{i-1},\alpha_i,\alpha_{i+1})$$
for $i=0,\ldots,n$.
If $j$ is smaller than $0$ or larger than $n-1$ then we set $\alpha_j = \varnothing$.

In other words, the next state of the automaton $r$ at point $i$ obtained by applying the rule $r$ to the values of $\alpha$ at $i$ and its two neighbors.
:::

::: {.theorem title="One dimensional automata are Turing complete" #onedimcathm}
For every NAND++ program $P$,  there is a one dimension cellular automaton that can simulate $P$ on every input $x$.

Specifically, for every NAND++ program $P$, there is a finite alphabet $\Sigma$ and an automaton $\mathcal{A}$  over this alphabet, as well as an efficient mapping from the inputs to $P$ to starting configurations for  $\mathcal{A}$ and from configurations of $\mathcal{A}$ whose first coordinate has a special form into outputs of $P$.
Namely, there is a computable map $ENCODE:\{0,1\}^* \rightarrow \Sigma^*$ and two special symbols $\sigma_0,\sigma_1 \in \Sigma$, such that for every $x\in \{0,1\}^*$, $P(x)$ halts with input $b\in \{0,1\}$ if and only if the automaton $\mathcal{A}$ initialized with configuration $ENCODE(x)$ eventually reaches a configuration with $\beta_0 = \sigma_b$.
:::

::: { .pause }
The theorem is a little cumbersome to state but try to think how _you_ would formalize the notion of an "automaton simulating a NAND++ program".
:::

::: {.proofidea data-ref="onedimcathm"}
A _configuration_ of $P$ contains its full state at after a particular iteration. That is, the contents of all the array and scalar variables, as well  as the value of the index variable `i`.
We can encode such  a configuration of $P$ as a string $\alpha$ over an alphabet $\Sigma$  of  $2^a + 2^{a+b}$ symbols (where $a$ is the number of array variables  in $P$ and $b$ is the number of scalar variables).
The idea is that in all locations $j$ except  that corresponding to the current value of `i`, we will encode at $\alpha_j$ the values of the array  variables at location $j$. In the location corresponding to `i` we will also include in the encoding the values of all the scalar variables.

Given this notion of an encoding, and the fact that `i` moves only one step  in each iteration, we can see that after one iteration of the program $P$, the configuration largely stays the same except the locations $i,i-1,i+1$ corresponding to the location of the current variable `i` and its immediate neighbors. Once we realize this, we can phrase the progression from one configuration to the next as a one dimensional ceullar automaton!
From this observation, [onedimcathm](){.ref} follows in a fairly straightforward manner.
:::

Before proving [onedimcathm](){.ref}, let us formally define the notion of a _configuration_ of a NAND++ program (see also [nandppconfigfig](){.ref}). We will come back to this notion in later chapters as well.
We restrict attention to so called _well formed_ NAND++ programs (see [wellformeddef](){.ref}), that have a clean separation of array and scalar variables.
Of course, this is not really a restriction since every NAND++ program $P$ can be transformed into an equivalent one that is well formed (see [wellformedlem](){.ref}).

![A _configuration_ of a (well formed) NAND++ program $P$ with $a$ array variables and $b$ scalar variables is a a list  $\alpha$ of strings  in $\{0,1\}^a \cup \{0,1\}^{a+b}$. In exactly one index $i$, $\alpha_i \in \{0,1\}^{a+b}$. This corresponds to the index variable `i` $=i$, and $\alpha_i$ encodes both the contents of the scalar variables, as well as the array variables at the location $i$. For $j\neq i$, $\alpha_j$ encodes the contents of the array variables at the location $j$. The length of the list $\alpha$ denotes the largest index that has been reached so far in the execution of the program. If in one iteration we move from $\alpha$ to $\alpha'$, then for every $j$, $\alpha'_j$ is a function of $\alpha_{j-1},\alpha_j,\alpha_{j+1}$.](../figure/nandppconfiguration2.png){#nandppconfigfig .class width=300px height=300px}

::: { .pause }
[confignandppdef](){.ref} has many technical details, but is not actually deep and complicated.
You would probably understand it better if before starting to read it, you take a moment to stop and think how _you_ would encode as a string the state of a NAND++ program at a given point in an execution.

Think what are all the components that you need to know in order to be able to continue the execution from this point onwards, and what is a simple way to encode them using a list of strings (which in turn can be encoded as a string). In particular, with an eye towards our future applications, try to think of an encoding which will make it as simple as possible to map  a configuration at step $t$ to the configuration at step $t+1$.
:::

::: {.definition title="Configuration of NAND++ programs." #confignandppdef}
Let $P$ be a well-formed NAND++ program (as per [wellformeddef](){.ref}) with $a$ array variables and $b$ scalar variables.
A _configuration_ of $P$ is a list of strings $\alpha = (\alpha_0,\ldots,\alpha_{t-1})$ such that for every $j \in [t]$, $\alpha_j$ is either in $\{0,1\}^a$ or in $\{0,1\}^{a+b}$. Moreover,  there  is exactly a single coordinate $i \in [t]$, such that
$\alpha_i \in \{0,1\}^{a+b}$ and for all other coordinates $j \neq i$,
$\alpha_j \in \{0,1\}^a$.

A configuration $\alpha$ corresponds to the state of $P$ at the
beginning of some iteration as follows:

* The value of the index variable `i` is the index $i$ such that $\alpha_i \in \{0,1\}^{a+b}$.  The value of the $b$ scalar variables is encoded by the last $b$ bits of $\alpha_i$, while the value of the $a$ array variables at the location $i$ is encoded by the first $a$ bits of $\alpha_i$.

* For every $j\neq i$, the value of the $a$ array variables at the location $j$ is encoded by $\alpha_j$.

* The length of $\alpha$ corresponds to the largest position `i` that the program have reached up until this point in the execution. (And so in particular by our convention, the value of all array variables at locations greater or equal to $|\alpha|$ defaults to zero.)

If $\alpha$ is a configuration of $P$, then $\alpha' = NEXT_P(\alpha)$ denotes the configuration of $P$ after completing one iteration.
Note that $\alpha'_j = \alpha_j$ for all $j\not\in \{i-1,i,i+1\}$, and that more generally $\alpha'_j$ is a function of $\alpha_{j-1},\alpha_j,\alpha_{j+1}$.^[Since $P$ is well-formed, we assume it contains an `indexincreasing` variable that can be used to compute whether `i` increases or decreases at the end of an iteration.]
:::

::: {.remark title="Configurations as binary strings" #confencoding}
We can represent  a configuration $(\alpha_0,\ldots,\alpha_{t-1})$ as a  binary string in $\{0,1\}^*$ by concatenating prefix-free encodings of $\alpha_0,\ldots,\alpha_{t-1}$. Specifically we will use a fixed length encoding of $\{0,1\}^a \cup \{0,1\}^{a+b}$ to $\{0,1\}^{a+b+3}$ by padding every string string $\alpha_i$ by concatenating it with  a string of the form $10^k1$ for some $k>0$ to ensure it is of this length. The encoding of $(\alpha_0,\ldots,\alpha_{t-1})$ as a binary string consists of the concatenation of all these fixed-length encodings of $\alpha_0,\ldots,\alpha_{t-1}$.

When we refer to a configuration as a binary string (for example when feeding it as input to other programs) we will assume that this string represents the configuration via the above encoding. Hence we can think of $NEXT_P$ as a function mapping $\{0,1\}^*$ to $\{0,1\}^*$.
Note that this function satisfies that for every string $\sigma \in \{0,1\}^*$ encoding a valid configuration, $NEXT_p(\sigma)$ differs from $\sigma$ in at most $3(a+b+3)$ coordinates which is a constant independent of the length of the input or the number of times the program was executed.
:::

[confignandppdef](){.ref} is a little cumbersome, but ultimately a configuration is simply a string that encodes a _snapshot_ of the state of the NAND++ program at a given point in the execution. (In operating-systems lingo, it would be a  ["core dump"](https://goo.gl/AsccXh).)
Such a snapshot needs to encode the following components:

1. The current value of the index variable `i`.

2. For every scalar variable `foo`, the value of `foo`.

3. For every array variable `Bar`, the value `Bar[`$i$`]` for every $i \in \{0,\ldots, m-1\}$ where $m-1$ is the largest value that the index variable `i` ever achieved in the computation.

The function $NEXT_P$ takes a string $\sigma \in \{0,1\}^*$ that encodes the configuration after $t$ iterations, and maps it to the string $\sigma'$ that encodes the configuration after $t-1$.
The specific details of how we represent configurations and how $NEXT_P$ are not so important as much as the following points:

* $\sigma$ and $\sigma'$ agree with each other in all but a constant number of coordinates.

* Every bit of $\sigma'$ is a function of a constant number of bits of $\sigma$.

Specifically, For every NAND++ program $P$ there is a constant $C>0$ and a finite function $MAP_P:\{0,1\}^{2C} \rightarrow \{0,1, \bot \}$ such that for every $i \in \N$ and string $\sigma$ that encodes a valid configuration of $P$, the $i$-the bit of $NEXT_P(\sigma)$ is obtained by applying the finite function $MAP_P$ to the  $2C$ bits of $\sigma$ corresponding to coordinates $i-C,i-C+1,\ldots,i+C$.^[If one of those is "out of bounds"- corresponds to $\sigma_j$ for $j<0$ or $j \geq |\sigma|$ - then we replace it with $0$. If $i \geq |NEXT_P(\sigma)|$ then we think of the $i$-th bit of $NEXT_P(\sigma)$ as equaling $\bot$.]



::: {.remark title="Configurations of Turing Machines" #tmconfigrem}
The same ideas  can (and often are) used to define configurations of _Turing Machines_. If $M$ is a Turing machine with tape alphabet $\Sigma$ and state space $Q$, then a configuration of $M$ can be encoded as a string $\alpha$ over the alphabet  $\Sigma \cup (\Sigma \times Q)$, such that only a single coordinate (corresponding to the tape's head) is in the larger alphabet $\Sigma \times Q$, and the rest are in $\Sigma$. Once again, such a configuration can also be encoded as a binary string.
The configuration encodes the tape contents, current state, and head location in the natural way.
All of our arguments that use NAND++ configurations can be carried out with Turing machine configurations as well.
:::


::: {.proof data-ref="onedimcathm"}
Assume without loss of generality that  $P$ is a well-formed NAND++ program with $a$ array variables and $b$ scalar variables. (Otherwise we can translate it to such a program.)  Let $\Sigma = \{0,1\}^{a+b+3}$ (a space which, as we saw, is large enough to encode every coordinate of a configuration), and hence think of a configuration as a string in $\sigma \in \Sigma^*$ such that the $i$-th coordinate in $\sigma' = NEXT_P(\sigma)$  only depends on the $i-1$-th, $i$-th, and $i+1$-th coordinate of $\sigma$.
Thus $NEXT_P$ (the function of [confignandppdef](){.ref} that maps a configuration of $P$ into the next one) is in fact a valid rule for a  one dimensional automata. The only thing we have to do is to identify the default value of $\varnothing$ with the value $0^a$ (which corresponds to the index not being in this location and all array variables are set to $0$).


For every input $x$, we can  compute $\alpha(x)$ to be the configuration corresponding to the initial state of $P$ when executed on input $x$.
We can modify the program $P$ so that when it decides to halt, it will first wait until the index variable `i` reaches the $0$ position and also zero out all of its scalar and array variables except for `Y` and `Yvalid`.
Hence the program eventually halts if and only the automaton eventually reaches a configuration $\beta$ in which $\beta_0$ encodes the value of `loop` as $0$, and moreover in this case, we can "read off" the output from $\beta_0$.
:::

The automaton arising from the proof of [onedimcathm](){.ref} has a large alphabet, and furthermore one whose size that depends on the program $P$ that is being simulated. It turns out that one can obtain an automaton with an alphabet of fixed size that is independent of the program being simulated, and in fact the alphabet of the automaton can be  the minimal set $\{0,1\}$! See [onedimautfig](){.ref} for an example of such an Turing-complete automaton.


![Evolution of a one dimensional automata. Each row in the figure corresponds to the configuration. The initial configuration corresponds to the top row and contains only a single "live" cell. This figure corresponds to the "Rule 110" automaton of Stefan Wolfram which is Turing Complete. Figure taken from [Wolfram MathWorld](http://mathworld.wolfram.com/Rule110.html).](../figure/Rule110Big.jpg){#onedimautfig .class width=300px height=300px}


## Turing completeness and equivalence, a formal definition (optional) {#turingcompletesec }

A _computational model_ is some way to define what it means for a _program_ (which is represented by a string) to compute a (partial) _function_.
A _computational model_ $\mathcal{M}$ is _Turing  complete_, if we can map every Turing machine (or equivalently NAND++ program) $Q$ into a program $P$ for $\mathcal{M}$ that computes the same function as $Q$.
It is _Turing equivalent_ if the other direction holds as well (i.e., we can map every program in $\mathcal{M}$ to a Turing machine/NAND++ program that computes the same function).
Formally, we can define this notion as follows:

::: {.definition title="Turing completeness and equivalence" #turingcompletedef}
Let $\mathcal{F}$ be the set of all partial functions from $\{0,1\}^*$ to $\{0,1\}^*$. A _computational model_ is a map $\mathcal{M}:\{0,1\}^* \rightarrow \mathcal{F}$.
We say that a program $P$ in the model $\mathcal{M}$ _computes_ a function $F\in \mathcal{F}$ if $\mathcal{M}(P) = F$.

A computational model $\mathcal{M}$ is _Turing complete_ if there is a computable map $ENCODE_M:\{0,1\}^* \rightarrow \{0,1\}^*$ for every NAND++ program $P$ (represented as a string),  $\mathcal{M}(ENCODE_M(P))$ is equal to the partial function computed by $P$.^[We could have equally well made this definition using Turing machines, NAND<<, $\lambda$ calculus, and many other models.]
A computational model $\mathcal{M}$ is _Turing equivalent_ if it is Turing complete and there exists a computable map $DECODE_M:\{0,1\}^* \rightarrow \{0,1\}^*$ such that or every string $Q\in \{0,1\}^*$,  $P=ENCODE_M(Q)$ is a string representation of a NAND++ program that  computes the function $\mathcal{M}(Q)$.
:::

Some examples of Turing Equivalent models include:

* Turing machines
* NAND++ programs
* NAND<< programs
* $\lambda$ calculus
* Game of life (mapping programs and inputs/outputs to starting and ending configurations)
* Programming languages such as Python/C/Javascript/OCaml... (allowing for unbounded storage)


## The Church-Turing Thesis (discussion) {#churchturingdiscussionsec }


>_"[In 1934], Church had been speculating, and finally definitely proposed, that the $\lambda$-definable functions are all the effectively calculable functions .... When Church proposed this thesis, I sat down to disprove it ... but, quickly realizing that [my approach failed], I became overnight a supporter of the thesis."_, Stephen Kleene, 1979.

>_"[The thesis is] not so much  a definition or to an axiom but ... a natural law."_, Emil Post, 1936.

We have defined functions to be _computable_ if they can be computed by a NAND++ program, and we've seen that the definition would remain the same if we replaced NAND++ programs by Python programs, Turing machines, $\lambda$ calculus,  cellular automata, and many other computational models.
The _Church-Turing thesis_ is that this is the only sensible definition of "computable" functions.
Unlike the "Physical Extended Church Turing Thesis" (PECTT) which we saw before, the Church Turing thesis does not make a concrete physical prediction that can be experimentally tested, but it certainly motivates predictions such as the PECTT.
One can think of the Church-Turing Thesis as either advocating a definitional choice, making some prediction about all potential computing devices, or suggesting some laws of nature that constrain the natural world.
In Scott Aaronson's words, "whatever it is, the Church-Turing thesis can only be regarded as extremely successful".
No candidate computing device (including quantum computers, and also much less reasonable models such as the hypothetical "closed time curve" computers we mentioned before) has so far mounted a serious challenge to the Church Turing thesis.
These devices might potentially make some computations more _efficient_, but they do not change the difference between what is finitely computable and what is not.^[The _extended_ Church Turing thesis, which we'll discuss later in this course, is that NAND++ programs even capture the limit of what can be _efficiently_ computable. Just like the PECTT, quantum computing presents the main challenge to this thesis.]






## Our models vs other texts

We can summarize the models we use versus those used in other texts in the following table:


| Model                        | These notes          | Other texts                             |
|------------------------------|----------------------|-----------------------------------------|
| Nonuniform                   | NAND programs        | Boolean circuits, straightline programs |
| Uniform  (random access)     | NAND<< programs      | RAM machines                            |
| Uniform  (sequential access) | NAND++ programs      | Oblivious one-tape Turing machines      |

    \



Later on in this course we may study _memory bounded_ computation.
It turns out that NAND++ programs with a constant amount of memory are equivalent to the model of _finite automata_ (the adjectives "deterministic" or "nondeterministic" are sometimes added as well, this model is also known as _finite state machines_) which in turns captures the notion of _regular languages_ (those that can be described by [regular expressions](https://en.wikipedia.org/wiki/Regular_expression)).





> # { .recap }
* While we defined computable functions using NAND++ programs, we could just as well have done so using many other models, including not just NAND<< but also Turing machines, RAM machines, the $\lambda$-calculus and many other models.
* Very simple models turn out to be "Turing complete" in the sense that they can simulate arbitrarily complex computation.


## Exercises

::: {.remark title="Disclaimer" #disclaimerrem}
Most of the exercises have been written in the summer of 2018 and haven't yet been fully debugged. While I would prefer people do not post online solutions to the exercises, I would greatly appreciate if you let me know of any bugs. You can do so by posting a [GitHub issue](https://github.com/boazbk/tcs/issues) about the exercise, and optionally complement this with an email to me with more details about the attempted solution.
:::

^[TODO: Add an exercise showing that NAND++ programs where the integers are represented using the _unary_ basis are equivalent up to polylog terms with multi-tape Turing machines.]

::: {.exercise title="Pairing" #pair-ex}
Let $embed:\N^2 \rightarrow \N$ be the function defined as $embed(x_0,x_1)= \tfrac{1}{2}(x_0+x_1)(x_0+x_1+1) + x_1$. \

1. Prove that for every $x^0,x^1 \in \N$, $embed(x^0,x^1)$ is indeed a natural number. \

2. Prove that $embed$ is one-to-one \

3. Construct a NAND++ program $P$ such that for every $x^0,x^1 \in \N$, $P(pf(x^0)pf(x^1))=pf(embed(x^0,x^1))$, where $pf$ is the prefix-free encoding map defined above. You can use the syntactic sugar for inner loops, conditionals, and incrementing/decrementing the counter. \

4. Construct NAND++ programs $P_0,P_1$ such that for for every $x^0,x^1 \in \N$ and $i \in N$, $P_i(pf(embed(x^0,x^1)))=pf(x^i)$. You can use the syntactic sugar for inner loops, conditionals, and incrementing/decrementing the counter.

:::

> # {.exercise title="lambda calculus requires three variables" #lambda-calc-ex}
Prove that for every $\lambda$-expression $e$ with no free variables there is an equivalent $\lambda$-expression $f$ using only the variables $x,y,z$.^[__Hint:__ You can reduce the number of variables a function takes by "pairing them up". That is, define a $\lambda$ expression $PAIR$ such that for every $x,y$ $PAIR xy$ is some function $f$ such that $f0=x$ and $f1=y$. Then use $PAIR$ to iteratively reduce the number of variables used.]


## Bibliographical notes

^[TODO: Recommend Chapter 7 in the nature of computation]

## Further explorations

Some topics related to this chapter that might be accessible to advanced students include:

* Tao has [proposed](https://terrytao.wordpress.com/2014/02/04/finite-time-blowup-for-an-averaged-three-dimensional-navier-stokes-equation/) showing the Turing completeness of fluid dynamics (a "water computer") as a way of settling the question of the behavior of the Navier-Stokes equations, see this [popular article](https://www.quantamagazine.org/terence-tao-proposes-fluid-new-path-in-navier-stokes-problem-20140224/.)


## Acknowledgements
