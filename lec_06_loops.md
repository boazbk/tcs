# Loops and infinity

> # { .objectives }
* Learn the model of NAND++ programs that involve loops.
* See some basic syntactic sugar for NAND++
* See equivalence between NAND++ programs and Turing Machines.
* Understand the relation between NAND++ and NAND programs.

>_"We thus see that when $n=1$, nine operation-cards are used; that when $n=2$, fourteen Operation-cards are used; and that when $n>2$, twenty-five operation-cards are used; but that no more are needed, however great $n$ may be; and not only this, but that these same twenty-five cards suffice for the successive computation of all the numbers"_, Ada Augusta, countess of Lovelace, 1843^[Translation of  "Sketch of the Analytical Engine" by L. F. Menabrea, Note G.]

>_"It is found in practice that (Turing machines) can do anything that could be described as 'rule of thumb' or 'purely mechanical'... (Indeed,) it is  now agreed amongst logicians that 'calculable by means of (a Turing Machine)' is the correct accurate rendering of such phrases."_, Alan Turing, 1948



The NAND programming language has one very significant drawback: a finite NAND program $P$ can only compute a finite function $F$, and in particular the number of inputs of $F$ is always smaller than (twice) the number of lines of $P$.^[This conceptual point holds for any straightline programming language, and is independent  of the particular syntactical choices we made for NAND. The particular ratio of "twice" is true for NAND because input variables cannot be written to, and hence a NAND program of $s$ lines includes at most $2s$ input variables. Coupled with the fact that a NAND program can't include `X[` $i$ `]` if it doesn't include `X[` $j$ `]` for $j<i$, this implies that the length of the input is at most $2s$.]

This does not capture our intuitive notion of an algorithm as a _single recipe_ to compute a potentially infinite function.
For example, the standard elementary school multiplication algorithm is a _single_ algorithm that multiplies numbers of all lengths, but yet we cannot express this algorithm as a single NAND program, but rather need a different NAND program for every input length.


Let us consider the case of the simple _parity_ or _XOR_ function  $XOR:\{0,1\}^* \rightarrow \{0,1\}$, where $XOR(x)$ equals $1$ iff the number of $1$'s in $x$ is odd.
As simple as it is, the $XOR$ function cannot be computed by a NAND program.
Rather, for every $n$, we can compute $XOR_n$ (the restriction of $XOR$ to $\{0,1\}^n$) using a different NAND program. For example, here is the NAND program to compute $XOR_5$: (see also [XOR5fig](){.ref})

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

