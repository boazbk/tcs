---
title: "Syntactic sugar, and computing every function"
filename: "lec_03a_computing_every_function"
chapternum: "4"
---


# Syntactic sugar, and computing every function {#finiteuniversalchap }

> ### { .objectives }
* Get comfort with syntactic sugar or automatic translation of higher level logic to low level gates. \
* Learn proof of major result: every finite function can be computed by a Boolean circuit. \
* Start thinking _quantitatively_ about number of lines required for computation.



>_"[In 1951] I had a running compiler and nobody would touch it because, they carefully told me, computers could only do arithmetic; they could not do programs."_,  Grace Murray Hopper, 1986.


>_"Syntactic sugar causes cancer of the semicolon."_, Alan Perlis, 1982.




The computational models we considered thus far are as "bare bones" as they come.
For example, our NAND-CIRC "programming language" has only the single operation `foo = NAND(bar,blah)`.
In this chapter we will  see that these simple models are actually _equivalent_ to more powerful ones.
The key observation is that we can implement more complex features using our basic building blocks, and then use these new features themselves as building blocks for even more sophisticated features.
This is known as "syntactic sugar" in the field of programming language design, since we are not modifying the underlying programming model itself but rather we merely implement new features by syntactically transforming a program that uses such features into one that doesn't.


This chapter provides a "toolkit" that can be used to show that many functions can be computed by  NAND-CIRC programs, and hence also by Boolean circuits.
We will also use this toolkit to prove a fundamental theorem: _every_ finite function $f:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a Boolean circuit, see [circuit-univ-thm](){.ref} below.
While the syntactic sugar toolkit is important in its own right, [circuit-univ-thm](){.ref} can also be proven directly without using this toolkit.
We present this alternative proof in [seccomputalternative](){.ref}.
See [computefuncoverviewfig](){.ref} for an outline of the results of this chapter.



