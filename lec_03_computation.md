# Defining computation

>_"there is no reason why mental as well as bodily labor should not be economized by the aid of machinery"_, Charles Babbage, 1852


>_"If, unwarned by my example, any man shall undertake and shall succeed in constructing an engine embodying in itself the whole of the executive department of mathematical analysis upon different principles or by simpler mechanical means, I have no fear of leaving my reputation in his charge, for he alone will be fully able to appreciate the nature of my efforts and the value of their results."_, Charles Babbage, 1864


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

We define the notion of computing a function by a NAND program in the natural way:

> # {.definition title="Computing a function" #computefuncNAND}
The _number of inputs_ in a NAND program $P$ is the largest number $n$ such that $P$ contains a variable of the form `x_`$\expr{n-1}$, and the _number of outputs_ is the largest number $m$ such that $P$ contains a variable of the form `y_`$\expr{m-1}$.
>
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$. A NAND program $P$ with $n$ inputs and $m$ outputs _computes $F$_ if for every $x\in \{0,1\}^n$, whenever $P$ is executed with the `x_`$\expr{i}$ variable initialized to $x_i$ for all $i\in [n]$, at the end of the execution the variable `y_`$\expr{j}$ will equal $y_j$ for all $j\in [m]$ where $y=F(x)$.
>
For every $L\in \N$, we define $SIZE(L)$ to be the set of all functions that are computable by a NAND program of at most $L$ lines.^[As mentioned in the appendix, we require that all output variables are assigned a value, and that the largest index used in an $L$ line NAND program is smaller than $L$, and so all functions in $SIZE(L)$ have at most $L$ inputs and $L$ outputs.]

> # { .pause }
Please pause here and verify why [computefuncNAND](){.ref} does indeed capture the natural notion of computing a function by a NAND program.

Let $XOR_n:\{0,1\}^n \rightarrow \{0,1\}$ be the function that maps $x\in \{0,1\}^n$ to $\sum_{i=0}^n x_i (\mod 2)$.
The NAND program we presented above yields a proof of the following theorem

> # {.theorem title="Computing XOR" #xortwothm}
$XOR_2 \in SIZE(4)$

Similarly, the addition program we presented shows that   $ADD_1 \in SIZE(5)$.

## Composing functions

