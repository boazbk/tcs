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
In this lecture we justify this choice by showing that the definition of computable functions will remain the same under a wide variety of computational models.
In fact, a widely believed claim known as the _Church-Turing Thesis_ holds that _every_ "reasonable" definition of computable function is equivalent to ours.
We will discuss the Church-Turing Thesis and the potential definitions of "reasonable" at the end of this lecture.

## RAM machines and NAND<<

One of the limitations of NAND++ (and Turing machines) is that we can only access one location of our arrays/tape at a time.
If currently `i`$=22$ and we want to access `Foo[`$957$`]` then it will take us at least 923 steps to get there.
In contrast, almost every programming language has a formalism for directly accessing memory locations.
Hardware implementations also provide so called _Random Access Memory (RAM)_ which can be thought of as a large array `Mem`, such that given an index $p$ (i.e., memory address, or a _pointer_), we can read from and write to the $p^{th}$ location of `Mem`.

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

* We allow _indirect access_ to arrays. If `foo` is a scalar and `Bar` is an array, then `Bar[foo]` refers to the location of `Bar` indexed by the value of `foo`.

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

1. _Random access of bit arrays:_ NAND<< generalizes NAND++ in two main ways: __(a)__ adding _random access_ to the arrays (ie.., `Foo[bar]` syntax) and __(b)__ moving from _Boolean valued_ variables to _integer valued_ ones. We will start by showing how to handle __(a)__.
Namely, we will show how we can implement in NAND++ the operation `Setindex(Bar)` such that if `Bar` is an array that encodes some integer $j$, then after executing `Setindex(Bar)` the value of `i` will equal to $j$. This will allow us to simulate syntax of the form `Foo[Bar]` by `Setindex(Bar)` followed by `Foo[i]`.

2. _Two dimensional bit arrays:_ We will then show how we can use "syntactiv sugar" to  augment NAND++  with _two dimensional arrays_. That is, have _two indices_ `i` and `j` and _two dimensional arrays_, such that we can use the syntax `Foo[i][j]` to access the (`i`,`j`)-th location of `Foo`

3. _Arrays of integers:_ Finally we will encode a one dimensional array `Arr` of _integers_ by a two dimensional `Arrbin` of _bits_. The idea is simple: if $a_{i,0},\ldots,a_{i,\ell}$ is a binary  (prefix free) representation of `Arr[`$i$`]`, then `Arrbin[`$i$`][`$j$`]` will be equal to $a_{i,j}$.

Once we have arrays of integers, we can use our usual syntactic sugar for functions, `GOTO` etc. to implement the arithmetic  and control flow operations of NAND<<.
:::

We do not show the full formal proof of  [RAMTMequivalencethm](){.ref} but 

::: {.proof data-ref="RAMTMequivalencethm"}

:::



## The "Best of both worlds" paradigm

The equivalence between NAND++ and NAND<< allows us to choose the most convenient language for the task at hand:

* When we want to give a theorem about all programs, we can use NAND++ because it is simpler and easier to analyze. In particular, if we want to show that a certain function _can not_ be computed, then we will use NAND++.

* When we want to show the existence of a program computing a certain function, we can use NAND<<, because it is higher level and easier to program in. In particular, if we want to show that a function _can_ be computed then we can use NAND<<. In fact, because NAND<< has much of  the features of high level programming languages, we will often describe NAND<< programs in an informal manner, trusting that the reader can fill in the details and translate the high level description to the precise program. (This is just like the way people typically use informal or "pseudocode" descriptions of algorithms, trusting that their  audience will know to translate these descriptions to code if needed.)

Our usage of NAND++ and NAND<< is very similar to the way people use in practice  high and low level programming languages.
When one wants to produce a device that executes programs, it is convenient  to do so for very simple and "low level" programming language. When one wants to describe an algorithm, it is convenient to use as high level a formalism as possible.

