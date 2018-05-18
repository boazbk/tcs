# Code as data, data as code

> # { .objectives }
* Understand one of the most important concepts in computing: duality between code and data. \
* Build up comfort in moving between different representations of programs. \
* Follow the construction of a "universal NAND program" that can evaluate other NAND programs given their representation. \
* See and understand the  proof of a major result that compliments the result last lecture: some functions require an _exponential_ number of NAND lines to compute.
* Understand the _physical extended Church-Turing thesis_ that NAND programs capture _all_ feasible computation in the physical world, and its physical and philosophical implications.



>_"The term code script is, of course, too narrow. The chromosomal structures are at the same time instrumental in bringing about the development they foreshadow. They are law-code and executive power - or, to use another simile, they are architect’s plan and builder’s craft - in one."_ ,  Erwin Schrödinger, 1944.

>_"The importance of the universal machine is clear. We do not need to have an infinity of different machines doing different jobs. ... The engineering problem of producing various machines for various jobs is replaced by the office work of 'programming' the universal machine"_, Alan Turing, 1948



A NAND program can be thought of as simply a sequence of symbols, each of which can be encoded with zeros and ones using (for example) the ASCII standard.
Thus we can represent every NAND program as a binary string.
This statement seems obvious but it is actually quite profound.
It means that we can treat a NAND program both as instructions to carrying computation and also as _data_ that could potentially be input to other computations.


