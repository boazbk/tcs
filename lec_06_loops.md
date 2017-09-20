# Loops and infinity

> # { .objectives }
* Learn the model of NAND++ program that involve loops.
* See some basic syntactic sugar for NAND++
* Get comfort with switching between representation of NAND++ programs as code and as tuples.
* Learn the notion of _configurations_ for NAND++ programs.
* Understand the relation between NAND++ and NAND programs.

>_"We thus see that when $n=1$, nine operation-cards are used; that when $n=2$, fourteen Operation-cards are used; and that when $n>2$, twenty-five operation-cards are used; but that no more are needed, however great $n$ may be; and not only this, but that these same twenty-five cards suffice for the successive computation of all the numbers"_, Ada Augusta, countess of Lovelace, 1843^[Translation of  "Sketch of the Analytical Engine" by L. F. Menabrea, Note G.]

>_"It is found in practice that (Turing machines) can do anything that could be described as 'rule of thumb' or 'purely mechanical'... (Indeed,) it is  now agreed amongst logicians that 'calculable by means of (a Turing Machine)' is the correct accurate rendering of such phrases."_, Alan Turing, 1948



The NAND programming language has one very significant drawback: a finite NAND program $P$ can only compute a finite function $F$, and in particular the number of inputs of $F$ is always smaller than the number of lines of $P$.
This does not capture our intuitive notion of an algorithm as a _single recipe_ to compute a potentially infinite function.
For example, the standard elementary school multiplication algorithm is a _single_ algorithm that multiplies numbers of all lengths, but yet we cannot express this algorithm as a single NAND program, but rather need a different NAND program for every input length.


Let us consider the case of the simple _parity_ or _XOR_ function  $XOR:\{0,1\}^* \rightarrow \{0,1\}$, where $XOR(x)$ equals $1$ iff the number of $1$'s in $x$ is odd.
As simple as it is, the $XOR$ function cannot be computed by a NAND program.
Rather, for every $n$, we can compute $XOR_n$ (the restriction of $XOR$ to $\{0,1\}^n$) using a different NAND program. For example, here is the NAND program to compute $XOR_5$:

~~~~ { .go .numberLines }
u   := x_0 NAND x_1
v   := x_0 NAND u
w   := x_1 NAND u
s   := v   NAND w
u   := s   NAND x_2
v   := s   NAND u
w   := x_2 NAND u
s   := v   NAND w
u   := s   NAND x_3
v   := s   NAND u
w   := x_3 NAND u
s   := v   NAND w
u   := s   NAND x_4
v   := s   NAND u
w   := x_4 NAND u
y_0 := v   NAND w
~~~~

This is rather repetitive, and more importantly, does not capture the fact that there is a _single_ algorithm to compute the parity on all inputs.
Typical programming language use the notion of _loops_ to express such an algorithm, and so we might have wanted to use code such as:

~~~~ { .go .numberLines }
# s is the "running parity", initalized to 0
while i < length(x):
    u   := x_i NAND s
    v   := s   NAND u
    w   := x_i NAND u
    s  := v   NAND w
    i++
ns  := s  NAND s
y_0 := ns NAND ns
~~~~

We will now discuss how we can extend the  NAND programming language so that it can capture this kind of a construct.


## The NAND++ Programming language

Keeping to our minimalist form, we will not add a `while` keyword to the NAND programming language.
But we will extend this language in a way that allows for executing loops and accessing arrays of arbitrary length.  
The main new ingredients are the following:

* We add a special variable `loop` with the following semantics: after executing the last line of the program, if `loop` is equal to one, then instead of halting, the program goes back to the first line. If `loop` is equal to zero after executing the last line then the program halts as is usually with NAND.^[This corresponds to wrapping the entire program in one big loop that is executed at least once and continues as long as `loop` is equal to $1$. For example, in the C programming language this would correspond with wrapping the entire program with the construct `do { ...} while (loop);`.]

* We add a special _integer valued_ variable `i`, and allow expressions of the form `foo_i` (for every variable identifier `foo`) which are evaluated to equal `foo_`$\expr{i}$ (where $\expr{i}$ denotes the current value of the variable `i`).
For example, if the current value of `i` is equal to 15, then `foo_i` corresponds to `foo_15`.^[Note that the variable `i`, like all variables in NAND, is a _global_ variable, and hence  all expressions of the form `foo_i`, `bar_i` etc. refer to the same value of `i`.]
In the first loop of the program, `i` is assigned the value $0$, but each time the program loops back to the first line, the value of `i` is updated in the following manner:
in the $k$-th iteration the value of `i` equals $I(k)$ where $I=(I(0),I(1),I(2),\ldots)$ is the following sequence (see [indextimefig](){.ref}):