![An outline of the results of this chapter. In [secsyntacticsugar](){.ref} we give a toolkit of "syntactic sugar" transformations showing how to implement features such as programmer-defined functions and conditional statements in NAND-CIRC. We use these tools in [seclookupfunc](){.ref}  to give a NAND-CIRC program (or alternatively a Boolean circuit) to compute the  $LOOKUP$ function. We then build on this result to show in [seccomputeallfunctions](){.ref} that NAND-CIRC programs (or equivalently, Boolean circuits) can compute _every_ finite function. An alternative direct proof of the same result is given in [seccomputalternative](){.ref}.](../figure/compute_every_function_overview.png){#computefuncoverviewfig  }









## Some examples of syntactic sugar  { #secsyntacticsugar }

We now present some examples of "syntactic sugar" transformations that we can use in constructing straightline programs or circuits.
We focus on the _straight-line programming language_ view of our computational models, and specifically(for the sake of concreteness) on the NAND-CIRC programming language.
This convenient is because many of the syntactic sugar transformations we present are easiest to think about in terms of applying "search and replace" operations to the source code of a program.
However,  by [equivalencemodelsthm](){.ref}, all of our results hold equally well for circuits, whether ones using NAND gates or Boolean circuits that use the  AND, OR, and NOT operations.
Enumerating the examples of such  syntactic sugar transformations can be a little tedious, but we do it for two reasons:

1. To convince you that despite their seeming simplicity and limitations, simple models such as Boolean circuits or  the NAND-CIRC programming language are actually quite powerful.

2. So you can realize how lucky you are to be taking a theory of computation course and not a compilers course... `:)`









### User-defined procedures

One staple of almost any programming language is the ability to define and then execute _procedures_ or _subroutine_.
(These are often  known as _functions_ in some programming languages, but we prefer the names _procedures_ 
to avoid confusion with the function that a program computes.)
The NAND-CIRC programming language does not have this mechanism built in.
However, we can achieve the same effect using the time honored technique of  "copy and paste".
Specifically, we can replace code which defines a procedure such as

```python
def Proc(a,b):
    proc_code
    return c
some_code
f = Proc(e,d)
some_more_code
```

with the following code where we "paste" the code of `Proc`

```python
some_code
proc_code'
some_more_code
```

and where `proc_code'` is obtained by replacing all occurrences of `a` with `d`,`b` with `e`, `c` with `f`.
When doing that we will need to ensure that all other variables appearing in `proc_code'` don't interfere with other variables.
We can always do so by renaming variables to new names that were not used before.
The above reasoning leads to the proof of the following theorem:

> ### {.theorem title="Procedure definition synctatic sugar" #functionsynsugarthm}
Let NAND-CIRC-PROC be the programming language NAND-CIRC augmented with the syntax above for defining procedures.
Then for every NAND-CIRC-PROC program $P$, there exists a standard (i.e., "sugar free") NAND-CIRC program $P'$ that computes the same function as $P$.


[functionsynsugarthm](){.ref} can be proven using the transformation above, but since the formal proof is somewhat long and tedious, we omit it here.
program that does not use them.


::: {.example title="Computing Majority from NAND using syntactic sugar" #majcircnand}
Procedures allow us to express NAND-CIRC programs much more cleanly and succinctly.
For example, because we can compute AND,OR, and NOT using NANDs, we can compute the _Majority_ function as follows:

```python
def NOT(a): 
    return NAND(a,a)
def AND(a,b):
    temp = NAND(a,b) 
    return NOT(temp)
def OR(a,b):
    temp1 = NOT(a)
    temp2 = NOT(b) 
    return NAND(temp1,temp2)

def MAJ(a,b,c):
    and1 = AND(a,b)
    and2 = AND(a,c)
    and3 = AND(b,c)
    or1 = OR(and1,and2)
    return OR(or1,and3)

print(MAJ(0,1,1))
# 1
```

[progcircmajfig](){.ref} presents the "sugar free" NAND-CIRC program (and the corresponding circuit) that is obtained by "expanding out" this program, replacing the calls to procedures with their definitions.
:::



::: { .bigidea #synsugar}
Once we show that a computational model $X$ is equivalent in power to the model with an additional feature $Y$, we can use this feature whenever we need to show that some function $f$ is computable by $X$.
:::




![A standard (i.e., "sugar free") NAND-CIRC program that is obtained by expanding out the procedure definitions in the program for Majority of [majcircnand](){.ref}. The corresponding circuit is on the right. Note that this is not the most efficient NAND circuit/program for majority: we can save on some gates by "short cutting" steps where a gate $u$ computes $NAND(v,v)$ and then a gate $w$ computes $NAND(u,u)$ (as indicated by the dashed green arrows in the above figure).](../figure/progcircmaj.png){#progcircmajfig}





::: {.remark title="Counting lines" #countinglines}
While we can use syntactic sugar to _present_ NAND-CIRC programs in more readable ways, we did not change the definition of the language itself.
Therefore, whenever we say that some function $f$ has an $s$-line NAND-CIRC program we mean a standard "sugar free" NAND-CIRC program, where all syntactic sugar has been expanded out.
For example, the program of [majcircnand](){.ref} is a $12$-line program for computing the $MAJ$ function, even though it can be written in fewer lines using the procedure definition syntactic sugar.
:::



### Proof by Python (optional) { #functionsynsugarthmpython }

We can write a Python program that implements the proof of [functionsynsugarthm](){.ref}.
This is a Python program that takes a  NAND-CIRC-PROC program $P$ that includes procedure definitions and uses simple "search and replace" to transform $P$ into a standard (i.e., "sugar free") NAND-CIRC program $P'$ that computes the same function as $P$ without using any procedures.
The idea is simple: if the program $P$ contains a definition of a procedure `Proc` of two arguments `x` and `y`, then whenever we see a line of the form `foo = Proc(bar,blah)`, we can replace this line by:


1. The body of the procedure `Proc` (replacing all occurrences of `x` and `y` with `bar` and `blah` respectively).^[If some of the internal variables of `Proc` share the same name with variables used in the program $P$ then we can ensure they are unique by adding some prefix to them. For simplicity, we ignore this issue below.]

2. A line `foo = exp`, where `exp` is the expression following the `return` statement in the definition of the procedure `Proc`.

To make this more robust we  a prefix to the internal variables used by `Proc` to ensure they don't conflict with the variables of $P$; for simplicity we ignore this issue in the code below though it can be easily added.

The code in [desugarcode](){.ref} achieves such a  transformation:^[This code uses _regular expressions_ to make the search and replace parts a little easier. We will see the theoretical basis for regular expressions in [restrictedchap](){.ref}.]

``` { .python .full #desugarcode title="Python code for transforming NAND-CIRC-PROC programs into standard sugar free NAND-CIRC programs." }
import re
def desugar(code,proc_name, proc_args,proc_body):
"""Use `search and replace' to remove procedure calls.  
   Replace line of form 'foo = proc_name(a,b)' with 
      proc_body[x->a,y->b]
      foo = exp
    where last line of proc_body is 'return exp'"""
    # regexp for list of variable names separated by commas
    arglist = ",".join([r"([a-zA-Z0-9\_\[\]]+)" for i in range(len(proc_args))])
    # regexp for "variable = proc_name(arguments)"
    regexp = fr'([a-zA-Z0-9\_\[\]]+)\s*=\s*{proc_name}\({arglist}\)\s*$'
    m = re.search(regexp,code, re.MULTILINE)
    if not m: return code # if no match then there's nothing to do
    newcode = proc_body 
    # replace arguments by  variables from invocation
    for i in range(len(proc_args)): 
        newcode = newcode.replace(proc_args[i],m.group(i+2))    
    # Splice the new code inside
    newcode = newcode.replace('return',m.group(1)+" = ")
    newcode = code[:m.start()] + newcode + code[m.end()+1:]
    # Continue recursively to check for more matches
    return desugar(newcode,proc_name,proc_args,proc_body)
```

[progcircmajfig](){.ref} shows the result of applying the code of [desugarcode](){.ref} to the program of [majcircnand](){.ref} that uses syntactic sugar to compute the Majority function.
Specifically, we first apply `desugar` to remove usage of the OR function, then apply it to remove usage of the AND function, and finally apply it a third time to remove usage of the NOT function.


::: {.remark title="Parsing function definitions (optional)" #parsingdeg}
The function `desugar` in [desugarcode](){.ref} assumes that it is given the procedure already split up into its name, arguments, and body.
It is not crucial for our purposes to describe precisely to scan a definition and splitting it up to these components, but in case you are curious, it can be achieved in Python via the following code:

```python
def parse_func(code):
    """Parse a procedure definition into name, arguments and body"""
    lines = [l.strip() for l in code.split('\n')]
    regexp = r'def\s+([a-zA-Z\_0-9]+)\(([\sa-zA-Z0-9\_,]+)\)\s*:\s*'
    m = re.match(regexp,lines[0])
    return m.group(1), m.group(2).split(','), '\n'.join(lines[1:])
```
:::







### Conditional statements {#ifstatementsec }

Another sorely missing feature in NAND-CIRC is a conditional statement such as the `if`/`then` constructs that are found in many programming languages.
However, using procedure, we can obtain an ersatz if/then construct.
First we can compute the function $IF:\{0,1\}^3 \rightarrow \{0,1\}$ such that $IF(a,b,c)$ equals $b$ if $a=1$ and $c$ if $a=0$.

> ### { .pause }
Before reading onward, try to see how you could compute the $IF$ function using $NAND$'s.
Once you you do that, see how you can use that to emulate `if`/`then` types of constructs.

The $IF$ function can be implemented from NANDs as follows (see [mux-ex](){.ref}):

```python
def IF(cond,a,b):
    notcond = NAND(cond,cond)
    temp = NAND(b,notcond)
    temp1 = NAND(a,cond)
    return NAND(temp,temp1)
```

The $IF$ function is also known as the _multiplexing_ function, since $cond$ can be thought of as a switch that controls whether the output is connected to $a$ or $b$.
Once we have a procedure for computing the $IF$ function, we can implement conditionals in NAND.
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

Using such transformations, we can prove the following theorem.
Once again we omit the (not too insightful) full formal proof, though see [conditionalsugarthmex](){.ref} for some hints on how to obtain it.

> ### {.theorem title="Conditional statements synctatic sugar" #conditionalsugarthm }
Let NAND-CIRC-IF be the programming language NAND-CIRC augmented with `if`/`then`/`else` statements for allowing code to be conditionally executed based on whether a veriable is equal to $0$ or $1$.  
Then for every NAND-CIRC-IF program $P$, there exists a standard (i.e., "sugar free") NAND-CIRC program $P'$ that computes the same function as $P$.








## Extended example: Addition and Multiplication (optional) { #addexample }


Using "syntactic sugar",  we can write the integer addition function as follows:

```python
# Add two n-bit integers
# Use LSB first notation for simplicity
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
By expanding out all the features, for every value of $n$ we can translate the above program into a standard ("sugar free") NAND-CIRC program. [add2bitnumbersfig](){.ref} depicts what we get for $n=2$.

![The NAND-CIRC program and corresponding NAND circuit for adding two-digit binary numbers that are obtained by "expanding out" all the syntactic sugar. The program/circuit has 43 lines/gates which is by no means necessary. It is possible to add $n$ bit numbers using $9n$ NAND gates, see [halffulladderex](){.ref}.](../figure/add2bitnumbers.png){#add2bitnumbersfig .class  }

By going through the above program carefully and accounting for the number of gates, we can see that it yields a proof of the following theorem (see also [addnumoflinesfig](){.ref}):

> ### {.theorem title="Addition using NAND-CIRC programs" #addition-thm}
For every $n\in \N$, let $ADD_n:\{0,1\}^{2n}\rightarrow \{0,1\}^{n+1}$ be the function that, given $x,x'\in \{0,1\}^n$ computes the representation of the sum of the numbers that $x$ and $x'$ represent. Then there is a constant $c \leq 30$ such that for every $n$ there is a NAND-CIRC program of at most $c$ lines computing $ADD_n$.^[The value of $c$ can be improved to $9$, see   [halffulladderex](){.ref}.]


![The number of lines in our NAND-CIRC program to add two $n$ bit numbers, as a function of $n$, for $n$'s between $1$ and $100$. This is not the most efficient program for this task, but the important point is that it has the form $O(n)$.](../figure/addnumberoflines.png){#addnumoflinesfig .margin  }


Once we have addition, we can use the grade-school algorithm to obtain multiplication as well, thus obtaining the following theorem:


> ### {.theorem title="Multiplication using NAND-CIRC programs" #theoremid}
For every $n$, let $MULT_n:\{0,1\}^{2n}\rightarrow \{0,1\}^{2n}$ be the function that, given $x,x'\in \{0,1\}^n$ computes the representation of the product of the numbers that $x$ and $x'$ represent. Then there is a constant $c$ such that for every $n$, there is a NAND-CIRC program of at most $cn^2$ that computes the function $MULT_n$.

We omit the proof, though in [multiplication-ex](){.ref} we ask you to supply a "constructive proof" in the form of a program (in your favorite programming language) that on input a number $n$, outputs the code of a NAND-CIRC program of at most $1000n^2$ lines that computes the $MULT_n$ function.
In fact, we can use Karatsuba's algorithm to show that there is a NAND-CIRC program of $O(n^{\log_2 3})$ lines to compute $MULT_n$ 
(and can get even further asymptotic improvements using better algorithms).


## The LOOKUP function { #seclookupfunc }

The $LOOKUP$ function  will play an important role in this chapter and later.
It is defined as follows: 


> ### {.definition title="Lookup function" #lookup-def}
For every $k$, the _lookup_ function of order $k$, $LOOKUP_k: \{0,1\}^{2^k+k}\rightarrow \{0,1\}$ is defined as follows.
For every $x\in\{0,1\}^{2^k}$ and $i\in \{0,1\}^k$,
$$
LOOKUP_k(x,i)=x_i
$$
where $x_i$ denotes the $i^{th}$ entry of $x$, using the binary representation to identify $i$ with a number in $\{0,\ldots,2^k - 1 \}$.

![The $LOOKUP_k$ function takes an input in $\{0,1\}^{2^k+k}$, which we denote by $x,i$ (with $x\in \{0,1\}^{2^k}$ and $i \in \{0,1\}^k$). The output is $x_i$: the $i$-th coordinate of $x$, where we identify $i$ as a number in $[k]$ using the binary representation. In the above example $x\in \{0,1\}^{16}$ and $i\in \{0,1\}^4$. Since $i=0110$ is the binary representation of the number $6$, the output of $LOOKUP_4(x,i)$ in this case is $x_6 = 1$.](../figure/lookupfunc.png){#lookupfig}

See [lookupfig](){.ref} for an illustration of the LOOKUP function.
It turns out that for every $k$, we can compute $LOOKUP_k$ using a NAND-CIRC program:

># {.theorem title="Lookup function" #lookup-thm}
For every $k>0$, there is a NAND-CIRC program that computes the function $LOOKUP_k: \{0,1\}^{2^k+k}\rightarrow \{0,1\}$. Moreover, the number of lines in this program is at most  $4\cdot 2^k$.

An immediate corollary of [lookup-thm](){.ref} is that for every $k>0$, $LOOKUP_k$ can be computed by a Boolean circuit (with AND, OR and NOT gates) of at most $8 \cdot 2^k$ gates.




### Constructing a NAND-CIRC program for $LOOKUP$

We  prove [lookup-thm](){.ref} by induction.
For the case $k=1$, $LOOKUP_1$  maps $(x_0,x_1,i) \in \{0,1\}^3$ to $x_i$.
In other words, if $i=0$ then it outputs $x_0$ and otherwise it outputs $x_1$, which (up to reordering variables) is the same as 
the $IF$ function presented in  [ifstatementsec](){.ref}, which can be computed by a 4-line NAND-CIRC program.

As a warm-up for the case of general $k$,  let us consider the case of $k=2$.
Given input $x=(x_0,x_1,x_2,x_3)$ for $LOOKUP_2$ and an index $i=(i_0,i_1)$, if the most significant bit $i_0$ of the index is $0$ then $LOOKUP_2(x,i)$ will equal $x_0$ if $i_1=0$ and equal $x_1$ if $i_1=1$.
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

More generally, as shown in the following lemma,  we can compute $LOOKUP_k$ using two invocations of $LOOKUP_{k-1}$ and one invocation of $IF$:

> ### {.lemma title="Lookup recursion" #lookup-rec-lem}
For every $k \geq 2$, $LOOKUP_k(x_0,\ldots,x_{2^k-1},i_0,\ldots,i_{k-1})$
is equal to
$$
IF(i_0,LOOKUP_{k-1}(x_0,\ldots,x_{2^{k-1}-1},i_1,\ldots,i_{k-1}), LOOKUP_{k-1}(x_{2^{k-1}},\ldots,x_{2^k-1},i_1,\ldots,i_{k-1}))
$$

> ### {.proof data-ref="lookup-rec-lem"}
If the most significant bit $i_{0}$  of $i$ is zero, then the index $i$ is in $\{0,\ldots,2^{k-1}-1\}$ and hence we can perform the lookup on the "first half" of $x$ and the result of  $LOOKUP_k(x,i)$ will be the same as $a=LOOKUP_{k-1}(x_0,\ldots,x_{2^{k-1}-1},i_1,\ldots,i_{k-1})$.
On the other hand, if this most significant bit $i_{0}$  is equal to $1$, then the index is in $\{2^{k-1},\ldots,2^k-1\}$, in which case the result of $LOOKUP_k(x,i)$ is the same as $b=LOOKUP_{k-1}(x_{2^{k-1}},\ldots,x_{2^k-1},i_1,\ldots,i_{k-1})$.
Thus we can compute $LOOKUP_k(x,i)$ by first computing $a$ and $b$ and then outputting $IF(i_{k-1},a,b)$.


__Proof of [lookup-thm](){.ref} from [lookup-rec-lem](){.ref}.__ Now that we have [lookup-rec-lem](){.ref},
we can complete the proof of [lookup-thm](){.ref}. 
We will prove by induction on $k$ that there is a NAND-CIRC program of at most $4\cdot 2^k$ lines for $LOOKUP_k$.
For $k=1$ this follows by the four line program for $IF$ we've seen before.
For $k>1$, we use the following pseudocode

```python
a = LOOKUP_(k-1)(X[0],...,X[2^(k-1)-1],i[1],...,i[k-1])
b = LOOKUP_(k-1)(X[2^(k-1)],...,Z[2^(k-1)],i[1],...,i[k-1])
return IF(i[k-1],a,b)
```

If we let $L(k)$ be the number of lines required for $LOOKUP_k$, then the above pseudo-code shows that
$$
L(k) \leq 2L(k-1)+4 \;. \label{induction-lookup}
$$
which solves for $L(k) \leq 4(2^k-1)$.
See [lookuplinesfig](){.ref} for a plot of the actual number of lines in our implementation of $LOOKUP_k$.

![The number of lines in our implementation of the `LOOKUP_k` function as a function of $k$ (i.e., the length of the index). The number of lines in our implementation is roughly $3 \cdot 2^k$.](../figure/lookup_numlines.png){#lookuplinesfig .margin  }


## Computing _every_ function { #seccomputeallfunctions }

At this point we know the following facts about NAND-CIRC programs (and so equivalently about Boolean circuits and our other equivalent models):

1. They can compute at least some non trivial functions.

2. Coming up with NAND-CIRC programs for various functions is a very tedious task.

Thus I would not blame the reader if they were not particularly looking forward to a long sequence of examples of functions that can be computed by NAND-CIRC programs.
However, it turns out we are not going to need this, as we can show in one fell swoop that NAND-CIRC programs can compute _every_ finite function:

> ### {.theorem title="Universality of NAND" #NAND-univ-thm}
There exists some constant $c>0$ such that for every $n,m>0$ and function $f: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a NAND-CIRC program  with at most $c \cdot m 2^n$ lines that computes the function $f$ .

By [equivalencemodelsthm](){.ref},  the models of NAND circuits, NAND-CIRC programs, AON-CIRC programs, and Boolean circuits, are all equivalent to one another, and hence [NAND-univ-thm](){.ref} holds for all these models.
In particular, the following theorem is equivalent to [NAND-univ-thm](){.ref}:


> ### {.theorem title="Universality of Boolean circuits" #circuit-univ-thm}
There exists some constant $c>0$ such that for every $n,m>0$ and function $f: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a Boolean circuit with at most $c \cdot m 2^n$ gates that computes the function $f$ .

::: { .bigidea #finitecomputation }
_Every_ finite function can be computed by a large enough Boolean circuit.
:::






_Improved bounds._ Though it will not be of great importance to us , it is possible to improve on the proof of 
[NAND-univ-thm](){.ref}  and shave an extra factor of $n$, as well as optimize the constant $c$, and so prove that 
for every $\epsilon>0$, $m\in \N$ and sufficiently large $n$, if $f:\{0,1\}^n \rightarrow \{0,1\}^m$ then $f$ can be computed by a NAND circuit of at most
$(1+\epsilon)\tfrac{m\cdot 2^n}{n}$ gates. 
The proof of this result is beyond the scope of this book, but we do discuss how to obtain a bound of the form $O(\tfrac{m \cdot 2^n}{n})$ in [tight-upper-bound](){.ref}; see also the biographical notes.





### Proof of NAND's Universality

To prove [NAND-univ-thm](){.ref}, we need to give a NAND circuit, or equivalently a NAND-CIRC program,  for _every_ possible function.
We will restrict our attention to the case of Boolean functions (i.e., $m=1$).
[mult-bit-ex](){.ref} asks you  to extend the proof for all values of $m$.
A function $F: \{0,1\}^n\rightarrow \{0,1\}$ can be specified by a table of its values for each one of the $2^n$ inputs.
For example, the table below describes one particular function $G: \{0,1\}^4 \rightarrow \{0,1\}$:^[In case you are curious, this is the function on input $i\in \{0,1\}^4$ (which we interpret as a number in $[16]$), outputs the $i$-th digit of $\pi$ in the binary basis.]


| Input ($x$) | Output ($G(x)$) |
|:------------|:----------------|
| $0000$      | 1               |
| $0001$      | 1               |
| $0010$      | 0               |
| $0011$      | 0               |
| $0100$      | 1               |
| $0101$      | 0               |
| $0110$      | 0               |
| $0111$      | 1               |
| $1000$      | 0               |
| $1001$      | 0               |
| $1010$      | 0               |
| $1011$      | 0               |
| $1100$      | 1               |
| $1101$      | 1               |
| $1110$      | 1               |
| $1111$      | 1               |


Table: An example of a function $G:\{0,1\}^4 \rightarrow \{0,1\}$. {#tablefunctiong}




For every $x\in \{0,1\}^4$, $G(x)=LOOKUP_4(1100100100001111,x)$, and so the following is NAND-CIRC "pseudocode"  to compute $G$ using synctactic sugar for the `LOOKUP_4` procedure.


```python
G0000 = 1
G1000 = 1
G0100 = 0
...
G0111 = 1
G1111 = 1
Y[0] = LOOKUP_4(G0000,G1000,...,G1111,
              X[0],X[1],X[2],X[3])
```


We can translate this pseudocode into an actual NAND-CIRC program by adding three lines to define variables `zero` and `one` that are initialized to $0$ and $1$ respectively,
and then replacing a statement such as `Gxxx = 0` with `Gxxx = NAND(one,one)` and a statement such as `Gxxx = 1` with `Gxxx = NAND(zero,zero)`.
The call to `LOOKUP_4` will be replaced by the NAND-CIRC program that computes $LOOKUP_4$, plugging in the appropriate inputs.

There was nothing about the above reasoning that was particular to the function $G$ of [tablefunctiong](){.ref}.
Given _every_ function $F: \{0,1\}^n \rightarrow \{0,1\}$, we can write a NAND-CIRC program that does the following:

1. Initialize $2^n$ variables of the form `F00...0` till `F11...1` so that for every $z\in\{0,1\}^n$,  the variable corresponding to $z$ is assigned the value $F(z)$.

2. Compute $LOOKUP_n$ on the $2^n$ variables initialized in the previous step, with the index variable being the input variables `X[`$0$ `]`,...,`X[`$2^n-1$ `]`. That is, just like in the pseudocode for `G` above, we use `Y[0] = LOOKUP(F00..00,...,F11..1,X[0],..,x[`$n-1$`])`

The total number of lines in the resulting program is $3+2^n$ lines for initializing the variables plus the $4\cdot 2^n$ lines that we pay for computing $LOOKUP_n$.
This completes the proof of [NAND-univ-thm](){.ref}.



> ### {.remark title="Result in perspective" #discusscomputation}
While [NAND-univ-thm](){.ref} seems striking at first, in retrospect, it is perhaps not that surprising that every finite function can be computed with a NAND-CIRC program. After all, a finite function $F: \{0,1\}^n \rightarrow \{0,1\}^m$ can be represented by simply the list of its outputs for each one of the $2^n$ input values.
So it makes sense that we could write a NAND-CIRC program of similar size to compute it.
What is more interesting is that _some_ functions, such as addition and multiplication,  have a much more efficient representation: one that only requires $O(n^2)$ or even smaller number of lines.


### Improving by a factor of $n$ (optional) {#tight-upper-bound}

By being a little more careful, we can improve the bound of [NAND-univ-thm](){.ref} and show that every function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a NAND-CIRC program of at most $O(m 2^n/n)$ lines.
In other words, we can prove  the following improved version:

> ### {.theorem title="Universality of NAND circuits, improved bound" #NAND-univ-thm-improved}
There exists a constant $c>0$ such that for every $n,m>0$ and function $f: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a NAND-CIRC program  with at most $c \cdot m 2^n / n$ lines that computes the function $f$ .


::: {.proof data-ref="NAND-univ-thm-improved"}
As before, it is enough to prove the case that $m=1$.

The idea is to use the technique known as _memoization_.
Let $k= \log(n-2\log n)$ (the reasoning behind this choice will become clear later on).
For every $a \in \{0,1\}^{n-k}$ we define $F_a:\{0,1\}^k \rightarrow \{0,1\}$ to be the function that maps $w_0,\ldots,w_{k-1}$ to $F(a_0,\ldots,a_{n-k-1},w_0,\ldots,w_{k-1})$.

On input $x=x_0,\ldots,x_{n-1}$, we can compute $F(x)$ as follows:
First we compute a $2^{n-k}$ long string $P$ whose $a^{th}$ entry (identifying $\{0,1\}^{n-k}$ with $[2^{n-k}]$) equals $F_a(x_{n-k},\ldots,x_{n-1})$.
One can verify that $F(x)=LOOKUP_{n-k}(P,x_0,\ldots,x_{n-k-1})$.
Since we can compute $LOOKUP_{n-k}$ using $O(2^{n-k})$ lines, if we can compute the string $P$ (i.e., compute variables `P_`$0$, ..., `P_`$2^{n-k}-1$) using $T$ lines, then we can compute $F$ in $O(2^{n-k})+T$ lines.

The trivial way to compute the string $P$ would be to use $O(2^k)$ lines to compute for every $a$ the map $x_0,\ldots,x_{k-1} \mapsto F_a(x_0,\ldots,x_{k-1})$ as in the proof of [NAND-univ-thm](){.ref}.
Since there are $2^{n-k}$ $a$'s,  that would be a total cost of $O(2^{n-k} \cdot 2^k) = O(2^n)$ which would not improve at all on the bound of [NAND-univ-thm](){.ref}.
However, a more careful observation shows that we are making some _redundant_ computations.
After all, there are only $2^{2^k}$ distinct functions mapping $k$ bits to one bit.
If $a$ and $a'$ satisfy that $F_a = F_{a'}$ then we don't need to spend $2^k$ lines computing both $F_a(x)$ and $F_{a'}(x)$ but rather can only compute the variable `P_`$a$ and then copy `P_`$a$ to `P_`$a'$ using $O(1)$ lines.
Since we have $2^{2^k}$ unique functions, we can bound the total cost to compute $P$ by $O(2^{2^k}2^k)+O(2^{n-k})$.

Now it just becomes a matter of calculation.
By our choice of $k$, $2^k = n-2\log n$ and hence $2^{2^k}=\tfrac{2^n}{n^2}$.
Since $n/2 \leq 2^k \leq n$, we can bound the total cost of computing $F(x)$ (including also the additional $O(2^{n-k})$ cost of computing $LOOKUP_{n-k}$) by $O(\tfrac{2^n}{n^2}\cdot n)+O(2^n/n)$, which is what we wanted to prove.
:::

Using the connection between NAND-CIRC programs and Boolean circuits, an immediate corollary of  [NAND-univ-thm-improved](){.ref} is the following improvement to  [circuit-univ-thm](){.ref}:

> ### {.theorem title="Universality of Boolean circuits,  improved bound" #circuit-univ-thm-improved}
There exists some constant $c>0$ such that for every $n,m>0$ and function $f: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a Boolean circuit with at most $c \cdot m 2^n / n$ gates that computes the function $f$ .


## Computing every function: An alternative proof {#seccomputalternative }

[circuit-univ-thm](){.ref} is a fundamental result in the theory (and practice!) of computation.
In this section we present an alternative proof of this basic fact that Boolean circuits can compute every finite function.
This alternative proof gives somewhat worse quantitative bound on the number of gates but it has the advantage of being simpler, working directly with circuits and avoiding the usage of all the syntactic sugar machinery.
(However, that machinery is useful in its own right, and will find other applications later on.)


> ### {.theorem title="Universality of Boolean circuits (alternative phrasing)" #circuit-univ-alt-thm}
There exists some constant $c>0$ such that for every $n,m>0$ and function $f: \{0,1\}^n\rightarrow \{0,1\}^m$, there is a Boolean circuit with at most $c \cdot m\cdot n 2^n$ gates that computes the function $f$ .

![Given a function $f:\{0,1\}^n \rightarrow \{0,1\}$, we let $\{ x_0, x_1, \ldots, x_{N-1} \} \subseteq \{0,1\}^n$ be the set of inputs such that $f(x_i)=1$, and note that $N \leq 2^n$. We can express $f$ as the OR of $\delta_{x_i}$ for $i\in [N]$ where the function $\delta_\alpha:\{0,1\}^n \rightarrow \{0,1\}$ (for $\alpha \in \{0,1\}^n$) is defined as follows:  $\delta_\alpha(x)=1$ iff $x=\alpha$. We can compute the OR of $N$ values using $N$ two-input OR gates. Therefore if we have a circuit of size $O(n)$ to compute $\delta_\alpha$ for every $\alpha \in \{0,1\}^n$, we can compute $f$ using a circuit of size $O(n \cdot N) = O(n \cdot 2^n)$. ](../figure/computeallfunctionalt.png){#computeallfuncaltfig  }



> ### {.proofidea data-ref="circuit-univ-alt-thm"}
The idea of the proof is illustrated in [computeallfuncaltfig](){.ref}. As before, it is enough to focus on the case that $m=1$ (the function $f$ has a single output), since we can always extend this to the case of $m>1$ by looking at the composition of $m$ circuits each computing a different output bit of the function $f$.
We start by showing that for every $\alpha \in \{0,1\}^n$, there is an $O(n)$ sized circuit that computes the function $\delta_\alpha:\{0,1\}^n \rightarrow \{0,1\}$ defined as follows: $\delta_\alpha(x)=1$ iff $x=\alpha$ (that is. $\delta_\alpha$ outputs $0$ on all inputs except the input $\alpha$). We can then write any function $f:\{0,1\}^n \rightarrow \{0,1\}$ as the OR of at most $2^n$ functions $\delta_\alpha$ for the $\alpha$'s on which $f(\alpha)=1$. 

::: {.proof data-ref="circuit-univ-alt-thm"}
We prove the theorem for the case $m=1$. The result can be extended for $m>1$ as before (see also [mult-bit-ex](){.ref}).
Let $f:\{0,1\}^n \rightarrow \{0,1\}$.
We will prove that there is an $O(n\cdot 2^n)$-sized Boolean circuit to compute $f$ in the following steps:

1. We show that for every $\alpha\in \{0,1\}^n$, there is an $O(n)$ sized circuit that computes the function $\delta_\alpha:\{0,1\}^n \rightarrow \{0,1\}$, where $\delta_\alpha(x)=1$ iff $x=\alpha$.

2. We then show that this implies the existence of an $O(n\cdot 2^n)$-sized circuit that computes $f$, by writing $f(x)$ as the OR of $\delta_\alpha(x)$ for all  $\alpha\in \{0,1\}^n$ such that $f(\alpha)=1$.

We start with Step 1:

__CLAIM:__ For $\alpha \in \{0,1\}^n$, define $\delta_\alpha:\{0,1\}^n$ as follows:
$$
\delta_\alpha(x) = \begin{cases}1 & x=\alpha \\ 0 & \text{otherwise} \end{cases} \;.
$$
then there is a Boolean circuit using at most $2n$ gates that computes $\delta_\alpha$.

__PROOF OF CLAIM:__ The proof is illustrated in [deltafuncfig](){.ref}.
As an example, consider the function $\delta_{011}:\{0,1\}^3 \rightarrow \{0,1\}$.
This function outputs $1$ on $x$ if and only if $x_0=0$, $x_1=1$ and $x_2=1$, and so we can write $\delta_{011}(x) = \overline{x_0} \wedge x_1 \wedge x_2$, which translates into a Boolean circuit with one NOT gate and two AND gates.
More generally, for every $\alpha \in \{0,1\}^n$, we can express $\delta_{\alpha}(x)$  as $(x_0 = \alpha_0) \wedge (x_1 = \alpha_1) \wedge \cdots \wedge (x_{n-1} = \alpha_{n-1})$, where if $\alpha_i=0$ we replace $x_i = \alpha_i$ with $\overline{x_i}$ and if $\alpha_i=1$ we replace $x_i=\alpha_i$ by simply $x_i$. 
This yields a circuit that computes $\delta_\alpha$ using $n$ AND gates and at most $n$ NOT gates and so a total of at most $2n$ gates.

Now for every function $f:\{0,1\}^n \rightarrow \{0,1\}$, we can write 

$$
f(x) = \delta_{x_0}(x) \vee \delta_{x_1}(x) \vee \cdots \vee \delta_{x_{N-1}}(x) \label{eqorofdeltafunc}
$$

where $S=\{ x_0 ,\ldots, x_{N-1}\}$ is the set of inputs on which $f$ outputs $1$.
(To see this, you can verify that the right-hand side of [eqorofdeltafunc](){.eqref} evaluates to $1$ on $x\in \{0,1\}^n$ if and only if $x$ is in the set $S$.)

Therefore we can compute $f$ using a Boolean circuit of at most $2n$ gates for each of the $N$ functions $\delta_{x_i}$ and combine that with at most $N$ OR gates, thus obtaining a circuit of at most $2n\cdot N + N$ gates.
Since $S \subseteq \{0,1\}^n$, its size $N$ is at most $2^n$ and hence the total number of gates in this circuit is $O(n\cdot 2^n)$.
:::



![For every string $\alpha\in \{0,1\}^n$, there is a Boolean circuit of $O(n)$ gates to compute the function $\delta_\alpha:\{0,1\}^n \rightarrow \{0,1\}$ such that $\delta_\alpha(x)=1$ if and only if $x=\alpha$. The circuit is very simple. Given input $x_0,\ldots,x_{n-1}$ we compute the  AND of $z_0,\ldots,z_{n-1}$ where $z_i=x_i$ if $\alpha_i=1$ and $z_i = NOT(x_i)$ if $\alpha_i=0$. While formally Boolean circuits only have a gate for computing the AND of two inputs, we can implement an AND of $n$ inputs by composing $n$ two-input ANDs.](../figure/deltafunc.png){#deltafuncfig .margin }


## The class $SIZE_{n,m}(T)$ {#secdefinesizeclasses }


We have seen that _every_ function $f:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a circuit of size $O(m\cdot 2^n)$, and _some_ functions (such as addition and multiplication) can be computed by much smaller circuits.
This motivates the following definition:
we define $SIZE_{n,m}(s)$ to be the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$ that can be computed by NAND circuits of at most $s$ gates (or equivalently, by NAND-CIRC programs of at most $s$ lines).
In other words, $SIZE_{n,m}(s)$ is defined as follows:

> ### {.definition title="Size class of functions" #sizedef}
Let $n,m,s \in \N$ be numbers with $s \geq m$.
The set $SIZE_{n,m}(s)$ denotes the set of all functions $f:\{0,1\}^n \rightarrow \{0,1\}^m$ such that there exists a NAND circuit of at most $s$ gates that computes $f$.
We denote by $SIZE_n(s)$ the set $SIZE_{n,1}(s)$.

[funcvscircfig](){.ref} depicts the sets $SIZE_{n,1}(s)$, note that $SIZE_{n,m}(s)$ is a set of _functions_, not of _programs!_ (asking if a program or a circuit is a member of $SIZE_{n,m}(s)$ is a _category error_ as in the sense of  [cucumberfig](){.ref}).


![There are $2^{2^n}$ functions mapping $\{0,1\}^n$ to $\{0,1\}$, and an infinite number of circuits with $n$ bit inputs and a single bit of output. Every circuit computes one function, but every function can be computed by many circuits. We say that $f \in SIZE_{n,1}(s)$ if the smallest circuit that computes $f$ has $s$ or fewer gates. For example $XOR_n \in SIZE_{n,1}(4n)$. [NAND-univ-thm](){.ref} shows that _every_ function $g$ is computable by some circuit of at most $c\cdot 2^n/n$ gates, and hence $SIZE_{n,1}(c\cdot 2^n/n)$ corresponds to the set of _all_ functions from $\{0,1\}^n$ to $\{0,1\}$.](../figure/funcvscircs.png){#funcvscircfig .class  }


While we defined $SIZE_{n,m}(s)$ with respect to NAND gates, we would get essentially the same class if we defined it with respect to AND/OR/NOT gates:

> ### {.lemma #nandaonsizelem}
Let $SIZE^{AON}_{n,m,s}$ denote the set of all functions $f:\{0,1\}^n \rightarrow \{0,1\}^m$ that can be computed by an AND/OR/NOT Boolean circuit of at most $s$ gates.
Then,
$$
SIZE_{n,m}(s/2) \subseteq SIZE^{AON}_{n,m}(s) \subseteq SIZE_{n,m}(3s)
$$

::: {.proof data-ref="nandaonsizelem"}
If $f$ can be computed by a NAND circuit of at most $s/2$ gates, then by replacing each NAND with the two gates NOT and AND, we can obtain an AND/OR/NOT Boolean circuit of at most $s$ gates that computes $f$.
On the other hand, if $f$ can be computed by a Boolean AND/OR/NOT circuit of at most $s$ gates, then by [NANDuniversamthm](){.ref} it can be computed by a NAND circuit of at most $3s$ gates.
:::




![A "category error" is a question such as "is a cucumber even or odd?" which does not even make sense. In this book one type of category errors you should watch out for is confusing _functions_ and _programs_ (i.e., confusing _specifications_ and _implementations_). If $C$ is a circuit or program, then asking if $C \in SIZE_{n,1}(s)$ is a category error, since $SIZE_{n,1}(s)$ is a set of _functions_ and not programs or circuits.](../figure/cucumber.png){#cucumberfig .margin  }


The results we have seen in this chapter can be phrased as showing that $ADD_n \in SIZE_{2n,n+1}(100 n)$
and $MULT_n \in SIZE_{2n,2n}(10000 n^{\log_2 3})$.
[NAND-univ-thm](){.ref} shows that  for some constant $c$, $SIZE_{n,m}(c m 2^n)$ is equal the set of all functions from $\{0,1\}^n$ to $\{0,1\}^m$.

> ### { .pause }
Note that $SIZE_{n,m}(s)$ does __not__ correspond to a set of programs!
Rather, it is a set of _functions_ (see [cucumberfig](){.ref}).
As we discussed in [specvsimplrem](){.ref} (and  [secimplvsspec](){.ref}), the distinction between _programs_ and _functions_ is absolutely crucial.
You should always remember that while a program _computes_ a function, it is not _equal_ to a function.
In particular, as we've seen, there can be more than one program to compute the same function.



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
We can rename the variable `Y[0]` in $P$ to a variable `temp` and add the line

```python
Y[0] = NAND(temp,temp)
```

at the very end to obtain a program $P'$ that computes $1-f$.
:::



> ### { .recap }
* We can define the notion of computing a function via a simplified "programming language", where computing a function $F$ in $T$ steps would correspond to having a $T$-line NAND-CIRC program that computes $F$.
* While the NAND-CIRC programming only has one operation, other operations such as functions and conditional execution can be implemented using it.
* Every function $f:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed by a circuit of at most $O(m 2^n)$ gates (and in fact at most $O(m 2^n/n)$ gates).
* Sometimes (or maybe always?) we can translate an _efficient_ algorithm to compute $f$ into a circuit that computes $f$  with a number of gates comparable to the number of steps in this algorithm.



## Exercises



::: {.exercise title="Pairing" #embedtuples-ex}
This exercise asks you to give a one-to-one map from $\N^2$ to $\N$. This can be useful to implement two-dimensional arrays as "syntacic sugar" in programming languages that only have one-dimensional array.

1. Prove that the map $F(x,y)=2^x3^y$ is a one-to-one map from $\N^2$ to $\N$.

2. Show that there is a one-to-one map $F:\N^2 \rightarrow \N$ such that for every $x,y$, $F(x,y) \leq 100\cdot \max\{x,y\}^2+100$.

3. For every $k$, show that there is a one-to-one map $F:\N^k \rightarrow \N$ such that for every $x_0,\ldots,x_{k-1} \in \N$, $F(x_0,\ldots,x_{k-1}) \leq 100 \cdot (x_0+x_1+\ldots+x_{k-1}+100k)^k$.
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


> ### {.exercise title="At least two / Majority" #atleasttwo-ex}
Give a NAND-CIRC program of at most 6 lines to compute the function  $MAJ:\{0,1\}^3 \rightarrow \{0,1\}$
where $MAJ(a,b,c) = 1$ iff $a+b+c \geq 2$.

::: ### {.exercise title="Conditional statements" #conditionalsugarthmex}
In this exercise we will explore [conditionalsugarthm](){.ref}: transforming NAND-CIRC-IF programs that use code such as `if .. then .. else ..` to standard NAND-CIRC programs.

1. Give a "proof by code" of [conditionalsugarthm](){.ref}: a program in a programming language of your choice that transforms a NAND-CIRC-IF program $P$ into a "sugar free" NAND-CIRC program $P'$ that computes the same function.^[_Hint:_ You can start by transforming $P$ into a NAND-CIRC-PROC program that uses procedure statments, and then use the code of [desugarcode](){.ref} to transform the latter into a "sugar free" NAND-CIRC program.] 

2. Prove the following statement, which is the heart of  [conditionalsugarthm](){.ref}: suppose that there exists an $s$-line NAND-CIRC program to compute $f:\{0,1\}^n \rightarrow \{0,1\}$ and an $s'$-line NAND-CIRC program to compute $g:\{0,1\}^n \rightarrow \{0,1\}$.
Prove that there exist a NAND-CIRC program of at most $s+s'+10$ lines to compute the function $h:\{0,1\}^{n+1} \rightarrow \{0,1\}$ where $h(x_0,\ldots,x_{n-1},x_n)$ equals $f(x_0,\ldots,x_{n-1})$ if $x_n=0$ and equals $g(x_0,\ldots,x_{n-1})$ otherwise. (All programs in this item are standard "sugar-free" NAND-CIRC programs.)
:::



::: {.exercise title="Half and full adders" #halffulladderex}
1. A _half adder_ is the function $HA:\{0,1\}^2 :\rightarrow \{0,1\}^2$ that corresponds to adding two binary bits. That is, for every $a,b \in \{0,1\}$, $HA(a,b)= (e,f)$ where $2e+f = a +b$. Prove that there is a NAND circuit of at most five NAND gates that computes $HA$.

2. A _full adder_ is the function $FA:\{0,1\}^3 \rightarrow \{0,1\}$ that takes in two bits and a "carry" bit and outputs their sum. That is, for every $a,b,c \in \{0,1\}$, FA(a,b,c) = (e,f)$ such that $2e+f = a+b+c$. Prove that there is a NAND circuit of at most nine NAND gates that computes $FA$.

3. Prove that if there is a NAND circuit of $c$ gates that computes $FA$, then there is a circuit of $cn$ gates that computes $ADD_n$ where (as in [addition-thm](){.ref}) $ADD_n:\{0,1\}^{2n} \rightarrow \{0,1\}^n$ is the function that outputs the addition of two input $n$-bit numbers. See footnote for hint.^[Use a "cascade" of adding the bits one after the other, starting with the least significant digit, just like in the elementary-school algorithm.]

4. Show that for every $n$ there is a NAND-CIRC program to compute $ADD_n$ with at most $9n$ lines.
:::


> ### {.exercise title="Addition" #addition-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND-CIRC program that computes $ADD_n$. Can you ensure that the program it outputs for $ADD_n$ has fewer than $10n$ lines?

> ### {.exercise title="Multiplication" #multiplication-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND-CIRC program that computes $MULT_n$. Can you ensure that the program it outputs for $MULT_n$ has fewer than $1000\cdot n^2$ lines?

> ### {.exercise title="Efficient multiplication (challenge)" #eff-multiplication-ex}
Write a program using your favorite programming language that on input an integer $n$, outputs a NAND-CIRC program that computes $MULT_n$ and has at most $10000 n^{1.9}$ lines.^[__Hint:__ Use Karatsuba's algorithm.] What is the smallest number of lines you can use to multiply two 2048 bit numbers?


::: {.exercise title="Multibit function" #mult-bit-ex}
In the text [NAND-univ-thm](){.ref} is only proven for the case $m=1$.
In this exercise you will extend the proof for every $m$.

Prove that

1. If there is an $s$-line NAND-CIRC program to compute $f:\{0,1\}^n \rightarrow \{0,1\}$ and an $s'$-line NAND-CIRC program to compute $f':\{0,1\}^n \rightarrow \{0,1\}$ then there is an $s+s'$-line program to compute the function $g:\{0,1\}^n \rightarrow \{0,1\}^2$ such that $g(x)=(f(x),f'(x))$.

2. For every function $f:\{0,1\}^n \rightarrow \{0,1\}^m$, there is a NAND-CIRC program of at most $10m\cdot 2^n$ lines that computes $f$. (You can use the $m=1$ case of [NAND-univ-thm](){.ref}, as well as Item 1.)
:::


::: {.exercise title="Simplifying using syntactic sugar" #usesugarex}
Let $P$ be the following NAND-CIRC program:

```python
Temp[0] = NAND(X[0],X[0])
Temp[1] = NAND(X[1],X[1])
Temp[2] = NAND(Temp[0],Temp[1])
Temp[3] = NAND(X[2],X[2])
Temp[4] = NAND(X[3],X[3])
Temp[5] = NAND(Temp[3],Temp[4])
Temp[6] = NAND(Temp[2],Temp[2])
Temp[7] = NAND(Temp[5],Temp[5])
Y[0] = NAND(Temp[6],Temp[7])
```

1. Write a program $P'$ with at most three lines of code that uses both `NAND` as well as the syntactic  sugar `OR` that computes the same function as $P$.

2. Draw a circuit that computes the same function as $P$ and uses only $AND$ and $NOT$ gates.
:::



In the following exercises you are asked  to compare the power of pairs programming languages.
By "comparing the power" of two programming languages $X$ and $Y$ we mean determining the relation between the set of functions that are computable using programs in  $X$ and $Y$ respectively. That is, to answer such a question you need to do both of:

1. Either prove that for every program $P$ in $X$ there is a program $P'$ in $Y$ that computes the same function as $P$, _or_ give an example for a function that is computable by an $X$-program but not computable by a $Y$-program.

_and_

1. Either prove that for every program $P$ in $Y$ there is a program $P'$ in $X$ that computes the same function as $P$, _or_ give an example for a function that is computable by a $Y$-program but not computable by an $X$-program.

When you give an example as above of a function that is computable in one programming language but not the other, you need to _prove_ that the function you showed is _(1)_ computable in the first programming language, _(2)_ _not computable_ in the second programming programming language.

::: {.exercise title="Compare IF and NAND" #compareif}
Let IF-CIRC be the programming language where we have the following operations `foo = 0`, `foo = 1`, `foo = IF(cond,yes,no)`  (that is, we can use the constants $0$ and $1$, and the $IF:\{0,1\}^3 \rightarrow \{0,1\}$ function such that $IF(a,b,c)$ equals $b$ if $a=1$ and equals $c$ if $a=0$). Compare the power of the NAND-CIRC programming language and the IF-CIRC programming language.
:::

::: {.exercise title="Compare XOR and NAND" #comparexor}
Let XOR-CIRC be the programming language where we have the following operations `foo = XOR(bar,blah)`, `foo = 1` and `bar = 0` (that is, we can use the constants $0$, $1$ and the $XOR$ function that maps $a,b \in \{0,1\}^2$ to $a+b \mod 2$). Compare the power of the NAND-CIRC programming language and the XOR-CIRC programming language.^[_Hint:_ You can use the fact that $(a+b)+c \mod 2 = a+b+c \mod 2$. In particular it means that if you have the lines `d = XOR(a,b)` and `e = XOR(d,c)` then `e` gets the sum modulo $2$ of the variable `a`, `b` and `c`.]
:::

::: {.exercise title="Circuits for majority" #majasymp}
Prove that there is some constant $c$ such that for every $n>1$, $MAJ_n \in Size(cn)$ where $MAJ_n:\{0,1\}^n \rightarrow \{0,1\}$ is the majority function on $n$ input bits. That is $MAJ_n(x)=1$ iff $\sum_{i=0}^{n-1}x_i > n/2$. NOTE: You can get __16 points__ by proving the weaker statement $MAJ_n \in Size(c \cdot n \log n)$ for some constant $c$.^[_Hint:_ One approach to solve this is using recursion and the  so-called Master Theorem.]
:::


::: {.exercise title="Circuits for threshold" #thresholdcirc}
Prove that there is some constant $c$ such that for every $n>1$, and integers $a_0,\ldots,a_{n-1},b \in \{-2^n,-2^n+1,\ldots,-1,0,+1,\ldots,2^n\}$, there is a NAND circuit with at most $n^c$ gates that computes the _threshold_ function $f_{a_0,\ldots,a_{n-1},b}:\{0,1\}^n \rightarrow \{0,1\}$ that on input $x\in \{0,1\}^n$ outputs $1$ if and only if $\sum_{i=0}^{n-1} a_i x_i > b$.
:::



## Bibliographical notes


See Jukna's and Wegener's books [@Jukna12, @wegener1987complexity] for much more extensive discussion on circuits.
Shannon showed that every Boolean function can be computed by a circuit of exponential size [@Shannon1938]. The improved bound of $c \cdot 2^n/n$ (with the optimal value of $c$ for many bases) is due to Lupanov [@Lupanov1958]. An exposition of this for the case of NAND is given in Chapter 4 of his   book [@lupanov1984].
(Thanks to Sasha Golovnev for tracking down this reference!)

The concept of "synctatic sugar" is also known as "macros" or "meta-programming" and is sometimes implemented via a preprocessor or macro language in a programming language or a text editor. One modern example is the [Babel](https://babeljs.io/) JavaScript syntax transformer, that converts JavaScript programs written using the latest features into a format that older Browsers can accept. It even has a [plug-in](https://babeljs.io/docs/plugins/) architecture, that allows users to add their own syntactic sugar to the language.
We mentioned that almost all programming language support user-defined functions, but one notable exception is the original version of the FORTRAN programming language, developed in the early 1950's. This was however quickly added in FORTRAN II, released in 1958.



