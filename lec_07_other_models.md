# Equivalent models of computation



>_"Computing is normally done by writing certain symbols on paper. We may suppose that this paper is divided into squares like a child's arithmetic book.. The behavior of the \[human\] computer at any moment is determined by the symbols which he is observing, and of his 'state of mind' at that moment... We may suppose that in a simple operation not more than one symbol is altered."_, \
>_"We compare a man in the process of computing ... to a machine which is only capable of a finite number of configurations... The machine is supplied with a 'tape' (the analogue of paper) ... divided into sections (called 'squares') each capable of bearing a 'symbol' "_, Alan Turing, 1936

We have defined the notion of computing a  function based on the rather esoteric NAND++ programming language.
In this lecture we justify this choice by showing that the definition of computable functions will remain the same under a wide variety of computational models.
In fact, a widely believed claim known as the _Church-Turing Thesis_ holds that _every_ "reasonable" definition of computable function will be equivalent to ours.
We will discuss the Church-Turing Thesis and the potential definitions of "reasonable" at the end of this lecture.

## Turing machines

The "granddaddy" of all models of computation is the _Turing Machine_, which is the standard  model of computation in most textbook.^[This definitional choice does not make much difference since, as we will show, NAND++/NAND<< programs are equivalent to Turing machines in their computing power.]
Turing machines were defined in 1936 by Alan Turing in an attempt to formally capture all the functions that can be computed by human "computers" that follow a well-defined set of rules, such as the standard algorithms for addition or multiplication.