![The circuit for computing the XOR of $5$ bits. Note how it merely repeats four times  the circuit to compute the XOR of $2$ bits.](../figure/XOR5circuit.png){#XOR5fig .class width=300px height=300px}


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

We will now discuss how we can extend the  NAND programming language so that it can capture these kinds of  constructs.


## The NAND++ Programming language

The NAND++ programming language aims to capture the notion of a _single uniform algorithm_ that can compute a function that takes inputs of _arbitrary lengths_.
To do so, we need to extend the NAND programming language with two constructs:

* _Loops_: NAND is a _straightline_ programming language- a NAND program of $s$ lines takes exactly $s$ steps of computation and hence in particular cannot even touch more than $3s$ variables. _Loops_ allow us to capture in a short program the instructions for a computation that can take an arbitrary amount of time.

* _Arrays_: A NAND program of $s$ lines touches at most $3s$ variables. While we allow in NAND variables such as `Foo[17]` or `Bar[22]`, they are not true arrays, since the number inside the brackets is a constant that is "hardwired" into the program. In particular a NAND program of $s$ lines cannot read an input `X[` $i$ `]` for $i>2s$.


Thus a good way to remember  NAND++ is  using the following informal equation:

$$
NAND++ \;=\; NAND \;+\; \text{loops} \;+\; \text{arrays} \label{eqnandloops}
$$

> # {.remark title="NAND + loops + arrays = everything." #otherpl}
It turns out that adding loops and arrays is enough to not only enable computing XOR, but in fact capture the full power of all programming languages! Hence we could replace "NAND++" with any of _Python_, _C_, _Javascript_, _OCaml_,  etc... in the lefthand side of  [eqnandloops](){.eqref}.
But we're getting ahead of ourselves: this issue will be discussed in [chapequivalentmodels](){.ref}.


### Enhanced NAND++ programs

We now turn to describing the syntax of NAND++ programs.
We'll start by describing what we call the "enhanced NAND++ programming language".
Enhanced NAND++ has some extra features on top of NAND++ that make it easier to describe.
However, we will see in [enhancednandequivalence](){.ref}  that these extra features can be implemented as "syntactic sugar" on top of standard or "vanilla" NAND++, and hence these two programming languages are equivalent in power.

Enhanced NAND++ programs add the following features on top of NAND:

* We add a special Boolean variable `loop`. If `loop` is equal to $1$ at the end of the execution then execution loops back to the first line of the program.

* We add a special _integer valued_ variable `i`. We add the commands `i += foo` and `i -= bar` that can add or subtract to `i` either zero or one, where `foo` and `bar` are standard (Boolean valued) variables.^[The variable `i` will actually always be a _non-negative_ integer, and hence `i -= foo` will have no effect if `i`= $0$. This choice is made for notational convenience, and the language would have had the same power if we allowed `i`  to take negative values.]

* We add  _arrays_ to the language by allowing variable identifiers to have the form `Foo[i]`. `Foo` is an array of Boolean values, and `Foo[i]` refers to the value of this array at location equal to the current value of  the variable `i`.

* The input and output `X` and `Y` are now considered _arrays_ with values of zeroes and ones. Since both input and output could have arbitrary length, we also add two new arrays `Xvalid` and `Yvalid` to mark their length. We define `Xvalid[` $i$ `]` $=1$  if and only if $i$ is smaller than the length of the input, and similarly we will set `Yvalid[` $j$ `]` to equal $1$ if and only if $j$ is smaller than the length of the output.



:::  {.example title="XOR in Enhanced NAND++" #XORENANDPP}
The following is an enhanced NAND++ program to compute the XOR function
on inputs of arbitrary length.
That is $XOR:\{0,1\}^* \rightarrow \{0,1\}$ such that $XOR(x) = \sum_{i=0}^{|x|-1} x_i \mod 2$ for every $x\in \{0,1\}^*$.

```python
temp_0 = NAND(X[0],X[0])
Yvalid[0] = NAND(X[0],temp_0)
temp_2 = NAND(X[i],Y[0])
temp_3 = NAND(X[i],temp_2)
temp_4 = NAND(Y[0],temp_2)
Y[0] = NAND(temp_3,temp_4)
loop = Xvalid[i]
i += Xvalid[i]
```
:::

::: {.example title="Increment in Enhanced NAND++" #INCENANDPP}
We now present enhanced NAND++ program to compute the _increment function_.
That is, $INC:\{0,1\}^* \rightarrow \{0,1\}^*$ such that for every $x\in \{0,1\}^n$, $INC(x)$ is the $n+1$ bit long string $y$ such that if $X = \sum_{i=0}^{n-1}x_i \cdot 2^i$ is the number represented by $x$, then $y$ is the binary representation of the number $X+1$.

We start by showing the program using the "syntactic sugar" we've seen before of using shorthand for some NAND programs we have seen before to compute simple functions such as `IF`, `XOR` and `AND` (as well as the constant `one` function as well as the function `COPY` that just maps a bit to itself).

```python
carry = IF(started,carry,one(started))
started = one(started)
Y[i] = XOR(X[i],carry)
carry = AND(X[i],carry)
Yvalid[i] = one(started)
loop = COPY(Xvalid[i])
i += loop
```
The above is not, strictly speaking, a valid enhanced NAND++ program.
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
Yvalid[i] = NAND(started,temp_14)
temp_16 = NAND(Xvalid[i],Xvalid[i])
loop = NAND(temp_16,temp_16)
i += loop
```
:::

::: { .pause }
Working out the above two example can go a long way towards understanding NAND++.
See the appendix for a full specification of the language.
:::

### "Oblivious" / "Vanilla" NAND++

Since our goal in theoretical computer science is not as much to _construct_
programs  as to _analyze_ them, we want to use as simple as possible computational models.
Hence our actual NAND++ programming language will be even more "bare bones" than enhanced NAND++.
In particular, NAND++ does _not_ contain the commands `i += foo` and `i -= bar` to control the integer-valued variable `i`.
Rather in NAND++ the variable `i` always progresses according to the same sequence.
In the first iteration `i`$=0$, in the second one `i`$=1$, in the third iteration, `i=`$0$ again, and then in the fourth to seventh iterations `i` travels to $2$ and back to $0$ again, and so on and so forth.
Generally, in the $k$-th iteration the value of `i` equals $I(k)$ where $I=(I(0),I(1),I(2),\ldots)$ is the following sequence (see [indextimefig](){.ref}):^[TODO: Potentially change in the future to Salil's sequence $INDEX(\ell) = min{\ell-floor(sqrt(\ell))^2,ceiling(sqrt(\ell))^2-\ell}$ which has the form $0,0,1,1,0,1,2,2,1,0,1,2,3,3,2,1,0,1,2,3,4,4,3,2,1,0,\ldots$.]

$$
0,1,0,1,2,1,0,1,2,3,2,1,0,1,\ldots
$$

![The value of `i` as a function of the current iteration. The variable `i` progresses according to the sequence $0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots$.  At the $k$-th iteration the value of `i` equals $k-r(r+1)$ if $k \leq (r+1)^2$ and $(r+1)(r+2)-k$ if $k<(r+1)^2$ where $r= \floor{\sqrt{k+1/4}-1/2}$.](../figure/indextime.png){#indextimefig .class width=300px height=300px}

::: {.example title="XOR in vanilla NAND++" #XORNANDPP}
Here is the XOR function in NAND++ (using our standard syntactic sugar to make it more readable):

```python
Yvalid[0] = one(X[0])
Y[0] = IF(Visited[i],Y[0],XOR(X[i],Y[0]))
Visited[i] = one(X[0])
loop = Xvalid[i]
```

Note that we use the array `Visited` to "mark" the positions of the input that we have already visited.
The line `IF(Visited[i],Y[0],XOR(X[i],Y[0]))` ensures that the output value  `Y[0]`
is XOR'ed with the $i$-th bit of the input only at the first time we see it.
:::

::: { .pause }
It would be very instructive for you to compare the enhanced NAND++ program for XOR of [XORENANDPP](){.ref} with the standard NAND++ program of [XORNANDPP](){.ref}.
:::

::: {.solvedexercise title="Computing index location" #computeindex}
Prove that at the $k$-iteration of the loop, the value of the variable `i` is equal to $index(k)$ where $index:\N \rightarrow \N$ is defined as follows:
$$
index(k) = \begin{cases} k- r(r+1) & k \leq (r+1)^2 \\ (r+1)(r+2)-k & \text{otherwise} \end{cases} \label{eqindex}
$$
where $r= \floor{\sqrt{k+1/4}-1/2}$.
:::

::: {.solution data-ref="computeindex"}
We say that a NAND program completed its _$r$-th round_ when the index variable `i` completed the sequence:

$$
0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots,0,1,\ldots,r,r-1,\ldots,0
$$

This happens when the program completed

$$
1+2+4+6+\cdots+2r =r^2 +r + 1
$$

iterations of its main loop. (The last equality is obtained by applying the formula for the sum of an arithmetic progression.)
This means that if we keep a "loop counter" $k$ that is initially set to $0$ and increases by one at the end of any iteration, then  the "round" $r$ is the largest integer such that $r(r+1) \leq k$.
One can verify that this means that $r=\floor{\sqrt{k+1/4}-1/2}$.
When $k$ is between $r(r+1)$ and $(r+1)^2$ then the index `i`
is ascending, and hence the value of $index(k)$ will be $k-r(r+1)$.
When $k$ is between $(r+1)^2$ and $(r+1)(r+2)$ then the index `i` is descending,  and hence the value of $index(k)$ will be $r-(k-(r+1)^2)= (r+1)(r+2)-k$.
:::




> # {.remark title="Variables as arrays" #arrays}
In NAND we allowed variables to have names such as `foo_17` or even `Bar[23]` but the numerical part of the identifier played essentially the same role as alphabetical part. In particular, NAND would be just as powerful if we didn't allow any numbers in the variable identifiers.
With the introduction of the special index variable `i`, in NAND++ things are different, and we do have actual arrays.
>
To make sure there is no confusion, we will insist that plain variables are written with all lower case, and _array variables_ begin with an upper case letter.
Moreover, it turns out that we can ensure without loss of generality that arrays are always indexed by the variable `i`.
Hence all the variable identifiers in "well formed" NAND++ programs will either have the form `foo_123` (a sequence of lower case letters, underscores, and numbers, with no brackets or upper case letters) or the form `Bar[i]` (an identifier starting with an upper case letter, and ending with `[i]`).
>
Some of our example programs, such as the program to compute XOR  in [XORNANDPP](){.ref}, are not well formed, in the sense that they index the `X` and `Y` arrays with `0` and not just `i`.
However, it is not hard to transform them into well formed programs (see [noabsoluteindexex](){.ref})





## Computable functions


We now turn to making one of the most important definitions in this book,
that of _computable functions_.
This definition is deceptively simple, but will be the starting point of many deep results and questions:



> # {.definition title="Computing a function" #computablefuncdef}
Let $F:\{0,1\}^* \rightarrow \{0,1\}^*$ be a function and let $P$ be a
NAND++ program.
We say that $P$ _computes_ $F$ if for every $x\in \{0,1\}^*$, if we execute $P$ while initializing the variables `X[`$i$`]`$=x_i$ and `Xvalid[`$i$`]`$=1$ for every $i\in \{0,\ldots,|x|-1\}$,
then $P$ halts eventually and moreover, if we let $P(x)$ denote  the value of the variables `Y[`$0$`]`,$\ldots$,`Y[`$m-1$`]`  (where $m$ is the smallest number such that the value of `Yvalid[`$m$`]`  is equal to $0$) then $P(x)=F(x)$.
>
We say that a function $F$ is _NAND++ computable_ if there is a NAND++ program that computes it.


We will often drop the "NAND++" qualifier and simply call a function _computable_ if it is NAND++ computable.
This may seem "reckless" but, as we'll see in future lectures, it turns out that  being NAND++-computable is equivalent to being computable in essentially any reasonable model of computation.

::: { .pause }
[computablefuncdef](){.ref} is, as we mentioned above, one of the most important definitions in this book. Please re-read it and make sure you understand it. Try to think how _you_ would define the notion of a NAND++ program $P$ computing a function, and make sure that you arrive at the same definition.
:::

This is a good point to remind the reader of  the distinction between _functions_ and _programs_:

$$ \text{Functions} \;\neq; \text{Programs} $$

A program $P$  can _compute_ some function  $F$, but it is not the same as $F$.
In particular there can be more than one program to compute the same function.
Being "NAND++ computable" is a property of _functions_, not of programs.



::: {.remark title="Infinite loops" #infiniteloops}
One crucial difference between NAND and NAND++ programs is the following.
Looking at a NAND program $P$, we can always tell how many inputs and how many outputs it has (by simply looking  at the `X` and `Y` variables).
Furthermore, we  are guaranteed that if we invoke $P$ on any input then _some_ output will be produced.

In contrast, given any particular NAND++ program $P'$, we cannot determine a priori the length of the output.
In fact, we don't even know  if an output would be produced at all!
For example, the following NAND++ program would go into an infinite loop if the first bit of the input is zero:

```python
loop = NAND(X[0],X[0])
```

If a program $P$ fails to stop and produce an output on some an input $x$, then it cannot compute any total function. However, it can still compute a _partial_ function.^[A _partial function_ $F$ from a set $A$ to a set $B$ is a function that is only defined on a _subset_ of $A$, (see [functionsec](){.ref}). We can also think of such a function as mapping $A$ to $B \cup \{ \bot \}$ where $\bot$ is a special "failure" symbol such that $F(a)=\bot$  indicates the function $F$ is not defined on $a$.]
We say that a NAND++ program $P$ computes a partial function $F$ if for every $x$ on which $F$ is defined, on input $x$, $P$ halts and outputs $F(x)$.
:::

> # {.remark title="Decidable languages" #decidablelanguages}
If $F:\{0,1\}^* \rightarrow \{0,1\}$ is a Boolean function, then computing $F$ is equivalent to deciding membership in the set $L=\{ x\in \{0,1\}^* \;|\; F(x)=1 \}$. Subsets of $\{0,1\}^*$ are known as _languages_ in the literature. Such a language  $L \subseteq \{0,1\}^*$ is known as _decidable_ or _recursive_ if the corresponding function $F$ is computable.
The corresponding concept to a _partial function_ is known as a [promise problem](https://goo.gl/sBczFM).





## Equivalence of "vanilla" and "enhanced" NAND++

We have defined so far not one but two programming languages to handle functions with unbounded input lengths: "enhanced" NAND++ which contains the `i += bar` and `i -= foo` operations, and the standard or "vanilla" NAND++, which does not contain these operations, but rather where the index `i` travels obliviously according to the schedule $0,1,0,1,2,1,0,1,\ldots$.

We now show these two versions are equivalent in power:

> # {.theorem title="Equivalence of enhanced and standard NAND++" #enhancednandequivalence}
Let $F:\{0,1\}^* \rightarrow \{0,1\}^*$.
Then $F$ is computable by a NAND++ program if and only if $F$ is computable by an enhanced NAND++ program.

> # {.proofidea data-ref="enhancednandequivalence"}
To prove the theorem we need to show  __(1)__ that for every NAND++ program $P$ there is an enhanced NAND++ program $Q$ that computes the same function as $P$, and __(2)__  that for every enhanced NAND++ program $Q$, there is a NAND++ program $P$ that computes the same function as $Q$.
>
Showing __(1)__ is quite straightforward: all we need to do is to show that we can ensure that `i` follows the sequence $0,1,0,1,2,1,0,1,\ldots$ using the `i += foo` and `i -= foo` operations.
The idea is that we use a `Visited` array to keep track at which places we visited, as well as a special `Atstart` array for which we ensure that `Atstart[`$0$`]`$=1$ but `Atstart[`$i$`]`$=0$ for every $i>0$.
We can use these arrays to check in each iteration whether `i` is equal to $0$ (in which case we want to execute `i += 1` at the end of the iteration), whether `i` is at a point which we haven't seen before (in which case we want to execute `i -= 1` at the end of the iteration), or whether it's at neither of those extremes (in which case we should add or subtract to `i` the same value as the last iteration).
>
Showing __(2)__ is a little more involved. Our main observation is that we can simulate a conditional `GOTO` command in NAND++. That is, we can come up with some "syntactic sugar" that will have the effect of jumping to a different line in the program if a certain variable is equal to $1$. Once we have this, we can implement looping commands such as `while`. This allows us to simulate a command such as `i += foo` when `i` is currently in the "decreasing phase" of its cycle  by simply waiting until `i`  reaches the same point in the "increasing phase". The intuition is that the difference between standard and enhanced NAND++ is like the difference between a bus and a taxi. Ennhanced NAND++ is like a taxi - you tell `i` where to do.  Standard NAND++ is like a bus - you wait until `i` arrives at the point you want it to be in. A bus might be a little slower, but will eventually get you to the same place.


We split the full proof of  [enhancednandequivalence](){.ref} into two parts.
In [vanillatoenhancedsec](){.ref} we show the easier direction of simulating standard NAND++ programs by enhanced ones.
In [nhanvedtovanillasec](){.ref} we show the harder direction of simulating enhanced NAND++ programs by standard ones.
Along the way we will show how we can simulate the `GOTO` operation in NAND++ programs.



### Simulating NAND++ programs by enhanced NAND++ programs. { #vanillatoenhancedsec }

Let $P$ be a standard NAND++ program. To create an enhanced NAND++ program that computes the same function, we will add a variable `indexincreasing` and code to ensure that at the end of the iteration, if `indexincreasing` equals $1$ then `i` needs to increase by $1$ and otherwise `i` needs to decrease by $1$.
Once we ensure that, we can emulate $P$ by simply adding the following lines to the end of the program

```python
i += indexincreasing
i -= NOT(indexincreasing)
```

where `one` and `zero` are variables which are always set to be zero or one, and `IF` is shorthand for NAND implementation of our usual $IF$ function (i.e., $IF(a,b,c)$ equals $b$ if $a=1$ and $c$ otherwise).

To compute `indexincreasing` we use the fact that the sequence $0,1,0,1,2,1,0,1,\ldots$ of  `i`'s travels in  a standard NAND++ program is obtained from the following rules:

1. At the beginning `i` is increasing.
2. If `i` reaches a point which it hasn't seen before, then it starts decreasing.
3. If `i` reaches the initial point $0$, then it starts increasing.

To know which points we have seen before, we can borrow Hansel and Gretel's technique of leaving _"breadcrumbs"_.
That is, we will create an array `Visited` and add code `Visited[i] = one` at the end of every iteration.
This means that if `Visited[i]`$=0$ then we know we have not visited this point before.
Similarly we create an array `Atstart` array and add code `Atstart[0] = one` (while all other location remain at the default value of zero).
Now we can use `Visited` and `Atstart` to compute the value of `indexincreasing`.
Specifically, we will add the following pieces of code

```python
Atstart[0] = COPY(one)
indexincreasing = IF(Visited[i],indexincreasing,zero)
indexincreasing = IF(Atstart[i],one,indexincreasing)
Visited[i] = COPY(one)
```

at the very end of the program.

![We can know if the index variable `i` should increase or decrease by keeping an array `atstart` letting us know when `i` reaches $0$, and hence `i` starts increasing, and `breadcrumb` letting us know when we reach a point we haven't seen before, and hence `i` starts decreasing.  TODO: update figure to `Atstart` and `Visited` notation. ](../figure/breadcrumbs.png){#breadcrumbspng .class width=300px height=300px}

Given any standard NAND++ program $P$, we can add the above lines of code to it to obtain an enhanced NAND++ program $Q$ that will behave in exactly the same way as $P$ and hence will compute the same function.
This completes the proof of the first part of [enhancednandequivalence](){.ref}.


### Simulating enhanced NAND++ programs by NAND++ programs. { #nhanvedtovanillasec }

To simulate enhanced NAND++ programs by vanilla ones, we will do as follows.
We introduce an array `Markposition` which normally would be all zeroes.
We then replace the line `i += foo` with code that achieves the following:

1. We first check if `foo=0`. If so, then we do nothing.
2. Otherwise we set `Markposition[i]=one`.
3. We then want to add code that will do nothing until we we get to the position `i+1`. We now that we got to this position when we reach the end of the program iteration and both `Markposition[i]`$=1$  and `indexincreasing`$=1$. We do so by setting a special variable named `waiting`, which basically tells the program to do nothing except check the condition until `waiting`$=0$.

We will start by describing this program under the assumption that we have access to `GOTO` and `LABEL` operations.
`LABEL(l)` simply marks a line of code with the string `l`. `GOTO(l,cond)` jumps in execution to the position labeled `l` if `cond` is equal to $1$.^[Since this is a NAND++ program, we assume that if the label `l` is _before_ the `GOTO` then jumping in execution means that another iteration of the program is finished, and the index variable `i` is increased or decreased as usual.]

If the original program had the form:

```python
precode... #pre-increment-code

i += foo

postcode... # post-increment-cod
```

Then the new program will have the following form:

```python
precode... #pre-increment-code

# relacement for i += foo
waiting = foo # if foo=1 then we need to wait
Markposition[i] = foo # we mark the position we were at
GOTO("end",waiting) # If waiting then jump till end.

LABEL("postcode")
waiting = zero
timeforpostcode = zero
postcode..

LABEL("end")
maintainance # maintain value of indexincreasing variable as before
condition = AND(Markposition[i],indexincreasing) # when to stop waiting.
Markposition[i] = IF(condition,zero,Markposition[i]) # zero out Markposition if we are done waiting
GOTO("postcode",AND(condition,waiting))  # If condition is one and we  were waiting then go to instruction after increment
GOTO("end",waiting) # If we are still in waiting then go back to "end" skipping all the rest of the code
# (since this is another iteration of the program i keeps travelling as usual.)
```
> # { .pause }
Please make sure you understand the above construct.
Also note that the above only works when there is a _single_ line of the form ` i += foo` or `i -= bar` in the program.
When there are multiple lines then we need to add more labels and variables to take care of each one of them separately.
Stopping here and working out how to handle more labels is an excellent way to get a better understanding of this construction.

__Implementing GOTO: the importance of doing nothing.__
The above reduced the task of completing the proof of [enhancednandequivalence](){.ref} to implementing the `GOTO` function, but we have not yet shown how to do so.
We now describe how we can implement `GOTO` in NAND++.
The idea is simple: to simulate `GOTO(l,cond)`, we modify all the lines between  the `GOTO` and `LABEL` commands to do nothing if the condition is true.
That is, we modify code of the form:

```python
precode...

GOTO(l,cond)

incode...

LABEL(l)

postcode...
```

to the form

```python
precode ...
donothing = cond

GUARDED(incode,donothing)

donothing = 1
postcode..
```

where `GUARDED(incode,donothing)` refers to transforming every line in `incode` of the form `foo = NAND(bar,blah)` to the form `foo = IF(donothing,foo,NAND(bar,blah))`.
That is, the "guarded" version of the code keeps the value of every variable the same if `donothing` equals $1$.
We leave to you to verify that the above approach extends to multiple `GOTO` statements.
This  completes the proof of the second and final part of [enhancednandequivalence](){.ref}.

::: { .pause }
It is important to go over this proof and   verify you understand it.
One good way to do so is to understand how you the proof handles multiple `GOTO` statements. You can do so by eliminating  one  `GOTO` statement at a time, taking care to not to "override" the variable `donothing`, but rather use a unique variable for each occurence of the statement.
:::


::: {.remark title="GOTO's in programming languages" #gotorem}
The `GOTO` statement was a staple of most early programming languages, but has largely fallen out of favor and is not included in many modern languages such as _Python_, _Java_,  _Javascript_.
In a famous 1968 letter editor Edsger Dijsktra argued that "[Go to statement considered harmful.](https://goo.gl/bnNsjo)" (see also [xkcdgotofig](){.ref}).
The main trouble with `GOTO` is that it makes analysis of programs more difficult by making it harder to argue about _invariants_ of the program.

When a program contains  a loop of the form:

```python
for j in range(100):
    do something

do blah
```


you know that  the line of code `do blah` can only be reached if the loop ended, in which case you know that `j` is equal to $100$, and might also be able to argue other properties of the state of the program.
In contrast, if the program might jump to `do blah` from any other point in the code, then it's very hard for you as the programmer to know what you can rely upon in this code.
As Dijkstra said, such invariants are important because _"our intellectual powers are rather geared to master static relations and .. our powers to visualize processes evolving in time are relatively poorly developed"_ and so  _"we should ... do ...our utmost best to shorten the conceptual gap between the static program and the dynamic process."_

That said, `GOTO` is still a staple of lower level languages where it is used to implement higher level looping constructs such as `while` and `for` loops.
For example, even though _Java_ doesn't have a `GOTO` statement, the Java Bytecode (which is a lower level representation of Java) does have such a statement.
Similarly, Python bytecode has instructions such as  `POP_JUMP_IF_TRUE` that implement the `GOTO` functionality, and similar instructions are included in many assembly languages.
The way we use `GOTO` to implement a higher level functionality in NAND++ is reminiscent of the way these various jump instructions are used to implement higher level looping constructs.
:::

![XKCD's take on the `GOTO` statement.](../figure/xkcdgoto.png){#xkcdgotofig .class width=300px height=300px}

## Turing Machines


>_"Computing is normally done by writing certain symbols on paper. We may suppose that this paper is divided into squares like a child's arithmetic book.. The behavior of the \[human\] computer at any moment is determined by the symbols which he is observing, and of his 'state of mind' at that moment... We may suppose that in a simple operation not more than one symbol is altered."_, \
>_"We compare a man in the process of computing ... to a machine which is only capable of a finite number of configurations... The machine is supplied with a 'tape' (the analogue of paper) ... divided into sections (called 'squares') each capable of bearing a 'symbol' "_, Alan Turing, 1936


>_"What is the difference between a Turing machine and the modern computer? It's the same as that between Hillary's ascent of Everest and the establishment of a Hilton hotel on its peak."_ , Alan Perlis, 1982.


The "granddaddy" of all models of computation is the _Turing Machine_, which is the standard  model of computation in most textbooks.^[This definitional choice does not make much difference since, as we  show here, NAND++  programs are equivalent to Turing machines in their computing power.]
Turing machines were defined in 1936 by Alan Turing in an attempt to formally capture all the functions that can be computed by human "computers" that follow a well-defined set of rules, such as the standard algorithms for addition or multiplication.

![Until the advent of electronic computers, the word "computer" was used to describe a person, often female, that performed calculations. These human computers were absolutely essential to many achievements including mapping the stars, breaking the Enigma cipher, and the NASA space mission. Two recent books about  these "computers" and their important contributions are [The Glass Universe](https://www.amazon.com/Glass-Universe-Harvard-Observatory-Measure-ebook/dp/B01CZCW45O) (from which this photo is taken) and [Hidden Figures](https://www.amazon.com/Hidden-Figures-American-Untold-Mathematicians/dp/006236359X).](../figure/HumanComputers.jpg){#figureid .class width=300px height=300px}

Turing thought of such a person as having access to as much "scratch paper" as they need.
For simplicity we can think of this scratch paper as a one dimensional piece of graph paper (commonly known as "work tape"), where in each box or "cell" of the tape holds a  single symbol from some finite alphabet (e.g., one digit or letter).
At any point in time, the person can read and write a single box of the paper, and based on the contents can update his/her finite mental  state, and/or move to the box immediately to the left or right.

Thus, Turing modeled  such a computation by a "machine" that maintains one of $k$ states, and at each point can read and write a single symbol from some alphabet $\Sigma$ (containing $\{0,1\}$) from its "work tape".
To perform computation using this machine, we write the input $x\in \{0,1\}^n$ on the tape, and the goal of the machine is to ensure that at the end of the computation, the value $F(x)$ will be written there.
Specifically, a computation of a Turing Machine $M$ with $k$ states and alphabet $\Sigma$ on input $x\in \{0,1\}^*$ proceeds as  follows:

* Initially the machine is at state $0$ (known as the "starting state") and the tape is initialized to $\triangleright,x_0,\ldots,x_{n-1},\varnothing,\varnothing,\ldots$.^[We use the symbol $\triangleright$ to denote the beginning of the tape, and the symbol $\varnothing$ to denote an empty cell. Hence we will assume that $\Sigma$ contains these symbols, along with $0$ and $1$.]
* The location $i$ to which the machine points to is set to $0$.
* At each step, the machine reads the symbol $\sigma = T[i]$ that is in the $i^{th}$ location of the tape, and based on this symbol and its state $s$ decides on:
    * What symbol $\sigma'$ to write on the tape \
    * Whether to move **L**eft (i.e., $i \leftarrow i-1$) or **R**ight  (i.e., $i \leftarrow i+1$) \
    * What is going to be the new state $s \in [k]$
* When the machine reaches the state $s=k-1$ (known as the "halting state") then it halts. The output of the machine is obtained by reading off the tape from location $1$ onwards, stopping at the first point where the symbol is not $0$ or $1$.


![A Turing machine has access to a _tape_ of unbounded length. At each point in the execution, the machine can read/write a single symbol of the tape, and based on that decide whether to move left, right or halt.](../figure/turing_machine.png){#turing-machine-fig .class width=300px height=300px}

^[TODO: update figure to $\{0,\ldots,k-1\}$.]


The formal definition of Turing machines is as follows:

> # {.definition title="Turing Machine" #TM-def}
A (one tape) _Turing machine_ with $k$ states and alphabet $\Sigma \supseteq \{0,1, \triangleright, \varnothing \}$ is a function
$M:[k]\times \Sigma \rightarrow [k] \times \Sigma  \times \{ L , R \}$.
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
* Let $m$ be the first index  such that $T[m] \not\in \{0,1\}$. We define the output of the process to be $T[1]$,$\ldots$,$T[m-1]$. The number of steps that the Turing Machine $M$ takes on input $x$ is the number of times that the while loop above  is executed. (If the process never stops then we say that the machine did not halt on $x$.)


::: { .pause }
You should make sure you see why this formal definition corresponds to our informal description of a Turing Machine.
To get more intuition on Turing Machines, you can play with some of the online available simulators such as [Martin Ugarte's](https://turingmachinesimulator.com/), [Anthony Morphett's](http://morphett.info/turing/turing.html), or [Paul Rendell's](http://rendell-attic.org/gol/TMapplet/index.htm).
:::

As mentioned, Turing machines turn out to be equivalent to NAND++ programs:

> # {.theorem title="Turing machines and NAND++ programs" #TM-equiv-thm}
For every $F:\{0,1\}^* \rightarrow \{0,1\}^*$, $F$ is computable by a NAND++ program if and only if there is a Turing Machine $M$ that computes $F$.

> # {.proofidea data-ref="TM-equiv-thm"}
Once again, to prove such an equivalence theorem, we need to show two directions. We need to be able to __(1)__  transform a Turing machine $M$ to a NAND++ program $P$ that computes the same function as $P$  and __(2)__ transform a NAND++ program $P$ into a Turing machine $M$ that computes the same function as $P$.
>
To show __(1)__, given a Turing machine $M$, we will create a NAND program $P$ that will have an array `Tape` for the tape of $M$ and scalar variable(s) `state` for the state of $M$.
Specifically, since the state of a Turing machine is not in $\{0,1\}$ but rather in a larger set $[k]$, we will use $\ceil{\log k}$ variables `state_`$0$ , $\ldots$, `state_`$\ceil{\log k}-1$ variables to store the representation of the state.
Similarly, to encode the larger alphabet $\Sigma$ of the tape, we will use $\ceil{\log |\Sigma|}$ arrays `Tape_`$0$ , $\ldots$, `Tape_`$\ceil{\log |\Sigma|}-1$, such that the `$i^{th}$ location of these arrays encodes the $i^{th}$ symbol in the tape for every tape.
Using the fact that _every_ function can be computed by a NAND program, we will be able to compute the transition function of $M$, replacing moving left and right by decrementing and incrementing `i` respectively.
>
We show __(2)__ using very similar ideas. Given a program $P$ that uses $a$ array variables and $b$ scalar variables, we will create a Turing machine with about $2^b$ states to encode the values of scalar variables, and an alphabet of about $2^a$ so we can encode the arrays using our tape. (The reason the sizes are only "about" $2^a$ and $2^b$ is that we will need to add some symbols and steps for bookkeeping purposes.) The Turing Machine $M$ will simulate each iteration of the program $P$ by updating its state and tape accordingly.

### Simulating Turing machines with NAND++ programs

We now prove the "if" direction of [TM-equiv-thm](){.ref}, namely we show that given a Turing machine $M$, we can find a NAND++ program $P_M$ such that for every input $x$, if $M$ halts on input $x$ with output $y$ then $P_M(x)=y$.
Because enhanced and plain NAND++ are equivalent in power, it is sufficient to construct an enhanced NAND<< program that has this property.
Moreover, since our goal is just to show such a program _exists_, we don't need to write out its full code line by line, and can take advantage of our various "syntactic sugar" in describing it.

If $M:[k]\times \Sigma \rightarrow [k] \times \Sigma  \times \{ L , R \}$ then there is a finite length NAND program `ComputeM` that computes the finite function $M$ (representing the finite sets $[k]$,$\Sigma$, $\{L,R\}$ appropriately by bits).
The enhanced NAND++ program simulating $M$ will be the following:

```python
state, Tape[i], direction = ComputeM(state, Tape[i])
i += direction
i -= NOT(direction)
```

where we use `state` as shorthand for the tuple of variables `state_`$0$, $\ldots$, `state_`$\ell-1$ and `Tape[i]` as shorthand for `Tape_`$0$`[i]` ,$\ldots$, `Tape_`$\ell'-1$`[i]` where $\ell = \ceil{\log k}$ and $\ell' = \ceil{\log |\Sigma|}$.


<!--
```python
// tape is an array with the alphabet Sigma
// we use ">" for the start-tape marker and "." for the empty cell
// in the syntactic sugar below, we assume some binary encoding of the alphabet.
// we also assume we can index an array with a variable other than i,
// and with some simple expressions of it (e.g., foo_{j+1})
// this can be easily simulated in NAND<<
//
// we assume an encoding such that the default value for tape_j is "."

// below k is the number of states of the machine M
// ComputeM is a function that maps a symbol in Sigma and a state in [k]
// to the new state, symbol to write, and direction

tape_0 := ">"
j = 0
while (validx_j) { // copy input to tape
    tape_{j+1} := x_j
    j++
}

state := 0
head  := 0 // location of the head
while NOT EQUAL(state,k-1) { // not ending state
   state', symbol, dir := ComputeM(tape_head,state)
   tape_head := symbols
   if EQUAL(dir,`L`) AND NOT(EQUAL(tape_head,">")) {
       head--
   }
   if EQUAL(dir,'R') {
       head++
   }
   state' := state
}

// after halting, we copy the contents of the tape
// to the output variables
// we stop when we see a non-boolean symbol
j := 1
while EQUAL(tape_j,0) OR EQUAL(tape_j,1) {
   y_{j-1} := tape_j
}
```

-->

In addition to the standard syntactic sugar, we are also assuming in the above code that  we can make function calls to the function `EQUAL` that checks equality of two symbols as well as the finite function `ComputeM`  that corresponds to the transition function of the Turing machine.
Since these are _finite_ functions (whose input and output length only depends on the number of states and symbols of the machine $M$, and not the input length), we can compute them  using a NAND (and hence in particular a NAND++ or NAND<<) program.

### Simulating NAND++ programs with Turing machines

To prove the second direction of [TM-equiv-thm](){.ref}, we need to show that for  every NAND++ program $P$, there is a Turing machine $M$ that computes the same function as $P$.
The idea behind the proof is that the TM $M$ will _simulate_ the program $P$ as follows: (see also [TMsimNANDfig](){.ref})

* The _head position_ of $M$ will correspond to the position of the index `i` in the current execution of the program $P$.

* The _alphabet_ of $M$ will be large enough so that in position $i$ of the tape will store the contents of all the variables of $P$ of the form `foo_`$\expr{i}$. (In particular this means that the alphabet of $M$ will have at least $2^t$ symbols when $t$ is the number of variables of $P$.)

* The _states_ of $M$ will be large enough to encode the current line number that is executed by $P$, as well as the contents of all variables that are indexed in the program by an absolute numerical index (e.g., variables of the form `foo` or `bar_17` that are not indexed with `i`.)

The key point is that the number of lines of $P$ and the number of variables are constants that do not depend on the length of the input and so can be encoded in the alphabet and state size. More specifically, if $V$ is the set of variables of $P$, then the alphabet of $M$ will contain  (in addition to the symbols $\{0,1, \triangleright, \varnothing \}$) the finite set of all functions from $V$ to   $\{0,1\}$, with the semantics that if $\sigma: V \rightarrow \{0,1\}$ appears in the $i$-th position of the tape then for every variable $v\in V$, the value of $v$`_`$\expr{i}$ equals $\sigma(v)$.
Similarly, we will think of the state space of $M$ as containing all pairs of the form $(\ell,\tau)$ where $\ell$ is a number between $0$ and the number of lines in $P$ and $\tau$ is a function from $V\times [c]$ to $\{0,1\}$  where $c-1$ is the largest absolute numerical index that appears in the program.^[While formally the state space of $M$ is a number between  $0$ and $k-1$ for some $k\in \N$, by making $k$ large enough, we can encode all pairs  $(\ell,\tau)$ of the form above as elements of the state space of the amchine, and so we can  think of the state as having this form.]
The semantics are that $\ell$ encodes the line of $P$ that is about to be executed, and $\tau(v,j)$ encodes the value of the variable $v$`_`$\expr{j}$.

To simulate the execution of one step in $P$'s computation, the machine $M$ will do the following:

1. The contents of the symbol at the current head position and its state encode all information about the current line number to be executed, as well as the contents of all variables of the program of the form `foo_`$\expr{i}$ where $i$ is the current value of the index variable in the simulated program. Hence we can use that to compute the new line to be executed.

2. $M$ will write to the tape and update its state to reflect the update to the variable that is assigned a new value in the execution of this line.

3. If the current line was the last one in the program, and the `loop` variable (which is encoded in $M$'s state) is equal to $1$ then $M$ will decide whether to move the head left or right based on whether the index is going to increase and decrease. We can ensure this is is a function of the current variables of $P$ by adding to the program the variables `breadcrumbs_i`, `atstart_i` and `indexincreasing` and the appropriate code so that `indexincreasing` is set to $1$ if and only if the index will increase in the next iteration.^[While formally we did not allow the head of the Turing machine to stay in place, we can simulate this by adding a "dummy step" in which $M$'s head  moves right and goes into a special state that will move left in the next step.]

The simulation will also contain an _initialization_ and a  _finalization_ phases. In the _initialization phase_, $M$ will scan the input and modify the  tape  so it contains the proper encoding of  `x_i`'s  `validx_i`'s variables as well as load into its state all references to these variables with absolute numerical indices.
In the _finalization phase_, $M$ will scan its tape to copy the contents of the  `y_i`'s  (i.e., output) variables to the beginning of the tape, and write a non $\{0,1\}$ value at their end.
We leave verifying the (fairly straightforward) details of implementing these steps to the reader. Note that we can add a finite number of states to $M$ or symbols to its alphabet to make this  implementation easier.
 Writing down the full description of $M$ from the above "pseudocode" is  straightforward, even if somewhat painful, exercise, and hence this completes the proof of [TM-equiv-thm](){.ref}.


![To simulate a NAND++ program $P$ using a machine $M$ we introduce a large alphabet $\Sigma$ such that each symbol in $\Sigma$ can be thought of as a "mega symbol" that encodes the value of all the variables indexed at $i$, where $i$ is the current tape location. Similarly each state of $M$ can be thought of as a "mega state" that encodes the value of all variables of $P$ that have an absolute numerical index, as well as the current line that is about to be executed.](../figure/TMsimNAND.png){#TMsimNANDfig .class width=300px height=300px}


> # {.remark title="Polynomial equivalence" #polyequivrem}
If we examine the proof of [TM-equiv-thm](){.ref} then we can see  that the equivalence between NAND++ programs and Turing machines is up to polynomial overhead in the number of steps.
Specifically, our NAND<< program to simulate a Turing Machine $M$, has two loops to copy the input and output and then one loop that iterates once per each step of the machine $M$.
In particular this means that if the Turing machine $M$ halts on every $n$-length input $x$ within $T(n)$ steps, then the NAND<< program computes the same function within $O(T(n)+n+m)$ steps.
Moreover, the transformation of NAND<< to NAND++ has  polynomial overhead, and hence for any such machine $M$ there is a NAND++ program $P'$ that computes the same function within $poly(T(n)+n+m)$ steps (where $poly(f(n))$ is shorthand for $f(n)^{O(1)}$ as defined in the mathematical background section).
In the other direction, our Turing machine $M$ simulates each step of a NAND++ program $P$ in a constant number of steps.
The initialization and finalization phases involve scanning over $O(n+m)$ symbols and copying them around. Since the cost to move a symbol to a point that is of distance $d$ in the tape can be $O(d)$ steps, the total cost of these phases will be $O((n+m)^2)$
Thus, for every NAND++ program $P$, if $P$ halts on input $x$ after $T$ steps, then the corresponding Turing machine $M$ will halt after $O(T+(n+m)^2)$ steps.







## Uniformity, and NAND vs NAND++


While NAND++ adds an extra operation over NAND, it is not exactly accurate to say that NAND++ programs are "more powerful" than NAND programs.
NAND programs, having no loops, are simply not applicable for computing functions with more inputs than they have lines.
The key difference between NAND and NAND++ is that NAND++ allows us to express the fact that the algorithm for computing parities of length-$100$ strings is really the same one as the algorithm for computing parities of length-$5$ strings (or similarly the fact that the algorithm for adding $n$-bit numbers is the same for every $n$, etc.).
That is, one can think of the NAND++ program for general parity as the "seed" out of which we can grow NAND programs for length $10$, length $100$, or length $1000$ parities as needed.
This notion of a single algorithm that can compute functions of all input lengths is known as _uniformity_ of computation and hence we think of NAND++ as  _uniform_ model of computation, as opposed to NAND which is a _nonuniform_ model, where we have to specify a different program for every input length.


Looking ahead, we will see that this uniformity leads to another crucial difference between NAND++ and NAND programs.
NAND++ programs can have inputs and outputs that are longer than the description of the program and in particular we can have a NAND++ program that "self replicates" in the sense that it can print its own code.
This notion of "self replication", and the related notion of "self reference" is crucial to many aspects of computation, as well  of course to life itself, whether in the form of digital or biological programs.

<!--

### Growing a NAND tree


If $P$ is a NAND++ program and $n,T\in \N$ are some numbers, then we can easily obtain a NAND program $P'=expand_{T,n}(P)$ that, given any $x\in \{0,1\}^n$, runs $T$ loop iterations of the program $P$ and outputs the result.
If $P$ is a simple program, then we are guaranteed that, if $P$ does not enter an infinite loop on $x$, then as long as we make $T$ large enough, $P'(x)$ will equal $P(x)$.
To obtain the program $P'$ we can simply place $T$ copies of the program $P$ one after the other, doing a "search and replace" in the $k$-th copy of any instances of `_i` with the value $index(k)$, where the function $index$ is defined as in [eqindex](){.eqref}. For example, [expandnandpng](){.ref} illustrates  the expansion of the  NAND++ program for parity.


![The circuit corresponding to a  NAND program for parity obtained by expanding the NAND++ program](../figure/paritynandppcircuit.png){#expandnandpng .class width=300px height=300px}

We can also obtain such an expansion by using the `for .. do { .. }` syntactic sugar.
For example, the NAND program below corresponds to running the parity program for 17 iterations, and computing $XOR_5:\{0,1\}^5 \rightarrow \{0,1\}$. Its standard "unsweetened" version will have $17 \cdot 10$ lines.^[This is of course not the most efficient way to compute $XOR_5$. Generally, the NAND program to compute $XOR_n$ obtained by expanding out the  NAND++ program will require $\Theta(n^2)$ lines, as opposed to the $O(n)$ lines that is possible to achieve directly in NAND. However, in most cases this difference will not be so crucial for us.]

```python
for i in [0,1,0,1,2,1,0,1,2,3,2,1,0,1,2,3,4] do {
tmp1  := seen_i NAND seen_i
tmp2  := x_i NAND tmp1
val   :=  tmp2 NAND tmp2
ns   := s   NAND s
y_0  := ns  NAND ns
u    := val NAND s
v    := s   NAND u
w    := val NAND u
s    := v   NAND w
seen_i := zero NAND zero
}
```



In particular we have the following theorem

> # {.theorem title="Expansion of NAND++ to NAND" #NANDexpansionthm}
For every simple NAND++ program $P$ and function $F:\{0,1\}^* \rightarrow \{0,1\}$, if $P$ computes $F$ then for every $n\in\N$ there exists $T\in \N$ such that $expand_{T,n}(P)$ computes $F_n$.

```python
# Expand a NAND++ program and a given time bound T and n to an n-input T-line NAND program
def expand(P,T,n):
    result = ""

    for k in range(T):
        i=index(k)
        validx = ('one' if i<n else 'zero')
        result += P.replace('validx_i',validx).replace('x_i',('x_i' if i<n else 'zero')).replace('_i','_'+str(i))

    return result


def index(k):
    r = math.floor(math.sqrt(k+1/4)-1/2)
    return (k-r*(r+1) if k <= (r+1)*(r+1) else (r+1)*(r+2)-k)
```



  \

> # {.proof data-ref="NANDexpansionthm"}
We'll start with a "proof by code". Above is a  Python program `expand` to compute $expand_{T,n}(P)$.
On  input the code $P$ of a NAND++ program and numbers $T,n$, `expand` outputs the code of the NAND program $P'$ that works on length $n$ inputs and is obtained by running $T$ iterations of $P$:
>
If the original program had $s$ lines, then for every $\ell \in [sT]$, line  $\ell$ in the output of `expand(P,T,n)` corresponds exactly to the line executed in step $\ell$ of the execution $P(x)$.^[In the notation above (as elsewhere),  we index both  lines and steps from $0$.]
Indeed, in step $\ell$ of the execution of $P(x)$, the line executed is $k=\ell \bmod s$, and line $\ell$ in the output of `expand(P,T,n)` is a copy of line $k$ in $P$.
If that line involved unindexed variables, then it is copied as is in the returned program `result`.
Otherwise, if it involved the index `_i` then we replace `i` with the current value of $i$.
Moreover, we replace the variable `validx_i` with either `one` or `zero` depending on whether $i < n$.
>
Now, if a simple  NAND++ program $P$ computes some function $F:\{0,1\}^* \rightarrow \{0,1\}$, then for every $x\in \{0,1\}^*$  there is some number $T_P(x)$ such that on input $x$ halts within $T(x)$ iterations of its main loop and outputs $F(x)$.
Moreover, since $P$ is simple, even if we run it for more iterations than that, the output value will not change.
For every $n \in \N$, define $T_P(n) = \max_{x\in \{0,1\}^n} T(x)$. Then $P'=expand_{T_P(n),n}(P)$ computes the function $F_n:\{0,1\}^n \rightarrow \{0,1\}$ which is the restriction of $F$ to $\{0,1\}^n$.





## NAND++ Programs as tuples

Just like we did with NAND programs, we can represent NAND++ programs as tuples.
A minor difference is that since in NAND++ it makes sense to keep track of indices, we will represent a  variable `foo_`$\expr{j}$ as a pair of numbers $(a,j)$ where $a$ corresponds to the identifier `foo`.
Thus we will use a 6-tuple of the form $(a,j,b,k,c,\ell)$ to represent each line of the form `foo_`$\expr{j}$ ` := ` `bar_`$\expr{k}$ ` NAND ` `baz_`$\expr{\ell}$, where $a,b,c$ correspond to the variable identifiers `foo`, `bar` and `baz` respectively.^[This difference between three tuples and six tuples is made for convenience and is not particularly important. We could have also  represented NAND programs using six-tuples and NAND++ using three-tuples. Also recall that we use the convention that an unindexed variable identifier `foo` is equivalent to `foo_0`.]
If one of the indices is the special variable `i` then we will use the number $s$ for it where $s$ is the number of lines (as no index is allowed to be this large in a NAND++ program).
We can now define NAND++ programs in a way analogous to [NANDprogram](){.ref}:

> # {.definition title="NAND++" #NANDpp}
A _NAND++ program_ is a 6-tuple $P=(V,X,Y,VALIDX,LOOP,L)$ of the following form:
>
* $V$ (called the _variable identifiers_) is some finite set.
>
* $X\in V$ is called the _input identifier_.
>
* $Y\in V$ is called the _output identifier_.
>
* $VALIDX \in V$ is the _input length identifier_.
>
* $LOOP \in V$ is the _loop variable_.
>
* $L \in (V\times [s+1] \times V \times [s+1] \times V \times [s+1])^*$ is a list of 6-tuples of the form $(a,j,b,k,c,\ell)$ where $a,b,c \in V$ and $j,k,\ell \in [s+1]$ for $s=|L|$.
That is, $L= ( (a_0,j_0,b_0,k_0,c_0,\ell_0),\ldots,(a_{s-1},j_{s-1},b_{s-1},k_{s-1},c_{k-1},\ell_{s-1}))$ where for every $t\in \{0,\ldots, s-1\}$, $a_t,b_t,c_t \in V$ and $j_t,k_t,\ell_t \in [s+1]$.
Moreover $a_t \not\in  \{X,VALIDX\}$ for every $t\in [s]$ and $b_t,c_t \not\in \{ Y,LOOP\}$ for every $t \in [s]$.
>

> # { .pause }
This definition is long but ultimately translating a NAND++ program from code to tuples can be done in  a fairly straightforward way. Please read the definition again to see that you can follow this transformation.
Note that there is a difference between the way we represent NAND++ and NAND programs.
In NAND programs, we used a different element of $V$ to represent, for example, `x_17` and `x_35`.
For NAND++ we will represent these two variables by $(X,17)$ and $(X,35)$ respectively where $X$ is the input identifier.
For this reason, in our definition of NAND++, $X$ is a single element of $V$ as opposed to a tuple of elements as in [NANDprogram](){.ref}.
For the same reason, $Y$ is a single element and not a tuple as well.

Just as was the case for NAND programs, we can define a _canonical form_ for NAND++ variables.
Specifically in the canonical form we will use $V=[t]$ for some $t>3$, $X=0$,$Y=1$,$VALIDX=2$ and $LOOP=3$.
Moreover, if $P$ is _simple_ in the sense of [simpleNANDpp](){.ref} then we will assume that the `halted` variable is encoded by $4$, and the `indexincreasing` variable is encoded by $5$.
The canonical form representation of  a NAND++ program is specified simply by a length $s$ list of $6$-tuples of natural numbers $(a,j,b,k,c,\ell)$ where $a,b,c \in [t]$ and $j,k,\ell \in [s+1]$.

Here is a Python code to evaluate a NAND++ program given the list of 6-tuples representation:

```python

```

```python
# Evaluates a  NAND++ program P on input x
# P is given in the list of tuples representation
# untested code
def EVALpp(P,x):
    vars = { 0:x , 2: [1]*len(x) } # vars[var][idx] is value of var_idx.
    # special variables: 0:X, 1:Y, 2:VALIDX, 3:LOOP
    t = len(P)

    def index(k): # compute i at loop j
        r = math.floor(math.sqrt(k+1/4)-1/2)
        return (k-r*(r+1) if k <= (r+1)*(r+1) else (r+1)*(r+2)-k)

    def getval(var,idx): # returns current value of var_idx
        if idx== t: idx = index(k)
        l = vars.getdefault(var,[])
        return l[idx] if idx<len(l) else 0

    def setval(var,idx,v): # sets var_idx := v
        l = vars.setdefault(var,[])
        l.append([0]*(1+idx-len(l)))
        l[idx]=v
        vars[var] = l

    k = 0
    while True:
        for t in P:
            setval(t[0],t[1], 1-getval(t[2],t[3])*getval(t[4],t[5]))
        if not getval(3,0): break
        k += 1

    return vars[1]
```

### Configurations

Just like we did for NAND programs, we can define the notion of a _configuration_ and a _next step function_ for NAND++ programs.
That is, a configuration of a program $P$ records all the state of $P$ at a given point in the execution, and contains everything we need to know in order to continue from this state.
The next step function of $P$ maps a configuration of $P$ into the configuration that occurs after executing one more line of $P$.

> # { .pause }
Before reading onwards, try to think how _you_ would define the notion of a configuration of a NAND++ program.

While we can define configurations in full generality, for concreteness we will restrict our attention to configurations of "simple" programs NAND++ programs in the sense of [simpleNANDpp](){.ref}, that are given in a canonical form.
Let $P$ be a canonical form simple program, represented as a list of $6$ tuples $L=((a_0,j_0,b_0,k_0,c_0,\ell_0),\ldots,(a_{s-1},j_{s-1},b_{s-1},k_{s-1},c_{s-1},\ell_{s-1}))$.
Let $s$ be the number of lines and $t$ be one more than the largest number appearing among the $a$'s, $b$'s or $c$'s.

Just like we did for NAND, a _configuration_ of the program $P$ will denote the current line being executed and the current value of all variables.
For our convenience we will use a somewhat different encoding than we did for NAND.
We will encode the configuration as a string $\sigma \in \{0,1\}^*$, which is composed of _blocks_, that is, $\sigma$ will be the concatenation of $\sigma^0,\ldots,\sigma^{r-1}$ for some $r\in \N$ (that will represent the maximum among $n-1$, where $n$ is the input length, the largest numerical index appearing in the program, and the  largest index that the program has ever reached in the execution).
Each block $\sigma^i$ will be a string of length $B$ (for some constant $B$ depending on $t,s$) that encodes the following:

* The  values of variables indexed by $i$ (e.g.,  `foo_`$\expr{i}$, `bar_`$\expr{i}$, etc.).

* Whether or not the block is "active" (i.e., whether the current value of the index variable `i` is $i$), and in the latter case, the current line that is being executed.

* Whether this is the first or last block.


> # {.remark title="High level points about configurations" #configdetails}
For the sake of completeness, we will describe below precisely how  configurations of NAND++ programs and the next-step function are defined.
However, the details are as important as the high level points, which are the following:
A configuration encodes all the information of the state of the program at a given step in the computation, including the values of all variables (both the Boolean variables and the special index variable `i`) and the current line number that is to be executed.
The next step function of a program $P$ updates that configuration by computing one line of the program, and updating the value of the variable that is assigned a value in this program.
The variables involved in that line either have absolute numerical indices (in which case they are encoded in one of the first $s$ blocks, as numerical indices can't be larger than the number of lines) or are indexed by the special variable `i` (in which case they are encoded in the active block).
If the line is the last one in the program, the next step function also determines whether to halt based on the `loop` variable, and updates the active block based on whether the index will be increasing or decreasing.



We now describe a precise encoding for the configurations of a NAND++ program.
Many of the choices below are made for convenience and other choices would be just as valid.
We will think of encoding each block as using the alphabet $\Sigma = \{ \mathtt{BB}, \mathtt{EB}, 0 , 1 \}$. ($\mathtt{BB}$ and $\mathtt{EB}$ stand for "begin block" and "end block" respectively; we can later encode this as a binary string using the map $0 \mapsto 00, 1\mapsto 11, \mathtt{BB} \mapsto 01, \mathtt{EB} \mapsto 10$.)
In this alphebt $\Sigma$, every block $\sigma^i$ will have the form

$$
\sigma^i = \mathtt{BB}\;\hat{\sigma}^{i} \; first \; last \; active \; p \; \mathtt{EB}
$$

where $\hat{\sigma}^i$ is a string in $\{0,1\}^t$  that encodes the values of all the variables in the program indexed by $i$.
That is, the $a$-th coordinate of $\hat{\sigma}^i$  corresponds to the value of the variable represented by $(a,i)$.
For example, if we encode `foo` by the number $11$ then $\hat{\sigma}^{17}_{11}$  corresponds to the value of `foo_17` at the given point in the execution.
We use the same indexing of variables as in representations and so in particular coordinates $0,1,2,3,4,5$ of $\hat{\sigma}^i$ correspond to the variables `x_i`,`y_i`,`validx_i`,`loop_i`,`halted_i`,`indexincreasing_i` respectively.^[Recall that we identify an unindexed variable identifier such as `foo` with `foo_0`, and so in particular the values of `loop`, `halted` and `indexincreasing` are encoded in the block $\sigma^0$.]


The values $active$, $first$, and $last$ are each bits that are set to $1$ or $0$ depending on whether  the current block is _active_ (i.e. the current value of `i` is $i$), is the _first_ block in the configuration and the _last_ block, respectively.
The parameter $p$ is a string in $\{0,1\}^{\ceil{\log(s+1)}}$, which (via the binary representation) we think of also as number in $[s+1]$.
The value of $p$ is equal to the current line that is about to be executed if the block is active, and to $0$ if the block is not active.
If $p=s$ then this means that we have halted.


Note that in the alphabet $\Sigma$, our encoding takes $2$ symbols for $\mathtt{BB}$ and $\mathtt{EB}$, $t$ symbols for $\hat{\sigma}^i$, three symbols for $first$,$last$,$active$, and $\log \ceil{s+1}$ symbols for encoding $p$.
Hence in the binary alphabet, each block $\sigma^i$ will be encoded as a string of length $B=2(5+t+\log(\ceil{s+1}))$ bits, and a configuration will be encoded as a binary string of length $(r+1)B$ where $r$ is the largest index that the variable `i` has reached so far in the execution.
See [configurationsnandpppng](){.ref} for an illustration of the configuration.

![A configuration of an $s$-line $t$-variable simple NAND++ program can be encoded as a string in $\{0,1\}^{rB}$, the $i$-th block encodes the value of all variables of the form `foo_`$\expr{i}$, as well as whether the block is first, last or active in the sense that `i`=$i$ and in the latter case, also the index of the current line being executed.](../figure/nandppconfiguration.png){#configurationsnandpppng .class width=300px height=300px}


For a simple $s$-line $t$-variable NAND++ program $P$ the _next configuration function_ $NEXT_P:\{0,1\}^* \rightarrow  \{0,1\}^*$ is defined in the natural way.^[We define $NEXT_P$ as a _partial_ function, that is only defined on strings that are valid encoding of a configuration, and in particular have only a single block with its active bit set, and where the initial and final bits are also only set for the first and last block respectively. It is of course possible to extend $NEXT_P$ to be a total function by defining it on invalid configurations in some way.]
That is,  on input a configuration $\sigma$, one can compute $\sigma'=NEXT_P(\sigma)$ as follows:

1. Scan the configuration $\sigma$ to find the index $i$ of the active block (block where the _active_ bit is set to $1$) and the current line $p$ that needs to be executed (which is enc). We  denote the new active block and current line in the configuration $\sigma'$ by $(i',p')$.

2. If $p=s$ then this $\sigma$ a halting configuration and $NEXT_p(\sigma) = \sigma$. Otherwise we continue to the following steps:

3.  Execute the line $p$: if the $p$-th tuple in the program is $(a,j,b,k,c,\ell)$ then we update $\sigma$ to $\sigma'$ based on the value of this program. That is,  in the configuration $\sigma'$, we encode the value of of the variable corresponding to $(a,j)$ as the NAND of the values of variables corresponding to  $(b,k)$ and $(c,\ell)$.^[Recall that according to the way we represent NAND++ programs as 6-tuples, if $a$ is the number corresponding to the identifier `foo` then $(a,j)$ corresponds to `foo_`$\expr{j}$ if $j<s$, and corresponds to `foo_`$\expr{i}$ if $j=s$ where $i$ is the current value of the index variable `i`.]

4. Updating the value of $i$: if $p=s-1$ (i.e., $p$ corresponds to the last line of the program), then we check whether the value of the `loop` or `loop_0` variable (which by our convention is encoded as the variable with index $3$ in the first block) and if so set in $\sigma'$ the value $p'=s$ which corresponds to a halting configuration. Otherwise, $i$ is either incremented and decremented based on  `indexincreasing` (which we can read from the first block). That is, we let $i'$ be either $i+1$ and $i-1$ based on `indexincreasing` and modify the active block in $\sigma'$ to be $i'$. (If $i$ is the final block and $i'=i+1$ then we create a new block and mark it to be the last one.)

5. We update $p'= p+1 \mod s$, and encode $p'$ in the active block of $\sigma'$.


One important property of $NEXT_P$ is that to compute it we only need to access the blocks $0,\ldots,s-1$ (since the largest absolute numerical index in the program is at most $s-1$) as well as the current active block and its immediate neighbors.
Thus in each step, $NEXT_P$ only reads or modifies a constant number of blocks.

Here is some Python code for the next step function:

```python
# compute the next-step configuration
# Inputs:
# P: NAND++ program in list of 6-tuples representation  (assuming it has an "indexincreasing" variable)
# conf: encoding of configuration as a string using the alphabet "B","E","0","1".
def next_step(P,conf):
    s = len(P) # numer of lines
    t = max([max(tup[0],tup[2],tup[4]) for tup in P])+1 # number of variables
    line_enc_length = math.ceil(math.log(s+1,2)) # num of bits to encode a line
    block_enc_length = t+3+line_enc_length # num of bits to encode a block (without bookends of "E","B")
    LOOP = 3
    INDEXINCREASING = 5
    ACTIVEIDX = block_enc_length -line_enc_length-1 # position of active flag
    FINALIDX =  block_enc_length  -line_enc_length-2 # position of final flag

    def getval(var,idx):
        if idx<s: return int(blocks[idx][var])
        return int(active[var])

    def setval(var,idx,v):
        nonlocal blocks, i
        if idx<s: blocks[idx][var]=str(v)
        blocks[i][var]=str(v)

    blocks = [list(b[1:]) for b in conf.split("E")[:-1]] # list of blocks w/o initial "B" and final "E"

    i = [j for j in range(len(blocks))  if blocks[j][ACTIVEIDX]=="1" ][0]
    active = blocks[i]

    p = int("".join(active[-line_enc_length:]),2) # current line to be executed

    if p==s: return conf # halting configuration

    (a,j,b,k,c,l) = P[p] #  6-tuple corresponding to current line#  6-tuple corresponding to current line
    setval(a,j,1-getval(b,k)*getval(c,l))

    new_p = p+1
    new_i = i
    if p==s-1: # last line
        new_p = (s if getval(LOOP,0)==0 else 0)
        new_i = (i+1 if getval(INDEXINCREASING,0) else i-1)
        if new_i==len(blocks): # need to add another block and make it final
            blocks[len(blocks)-1][FINALIDX]="0"
            new_final = ["0"]*block_enc_length
            new_final[FINALIDX]="1"
            blocks.append(new_final)

        blocks[i][ACTIVEIDX]="0" # turn off "active" flag in old active block
        blocks[i][ACTIVEIDX+1:ACTIVEIDX+1+line_enc_length]=["0"]*line_enc_length # zero out line counter in old active block
        blocks[new_i][ACTIVEIDX]="1" # turn on "active" flag in new active block
    new_p_s = bin(new_p)[2:]
    new_p_s = "0"*(line_enc_length-len(new_p_s))+new_p_s
    blocks[new_i][ACTIVEIDX+1:ACTIVEIDX+1+line_enc_length] = list(new_p_s) # add binary representation of next line in new active block

    return "".join(["B"+"".join(block)+"E" for block in blocks]) # return new configuration
```


### Deltas

Sometimes it is  easier to keep track of merely the _changes_ (sometimes known as "deltas") in the state of a NAND++ program, rather than the full configuration.
Since every step of a NAND++ program assigns a value to a single variable, this motivates the following definition:

> # {.definition title="Modification logs of NAND++ program" #deltas}
The _modification log_ (or "deltas") of an $s$-line simple NAND++ program $P$ on an input $x\in \{0,1\}^n$ is the string $\Delta$ of length $sT+n$ whose first $n$ bits are equal to $x$ and the last $sT$ bits correspond to the value assigned in each step of the program. That is, for every $i\in [n]$, $\Delta_i=x_i$  and for every $\ell \in [sT]$,  $\Delta_{\ell+n}$ equals to the value that is assigned by the line executed in step $\ell$ of the execution of $P$ on input $x$, where $T$ is the number of iterations of the loop that $P$ does on input $x$.

If $\Delta$  is the "deltas" of $P$ on input $x \in \{0,1\}^n$, then for every $\ell\in [Ts]$, $\Delta_\ell$  is the same as the value assigned by line $\ell$  of the NAND program $expand_{T',n}(P)$ where $s$ is the number of lines in $P$, and for every $T'$ which is at least the number of loop iterations that $P$ takes on input $x$.

> # {.remark title="Snapshots and deltas: what you need to remember" #snapshotsremark}
The details of the definitions of configuration and deltas are not as important as the main points which are: \
>
* A _configuration_ is the full state of the program at a certain point in the computation. Applying the $NEXT_P$ function to the current configuration yields the next configuration. \
>
* Each configuration can be thought of as a string which is a  sequence of constant-size _blocks_. The $NEXT_P$ function only depends and modifies  a constant number of blocks: the $t$ first ones, the current active block, and its two adjacent neighbors. \
>
* The "delta" or "modification log" of computation is a succinct description of how the configuration changed in each step of the computation. It is simply the string $\Delta$  of length $T$ such that for every $\ell \in T$, $\Delta_\ell$ is denotes the value assigned in the $\ell$-th step of the computation.
>
Both configurations and Deltas are technical ways to capture the fact that computation is a complex process that is obtained as the result of a long sequence of simple steps.

-->


> # { .recap }
* NAND++ programs introduce the notion of _loops_, and allow us to capture a single algorithm that can evaluate functions of any input length.
* Running a NAND++ program for any finite number of steps corresponds to a NAND program. However, the key feature of NAND++ is that the number of iterations can depend on the input, rather than being a fixed upper bound in advance.
* A _configuration_ of a NAND++ program encodes the state of the program at a given point in the computation. The _next step function_ of the program maps the current configuration to the next one.

## Exercises


::: {.exercise title="Well formed NAND++ programs" #noabsoluteindexex}
Let $P$ be a NAND++ program. Prove that there exists a NAND++ program $P'$ that computes the same function as $P$, such that every variable in $P'$ is either a scalar (non array variable), or is an array indexed by `i`.^[_Hint:_   We can replace references to `Foo[17]` with `foo_17`. We can also use a finite number of variables to keep track of when the index variable `i` reaches the point `17`, in which case we write `foo_17` to the value of `Foo[i]`.]
:::



## Bibliographical notes

The notion of "NAND++ programs" we use is nonstandard but (as we will see)  they are equivalent to standard models used in the literature.
Specifically, NAND++ programs are closely related (though not identical) to _oblivious one-tape Turing machines_, while NAND<< programs are essentially the same as RAM machines.
As we've seen in these lectures, in a qualitative sense these two models are also equivalent to one another, though the distinctions between them matter if one cares (as is typically the case in algorithms research) about polynomial factors in the running time.

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