![By having the two equivalent languages NAND++ and NAND<<, we can "have our cake and eat it too", using NAND++ when we want to prove that programs _can't_ do something, and using NAND<< or other high level languages when we want to prove that programs _can_ do something.](../figure/have_your_cake_and_eat_it_too-img-intro.png){#cakefig .class width=300px height=300px}



> # {.remark title="Recursion in NAND<<" #recursion}
One high level tool we can use in describing NAND<< programs is _recursion_.
We can use the standard implementation of the [stack data structure](https://goo.gl/JweMj), which can be (and in fact is) used to implement recursion.
A _stack_ is a data structure containing a sequence of elements, where we can "push"  elements into it and "pop" them from it in "first in last out" order.
We can implement   `stack` by an array of integers `stack_0`, $\ldots$, `stack_`$\expr{k-1}$ and `stackpointer` will be the number $k$ of items in the stack.
We implement `push(foo)` by doing `i := stackpointer` and `stack_i := foo` and `pop()` by letting `stackpointer := stackpointer - 1`.
By encoding strings as integers, we can have allow strings in our stack as well.
>
Now we can implement recursion using the stack just as is done in most programming languages.
The idea is that  a (recursive or non recursive) call to a function $F$ is implemented by pushing the arguments for $F$ into the stack.
The code of $F$ will "pop" the arguments from the stack, perform the computation (which might involve making recursive or non recursive calls) and then "push" its return value into the stack.
Because of the "first in last out" nature of a stack, we do not return control to the calling procedure until all the recursive calls are done.
>
Specifically,  we note that using loops and conditionals, we can implement "goto" statements in NAND<<.
Moreover, we can even implement "dynamic gotos", in the sense that we can set integer labels for certain lines of codes, and have a `goto foo` operation that moves execution to the line labeled by `foo`.
Now, if we want to make a  call to a function $F$ with parameter `bar` then we will push into the stack the label of the next line and `bar`, and then make a `goto` to the code of $F$. That code will pop its parameter from the stack, do the computation of $F$, and when it needs to resume execution, will pop the label from the stack and `goto` there.
>
You can find  online a tutorial on how recursion is implemented via stack in your favorite programming language, whether it's [Python](http://interactivepython.org/runestone/static/pythonds/Recursion/StackFramesImplementingRecursion.html) , [JavaScript](https://javascript.info/recursion), or [Lisp/Scheme](https://mitpress.mit.edu/sicp/full-text/sicp/book/node110.html).


### Let's talk about abstractions.

At some point in any theory of computation course, the instructor and students need to have _the talk_.
That is, we need to discuss the _level of abstraction_ in describing algorithms.
In algorithms courses, one typically describes  algorithms in English, assuming readers can "fill in the details" and would be able to convert such an algorithm into an implementation if needed.
For example, we might describe the [breadth first search](https://en.wikipedia.org/wiki/Breadth-first_search) algorithm to find if two vertices $u,v$ are connected as follows:

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



### Imperative languages


![A punched card corresponding to a Fortran statement.](../figure/FortranProg.jpg){#fortranfig .class width=300px height=300px}


As we discussed before, any function computed by a standard programming language such as `C`, `Java`, `Python`, `Pascal`, `Fortran` etc. can be computed by a NAND++ program.
Indeed,  a _compiler_ for such languages translates programs into machine languages  that are quite similar to   NAND<< programs or RAM machines.
We can also translate NAND++ programs to such programming languages.
Thus all these programming languages are Turing equivalent.^[Some programming language have hardwired fixed (even if extremely large) bounds on the amount of memory they can access. We ignore such issues in this discussion and assume access to some storage device without a fixed upper bound on its capacity.]

## Lambda calculus and functional programming languages

The [$\lambda$ calculus](https://goo.gl/B9HwT8) is another way to define computable functions.
It was proposed by Alonzo Church in the 1930's around the same time as Alan Turing's proposal of the Turing Machine.
Interestingly, while Turing Machines are not used for practical computation,  the $\lambda$ calculus has inspired functional programming languages such as LISP, ML and Haskell, and so indirectly, the development of many other programming languages as well.


__The $\lambda$ operator.__
At the core of the $\lambda$ calculus  is a way to define "anonymous" functions.
For example, instead of defining the squaring function as

$$
square(x) = x\cdot x
$$

we write it as

$$
\lambda x. x\cdot x
$$

Generally, an expression of the form

$$
\lambda x. e
$$

corresponds to the function that maps any expression $z$ into the expression $e[x \rightarrow z]$ which is obtained by replacing every occurrence of $x$ in $e$ with $z$.^[More accurately, we replace every expression of $x$ that is _bound_ by the $\lambda$ operator. For example, if we have the $\lambda$ expression $\lambda x.(\lambda x. x+1)(x)$ and invoke it on the number $7$ then we get $(\lambda x.x+1)(7)=8$ and not the nonsensical expression $(\lambda 7.7+1)(7)$. To avoid such annoyances, we can always ensure that every instance of $\lambda var.e$ uses a unique variable identifier $var$. See the "logical operators" section in the math background lecture for more discussion on bound variables.]


__Currying.__ The expression $e$ can itself involve $\lambda$, and so for example the function

$$
\lambda x. (\lambda y. x+y)
$$

maps $x$ to the function $y \mapsto x+y$.

In particular, if we invoke this function on $a$ and then invoke the result on $b$ then we get $a+b$.
We can use this approach to achieve the effect of functions with more than one input and so we will use the shorthand $\lambda x,y. e$ for $\lambda x. (\lambda y. e)$.^[This technique of simulating multiple-input functions with single-input functions is known as [Currying](https://en.wikipedia.org/wiki/Currying) and is named after the logician [Haskell Curry](https://goo.gl/C9hKz1). Curry himself attributed this concept to [Moses Schönfinkel](https://goo.gl/qJqd47), though for some reason the term "Schönfinkeling" never caught on..]

![In the "currying" transformation, we can create the effect of a two parameter function $f(x,y)$ with the $\lambda$ expression $\lambda x.(\lambda y. f(x,y))$ which on input $x$ outputs a one-parameter function $f_x$ that has $x$ "hardwired" into it and such that $f_x(y)=f(x,y)$. This can be illustrated by a circuit diagram; see [Chelsea Voss's site](https://tromp.github.io/cl/diagrams.html).](../figure/currying.png){#currying .class width=300px height=300px}

__Precedence and parenthesis.__
The above is a complete description of the $\lambda$ calculus.
However, to avoid clutter, we will allow to drop parenthesis for function invocation, and so if $f$ is a $\lambda$ expression and $z$ is some other expression, then we can write  $fz$ instead of $f(z)$ for the expression corresponding to invoking $f$ on $z$.^[When using  identifiers with multiple letters for $\lambda$ expressions,  we'll separate them with spaces or commas.]
That is, if $f$ has the form $\lambda x.e$ then $fz$ is the same as $f(z)$, which corresponds to the expression $e[x \rightarrow z]$ (i.e., the expression obtained by invoking $f$ on $z$ via replacing all copies of the $x$ parameter with $z$).

We can still use parenthesis for grouping and so $f(gh)$ means invoking $g$ on $h$ and then invoking $f$ on the result, while $(fg)h$ means invoking $f$ on $g$ and then considering the result as a function which then is invoked on $h$.
We will associate from left to right and so identify $fgh$ with $(fg)h$.
For example, if $f = \lambda x.(\lambda y.x+y)$ then $fzw=(fz)w=z+w$.


__Functions as first-class citizens.__
The key property of the $\lambda$ calculus (and functional languages in general) is that functions are "first-class citizens" in the sense that they can be used as parameters and return values of other functions.
Thus, we can invoke one $\lambda$ expression on another.
For example if  $DOUBLE$ is the $\lambda$ expression $\lambda f.(\lambda x. f(fx))$, then for every function $f$, $DOUBLE f$ corresponds to the function that invokes $f$ twice on $x$ (i.e., first computes $fx$ and then invokes $f$ on the result).
In particular, if  $f=\lambda y.(y+1)$ then  $DOUBLE f = \lambda x.(x+2)$.

__(Lack of) types.__ Unlike most programming languages, the pure $\lambda$-calculus doesn't have the notion of _types_.
Every object in the $\lambda$ calculus can also be thought of as a $\lambda$ expression and hence as a function that takes  one input and returns one output.
All functions take one input and return one output, and if you feed a function an input of a form  it didn't expect, it still evaluates the $\lambda$ expression  via "search and replace", replacing all instances of its parameter with copies of the input expression you fed it.


### The "basic" lambda calculus objects

To calculate, it seems we need some basic objects such as $0$ and $1$, and so we will consider the following set of "basic" objects and operations:

* __Boolean constants:__ $0$ and $1$. We  also have the $IF(cond,a,b)$ functions that outputs $a$ if $cond=1$ and $b$ otherwise. Using $IF$ we can also compute logical operations such as $AND,OR,NOT,NAND$ etc.: can you see why?

* __The empty string:__ The value $NIL$ and the function $ISNIL(x)$ that returns $1$ iff $x$ is $NIL$.

* __Strings/lists:__ The function $PAIR(x,y)$ that creates a pair from $x$ and $y$. We will also have the function $HEAD$ and $TAIL$ to extract the first and second member of the pair. We can now create the list $x,y,z$ by $PAIR(x,PAIR(y,PAIR(z,NIL)))$, see [lambdalistfig](){.ref}.  A _string_ is of course simply a list of bits.^[Note that if $L$ is a list, then $HEAD(L)$ is its first element, but $TAIL(L)$ is not the last element but rather all the elements except the first. We use $NIL$ to denote the empty list and hence $PAIR(x,NIL)$ denotes the list with the single element $x$.]



* __List operations:__ The functions $MAP,REDUCE,FILTER$. Given a list $L=(x_0,\ldots,x_{n-1})$ and a function $f$, $MAP(L,f)$ applies $f$ on every member of the list to obtain $L=(f(x_0),\ldots,f(x_{n-1}))$.
The function $FILTER(L,f)$ returns the list of $x_i$'s such that $f(x_i)=1$, and $REDUCE(L,f)$ "combines" the list by  outputting
$$
f(x_0,f(x_1,\cdots f(x_{n-3},f(x_{n-2},f(x_{n-1},NIL))\cdots)
$$
For example $REDUCE(L,+)$ would output the sum of all the elements of the list $L$.
See [reduceetalfig](){.ref} for an illustration of these three operations.



![A list $(x_0,x_1,x_2)$ in the $\lambda$ calculus is constructed from the tail up, building the pair $(x_2,NIL)$, then the pair $(x_1,(x_2,NIL))$ and finally the pair $(x_0,(x_1,(x_2,NIL)))$. That is, a list is a pair where the first element of the pair is the first element of the list and the second element is the rest of the list. The figure on the left renders this "pairs inside pairs" construction, though it is often easier to think of a list as a "chain", as in the figure on the right, where the second element of each pair is thought of as a _link_, _pointer_  or _reference_ to the  remainder of the list.](../figure/lambdalist.png){#lambdalistfig .class width=300px height=300px}

![Illustration of the $MAP$, $FILTER$ and $REDUCE$ operations.](../figure/reducemapfilter.png){#reduceetalfig .class width=300px height=300px}


Together these operations more or less amount to the Lisp/Scheme programming language.^[In Lisp, the $PAIR$, $HEAD$ and $TAIL$ functions are [traditionally called](https://en.wikipedia.org/wiki/CAR_and_CDR) `cons`, `car` and `cdr`.]
Given that, it is perhaps not surprising that we can simulate NAND++ programs using the $\lambda$-calculus plus these basic elements, hence showing the following theorem:

> # {.theorem title="Lambda calculus and NAND++" #lambdaturing-thm}
For every function $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable in the $\lambda$ calculus with the above basic operations if and only if it is computable by a NAND++ program.

> # {.proof data-ref="lambdaturing-thm"}
We only sketch the proof. The "only if" direction is simple. As mentioned above, evaluating $\lambda$ expressions basically amounts to "search and replace". It is also a fairly straightforward programming exercise to implement all the above basic operations in an imperative language such as Python or C, and using the same ideas we can do so in NAND<< as well, which we can then transform to a NAND++ program.
>
For the "if" direction, we start by showing that for every normal-form NAND++ program $P$, we can compute the next-step function $NEXT_P:\{0,1\}^* \rightarrow \{0,1\}^*$ using the above operations.
It turns out not to be so hard.
A configuration  $\sigma$ of $P$ is a string of length $TB$ where $B$ is the (constant sized) block size, and so we can think of it as a list $\sigma=(\sigma^1,\ldots,\sigma^T)$ of $T$ lists of bits, each of length $B$.
There is some constant index  $a\in [B]$ such that the $i$-th block is active if and only if $\sigma^i_a=1$, and similarly there are also indices $s,f$ that tell us if a block is the first or final block.
>
For every index $c$, we can extract from the configuration $\sigma$  the $B$ sized string corresponding to the block $\sigma^i$ where $\sigma^i_c=1$ using a single $REDUCE$ operation.
Therefore, we can extract the first block $\sigma^0$, as well as the active block $\sigma^i$, and using similar ideas we can also extract a constant number of blocks that follow the first blocks ($\sigma^1,\sigma^2,\ldots,\sigma^{c'}$ where $c'$ is the largest numerical index that appears in the program.)^[It's also not hard to modify the program so that the largest numerical index is zero, without changing its functionality]
>
Using the first blocks and active block, we can update the configuration, execute the corresponding line, and also tell if this is an operation where the index `i` stays the same, increases, or decreases.
If it stays the same then we can compute $NEXT_P$ via a $MAP$ operation, using the function that on input $C \in \{0,1\}^B$, keeps $C$ the same if $C_a=0$ (i.e., $C$ is not active) and otherwise updates it to the value in its next step.
If `i` increases, then we can update $\sigma$ by a $REDUCE$ operation, with the function that on input a block $C$ and a list $S$, we output $PAIR(C,S)$ unless $C_a=1$ in which case we output $PAIR(C',PAIR(C'',TAIL(S)))$ where $(C',C'')$ are the new values of the blocks $i$ and $i+1$.
The case for decreasing $i$ is analogous.
>
Once we have a $\lambda$ expression $\varphi$ for computing $NEXT_P$, we can compute the final expression by defining
$$APPLY = \lambda f,\sigma. IF(HALT \sigma,\sigma,f f \varphi \sigma)$$
now for every configuration $\sigma_0$, $APPLY\; APPLY \sigma$ is the final configuration $\sigma_t$ obtained after running the next-step function continuosly.
Indeed, note that if $\sigma_0$ is not halting, then $APPLY\; APPLY \sigma_0$ outputs $APPLY\; APPLY \varphi \sigma_0$ which (since $\varphi$ computes the $NEXT_P$) function is the same as $APPLY \;  APPLY \sigma_1$. By the same reasoning we see that we will eventually get $APPLY\;  APPLY \sigma_t$ where $\sigma_t$ is the halting configuration, but in this case we will get simply the output $\sigma_t$.^[If this looks like recursion then this is not accidental- this is a special case of a general technique for simulating recursive functions in the $\lambda$ calculus. See the discussion on the $Y$ combinator below.]

### How basic is "basic"?

While the collection of "basic" functions we allowed for $\lambda$ calculus is smaller than what's provided by most Lisp dialects, coming from NAND++ it still seems a little "bloated".
Can we make do with less?
In other words, can we find a subset of these basic operations that can implement the rest?




> # { .pause  }
This is a good point to pause and think how you would implement these operations yourself. For example, start by thinking how you could implement $MAP$ using $REDUCE$, and then try to continue and minimize things further, trying to implement $REDUCE$ with from $0,1,IF,PAIR,HEAD,TAIL$ together with the $\lambda$ operations. Remember that your functions can take functions as input and return functions as output.

It turns out that there is in fact a proper subset of these basic operations that can be used to implement the rest.
That subset is the empty set.
That is, we can implement _all_ the operations above using the $\lambda$ formalism only, even without using $0$'s and $1$'s.
It's $\lambda$'s all the way down!
The idea is that we encode $0$ and $1$  themselves as $\lambda$ expressions, and build things up from there.
This notion is known as [Church encoding](https://en.wikipedia.org/wiki/Church_encoding), as was originated by Church in his effort to show that the $\lambda$ calculus can be a basis for all computation.

We now outline how this can be done:

* We define $0$ to be the function that on two inputs $x,y$ outputs $y$, and $1$ to be the function that on two inputs $x,y$ outputs $x$. Of course we use Currying to achieve the effect of two inputs and hence $0 = \lambda x. \lambda y.y$ and $1 = \lambda x.\lambda y.x$.^[We could of course have flipped the definitions of $0$ and $1$, but we use the above because it is the common convention in the $\lambda$ calculus, where people think of $0$ and $1$ as "false" and "true".]

* The above implementation makes the $IF$ function trivial: $IF(cond,a,b)$ is simply $cond \; a\; b$ since $0ab = b$ and $1ab = a$. (We can write $IF = \lambda x.x$ to achieve $IF \; cond \; a \; b = cond \; a \; b$.)

* To encode a pair $(x,y)$ we will produce a function $f_{x,y}$ that has $x$ and $y$ "in its belly" and such that $f_{x,y}g = g x y$ for every function $g$. That is, we write $PAIR = \lambda x,y. \lambda g. gxy$. Note that now we can extract the first element of a pair $p$ by writing $p1$ and the second element by writing $p0$, and so $HEAD = \lambda p. p1$ and $TAIL = \lambda p. p0$.

* We define $NIL$ to be the function that ignores its input and always outputs $1$. That is, $NIL = \lambda x.1$. The $ISNIL$ function checks, given an input $p$, whether we get $1$ if we apply $p$ to the function $0_{x,y}$ that ignores both its inputs and always outputs $0$.
For every valid pair $p0_{x,y} = 0$ while $NIL 0_{x,y}=1$.
Formally, $ISNIL = \lambda p. p (\lambda x,y.0)$.

### List processing and recursion without recursion

Now we come to the big hurdle, which is how to implement $MAP$, $FILTER$, and $REDUCE$ in the $\lambda$ calculus.
It turns out that we can build $MAP$ and $FILTER$ from $REDUCE$.
For example $MAP(L,f)$ is the same as $REDUCE(L,g)$ where $g$ is the operation that on input $x$ and $y$, outputs $PAIR(f(x),NIL)$ if $y$ is NIL and otherwise outputs $PAIR(f(x),y)$.
(I leave checking this as a (recommended!) exercise for you, the reader.)
So, it all boils down to implementing $REDUCE$.
We can define $REDUCE(L,g)$ recursively, by setting $REDUCE(NIL,g)=NIL$ and stipulating that given a non-empty list $L$, which we can think of as a pair $(head,rest)$, $REDUCE(L,g) = g(head, REDUCE(rest,g)))$.
Thus, we might try to write a $\lambda$ expression for $REDUCE$ as follows

$$
REDUCE = \lambda L,g. IF(ISNIL(L),NIL,g HEAD(L) REDUCE(TAIL(L),g)) \label{reducereceq} \;.
$$

The only fly in this ointment is that the $\lambda$ calculus does not have the notion of recursion, and so this is an invalid definition.
This seems like a very serious hurdle: if we don't have loops, and don't have recursion, how are we ever going to be able to compute a function like $REDUCE$?

The idea is to use the "self referential" properties of the $\lambda$ calculus.
Since we are able to work with $\lambda$ expressions, we can possibly inside $REDUCE$ compute a $\lambda$ expression that amounts to running $REDUCE$ itself.
This is very much like the common exercise of a program that prints its own code.
For example, suppose that you have some programming language with an `eval` operation that given a string `code` and an input `x`, evaluates `code` on `x`.
Then, if you have a program $P$ that can print its own code, you can use `eval` as an alternative to recursion: instead of using a recursive call on some input `x`, the program will compute its own code,  store it in some string variable `str` and then use `eval(str,x)`.
You might find this confusing.
_I_ definitely find this confusing.
But hopefully the following will make things a little more concrete.

^[TODO: add a direct example how to implement $REDUCE$ with $XOR$ without using the $Y$ combinator. Hopefully it can be done in a way that makes things more intuitive.]

### The Y combinator

The solution is to think of a recursion  as a sort of "differential equation" on functions.
For example, suppose that all our lists contain either $0$ or $1$ and consider $REDUCE(L,XOR)$ which simply computes the _parity_ of the list elements.
The ideas below will clearly generalize for implementing $REDUCE$ with any other function, and in fact for implementing recursive functions in general.
We can define the parity function $par$ recursively as
$$
par(x_0,\ldots,x_n) = \begin{cases} 0 & |x|=0 \\ x_0 \oplus par(x_1,\ldots,x_n) & \text{otherwise} \end{cases}
\label{eq:par-recurse}
$$
where $\oplus$ denotes the XOR operator.


Our key insight would be to recast [eq:par-recurse](){.eqref} not as a _definition_ of the parity function but rather as an _equation_ on it.
That is, we can think of [eq:par-recurse](){.eqref} as stating that

$$
par = PAREQ(par) \label{eq:pareq}
$$

where $PAREQ$ is a _non-recursive_ function that takes a function $p$ as input, and returns the function $q$ defined as

$$
q(x_0,\ldots,x_n) = \begin{cases} 0 & |x|=0 \\ x_0 \oplus p(x_1,\ldots,x_n) & \text{otherwise} \end{cases}
\label{eq:par-nonrecurse}
$$

In fact, it's not hard to see that satisfying [eq:pareq](){.eqref} is _equivalent_ to satisfying [eq:par-recurse](){.eqref}, and hence $par$ is the _unique_ function that satisfies the condition [eq:pareq](){.eqref}.
This means that to find a function $par$ computing parity, all we need is  a "magical function" $SOLVE$ that given a function $PAREQ$ finds  "fixed point" of $PAREQ$: a function $p$ such that $PAREQ(p) = p$.
Given such a "magical function",  we could give a non-recursive definition for $par$ by writing $par = SOLVE(PAREQ)$.

It turns out that we _can_ find such a "magical function" $SOLVE$ in the $\lambda$ calculus, and this is known as the [Y combinator](https://en.wikipedia.org/wiki/Fixed-point_combinator#Fixed_point_combinators_in_lambda_calculus).

> # {.theorem title="Y combinator" #Ycombinatorthm}
Let
$$
Y = \lambda f. (\lambda x. f (x x)) (\lambda y. f (y y))
$$
then for every $\lambda$ expression $F$, if we let $h=YF$ then $h=Fh$.

> # {.proof data-ref="Ycombinatorthm"}
Indeed, for every $\lambda$ expression $F$ of the form $\lambda t. e$, we can see that
>
$$
YF = (\lambda x. F(x x))(\lambda y. F(y y))
$$
>
But this is the same as applying $F$ to $g g$ where $g=\lambda y. F(y,y)$, or in other words
>
$$
YF = F \left( (\lambda y. F(y,y))(\lambda y. F(y,y)) \right)
$$
>
but by a change of variables the RHS is the same as $F(YF)$.


Using the $Y$ combinator we can implement recursion in the $\lambda$-calculus, and hence loops.
This can be used to complete the "if" direction of [lambdaturing-thm](){.ref}.

For example, to compute parity we first give a recursive definition of parity using the $\lambda$-calculus as

$$
par L = IF(ISNIL(L), 0 , XOR HEAD(L) par(TAIL(L))) \label{eq:par-recurse-lambda}
$$

We then avoid the recursion by converting [eq:par-recurse-lambda](){.eqref} to the operator $PAREQ$ defined as

$$
PAREQ  = \lambda p. \lambda L. IF(ISNIL(L), 0 , XOR HEAD(L) p(TAIL(L)))
$$

and then we can define $par$ as  $Y PAREQ$ since this will be the unique solution to $p= PAREQ p$.


__Infinite loops in $\lambda$-expressions.__
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
Each cell has only two states: "dead" (which we can encode as $0$) or "alive" (which we can encode as $1$).
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
It turns out that even [one dimensional cellular automata](https://en.wikipedia.org/wiki/Rule_110) can be Turing complete, see [onedimautfig](){.ref}.


![A Game-of-Life configuration simulating a Turing Machine. Figure by [Paul Rendell](http://rendell-attic.org/gol/tm.htm).](../figure/turing_gol.jpg){#golfig .class width=300px height=300px}



![Evolution of a one dimensional automata. Each row in the figure corresponds to the configuration. The initial configuration corresponds to the top row and contains only a single "live" cell. This figure corresponds to the "Rule 110" automaton of Stefan Wolfram which is Turing Complete. Figure taken from [Wolfram MathWorld](http://mathworld.wolfram.com/Rule110.html).](../figure/Rule110Big.jpg){#onedimautfig .class width=300px height=300px}



## Our models vs standard texts

We can summarize the models we use versus those used in other texts in the following table:


| Model                        | These notes          | Other texts                             |
|------------------------------|----------------------|-----------------------------------------|
| Nonuniform                   | NAND programs        | Boolean circuits, straightline programs |
| Uniform  (random access)     | NAND<< programs      | RAM machines                            |
| Uniform  (sequential access) | NAND++ programs      | Oblivious one-tape Turing machines      |

    \



Later on in this course we may study _memory bounded_ computation.
It turns out that NAND++ programs with a constant amount of memory are equivalent to the model of _finite automata_ (the adjectives "deterministic" or "nondeterministic" are sometimes added as well, this model is also known as _finite state machines_) which in turns captures the notion of _regular languages_ (those that can be described by [regular expressions](https://en.wikipedia.org/wiki/Regular_expression)).


## The Church-Turing Thesis

We have defined functions to be _computable_ if they can be computed by a NAND++ program, and we've seen that the definition would remain the same if we replaced NAND++ programs by Python programs, Turing machines, $\lambda$ calculus,  cellular automata, and many other computational models.
The _Church-Turing thesis_ is that this is the only sensible definition of "computable" functions.
Unlike the "Physical Extended Church Turing Thesis" (PECTT) which we saw before, the Church Turing thesis does not make a concrete physical prediction that can be experimentally tested, but it certainly motivates predictions such as the PECTT.
One can think of the Church-Turing Thesis as either advocating a definitional choice, making some prediction about all potential computing devices, or suggesting some laws of nature that constrain the natural world.
In Scott Aaronson's words, "whatever it is, the Church-Turing thesis can only be regarded as extremely successful".
No candidate computing device (including quantum computers, and also much less reasonable models such as the hypothetical "closed time curve" computers we mentioned before) has so far mounted a serious challenge to the Church Turing thesis.
These devices might potentially make some computations more _efficient_, but they do not change the difference between what is finitely computable and what is not.^[The _extended_ Church Turing thesis, which we'll discuss later in this course, is that NAND++ programs even capture the limit of what can be _efficiently_ computable. Just like the PECTT, quantum computing presents the main challenge to this thesis.]







## Lecture summary

* While we defined computable functions using NAND++ programs, we could just as well have done so using many other models, including not just NAND<< but also Turing machines, RAM machines, the $\lambda$-calculus and many other models.
* Very simple models turn out to be "Turing complete" in the sense that they can simulate arbitrarily complex computation.


## Exercises

^[TODO: Add an exercise showing that NAND++ programs where the integers are represented using the _unary_ basis are equivalent up to polylog terms with multi-tape Turing machines.]

> # {.exercise title="lambda calculus requires three variables" #lambda-calc-ex}
Prove that for every $\lambda$-expression $e$ with no free variables there is an equivalent $\lambda$-expression $f$ using only the variables $x,y,z$.^[__Hint:__ You can reduce the number of variables a function takes by "pairing them up". That is, define a $\lambda$ expression $PAIR$ such that for every $x,y$ $PAIR xy$ is some function $f$ such that $f0=x$ and $f1=y$. Then use $PAIR$ to iteratively reduce the number of variables used.]


## Bibliographical notes

^[TODO: Recommend Chapter 7 in the nature of computation]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

* Tao has [proposed](https://terrytao.wordpress.com/2014/02/04/finite-time-blowup-for-an-averaged-three-dimensional-navier-stokes-equation/) showing the Turing completeness of fluid dynamics (a "water computer") as a way of settling the question of the behavior of the Navier-Stokes equations, see this [popular article](https://www.quantamagazine.org/terence-tao-proposes-fluid-new-path-in-navier-stokes-problem-20140224/.)


## Acknowledgements