Computing the XOR or addition of two bits is all well and good, but still seems a long way off from even the algorithms we all learned in elementary school, let alone [World of Warcraft](https://worldofwarcraft.com/en-us/).
We will get to computing more interesting functions, but for starters let us prove the following simple extension of [xortwothm](){.ref}

> # {.theorem title="Computing four bit parity" #xorfourthm}
$XOR_4 \in SIZE(12)$

We can prove [xorfourthm](){.ref} by explicitly writing down a 12 line program.
But writing NAND programs by hand can get real old real fast.
So, we will prove more general results about _composing_ functions:

> # {.theorem title="Sequential composition of functions" #seqcompositionthm}
If $F:\{0,1\}^n \rightarrow \{0,1\}^m$ is a function in $SIZE(L)$ and $G:\{0,1\}^m \rightarrow \{0,1\}^k$ is a function in $SIZE(L')$ then $G\circ F$ is a function in $SIZE(L+L')$, where $G\circ G:\{0,1\}^n \rightarrow \{0,1\}^k$ is the function that maps $x\in \{0,1\}^n$ to $G(F(x))$.


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
Note that the vertices of the form $(0,i)$ have  in-degree zero, and all edges of the form $\overright{(1,\ell')\;(1,\ell)}$ satisfy $\ell>\ell'$.
Hence this graph is a DAG, as in any cycle there would have to be at least on edge going from a vertex of the form $(1,\ell)$ to a vertex of the form $(1,\ell')$ for $\ell'<\ell$ (can you see why?).
Also, since we don't allow a variable of the form `y_`$\expr{j}$ on the right-hand side of a NAND operation, the output vertices have out-degree zero.
To complete the proof of this direction, we need to show that the circuit $C$ computes the same function as the program $P$.
Indeed, 






### Adding two-bit numbers

Let us now show how to compute addition of _two bit_ numbers.
That is, the function $ADD_2:\{0,1\}^4\rightarrow\{0,1\}^3$ that takes two numbers $x,x'$ each between $0$ and $3$ (each represented with two bits using the binary representation) and outputs their sum, which is a number between $0$ and $6$ that can be represented using three bits.
The gradeschool algorithm gives us a way to compute $ADD_2$ using $ADD_1$.
That is, we can add each digit using $ADD_1$ and then take care of the carry.
That is, if the two input numbers have the form $x_0+2x_1$ and $x_2+2x_3$, then the output number $y_0+y_12+y_32^2$ can be computed via the following "pseudocode" (see also [addtwofig](){.ref})

```
y_0,c_1   := ADD_1(x_0,x_2) // add least significant digits
z'_1,c_2  := ADD_1(x_1,x_3) // add second digits
y_1, c'_2 := ADD_1(z_1,c_1) // second output is sum + carry
y_3       := z'_1 OR c_2    // top digit is one if one of the top carries is
```

![Adding two $2$-bit numbers via the gradschool algorithm.](../figure/add2.png){#addtwofig .class width=300px height=300px}

The NAND programing language does not have a built-in way to define functions so we can reuse code, but we can still use the time-honored technique of "copy and paste" and simply copy the code for $ADD_1$ three times and the code for XOR once (while renaming the variables appropriately) to obtain the following NAND program for adding two bit numbers:

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

The above is a particular instance of the general notion of _composition_.
That is, if we have an $s$ line program $P$ that computes the function $F$, and a $t$ line program $P'$ that can compute the function $G$ using $k$ calls to a "black box" for computing $F$, then we can obtain a $t + ks$ line program $P''$ to compute $G$ (without any "magic boxes") by replacing every call to $F$ in $P'$ with a copy of $P$ (while appropriately renaming the variables).

![We can compose a program $P$ that computes $F$ with a program $P'$ that computes $G$ by making calls to $F$, to obtain a program $P''$ that computes $G$ without any calls.](../figure/composition.png){#composition-fig .class width=300px height=300px}


## "Syntactic sugar"

The NAND programing language is pretty "bare bones", but we can implement some "added features" on top of it.
That is, we can show how we can implement those features using the underlying mechanisms of the language.
For example, example  we can implement a variable assignment operation by transforming a code such as

```
foo := bar
```

into the valid NAND code:

```
notbar := bar    NAND bar
foo    := notbar NAND notbar
```

Thus in describing NAND programs we will allow ourselves to use the variable assignment operation, with the understanding that in actual programs we will replace every line of the first form with the two lines of the second form.
In programming language parlance this is known as "syntactic sugar", since we are not changing the definition of the language, but merely introducing some convenient notational shortcuts.^[This concept is also known as "macros" and is sometimes implemented via a preprocessor. Some text editors also give programmers the ability to use such shortcuts via mechanisms of macro languages or text snippets.]
We will use several such "syntactic sugar" constructs to make our descriptions of NAND programs shorter and simpler.
However, these descriptions are  merely shorthand for the equivalent standard or "sugar free" NAND program that is obtained after removing the use of all these constructs.
In particular, when we  say that a function $F$ has an $s$-line NAND program, we mean a standard NAND program, that does not use any syntactic sugar.
The website [http://www.nandpl.org](http://www.nandpl.org) contains an online "unsweetener" that can take a NAND program that uses  these features and modifies it to an equivalent program that does not use them.

In the rest of this section, we will list some additional examples of "syntactic sugar" transformations.
Going over all these examples can be somewhat tedious, but we do it for two reasons:

1. To convince you that despite its seeming simplicity and limitations, the NAND programming language is actually quite powerful and can capture many of the fancy programming constructs such as `if` statements and function definitions  that exists in more fashionable languages.

2. So you can realize how lucky you are to be  taking a theory of computation course and not a compilers course.. `:)`



### Constants

We can create variables `zero` and `one` that are have the values  $0$ and $1$ respectively by adding the lines

~~~~ { .go .numberLines }
notx_0 := x_0 NAND x_0
one    := x_0 NAND notx_0
zero   := one NAND one   
~~~~

Note that since for every $x\in \{0,1\}$, $NAND(x,\overline{x})=1$, the variable `one` will get the value $1$ regardless of the value of $x_0$, and the variable `zero` will get the value $NAND(1,1)=0$.^[We could have saved a couple of lines using the convention that uninitialized variables default to $0$, but it's always nice to be explicit.]
Hence we can replace code such as `a := 0` with `a := one NAND one` and similarly `b := 1` will be replaced with `b:= zero NAND zero`.


### Conditional statements

Another sorely missing feature in NAND is a conditional statement.
We would have liked to be able to write something like


~~~~ { .go .numberLines }
if (a) {
    ...
   some code here
   ...
}
~~~~

To ensure that there is code that will only be executed when the variable `a` is equal to $1$.
We can do so by replacing every variable `var` that is assigned a value in the code by a variable `tempvar` and then execute it normally.
After it is executed, we assign to every such variable the value `MUX(a,var,tempvar)` where $MUX:\{0,1\}^3 \rightarrow \{0,1\}$ is the _multiplexer_ function that on input $(a,b,c)$ outputs $b$ if $a=0$ and $c$ if $a=1$.
This function has a 4-line NAND program:

~~~~
nx_2 := x_2 NAND x_2
u    := x_0 NAND nx_2
v    := x_1 NAND x_2
y_0  := u   NAND v
~~~~

We leave it as [mux-ex](){.ref} to verify that this program does indeed compute the $MUX$ function.

### Functions / Macros

Another staple of almost any programming language is the ability to execute functions.
However, we can achieve the same effect as (non recursive) functions using  "copy pasting".
That is, we can replace code such as

~~~~ { .go .numberLines }
def a,b := Func(c,d) {
    function_code
}
...
e,f := Func(g,h)
~~~~

with

~~~~ { .go .numberLines }
...
function_code'
...
~~~~

where `function_code'` is obtained by replacing all occurrences of `a` with `e`,`f` with `b`, `c` with `g`, `d` with `h`.
When doing that we will need to  ensure that all other variables appearing in `function_code'` don't interfere with other variables by replacing every instance of a variable `foo` with `upfoo` where `up` is some unique prefix.

### Example:

Using these features, we can express the code of the  $ADD_2$ function a bit more succinctly as  

~~~~ { .go .numberLines  }
def c := AND(a,b) {
   notc := a NAND b
   c    := notc NAND c
}
def c := XOR(a,b) {
    u   := a NAND b
    v   := a NAND u
    w   := b NAND u
    c := v NAND w
}
y_0 := XOR(x_0,x_2) // add first digit
c_1 := AND(x_0,x_2)
z_1 := XOR(x_1,x_2) // add second digit
c_2 := AND(x_1,x_2)
y_1 := XOR(c_1,y_2) // add carry from before
c'_2 := AND(c_1,y_2)
y_2 := XOR(c'_2,x_2)
~~~~  

### More indices

As stated, the NAND programming language only allows for "one dimensional arrays", in the sense that we can use variables such as `foo_7` or `foo_29` but not `foo_{5,15}`.
However we can easily embed two dimensional arrays in one-dimensional ones using a one-to-one function $PAIR:\N^2 \rightarrow \N$.
(For example, we can use $PAIR(x,y)=2^x3^y$, but there are also more efficient embeddings, see [embedtuples-ex](){.ref}.)
Hence we can replace any  variable of the form `foo_{`$\expr{i}$`,`$\expr{j}$`}`  with `foo_`$\expr{PAIR(i,j)}$, and similarly for three dimensional arrays.


### Non-Boolean  variables, lists and integers

While the basic variables in NAND++ are Boolean (only have $0$ or $1$), we can easily extend this to other objects using encodings.
For example, we can encode the alphabet $\{$`a`,`b`,`c`,`d`,`e`,`f` $\}$ using three bits as $000,001,010,011,100,101$.
Hence, given such an encoding, we could  use the code

~~~~ { .go .numberLines }
foo := "b"
~~~~

 would be a shorthand for the program  

~~~~ { .go .numberLines }
foo_0   := 0
foo_1  := 0
foo_2 := 1
~~~~

Using our notion of multi-indexed arrays, we can also use code such as

~~~~ { .go .numberLines }
foo  := "be"
~~~~

as a shorthand for

~~~~ { .go .numberLines }
foo_{0,0}  := 0
foo_{0,1}  := 0
foo_{0,2}  := 1
foo_{1,0}  := 1
foo_{1,1}  := 0
foo_{1,2}  := 0
~~~~

which can then in turn be mapped to standard NAND code using a one-to-one embedding $pair: \N \times \N \rightarrow \N$ as above.

^[TODO: possibly add an exercise using this with the alphabet including `[`,`]`,`,` to encode lists.]


### Storing integers

We can also handle non-finite alphabets, such as integers, by using some prefix-free encoding and encoding the integer in an array.
To store non-negative integers, we will use the convention that `01` stands for $0$, `11` stands for $1$, and `00`
is the end marker.
To store integers that could be potentially negative we will use the convention that `10` in the first coordinate stands for the negative sign.^[TODO: I am not sure that this representation is the best or most convenient convention. Not sure it matters much though.]

So,  code such as

~~~~ { .go .numberLines }
foo := 5  // (1,0,1) in binary
~~~~

will be shorthand for

~~~~ { .go .numberLines }
foo_0   := 1   
foo_1  := 1
foo_2  := 0
foo_3  := 1
foo_4 := 1
foo_5  := 1
foo_6  := 0
foo_7  := 0
~~~~

while

~~~~ { .go .numberLines }
foo := -5   
~~~~

will be the same as

~~~~ { .go .numberLines }
foo_0   := 1
foo_1  := 0
foo_2   := 1   
foo_3  := 1
foo_4   := 0
foo_5  := 1
foo_6  := 1
foo_7  := 1
foo_8  := 0
foo_9  := 0
~~~~

Using multidimensional arrays, we can use arrays of integers and hence replace code such as

~~~~ { .go .numberLines }
 foo := [12,7,19,33]
~~~~

with the equivalent NAND expressions.


For integer valued variables, we can use the standard algorithms of addition, multiplication, comparisons etc.. to   write code such as


~~~~ { .go .numberLines }
j := k + l
if (m*n>k) {
    code...
}
~~~~

which then gets translated into standard NAND++ program by copy pasting these algorithms.




## Adding and multiplying $n$ bit numbers

We have seen how to add one and two bit numbers.
We can use the gradeschool algorithm to show that NAND programs can add $n$-bit numbers for every $n$:

> # {.theorem title="Addition using NAND programs" #addition-thm}
For every $n$, let $ADD_n:\{0,1\}^{2n}\rightarrow \{0,1\}^{n+1}$ be the function that, given $x,x'\in \{0,1\}^n$ computes the representation of the sum of the numbers that $x$ and $x'$ represent. Then there is a NAND program that computes the function $ADD_n$. Moreover, the number of lines in this program is smaller than $100n$.

![Translating the gradeschool addition algorithm into a NAND program. If at the $i^{th}$ stage, the $i^{th}$  digits of the two numbers are $x_i$ and $x_{n+i}$ and the carry is $c_i$, then the $i^{th}$ digit of the sum will be $(x_i XOR x_{n+i}) XOR c_i$ and the new carry $c_{i+1}$ will be equal to $1$ if any two values among $c_i,x_i,x_{n+i}$ are $1$.](../figure/addition-alg-nand.png){#addition-fig .class width=300px height=300px}



> # {.proof data-ref="addition-thm"}
To prove this theorem we repeatedly appeal to the notion of composition, and to the "gradeschool" algorithm for addition.
To add the numbers $(x_0,\ldots,x_{n-1})$ and $(x_n,\ldots,x_{2n-1})$, we set $c_0=0$ and  do the following for $i=0,\ldots,n-1$: \
  >* Compute $z_i  = XOR(x_i,x_{n+i})$ (add the two corresponding digits) \
  >* Compute $y_i = XOR(z_i,c_i)$ (add in the carry to get the final digit) \
  >* Compute $c_{i+1} = ATLEASTTWO(x_i,x_{n+i},c_i)$ where $ATLEASTTWO:\{0,1\}^3 \rightarrow \{0,1\}$ is the function that maps $(a,b,c)$ to $1$ if $a+b+c \geq 2$. (The new carry is $1$ if and only if at least two of the values $x_i,x_{n+i},y_i$ were equal to $1$.)
The most significant digit $y_n$ of the output will of course be the last carry $c_n$.
>
To transform this algorithm to a NAND program we just need to plug in the program for XOR, and use the observation (see [atleasttwo-ex](){.ref}) that
$$
\begin{split}
ATLEASTTWO(a,b,c)  &=  (a \wedge b) \vee (a \wedge c) \vee (b \wedge c)  \\
  &= NAND(NOT(NAND(NAND(a,b),NAND(a,c))),NAND(b,c))
\end{split}
$$
>
We leave accounting for the number of lines, and verifying that it is smaller than $100n$, as an exercise to the reader.



See the website [http://nandpl.org](http://nandpl.org) for an applet that produces, given $n$, a  NAND program that computes $ADD_n$.^[TODO: maybe add the example of the code of $ADD_4$? (using syntactic sugar)]

### Multiplying numbers


Once we have addition, we can use the gradeschool algorithm to obtain multiplication as well, thus obtaining the following theorem:


> # {.theorem title="Multiplication NAND programs" #theoremid}
 For every $n$, let $MULT_n:\{0,1\}^{2n}\rightarrow \{0,1\}^{2n}$ be the function that, given $x,x'\in \{0,1\}^n$ computes the representation of the product of the numbers that $x$ and $x'$ represent. Then there is a NAND program that computes the function $MULT_n$. Moreover, the number of lines in this program is smaller than $1000n^2$.

We omit the proof, though in [multiplication-ex](){.ref} we ask you to supply a "constructive proof" in the form of a program (in your favorite programming language) that on input a number $n$, outputs the code of a NAND program of at most $1000n^2$ lines that computes the $MULT_n$ function.
In fact, we can use Karatsuba's algorithm to show that there is a NAND program of $O(n^{\log_2 3})$ lines to compute $MULT_n$ (and one can even get further asymptotic improvements using the newer algorithms).


## Functions beyond arithmetic

We have seen that NAND programs can add and multiply numbers.  But can they compute other type of functions, that have nothing to do with arithmetic?
Here is one example:


> # {.definition title="Lookup function" #lookup-def}
For every $k$, the _lookup_ function $LOOKUP_k: \{0,1\}^{2^k+k}\rightarrow \{0,1\}$ is defined as follows:
For every $x\in\{0,1\}^{2^k}$ and $i\in \{0,1\}^k$,  
$$
LOOKUP_k(x,i)=x_i
$$
where $x_i$ denotes the $i^{th}$ entry of $x$, using the binary representation to identify $i$ with a number in $\{0,\ldots,2^k - 1 \}$.

The function $LOOKUP_1: \{0,1\}^3 \rightarrow \{0,1\}$ maps $(x_0,x_1,i) \in \{0,1\}^3$ to $x_i$.
It is actually the same as the $MUX$ function we have seen above, that has a 4 line NAND program.
However, can we compute higher levels of $LOOKUP$?
This turns out to be the case:

> # {.theorem title="Lookup function" #lookup-thm}
 For every $k$, there is a NAND program that computes the function $LOOKUP_k: \{0,1\}^{2^k+k}\rightarrow \{0,1\}$. Moreover, the number of lines in this program is at most  $4\cdot 2^k$.

### Constructing a NAND program for $LOOKUP$

We now prove [lookup-thm](){.ref}.
We will do so by induction.
That is, we show how to use a NAND program for computing $LOOKUP_k$ to compute $LOOKUP_{k+1}$.
Let us first see how we do this for $LOOKUP_2$.
Given input $x=(x_0,x_1,x_2,x_3)$ and an index $i=(i_0,i_1)$, if the most significant bit $i_1$ of the index  is $0$ then $LOOKUP_2(x,i)$ will equal $x_0$ if $i_0=0$ and equal $x_1$ if $i_0=1$.
Similarly, if the most significant bit $i_1$ is $1$ then $LOOKUP_2(x,i)$ will equal $x_2$ if $i_0=0$ and will equal $x_3$ if $i_0=1$.
Another way to say this is that
$$
LOOKUP_2(x_0,x_1,x_2,x_3,i_0,i_1) = LOOKUP_1(LOOKUP_1(x_0,x_1,i_0),LOOKUP_1(x_2,x_3,i_0),i_1)
$$
That is, we can compute $LOOKUP_2$ using three invocations of $LOOKUP_1$.
The "pseudocode" for this program will be

~~~~ { .go .numberLines }
z_0 := LOOKUP_1(x_0,x_1,x_4)
z_1 := LOOKUP_1(x_2,x_3,x_4)
y_0 := LOOKUP_1(z_0,z_1,x_5)
~~~~
(Note that since we call this function with $(x_0,x_1,x_2,x_3,i_0,i_1)$, the inputs `x_4` and `x_5` correspond to  $i_0$ and $i_1$.)
We can obtain  an actual "sugar free" NAND program of at most $12$ lines  by replacing the calls to `LOOKUP_1` by an appropriate copy of the program above.

We can generalize this to compute $LOOKUP_3$ using two invocations of $LOOKUP_2$ and one invocation of $LOOKUP_1$. That is, given input $x=(x_0,\ldots,x_7)$ and $i=(i_0,i_1,i_2)$ for $LOOKUP_3$, if the most significant bit of the index $i_2$ is $0$, then the output of $LOOKUP_3$ will equal $LOOKUP_2(x_0,x_1,x_2,x_3,i_0,i_1)$, while if this index $i_2$ is $1$ then the output will be $LOOKUP_2(x_4,x_5,x_6,x_7,i_0,i_1)$, meaning that the following pseudocode can compute $LOOKUP_3$,

~~~~ { .go .numberLines }
z_0 := LOOKUP_2(x_0,x_1,x_2,x_3,x_8,x_9)
z_1 := LOOKUP_2(x_4,x_5,x_6,x_7,x_8,x_9)
y_0 := LOOKUP_1(z_0,z_1,x_10)
~~~~

where again we can replace the calls to `LOOKUP_2` and `LOOKUP_1` by invocations of the process above.


Formally, we can prove the following lemma:

> # {.lemma title="Lookup recursion" #lookup-rec-lem}
For every $k \geq 2$, $LOOKUP_k(x_0,\ldots,x_{2^k-1},i_0,\ldots,i_{k-1})$
is equal to
$$
LOOKUP_1(LOOKUP_{k-1}(x_0,\ldots,x_{2^{k-1}-1},i_0,\ldots,i_{k-2}), LOOKUP_{k-1}(x_{2^{k-1}},\ldots,x_{2^k-1},i_0,\ldots,i_{k-2}),i_{k-1})
$$

> # {.proof data-ref="lookup-rec-lem"}
If the most significant bit $i_{k-1}$  of $i$ is zero, then the index $i$ is in $\{0,\ldots,2^{k-1}-1\}$ and hence we can perform the lookup on the "first half" of $x$ and  the result of  $LOOKUP_k(x,i)$ will be the same as $a=LOOKUP_{k-1}(x_0,\ldots,x_{2^{k-1}-1},i_0,\ldots,i_{k-1})$.
On the other hand, if this most significant bit $i_{k-1}$  is equal to $1$, then the index is in $\{2^{k-1},\ldots,2^k-1\}$, in which case the result of $LOOKUP_k(x,i)$ is the same as $b=LOOKUP_{k-1}(x_{2^{k-1}},\ldots,x_{2^k-1},i_0,\ldots,i_{k-1})$.
Thus we can compute $LOOKUP_k(x,i)$ by first computing $a$ and $b$ and then outputting $LOOKUP_1(a,b,i_{k-1})$.

[lookup-rec-lem](){.ref} directly implies [lookup-thm](){.ref}.
We prove by induction on $k$ that there is a NAND program of at most $4\cdot 2^k$ lines for $LOOKUP_k$.
For $k=1$ this follows by the  four line program for $LOOKUP_1$ we've seen before.
For $k>1$, we use the following pseudocode

~~~~ { .go .numberLines }
a = LOOKUP_(k-1)(x_0,...,x_(2^(k-1)-1),i_0,...,i_(k-2))
b = LOOKUP_(k-1)(x_(2^(k-1)),...,x_(2^(k-1),i_0,...,i_(k-2))
y_0 = LOOKUP_1(a,b,i_{k-1})
~~~~

If we let $L(k)$ be the number of lines required for $LOOKUP_k$, then the above shows that
$$
L(k) \leq 2L(k-1)+4 \;. \label{induction-lookup}
$$
We will prove by induction that $L(k) \leq 4(2^k-1)$.
This is true for $k=1$ by our construction.
For $k>1$, using the inductive hypothesis and [induction-lookup](){.eqref},
we get that
$$
L(k) \leq 2\cdot 4 \cdot (2^{k-1}-1)+4= 4\cdot 2^k - 8 + 4 = 4(2^k-1)
$$
completing the proof of [lookup-thm](){.ref}.

## Computing _every_ function

At this point we know the following facts about NAND programs:

1. They can compute at least some non trivial functions.
2. Coming up with NAND programs for various functions is a very tedious task.

Thus I would not blame the reader if they were not particularly looking forward to a long sequence of examples of functions that can be computed by NAND programs.
However, it turns out we are not going to need this, as we can show in one fell swoop that NAND programs can compute _every_ finite function:

> # {.theorem title="Universality of NAND" #NAND-univ-thm}
For every $n,m$ and function $F: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a NAND program that computes the function $F$. Moreover, there is such a program with at most $O(m 2^n)$ lines.

The implicit constant in the $O(\cdot)$ notation can be shown to be at most $10$.
We also note that the bound of [NAND-univ-thm](){.ref} can be improved to $O(m 2^n/n)$, see
[tight-upper-bound](){.ref}.

### Proof of NAND's Universality

To prove [NAND-univ-thm](){.ref}, we need to give a NAND program  for _every_ possible function.
We will restrict our attention to the case of Boolean functions (i.e., $m=1$).
In [mult-bit-ex](){.ref} you will show how to extend the proof for all values of $m$.
A function $F: \{0,1\}^n\rightarrow \{0,1\}$ can be specified by a table of  its values for each one of the $2^n$ inputs.
Here is for example one particular function $G: \{0,1\}^4 \rightarrow \{0,1\}$:^[In case you are curious, this is the function that computes the digits of $\pi$ in the binary basis.]


| Input  | Output |
|--------|--------|
| $0000$ | 1      |
| $0001$ | 1      |
| $0010$ | 0      |
| $0011$ | 0      |
| $0100$ | 1      |
| $0101$ | 0      |
| $0110$ | 0      |
| $0111$ | 1      |
| $1000$ | 0      |
| $1001$ | 0      |
| $1010$ | 0      |
| $1011$ | 0      |
| $1100$ | 1      |
| $1101$ | 1      |
| $1110$ | 1      |
| $1111$ | 1      |


 \



We can see that for every $x\in \{0,1\}^4$, $G(x)=LOOKUP_4(1100100100001111,x)$.
Therefore the following is NAND "pseudocode" to compute $G$:



~~~~ { .go .numberLines }
G0000 := 1
G0001 := 1
G0010 := 0
G0011 := 0
G0100 := 1
G0101 := 0
G0110 := 0
G0111 := 1
G1000 := 0
G1001 := 0
G1010 := 0
G1011 := 0
G1100 := 1
G1101 := 1
G1110 := 1
G1111 := 1
y_0 := LOOKUP(G0000,G0001,G0010,G0011,G0100,G0101,G0110,G0111,
             G1000,G1001,G1010,G1011,G1100,G1101,G1111,x_0,x_1,x_2,x_3)   
~~~~

Recall that we can translate this pseudocode into an actual NAND program by adding three lines to define variables `zero` and `one` that are initialized to $0$ and $1$ repsectively, and then  replacing a statement such as `Gxxx := 0` with `Gxxx := one NAND one` and a statement such as `Gxxx := 1` with `Gxxx := zero NAND zero`.
The call to `LOOKUP` will be replaced by the NAND program that computes $LOOKUP_4$, but we will replace the variables `i_0`,$\ldots$,`i_3` in this program with `x_0`,$\ldots$,`x_3` and the variables `x_0`,$\ldots$,`x_15` with `G000`, $\ldots$, `G1111`.

There was nothing about the above reasoning that was particular to this program. Given every function $F: \{0,1\}^n \rightarrow \{0,1\}$, we can write a NAND program that does the following:

1. Initialize $2^n$ variables of the form `F00...0` till `F11...1` so that for every $z\in\{0,1\}^n$,  the variable corresponding to $z$ is assigned the value $F(z)$.

2. Compute $LOOKUP_n$ on the $2^n$ variables initialized in the previous step, with the index variable being the input variables `x_`$\expr{0}$,...,`x_`$\expr{2^n-1}$. That is, just like in the pseudocode for `G` above, we use `y_0 := LOOKUP(F00..00,F00...01,...,F11..1,x_0,..,x_`$\expr{2^n-1}$`)`

The total number of lines in the program will be $2^n$ plus the $4\cdot 2^n$ lines that we pay for computing $LOOKUP_n$.
This completes the proof of [NAND-univ-thm](){.ref}.

The [NAND programming language website](http://nandpl.org) allows you to construct a NAND program for an arbitrary function.


> # {.remark title="Advanced note: improving  by a factor of $n$" #tight-upper-bound}
By being a little more careful, we can improve the bound of [NAND-univ-thm](){.ref} and show that every function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a NAND program of at most $O(m 2^n/n)$ lines.
As before, it is enough to prove the case that $m=1$.
>
The idea is to use the technique known as _memoization_.
Let $k= \log(n-2\log n)$ (the reasoning behind this choice will become clear later on).
For every $a \in \{0,1\}^{n-k}$ we define $F_a:\{0,1\}^k \rightarrow \{0,1\}$ to be the function that maps $w_0,\ldots,w_{k-1}$ to $F(a_0,\ldots,a_{n-k-1},w_0,\ldots,w_{k-1})$.
On input $x=x_0,\ldots,x_{n-1}$, we can compute $F(x)$ as follows:
First we  compute a $2^{n-k}$ long string $P$ whose $a^{th}$ entry (identifying $\{0,1\}^{n-k}$ with $[2^{n-k}]$ equals $F_a(x_{n-k},\ldots,x_{n-1})$.
One can verify that $F(x)=LOOKUP_{n-k}(P,x_0,\ldots,x_{n-k})$.
Since we can compute $LOOKUP_{n-k}$ using $O(2^{n-k})$ lines, if we can compute the string $P$ (i.e., compute variables `P_`$\expr{0}$, ..., `P_`$\expr{2^{n-k}-1}$) using $T$ lines, then we can compute $F$ in $O(2^{n-k})+T$ lines.
The trivial way to compute the string $P$ would by to use $O(2^k)$ lines to compute for every $a$ the map $x_0,\ldots,x_{k-1} \mapsto F_a(x_0,\ldots,x_{k-1})$ as in the proof of [NAND-univ-thm](){.ref}.
Since there are $2^{n-k}$ $a$'s,  that would be a total cost of $O(2^{n-k} \cdot 2^k) = O(2^n)$ which would not improve at all on the bound of [NAND-univ-thm](){.ref}.
However, a more careful observation shows that we are making some _redundant_ computations.
After all, there are only $2^{2^k}$ distinct functions mapping $k$ bits to one bit.
If $a$ and $a'$ satisfy that $F_a = F_{a'}$ then we don't need to spend $2^k$ lines computing both $F_a(x)$ and $F_{a'}(x)$ but rather can only compute the variable `P_`$\expr{a}$ and then copy `P_`$\expr{a}$ to `P_`$\expr{a'}$ using $O(1)$ lines.
Since we have $2^{2^k}$ unique functions, we can bound the total cost to compute $P$ by $O(2^{2^k}2^k)+O(2^{n-k})$.
Now it just becomes a matter of calculation.
By our choice of $k$, $2^k = n-2\log n$ and hence $2^{2^k}=\tfrac{2^n}{n^2}$.
Since $n/2 \leq 2^k \leq n$, we can bound the total cost of computing $F(x)$ (including also the additional $O(2^{n-k})$ cost of computing $LOOKUP_{n-k}$) by $O(\tfrac{2^n}{n^2}\cdot n)+O(2^n/n)$, which is what we wanted to prove.




>__Discussion:__ In retrospect, it is perhaps not surprising that every finite function can be computed with a NAND program. A finite function $F: \{0,1\}^n \rightarrow \{0,1\}^m$ can be represented by simply the list of its  outputs for each one of the $2^n$ input values.
So it makes sense that we could write a NAND program of similar size to compute it.
What is more interesting is that  _some_ functions, such as addition and multiplication,  have a much more efficient representation: one that only requires $O(n^2)$ or even smaller number of lines.

## The class $SIZE_{n,m}(T)$

For every $n,m,T \in \N$, we denote by $SIZE_{n,m}(T)$, the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$ that can be computed by NAND programs  of at most $T$ lines.
[NAND-univ-thm](){.ref} shows that  $SIZE_{n,m}(4 m 2^n)$ is the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$.
The results we've seen before can be phrased as showing  that $ADD_n \in SIZE_{2n,n+1}(100 n)$
and $MULT_n \in SIZE_{2n,2n}(10000 n^{\log_2 3})$.^[TODO: check constants]



## Lecture summary

* We can define the notion of computing a function via a simplified "programming language", where computing a function $F$ in $T$ steps would correspond to having a $T$-line NAND program that computes $F$.
* While the NAND programming only has one operation, other operations such as functions and conditional execution can be implemented using it.   
* Every function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a NAND program of at most $O(m 2^n)$ lines (and in fact at most $O(m 2^n/n)$ lines).
* Sometimes (or maybe always?) we can translate an _efficient_ algorithm to compute $F$ into a NAND program that computes $F$  with a  number of lines comparable to the number of steps in this algorithm.



## Exercises

> # {.exercise  #exid}
Which of the following statements is false?
   a. There is a NAND program to add two $4$-bit numbers that has at most $100$ lines.
   b. Every NAND program to add two $4$-bit numbers has  at most $100$ lines.
   c. Every NAND program to  add two $4$-bit numbers  has least  $5$ lines.

> # {.exercise title="Composition" #composition-ex}
Suppose that $F:\{0,1\}^n \rightarrow \{0,1\}^n$ can be computed by a NAND program of at most $s$ lines and $F':\{0,1\}^n \rightarrow \{0,1\}^n$ can be computed by a NAND program of at most $s'$ lines. Prove that the function $G:\{0,1\}^n \rightarrow \{0,1\}^n$ defined as $G(x)=F'(F(x))$ can be computed by a NAND program of at most $s+s'$ lines.

> # {.exercise title="Pairing" #embedtuples-ex}
1. Prove that the map $F(x,y)=2^x3^y$ is a one-to-one map from $\N^2$ to $\N$. \
2. Show that there is a one-to-one map $F:\N^2 \rightarrow \N$ such that for every $x,y$, $F(x,y) \leq 100\cdot \max\{x,y\}^2$. \
3. For every $k$, show that there is  a one-to-one map $F:\N^k \rightarrow \N$ such that for every $x_0,\ldots,x_{k-1}$, $F(x_0,\ldots,x_{k-1}) \leq 100 \cdot \max\{x_0,\ldots,x_{k-1}\}^k$.


> # {.exercise title="Computing MUX" #mux-ex}
Prove that the NAND program below computes the function $MUX$ (or $LOOKUP_1$) where $MUX(a,b,c)$ equals $a$ if $c=0$ and equals $b$ if $c=1$:

~~~~
nx_2 := x_2 NAND x_2
u    := x_0 NAND nx_2
v    := x_1 NAND x_2
y_0  := u   NAND v
~~~~


> # {.exercise title="At least two" #atleasttwo-ex}
Give a NAND program of at most 6 lines to compute  $ATLEASTTWO:\{0,1\}^3 \rightarrow \{0,1\}$
where $ATLEASTTWO(a,b,c) = 1$ iff $a+b+c \geq 2$.

> # {.exercise title="Conditional statements" #conditional-statements}
In this exercise we will show that even though the NAND programming language does not have an `if .. then .. else ..` statement, we can still implement it.
Suppose that there is an $s$-line NAND program to compute $F:\{0,1\}^n \rightarrow \{0,1\}$ and an $s'$-line NAND program to compute $F':\{0,1\}^n \rightarrow \{0,1\}$.
Prove that there is a program of at most $s+s'+10$ lines to compute the function $G:\{0,1\}^{n+1} \rightarrow \{0,1\}$ where $G(x_0,\ldots,x_{n-1},x_n)$ equals $F(x_0,\ldots,x_{n-1})$ if $x_n=0$ and equals $F'(x_0,\ldots,x_{n-1})$ otherwise.



> # {.exercise  #exid}
Write a NAND program that adds two $3$-bit numbers.

> # {.exercise  #paritycircuitex}
Prove [paritycircuitthm](){.ref}.^[__Hint:__ Prove by induction that for every $n>1$ which is a power of two, $XOR_n \in SIZE(4(n-1))$. Then use this to prove the result for every $n$.]

> # {.exercise title="Addition" #addition-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND program that computes $ADD_n$. Can you ensure that the program it outputs for $ADD_n$ has fewer than $10n$ lines?

> # {.exercise title="Multiplication" #multiplication-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND program that computes $MULT_n$. Can you ensure that the program it outputs for $MULT_n$ has fewer than $1000\cdot n^2$ lines?

> # {.exercise title="Efficient multiplication (challenge)" #eff-multiplication-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND program that computes $MULT_n$ and has at most $10000 n^{1.9}$ lines.^[__Hint:__ Use Karatsuba's algorithm] What is the smallest number of lines you can use to multiply two 64 bit numbers?


> # {.exercise title="Multibit function" #mult-bit-ex}
 Prove that \
a. If there is an $s$-line NAND program to compute $F:\{0,1\}^n \rightarrow \{0,1\}$ and an $s'$-line NAND program to compute $F':\{0,1\}^n \rightarrow \{0,1\}$ then there is an $s+s'$-line program to compute the function $G:\{0,1\}^n \rightarrow \{0,1\}^2$ such that $G(x)=(F(x),F'(x))$. \
b. For every function $F:\{0,1\}^n \rightarrow \{0,1\}^m$, there is a NAND program of at most $10m\cdot 2^n$ lines that computes $F$.


## Bibliographical notes

The exact notion of  "NAND programs" we use is nonstandard, but these are equivalent to standard models in the literature  such as _straightline programs_ and _Boolean circuits_.

An historical review of calculating machines can be found in Chapter I of the 1946 ["operating manual" for the Harvard Mark I computer](http://www.boazbarak.org/cs121/MarkI_operMan_1946.pdf), written by Lieutenant Grace Murray Hopper and the staff of the Harvard Computation Laboratory.

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

(to be completed)

## Acknowledgements
