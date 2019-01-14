% Computing every function
% Boaz Barak


# Syntactic sugar, and computing every function

> # { .objectives }
* Get comfort with syntactic sugar or automatic translation of higher level logic to  low level gates. \
* Learn proof of major result: every finite function can be computed by a Boolean circuit. \
* Start thinking _quantitatively_ about number of lines required for computation.



>_"[In 1951] I had a running compiler and nobody would touch it because, they carefully told me, computers could only do arithmetic; they could not do programs."_,  Grace Murray Hopper, 1986.


>_"Syntactic sugar causes cancer of the semicolon."_, Alan Perlis, 1982.




The NAND-CIRC programing language is pretty much as "bare bones" as programming languages come.
After all, it only has a single operation.
But, it turns out we can implement some "added features" on top of it.
That is, we can show how we can implement those features using the underlying mechanisms of the language.


For example, some calculations can  more convenient to express using AND, OR and NOT than with NAND, but we can always translate code such as

```python
foo = OR(bar,blah)
```

into the valid NAND-CIRC code:

```python
notbar  = NAND(bar,bar)
notblah = NAND(blah,blah)
foo    = NAND(notbar,notblah)
```



Thus in describing NAND-CIRC programs we can (and will) allow ourselves to use operations such as OR, with the understanding that in actual programs we will replace every line of the first form with the three lines of the second form.
In programming language parlance this is known as _"syntactic sugar"_, since we are not changing the definition of the language, but merely introducing some convenient notational shortcuts.^[This concept is also known as "macros" or "meta-programming" and is sometimes implemented via a preprocessor or macro language in a programming language or a text editor. One modern example is the [Babel](https://babeljs.io/) JavaScript syntax transformer, that converts JavaScript programs written using the latest features into a format that older Browsers can accept. It even has a [plug-in](https://babeljs.io/docs/plugins/) architecture, that allows users to add their own syntactic sugar to the language.]
We will use several such "syntactic sugar" constructs to make our descriptions of NAND-CIRC programs shorter and simpler.
However, these descriptions are  merely shorthand for the equivalent standard or "sugar free" NAND-CIRC program that is obtained after removing the use of all these constructs.
In particular, when we  say that a function $f$ has an $s$-line NAND-CIRC program, we mean a _standard_ NAND-CIRC program, that does not use any syntactic sugar.

## Some examples syntactic sugar

Here are some examples of "syntactic sugar" that we can use in constructing NAND-CIRC programs.
This is not an exhaustive list - if you find yourself needing to use an extra feature in your NAND-CIRC program then you can just show how to implement it based on the existing ones.
Going over  examples for syntatic sugar can be a little tedious, but we do it for two reasons:

1. To convince you that despite its seeming simplicity and limitations, the NAND-CIRC programming language is actually quite powerful and can capture many of the fancy programming constructs such as `if` statements and function definitions  that exists in more fashionable languages.

2. So you can realize how lucky you are to be  taking a theory of computation course and not a compilers course... `:)`



### Constants

We can create variables `zero` and `one` that  have the values  $0$ and $1$ respectively by adding the lines

```python
temp = NAND(X[0],X[0])
one  = NAND(temp,X[0])
zero = NAND(one,one)
```


Note that since for every $x\in \{0,1\}$, $NAND(x,\overline{x})=1$, the variable `one` will get the value $1$ regardless of the value of $x_0$, and the variable `zero` will get the value $NAND(1,1)=0$.


### Functions / Macros

Another staple of almost any programming language is the ability to execute _functions_.
However, we can achieve the same effect as (non recursive) functions using the time honored technique of  "copy and paste".
That is, we can replace code which defines a macro

```python
def Func(a,b):
    function_code
    return c
some_code
f = Func(e,d)
some_more_code
```

with the following code where we "paste" the code of `Func`

```python
some_code
function_code'
some_more_code
```

and where `function_code'` is obtained by replacing all occurrences of `a` with `d`,`b` with `e`, `c` with `f`.
When doing that we will need to  ensure that all other variables appearing in `function_code'` don't interfere with other variables.
We can always do so by renaming variables to new names that were not used before.

### Example: Computing Majority via NAND's

Function definitions allow us to express NAND-CIRC programs much more cleanly and succinctly. For example, because we can compute AND,OR, NOT using NANDs, we can compute the _Majority_ function as well.

```python
def NOT(a): return NAND(a,a)
def AND(a,b): return NOT(NAND(a,b))
def OR(a,b): return NAND(NOT(a),NOT(b))

def MAJ(a,b,c):
    return OR(OR(AND(a,b),AND(b,c)),AND(a,c))

print(MAJ(0,1,1))
# 1
```

This is certainly much more pleasant than the full NAND alternative:

```python
Temp[0] = NAND(X[0],X[1])
Temp[1] = NAND(Temp[0],Temp[0])
Temp[2] = NAND(X[1],X[2])
Temp[3] = NAND(Temp[2],Temp[2])
Temp[4] = NAND(Temp[1],Temp[1])
Temp[5] = NAND(Temp[3],Temp[3])
Temp[6] = NAND(Temp[4],Temp[5])
Temp[7] = NAND(X[0],X[2])
Temp[8] = NAND(Temp[7],Temp[7])
Temp[9] = NAND(Temp[6],Temp[6])
Temp[10] = NAND(Temp[8],Temp[8])
Y[0] = NAND(Temp[9],Temp[10])
```


### Conditional statements

Another sorely missing feature in NAND is a conditional statement such as the `if`/`then` constructs that are found in many programming languages.
However, using functions, we can obtain an ersatz if/then construct.
First we can compute the function $IF:\{0,1\}^3 \rightarrow \{0,1\}$ such that $IF(a,b,c)$ equals $b$ if $a=1$ and $c$ if $a=0$.

> # { .pause }
Before reading onwards, try to  see how you could compute the $IF$ function using $NAND$'s.
Once you  you do that, see how you can use that to emulate `if`/`then` types of constructs.

The $IF$ function can be implemented from NANDs as follows (see [mux-ex](){.ref}):

```python
def IF(cond,a,b):
    notcond = NAND(cond,cond)
    temp = NAND(b,notcond)
    temp1 = NAND(a,cond)
    return NAND(temp,temp1)


print(IF(0,1,0))
# 0
print(IF(1,1,0))
# 1
```

The $IF$ function is also known as the _multiplexing_ function, since $cond$ can be thought of as a switch that controls whether the output is connected to $a$ or $b$.

Using the $IF$ function, we can implement conditionals in NAND.
The idea is that we replace code of the form

```python
if (condition):  assign blah to variable foo
```

with code of the form

```python
foo   = IF(condition,blah, foo)
```

that assigns to `foo` its old value when `condition` equals $0$, and assign to `foo` the value of `blah` otherwise.
More generally we can replace code of the form

```python
if (cond):
    a = ...
    b = ...
    c = ...
```

with code of the form

```python
temp_a = ...
temp_b = ...
temp_c = ...
a = IF(cond,temp_a,a)
b = IF(cond,temp_b,b)
c = IF(cond,temp_c,c)
```


## Extended example: Addition and Multiplicatoin (optional) { #addexample }


Using "syntactic sugar",  we can write the integer addition function as follows:^[We use here least-significant-digit first convention  for simplicity of notation.]

```python
# Add two n-bit integers
def ADD(A,B):
    Result = [0]*(n+1)
    Carry  = [0]*(n+1)
    Carry[0] = zero(A[0])
    for i in range(n):
        Result[i] = XOR(Carry[i],XOR(A[i],B[i]))
        Carry[i+1] = MAJ(Carry[i],A[i],B[i])
    Result[n] = Carry[n]
    return Result

ADD([1,1,1,0,0],[1,0,0,0,0]);;
# [0, 0, 0, 1, 0, 0]
```

where `zero` is the constant zero function, and `MAJ` and `XOR` correspond to the majority and XOR functions respectively.

In the above we used the _loop_ `for i in range(n)`  but we can expand this out by simply repeating the code $n$ times, replacing the value of `i` with $0,1,2,\ldots,n-1$.
The crucial point is that (unlike most programming languages) we do not allow the number of times the loop is executed to  depend on the input, and so it is always possible to "expand out" the loop by simply copying the code the requisite number of times.


By expanding out all the features, for every value of $n$ we can translate the above program into a standard ("sugar free") NAND-CIRC program. Here is what we get for $n=2$:

```python
Temp[0] = NAND(X[0],X[0])
Temp[1] = NAND(X[0],Temp[0])
Temp[2] = NAND(Temp[1],Temp[1])
Temp[3] = NAND(X[0],X[2])
Temp[4] = NAND(X[0],Temp[3])
Temp[5] = NAND(X[2],Temp[3])
Temp[6] = NAND(Temp[4],Temp[5])
Temp[7] = NAND(Temp[2],Temp[6])
Temp[8] = NAND(Temp[2],Temp[7])
Temp[9] = NAND(Temp[6],Temp[7])
Y[0] = NAND(Temp[8],Temp[9])
Temp[11] = NAND(Temp[2],X[0])
Temp[12] = NAND(Temp[11],Temp[11])
Temp[13] = NAND(X[0],X[2])
Temp[14] = NAND(Temp[13],Temp[13])
Temp[15] = NAND(Temp[12],Temp[12])
Temp[16] = NAND(Temp[14],Temp[14])
Temp[17] = NAND(Temp[15],Temp[16])
Temp[18] = NAND(Temp[2],X[2])
Temp[19] = NAND(Temp[18],Temp[18])
Temp[20] = NAND(Temp[17],Temp[17])
Temp[21] = NAND(Temp[19],Temp[19])
Temp[22] = NAND(Temp[20],Temp[21])
Temp[23] = NAND(X[1],X[3])
Temp[24] = NAND(X[1],Temp[23])
Temp[25] = NAND(X[3],Temp[23])
Temp[26] = NAND(Temp[24],Temp[25])
Temp[27] = NAND(Temp[22],Temp[26])
Temp[28] = NAND(Temp[22],Temp[27])
Temp[29] = NAND(Temp[26],Temp[27])
Y[1] = NAND(Temp[28],Temp[29])
Temp[31] = NAND(Temp[22],X[1])
Temp[32] = NAND(Temp[31],Temp[31])
Temp[33] = NAND(X[1],X[3])
Temp[34] = NAND(Temp[33],Temp[33])
Temp[35] = NAND(Temp[32],Temp[32])
Temp[36] = NAND(Temp[34],Temp[34])
Temp[37] = NAND(Temp[35],Temp[36])
Temp[38] = NAND(Temp[22],X[3])
Temp[39] = NAND(Temp[38],Temp[38])
Temp[40] = NAND(Temp[37],Temp[37])
Temp[41] = NAND(Temp[39],Temp[39])
Y[2] = NAND(Temp[40],Temp[41])
```

Which corresponds to the following circuit:

![](../figure/add2bitcirc.png){#figid .class width=300px height=300px} \

By going through the above program carefully and accounting for the number of gates, we can see that it yields a proof of the following theorem (see also [addnumoflinesfig](){.ref}):

> # {.theorem title="Addition using NAND-CIRC programs" #addition-thm}
For every $n$, let $ADD_n:\{0,1\}^{2n}\rightarrow \{0,1\}^{n+1}$ be the function that, given $x,x'\in \{0,1\}^n$ computes the representation of the sum of the numbers that $x$ and $x'$ represent. Then there is a NAND-CIRC program that computes the function $ADD_n$. Moreover, the number of lines in this program is smaller than $20n$.


![The number of lines in our NAND-CIRC program to add two $n$ bit numbers, as a function of $n$, for $n$'s between $1$ and $100$.](../figure/addnumberoflines.png){#addnumoflinesfig .class width=300px height=300px}


Once we have addition, we can use the grade-school algorithm to obtain multiplication as well, thus obtaining the following theorem:


> # {.theorem title="Multiplication NAND-CIRC programs" #theoremid}
For every $n$, let $MULT_n:\{0,1\}^{2n}\rightarrow \{0,1\}^{2n}$ be the function that, given $x,x'\in \{0,1\}^n$ computes the representation of the product of the numbers that $x$ and $x'$ represent. Then there is a NAND-CIRC program that computes the function $MULT_n$. Moreover, the number of lines in this program is smaller than $1000n^2$.

We omit the proof, though in [multiplication-ex](){.ref} we ask you to supply a "constructive proof" in the form of a program (in your favorite programming language) that on input a number $n$, outputs the code of a NAND-CIRC program of at most $1000n^2$ lines that computes the $MULT_n$ function.
In fact, we can use Karatsuba's algorithm to show that there is a NAND-CIRC program of $O(n^{\log_2 3})$ lines to compute $MULT_n$ (and one can even get further asymptotic improvements using the newer algorithms).


## The LOOKUP function

We have seen that NAND-CIRC programs can add and multiply numbers.  But can they compute other type of functions, that have nothing to do with arithmetic?
Here is one example:


> # {.definition title="Lookup function" #lookup-def}
For every $k$, the _lookup_ function $LOOKUP_k: \{0,1\}^{2^k+k}\rightarrow \{0,1\}$ is defined as follows:
For every $x\in\{0,1\}^{2^k}$ and $i\in \{0,1\}^k$,
$$
LOOKUP_k(x,i)=x_i
$$
where $x_i$ denotes the $i^{th}$ entry of $x$, using the binary representation to identify $i$ with a number in $\{0,\ldots,2^k - 1 \}$.

The function $LOOKUP_1: \{0,1\}^3 \rightarrow \{0,1\}$ maps $(x_0,x_1,i) \in \{0,1\}^3$ to $x_i$.
It is actually the same as the $IF$/$MUX$ function we have seen above, that has a 4 line NAND-CIRC program.
However, can we compute higher levels of $LOOKUP$?
This turns out to be the case:

># {.theorem title="Lookup function" #lookup-thm}
For every $k$, there is a NAND-CIRC program that computes the function $LOOKUP_k: \{0,1\}^{2^k+k}\rightarrow \{0,1\}$. Moreover, the number of lines in this program is at most  $4\cdot 2^k$.

As a corollary,  for every $k>0$, $LOOKUP_k$ can be computed by a Boolean circuit (with AND, OR and NOT gates) of at most $8 \cdot 2^k$.




### Constructing a NAND-CIRC program for $LOOKUP$

We now prove [lookup-thm](){.ref}.
The idea is actually quite simple.
Consider the function $LOOKUP_3 : \{0,1\}^{2^3+3} \rightarrow \{0,1\}$ that takes a an input of $8+3=11$ bits and output a single bit.
We can write this function in pseudocode as follows:

```python
def LOOKUP_3(X[0],X[1],X[2],X[3],X[4],X[5],X[6],X[7],i[0],i[1],i[8]):
    if i == (0,0,0): return X[0]
    if i == (0,0,1): return X[1]
    if i == (0,1,0): return X[2]
    ...
    if i == (1,1,1): return X[7]
```

A condition such as `i==(0,1,0)` can be expanded out to the AND of `NOT(i[0])`, `i[1]` and `NOT(i[2])` and each one of these `AND` and `NOT` gates can be then translated into `NAND`.
The above can yield a proof of a version of [lookup-thm](){.ref} with a slightly larger number of gates, but if we are a little more careful we can prove the theorem with the number of gates as stated.


Specifically, we will prove [lookup-thm](){.ref} by induction.
We will do so by induction.
That is, we show how to use a NAND-CIRC program for computing $LOOKUP_k$ to compute $LOOKUP_{k+1}$.
For the  case $k=1$, $LOOKUP_1$ is the same as `IF` for which we given a NAND-CIRC program with four line.

Now let us consider the case of $k=2$.
Given input $x=(x_0,x_1,x_2,x_3)$ for $LOOKUP_2$ and an index $i=(i_0,i_1)$, if the most significant bit $i_0$ of the index  is $0$ then $LOOKUP_2(x,i)$ will equal $x_0$ if $i_1=0$ and equal $x_1$ if $i_1=1$.
Similarly, if the most significant bit $i_0$ is $1$ then $LOOKUP_2(x,i)$ will equal $x_2$ if $i_1=0$ and will equal $x_3$ if $i_1=1$.
Another way to say this is that we can write $LOOKUP_2$ as follows:

```python
def LOOKUP2(X[0],X[1],X[2],X[3],i[0],i[1]):
    if i[0]==1:
        return LOOKUP1(X[2],X[3],i[1])
    else:
        return LOOKUP1(X[0],X[1],i[1])
```

or in other words,

```python
def LOOKUP2(X[0],X[1],X[2],X[3],i[0],i[1]):
    a = LOOKUP1(X[2],X[3],i[1])
    b = LOOKUP1(X[0],X[1],i[1])
    return IF( i[0],a,b)
```

Similarly, we can write


```python
def LOOKUP3(X[0],X[1],X[2],X[3],X[4],X[5],X[6],X[7],i[0],i[1],i[2]):
    a = LOOKUP2(X[3],X[4],X[5],X[6],i[1],i[2])
    a = LOOKUP2(X[0],X[1],X[2],X[3],i[1],i[2])
    return IF( i[0],a,b)
```

and so on and so forth.
Generally, we can compute $LOOKUP_k$ using two invocations of $LOOKUP_{k-1}$ and one invocation of $IF$, which yields the following lemma:

> # {.lemma title="Lookup recursion" #lookup-rec-lem}
For every $k \geq 2$, $LOOKUP_k(x_0,\ldots,x_{2^k-1},i_0,\ldots,i_{k-1})$
is equal to
$$
IF(i_0,LOOKUP_{k-1}(x_0,\ldots,x_{2^{k-1}-1},i_1,\ldots,i_{k-1}), LOOKUP_{k-1}(x_{2^{k-1}},\ldots,x_{2^k-1},i_1,\ldots,i_{k-1}))
$$

> # {.proof data-ref="lookup-rec-lem"}
If the most significant bit $i_{0}$  of $i$ is zero, then the index $i$ is in $\{0,\ldots,2^{k-1}-1\}$ and hence we can perform the lookup on the "first half" of $x$ and  the result of  $LOOKUP_k(x,i)$ will be the same as $a=LOOKUP_{k-1}(x_0,\ldots,x_{2^{k-1}-1},i_1,\ldots,i_{k-1})$.
On the other hand, if this most significant bit $i_{0}$  is equal to $1$, then the index is in $\{2^{k-1},\ldots,2^k-1\}$, in which case the result of $LOOKUP_k(x,i)$ is the same as $b=LOOKUP_{k-1}(x_{2^{k-1}},\ldots,x_{2^k-1},i_1,\ldots,i_{k-1})$.
Thus we can compute $LOOKUP_k(x,i)$ by first computing $a$ and $b$ and then outputting $IF(i_{k-1},a,b)$.


[lookup-rec-lem](){.ref} directly implies [lookup-thm](){.ref}.
We prove by induction on $k$ that there is a NAND-CIRC program of at most $4\cdot 2^k$ lines for $LOOKUP_k$.
For $k=1$ this follows by the  four line program for $IF$ we've seen before.
For $k>1$, we use the following pseudocode

```python
a = LOOKUP_(k-1)(X[0],...,X[2^(k-1)-1],i[1],...,i[k-1])
b = LOOKUP_(k-1)(X[2^(k-1)],...,Z[2^(k-1)],i[1],...,i[k-1])
return  IF(i[k-1],a,b)
```

If we let $L(k)$ be the number of lines required for $LOOKUP_k$, then the above shows that
$$
L(k) \leq 2L(k-1)+4 \;. \label{induction-lookup}
$$
which solves for $L(k) \leq 4(2^k-1)$.
(See [lookuplinesfig](){.ref} for a plot of the actual number of lines in our implementation of $LOOKUP_k$.)

![The number of lines in our implementation of  the `LOOKUP_k` function as a function of $k$ (i.e., the length of the index). The number of lines in our implementation is roughly $3 \cdot 2^k$.](../figure/lookup_numlines.png){#lookuplinesfig .class width=300px height=300px}

## Computing _every_ function

At this point we know the following facts about NAND-CIRC programs:

1. They can compute at least some non trivial functions.

2. Coming up with NAND-CIRC programs for various functions is a very tedious task.

Thus I would not blame the reader if they were not particularly looking forward to a long sequence of examples of functions that can be computed by NAND-CIRC programs.
However, it turns out we are not going to need this, as we can show in one fell swoop that NAND-CIRC programs can compute _every_ finite function:

> # {.theorem title="Universality of NAND" #NAND-univ-thm}
For every $n,m$ and function $f: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a NAND-CIRC program that computes the function $f$. Moreover, there is such a program with at most $O(m 2^n)$ lines.

The implicit constant in the $O(\cdot)$ notation can be shown to be at most $10$.
We also note that the bound of [NAND-univ-thm](){.ref} can be improved to $O(m 2^n/n)$, see
[tight-upper-bound](){.ref}.
Of course, the above means that we can compute every function $f:\{0,1\}^n \rightarrow \{0,1\}^m$ by a NAND circuit (or a Boolean circuit with AND/OR/NOT gates) of size $O(m\cdot 2^n)$

::: { .bigidea #universalaity }
_Every_ finite function can be computed by a large enough Boolean circuit.
:::

### Proof of NAND's Universality

To prove [NAND-univ-thm](){.ref}, we need to give a NAND-CIRC program  for _every_ possible function.
We will restrict our attention to the case of Boolean functions (i.e., $m=1$).
In [mult-bit-ex](){.ref} you will show how to extend the proof for all values of $m$.
A function $F: \{0,1\}^n\rightarrow \{0,1\}$ can be specified by a table of  its values for each one of the $2^n$ inputs.
For example, the table below describes one particular function $G: \{0,1\}^4 \rightarrow \{0,1\}$:^[In case you are curious, this is the function that computes the digits of $\pi$ in the binary basis. Note that as per the convention of this course, if we think of strings as numbers then we right them with the least significant digit first.]


| Input ($x$) | Output ($G(x)$) |
|:------------|:----------------|
| $0000$      | 1               |
| $1000$      | 1               |
| $0100$      | 0               |
| $1100$      | 0               |
| $0010$      | 1               |
| $1010$      | 0               |
| $0110$      | 0               |
| $1110$      | 1               |
| $0001$      | 0               |
| $1001$      | 0               |
| $0101$      | 0               |
| $1101$      | 0               |
| $0011$      | 1               |
| $1011$      | 1               |
| $0111$      | 1               |
| $1111$      | 1               |



 \



We can see that for every $x\in \{0,1\}^4$, $G(x)=LOOKUP_4(1100100100001111,x)$.
Therefore the following is NAND "pseudocode" to compute $G$:




```python
G0000 = 1
G1000 = 1
G0100 = 0
G1100 = 0
G0010 = 1
G1010 = 0
G0110 = 0
G1110 = 1
G0001 = 0
G1001 = 0
G0101 = 0
G1101 = 0
G0011 = 1
G1011 = 1
G0111 = 1
G1111 = 1
Y[0] = LOOKUP(G0000,G1000,G0100,G1100,G0010,
              G1010,G0110,G1110,G0001,G1001,
              G0101,G1101,G0011,G1011,G1111,
              X[0],X[1],X[2],X[3])
```

We can translate this pseudocode into an actual NAND-CIRC program by adding three lines to define variables `zero` and `one` that are initialized to $0$ and $1$ repsectively, and then  replacing a statement such as `Gxxx = 0` with `Gxxx = NAND(one,one)` and a statement such as `Gxxx = 1` with `Gxxx = NAND(zero,zero)`.
The call to `LOOKUP` will be replaced by the NAND-CIRC program that computes $LOOKUP_4$, but we will replace the variables `X[16]`,$\ldots$,`X[19]` in this program with `X[0]`,$\ldots$,`X[3]` and the variables `X[0]`,$\ldots$,`X[15]` with `G000`, $\ldots$, `G1111`.

There was nothing about the above reasoning that was particular to this program. Given every function $F: \{0,1\}^n \rightarrow \{0,1\}$, we can write a NAND-CIRC program that does the following:

1. Initialize $2^n$ variables of the form `F00...0` till `F11...1` so that for every $z\in\{0,1\}^n$,  the variable corresponding to $z$ is assigned the value $F(z)$.

2. Compute $LOOKUP_n$ on the $2^n$ variables initialized in the previous step, with the index variable being the input variables `X[`$\expr{0}$ `]`,...,`X[`$\expr{2^n-1}$ `]`. That is, just like in the pseudocode for `G` above, we use `Y[0] = LOOKUP(F00..00,...,F11..1,X[0],..,x[`$\expr{n-1}$`])`

The total number of lines in the program will be $2^n$ plus the $4\cdot 2^n$ lines that we pay for computing $LOOKUP_n$.
This completes the proof of [NAND-univ-thm](){.ref}.



> # {.remark title="Result in perspective" #discusscomputation}
While [NAND-univ-thm](){.ref} seems striking at first, in retrospect, it is perhaps not that surprising that every finite function can be computed with a NAND-CIRC program. After all, a finite function $F: \{0,1\}^n \rightarrow \{0,1\}^m$ can be represented by simply the list of its  outputs for each one of the $2^n$ input values.
So it makes sense that we could write a NAND-CIRC program of similar size to compute it.
What is more interesting is that  _some_ functions, such as addition and multiplication,  have a much more efficient representation: one that only requires $O(n^2)$ or even smaller number of lines.


### Improving  by a factor of $n$ (optional) {#tight-upper-bound}

By being a little more careful, we can improve the bound of [NAND-univ-thm](){.ref} and show that every function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a NAND-CIRC program of at most $O(m 2^n/n)$ lines.
As before, it is enough to prove the case that $m=1$.

The idea is to use the technique known as _memoization_.
Let $k= \log(n-2\log n)$ (the reasoning behind this choice will become clear later on).
For every $a \in \{0,1\}^{n-k}$ we define $F_a:\{0,1\}^k \rightarrow \{0,1\}$ to be the function that maps $w_0,\ldots,w_{k-1}$ to $F(a_0,\ldots,a_{n-k-1},w_0,\ldots,w_{k-1})$.

On input $x=x_0,\ldots,x_{n-1}$, we can compute $F(x)$ as follows:
First we  compute a $2^{n-k}$ long string $P$ whose $a^{th}$ entry (identifying $\{0,1\}^{n-k}$ with $[2^{n-k}]$) equals $F_a(x_{n-k},\ldots,x_{n-1})$.
One can verify that $F(x)=LOOKUP_{n-k}(P,x_0,\ldots,x_{n-k-1})$.
Since we can compute $LOOKUP_{n-k}$ using $O(2^{n-k})$ lines, if we can compute the string $P$ (i.e., compute variables `P_`$\expr{0}$, ..., `P_`$\expr{2^{n-k}-1}$) using $T$ lines, then we can compute $F$ in $O(2^{n-k})+T$ lines.

The trivial way to compute the string $P$ would be to use $O(2^k)$ lines to compute for every $a$ the map $x_0,\ldots,x_{k-1} \mapsto F_a(x_0,\ldots,x_{k-1})$ as in the proof of [NAND-univ-thm](){.ref}.
Since there are $2^{n-k}$ $a$'s,  that would be a total cost of $O(2^{n-k} \cdot 2^k) = O(2^n)$ which would not improve at all on the bound of [NAND-univ-thm](){.ref}.
However, a more careful observation shows that we are making some _redundant_ computations.
After all, there are only $2^{2^k}$ distinct functions mapping $k$ bits to one bit.
If $a$ and $a'$ satisfy that $F_a = F_{a'}$ then we don't need to spend $2^k$ lines computing both $F_a(x)$ and $F_{a'}(x)$ but rather can only compute the variable `P_`$\expr{a}$ and then copy `P_`$\expr{a}$ to `P_`$\expr{a'}$ using $O(1)$ lines.
Since we have $2^{2^k}$ unique functions, we can bound the total cost to compute $P$ by $O(2^{2^k}2^k)+O(2^{n-k})$.

Now it just becomes a matter of calculation.
By our choice of $k$, $2^k = n-2\log n$ and hence $2^{2^k}=\tfrac{2^n}{n^2}$.
Since $n/2 \leq 2^k \leq n$, we can bound the total cost of computing $F(x)$ (including also the additional $O(2^{n-k})$ cost of computing $LOOKUP_{n-k}$) by $O(\tfrac{2^n}{n^2}\cdot n)+O(2^n/n)$, which is what we wanted to prove.






## The class $SIZE_{n,m}(T)$


We now make a fundamental definition, we let $SIZE_{n,m}(s)$ denote the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$ that can be computed by NAND circuits of at most $s$ gates (or equivalently, by NAND-CIRC programs of at most $s$ lines):

> # {.definition title="Size class" #sizedef}
Let $n,m,s \in \N$ be numbers with $s \geq m$.
The set $SIZE_{n,m}(s)$ denotes the set of all functions $f:\{0,1\}^n \rightarrow \{0,1\}^m$ such that there exists a NAND circuit of at most $s$ gates that computes $f$.
We denote by $SIZE_n(s)$ the set $SIZE_{n,1}(s)$.

While we defined $SIZE_{n,m}(s)$ with respect to NAND gates, we would get essentially the same class if we defined it with respect to AND/OR/NOT gates:

> # {.lemma #nandaonsizelem}
Let $SIZE^{AON}_{n,m,s}$ denote the set of all functions $f:\{0,1\}^n \rightarrow \{0,1\}^m$ that can be computed by an AND/OR/NOT Boolean circuit  of at most $s$ gates.
Then,
$$
SIZE_{n,m}(s/2) \subseteq SIZE^{AON}_{n,m}(s) \subseteq SIZE_{n,m}(3s)
$$

::: {.proof data-ref="nandaonsizelem"}
If $f$ can be computed by a NAND circuit of at most $s/2$ gates, then by replacing each NAND with the two gates NOT and AND, we can obtain an AND/OR/NOT Boolean circuit  of at most $s$ gates that computes $f$.
On the other hand, if $f$ can be computed by a Boolean AND/OR/NOT circuit of at most $s$ gates, then by [NANDuniversamthm](){.ref} it can be computed by a NAND circuit of at most $3s$ gates.
:::




![A "category error" is a question such as "is a cucumber even or odd?" which does not even make sense. In this book the category errors one needs to watch out for are confusing _functions_ and _programs_ (i.e., confusing _specifications_ and _implementations_). If $C$ is a circuit or program, then asking if $C \in SIZE_{n,1}(s)$ is a category error, since $SIZE_{n,1}(s)$ is a set of _functions_ and not programs or circuits.](../figure/cucumber.png){#cucumberfig .class width=300px height=300px}


The results we've seen before can be phrased as showing  that $ADD_n \in SIZE_{2n,n+1}(100 n)$
and $MULT_n \in SIZE_{2n,2n}(10000 n^{\log_2 3})$.
[NAND-univ-thm](){.ref} shows that  $SIZE_{n,m}(4 m 2^n)$ is equal the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$.
See [sizeclassesfig](){.ref}.

> # { .pause }
Note that $SIZE_{n,m}(s)$ does __not___  correspond to a set of programs!
Rather, it is a set of _functions_ (see [cucumberfig](){.ref}).
This distinction between _programs_ and _functions_ will be crucial for us in this course.
You should always remember that while a program _computes_ a function, it is not _equal_ to a function.
In particular, as we've seen, there can be more than one program to compute the same function.


![A rough illustration of the relations between the different classes of functions computed by NAND-CIRC programs of given size. For every $n,m$, the class $SIZE_{n,m}(s)$ is a subset of the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$, and if $s \leq s'$ then $SIZE_{n,m}(s) \subseteq SIZE_{n,m}(s')$. [NAND-univ-thm](){.ref} shows that $SIZE_{n,m}(O(m\cdot 2^n))$ is equal to the set of all functions, and using [tight-upper-bound](){.ref} this can be improved to $O(m \cdot 2^n/n)$. If we consider all functions mapping $n$ bits to $n$ bits, then addition of two $n/2$ bit numbers can be done in $O(n)$ lines, while we don't know of such a program for _multiplying_ two $n$ bit numbers, though we do know it can be done in $O(n^2)$ and in fact even better size. In the above  $FACTOR_n$ corresponds to the inverse problem of multiplying- finding the _prime factorization_ of a given number. At the moment  we do not know  of any NAND-CIRC program with a polynomial (or even sub-exponential) number of lines that can compute $FACTOR_n$. ](../figure/sizeclasses.png){#sizeclassesfig .class width=300px height=300px}



:::  {.remark title="Finite vs infinite functions" #infinitefunc}
A NAND-CIRC program $P$ can only compute a function with a certain number $n$ of inputs and a certain number $m$ of outputs. Hence for example there is no single NAND-CIRC program that can compute the increment function $INC:\{0,1\}^* \rightarrow \{0,1\}^*$ that maps a string $x$ (which we identify with a number via the binary representation) to the string that represents $x+1$. Rather for every $n>0$, there is a NAND-CIRC program $P_n$ that computes the restriction $INC_n$ of the function $INC$ to inputs of length $n$. Since it can be shown that for every $n>0$ such a program $P_n$ exists of length at most $10n$, $INC_n \in SIZE(10n)$ for every $n>0$.

If $T:\N \rightarrow \N$ and $F:\{0,1\}^* \rightarrow \{0,1\}^*$, we will sometimes slightly abuse notation and write $F \in SIZE(T(n))$ to indicate that for every $n$ the restriction $F_{\upharpoonright n}$ of $F$ to inputs in $\{0,1\}^n$ is in $SIZE(T(n))$. Hence we can write $INC \in SIZE(10n)$. We will come back to this issue of finite vs infinite functions later in this course.
:::


::: {.solvedexercise title="$SIZE$ closed under complement." #sizeclosundercomp}
In this exercise we prove a certain "closure property" of the class $SIZE_n(s)$.
That is, we show that if $f$ is in this class then (up to some small additive term) so is the complement of $f$, which is the function $g(x)=1-f(x)$.

Prove that there is a constant $c$ such that for every $f:\{0,1\}^n \rightarrow \{0,1\}$ and $s\in \N$, if $f \in SIZE_n(s)$  then $1-f \in SIZE_n(s+c)$.
:::

::: {.solution data-ref="sizeclosundercomp"}
If $f\in SIZE(s)$ then there is an $s$-line NAND-CIRC program $P$ that computes $f$.
We can rename the variable `Y[0]` in $P$ to a  variable `temp` and add the line

```python
Y[0] = NAND(temp,temp)
```

at the very end to obtain a program $P'$ that computes $1-f$.
:::



> # { .recap }
* We can define the notion of computing a function via a simplified "programming language", where computing a function $F$ in $T$ steps would correspond to having a $T$-line NAND-CIRC program that computes $F$.
* While the NAND-CIRC programming only has one operation, other operations such as functions and conditional execution can be implemented using it.
* Every function $f:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a circuit  of at most $O(m 2^n)$ gates (and in fact at most $O(m 2^n/n)$ gates).
* Sometimes (or maybe always?) we can translate an _efficient_ algorithm to compute $f$ into a circuit that computes $f$  with a  number of gates comparable to the number of steps in this algorithm.



## Exercises



::: {.exercise title="Pairing" #embedtuples-ex}
This exercise asks you to give a one-to-one map from $\N^2$ to $\N$. This can be useful to implement two-dimensional arrays as "syntacic sugar" in programming languages that only have one-dimensional array.

1. Prove that the map $F(x,y)=2^x3^y$ is a one-to-one map from $\N^2$ to $\N$.

2. Show that there is a one-to-one map $F:\N^2 \rightarrow \N$ such that for every $x,y$, $F(x,y) \leq 100\cdot \max\{x,y\}^2+100$.

3. For every $k$, show that there is  a one-to-one map $F:\N^k \rightarrow \N$ such that for every $x_0,\ldots,x_{k-1} \in \N$, $F(x_0,\ldots,x_{k-1}) \leq 100 \cdot (x_0+x_1+\ldots+x_{k-1}+100k)^k$.
:::

::: {.exercise title="Computing MUX" #mux-ex}
Prove that the NAND-CIRC program below computes the function $MUX$ (or $LOOKUP_1$) where $MUX(a,b,c)$ equals $a$ if $c=0$ and equals $b$ if $c=1$:

```python
t = NAND(X[2],X[2])
u = NAND(X[0],t)
v = NAND(X[1],X[2])
Y[0] = NAND(u,v)
```
:::


> # {.exercise title="At least two / Majority" #atleasttwo-ex}
Give a NAND-CIRC program of at most 6 lines to compute  $MAJ:\{0,1\}^3 \rightarrow \{0,1\}$
where $MAJ(a,b,c) = 1$ iff $a+b+c \geq 2$.

> # {.exercise title="Conditional statements" #conditional-statements}
In this exercise we will show that even though the NAND-CIRC programming language does not have an `if .. then .. else ..` statement, we can still implement it.
Suppose that there is an $s$-line NAND-CIRC program to compute $f:\{0,1\}^n \rightarrow \{0,1\}$ and an $s'$-line NAND-CIRC program to compute $f':\{0,1\}^n \rightarrow \{0,1\}$.
Prove that there is a program of at most $s+s'+10$ lines to compute the function $g:\{0,1\}^{n+1} \rightarrow \{0,1\}$ where $g(x_0,\ldots,x_{n-1},x_n)$ equals $f(x_0,\ldots,x_{n-1})$ if $x_n=0$ and equals $f'(x_0,\ldots,x_{n-1})$ otherwise.



> # {.exercise title="Addition" #addition-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND-CIRC program that computes $ADD_n$. Can you ensure that the program it outputs for $ADD_n$ has fewer than $10n$ lines?

> # {.exercise title="Multiplication" #multiplication-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND-CIRC program that computes $MULT_n$. Can you ensure that the program it outputs for $MULT_n$ has fewer than $1000\cdot n^2$ lines?

> # {.exercise title="Efficient multiplication (challenge)" #eff-multiplication-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND-CIRC program that computes $MULT_n$ and has at most $10000 n^{1.9}$ lines.^[__Hint:__ Use Karatsuba's algorithm] What is the smallest number of lines you can use to multiply two 2048 bit numbers?


::: {.exercise title="Multibit function" #mult-bit-ex}
 Prove that

a. If there is an $s$-line NAND-CIRC program to compute $f:\{0,1\}^n \rightarrow \{0,1\}$ and an $s'$-line NAND-CIRC program to compute $f':\{0,1\}^n \rightarrow \{0,1\}$ then there is an $s+s'$-line program to compute the function $g:\{0,1\}^n \rightarrow \{0,1\}^2$ such that $g(x)=(f(x),f'(x))$.

b. For every function $f:\{0,1\}^n \rightarrow \{0,1\}^m$, there is a NAND-CIRC program of at most $10m\cdot 2^n$ lines that computes $f$.
:::


## Bibliographical notes


See Jukna's  and Wegener's books [@Jukna12, @wegener1987complexity] for much more extensive discussion on circuits.
Shannon showed that every Boolean function can be computed by a circuit of exponential size [@Shannon1938]. The improved bound of $O(2^n/n)$ is due to Lupanov [@Lupanov1958].
