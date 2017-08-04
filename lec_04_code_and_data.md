# Code as data, data as code

>_"The term code script is, of course, too narrow. The chromosomal structures are at the same time instrumental in bringing about the development they foreshadow. They are law-code and executive power - or, to use another simile, they are architect’s plan and builder’s craft - in one."_ ,  Erwin Schrödinger, 1944.

>_"The importance of the universal machine is clear. We do not need to have an infinity of different machines doing different jobs. ... The engineering problem of producing various machines for various jobs is replaced by the office work of 'programming' the universal machine"_, Alan Turing, 1948


A NAND program can be thought of as simply a sequence of symbols, each of which can be encoded with zeros and ones using (for example) the ASCII standard.
Thus we can represent every NAND program as a binary string.
This statement seems obvious but it is actually quite profound.
It means that we can treat a NAND program both as instructions to carrying computation and also as _data_ that could potentially be input to other computations.


This correspondence between _code_ and _data_ is one of the most fundamental aspects of computing.
It  underlies  the notion of _general purpose_ computers, that are not pre-wired to compute only one task, and it is also the basis of our  hope for obtaining _general_ artificial intelligence.
This concept finds immense use in all areas of computing, from scripting languages to machine learning, but it is fair to say that we haven't yet fully mastered it.
Indeed many security exploits involve cases such as "buffer overflows" when attackers manage to inject code where the system expected only "passive" data.
The idea of code as data reaches beyond the realm of electronic computers.
For example, DNA can be thought of as both a program and data (in the words of Schrödinger, who wrote  before DNA's discovery a book that inspired Watson and Crick, it is both "architect's plan and builder's craft").

![As illustrated in this xkcd cartoon, many exploits, including buffer overflow, SQL injections, and more, utilize the blurry line between "active programs" and "static strings".](../figure/exploits_of_a_mom.png){#XKCD .class width=300px height=300px}


## A NAND interpreter in NAND

One of the most interesting consequences of the fact that we can represent programs as strings is the following theorem:

> # {.theorem title="Bounded Universality of NAND programs" #bounded-univ}
For every $s,n,m \in \N$ there is a NAND program that computes the  function
$$
EVAL_{s,n,m}:\{0,1\}^{s+n} \rightarrow \{0,1\}^m
$$
defined as follows: For every string $(P,x)$ where $P \in \{0,1\}^s$ and $x\in\{0,1\}^n$, if $P$ describes a NAND program with $n$ input bits and $m$ outputs bits, then   $EVAL_{s,n,m}(x)$ is the output of this program on input $x$.^[If $P$ does not describe a program then we don't care what $EVAL_{s,n,m}(P,x)$ is, but for concreteness we will set it to be $0^m$.]


Of course to fully specify $EVAL_{s,n,m}$, we need to fix a precise representation scheme  for NAND programs as binary strings.
We can simply use the ASCII representation, though later we will use a somewhat more convenient representation.
But regardless of the choice of representation,
[bounded-univ](){.ref} is an immediate corollary of the fact that _every_ finite function, and so in particular the function $EVAL_{s,n,m}$ above, can be computed by _some_ NAND program.


[bounded-univ](){.ref} can be thought of as providing  a "NAND interpreter in NAND".
That is, for a particular size bound, we give a _single_ NAND program that can evaluate all NAND programs of that size.
We call the NAND program $U_{s,n,m}$ that computes $EVAL_{s,n,m}$ a _bounded universal program_.
"Universal" stands for the fact that this is a _single program_ that can evaluate _arbitrary_ code,  where "bounded" stands for the fact that $U_{s,n,m}$ only evaluates programs of bounded size.
Of course this limitation is inherent for the NAND programming language where an $N$-line program can never compute a function with more than $N$ inputs.
(We will later on introduce the concept of _loops_, that  allows  to escape this limitation.)


It turns out that we don't even need to pay that much of an overhead for universality

> # {.theorem title="Efficient bounded universality of NAND programs" #eff-bounded-univ}
For every $s,n,m \in \N$ there is a NAND program of at most $O(s \log s)$ lines that computes the  function
$EVAL_{s,n,m}:\{0,1\}^{s+n} \rightarrow \{0,1\}^m$ defined above.

We will prove a weaker version of [eff-bounded-univ](){.ref}, that will use a large number of  $O(s^3 \log s)$ lines instead of $O(s \log s)$ as stated in the theorem.
We will sketch  how we can improve this proof and get the  $O(s \log s)$ bound in the next lecture.
Unlike [bounded-univ](){.ref}, [eff-bounded-univ](){.ref} is not a trivial corollary of the fact that every function can be computed, and  takes much more effort to prove.
It requires us to present a concrete NAND program for the $EVAL_{s,n,m}$ function.
We will do so in several stages.

First, we will spell out precisely how represent NAND programs as strings.
We can prove  [eff-bounded-univ](){.ref}  using the ASCII representation, but a "cleaner" representation will be more convenient for us.
Then, we will show how we can write a  program to compute $EVAL_{s,n,m}$ in _Python_.^[We will not use much about Python, and a reader that has familiarity with programming in any language should be able to follow along.]
Finally, we will show how we can transform this Python program into a NAND program.

## Concrete representation for NAND programs

![In the Harvard Mark I computer, a program was represented as a list of triples of numbers, which were then encoded by perforating holes in a control card.](../figure/tapemarkI.png){#figureid .class width=300px height=300px}


Every line in a NAND program has the form

~~~~ { .go }
foo := bar NAND baz   
~~~~

Since the actual labels for the variables are meaningless (except for designating if they are input, output or "workspace" variables), we can encode them as numbers from $0$ to $t-1$, where $t$  is a bound on the largest index and the number of  distinct variables used in the program.
(We can set $t=3s$, where $s$ is the number of lines in the program, since every line in the program involves at most three distinct variables.)
We encode a variable of the form `foo_`$\expr{i}$ as the pair of natural numbers $(a,i)$ where $a$ is the number corresponding to the label `foo`.
Thus we   encode a line of the form

`foo_`$\expr{i}$`  :=  bar_`$\expr{j}$ `  NAND  baz_`$\expr{k}$

as a six-tuple $(a,i,b,j,c,k)$ where $a,b,c$ are the numbers corresponding to `foo`,`bar`,`baz` respectively.
We encode a NAND program of $s$ lines as simply a list of $s$ six-tuples.^[If a variable `foo` appears in the program without an index, then we assume that this is the same as `foo_0`.]
For example, the XOR program:

~~~~ { .go .numberLines  }
u_0   := x_0 NAND x_1
v_0   := x_0 NAND u_0
w_0   := x_1 NAND u_0
y_0   := v_0 NAND w_0
~~~~  

is  represented by the following list of four six-tuples:
```
[ [2, 0, 0, 0, 0, 1],
  [3, 0, 0, 0, 2, 0],
  [4, 0, 0, 1, 2, 0],
  [1, 0, 3, 0, 4, 0] ]
```

Note that even if we renamed `u`, `v` and `w` to `foo`, `bar` and `blah` then the representation of the program will remain the same (which is fine, since it does not change its semantics).  
It is very easy to transform a string containing the program code to a the list-of-tuples representation; for example, it can be done in 15 lines of Python.^[If you're curious what these 15 lines are, see the appendix or the website [http://nandpl.org](http://nandpl.org).]  

To evaluate a NAND program $P$ given in this representation, on an input $x$, we will do the following:

* We create an array `avars` of $ts$ integers. The value of the variable with label $a$ and index $i$ is will be stored in the $t\cdot i + a$ location of this array.

* We initialize the value of the input variables. We set $0$ to be the index corresponding to the label `x`, and so to initialize the value of  the `x_`$\expr{i}$ variables  we set the $(t\cdot i)^{th}$ coordinate of `avars` to $x_i$ for every $i\in [n]$.

* For every line $(a,i,b,j,c,k)$ in the program, we read from `avars` the values $x,y$ of the variables $(b,j)$ and $(c,k)$ respectively, and then set the value of the variable $(a,i)$ to $NAND(x,y)=1-x\cdot y$. That is, we set `avars[i*t+a] = 1-avars[j*t+b]*avars[k*t+c]`.

* We set $1$ to be the index corresponding to the label `y` and so the  output is the value of the variables $(1,0),\ldots,(0,m-1)$ which are equal to `avars[0*t+1]`,...,`avars[(m-1)*t+1]`.

^[TODO: Perhaps comment that we will not use the indices $2$ and $3$ as to maintain compatiblity with the representation of NAND++ that will be introduced later on.]


The following is a   _Python_ function `EVAL` that on input $n,m,P,x$ where $P$ is a list of six-tuples and $x$ is list of $0/1$ values, returns the result of the execution of the NAND program represented by $P$ on $x$:^[To keep things simple, we will not worry about the case that $P$ does not represent a valid program of $n$ inputs and $m$ outputs.]


~~~~ { .python .numberLines }
# Evaluates an n-input, m-output NAND program P on input x
# P is given in the list of tuples representation
def EVAL(n,m,P,x):
    s = len(P)    # no. of lines in the program
    t = 3*len(P)  # maximum no. of unique labels
    avars = [0]*(t*s) # initialize array to 0
    for i in range(n): # initalize inputs to x
        avars[i*t] = x[i]

    for (a,i,b,j,c,k) in P: # evaluate every line of program
        avars[i*t+a] = 1-avars[j*t+b]*avars[k*t+c]

    #  return y_0...y_(m-1) which is
    # avars[1],avars[t+1],...,avars[(m-1)*t+1]
    return [avars[i*t+1] for i in range(m)]
~~~~


For example, if we run

```python
EVAL(2,1,
  [[2, 0, 0, 0, 0, 1],
  [3, 0, 0, 0, 2, 0],
  [4, 0, 0, 1, 2, 0],
  [1, 0, 3, 0, 4, 0]],
  [0,1])
```
then this corresponds to running our XOR program on the input $(0,1)$ and hence the resulting output is `[1]`.


Accessing an  element  of the array `avars` at a given index takes a constant number of basic operations.^[Python does not distinguish between lists and arrays, but allows constant time random access to an indexed elements to both of them. One could argue that if we allowed programs of truly unbounded length (e.g., larger than $2^{64}$) then the price  would not be constant but logarithmic in the length of the array/lists, but the difference between $O(1)$ and $O(\log s)$ will not be important for our discussions.] Hence (since $n,m \leq s$), apart from the initialization phase that costs $O(ts)=O(s^2)$ steps, the program above will use  $O(s)$ basic operations.

## A NAND interpreter in NAND  

To prove [eff-bounded-univ](){.ref} it is of course not enough to give a Python program.
We need to transform the code above to a NAND program that will compute the function $EVAL_{n,m,s}$ that takes a (representation of) $s$-line NAND program $P$ computing a function on $n$ inputs and with $m$ outputs, and an input $w\in \{0,1\}^n$, and outputs $P(w))$.

The total number of distinct labels and indices in an $s$ line program is at most $t=3s$.
Hence we can think of the six-tuple representation of  such a program as simply a sequence of $6s$ numbers between $0$ and $t-1$, each of which can be represented by $\ell=\lceil \log t \rceil$ bits, meaning that such a program $P$ can be identified with a string in $\{0,1\}^{6s\ell}$.

The NAND program takes an input $(P,w)$ of length $6s\ell+n$ and needs to output the result of applying $P$ to $w$.
It will follow very closely the Python implementation above:

* We define variables `avars_0`,$\ldots$,`avars_`$\expr{t\cdot s}$.

* Every line of the program is represented by a string of length $6\ell$, which we can think of as having the form $(a,i,b,j,c,k)$ with $a,i,b,j,c,k$ being numbers in $\{0,\ldots,t-1\}$ represented using the binary representation as $\ell$-bit strings.

* We will go over  every line of the original program and execute it just as the Python program does: we will retrieve the values corresponding to $(b,j)$ and $(c,k)$ in `avars`, and then update `avars` in the location corresponding to $(a,i)$ to the NAND of these values.

Since we have algorithms for addition and multiplication, we can  transform a pair $(a,i)$ to the index $u=t\cdot i + a$ in $O(\ell^2)$ time.
Hence to evaluate such a line, we need to be able to compute the following functions:

* $GETVAL$, which maps  a string $vars \in \{0,1\}^N$ and an index $u \in \{0,\ldots, N-1\}$ (which we also think of as a string in $\{0,1\}^{\log N}$), outputs $var_u$.

* $SETVAL$, which maps a string $vars\in \{0,1\}^N$, an index $u\in \{0,\ldots,N-1\}$ (which as above can also be considered as a string in $\{0,1\}^{\log N}$), and a value $v\in \{0,1\}$, returns $vars' \in \{0,1\}^N$ such that $vars'$ is the same as $vars$ except that $vars'_u = v$.

By rounding up $st$ to the nearest power of $2$ (which at most doubles its size), we can assume the array `avars` is of length $2^k$ for $k=\lceil st \rceil$.
What is left is to show that we can implement both $GETVAL$ and $SETVAL$ in $O(2^k)$ lines.

1. A moment of reflection shows that $GETVAL$ is simply the $LOOKUP_k$ function which we know can be implemented with $O(2^k)=O(st)$ lines.

2.  The function $SETVAL$ is also very simple. For every index $u'$, the $u'^{th}$ output of $SETVAL$ is equal to $vars_{u'}$ if $u\neq u'$ and is equal to $v$ otherwise.
So, to compute $SETVAL$ we need to compute for every $u'$ the function $EQUAL_{u'}:\{0,1\}^{\log N} \rightarrow \{0,1\}$ such that $EQUAL_{u'}(u')=1$ and $EQUAL_{u'}(u)=0$ for every $u \neq u'$.
That is $EQUAL_{u'}(u)$ corresponds to the AND of the $\log N$ conditions $u_i=u'_i$ for $i\in \{0,\ldots,\log N\}$.
It is not hard to verify that we can compute $EQUAL_{u'}$ in $O(\log N)$ lines.
Since $SETVAL(vars,u,v)_{u'}=LOOKUP_1(vars_u,v,EQUAL_{u'}(u))$, we get that $SETVAL$ can be  be computed using $O(N \log N)$ lines.


The total cost to compute $EVAL$ will be $s$ times the cost to compute two $GETVAL$'s and one $SETVAL$, which will come up to $O(s(st)\log(st))=O(s^3 \log s)$.
This completes the proof of [eff-bounded-univ](){.eqref}.

If you want to see the actual resulting code,  the website [http://nandpl.org](http://nandpl.org) contains (or will eventually contain..) the full implementation of this NAND program where you can also play with it by feeding it various other programs as inputs.
The NAND program above is less efficient that its Python counterpart, since NAND does not offer arrays with efficient random access, and hence the `LOOKUP` operation on an array of $N$ bits takes $\Omega(N)$ lines in NAND even though it takes $O(1)$ steps (or maybe $O(\log N)$ steps, depending how we count) in _Python_.
It is not hard to improve our $O(s^3 \log s)$ bound to $O(s^2 \log s)$, since we were quite wasteful in allocating an array of size $ts$ for what can be at most $3s$ distinct variables (see [square-eval-ex](){.ref}).
We will see in a future lecture how to improve this to $O(s \log^c s)$ for some constant $c$.



##  A Python interpreter in NAND

To prove [eff-bounded-univ](){.ref} we essentially translated every line of the Python program for `EVAL` into an equivalent NAND snippet.
It turns out that none of our reasoning  was specific to the  particular function $EVAL$.
It is possible to translate _every_ Python program into an equivalent `NAND` program of comparable efficiency.^[More concretely, if when executed the Python program takes $T(n)$ operations on inputs of length at most $n$ then we can find a NAND program for the function restricted to $n$ inputs will have $O(T(n) \log T(n))$ lines.]
Actually doing so requires taking care of many details and is beyond the scope of this course, but let me convince you why you should believe it is possible in principle.
We can use [CPython](https://en.wikipedia.org/wiki/CPython) (the reference implementation for Python), to evaluate every Python program using a `C` program.
We can combine this with a C compiler to transform a Python program to various flavors of "machine language".


So, to transform a Python program into an equivalent NAND program, it is enough to show how to transform a machine language program into an equivalent NAND program.
One minimalistic (and hence convenient) family of machine languages is known as the _ARM architecture_ which powers a great many mobile devices including essentially all Android devices.^[ARM stands for "Advanced RISC Machine" where RISC in turn stands for "Reduced instruction set computing"]  
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



## Counting programs, and lower bounds on the size of NAND programs.

One of the consequences of our representation is the following:

> # {.theorem title="Counting programs" #program-count}
There are at most $2^{O(s\log s)}$ functions computed by $s$-line NAND programs.

Moreover, the implicit constant in the $O(\cdot)$ notation in [program-count](){.ref} at most $10$.
Using the notation introduced in the last lecture, another way to  state [program-count](){.ref}, is that for every $n,m,s$, $|SIZE_{n,m}(s)| \leq 2^{10s \log s}$.
The idea of the proof is that because every such program can be represented by a binary string of at most $10s \log s$ bits, the number of functions they compute cannot be larger than the number of such strings. Let us now show the formal proof.

> # {.proof data-ref="program-count"}
Every NAND program with $s$ lines has at most $s$ inputs, $s$ outputs, and $s$ workspace variables.
Hence it can be represented by $s$ six-tuples of numbers in $\{0,\ldots,3s-1\}$.
If two programs compute distinct functions then they have distinct representations.
>
Let $\mathcal{T}_s$ be the set of lists of at most $6s$ numbers between $\{0,\ldots,3s-1\}$.
Note that $|\mathcal{T}_s| = \sum_{t=1}^{6s}(3s)^t \leq (6s)(3s)^{6s} \leq 2^{10s\log s}$.
Let  $\mathcal{F}_s$ be the set of functions from $\{0,1\}^*$ to $\{0,1\}^*$ that can be computed by
$s$-line NAND programs. We can define a one-to-one map $R:\mathcal{F}_s \rightarrow \mathcal{T}_s$ by setting  for
every function $F\in\mathcal{F}_s$ the value $R(F)$ to be the representation of the shortest NAND program that computes the function $F$ (breaking ties arbitrarily).
Note that $R(F)$ is indeed in $\mathcal{T}_S$ since for every $F\in \mathcal{F}_s$, the shortest program that computes it will have at most $s$ lines.
Since $F \neq F'$ means that the programs $R(F)$ and $R(F')$ compute different functions, and hence have distinct representations, $R$ is a one-to-one function
implying that $|\mathcal{F}_s| \leq |\mathcal{T}_s| \leq 2^{10s\log s}$.

__Note:__ We can also establish [program-count](){.ref} directly from the ASCII representation of the source code.  Since an $s$-line NAND program has at most $3s$ distinct variables,  we can change all the workspace variables of such a program to have the form `work_`$\expr{i}$ for $i$ between $0$ and $3s-1$ without changing the function that it computes. This means that  after removing comments and extra whitespaces, every line of such a program (which will  the form `var := var' NAND var''` for variable identifiers which will be either `x_###`,`y_###` or `work_###` where `###` is some number smaller than $3s$) will require at most, say, $20 + 3\log_{10} (3s) \leq O(\log s)$ characters. Since each one of those characters can be encoded using seven bits in the ASCII representation, we see that the number of functions computed by $s$-line NAND programs is at most $2^{O(s \log s)}$.

A function mapping $\{0,1\}^2$ to $\{0,1\}$ can be identified with the table of its four values on the inputs $00,01,10,11$;
a function mapping $\{0,1\}^3$ to $\{0,1\}$ can be identified with the table of its eight values on the inputs $000,001,010,100,101,110,111$.
More generally, every function $F:\{0,1\}^n \rightarrow \{0,1\}$ can be identified with the table of its  $2^n$  values  on the inputs $\{0,1\}^n$.
Hence the number of functions mapping $\{0,1\}^n$ to $\{0,1\}$ is equal to the number of such tables which (since we can choose either $0$ or $1$ for every row) is exactly $2^{2^n}$. This has the following interesting corollary:

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

## Lecture summary

* We can think of programs both as describing a _process_, as well as simply a list of symbols that can be considered as _data_ that can be fed as input to other programs.
* We can write a NAND program that evaluates arbitrary NAND programs. Moreover, the efficiency loss in doing so is not too large.
* We can even write a NAND programs that evaluates programs in other programming languages such as Python, C, Lisp, Java, Go, etc..

## Exercises

> # {.exercise #reading-comp}
Which one of the following statements is false: \
a. There is an $O(s^3)$ line NAND program that given as input program $P$ of $s$ lines in the list-of-tuples representation computes the output  of $P$ when all its input are equal to $1$. \
b. There is an $O(s^3)$ line NAND program that given as input program $P$ of $s$ characters encoded as a string of $7s$ bits using the ASCII encoding, computes the output  of $P$ when all its input are equal to $1$. \
c. There is an $O(\sqrt{s})$ line NAND program that given as input program $P$ of $s$ lines in the list-of-tuples representation computes the output  of $P$ when all its input are equal to $1$.


> # {.exercise title="Equals function" #equals}
For every $k$, show that there is an $O(k)$ line NAND program that computes the function $EQUALS_k:\{0,1\}^{2k} \rightarrow \{0,1\}$ where $EQUALS(x,x')=1$ if and only if $x=x'$.

> # {.exercise title="Improved evaluation" #square-eval-ex}
Show that there is an  $O(s^2 \log s)$-line NAND program to evaluate $EVAL_{n,m,s}$.^[__Hint:__ Show that that the array `avars` will alwaus have at most $O(s)$ nonzero values, and use that to give a more compact representation for it.]


> # {.exercise title="Random functions are hard (challenge)" #rand-lb-id}
Suppose $n>1000$ and that we choose a function $F:\{0,1\}^n \rightarrow \{0,1\}$ at random, choosing for every $x\in \{0,1\}^n$ the value $F(x)$ to be the result of tossing an independent unbiased coin. Prove that the probability that there is a $2^n/(1000n)$ line program that computes $F$ is at most $2^{-100}$.^[__Hint:__ An equivalent way to say this is that you need to prove that the set of functions that can be computed using at most $2^n/(1000n)$ has fewer than $2^{-100}2^{2^n}$ elements. Can you see why?]

> # {.exercise title="Circuit hierarchy theorem (challenge)"  #hierarchy-thm}
Prove that there is a constant $c$ such that for every $n$, there is some function $F:\{0,1\}^n \rightarrow \{0,1\}$ s.t. __(1)__ $F$ _can_ be computed by a NAND program of at most $c n^5$ lines, but __(2)__ $F$ can _not_ be computed by a NAND program of at most $n^4 /c$ lines.^[__Hint:__ Find an approriate value of $t$ and a function $G:\{0,1\}^t \rightarrow \{0,1\}$ that can be computed in $O(2^t/t)$ lines but _can't_ be computed in $\Omega(2^t/t)$ lines, and then extend this to a function mapping $\{0,1\}^n$ to $\{0,1\}$.]


^[TODO: add exercise to do  evaluation of $T$ line   programs in $\tilde{O}(T^{1.5})$ time.]





## Bibliographical notes

^[TODO: $EVAL$ is known as _Circuit Evaluation_ typically. More references regarding oblivious RAM etc..]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

* Lower bounds. While we've seen the "most" functions mapping $n$ bits to one bit require NAND programs of exponential size $\Omega(2^n/n)$, we actually do not know of any _explicit_ function for which we can _prove_ that it requires, say, at least $n^{100}$ or even $100n$ size. At the moment, the best we unconditional lower bound known is that there are quite simple and explicit $n$-variable functions that require at least $(5-o(1))n$ lines to compute, see [this paper of Iwama et al](http://www.wisdom.weizmann.ac.il/~ranraz/publications/P5nlb.pdf) as well as this more recent [work of Kulikov et al](http://logic.pdmi.ras.ru/~kulikov/papers/2012_5n_lower_bound_cie.pdf).
Proving lower bounds for restricted models of straightline programs (more often described as _circuits_) is an extremely interesting research area, for which [Jukna's book](http://www.thi.informatik.uni-frankfurt.de/~jukna/boolean/index.html) provides  very good introduction  and overview.




## Acknowledgements