This correspondence between _code_ and _data_ is one of the most fundamental aspects of computing.
It  underlies  the notion of _general purpose_ computers, that are not pre-wired to compute only one task, and it is also the basis of our  hope for obtaining _general_ artificial intelligence.
This concept finds immense use in all areas of computing, from scripting languages to machine learning, but it is fair to say that we haven't yet fully mastered it.
Indeed many security exploits involve cases such as "buffer overflows" when attackers manage to inject code where the system expected only "passive" data (see [XKCDmomexploitsfig](){.ref}).
The idea of code as data reaches beyond the realm of electronic computers.
For example, DNA can be thought of as both a program and data (in the words of Schrödinger, who wrote  before DNA's discovery a book that inspired Watson and Crick, it is both "architect's plan and builder's craft").

![As illustrated in this xkcd cartoon, many exploits, including buffer overflow, SQL injections, and more, utilize the blurry line between "active programs" and "static strings".](../figure/exploits_of_a_mom.png){#XKCDmomexploitsfig .class width=300px height=300px}


## A NAND interpreter in NAND

For every NAND program $P$, we can represent $P$ as a binary string.
In particular, this means that for any choice of such representation, the following is a well defined mathematical function
$EVAL:\{0,1\}^* \times \{0,1\}^* \rightarrow \{0,1\}^*$

$$
EVAL(P,x) = \begin{cases} P(x) & |x|= \text{no. of $P$'s inputs} \\ 0 & \text{otherwise} \end{cases}
$$
where we denote by $P(x)$ the output of the program represented by the string $P$ on the input $x$.

> # { .pause }
The above is one of those observations that are simultaneously both simple and profound. Please make sure that you understand __(1)__ how for every fixed choice of representing programs as strings, the function $EVAL$ above is well defined, and __(2)__ what this function actually does.


$EVAL$ takes strings arbitrarily of length, and hence cannot be computed by a NAND program, that has a fixed length of inputs.
However, one of the most interesting consequences of the fact that we can represent programs as strings is the following theorem:

> # {.theorem title="Bounded Universality of NAND programs" #bounded-univ}
For every $S,n,m \in \N$ there is a NAND program that computes the  function
$$
EVAL_{S,n,m}:\{0,1\}^{S+n} \rightarrow \{0,1\}^m
$$
defined as follows: For every string $(P,x)$ where $P \in \{0,1\}^S$ and $x\in\{0,1\}^n$, if $P$ describes a NAND program with $n$ input bits and $m$ outputs bits, then   $EVAL_{S,n,m}(P,x)$ is the output of this program on input $x$.^[If $P$ does not describe a program then we don't care what $EVAL_{S,n,m}(P,x)$ is, but for concreteness we will set it to be $0^m$. Note that in this theorem's statement we use $S$ to denote the number of bits describing the program, rather than the number of lines in it. However, these two quantities are very closely related.]


Of course to fully specify $EVAL_{S,n,m}$, we need to fix a precise representation scheme  for NAND programs as binary strings.
We can simply use the ASCII representation, though  we will use a  more convenient representation.
But regardless of the choice of representation,
[bounded-univ](){.ref} is an immediate corollary of [NAND-univ-thm](){.ref}, which states that _every_ finite function, and so in particular the function $EVAL_{S,n,m}$ above, can be computed by _some_ NAND program.

> # { .pause }
Once again, [bounded-univ](){.ref}  is subtle but important. Make sure you understand what this thorem means, and why it is a corollary of [NAND-univ-thm](){.ref}.

[bounded-univ](){.ref} can be thought of as providing  a "NAND interpreter in NAND".
That is, for a particular size bound, we give a _single_ NAND program that can evaluate all NAND programs of that size.
We call this  NAND program $U$ that computes $EVAL_{S,n,m}$ a _bounded universal program_.
"Universal" stands for the fact that this is a _single program_ that can evaluate _arbitrary_ code,  where "bounded" stands for the fact that  $U$ only evaluates programs of bounded size.
Of course this limitation is inherent for the NAND programming language where an $N$-line program can never compute a function with more than $N$ inputs.
(We will later on introduce the concept of _loops_, that  allows  to escape this limitation.)


It turns out that we don't even need to pay that much of an overhead for universality

> # {.theorem title="Efficient bounded universality of NAND programs" #eff-bounded-univ}
For every $S,n,m \in \N$ there is a NAND program of at most $O(S^2)$ lines that computes the  function
$EVAL_{S,n,m}:\{0,1\}^{S+n} \rightarrow \{0,1\}^m$ defined above.

Unlike [bounded-univ](){.ref}, [eff-bounded-univ](){.ref} is not a trivial corollary of the fact that every function can be computed, and  takes much more effort to prove.
It requires us to present a concrete NAND program for the $EVAL_{S,n,m}$ function.
We will do so in several stages.

1. First, we will spell out precisely how to  represent NAND programs as strings.
We can prove  [eff-bounded-univ](){.ref}  using the ASCII representation, but a "cleaner" representation will be more convenient for us.

2. Then, we will show how we can write a  program to compute $EVAL_{S,n,m}$ in _Python_.^[We will not use much about Python, and a reader that has familiarity with programming in any language should be able to follow along.]

3. Finally, we will show how we can transform this Python program into a NAND program.

### Concrete representation for NAND programs

![In the Harvard Mark I computer, a program was represented as a list of triples of numbers, which were then encoded by perforating holes in a control card.](../figure/tapemarkI.png){#figureid .class width=300px height=300px}


A NAND program is simply a sequence of lines of the form

```python
blah = NAND(baz,boo)
```

There is of course nothing special about these particular identifiers. Hence to represent a NAND program mathematically, we can simply identify the variables with natural numbers, and think of each line as a triple $(i,j,k)$ which corresponds to saying that we assign to the $i$-th variable  the NAND of the values of the $j$-th and $k$-th variables.
We will use the set $[t]= \{0,1,\ldots,t-1\}$ as our set of variables, and for concreteness we will let the input variables be the first $n$ numbers, and the output variables be the last $m$ numbers (i.e., the numbers $(t-m,\dots,t-1)$).
This motivates the following definition:

> # {.definition title="List of tuples representation" #nandtuplesdef}
Let $P$ be a NAND program of $n$ inputs, $m$ outputs, and $s$ lines, and let $t$ be the number of distinct variables used by $P$.
The _list of tuples representation of $P$_ is the triple $(n,m,L)$ where $L$ is a list of triples of the form $(i,j,k)$ for $i,j,k \in [t]$.
>
For every variable  of $P$, we assign a number in $[t]$ as follows:
>
* For every $i\in [n]$, the variable `X[`$i$`]` is assigned the number $i$. \
* For every $j\in [m]$, the variable `Y[`$j$`]` is assigned the number $t-m+j$. \
* Every other variable is assigned a number in $\{n,n+1,\ldots,t-m-1\}$ in the order of which it appears.

The list of tuples representation will be our default choice for representing NAND programs, and since "list of tuples representation" is a bit of a mouthful, we will often call this simply the  _representation_ for a program $P$.

> # {.example title="Representing the XOR program" #representXOR}
Our favorite NAND program, the XOR program:
>
`u = NAND(X[0],X[1])` \
`v = NAND(X[0],u)` \
`w = NAND(X[1],u)` \
`Y[0] = NAND(v,w)`
>
Is represented as the tuple $(2,1,L)$ where $L=((2, 0, 1), (3, 0, 2), (4, 1, 2), (5, 3, 4))$. That is, the variables `X[0]` and `X[1]` are given the indices  $0$ and $1$ respectively, the variables `u`,`v`,`w` are given the indices $2,3,4$ respectively, and the variable `Y[0]` is given the index $5$.



\iffalse

```python
%run "../code/NAND programming language.ipynb"
```

```python
def XOR(a,b):
    u = NAND(a,b)
    v = NAND(a,u)
    w = NAND(b,u)
    return  NAND(v,w)

nandrepresent(XOR)
```
\fi

Transforming a NAND program from its representation as code to the representation as a list of tuples is a fairly straightforward programming exercise, and in particular can be done in a few lines of _Python_.^[If you're curious what these 15 lines are, see the appendix.]
Note that this representation loses information such as the particular names we used for the variables, but this is OK since these names do not make a difference to the functionality of the program.

### Representing a program as a string

To obtain a representation that we can use as input to a NAND program, we need to take a step further and map the triple $(n,m,L)$ to a binary string.
Here there are many different choices, but let us fix one of them.
If the list $L$ has $s$ triples in it, we will represent it as simply the string $str(L)$ which will be the concatenation of the $3s$ numbers in the binary basis, which can be encoded as a string of length $3s\ell$ where $\ell = \ceil{\log 3s}$ is a number of bits that is guaranteed to be sufficient to  represent numbers in $[t]$ (since $t \leq 3s$).
We will represent the program $(n,m,L)$ as the string $\expr{n}\expr{m}\expr{s}str(L)$ where $\expr{n}$  and $\expr{m}$ are some  prefix free representations of $n$,  $m$ and $s$ (see [prefixfreesec](){.ref}).

In the context of computing $EVAL_{S,n,m}$ the number of lines, inputs, and outputs, is fixed, and so we can drop $n,m,s$ and simply think of it as a function that maps $\{0,1\}^{3s\ell + n}$ to $\{0,1\}^m$, where $\ell  = \ceil{\log 3s}$, and $s$ is the number of lines in programs whose representation has length $S$.
Note that $S = \Theta(s \log s)$.

Since the number $s$ of lines is easier to keep track of than the number of bits of representation, from now on we will consider the function $EVAL'_{s,n,m}:\{0,1\}^{3s\ceil{\log 3s}+n} \rightarrow \{0,1\}^m$
such that
$$EVAL'_{s,n,m}(str(L)x) = P(x) \label{evalprimeeq}
$$
where $P$ is the program represented by $(n,m,L)$.
That is $EVAL'_{s,n,m}$  maps the string $str(L)$ representing an $s$ line program $P$ on $n$ input and $m$ outputs, and the string $x\in \{0,1\}^n$, to the output $P(x)$.
To prove  [eff-bounded-univ](){.ref} we need to
show an $O((s \log s)^2)$ line NAND program to compute $EVAL'_{s,n,m}$, which would correspond to an $O(S^2)$ line program to compute $EVAL_{S,n,m}$.^[The numbers $n$ and $m$ of inputs and outputs are always smaller than $s$.]






### A NAND interpeter in "pseudocode"

To prove [eff-bounded-univ](){.ref} it suffices  to give a NAND program of $O(s^2 \log s) \leq  O((s\log s)^2)$ lines that can evaluate NAND programs of $s$ lines.
Let us start by thinking how we would evaluate such programs  if we weren't restricted to the NAND operations.
That is, let us describe informally an _algorithm_ that on input $n,m,s$, a list of triples $L$, and a string $x\in \{0,1\}^n$, evaluates the program represented by $(n,m,L)$ on the string $x$.

> # { .pause }
It would be highly worthwhile for you to stop here and try to solve this problem yourself.
For example, you can try thinking how you would write a program `NANDEVAL(n,m,s,L,x)` that compues this function in the programming language of your choice.

Here is a description of such an algorithm:

__Input:__ Numbers $n,m$ and a list $L$ of $s$ triples  of numbers in $[t]$ for some $t\leq 3s$, as well as a string $x\in \{0,1\}^n$.

__Goal:__ Evaluate the program represented by $(n,m,L)$ on the input $x\in \{0,1\}^n$.

__Operation:__

1. We will create a _dictionary_ data structure `Vartable` that for every $i \in [t]$ stores a bit. We will assume we have the operations `GET(Vartable,i)` which restore the bit corresponding to `i`, and the operation `UPDATE(Vartable,i,b)` which update the bit corresponding to `i` with the value `b`. (More concretely, we will write this as `Vartable = UPDATE(Vartable,i,b)` to emphasize the fact that the state of the data structure changes, and to keep our convention of using functions free of "side effects".)

2. We will initialize the table by setting the $i$-th value of `Vartable`  to $x_i$ for every $i\in [n]$.

3. We will go over the list $L$ in order, and for every triple  $(i,j,k)$ in $L$, we let $a$ be `GET(Vartable,`$j$`)`, $b$ be `GET(Vartable`$k$`)`, and then set the value corresponding to $i$ to the NAND of $a$ and $b$. That is, let `Vartable = UPDATE(Vartable,`$i$,`NAND(`$a$`,`$b$`))`.

4. Finally, we output the value `GET(Vartable,`$t-m+j$`)` for every $j\in [m]$.


> # { .pause }
Please make sure you understand this algorithm and why it does produce the right value.

### A NAND interpreter in Python

To make things more concrete, let us see how we implement the above algorithm in the _Python_ programming language.
We will construct a function `NANDEVAL` that  on input $n,m,L,x$  will output the result of evaluating the program represented by $(n,m,L)$ on $x$.^[To keep things simple, we will not worry about the case that $L$ does not represent a valid program of $n$ inputs and $m$ outputs. Also, there is nothing special about Python. We could have easily presented a corresponding function in JavaScript, C, OCaml, or any other programming language.]
(We will compute the value $s$ to be the size of $L$ and the value $t$ to be the maximum number appearing in $L$ plus one.)

```python
def NANDEVAL(n,m,L,X):
    # Evaluate a NAND program from its list of triple representation.
    s = len(L) # number of lines
    t = max(max(a,b,c) for (a,b,c) in L)+1 # maximum index in L + 1

    Vartable = [0] * t # we'll simply use an array to store data

    def GET(V,i): return V[i]
    def UPDATE(V,i,b):
        V[i]=b
        return V

    # load input values to Vartable:
    for i in range(n): Vartable = UPDATE(Vartable,i,X[i])

    # Run the program
    for (i,j,k) in L:
        a = GET(Vartable,j)
        b = GET(Vartable,k)
        c = NAND(a,b)
        Vartable = UPDATE(Vartable,i,c)

    # Return outputs Vartable[t-m], Vartable[t-m+1],....,Vartable[t-1]
    return [GET(Vartable,t-m+j) for j in range(m)]

# Test on XOR (2 inputs, 1 output)
L = ((2, 0, 1), (3, 0, 2), (4, 1, 2), (5, 3, 4))
print(NANDEVAL(2,1,L,(0,1))) # XOR(0,1)
# [1]
print(NANDEVAL(2,1,L,(1,1))) # XOR(1,1)
# [0]
```


Accessing an  element  of the array `Vartable` at a given index takes a constant number of basic operations.
Hence (since $n,m \leq s$ and $t \leq 3s$),  the program above will use  $O(s)$ basic operations.^[Python does not distinguish between lists and arrays, but allows constant time random access to an indexed elements to both of them. One could argue that if we allowed programs of truly unbounded length (e.g., larger than $2^{64}$) then the price  would not be constant but logarithmic in the length of the array/lists, but the difference between $O(s)$ and $O(s \log s)$ will not be important for our discussions.]

### A NAND interpreter in NAND

We now turn to describing the proof of  [eff-bounded-univ](){.ref}.
To do this, it is of course not enough to give a Python program.
Rather, we need to show  how we compute the $EVAL'_{s,n,m}$ function of [evalprimeeq](){.eqref} by a NAND program.
In other words, our job is to transform, for every $s,n,m$, the Python code above to a NAND program $U_{s,n,m}$ that  computes the function $EVAL'_{s,n,m}$.

> # { .pause }
Before reading further, try to think how _you_ could give a "constructive proof" of [eff-bounded-univ](){.ref}.
That is, think of how you would write, in the programming language of your choice, a function `universal(s,n,m)` that on input $s,n,m$ outputs the code for the NAND program $U_{s,n,m}$ such that $U_{s,n,m}$ computes $EVAL_{S,n,m}$.
Note that there is a subtle but crucial difference between this function and the Python `NANDEVAL` program described above.
Rather than actually evaluating a given program $P$ on some input $w$, the function `universal` should output the _code_ of a NAND program that computes the map $(P,x) \mapsto P(x)$.

Our construction will follow very closely the Python implementation of `EVAL` above.
We will use variables `Vartable[`$0$`]`,$\ldots$,`Vartable[`$2^\ell-1$`]`, where $\ell = \ceil{\log 3s}$ to store our variables.
However, NAND doesn't have integer-valued variables, so we cannot write code such as
`Vartable[i]` for some variable `i`.
However, we _can_ implement the function `GET(Vartable,i)` that outputs the `i`-th bit of the array `Vartable`.
Indeed, this is nothing by the function `LOOKUP` that we have seen in [lookup-thm](){.ref}!

> # { .pause }
Please make sure that you understand why `GET` and `LOOKUP` are the same function.

We saw that we can compute `LOOKUP` on arrays of size $2^\ell$ in time $O(2^\ell)$, which will be $O(s)$ for our choice of $\ell$.

To compute the `update` function on input `V`,`i`,`b`, we need to scan the array `V`, and for  $j \in [2^\ell]$, have our $j$-th output be `V[`$j$`]` unless $j$ is equal to `i`, in which case the $j$-th output is `b`.
We can do this as follows:

1. For every $j\in [2^\ell]$, there is an $O(\ell)$ line NAND program to compute the function $EQ_j: \{0,1\}^\ell \rightarrow \{0,1\}$ that on input $i$ outputs $1$ if and only if $i$ is equal to (the binary representation of) $j$. (We leave verifying this as [equals](){.ref} and [equalstwo](){.ref}.)

2. We have seen that we can compute the function $IF:\{0,1\}^3 \rightarrow \{0,1\}$ such that $IF(a,b,c)$ equals $b$ if $a=1$ and $c$ if $a=0$.

Together, this means that we can compute `UPDATE` as follows:

```python
def UPDATE(V,i,b):
    # update a 2**ell length array at location i to the value b

    for j in range(2**ell):
        a = EQUALS(j,i)
        Y[j] = IF(a,b,V[j])

    return Y
```

Once we can compute `GET` and `UPDATE`, the rest of the implementation amounts to "book keeping" that needs to be done carefully, but is not too insightful.
Hence we omit these details from this chapter.
See the appendix for the full details of how to compute the universal NAND evaluator in NAND.



> # {.remark title="Improving to quasilinear overhead (advanced optional note)" #quasilinearevalrem}
The NAND program above is less efficient that its Python counterpart, since NAND does not offer arrays with efficient random access. Hence for example the `LOOKUP` operation on an array of $s$ bits takes $\Omega(s)$ lines in NAND even though it takes $O(1)$ steps (or maybe $O(\log s)$ steps, depending how we count) in _Python_.
>
It turns out that it is  possible to improve the bound of [eff-bounded-univ](){.ref}, and  evaluate $s$ line NAND programs using a NAND program of  $O(s \log s)$ lines.
The key is to consider the description of NAND programs as circuits, and in particular as directed acyclic graphs (DAGs) of bounded in degree.
A universal NAND program $U_s$ for $s$ line programs  will correspond to a _universal graph_ $H_s$ for such $s$ vertex DAGs.
We can think of such as graph $U_s$ as fixed "wiring" for communication network, that should be able to accommodate any arbitrary pattern of communication between $s$ vertices (where this pattern corresponds to an $s$ line NAND program).
It turns out that there exist such efficient [routing networks](https://goo.gl/NnkkjM) exist  that allow embedding any $s$ vertex circuit inside a universal graph of size $O(s \log s)$, see [this recent paper](https://eprint.iacr.org/2016/017) for more on this issue.




##  A Python interpreter in NAND

To prove [eff-bounded-univ](){.ref} we essentially translated every line of the Python program for `EVAL` into an equivalent NAND snippet.
It turns out that none of our reasoning  was specific to the  particular function $EVAL$.
It is possible to translate _every_ Python program into an equivalent `NAND` program of comparable efficiency.^[More concretely, if the Python program takes $T(n)$ operations on inputs of length at most $n$ then we can find a NAND program of $O(T(n) \log T(n))$ lines that agrees with the Python program on inputs of length $n$.]
Actually doing so requires taking care of many details and is beyond the scope of this course, but let me convince you why you should believe it is possible in principle.
We can use [CPython](https://en.wikipedia.org/wiki/CPython) (the reference implementation for Python), to evaluate every Python program using a `C` program.
We can combine this with a C compiler to transform a Python program to various flavors of "machine language".


So, to transform a Python program into an equivalent NAND program, it is enough to show how to transform a machine language program into an equivalent NAND program.
One minimalistic (and hence convenient) family of machine languages is known as the _ARM architecture_ which powers a great many mobile devices including essentially all Android devices.^[ARM stands for "Advanced RISC Machine" where RISC in turn stands for "Reduced instruction set computer".]
There are even simpler machine languages, such as the [LEG acrhitecture](https://github.com/frasercrmck/llvm-leg) for which a  backend for the [LLVM compiler](http://llvm.org/) was implemented (and hence can be the target of compiling any of [large and growing list](https://en.wikipedia.org/wiki/LLVM#Front_ends) of languages that this compiler supports).
Other examples include the  [TinyRAM](http://www.scipr-lab.org/doc/TinyRAM-spec-0.991.pdf) architecture (motivated by  interactive proof systems that we will discuss much later in this course) and  the teaching-oriented [Ridiculously Simple Computer](https://www.ece.umd.edu/~blj/RiSC/) architecture.^[The reverse direction of compiling NAND to C code, is much easier. We show code for a `NAND2C` function in the appendix.]

Going one by one over the instruction sets of such computers and translating them to NAND snippets is no  fun, but it is a feasible thing to do.
In fact, ultimately this is very similar to the transformation that takes place in converting our high level code to actual silicon gates that (as we will see in the next lecture) are not so different from the operations of a NAND program.
Indeed, tools such as [MyHDL](http://www.myhdl.org/) that transform "Python to Silicon" can be used to convert a Python program to a NAND program.

The NAND programming language is just a teaching tool, and by no means do I suggest that writing NAND programs, or compilers to NAND, is a practical, useful, or even enjoyable activity.
What I do want is to make sure you understand why it _can_ be done, and to have the confidence that if your life (or at least your grade in this course) depended on it, then you would be able to do this.
Understanding how programs in high level languages such as Python are eventually transformed into concrete low-level representation such as NAND is fundamental to computer science.

The astute reader might notice that the above paragraphs only outlined why it should be possible to find for every _particular_ Python-computable function $F$, a _particular_ comparably efficient NAND program $P$ that computes $F$.
But this still seems to fall short of our goal of writing a "Python interpreter in NAND" which would mean  that for every parameter $n$, we come up with a _single_ NAND program $UNIV_n$ such that given a description of a Python program $P$, a particular input $x$, and a bound $T$ on the number of operations (where the length of $P$, $x$ and the magnitude of $T$ are all at most $n$) would return the result of executing $P$ on $x$ for at most $T$ steps.
After all, the transformation above would transform every Python program into a different NAND program, but would not yield "one NAND program to rule them all" that can evaluate every Python program up to some given complexity.
However, it turns out that it is enough to show such a transformation for a single Python program.
The reason is that we can write a Python interpreter _in Python_: a Python program $U$ that takes a bit string, interprets it as Python code, and then runs that code.
Hence, we only need to show a NAND program $U^*$ that computes the same function as the particular Python program $U$, and this will give us a way to evaluate _all_ Python programs.

What we are seeing time and again is the notion of _universality_ or _self reference_ of computation, which is the sense that all reasonably rich models of computation are expressive enough that they can "simulate themselves".
The importance of this phenomena to both the theory and practice of computing, as well as far beyond it, including the foundations of mathematics and basic questions in science, cannot be overstated.



## Counting programs, and lower bounds on the size of NAND programs

One of the consequences of our representation is the following:

> # {.theorem title="Counting programs" #program-count}
$$|Size(s)| \leq 2^{O(s \log s)}.$$
That is, there are at most $2^{O(s\log s)}$ functions computed by  NAND programs of at most $s$ lines.

Moreover, the implicit constant in the $O(\cdot)$ notation in [program-count](){.ref} is at most $10$.^[By this we mean that for all sufficiently large $s$, $|Size(s)|\leq 2^{10s\log s}$.]

> # {.proofidea data-ref="program-count"}
The idea behind the proof is that we can represent every $s$ line program by a binary string of  $O(s \log s)$ bits.
Therefore the  number of functions  computed by $s$-line programs cannot be larger than the number of such strings, which is $2^{O(s \log s)}$.
In the actual proof, given below, we  count the number of representations a little more carefully, talking directly about triples rather than binary strings, although the idea remains the same.


> # {.proof data-ref="program-count"}
Every NAND program $P$ with $s$ lines has at most $3s$ variables.
Hence, using our canonical representation, $P$ can be represented by the numbers $n,m$ of $P$'s inputs and outputs, as well as by the list $L$ of $s$ triples of natural numbers, each of which is smaller or equal to $3s$.
>
If two programs compute distinct functions then they have distinct representations.
So we will simply count the number of such representations: for every $s' \leq s$, the number of $s'$-long lists of triples of numbers in $[3s]$ is $(3s)^{3s'}$, which in particular is smaller than $(3s)^{3s}$.
So, for every $s' \leq s$ and $n,m$, the total number of representations of $s'$-line programs with $n$ inputs and $m$ outputs is smaller than $(3s)^{3s}$.
>
Since a program of at most $s$ lines has at most $s$ inputs and outputs, the total number of representations of all programs of at most $s$ lines is smaller than
$$
s\times s \times s \times (3s)^{3s} = (3s)^{3s+3} \label{eqcountbound}
$$
(the factor $s\times s\ times s$ arises from taking all of the at most $s$ options for the number of inputs $n$, all of the at most $s$ options for the number of outputs $m$, and all of the at most $s$ options for the number of lines $s'$).
We claim that for $s$ large enough, the righthand side of [eqcountbound](){.eqref} (and hence the total number of representations of programs of at most $s$ lines) is smaller than $2^{4 s \log s}$.
Indeed, we can write $3s = 2^{\log(3s)}=2^{\log 3  + \log s} \leq 2^{2+\log s}$, and hence the righthand side of [eqcountbound](){.eqref} is at most $\left(2^{2+ \log s}\right)^{3s+3} = 2^{(2+\log s)(3s+3)} \leq 2^{4s\log s}$ for $s$ large enough.
>
For every function $F \in Size(s)$ there is a program $P$ of at most $s$ lines that computes it, and we can map $F$ to its representation as a tuple $(n,m,L)$.
If $F \neq F'$ then a program $P$ that computes $F$ must have an input on which it disagrees with any program $P'$ that computes $F'$, and hence in particular $P$ and $P'$ have distinct representations.
Thus we see that the map of $Size(s)$ to its representation is one to one, and so in particular $|Size(s)|$ is at most the number of distinct representations which is it at most $2^{4s\log s}$.

> # {.remark title="Counting by ASCII representation" #countingfromascii}
We can also establish [program-count](){.ref} directly from the ASCII representation of the source code.  Since an $s$-line NAND program has at most $3s$ distinct variables,  we can change all the workspace variables of such a program to have the form `work_`$\expr{i}$ for $i$ between $0$ and $3s-1$ without changing the function that it computes. This means that  after removing comments and extra whitespaces, every line of such a program (which will  the form `var := var' NAND var''` for variable identifiers which will be either `x_###`,`y_###` or `work_###` where `###` is some number smaller than $3s$) will require at most, say, $20 + 3\log_{10} (3s) \leq O(\log s)$ characters. Since each one of those characters can be encoded using seven bits in the ASCII representation, we see that the number of functions computed by $s$-line NAND programs is at most $2^{O(s \log s)}$.


A function mapping $\{0,1\}^2$ to $\{0,1\}$ can be identified with the table of its four values on the inputs $00,01,10,11$;
a function mapping $\{0,1\}^3$ to $\{0,1\}$ can be identified with the table of its eight values on the inputs $000,001,010,011,100,101,110,111$.
More generally, every function $F:\{0,1\}^n \rightarrow \{0,1\}$ can be identified with the table of its  $2^n$  values  on the inputs $\{0,1\}^n$.
Hence the number of functions mapping $\{0,1\}^n$ to $\{0,1\}$ is equal to the number of such tables which (since we can choose either $0$ or $1$ for every row) is exactly $2^{2^n}$. Note that this is _double exponential_ in $n$, and hence even for small values of $n$ (e.g., $n=10$) the number of functions from $\{0,1\}^n$ to $\{0,1\}$ is truly astronomical.^["Astronomical" here is an understatement: there are much fewer than $2^{2^{10}}$ stars, or even particles, in the observable universe.]
This has the following interesting corollary:

> # {.theorem title="Counting argument lower bound" #counting-lb}
There is a function $F:\{0,1\}^n\rightarrow \{0,1\}$ such that the  shortest NAND program to compute $F$ requires $2^n/(100n)$ lines.

> # {.proof data-ref="counting-lb"}
Suppose, towards the sake of contradiction, that every function $F:\{0,1\}^n\rightarrow\{0,1\}$ can be computed by a NAND program of at most $s=2^n/(100n)$ lines.
Then the by [program-count](){.ref} the total number of such functions would be at most $2^{10s\log s} \leq 2^{10 \log s \cdot 2^n/(100 n)}$.
Since $\log s = n - \log (100 n) \leq n$ this means that the total number of such functions would be at most $2^{2^n/10}$, contradicting the fact that there are $2^{2^n}$ of them.

We have seen before that _every_ function mapping $\{0,1\}^n$ to $\{0,1\}$ can be computed by an  $O(2^n /n)$ line program.
We now see that this is  tight in the sense that some functions do require such an astronomical number of lines to compute.
In fact, as we explore in the exercises below, this is the case for _most_ functions.
Hence  functions that can be computed in a small number of lines (such as addition, multiplication, finding short paths in graphs, or even the $EVAL$ function) are the exception, rather than the rule.

![All functions mapping $n$ bits to $m$ bits can be computed by NAND programs of $O(m 2^n/n)$ lines, but most
functions cannot be computed using much smaller programs. However there are many important exceptions which are functions such as addition, multiplication, program evaluation, and many others, that can be computed in polynomial time with a small exponent.](../figure/map_of_size.png){#size-bounds-fig .class width=300px height=300px}

> # {.remark title="Advanced note: more efficient representation" #efficientrepresentation}
The list of triples is not the shortest representation for NAND programs.
As we will see in the next lecture, every NAND program of $s$ lines and $n$ inputs can be represented by a directed graph of $s+n$ vertices, of which $n$ have in-degree zero, and the $s$ others have in-degree at most two. Using the adjacency list representation, such a graph can be represented using roughly $2s\log(s+n) \leq 2s (\log s + O(1))$ bits.
Using this representation we can reduce the implicit constant in [program-count](){.ref} arbitrarily close to $2$.



## The physical extended Church-Turing thesis

We've seen that  NAND gates can be implemented using very different systems in the physical world.
What about the reverse direction?
Can NAND programs simulate any physical computer?


We can take a leap of faith and stipulate that NAND programs do actually encapsulate _every_ computation that we can think of.
Such a statement (in the realm of infinite functions, which we'll encounter in a couple of lectures) is typically attributed to Alonzo Church and Alan Turing, and in that context is  known as the _Church Turing Thesis_.
As we will discuss in future lectures, the Church-Turing Thesis is not a mathematical theorem or conjecture.
Rather, like theories in physics, the Church-Turing Thesis is about mathematically modelling the real world.
In the context of finite functions, we can make the following informal hypothesis or prediction:

>_If a function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed in the physical world using $s$ amount of "physical resources" then it can be computed by a NAND program of roughly $s$ lines._

We call this hypothesis the **"Physical Extended Church-Turing Thesis"** or _PECTT_ for short.
A priori it might seem rather extreme to hypothesize that our meager NAND model captures all possible physical computation.
But yet, in more than a century of computing technologies, no one has yet built any  scalable computing device that challenges this hypothesis.

We now  discuss  the "fine print" of the PECTT in more detail, as well as the (so far unsuccessful) challenges that have been raised against it.
There is no single universally-agreed-upon formalization of "roughly $s$ physical resources",  but
we can approximate this notion by considering the size of any  physical computing device and the time it takes to compute the output, and ask that  any such device can be simulated by a NAND program with a number of lines that is a polynomial (with not too large exponent) in the size of the system and the time it takes it to operate.


In other words, we can phrase the PECTT as stipulating that any function that can be computed by a device of volume $V$ and time $t$, must be computable by a NAND program that has at most $\alpha(Vt)^\beta$ lines for some constants $\alpha,\beta$.
The exact values for $\alpha,\beta$ are not so clear, but it is generally accepted that if $F:\{0,1\}^n \rightarrow \{0,1\}$ is an _exponentially hard_ function, in the sense that it has no NAND program of fewer than, say, $2^{n/2}$ lines, then a demonstration of a physical device that can compute $F$ for moderate input lengths (e.g., $n=500$) would be a violation of the PECTT.


> # {.remark title="Advanced note: making PECTT concrete" #concretepectt}
We can attempt at a more exact phrasing of the PECTT as follows.
Suppose that $Z$ is a physical system that accepts $n$ binary stimuli and has a binary output, and can be enclosed in a sphere of volume $V$.
We say that the system $Z$ _computes_ a function $F:\{0,1\}^n \rightarrow \{0,1\}$ within $t$ seconds if whenever we set the stimuli to some value  $x\in \{0,1\}^n$,  if we measure the output after $t$ seconds then we obtain $F(x)$.
>
We can phrase the PECTT as stipulating  that if there exists such a system $Z$ that  computes $F$ within $t$ seconds, then  there exists  a NAND program that computes $F$ and has at most $\alpha(Vt)^2$ lines, where $\alpha$ is some normalization constant.^[We can also consider variants where we use [surface area](https://goo.gl/ALgbVS) instead of volume, or take $(Vt)$ to a  different power than $2$.  However, none of these choices makes a qualitative difference  to the discussion below.]
In particular, suppose that $F:\{0,1\}^n \rightarrow \{0,1\}$ is a function that requires $2^n/(100n)>2^{0.8n}$ lines for any NAND program (such a function exists by [counting-lb](){.ref}).
Then the PECTT would imply that either the volume or the time of a system that computes $F$ will have to be at least $2^{0.2 n}/\sqrt{\alpha}$.
Since this quantity grows _exponentially_ in $n$, it is not hard to set parameters so that even for moderately large values of $n$, such a system could not fit in our universe.
>
To fully make the PECTT  concrete, we need to decide on the units for measuring time and volume, and the normalization constant $\alpha$.
One  conservative choice is to assume that we could squeeze computation to the absolute physical limits (which are many orders of magnitude beyond current technology).
This corresponds to setting $\alpha=1$ and using the [Planck units](https://goo.gl/gkpmBF) for volume and time.
The _Planck length_ $\ell_P$ (which is, roughly speaking, the shortest distance that can theoretically be measured) is roughly $2^{-120}$ meters.
The _Planck time_ $t_P$ (which is the time it takes for light to travel one Planck length) is about $2^{-150}$ seconds.
In the above setting, if a function $F$ takes, say, 1KB of input (e.g., roughly $10^4$ bits, which can encode a $100$ by $100$ bitmap image), and requires at least $2^{0.8 n}= 2^{0.8 \cdot 10^4}$ NAND lines to compute, then any physical system that computes it would require either volume of $2^{0.2\cdot  10^4}$ Planck length cubed, which is more than $2^{1500}$ meters cubed or take at least $2^{0.2 \cdot 10^4}$ Planck Time units, which is larger than $2^{1500}$ seconds.
To get a sense of how big that number is, note that the universe is only about $2^{60}$ seconds old, and its observable radius is only roughly $2^{90}$ meters.
The above discussion suggests that it is possible to _empirically falsify_ the PECTT by presenting a smaller-than-universe-size system that computes such a function.^[There are of course several hurdles to refuting the PECTT in this way, one of which is that we can't actually test the system on all possible inputs. However,  it turns out that we can get around this issue using notions such as  _interactive proofs_ and _program checking_ that we might encounter later in this book. Another, perhaps more salient problem, is that while we know many hard functions exist, at the moment there is _no single explicit function_ $F:\{0,1\}^n \rightarrow \{0,1\}$ for which we can _prove_ an $\omega(n)$ (let alone  $\Omega(2^n/n)$) lower bound  on the number of lines that a NAND program needs to compute it.]

### Attempts at refuting  the PECTT

One of the admirable traits of mankind is the refusal to accept limitations.
In the best case this is manifested by people achieving longstanding "impossible" challenges such as heavier-than-air flight, putting a person on the moon, circumnavigating the globe, or even resolving [Fermat's Last Theorem](https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem).
In the worst case it is manifested by people continually following the footsteps of previous failures to try to do proven-impossible tasks such as build a [perpetual motion machine](https://en.wikipedia.org/wiki/Perpetual_motion), [trisect an angle](https://en.wikipedia.org/wiki/Angle_trisection) with a compass and straightedge, or refute [Bell's inequality](https://en.wikipedia.org/wiki/Bell%27s_theorem).
The Physical Extended Church Turing thesis (in its various forms) has attracted both types of people.
Here are some physical devices that have been speculated to  achieve computational tasks that cannot be done by not-too-large  NAND programs:

* **Spaghetti sort:** One of the first lower bounds that Computer Science students encounter is that sorting $n$ numbers requires making $\Omega(n \log n)$ comparisons. The "spaghetti sort" is a description of a proposed "mechanical computer" that would do this faster. The idea is that to sort $n$ numbers $x_1,\ldots,x_n$, we could cut $n$ spaghetti noodles into lengths $x_1,\ldots,x_n$, and then if we simply hold them together in our hand and bring them down to a flat surface, they will emerge in sorted order. There are a great many reasons why this is not truly a challenge to the PECTT hypothesis, and I will not ruin the reader's fun in finding them out by her or himself.

* **Soap bubbles:** One function $F:\{0,1\}^n \rightarrow \{0,1\}$ that is conjectured to require a large number of NAND lines to solve is the _Euclidean Steiner Tree_ problem. This is the problem where one is given $m$ points in the plane $(x_1,y_1),\ldots,(x_m,y_m)$ (say with integer coordinates ranging from $1$ till $m$, and hence the list can be represented as a string of $n=O(m \log m)$ size) and some number $K$.  The goal is to figure out whether it is possible to connect all the points by line segments of total length at most $K$. This function is conjectured to be hard because it is _NP complete_ - a concept that we'll encounter later in this course - and it is in fact reasonable to conjecture that as $m$ grows, the number of NAND lines required to compute this function grows _exponentially_ in $m$, meaning that the PECTT would predict that if $m$ is sufficiently large (such as few hundreds or so) then no physical device could compute $F$.
Yet, some people claimed that there is in fact a very simple physical device that could solve this problem, that can be constructed using some wooden pegs and soap. The idea is that if we take two glass plates, and put $m$ wooden pegs between them in the locations $(x_1,y_1),\ldots,(x_m,y_m)$ then bubbles will form whose edges touch those pegs in the way that will minimize the total energy which turns out to be a function of the total length of the line segments.
The problem with this device of course is that nature, just like people, often gets stuck in "local optima". That is, the resulting configuration will not be one that achieves the  absolute minimum of the total energy but rather one that can't be improved with local changes.
[Aaronson](http://www.scottaaronson.com/papers/npcomplete.pdf) has carried out actual experiments (see [aaronsonsoapfig](){.ref}), and  saw that while this device often is successful for three or four pegs, it starts yielding suboptimal results once the number of pegs grows beyond that.

![Scott Aaronson [tests](http://www.scottaaronson.com/blog/?p=266) a candidate device for computing Steiner trees using soap bubbles.](../figure/aaronsonsoapbubble.jpg){#aaronsonsoapfig .class width=300px height=300px}

* **DNA computing.** People have suggested using the properties of DNA to do hard computational problems. The main advantage of DNA is the ability to potentially encode a lot of information in relatively small physical space, as well as compute on this information in a highly parallel manner. At the time of this writing, it was [demonstrated](http://science.sciencemag.org/content/337/6102/1628.full) that one can use DNA to store about $10^{16}$ bits of information in a region of radius about milimiter, as opposed to about $10^{10}$ bits with the best known hard disk technology. This does not posit a real challenge to the PECTT but does suggest that one should be conservative about the choice of constant and not assume that current hard disk + silicon technologies are the absolute best possible.^[We were extremely conservative in the suggested parameters for the PECTT, having assumed that as many as $\ell_P^{-2}10^{-6} \sim 10^{61}$ bits could potentially be stored in a milimeter radius region.]

* **Continuous/real computers.** The physical world is often described using continuous quantities such as time and space, and people have suggested that analog devices might have direct access to computing with real-valued quantities and would be inherently more powerful than discrete models such as NAND machines.
Whether the "true" physical world is continuous or discrete is an open question.
In fact, we do not even know how to precisely _phrase_ this question, let alone answer it. Yet, regardless of the answer, it seems clear that the effort to measure a continuous quantity grows with the level of accuracy desired, and so there is no "free lunch" or way to bypass the PECTT using such machines (see also [this paper](http://www.cs.princeton.edu/~ken/MCS86.pdf)). Related to that are proposals  known as "hypercomputing" or  "Zeno's computers" which attempt to use the continuity of time by doing the first operation in one second, the second one in half a second, the third operation in a quarter second and so on..  These fail for a  similar reason to the one guaranteeing that Achilles will eventually catch the tortoise despite the  original Zeno's paradox.

* **Relativity computer and time travel.** The formulation above assumed the notion of time, but under the theory of relativity time is in the eye of the observer. One approach to solve hard problems is to leave the computer to run for a lot of time from _his_ perspective, but to ensure that this is actually a short while from _our_ perspective. One approach to do so is for the user to start the computer and then go for a quick jog at close to the speed of light before checking on its status. Depending on how fast one goes, few seconds from the point of view of the user might correspond to centuries in computer time (it might even finish updating its Windows operating system!). Of course the catch here is that the energy required from  the user is proportional to how close one needs to get to the speed of light. A more interesting proposal is to use time travel via _closed timelike curves (CTCs)_. In this case we could run an arbitrarily long computation by doing some calculations, remembering  the current state, and the travelling back in time to continue where we left off. Indeed, if CTCs exist then we'd probably have to revise the PECTT (though in this case I will simply travel back in time and edit these notes, so I can claim I never conjectured it in the first place...)


* **Humans.** Another computing system that has been proposed as a counterexample to the PECTT is a 3 pound computer of  about 0.1m radius, namely the human brain. Humans can walk around, talk, feel, and do others things that are not commonly  done by NAND programs, but can they compute partial functions that NAND programs cannot?
There are certainly computational tasks that _at the moment_  humans do better than computers (e.g., play some [video games](http://www.theverge.com/2016/11/4/13518210/deepmind-starcraft-ai-google-blizzard), at the moment), but based on our current understanding of the brain, humans (or other animals) have no _inherent_ computational advantage over computers.
The brain has about $10^{11}$ neurons, each operating in a speed of about $1000$ operations per seconds. Hence a rough first approximation is that a NAND program of about $10^{14}$ lines could simulate one second of a brain's activity.^[This is a very rough approximation that could be wrong to a few orders of magnitude in either direction. For one, there are other structures in the brain apart from neurons that one might need to simulate, hence requiring higher overhead. On ther other hand, it is by no mean clear that we need to fully clone the brain in order to achieve the same computational tasks that it does.]
Note that the fact that such a NAND program (likely) exists does not mean it is easy to _find_ it.
After all, constructing this program took evolution billions of years.
Much of the recent efforts in artificial intelligence research is focused on finding programs that replicate some of the brain's capabilities and they take massive computational effort to discover, these programs often turn out to be much smaller than the pessimistic estimates above. For example, at the time of this writing, Google's [neural network for machine translation](https://arxiv.org/pdf/1609.08144.pdf) has about $10^4$ nodes (and can be simulated by a NAND program of comparable size). Philosophers, priests and many others have since time immemorial argued that there is something about humans that cannot be captured by  mechanical devices such as computers; whether or not that is the case, the evidence is thin that humans can perform computational tasks that are inherently impossible to achieve by computers of similar complexity.^[There are some well known scientists that have [advocated](http://www.telegraph.co.uk/science/2017/03/14/can-solve-chess-problem-holds-key-human-consciousness/) that humans have inherent computational advantages over computers. See also [this](https://arxiv.org/abs/1508.05929).]


* **Quantum computation.** The most compelling attack on the Physical Extended Church Turing Thesis comes from the notion of _quantum computing_.
The idea was initiated by the observation that systems with strong quantum effects are very hard to simulate on a computer.
Turning this observation on its head, people have proposed using such systems to perform computations that we do not know how to do otherwise.
At the time of this writing, Scalable quantum computers have not yet been built, but it is a fascinating possibility, and one that does not seem to contradict any known law of nature.
We will discuss quantum computing in much more detail later in this course.
Modeling it will  essentially involve extending the NAND programming language to the "QNAND" programming language that has one more (very special) operation.
However, the main take away is that while quantum computing does suggest we need to amend the PECTT, it does _not_ require a complete revision of our worldview. Indeed, almost all of the content of this course remains the same whether the underlying computational model is the "classical" model of NAND programs or the quantum model of QNAND programs (also known as _quantum circuits_).


> # {.remark title="PECTT in practice" #PECTTpractice}
While even the precise phrasing of the PECTT, let alone understanding its correctness, is still a subject of research, some variant of it is already implicitly assumed in practice.
A statement such as "this cryptosystem provides 128 bits of security" really means that __(a)__ it is conjectured that there is no Boolean circuit (or, equivalently, a NAND gate) of size much smaller than $2^{128}$ that can break the system,^[We say "conjectured" and not "proved" because, while we can phrase such a  statement as a precise mathematical conjecture, at the moment we are unable to _prove_ such a statement for any cryptosystem. This is related to the P vs NP question we will discuss in future lectures] and __(b)__ we assume that no other physical mechanism can do better, and hence it would take roughly a $2^{128}$ amount of "resources" to break the system.




> # { .recap }
* We can think of programs both as describing a _process_, as well as simply a list of symbols that can be considered as _data_ that can be fed as input to other programs.
* We can write a NAND program that evaluates arbitrary NAND programs. Moreover, the efficiency loss in doing so is not too large.
* We can even write a NAND program that evaluates programs in other programming languages such as Python, C, Lisp, Java, Go, etc.
* By a leap of faith, we could hypothesize that the number of lines in the smallest NAND program for a function $F$ captures roughly the amount of physical resources required to compute $F$. This statement is known as the _Physical Extended Church-Turing Thesis (PECTT)_.
* NAND programs capture a surprisingly wide array of computational models. The strongest currently known challenge to the PECTT comes from the potential for using quantum mechanical effects to speed-up computation, a model known as _quantum computers_.


## Exercises

> # {.exercise #reading-comp}
Which one of the following statements is false: \
a. There is an $O(s^3)$ line NAND program that given as input program $P$ of $s$ lines in the list-of-tuples representation computes the output  of $P$ when all its input are equal to $1$. \
b. There is an $O(s^3)$ line NAND program that given as input program $P$ of $s$ characters encoded as a string of $7s$ bits using the ASCII encoding, computes the output  of $P$ when all its input are equal to $1$. \
c. There is an $O(\sqrt{s})$ line NAND program that given as input program $P$ of $s$ lines in the list-of-tuples representation computes the output  of $P$ when all its input are equal to $1$.


> # {.exercise title="Equals function" #equals}
For every $k \in \N$, show that there is an $O(k)$ line NAND program that computes the function $EQUALS_k:\{0,1\}^{2k} \rightarrow \{0,1\}$ where $EQUALS(x,x')=1$ if and only if $x=x'$.

> # {.exercise title="Equals to constant function" #equalstwo}
For every $k \in \N$ and $x' \in \{0,1\}^k$, show that there is an $O(k)$ line NAND program that computes the function $EQUALS_{x'} : \{0,1\}^k \rightarrow \{0,1\}$ that on input $x\in \{0,1\}^k$ outputs $1$ if and only if $x=x'$.




> # {.exercise title="Random functions are hard (challenge)" #rand-lb-id}
Suppose $n>1000$ and that we choose a function $F:\{0,1\}^n \rightarrow \{0,1\}$ at random, choosing for every $x\in \{0,1\}^n$ the value $F(x)$ to be the result of tossing an independent unbiased coin. Prove that the probability that there is a $2^n/(1000n)$ line program that computes $F$ is at most $2^{-100}$.^[__Hint:__ An equivalent way to say this is that you need to prove that the set of functions that can be computed using at most $2^n/(1000n)$ has fewer than $2^{-100}2^{2^n}$ elements. Can you see why?]

> # {.exercise title="Circuit hierarchy theorem (challenge)"  #hierarchy-thm}
Prove that there is a constant $c$ such that for every $n$, there is some function $F:\{0,1\}^n \rightarrow \{0,1\}$ s.t. __(1)__ $F$ _can_ be computed by a NAND program of at most $c n^5$ lines, but __(2)__ $F$ can _not_ be computed by a NAND program of at most $n^4 /c$ lines.^[__Hint:__ Find an approriate value of $t$ and a function $G:\{0,1\}^t \rightarrow \{0,1\}$ that can be computed in $O(2^t/t)$ lines but _can't_ be computed in $\Omega(2^t/t)$ lines, and then extend this to a function mapping $\{0,1\}^n$ to $\{0,1\}$.]


^[TODO: add exercise to do  evaluation of $T$ line   programs in $\tilde{O}(T^{1.5})$ time.]





## Bibliographical notes

^[TODO: $EVAL$ is known as _Circuit Evaluation_ typically. More references regarding oblivious RAM etc..]

Scott Aaronson's blog post on how [information is physical](http://www.scottaaronson.com/blog/?p=3327) is a good discussion on issues related to the physical extended Church-Turing Physics.
Aaronson's [survey on  NP complete problems and physical reality](http://www.arxiv.org/abs/quant-ph/0502072) is also a great source for some of these issues, though might be easier to read after we reach the lectures on NP and NP completeness.


## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

* Lower bounds. While we've seen the "most" functions mapping $n$ bits to one bit require NAND programs of exponential size $\Omega(2^n/n)$, we actually do not know of any _explicit_ function for which we can _prove_ that it requires, say, at least $n^{100}$ or even $100n$ size. At the moment, strongest such lower bound we know is that there are quite simple and explicit $n$-variable functions that require at least $(5-o(1))n$ lines to compute, see [this paper of Iwama et al](http://www.wisdom.weizmann.ac.il/~ranraz/publications/P5nlb.pdf) as well as this more recent [work of Kulikov et al](http://logic.pdmi.ras.ru/~kulikov/papers/2012_5n_lower_bound_cie.pdf).
Proving lower bounds for restricted models of straightline programs (more often described as _circuits_) is an extremely interesting research area, for which [Jukna's book](http://www.thi.informatik.uni-frankfurt.de/~jukna/boolean/index.html) provides  very good introduction  and overview.




## Acknowledgements