$$
0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots
$$


* Because the input to NAND++ programs can have variable length, we also add a special read-only array `validx` such that `validx_`$\expr{n}$ is equal to $1$ if and only if the $n$ is smaller than the length of the input. In particular, `validx_i` will equal to $1$ if and only if the value of  `i`  is smaller than the length of the input.


* Like NAND programs, the output of a  NAND++ program is the string `y_`$0$, $\ldots$, `y_`$\expr{k}$  where $k$ is the largest integer such that `y_`$\expr{k}$ was assigned a value.

![The value of `i` as a function of the current iteration. The variable `i` progresses according to the sequence $0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots$.  At the $k$-th iteration the value of `i` equals $k-r(r+1)$ if $k \leq (r+1)^2$ and $(r+1)(r+2)-k$ if $k<(r+1)^2$ where $r= \floor{\sqrt{k+1/4}-1/2}$.](../figure/indextime.png){#indextimefig .class width=300px height=300px}


See the appendix for a more formal specification of the NAND++ programming language, and the website [http://nandpl.org](http://nandpl.org) for an implementation.
Here is the NAND++ program to compute parity of arbitrary length:
(It is a good idea for you to see why this program does indeed compute the parity)


~~~~ { .go .numberLines }
# compute sum x_i (mod 2)
# s = running parity
# seen_i = 1 if this index has been seen before

# Do val := (NOT seen_i) AND x_i
tmp1  := seen_i NAND seen_i
tmp2  := x_i NAND tmp1
val   :=  tmp2 NAND tmp2

# Do s := s XOR val
ns   := s   NAND s
y_0  := ns  NAND ns
u    := val NAND s
v    := s   NAND u
w    := val NAND u
s    := v   NAND w

seen_i := zero NAND zero  
stop := validx_i NAND validx_i
loop := stop     NAND stop
~~~~


When we invoke this program on the input $010$, we get the following execution trace:

```
... (complete this here)
End of iteration 0, loop = 1, continuing to iteration 1
...
End of iteration 2, loop = 0, halting program  
```

### Computing the index location

We say that a NAND program completed its _$r$-th round_ when the index variable `i` completed the sequence:

$$
0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots,0,1,\ldots,r,r-1,\ldots,0
$$

This happens when the program completed

$$
1+2+4+6+\cdots+2r =r^2 +r + 1
$$

iterations of its main loop. (The last equality is obtained by applying the formula for the sum of an algebraic progression.)
This means that if we keep a "loop counter" $k$ that is initially set to $0$ and increases by one at the end of any iteration, then  the "round" $r$ is the largest integer such that $r(r+1) \leq k$, which (as you can verify) equals $\floor{\sqrt{k+1/4}-1/2}$.

Thus the value of `i` in the  $k$-th loop equals:

$$
index(k) = \begin{cases} k- r(r+1) & k \leq (r+1)^2 \\ (r+1)(r+2)-k & \text{otherwise} \end{cases} \label{eqindex}
$$

where $r= \floor{\sqrt{k+1/4}-1/2}$.
(We ask you to prove this in [computeidx-ex](){.ref}.)





### Infinite loops and computing a function

One crucial difference between NAND and NAND++ programs is the following.
Looking at a NAND program $P$, we can always tell how many inputs and how many outputs it has (by simply counting  the number of `x_` and `y_` variables).
Furthermore, we  are guaranteed that if we invoke $P$ on any input then _some_ output will be produced.  
In contrast, given any particular NAND++ program $P'$, we cannot determine a priori the length of the output.
In fact, we don't even know  if an output would be produced at all!
For example, the following NAND++ program would go into an infinite loop if the first bit of the input is zero:

~~~~ { .go .numberLines }
loop := x_0 NAND x_0
~~~~

For a NAND++ program $P$ and string $x\in \{0,1\}^*$, if $P$ produces an output when executed with input $x$ then we denote this output by $P(x)$.
If $P$ does not produce an output on $x$ then we say that $P(x)$ is _undefined_ and denote this as $P(x) = \bot$.

> # {.definition title="Computing a function" #compute}
We say that a NAND++ program $P$ _computes_ a function $F:\{0,1\}^* :\rightarrow \{0,1\}^*$ if $P(x)=F(x)$ for every $x\in \{0,1\}^*$.
>
If $F$ is a partial function then we say that _$P$ computes $F$_ if $P(x)=F(x)$ for every $x$ on which $F$ is defined.




## A spoonful of sugar

Just like NAND, we can add a bit of "syntactic sugar" to NAND++ as well.
These are constructs that can help us in expressing programs, though ultimately do not change the computational power of the model, since any program using these constructs can be "unsweetened" to obtain a program without them.

### Inner loops via syntactic sugar

While  NAND+  only has a single "outer loop",  we can use conditionals to implement inner loops as well.
That is, we can replace code such as


~~~~ { .go .numberLines }
PRELOOP_CODE
while (cond) {
 LOOP_CODE
}
POSTLOOP_CODE
~~~~


by

~~~~ { .go .numberLines }
// startedloop is initialized to 0
// finishedloop is initalized to 0
if NOT(startedloop)  {
    PRELOOP_CODE
    startedloop := 1
}
if NOT(finishedloop) {
    temploop := loop
    if (cond) {
        LOOP_CODE
        loop :=1
    }
    if NOT(cond) {
        finishedloop := 1
        loop := temploop
    }
}
if (finishedloop) {
    POSTLOOP_CODE
}
~~~~

(Applying the standard syntactic sugar transformations to convert the conditionals into NAND code.)
We can apply this transformation repeatedly to convert programs with multiple loops, and even nested loops, into a standard NAND++  program.

> # { .pause }
Please stop and verify that you understand why this transformation will result in a program that computes the same function as the original code with an inner loop.

### Controlling the index variable

NAND++ is an _oblivious_ programming model, in the sense that it gives  us no means of controlling the index variable `i`.
Rather to read a certain variable such as `foo_52` we need to wait until `i` will equal $52$.
However we can use syntactic sugar to simulate the effect of incrementing and decrementing `i`.
That is, rather than having `i` move according to a fixed schedule, we can assume that we have the operation `i++ (foo)` that increments `i` if `foo` is equal to $1$ (and otherwise leaves `i` in place), and similarly the operation `i-- (bar)` that decrements `i` if `bar` is $1$ and otherwise leaves `i` in place.

To achieve this, we start with the  observation  that in  a NAND++ program we can know whether the index is increasing or decreasing.
We achieve this using the Hansel and Gretel technique of leaving _"breadcrumbs"_.
Specifically, we create an array `atstart` such that `atstart_0` equals $1$ but `atstart_`$\expr{j}$ equals $0$ for all $j>0$, and an array `breadcrumb` where we set `breadcrumb_i` to $1$ in every iteration.
Then we can setup a variable `indexincreasing` and set it to $1$ when we reach the zero index (i.e., when `atstart_i` is equal to $1$) and set it to $0$ when we reach the end point (i.e., when we see an index for which `breadcrumb_i` is $0$ and hence we have reached it for the first time).
We can also maintain an array `arridx` that contains $0$ in all positions except the current value of `i`.

![We can simulate controlling the index variable `i` by keeping an array `atstart` letting us know when `i` reaches $0$, and hence `i` starts increasing, and `breadcrumb` letting us know when we reach a point we haven't seen before, and hence `i` starts decreasing. If we are at a point in which the index is increasing but we want it to decrease then we can mark our location on a special array `arridx` and enter a loop until the time we reach the same location again.](../figure/breadcrumbs.png){#breadcrumbspng .class width=300px height=300px}

Now we can simulate incrementing and decrementing `i` by one by simply waiting until our desired outcome happens naturally.
(This is similar to  the observation that a bus is like a taxi if you're willing to wait  long enough.)
That is, if we want to increment `i` and `indexincreasing` equals $1$ then we simply wait one step.
Otherwise (if `indexincreasing` is $0$) then we go into an inner loop in which we do nothing until we reach again the point when `arridx_i` is $1$ and  `indexincreasing` is equal to $1$.
Decrementing `i` is done in the analogous way.^[It can be verified that this transformation converts a program with $T$ steps that used the `i++ (foo)` and `i-- (bar)` operations into a program with $O(T^2)$ that doesn't use them.]

### "Simple" NAND++ programs

When analyzing NAND++ programs, it will sometimes be convenient for us to restrict our attention to programs of a somewhat nicer form.

> # {.definition title="Simple NAND++ programs" #simpleNANDpp}
We say that a NAND++ program $P$ is _simple_ if it has the following properties:
>
* The only output variable it ever writes to is `y_0` (and so it computes a Boolean function).
>
* The last line of the program has the form `halted := loop NAND loop` and so the variable `halted` gets the value $1$ when the program halts. Moreover, there is no other line in the program that writes to the variable `halted`.
>
* All lines that write to the variable `loop` or `y_0` are "guarded" by `halted` in the sense that we replace a line of the form `y_0 := foo NAND bar` with the (unsweetened equivalent to) `if NOT(halted) { y_0 := foo NAND bar }` and similarly `loop := blah NAND baz` is replaced with `if NOT(halted) {loop := blah NAND baz }`.
>
* It has an `indexincreasing` variable that is equal to $1$ if and only if in the next iteration the value of `i` will increase by $1$.
>
* It contains variables `zero` and `one` that are initialized to be $0$ and $1$ respectively, by having the first line be `one := zero NAND zero` and having no other lines that assign values to them.

Note that if $P$ is a simple program then even if we continue its execution beyond the point it should have halted in, the value of the `y_0` and `loop` variables will not change.
The following theorem shows that, in the context of Boolean functions, we can assume that every program is simple:^[The restriction to Boolean functions is not very significant, as we can always encode a non Boolean function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ by the Boolean function $G(x,i)=F(x)_i$ where we treat the second input $i$ as representing an integer. The crucial point is that we still allow the functions to have an unbounded _input length_ and hence in particular these are functions that cannot be computed by plain "loop less" NAND programs.]

> # {.theorem title="Simple program" #simpleNANDthm}
Let $F:\{0,1\}^* \rightarrow \{0,1\}$ be a (possibly partial) Boolean function. If there is a NAND++ program that computes $F$ then there is a simple NAND++ program $P'$ that computes $F$ as well.

> # {.proof data-ref="simpleNANDthm"}
If $P$ computes a Boolean function then it cannot write to any `y_`$\expr{j}$ variable when $j \neq 0$.
Now we obtain the simple NAND++ program $P'$ by simply modifying the code of $P$ to satisfy the properties above.
If $P$ already used a variable named `halted` then we rename it.
We then  we add the line `halted := loop NAND loop` to the end of the program, and replace all lines writing to the variables `y_0` and `loop` with their "guarded" equivalents.
Finally, we ensure the existence of the variable `indexincreasing` using the breadrumbs technique discussed above.



## Uniformity, and NAND vs NAND++


While NAND++ adds an extra operation over NAND, it is not exactly accurate to say that NAND++ programs are "more powerful" than NAND programs.
NAND programs, having no loops, are simply not applicable for computing functions with more inputs than they have lines.
The key difference between NAND and NAND++ is that NAND++ allows us to express the fact that the algorithm for computing parities of length-$100$ strings is really the same one as the algorithm for computing parities of length-$5$ strings (or similarly the fact that the algorithm for adding $n$-bit numbers is the same for every $n$, etc.).
That is, one can think of the NAND++ program for general parity as the "seed" out of which we can grow NAND programs for length $10$, length $100$, or length $1000$ parities as needed.
This notion of a single algorithm that can compute functions of all input lengths is known as _uniformity_ of computation and hence we think of NAND++ as  _uniform_ model of computation, as opposed to NAND which is a _nonuniform_ model, where we have to specify a different program for every input length.


Looking ahead, we will see that this uniformity leads to another crucial difference between NAND++ and NAND programs.
NAND++ programs can have inputs and outputs that are longer than the description of the program and in particular we can have a NAND++ program that "self replicates" in the sense that it can print its own code.   
This notion of "self replication", and the related notion of "self reference" is crucial to many aspects of computation, as well  of course to life itself, whether in the form of digital or biological programs.

### Growing a NAND tree


If $P$ is a NAND++ program and $n,T\in \N$ are some numbers, then we can easily obtain a NAND program $P'=expand_{T,n}(P)$ that, given any $x\in \{0,1\}^n$, runs $T$ iterations of the program $P$ and outputs the result.
If $P$ is a simple program, then we are guaranteed that, if $P$ does not enter an infinite loop on $x$, then as long as we make $T$ large enough, $P'(x)$ will equal $P(x)$.
To obtain the program $P'$ we can simply place $T$ copies of the program $P$ one after the other, doing a "search and replace" in the $k$-th copy of any instances of `_i` with the value $index(k)$, where the function $index$ is defined as in [eqindex](){.eqref}. For example, [expandnandpng](){.ref} illustrates  the expansion of the  NAND++ program for parity.


![A NAND program for parity obtained by expanding the NAND++ program](../figure/expandnand.png){#expandnandpng .class width=300px height=300px}

We can also obtain such an expansion by using the `for .. do { .. }` syntactic sugar.
For example, the NAND program below corresponds to running the parity program for 17 iterations, and computing $XOR_5:\{0,1\}^5 \rightarrow \{0,1\}$. Its standard "unsweetened" version will have $17 \cdot 10$ lines.^[This is of course not the most efficient way to compute $XOR_5$. Generally, the NAND program to compute $XOR_n$ obtained by expanding out the  NAND++ program will require $\Theta(n^2)$ lines, as opposed to the $O(n)$ lines that is possible to achieve directly in NAND. However, in most cases this difference will not be so crucial for us.]

~~~~ { .go .numberLines }
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
~~~~



In particular we have the following theorem

> # {.theorem title="Expansion of NAND++ to NAND" #NANDexpansionthm}
For every simple NAND++ program $P$ and function $F:\{0,1\}^* \rightarrow \{0,1\}$, if $P$ computes $F$ then for every $n\in\N$ there exists $T\in \N$ such that $expand_{T,n}(P)$ computes $F_n$.

> #{.proof}
We'll start with a "proof by code". Here is a Python program `expand` to compute $expand_{T,n}(P)$.
On  input the code $P$ of a NAND++ program and numbers $T,n$, `expand` outputs the code of the NAND program $P'$ that works on length $n$ inputs and is obtained by running $T$ iterations of $P$:
>
~~~~ { .python }
def index(k):
    r = math.floor(math.sqrt(k+1/4)-1/2)
    return (k-r*(r+1) if k <= (r+1)*(r+1) else (r+1)*(r+2)-k)

def expand(P,T,n):
    result = ""

    for k in range(T):
        i=index(k)
        validx = (`one` if i<n else `zero`)
        result += P.replace('validx_i',validx).replace('x_i',('x_i' if i<n else 'zero')).replace('_i','_'+str(i))

    return result
~~~~
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

~~~~ { .python }
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
~~~~

### Configurations

Just like we did for NAND programs, we can define the notion of a _configuration_ and a _next step function_ for NAND++ programs.
That is, a configuration of a program $P$ records all the state of $P$ at a given point in the execution, and contains everything we need to know in order to continue from this state.
The next step function of $P$ maps a configuration of $P$ into the configuration that occurs after executing one more line of $P$.

> # { .pause }
Before reading onwards, try to think how _you_ would define the notion of a configuration of a NAND++ program.

While we can define configurations in full generality, for concreteness we will restrict our attention to configurations of "simple" programs NAND++ programs in the sense of [simpleNANDpp](){.ref}, that are given in a canonical form.
Let $P$ be a canonical form simple program, represented as a list of $6$ tuples $L=((a_0,j_0,b_0,k_0,c_0,\ell_0),\ldots,(a_{s-1},j_{s-1},b_{s-1},k_{s-1},c_{s-1},\ell_{s-1}))$.
Let $t$ be one more than the largest number appearing among the $a$'s, $b$'s or $c$'s.
A _configuration_ of the program $P$ is a number $t' \in [t]$ and a binary string $\sigma$ of length $r(t+2)$ for some $r\in \N$ such that $\sigma = \sigma^0\sigma^1\cdots \sigma^{r-1}$ where each $\sigma_i$ is a block of $\sigma$ of length $t+2$.
The $a$-th coordinate of the block $\sigma^i$ (denoted by $\sigma^i_a$) corresponds to the value of the variable represented by $(a,i)$.
For example, if we encode `foo` by the number $11$ then $\sigma^{17}_{11}$ (i.e., the $12$-th coordinate  of the $17$-th block) corresponds to the value of `foo_17` at the given point in the execution.
The last two coordinates of $\sigma_i$ are special: $\sigma^i_t$ equals $1$ if and only if the current value of `i` is $i$, in which case we say that $\sigma^i$ is the _active_ block.
$\sigma^i_{t+1}$ equals $1$ if and only if $i=r-1$ (i.e., $i$ is the last block in the configuration). See [configurationsnandpppng](){.ref} for an illustration of the configuration.

![A configuration of a $t$-line simple NAND++ program can be encoded as a string in $\{0,1\}^{r(t+2)}$, the $i$-th block contains the value of all variables of the form `foo_`$\expr{i}$ and the last two bits of the block signal whether `i`=$i$ and whether this is the last block of the configuration.](../figure/configurationsnandpp.png){#configurationsnandpppng .class width=300px height=300px}

For a simple $t$-line NAND++ program $P$ the _next configuration function_ $NEXT_P:[t] \times \{0,1\}^* \rightarrow [t] \times \{0,1\}^*$ is defined in the natural way.
That is, given a line $p \in [t]$  and a configuration $\sigma$, we compute $p',\sigma'$ by:

*  Executing the line $p$: if $p=(a,j,b,k,c,\ell)$ then we let $\sigma'^\overline{j}_a = 1-\sigma^{\overline{k}}_b\cdot \sigma^{\overline{\ell}}_c$ where $\overline{j}$ equals $j$ if $j<t$ and equals the index of the current active block $i$ if $j=t$, and $\overline{k}$, $\overline{\ell}$ are defined analogously.

* Updating the value of $i$: we set $\sigma'^i_{t}=0$ and if $\sigma^0_5=1$ (which corresponds to `indexincreasing`) then we let $\sigma'^{i+1}_t=1$ and otherwise we let $\sigma'^{i-1}_t=1$. (If $i$ was the last active block then we create a new block and mark it to be the last one.)

* Moving to $p+1 \mod t$ unless $p=|t|$ and $\sigma^0_3$ (corresponding to `loop`) is equal to $0$, in which case we let $p'=t+1$, which is considered a halting configuration that is never modified by $NEXT_P$.

One important property of $NEXT_P$ is that to compute it we only need to access the blocks $0,\ldots,t-1$ (since the largest absolute numerical index in the program is at most $t-1$) as well as the current active block and its immediate neighbors.
Thus in each step, $NEXT_P$ only reads or modifies a constant number of blocks.

### Deltas

Sometimes it is  easier to keep track of merely the _changes_ (sometimes known as "deltas") in the state of a NAND++ program, rather than the full configuration.
Since every step of a NAND++ program assigns a value to a single variable, this motivates the following definition:

> # {.definition title="Modification logs of NAND++ program" #deltas}
The _modification log_ (or "deltas") of an $s$-line simple NAND++ program $P$ on an input $x\in \{0,1\}^n$ is the string $\Delta$ of length $sT$ such that for every $\ell \in [sT]$,  $\Delta_\ell$ equals to the value that is assigned by the line executed in step $\ell$ of the execution $P(x)$, where $T$ is the number of iterations of the loop that $P$ does on input $x$.

If $\Delta$  is the "deltas" of $P$ on input $x \in \{0,1\}^n$, then for every $\ell\in [Ts]$, $\Delta_\ell$  is the same as the value assigned by line $\ell$  of the NAND program $expand_{T',n}(P)$ where $s$ is the number of lines in $P$, and for every $T'$ which is at least the number of loop iterations that $P$ takes on input $x$.




## Lecture summary

* NAND++ programs introduce the notion of _loops_, and allow us to capture a single algorithm that can evaluate functions of any input length.
* Running a NAND++ program for any finite number of steps corresponds to a NAND program. However, the key feature of NAND++ is that the number of iterations can depend on the input, rather than being a fixed upper bound in advance.


## Exercises

> # {.exercise title="Compute index" #computeidx-ex}
Suppose that $pc$ is the "program counter" of a NAND++ program, in the sense that $pc$ is initialized to zero, and is incremented by one each time the program finishes an iteration and goes back to the first line.
Prove that the value of the variable `i` is equal to $pc-r(r+1)$ if $pc \leq (r+1)^2$ and equals $(r+2)(r+1)-pc$ otherwise, where $r = \floor{\sqrt{pc+1/4}-1/2}$.



## Bibliographical notes

The notion of "NAND++ programs" we use is nonstandard but (as we will see)  they are equivalent to standard models used in the literature.
Specifically, NAND++ programs are closely related (though not identical) to _oblivious one-tape Turing machines_, while NAND<< programs are essentially the same as RAM machines.
As we've seen in these lectures, in a qualitative sense these two models are also equivalent to one another, though the distinctions between them matter if one cares (as is typically the case in algorithms research) about polynomial factors in the running time.

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