![Until the advent of electronic computers, the word "computer" was used to describe a person, often female, that performed calculations. These human computers were absolutely essential to many achievements including mapping the stars, breaking the Engima cipher, and the NASA space mission. Two recent books about  these "computers" and their important contributions are [The Glass Universe](https://www.amazon.com/Glass-Universe-Harvard-Observatory-Measure-ebook/dp/B01CZCW45O) (from which this photo is taken) and [Hidden Figures](https://www.amazon.com/Hidden-Figures-American-Untold-Mathematicians/dp/006236359X).](../figure/HumanComputers.jpg){#figureid .class width=300px height=300px}

Turing thought of such a person as having access to as much "scratch paper" as they need.
For simplicity we can think of this scratch paper as a one dimensional piece of graph paper (commonly known as "work tape"), where in each box of this paper we can write  a single symbol.
At any point in time, the person can read and write a single box of the paper, and based on the contents can update his/her finite mental  state, and/or move to the box immediately to the left or right.

Thus, Turing thought of modeling such computation by a "machine" that maintains one of $k$ states, and at each point can read and write a single symbol from some alphabet $\Sigma$ (containing $\{0,1\}$) from its "work tape".
To perform computation using this machine, we write the input $x\in \{0,1\}^n$ on the tape, and the goal of the machine is to ensure that at the end of the computation, the value $F(x)$ will be written there.


Specifically, a computation of a Turing Machine $M$ with $k$ states and alphabet $\Sigma$ on input $x\in \{0,1\}^*$ proceeds as  follows:

* Initially the machine is at state $0$ (known as the "starting state") and the tape is initialized to $\triangleright,x_0,\ldots,x_{n-1},\varnothing,\varnothing,\ldots$.^[We use the symbol $\triangleright$ to denote the beginning of the tape, and the symbol $\varnothing$ to denote an empty cell. Hence we will assume that $\Sigma$ contains these symbols, along with $0$ and $1$.]
* The location $i$ to which the machine points to is set to $0$.
* At each step, the machine reads the symbol $\sigma = T[i]$ that is in the $i^{th}$ location of the tape, and based on this symbol and its state $s$ decides on:
    * What symbol $\sigma'$ to write on the tape \
    * Whether to move **L**eft (i.e., $i \leftarrow i-1$) or **R**ight  (i.e., $i \leftarrow i+1$) \
    * What is going to be the new state $s \in [k]$
* When the machine reaches the state $s=k-1$ (known as the "halting state") then it halts. The output of the machine is obtained by reading off the tape from location $1$ onwards, stopping at the first point where the symbol is not $0$ or $1$.


![A Turing machine has access to an _tape_ of unbounded length. At each point in the execution, the machine can read/write a single symbol of the tape, and based on that decide whether to move left, right or halt.](../figure/turing_machine.png){#turing-machine-fig .class width=300px height=300px}

^[TODO: update figure to $\{0,\ldots,k-1\}$.]


The formal definition of Turing machines is as follows:

> # {.definition title="Turing Machine" #TM-def}
A (one tape) _Turing machine_ with $k$ states and alphabet $\Sigma \supseteq \{0,1, \triangleright, \varnothing \}$ is a function
$M:[k]\times \Sigma \rightarrow \Sigma \times [k] \times \{ L , R \}$.
We say that the Turing machine $M$ _computes_ a (partial) function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ if for every $x\in\bits^*$ on which $F$ is defined, the result of the following process is $F(x)$:
>
* Initialize the array $T$ of symbols in $\Sigma$ as follows: $T[0] = \triangleright$, $T[i]=x_i$ for $i=1,\ldots,|x|$
>
* Let $s=1$ and $i=0$ and repeat the following while $s\neq k-1$: \
  >a. Let $\sigma = T[i]$. If $T[i]$ is not defined then let $\sigma = \varnothing$ \
  >b. Let $(s',\sigma',D) = M(s,\sigma)$ \
  >c. Modify $T[i]$ to equal $\sigma'$ \
  >d. If $D=L$ and $i>0$ then set $i \leftarrow i-1$. If $D=R$ then set $i \leftarrow i+1$. \
  >e. Set $s \leftarrow s'$ \
>
* Let $n$ be the first index larger than $0$ such that $T[i] \not\in \{0,1\}$. We define the output of the process to be $T[1],\ldots,T[n-1]$. The number of steps that the Turing Machine $M$ takes on input $x$ is the number of times that the while loop above  is executed. (If the process never stops then we say that the machine did not halt on $x$.)

## Turing Machines and NAND++ programs

As mentioned, Turing machines turn out to be equivalent to NAND++ programs:

> # {.theorem title="Turing machines and NAND++ programs" #TM-equiv-thm}
For every $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable by a NAND++ program if and only if there is a Turing Machine $M$ that computes $F$.


### Simulating Turing machines with NAND++ programs

We now prove the "if" direction of [TM-equiv-thm](){.ref}, namely we show that given a Turing machine $M$, we can find a NAND++ program $P_M$ such that for every input $x$, if $M$ halts on input $x$ with output $y$ then $P_M(x)=y$.
Because NAND<< and NAND++ are equivalent in power, it is sufficient to construct a NAND<< program that has this property.
Moreover, we can take advantage of  the syntactic sugar transformations we have seen before for NAND<<, including conditionals, loops, and function calls.


If $M:[k]\times \Sigma \rightarrow \Sigma \times [k] \times \{ L , R \}$ then there is a finite length NAND program `ComputeM` that computes the finite function $M$ (representing the finite sets $[k]$,$\Sigma$, $\{L,R\}$ appropriately by bits).
The NAND<< program simulating $M$ will be the following:

~~~~ { .go .numberLines }
// tape is an array with the alphabet Sigma
// we use ">" for the start-tape marker and "." for the empty cell
// in the syntactic sugar below, we assume some binary encoding of the alphabet.
tape_0 := ">"
k := 0
while (validx_j) { // copy input to tape
    tape_j := x_k
    k++
    j++
}
tape_j := "<"
state := 0
head  := 0 // location of the head
while NOT EQUAL(state,k-1) { // not ending state
   state', dir := ComputeM(tape_head,state)
   if EQUAL(dir,`L`) AND NOT(EQUAL(tape_head,">")) {
       head--
   }
   if EQUAL(dir,'R') {
       head++
   }
   state' := state
}

// copy output to y variables
j := 1
s := 0
while EQUAL(tape_j,0) OR EQUAL(tape_j,1) {
   y_s := tape_j
   j++
   s++
}
~~~~

In addition to the standard syntactic sugar, we assumed above we can make function calls to the function `EQUAL` that checks equality of two symbols as well as the finite function `ComputeM`  that corresponds to the transition function of the Turing machine.


### Simulating NAND++ programs with Turing machines

We now show the other direction of [TM-equiv-thm](){.ref}.
Namely, we show that given a NAND++ program $P$, we can come up with a Turing machine $M$ that computes the same function.
First of all, we will assume that $P$ has a variable `idxdecreasing` which will equal to $1$ if in the next step `i` will decrease and to $0$ otherwise.
We have seen before that we can use the "breadcrumbs" technique to ensure that the program has this property.

If $P$ has $t$ variables then the alphabet of $M$ will have, in addition to the standard elements of $0,1,\triangleright,\varnothing$ also the $2^t$ symbols $\{0,1\}^t$.
The convention will be that the $j^{th}$ location of $M$'s tape will store using one "megasymbol" in $\{0,1\}^t$ the values of `var_`$\expr{j-1}$ for all the variables `var` of $P$.
If the program $P$ has $s$ lines and  contains  $\ell$ references to variables without indices or variables with literal numeric indices such as `foo_5` or `bar_17` in the program, then we will set the number of states of $M$ to be $(2+s)\cdot 2^\ell$.
Hence the state of $M$ can encode the current line that $P$ is executing, and the value of all the variables that are not indexed by `i`, while the value of the variables indexed by `i` can be read from the tape.
Using this, we can easily simulate an execution of the program $P$ using a Turing machine $M$.
We will update the internal state of $M$ based on the actions of $P$ and update  the location of the head (with an increase corresponding to a right move and a decrease corresponding to a left move) based on the value of the variable `idxdecreasing`.


### Advanced note: polynomial equivalence

If we examine the proof of [TM-equiv-thm](){.ref} then we can see  that the equivalence between NAND++ programs and NAND<< programs is up to polynomial overhead in the number of steps. That is, for every NAND++ program $P$, there is a Turing machine $M$ and a constant $c$ such that for every $x\in \{0,1\}^*$, if on input $x$, $P$ halts within $T$ steps and outputs $y$, then on the same input $x$, $M$ halts within  $c\cdot T^c$ steps with the same output $y$.
Similarly, for every Turing machine $M$, there is a NAND++ program $P$ and a constant $d$ such that for every $x\in \{0,1\}^*$, if on input $x$, $M$ halts within $T$ steps and outputs $y$, then on the same input $x$, $P$ outputs within $d\cdot T^d$ steps with the same output $y$.^[TODO: check if the overhead is really what I say it is.]


## "Turing Completeness" and other  Computational models

A computational model $M$ is _Turing complete_ if  every partial function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ that is computable by a Turing Machine is also computable in $M$.
A model is _Turing equivalent_ if the other direction holds as well; that is, for every partial function $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable by a Turing machine if and only if it is computable in $M$.
Another way to state [TM-equiv-thm](){.ref} is that NAND++ is Turing equivalent.
Since we can simulate any NAND<< program by a NAND++ program (and vice versa), NAND<< is Turing equivalent as well.
It turns out that there are many other Turing-equivalent models of computation.
We now discuss a few examples.



### RAM Machines

The _Word RAM model_ is a computational model that is arguably more similar to real-world computers than Turing machines or NAND++ programs.
In this model the memory is an array of unbounded size where each cell can store a single _word_, which we think of as a string in $\{0,1\}^w$ and also as a number in $[2^w]$.
The parameter $w$ is known as the _word size_ and is chosen as some function of the input length $n$.
A typical choice is that $w = c\log n$ for some constant $c$.
This is sometimes known as the "transdichotomous RAM model".
In this model there are a constant number of _registers_ $r_1,\ldots,r_k$ that also contain a single word.
The operations in this model include loops, arithmetic on registers, and reading and writing from a memory location addressed by the register.
See [this lecture](http://people.seas.harvard.edu/~cs125/fall14/lec6.pdf) for a more precise definition of this model.

We will not show all the details but it is not hard to show that the word RAM model is equivalent to NAND<< programs.
Every NAND<< program can be easily simulated by a RAM machine as long as $w$ is larger than the logarithm of its running time.
In the other direction, a NAND<< program can simulate a RAM machine, using its variables as the registers.
The only significant difference between NAND<< and the word-RAM model is that in NAND<<, since we have a constant number of variables, we can think of our memory as an array where in each location there are only $t=O(1)$ bits stored (one bit for each distinct unindexed variable identifier used in the program). Thus we will need a factor of $O(w)$  multiplicative overheard to simulate the word-RAM model with an array storing $w$-length words.

### Imperative languages


![A punched card corresponding to a Fortran statement.](../figure/FortranProg.jpg){#fortranfig .class width=300px height=300px}


As we discussed before, any function computed by a standard programming language such as `C`, `Java`, `Python`, `Pascal`, `Fortran` etc.. can be computed by a NAND++ program.
Indeed,  a _compiler_ for such languages translates programs into machine languages  that are quite similar to   NAND<< programs or RAM machines.
We can also translate NAND++ programs to such programming languages.
Thus all these programming languages are Turing equivalent.^[Some programming language have hardwired fixed (even if extremely large) bounds on the amount of memory they can access. We ignore such issues in this discussion and assume access to some storage device without a fixed upper bound on its capacity.]

## Lambda calculus and functional programming languages

The [$\lambda$ calculus](https://en.wikipedia.org/wiki/Lambda_calculus) is another way to define computable functions.
It was proposed by Alonzo Church in the 1930's around the same time as Alan Turing's proposal of the Turing Machine.
Interestingly, while Turing Machines are not used for practical computation,  the $\lambda$ calculus has inspired functional programming languages such as LISP, ML and Haskell, and so indirectly, the development of many other programming languages as well.


__The $\lambda$ operator.__
At the core of the $\lambda$ calculus  is a way to define "anonymous" functions that are not given a name.
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

corresponds to the function that maps any expression $z$ into the expression $e[x \rightarrow z]$ which is obtained by replacing every occurrence of $x$ in $e$ with $z$.^[More accurately, we replace every expression of $x$ that is _bounded_ by the $\lambda$ operator. For example, if we have the $\lambda$ expression $\lambda x.(\lambda x. x+1)(x)$ and invoke it on the number $7$ then we get $(\lambda x.x+1)(7)=8$ and not the nonsensical expression $(\lambda 7.7+1)(7)$. To avoid such annoyances, we can always ensure that every instance of $\lambda var.e$ uses a unique variable identifier $var$.]


__Currying.__ The expression $e$ can itself involve $\lambda$, and so for example the function

$$
\lambda x. (\lambda y. x+y)
$$

maps $x$ to the function $y \mapsto x+y$.

In particular, if we invoke this function on $a$ and then invoke the result on $b$ then we get $a+b$.
We can use this approach,
to achieve the effect of functions with more than one input and so we will use the shorthand $\lambda x,y. e$ for $\lambda x. (\lambda y. e)$.^[This technique of simulating multiple-input functions with single-input functions is known as [Currying](https://en.wikipedia.org/wiki/Currying) and is named after the logician [Haskell Curry](https://en.wikipedia.org/wiki/Haskell_Curry).]

__Precedence and parenthesis.__
The above is a complete description of the $\lambda$ calculus.
However, to avoid clutter, we will allow to drop parenthesis for function invocation, and so if $f$ is a $\lambda$ expression and $z$ is some other expression, then we can write  $fz$ instead of $f(z)$ for the expression corresponding to invoking $f$ on $z$.^[When using  identifiers with multiple letters for $\lambda$ expressions,  we'll separate them with spaces or commas.]
That is, if $f$ has the form $\lambda x.e$ then $fz$ is the same as $f(z)$, which corresponds to the expression $e[x \rightarrow z]$ (i.e., the expression obtained by invoking $f$ on $z$ via replacing all copies of the $x$ parameter with $x$).

We can still use parenthesis for grouping and so $f(gh)$ means invoking $g$ on $h$ and then invoking $f$ on the result, while $(fg)h$ means invoking $f$ on $g$ and then considering the result as a function which then is invoked on $h$.
We will associate from left to right and so identify $fgh$ with $(fg)h$.
For example, if $f = \lambda x.(\lambda y.x+y)$ then $fzw=(fz)w=z+w$.


__Functions as first-class citizens.__
The key property of the $\lambda$ calculus (and functional languages in general) is that functions are "first-class citizens" in the sense that they can be used as parameters and return values of other functions.
Thus, we can invoke one $\lambda$ expression on another.
For example if  $DOUBLE$ is the $\lambda$ expression $\lambda f.(\lambda x. f(fx))$, then for every function $f$, $DOUBLE f$ corresponds to the function that invokes $f$ twice on $x$ (i.e., first computes $fx$ and then invokes $f$ on the result).
In particular, if  $f=\lambda y.y+1$ then  $DOUBLE f = \lambda x.x+2$.

### Defining bits and strings in the $\lambda$ calculus.

The pure $\lambda$-calculus does not contain the operations of addition, multiplication etc.., and in fact does not have any objects other than functions.
It turns out that this is enough, and we can define numbers using only $\lambda$ expressions.
Traditionally in the $\lambda$-calculus people use [Peano numbers](https://wiki.haskell.org/Peano_numbers) which means that we identify the number $2$ with the function $DOUBLE$ above, the number $3$ with the corresponding function $TRIPLE$ and so on and so forth.  
That is, the Peano  $\lambda$-expression for $1$ is the function $\lambda f.f$, the Peano $\lambda$-expression for $2$ is the function  $\lambda f.(\lambda x. f(fx))$, the Peano $\lambda$-expression for $3$ is $\lambda f.(\lambda x.f(f(fx)))$ and so on. (The Peano $\lambda$-expression for $0$ is $\lambda f.(\lambda x.x)$).


Since we want to work directly with bits and strings, rather than natural numbers, we will use a slightly different convention.
We will identify $0$  with the function $\lambda x,y.x$ and $1$ with the function $\lambda x,y.y$.^[Recall that by our convention, this means we identify $0$ with $\lambda x.(\lambda y.x)$ and $1$ with $\lambda x.(\lambda y.y)$.]
That is, you can think of $0$ as the function that maps a pair $(x,y)$ to $x$ and $1$ as the function that maps this pair to $y$.

With this identification, we can implement a function such as NOT simply as

$$
NOT = \lambda f.\lambda x,y.fyx
$$

Indeed, note that $NOT 0$ will be the function that takes $x,y$ and outputs $y$, and similarly $NOT 1$ will be the function that takes $y,x$ and outputs $0$.

Similarly, the following expression correspond to the $OR$ operation:

$$
OR = \lambda f,g. fgf
$$

For example, let us verify that $OR 0 1$ is indeed the $1$ function.
Indeed, since $0xy=x$ for every $x,y$, we get that $OR 01 = 010 = 1$.
Similarly, $OR 10 = 101=1$.


__String encoding:__
We can extend this to encode strings as functions as well.
For example, we will identify $00$  with the function that outputs the first element of a given four-tuple, and similarly $11$ will be the function that outputs the last element of a four-tuple.
More generally we identify a string $x \in \{0,1\}^n$ (which can also be thought of as a number in $[2^n]$) with the function $\lambda z_0,\ldots,z_{2^n-1}. z_x$.

__Concatenation.__
If we let $C = \lambda f,g.fgg$ then for a string $x$ and a bit $b$, $Cbx$ corresponds to the string $xb$ obtained by concatenating $b$ and $x$.
(It is a good exercise to pause here and verify that this indeed the case.)
By repeatedly applying the above operation, we can construct for every string $x\in \{0,1\}^*$ a $\lambda$-expression $\phi_x$ that corresponds to $x$.

__First and rest.__
Given a string $x=x_0x_1\ldots x_n$, we can define the functions $head$ and $rest$ (also known as `car` and `cdr` in Lisp parlance) such that $head(x)=x_0$ and $rest(x)=x_1\ldots x_{n-1}$.
^[TODO: complete this]

### $\lambda$-computable functions and NAND++ equivalence

We say that a $\lambda$-expression $e$ _computes_ a (partial) function $F: \{0,1\}^* \rightarrow \{0,1\}^*$ if for every $x\in \{0,1\}^*$ on which $F$ is defined, if $\phi_x$ is the $\lambda$-expression encoding $x$ then $e\phi_x$ is a $\lambda$-expression encoding $F(x)$.
We say that a function $F$ is  _$\lambda$-computable_ if and only if it can be computed  by a $\lambda$-expression.

Since evaluating a $\lambda$ expression simply corresponds to iteratively doing a "search and replace", we can easily write a NAND<< (or NAND++) program that given  $\lambda$ expressions $e$ and $f$, evaluates $ef$.
This can be used to show "only if" direction of the following theorem:

> # {.theorem title="$\lambda$-computable functions are computable" #lambdaturing-thm}
A partial function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ is computable by a $\lambda$-expression if and only if it is computable by a NAND++ program.

### The Y combinator and simulating NAND++ programs using $\lambda$ expressions.

The "if" direction of [lambdaturing-thm](){.ref} is less obvious, and we won't show the full details here.
Since we have AND and OR, we can obviously compute NANDs, which can be used to show to transform a NAND program into a $\lambda$ expression.

However, NAND programs can only compute finite functions, and we need some way to compute loops.
To handle   loops  we will  use _recursion_.
A priori it is not obvious how to do recursion in the pure $\lambda$ calculus.
We would like to write something like $f = \lambda x.e$ where $f$ itself appears in $e$, but cannot do it since we only have anonymous functions.

The solution is to think of a recursion  as a sort of "differential equation" on functions.
For example, consider the parity function $par:\{0,1\}^* \rightarrow \{0,1\}$.
We can define $par$ recursively as
$$
par(x_0,\ldots,x_n) = \begin{cases} 0 & |x|=0 \\ x_0 \oplus par(x_1,\ldots,x_n) \text{otherwise} \end{cases}
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
q(x_0,\ldots,x_n) = \begin{cases} 0 & |x|=0 \\ x_0 \oplus p(x_1,\ldots,x_n) \text{otherwise} \end{cases}
\label{eq:par-recurse}
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
par x = ITE(emptry(x), 0 , XOR first(x) par(rest(x))) \label{eq:par-recurse}
$$

where $ITE(a,b,c)$ is the function that outputs $b$ if $a=1$ and $c$ otherwise,  $empty(x)$ is the function that outputs $1$ if $x$ corresponds to the empty string, and $XOR(a,b)$ computes the XOR operation.

All of these are not hard to implement in the $\lambda$ calculus but of course the key issue with [eq:par-recurse](){.eqref} is that it is recursive.
We avoid the recursion by converting [eq:par-recurse](){.eqref} to the operator $PAREQ$ defined as

$$
PAREQ  = \lambda p. \lambda x. ITE(emptry(x), 0 , XOR first(x) p(rest(x)))
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
Chapter 8 of the book [The Nature of Computation](http://nature-of-computation.org/) is wonderful resource for some of those models.
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
The next state of a cell depends on its previous state and the states of its 8 vertical, horizontal and vertical neighbors.
A dead cell becomes alive only if exactly three of its neighbors are alive.
A live cell continues to live if it has two or three live neighbors.
Even though the number of cells is potentially infinite, we can have a finite encoding for the state by only keeping track of the live cells.
If we initialize the system in a configuration with a finite number of live cells, then the number of live cells will stay finite in all future steps.


We can think of such a system as encoding a computation by starting it in some initial configuration, and then defining some halting condition (e.g., we halt if the cell at position $(0,0)$ becomes dead) and some way to define an output (e.g., we output the state of the cell at position $(1,1)$).
Clearly, given any starting configuration $x$, we can simulate the game of life starting from $x$ using a NAND<< (or NAND++) program, and hence every "Game-of-Life computable" function is computable by a NAND<< program.
Surprisingly, it turns out that the other direction is true as well: as simple as its rules seem, we can simulate a NAND++ program using the game of life (see [golfig](){.ref}).
The [Wikipedia page](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) for the Game of Life contain some beautiful figures and animations of  configurations that produce some very interesting evolutions.
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

  \

Later on in this course we will study _memory bounded_ computation.
It turns out that NAND++ programs with a constant amount of memory are equivalent to the model of _finite automata_ (the adjectives "deterministic" or "nondeterministic" are sometimes added as well, this model is also known as _finite state machines_) which in turns captures the notion of _regular languages_ (those that can be described by [regular expressions](https://en.wikipedia.org/wiki/Regular_expression)).


## The Church-Turing Thesis

We have defined functions to be _computable_ if they can be computed by a NAND++ program, and we've seen that the definition would remain the same if we replaced NAND++ programs by Python programs, Turing machines, $\lambda$ calculus,  cellular automata, and many other computational models.
The _Church-Turing thesis_ is that this is the only sensible definition of "computable" functions.
Unlike the "Physical Extended Church Turing Thesis" (PECTT) which we saw before, the Church Turing thesis does not make a concrete physical prediction that can be experimentally tested, but it certainly motivates predictions such as the PECTT.
One can think of the Church-Turing Thesis as either advocating a definitional choice, making some prediction about all potential computing devices, or suggesting some laws of nature that constrain the natural world.
In Scott Aaronson's words, "whatever it is, the Church-Turing thesis can only be regarded as extremely successful".
No candidate computing device (including quantum computers, and also much less reasonable models such as the hypothetical "closed time curve" computers we mentioned before) has so far mounted a serious challenge to the Church Turing thesis.
These devices might potentially make some computations more _efficient_, but they do not change the difference between what is finitely computable and what is not.^[The _extended_ Church Turing thesis, which we'll discuss later in this course, is that NAND++ programs even capture the limit of what can be _efficiently_ computable. Just like the PECTT, quantum computing presents the main challenge to this thesis.]


## Turing completeness as a bug

We have seen that seemingly simple formalisms can turn out to be Turing complete.
The [following webpage](http://beza1e1.tuxen.de/articles/accidentally_turing_complete.html) lists several examples of formalisms that "accidentally" turned out to Turing complete, including supposedly limited languages such as the C preprocessor, CCS, SQL, sendmail configuration, as well as games such as Minecraft, Super Mario, and  the card game "Magic: The gathering".
This is not always a good thing, as it means that such formalisms can give rise to arbitrarily complex behavior.
For example, the postscript format (a precursor of PDF) is a Turing-complete programming language meant to describe documents for printing.
The expressive power of postscript can allow for short description of very complex images.
But it also gives rise to some nasty surprises, such as the attacks described in  [this page](http://hacking-printers.net/wiki/index.php/PostScript) ranging from using infinite loops as a denial of service attack, to accessing the printer's file system.

An interesting recent example of the pitfalls of Turing-completeness arose in the context of the cryptocurrency [Ethereum](https://www.ethereum.org/).
The distinguishing feature of this currency is the ability to design "smart contract" using an expressive (and in particular Turing-complete) language.  
Whereas in our "human operated" economy, Alice and Bob might pool their funds together sign a contract to create a joint venture and agree that if condition X happens then they will invest in Charlie's company, Ethereum allows Alice and Bob to create a joint venture where Alice and Bob pool their funds together into an account that will be governed by some program $P$ that would decide under what conditions it disburses funds from it.
For example, one could imagine some code that interacts between Alice, Bob, and some program running on Bob's car that would allow Alice to rent out Bob's car without any human intervention or overhead.


Specifically Ethereum uses the Turing-complete programming  [solidity](https://solidity.readthedocs.io/en/develop/index.html) which has a syntax similar to Javascript.
The flagship of Ethereum was an experiment known as  The "Decentralized Autonomous Organization" or [The DAO](https://en.wikipedia.org/wiki/The_DAO_(organization)).
The idea was to create a smart contract that would create an autonomously run decentralized venture capital fund, without human managers, were shareholders could decide on investment opportunities.
The DAO was  the biggest crowdfunding success in history and at its height was worth 150 million dollars, which was more than ten percent of the total Ethereum market.
Investing in the DAO (or entering any other "smart contract") amounts to providing your funds to be run by a computer program. i.e., "code is law", or to use the words the DAO described itself: "The DAO is borne from immutable, unstoppable, and irrefutable computer code".
Unfortunately, it turns out that (as we'll see in the next lecture) understanding the behavior of Turing-complete computer programs is quite a hard thing to do.
A hacker (or perhaps, some would say, a savvy investor) was able to fashion an input that would cause the DAO code to essentially enter into an infinite recursive loop in which it continuously transferred funds into their account, thereby [cleaning out about 60 million dollars](https://www.bloomberg.com/features/2017-the-ether-thief/) out of the DAO.
While this transaction was "legal" in the sense that it complied with the code of the smart contract, it was obviously not what the humans who wrote this code had in mind.
There was a lot of debate in the Ethereum community how to handle this, including some partially successful "Robin Hood" attempts to use the same loophole to drain the DAO funds into a secure account.
Eventually it turned out that the code is mutable, stoppable, and refutable after all, and the Ethereum community decided to do a "hard fork" (also known as a "bailout") to revert history to before this transaction.
Some elements of the community strongly opposed this decision, and so an alternative currency called [Ethereum Classic](https://ethereumclassic.github.io/)  was created that preserved the original history.





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
