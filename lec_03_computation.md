# Defining computation

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


![Text pages from Algebra manuscript with geometrical solutions to two quadratic equations. Shelfmark: MS. Huntingdon 214 fol. 004v-005r](../figure/alKhwarizmi.jpg){#alKhwarizmi .class width=300px height=300px}

For the purposes of this course, we will need a much more precise way to define algorithms.
Fortunately (or is it unfortunately?), at least at the moment, computers lag far behind school-age children in learning from examples.
Hence in the 20th century people have come up with  exact formalisms for describing algorithms, namely _programming languages_.
Here is al-Khwarizmi's quadratic equation solving  algorithm described in the Python programming language:^[For concreteness we will sometimes include code of actual programming languages in these notes. However, these will be simple enough to be understandable even by people that are not familiar with these languages.]



~~~~ { .python .numberLines }
def solve_eq(b,c):
    # return solution of x^2 + bx = c using Al Khwarizmi's instructions
    val1 = b/2.0 # halve the number of the roots
    val2 = val1*val1 # this you multiply by itself
    val3 = val2 + c # Add this to thirty-nine (c)
    val4 = math.sqrt(val3) # take the root of this
    val5 = val4 - val1 # subtract from it half the number of roots
    return val5  # This is the root of the square which you sought for
~~~~


## The NAND Programming language

We can try to use a modern programming language such as Python or C for our formal model of computation, but it would be quite hard to reason about, given that the [Python language reference](https://docs.python.org/2/reference/) has more than 100 pages.
Thus we will define computation using an extremely simple "programming language": one that has only a single operation.
This raises the question of whether this language is rich enough to capture the power of modern computing systems.
We will see that (to a first approximation), the answer to this question is __Yes__.


We  start by defining a programming language that can only compute _finite_ functions.
That is, functions $F$ that map $\{0,1\}^n$ to $\{0,1\}^m$ for some natural numbers $m,n$.
Later we will discuss how to extend the language to allow for a single program that can compute a function of every length, but the finite case is already quite interesting and will give us a simple setting for exploring some of the salient features of computing.

The _NAND programming language_ has no loops, functions, or if statements.
It has only a single operation: `NAND`.
That is, every line in a NAND program has the form:

```
foo := bar NAND baz
```

where `foo`, `bar`, `baz` are variable names.^[The terms `foo` and `bar` are [often used](https://en.wikipedia.org/wiki/Foobar) to describe generic variable names in the context of programming, and we will follow this convention throughout the course.
See the appendix and the website [http://nandpl.org](http://nandpl.org) for a full specification of the NAND programming language.]
When this line is executed,  the variable `foo` is assigned the _negation of the logical AND_ of (i.e., the NAND operation applied to) the values of the two variables `bar` and `baz`.^[The _logical AND_ of two bits $x,x'\in \{0,1\}$  is equal to $1$ if $x=x'=1$ and is equal to $0$ otherwise. Thus its negation satisfies $NAND(0,0)=NAND(0,1)=NAND(1,0)=1$, while $NAND(1,1)=0$. If a variable hasn't been assigned a value, then its default value is zero.]  

All variables in the NAND programming language are _Boolean_: can take values that are either zero or one.
Variables such as `x_22` or `y_18` (that is, of the form `x_`$\expr{i}$  or `y_`$\expr{i}$  where $i$ is a natural number)  have a special meaning.^[In these lecture notes, we  use the convention that when we write $\expr{e}$  then we mean the numerical value of this expression. So for example if $k=10$ then we can write `x_`$\expr{k+7}$ to mean  `x_17`. This is just for the notes: in the NAND programming language itself the indices have to be absolute numerical constants.]
The variables beginning with `x_` are _input_ variables and those beginning with `y_` are _output_ variables.
Thus for example the following four line NAND program takes an input of two bits and outputs a single bit:


~~~~ { .go .numberLines  }
u   := x_0 NAND x_1
v   := x_0 NAND u
w   := x_1 NAND u
y_0 := v   NAND w
~~~~   

> # { .pause }
Can you guess what function from $\{0,1\}^2$ to $\{0,1\}$ this program computes? It might be a good idea for you to pause here and try to figure this out.


To find the function that this program computes, we can run it on all the four possible two bit inputs: $00$,$01$,$10$, and $11$.  
For example, let us consider the execution of this program on the input $00$, keeping track of the values of the variables as the program runs line by line.
On the website [http://nandpl.org](http://nandpl.org) we can run NAND programs in a "debug" mode, which will produce an _execution trace_ of the program.^[At present the web interface is not yet implemented, and you can run NAND program using an OCaml interpreter that you can download from that website. The implementation is in a fluid state and so the text below might not exactly match the output of the interpreter.]
When we run the program above on the input $01$, we get the following trace:

```
Executing step 1: "u   := x_0 NAND x_1"	 x_0 = 0, x_1 = 1, u   is assigned 1,
Executing step 2: "v   := x_0 NAND u"	 x_0 = 0, u   = 1, v   is assigned 1,
Executing step 3: "w   := x_1 NAND u"	 x_1 = 1, u   = 1, w   is assigned 0,
Executing step 4: "y_0 := v   NAND w"	 v   = 1, w   = 0, y_0 is assigned 1,
Output is y_0=1
```



On the other hand if we execute this program on the input $11$, then we get the following execution trace:

```
Executing step 1: "u   := x_0 NAND x_1"	 x_0 = 1, x_1 = 1, u   is assigned 0,
Executing step 2: "v   := x_0 NAND u"	 x_0 = 1, u   = 0, v   is assigned 1,
Executing step 3: "w   := x_1 NAND u"	 x_1 = 1, u   = 0, w   is assigned 1,
Executing step 4: "y_0 := v   NAND w"	 v   = 1, w   = 1, y_0 is assigned 0,
Output is y_0=0
```


You can verify that on input $10$ the program will also output $1$, while on input $00$ it will output zero.
Hence the output of this program on every input is summarized in the following table:

| Input          | Output         |
| :------------- | :------------- |
| $00$           | $0$            |
| $01$           | $1$            |
| $10$           | $1$            |
| $11$           | $0$            |

\





In other words, this program computes the _exclusive or_ (also known as XOR) function.


### Adding one-bit numbers

Now that we can compute XOR, let us try something just a little more ambitious: adding a pair of one-bit numbers.
That is, we want to compute the function $ADD_1:\{0,1\}^2\rightarrow\{0,1\}^2$ such that $ADD(x_0,x_1)$ is the binary representation of the addition of the two numbers $x_0$ and $x_1$. Since the sum of two $0/1$ values is a number in $\{0,1,2\}$, the output of the function $ADD_1$ is of length two bits.


If we write the sum $x_0+x_1$ as $y_02^0 + y_12^1$ then the table of values for $ADD_1$ is the following:



| Input |       | Output |       |
|-------|-------|--------|-------|
| `x_0` | `x_1` | `y_0`  | `y_1` |
| $0$   | $0$   | $0$    | $0$   |
| $1$   | $0$   | $1$    | $0$   |
| $0$   | $1$   | $1$    | $0$   |
| $1$   | $1$   | $0$    | $1$   |

 \


One can see that `y_0` will be the XOR of `x_0` and `x_1` and `y_1` will be the AND of `x_0` and `x_1`.^[This is a special case of the general rule that when you add two digits $x,x' \in \{0,1,\ldots,b-1\}$ over the $b$-ary basis (in our case $b=2$), then the output digit is $x+x' (\mod b)$ and the carry digit is $\lfloor (x+x')/b  \rfloor$.]
Thus we can compute one bit variable addition using the following program:

~~~~ { .go .numberLines  }
// Add two single-bit numbers
u   := x_0 NAND x_1
v   := x_0 NAND u
w   := x_1 NAND u
y_0 := v NAND w
y_1 := u NAND u
~~~~   

If we run this program on the input $(1,1)$ we get the execution trace

```
Executing step 1: "u   := x_0 NAND x_1"	 x_0 = 1, x_1 = 1, u   is assigned 0,
Executing step 2: "v   := x_0 NAND u"	 x_0 = 1, u   = 0, v   is assigned 1,
Executing step 3: "w   := x_1 NAND u"	 x_1 = 1, u   = 0, w   is assigned 1,
Executing step 4: "y_0 := v NAND w"	 v   = 1, w   = 1, y_0 is assigned 0,
Executing step 5: "y_1 := u NAND u"	 u   = 0, u   = 0, y_1 is assigned 1,
Output is y_0=0, y_1=1
```

and so you can see that the output $(0,1)$ is indeed the binary encoding of $1+1 = 2$.


### Formal definitions

For a NAND program $P$, its _input length_ is the largest number $n$ such that $P$ contains a variable of the form `x_`$\expr{n-1}$.
$P$'s  _output length_  is the largest number $m$ such that $P$ contains a variable of the form `y_`$\expr{m-1}$.^[As mentioned in the appendix, we require that all output variables are assigned a value, and that the largest index used in an $s$ line NAND program is smaller than $s$. In particular this means that an $s$ line program can have at most $s$ inputs and outputs.]
Intuitively, if $P$ is a NAND program with input length $n$ and output length $m$, and $F:\{0,1\}^n \rightarrow \{0,1\}^m$ is some function, then  $P$ computes $F$ if for every $x\in \{0,1\}^n$ and $y=F(x)$, whenever $P$ is executed with the `x_`$\expr{i}$ variable initialized to $x_i$ for all $i\in [n]$, at the end of the execution the variable `y_`$\expr{j}$ will equal $y_j$ for all $j\in [m]$.

To make sure we have a precise and unambiguous definition of computation, we will now model NAND programs using sets and tuples, and recast the notion of computing a function in these terms.


> # {.definition title="NAND program" #NANDprogram}
A _NAND program_ is a 4-tuple $P=(V,X,Y,L)$ of the following form: \
* $V$ (called the _variables_) is some finite set.
>
* $X$ (called the _input variables_) is a tuple of elements in $V$, i.e. $X \in V^*$. We require that the elements of $X$ are distinct: $X_i \neq X_j$ for all $i\neq j$ in $[n]$ where $n=|X|$.
>
* $Y$ (called the _output variables_) is a tuple of elements in $V$, i.e., $Y \in V^*$. We require that the elements of $Y$ are distinct (i.e.,  $Y_i \neq Y_j$ for all $i\neq j$ \in $[m]$ where $m=|Y|$) and that they are disjoint from $X$ (i.e., $Y_i \neq X_j$ for every $i\in [n]$ and $j\in [m]$).
>
* $L$ (called the _lines_) is a tuple of _triples_ of $V$, i.e., $L \in (V \times V \times V)^*$. Intuitively, if the $\ell$-the element of $L$ is a triple $(u,v,w)$ then this corresponds to the $\ell$-th line of the program being $u$ ` := ` $v$ ` NAND ` $w$. We require that for every triple $(u,v,w)$, $u$ does not appear in $X$ and $v,w$ do not appear in $Y$. Moreover, we require that for every $x\in V$, $x$ is contained in some  triple in $L$.
>
The _number of inputs_ of $P=(V,X,Y,Z)$ is equal to $|X|$ and the _number of outputs_ is equal to $|Y|$.


> # { .pause }
This definition is somewhat long and cumbersome, but really corresponds to a straightforward modelling of NAND programs, under the map that $V$ is the set of all variables appearing in the program, $X$ corresponds to the tuple $($`x_`$\expr{0}$, `x_`$\expr{1}$, $\ldots$, `x_`$\expr{n-1}$ $)$, $Y$ corresponds to the tuple $($ `y_`$\expr{0}$, `y_`$\expr{1}$, $\ldots$, `y_`$\expr{m-1}$, $)$ and $L$ corresponds to the list of triples of the form $($ `foo` $,$ `bar`, $,$ `baz` $)$ for every line `foo := bar NAND baz` in the program.
Please pause here and verify that you understand this correspondence.

Now that we defined NAND programs formally, we turn to formally defining  the notion of computing a function.
Before we do that, we will need to talk about the notion of the _configuration_ or  "snapshot" of a NAND program.
Such a configuration simply corresponds to the  current line that is executed and the current values of all variables at a certain point in the execution.
Thus we will model it as a pair $(\ell,\sigma)$ where $\ell$ is a number between $0$ and the total number of lines in the program, and $\sigma$ maps every variable to its current value.
The initial configuration has the form $(0,\sigma_0)$ where $0$ corresponds to the first line, and $\sigma_0$ is the assignment of zeroes to all variables and $x_i$'s to the input variables.
The final configuration will have the form $(s,\sigma_s)$ where $s$ is the number of lines (i.e., corresponding to "going past" the final line) and $\sigma_s$ is the final values assigned to all variables, which in particular encodes also the values of the output variables.
We now write the formal definition.
As always, it is a good practice to verify that this formal definition matches the intuitive description above:




> # {.definition title="Configuration of a NAND program" #NANDconfiguration}
Let $P=(V,X,Y,L)$ be a NAND program, and let $n=|X|$, $m=|Y|$ and $s=|L$. A _configuration_ of $P$ is a pair $(\ell,\sigma)$ where $\ell \in [s+1]$ and $\sigma$ is a  function $\sigma:V \rightarrow \{0,1\}$ that maps every variable of $P$ into a bit in $\{0,1\}$.
We define $CONF(P) = [s+1] \times \{ \sigma \;|\; \sigma:V \rightarrow \{0,1\} \}$ to be the set of all configurations of $P$.^[Note that $|CONF(P)| = |L+1|2^{|V|}$: can you see why?]
>
If $P$ has $n$ inputs, then for every $x\in \{0,1\}^n$, the _initial configuration of $P$ with input $x$_ is the the pair $(0,\sigma_0)$ where $\sigma_0:V \rightarrow \{0,1\}$ is the function defined as $\sigma_0(X_i)=x_i$ for every $i\in [n]$ and $\sigma_0(v)=0$ for all variables not in $X$.

An execution of a NAND program can be thought of as simply progressing, line by line, from the initial configuration to the next one:

> # {.definition title="NAND next step function" #nextstepNAND}
For every NAND program $P=(V,X,Y,L)$, the _next step function of $P$_, denoted by $NEXT_P$, is the function $NEXT_P:CONF(P) \rightarrow CONF(P)$ that defined as follows:
>
For every $(\ell,\sigma)  \in CONF(P)$, if $\ell=|L|$ then $NEXT_P(\ell,\sigma)=(\ell,\sigma)$.
Otherwise $NEXT_P(\ell,\sigma) = (\ell+1,\sigma')$ where $\sigma':V \rightarrow \{0,1\}$ is defined as follows:
$$
\sigma'(x) = \begin{cases} NAND(v,w)   & x=u \\
             \end{cases}   \sigma(x)   & \text{otherwise}
$$
where $(u,v,w)=L_\ell$ is the $\ell$-th triple in $L$.
>
For every input $x\in \{0,1\}^n$ and $\ell in [s+1]$, the _$\ell$-th configuration of $P$ on input $x$_, denoted as $conf_\ell(P,x)$ is defined recursively as follows:
$$
conf_\ell(P,x) = \begin{cases} (0,\sigma_0) & \ell=0 \\
                \end{cases}   NEXT_P(conf_{\ell-1}(P)) & \text{otherwise}
$$
where $(0,\sigma_0)$ is the configuration of $P$ on input $x$.


We can now finally formally define the notion of computing a function:

> # {.definition title="Computing a function" #computefuncNAND}
Let $P=(V,X,Y,L)$ and $n=|X|$, $m=|Y|$ and $s=|L|$.
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$.
We say that _$P$ computes $F$_ if for every $x\in \{0,1\}^n$, if $y=F(x)$ then $conf_s(P,x)=(s,\sigma)$ where $\sigma(Y_j) = y_j$ for every $j\in [m]$.
>
For every $s\in \N$, we define $SIZE(s)$ to be the set of all functions that are computable by a NAND program of at most $s$ lines.


> # { .pause }
The formal specification of any programming language, no matter how simple, is often cumbersome, and the definitions above are no exception.
You should go back and read them and make sure that you understand why they correspond to our informal description of computing a function via NAND circuits.
From this point on, we will not distinguish between the representation of  a NAND program in terms of lines of codes, and its representation as a tuple $P=(V,X,Y,L)$.

Let $XOR_n:\{0,1\}^n \rightarrow \{0,1\}$ be the function that maps $x\in \{0,1\}^n$ to $\sum_{i=0}^n x_i (\mod 2)$.
The NAND program we presented above yields a proof of the following theorem

> # {.theorem title="Computing XOR" #xortwothm}
$XOR_2 \in SIZE(4)$

Similarly, the addition program we presented shows that   $ADD_1 \in SIZE(5)$.


## Canonical input and output variables

The specific identifiers for  NAND variables (other than the inputs and outputs) do not make any difference in the program's functionality, as long as we give separate variable distinct identifiers.
For example, if I replace all instances of the variable `foo` with `boazisgreat` then, under the (unfortunately common) condition that `boazisgreat` was not used in the original program, the resulting  program will still compute the same function.
For convenience, it is sometimes useful to assume that all variables identifiers have some canonical form such as being either `x_`$\expr{i}$, `y_`$\expr{j}$ or `work_`$\expr{k}$.
Similarly, while we allowed in  [NANDprogram](){.ref} the  variables to be members of some arbitrary set $V$, it is sometimes useful to assume that $V$ is simply the set of numbers from $0$ to some natural number (which can never be more than $n+m$ plus twice the number of lines $s$).
This motivates the following definition:

> # {.definition title="Canonical variables" #NANDcanonical}
Let $P=(V,X,Y,L)$ be a NAND program and let $n=|X|$ and $m=|Y|$.
We say that $P$ has _canonical variables_ if $V=[t]$ for some $t\in \N$, $X=(0,1,\ldots,n-1)$ and $Y=(n,n+1,\ldots,n+m-1)$.

We have the following theorem:

> # {.theorem title="Convert to canonical variables" #canonicalvarsthm}
For every $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $s\in\N$, $F$ can be computed by an $s$-line NAND program if and only if it can be computed by an $s$-line NAND program with canonical variables.

> # {.proof data-ref="canonicalvarsthm"}
The "if" direction is trivial, since a NAND program with canonical variables is just a special case of a NAND program.
For the "only if" direction, let $P=(V,X,Y,L)$ be an $s$-line NAND program computing $F$, and let $t=|V|$.
We define a bijection $\pi:V \rightarrow [t]$ as follows: $\pi(X_i)=i$ for all $i\in [n]$, $\pi(Y_j)=n+j$ for all $j\in [m]$ and we map the remaining $t-m-n$ elements of $V$ to $\{ n+m,\ldots,t-1\}$ in some arbitrary one to one way. (We can do so because the $X$'s and $Y$'s are distinct and disjoint.)
Now define $P' = (\pi(V),\pi(X),\pi(Y),\pi(L))$, where by this we mean that we apply $\pi$ individually to every element of of $V$,$X$, $Y$, and the triples of $L$.
Since (as we leave you to verify) the definition of configurations and computing a function are invariant under bijections of $V$, $P'$ computes the same function as $P$.


Given [canonicalvarsthm](){.ref}, we will always be able to assume "without loss of generality" that a NAND program $P$ has canonical form.
A canonical form program $P$ can also be represented as a triple $(n,m,L)$ where $n,m$ are (as usual) the inputs and outputs, and $L$ is the lines.
This is because we recover the original representation $(V,X,Y,L)$ by simply setting $X=(0,1,\ldots,n-1)$, $Y =(n,n+1,\ldots,n+m-1)$ and $V=[t]$ where $t$ is one plus the largest number appearing in a triple of $L$.
In the following we will freely move between these two representations.
If $n,m$ are known from the context, then a canonical form program can be represented simply by the list of triples $L$.


## Composing functions

Computing the XOR or addition of two bits is all well and good, but still seems a long way off from even the algorithms we all learned in elementary school, let alone [World of Warcraft](https://worldofwarcraft.com/en-us/).
We will get to computing more interesting functions, but for starters let us prove the following simple extension of [xortwothm](){.ref}

> # {.theorem title="Computing four bit parity" #xorfourthm}
$XOR_4 \in SIZE(12)$

We can prove [xorfourthm](){.ref} by explicitly writing down a 12 line program.
But writing NAND programs by hand can get real old real fast.
So, we will prove more general results about _composing_ functions:

> # {.theorem title="Sequential composition of functions" #seqcompositionthm}
If $F:\{0,1\}^n \rightarrow \{0,1\}^m$ is a function in $SIZE(L)$ and $G:\{0,1\}^m \rightarrow \{0,1\}^k$ is a function in $SIZE(L')$ then $G\circ F$ is a function in $SIZE(L+L')$, where $G\circ F:\{0,1\}^n \rightarrow \{0,1\}^k$ is the function that maps $x\in \{0,1\}^n$ to $G(F(x))$.


> # {.theorem title="Parallel composition of functions" #parcompositionthm}
If $F:\{0,1\}^n \rightarrow \{0,1\}^m$ is a function in $SIZE(L)$ and $G:\{0,1\}^{n'} \rightarrow \{0,1\}^{m'}$ is a function in $SIZE(L')$ then $F \oplus G$ is a function in $SIZE(L+L')$, where
$G \oplus H: \{0,1\}^{n+n'} \rightarrow \{0,1\}^{m+m'}$ is the function that maps $x \in \{0,1\}^{n+n'}$ to $F(x_0,\ldots,x_{n-1})G(x_n,\ldots,x_{n+n'-1})$.


Before proving [seqcompositionthm](){.ref} and [parcompositionthm](){.ref}, note that they do imply [xorfourthm](){.ref}.
Indeed, it's easy to verify that for every $x \in \{0,1\}^4$,

$$
XOR_4(x) = \sum_{i=0}^3 x_i (\mod 3) = ((x_0+x_1 \mod 2) + (x_2+x_3 \mod 2) \mod 2) = XOR_2(XOR_2(x_0,x_1)XOR_2(x_2,x_3))
$$

and hence

$$
XOR_4= XOR_2 \circ (XOR_2 \oplus XOR_2) \;.
$$

Since $XOR_2$ is in $SIZE(4)$, it follows that $XOR_4 \in SIZE(4+(4+4))=SIZE(12)$.

Using the same idea we can prove the following more general result:

> # {.theorem title="Computing parity via NAND circuits" #paritycircuitthm}
For every $n>1$, $XOR_n \in SIZE(10n)$

We leave proving [paritycircuitthm](){.ref} as [paritycircuitex](){.ref}.

## Representing programs as graphs

We can prove [seqcompositionthm](){.ref} and [parcompositionthm](){.ref} by directly arguing that we can "copy and paste" the code for $F$ and $G$ to achieve a program that computes $F \circ G$ and $F \oplus G$ respectively.
However, we will use a more general approach, first giving a more "mathematical" representation for NAND programs as _graphs_, and then using this representation to prove these two theorems.

> # { .pause }
If you are not comfortable with the definitions of graphs, and in particular directed acyclic graphs (DAGs), now would be a great time to go back to the "mathematical background" lecture, as well as some of the resources [here](http://www.boazbarak.org/cs121/background/), and review these notions.

> # {.definition title="NAND circuit" #NANDcircdef}
A _NAND circuit_ with $n$ inputs and $m$ outputs is a labeled directed acyclic graph (DAG) in which every vertex has in-degree at most two. We require that there  are $n$ vertices with in-degree zero, known  as _input variables_, that are labeled with  `x_`$\expr{i}$ for $i\in [n]$.
Every vertex apart from the input variables is known as a _gate_. We require that there are $m$  vertices of out-degree zero, denoted as the _output gates_, and that are labeled with `y_`$\expr{j}$ for $j\in [m]$.
While not all vertices are labeled, no two vertices get the same label.
We denote the circuit  as $C=(V,E,L)$ where $V,E$ are the vertices and edges of the circuit, and $L:V \rightarrow_p S$ is the (partial) one-to-one labeling function that maps vertices into the set $S=\{$ `x_0`,$\ldots$,`x_`$\expr{n-1}$,`y_0`,$\ldots$, `y_`$\expr{m-1}$,$\}$.
The _size_ of a circuit $C$, denoted by $|C|$, is the number of gates that it contains.

The definition of NAND circuits is not ultimately that complicated, but may take  a second or third read  to fully parse.
It might help to look at [XORcircuitfig](){.ref}, which describes the NAND circuit that corresponds to the 4-line NAND program we presented above for the $XOR_2$ function.



![A NAND circuit for computing the $XOR_2$ function. Note that it has exactly four gates, corresponding to the four lines of the NAND program we presented above. The green labels $u,v,w$ for non-output gates are just for illustration and comparison with the NAND program, and are not formally part of the circuit.](../figure/XORcircuit.png){#XORcircuitfig .class width=300px height=300px}

A NAND circuit corresponds to computation in the following way.
To compute some output on an input $x\in \{0,1\}^n$, we start by assigning to the input vertex labeled with `x_`$\expr{i}$ the value $x_i$, and then proceed by assigning for every gate $v$ the value that is   the NAND of the values assigned to its in-neighbors (if it has less than two in-neighbors, we replace the value of the missing neighbors by zero).
The output $y\in \{0,1\}^m$  corresponds to the value assigned to the output gates, with $y_j$ equal to the value assigned to the value assigned to the gate labeled `y_`$\expr{j}$ for every $j\in [m]$.
Formally, this is defined as follows:

> # {.definition title="Computing a function by a NAND circuit" #NANDcirccomputedef}
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and let $C=(V,E,L)$ be a NAND circuit with $n$ inputs and $m$ outputs.
We say that _$C$ computes $F$_ if there is a map $Z:V \rightarrow \{0,1\}$, such that for every $x\in \{0,1\}^n$, if $y=F(x)$ then: \
* For every $i\in [n]$, if $v$ is labeled with `x_`$\expr{i}$ then $Z(v)=x_i$. \
* For every $j\in[m]$, if $v$ is labeled with `y_`$\expr{j}$ then $Z(v)=y_j$. \
* For every gate $v$ with in-neighbors $u,w$, if $a=Z(u)$ and $b=Z(w)$, $Z(v)=NAND(a,b)$. (If $v$ has fewer than two neighbors then we replace either $b$ or both $a$ and $b$ with zero in the condition above.)

> # { .pause }
You should make sure you understand _why_ [NANDcirccomputedef](){.ref} captures the informal description above. This might require reading the definition a second or third time, but would be crucial for the rest of this course.

The following theorem says that these two notions of computing a function are actually equivalent: we can transform a NAND program into a NAND circuit computing the same function, and vice versa.

> # {.theorem title="Equivalence of circuits and straightline programs" #circuitprogequivthm}
For every $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $S\in \N$, $F$ can be computed by an $S$-line NAND program if and only if $F$ can be computed by an $n$-input $m$-output NAND circuit of $S$ gates.

The idea behind the proof is simple.
Just like we did to the XOR program, if we have a NAND program $P$ of $S$ lines, $n$ inputs, and $m$ outputs, we can transform it into a NAND circuit with $n$ inputs and $m$ gates, where each gate corresponds to a line in the program $P$. If  line $\ell$ involves the NAND of two variables assigned to in lines $\ell'$ and $\ell''$, then we will have edges to the gate corresponding to $\ell$ from the gates correspnding to $\ell',\ell''$.
In the other direction, we can transform a NAND circuit $C$ of  $n$ inputs, $m$ outputs and $S$ gates to an $S$-line program by essentially inverting this process.
For every gate in the program, we will have a line in the program which assigns to a variable the NAND of the variables corresponding to the in-neighbors of this gate.
If the gate is an output gate labeled with `y_`$\expr{j}$ then the  corresponding line will assign the value to the variable `y_`$\expr{j}$.
Otherwise we will assign the value to a fresh "workspace" variable.
We now show the formal proof.

> # {.proof data-ref="circuitprogequivthm"}
We start with the "only if" direction.
That is, we show how to transform a NAND program to a circuit.
Suppose that $P$ is an $S$ line program that computes $F$.
We will build a NAND circuit $C=(V,E,L)$ that computes $F$ as follows.
The vertex set $V$ will have the $n+S$ elements $\{ (0,0), \ldots, (0,n-1),(1,0),\ldots,(1,S-1) \}$.
That is, it will have $n$ vertices of the form $(0,i)$ for $i\in [n]$ (corresponding to the $n$ inputs), and $S$ vertices of the form $(1,\ell)$ (corresponding to the lines in the program).
For every line $\ell$ in the program $P$ of the form `foo := bar NAND baz`, we put edges in the graph of the form $\overrightarrow{(1,\ell')\;(1,\ell)}$ and $\overrightarrow{(1,\ell'')\;(1,\ell)}$ where  $\ell'$ and $\ell'$ are the last lines before $\ell$ in which the variables `bar` and `baz` were assigned a value.
If the variable `bar` and/or `baz` was not assigned a value prior to the $\ell$-th line and is not an input variable then we don't add a corresponding edge.
If the variable `bar` and/or `baz` is an input variable `x_`$\expr{i}$ then we add the edge $\overrightarrow{(0,i)\;(1,\ell)}$.
We label the vertices of the form $(0,i)$ with `x_`$\expr{i}$ for every $i\in [n]$.
For every $j\in[m]$, let $\ell$ be the last line in which the variable `y_`$\expr{j}$ is assigned a value,^[As noted in the appendix, valid NAND programs must assign a value to all their output variables.] and label the vertex $(1,\ell)$ with `y_`$\expr{j}$.
Note that the vertices of the form $(0,i)$ have  in-degree zero, and all edges of the form $\overrightarrow{(1,\ell')\;(1,\ell)}$ satisfy $\ell>\ell'$.
Hence this graph is a DAG, as in any cycle there would have to be at least on edge going from a vertex of the form $(1,\ell)$ to a vertex of the form $(1,\ell')$ for $\ell'<\ell$ (can you see why?).
Also, since we don't allow a variable of the form `y_`$\expr{j}$ on the right-hand side of a NAND operation, the output vertices have out-degree zero.
>
To complete the proof of the "only if" direction, we need to show that the circuit $C$ we constructed computes the same function $F$ as the program $P$ we were given.
Indeed, let $x\in \{0,1\}^n$ and $y = F(x)$.
For every $\ell$, let $z_\ell$ be the value that is assigned by the $\ell$-th line in the execution of $P$ on input $x$.
Now, as per [NANDcirccomputedef](){.ref}, define the map $Z:V \rightarrow \{0,1\}$ as follows: $Z((0,i))=x_i$ for $i\in [n]$ and $Z((1,\ell))=z_\ell$ for every $\ell \in [S]$.
Then, by our construction of the circuit, the map satisfies the condition that for vertex $v$ with in-neighbors $u$ and $w$, the value $Z(v)$ is the NAND of $Z(u)$ and $Z(w)$ (replacing missing neighbors with the value $0$), and hence in particular for every $j\in [m]$, the value assigned in the last line that touches `y_`$\expr{j}$ equals $y_j$.
Thus the circuit $C$ does compute the same function $F$.
>
For the "if" direction, we need to transform an $S$-gate circuit $C=(V,E,L)$ that computes $F:\{0,1\}^n \rightarrow \{0,1\}^m$ into an $S$-line NAND program $P$ that computes the same function.
We start by doing a [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) of the graph $C$.
That is we sort the vertex set $V$ as $\{v_0,\ldots,v_{n+S-1} \}$ such that  $\overrightarrow{v_i v_j} \in E$, $v_i < v_j$.
Such a sorting can be found for every DAG.
Moreover, because the input vertices of $C$ are "sources" (have in-degree zero), we can ensure they are placed first in this sorting and moreover for every $i\in [n]$, $v_i$ is the input vertex labeled with `x_`$\expr{i}$.
>
Now for $\ell=0,1,\ldots,n+S-1$ we will define a variable  $var(\ell)$  in our resulting program as follows:
If $\ell<n$ then $var(\ell)$ equals `x_`$\expr{i}$.
If $v_\ell$ is an output gate  labeled with `y_`$\expr{j}$ then $var(\ell)$ equals `y_`$\expr{j}$.
otherwise  $var(\ell)$ will be a temporary workspace variable `temp_`$\expr{\ell-n}$.
Our program $P$ will have $S$ lines, where for every $k\in [S]$, if the in-neighbors of $v_{n+k}$ are $v_i$ and $v_j$ then the $k$-th line in the program will be $var(n+k)$ ` := ` $var(i)$ ` NAND ` $var(j)$.
If $v_k$ has fewer  than two in-neighbors then we replace the corresponding variable with the variable `zero` (which is never set to any value and hence retains its default value of $0$.
>
To complete the proof of the "if" direction we need to show that the program $P$ we constructed computes the function $F$ as the circuit $C$ we were given.
Indeed, let $x\in \{0,1\}^n$ and $y=F(x)$.
Since $C$ computes $F$, there is a map $Z:V \rightarrow \{0,1\}$ as per  [NANDcirccomputedef](){.ref}.
We claim that if we run the program $P$ on input $x$, then for every $k\in [S]$ the value assigned by the $k$-th line corresponds to $Z(v_{n+k})$.
Indeed by construction the value assigned in the $k$-th line corresponds to the NAND of the value assigned to the in-neighbors of $v_{n+k}$.
Hence in particular if $v_{n+k}$ is the output gate labeled `y_`$\expr{j}$ then this value will equal $y_j$, meaning that on input $x$ our program will output $y=F(x)$.



## Composition from graphs

Given [circuitprogequivthm](){.ref}, we can prove [seqcompositionthm](){.ref} and [parcompositionthm](){.ref} by showing how to transform a circuits for $F$ and $G$ into circuits for $F \circ G$ and $F \oplus G$.
This is what we do now:

> # {.theorem title="Sequential composition, circuit version" #seqcompositioncircthm}
If $C,D$ are NAND circuits such that $C$ computes $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $D$ computes $G:\{0,1\}^m \rightarrow \{0,1\}^k$  then there is a circuit $E$ of size $|C|+|D|$ computing  the function $G\circ F:\{0,1\}^n \rightarrow \{0,1\}^k$.

![Given a circuit $C$ computing $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and a circuit $D$ computing $G:\{0,1\}^m \rightarrow \{0,1\}^k$, we obtain a circuit $E$ computing $G\circ F$ by identifying the inputs of $D$ with the outputs of $C$. That is, the resulting circuit consists of the gates of both $C$ and $D$, where we replace every in-neighbor of $D$ that was an input gate with the corresponding output gate of $C$.](../figure/serial_comp.png){#serialcompfig .class width=300px height=300px}

> # {.proof data-ref="seqcompositioncircthm"}
Let $C$ be the $n$-input $m$-output circuit computing $F$ and $D$ be the $m$-input $k$-output circuit computing $G$.
The circuit to compute $G \circ F$ is illustrated in [serialcompfig](){.ref}.
We simply "stack" $D$ after $C$, by obtaining a combined circuit with $n$ inputs and $|C|+|D|$ gates. The gates of $C$ remain the same, except that we identify the output gates of $C$ with the input gates of $D$. That is, for every edge that connected the $i$-th input of $D$ to a gate $v$ of $D$, we now connect to $v$ the output gate of $C$ corresponding to `y_`$\expr{i}$ instead.
After doing so, we remove the output labels from $C$ and keep only the outputs of $D$.
For every input $x$, if we execute the composed circuits on $x$ (i.e., compute a map $Z$ from the vertices to $\{0,1\}$ as per [NANDcirccomputedef](){.ref}), then the output gates of $C$ will get the values corresponding to $F(x)$ and hence the output gates of $D$ will have the value $G(F(x))$.


> # {.theorem title="Parallel composition, circuit versions" #parcompositioncircthm}
If $C,D$ are NAND circuits such that $C$ computes $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $D$ computes $G:\{0,1\}^{n'} \rightarrow \{0,1\}^{m'}$  then there is a circuit $E$ of size $|C|+|D|$ computing  the function $G\oplus F : \{0,1\}^{n+n'} \rightarrow \{0,1\}^{m+m'}$.

![Given a circuit $C$ computing $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and a circuit $D$ computing $G:\{0,1\}^{n'}\rightarrow \{0,1\}^{m'}$ we obtain a circuit $E$ computing $F \oplus G$ be simply putting the circuits "side by side", and renaming the labels of the inputs and outputs of $D$ to `x_`$n$,..,`x_`$n+n'-1$ and `y_`$m$,..,`y_`$m+m'-1$.](../figure/parallel_composition_circ.png){#parallelcompositioncircfig .class width=300px height=300px}


> # {.proof data-ref="parcompositioncircthm"}
If $C,D$ are circuits that compute $F,G$ then we can transform them to a circuit $E$ that computes $F \oplus G$ as in [parallelcompositioncircfig](){.ref}.
The circuit $E$ simply consists of two disjoint copies of the circuits $C$ and $D$, where we modify the labelling of the inputs of $D$ from `x_`$0$,$\ldots$,`x_`$n'-1$ to `x_`$n$,$\ldots$,`x_`$n+n'-1$ and the labelling of the outputs of $D$ from `y_`$0$,$\ldots$,`y_`$m'-1$ to `y_`$m$,$\ldots$,`y_`$m+m'-1$.
By the fact that $C$ and $D$ compute $F$ and $G$ respectively, we see that $E$ computes the function $F \oplus G: \{0,1\}^{n+n'}\rightarrow \{0,1\}^{m+m'}$ that on input $x \in \{0,1\}^{n+n'}$ outputs $F(x_0,\ldots,x_{n-1})G(x_n,\ldots,x_{n+n'-1})$.

> # { .pause }
While we proved [seqcompositionthm](){.ref} and [parcompositionthm](){.ref}  using the circuit formalism, it is also possible to directly give syntactic transformations of the code of programs computing $F$ and $G$ to programs computing $G\circ F$ and $F \oplus G$ respectively.
It is a good exercise for you to pause here and see that you know how to give such a transformation.
Try to think how you would write a _program_ (in the programming language of your choice) that given two strings `C` and `D` that contain the code of NAND programs for computing $F$ and $G$, would output a string `E` that contains that code of a NAND program for $G\circ F$ (or $F \oplus G$).


### Example: Adding two-bit numbers

Using composition, we can show how to add _two bit_ numbers.
That is, the function $ADD_2:\{0,1\}^4\rightarrow\{0,1\}^3$ that takes two numbers $x,x'$ each between $0$ and $3$ (each represented with two bits using the binary representation) and outputs their sum, which is a number between $0$ and $6$ that can be represented using three bits.
The gradeschool algorithm gives us a way to compute $ADD_2$ using $ADD_1$.
That is, we can add each digit using $ADD_1$ and then take care of the carry.
That is, if the two input numbers have the form $x_0+2x_1$ and $x_2+2x_3$, then the output number $y_0+y_12+y_32^2$ can be computed via the following "pseudocode" (see also [addtwofig](){.ref})

```
y_0,c_1   := ADD_1(x_0,x_2) // add least significant digits
z_1,c_2  := ADD_1(x_1,x_3) // add second digits
y_1,c'_2 := ADD_1(z_1,c_1) // second output is sum + carry
y_2       := c_2 OR c'_2    // top digit is 1 if one of the top carries is 1
```

![Adding two $2$-bit numbers via the gradschool algorithm.](../figure/add2.png){#addtwofig .class width=300px height=300px}

To transform this pseudocode into an actual program or circuit, we can use [seqcompositionthm](){.ref} and [parcompositionthm](){.ref}.
That is, we first compute $(y_0,c_1,z_1,c_2) = ADD_1 \oplus ADD_1 (x_0,x_2,x_1,x_3)$, which we can do in $10$ lines  via [parcompositionthm](){.ref}, then apply  $ADD_1$ to $(z_1,c_1)$, and finally use the fact that $OR(a,b)=NAND(NOT(a),NOT(b))$ and $NOT(a)=NAND(a,a)$ to compute `c_2 OR c'_2` via three lines of NAND.
The resulting code is the following:

~~~~ { .go .numberLines  }
// Add a pair of two-bit numbers
// Input: (x_0,x_1) and (x_2,x_3)
// Output: (y_0,y_1,y_2) representing the sum
// x_0 + 2x_1 + x_2 + 2x_3
//
// Operation:
// 1) y_0,c_1 := ADD_1(x_0,x_2):
// add the least significant digits
// c_1 is the "carry"
u   := x_0 NAND x_2
v   := x_0 NAND u
w   := x_2 NAND u
y_0 := v NAND w
c_1 := u NAND u
// 2) z'_1,z_1 := ADD_1(x_1,x_3):
// add second digits
u   := x_1 NAND x_3
v   := x_1 NAND u
w   := x_3 NAND u
z_1 := v NAND w
z'_1 := u NAND u
// 3) Take care of carry:
// 3a) y_1 = XOR(z_1,c_1)
u   := z_1 NAND c_1
v   := z_1 NAND u
w   := c_1 NAND u
y_1 := v   NAND w
// 3b) y_2 = z'_1 OR (z_1 AND c_1)
//  = NAND(NOT(z'_1), NAND(z_1,c_1))
u   := z'_1 NAND z'_1
v   := z_1 NAND c_1
y_2 := u NAND v
~~~~  

For example, the computation of the deep fact that $2+3=5$ corresponds to running this program on the inputs $(0,1,1,1)$ which will result in the following trace:

```
Executing step 1: "u   := x_0 NAND x_2"	 x_0 = 0, x_2 = 1, u   is assigned 1,
Executing step 2: "v   := x_0 NAND u"	 x_0 = 0, u   = 1, v   is assigned 1,
Executing step 3: "w   := x_2 NAND u"	 x_2 = 1, u   = 1, w   is assigned 0,
Executing step 4: "y_0 := v NAND w"	 v   = 1, w   = 0, y_0 is assigned 1,
Executing step 5: "c_1 := u NAND u"	 u   = 1, u   = 1, c_1 is assigned 0,
Executing step 6: "u   := x_1 NAND x_3"	 x_1 = 1, x_3 = 1, u   is assigned 0,
Executing step 7: "v   := x_1 NAND u"	 x_1 = 1, u   = 0, v   is assigned 1,
Executing step 8: "w   := x_3 NAND u"	 x_3 = 1, u   = 0, w   is assigned 1,
Executing step 9: "z_1 := v NAND w"	 v   = 1, w   = 1, z_1 is assigned 0,
Executing step 10: "z'_1 := u NAND u"	 u   = 0, u   = 0, z'_1 is assigned 1,
Executing step 11: "u   := z_1 NAND c_1"	 z_1 = 0, c_1 = 0, u   is assigned 1,
Executing step 12: "v   := z_1 NAND u"	 z_1 = 0, u   = 1, v   is assigned 1,
Executing step 13: "w   := c_1 NAND u"	 c_1 = 0, u   = 1, w   is assigned 1,
Executing step 14: "y_1 := v   NAND w"	 v   = 1, w   = 1, y_1 is assigned 0,
Executing step 15: "u   := z'_1 NAND z'_1"	 z'_1 = 1, z'_1 = 1, u   is assigned 0,
Executing step 16: "v   := z_1 NAND c_1"	 z_1 = 0, c_1 = 0, v   is assigned 1,
Executing step 17: "y_2 := u NAND v"	 u   = 0, v   = 1, y_2 is assigned 1,
Output is y_0=1, y_1=0, y_2=1
```

### Composition in NAND programs

We can generalize the above examples to handle not just sequential and parallel but all forms of _composition_.
That is, if we have an $s$ line program $P$ that computes the function $F$, and a $t$ line program $P'$ that can compute the function $G$ using $k$ calls to a "black box" for computing $F$, then we can obtain a $t + ks$ line program $P''$ to compute $G$ (without any "magic boxes") by replacing every call to $F$ in $P'$ with a copy of $P$ (while appropriately renaming the variables).
Similarly, in the circuit formulation, we can transform an $s$-gate circuit $C$ for computing $G$, and a $t$-gate "augmented circuit" $C'$ that can compute $F$ using  $k$ "magic gates" that compute $G$ instead of NAND, into a standard $s+tk$ gate circuit $C''$  that computes $F$, by replacing each gate with a copy of $C$.

![We can compose a program $P$ that computes $F$ with a program $P'$ that computes $G$ by making calls to $F$, to obtain a program $P''$ that computes $G$ without any calls.](../figure/composition.png){#composition-fig .class width=300px height=300px}



## Lecture summary

* We can define the notion of computing a function via a simplified "programming language", where computing a function $F$ in $T$ steps would correspond to having a $T$-line NAND program that computes $F$.

* An equivalent formulation is that a function is computable by a NAND program if it can be computed by a NAND circuit.




## Exercises

> # {.exercise  #exid}
Which of the following statements is false?
   a. There is a NAND program to add two $4$-bit numbers that has at most $100$ lines. \
   b. Every NAND program to add two $4$-bit numbers has  at most $100$ lines. \
   c. Every NAND program to  add two $4$-bit numbers  has least  $5$ lines. \



> # {.exercise  #exid}
Write a NAND program that adds two $3$-bit numbers.

> # {.exercise  #paritycircuitex}
Prove [paritycircuitthm](){.ref}.^[__Hint:__ Prove by induction that for every $n>1$ which is a power of two, $XOR_n \in SIZE(4(n-1))$. Then use this to prove the result for every $n$.]


## Bibliographical notes

The exact notion of  "NAND programs" we use is nonstandard, but these are equivalent to standard models in the literature  such as _straightline programs_ and _Boolean circuits_.

An historical review of calculating machines can be found in Chapter I of the 1946 ["operating manual" for the Harvard Mark I computer](http://www.boazbarak.org/cs121/MarkI_operMan_1946.pdf), written by Lieutenant Grace Murray Hopper and the staff of the Harvard Computation Laboratory.

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

(to be completed)

## Acknowledgements
