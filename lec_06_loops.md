# Loops and infinity

>_"We thus see that when $n=1$, nine operation-cards are used; that when $n=2$, fourteen Operation-cards are used; and that when $n>2$, twenty-five operation-cards are used; but that no more are needed, however great $n$ may be; and not only this, but that these same twenty-five cards suffice for the successive computation of all the numbers"_, Ada Augusta, countess of Lovelace, 1843^[Translation of  "Sketch of the Analytical Engine" by L. F. Menabrea, Note G.]

>_"It is found in practice that (Turing machines) can do anything that could be described as 'rule of thumb' or 'purely mechanical'... (Indeed,) it is  now agreed amongst logicians that 'calculable by means of (a Turing Machine)' is the correct accurate rendering of such phrases."_, Alan Turing, 1948

>_"All problems in computer science can be solved by another level of indirection"_,  attributed to David Wheeler.




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

![The value of `i` as a function of the current iteration. The variable `i` progresses according to the sequence $0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots$.  At the $k$-th iteration the value of `i` equals $k-r(r+1)$ if $k \leq (r+1)^2$ and $(r+1)(r+2)-k$ if $k<(r+1)^2$ where $r= \floor{\sqrt{pc+1/4}-1/2}$.](../figure/indextime.png){#indextimefig .class width=300px height=300px}


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
index(k) = \begin{cases} k- r(r+1) & k \leq (r+1)^2 \\ (r+1)(r+2)-k & \text{otherwise} \end{cases}
$$

where $r= \floor{\sqrt{k+1/4}-1/2}$.
(We ask you to prove this in [computeidx-ex](){.ref}.)

### Remark: Inner loops via syntactic sugar

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




### Uniformity and NAND vs NAND++

While NAND++ adds an extra operation over NAND, it is not exactly accurate to say that NAND++ programs are "more powerful" than NAND programs.
NAND programs, having no loops, are simply not applicable for computing functions with more inputs than they have lines.
The key difference between NAND and NAND++ is that NAND++ allows us to express the fact that the algorithm for computing parities of length-$100$ strings is really the same one as the algorithm for computing parities of length-$5$ strings (or similarly the fact that the algorithm for adding $n$-bit numbers is the same for every $n$, etc.).
That is, one can think of the NAND++ program for general parity as the "seed" out of which we can grow NAND programs for length $10$, length $100$, or length $1000$ parities as needed.
This notion of a single algorithm that can compute functions of all input lengths is known as _uniformity_ of computation and hence we think of NAND++ as  _uniform_ model of computation, as opposed to NAND which is a _nonuniform_ model, where we have to specify a different program for every input length.


Looking ahead, we will see that this uniformity leads to another crucial difference between NAND++ and NAND programs.
NAND++ programs can have inputs and outputs that are longer than the description of the program and in particular we can have a NAND++ program that "self replicates" in the sense that it can print its own code.   
This notion of "self replication", and the related notion of "self reference" is crucial to many aspects of computation, as well  of course to life itself, whether in the form of digital or biological programs.


> # {.remark title="Advanced note: NAND++ as a 'seed' for NAND." #nandefficienct}
 This notion of a NAND++ program as a "seed" that can grow a different NAND program for every input length is one that we will come back to later on in this course, when we consider bounding the _time complexity_ of computation.
As we will see, we can think of a NAND++ program $P$ that computes some function $F$ in $T(n)$ steps on input length $n$, as a two phase process.
For any  input $x\in \{0,1\}^*$, the program $P$ can be thought of as first producing a $T(|x|)$-line NAND program $P'$, and then executing this program $P'$ on $x$.
This might not be easy to see at this point, but will become clearer in a few lectures when we tackle the issue of _efficiency_ in computation.


### Infinite loops and computing a function

There is another important difference between NAND and NAND++ programs: looking at a NAND program $P$, we can always tell how many inputs and how many outputs it has (by looking at the number of `x_` and `y_` variables).
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


### NAND++ normal form

In many programming language, we can make syntactic transformation on programs that do not change their operations, but might make them "cleaner" or "easier to understand" in some way.
For example, we could declare variables in the beginning of every function even if this is not required by the programming language.
For NAND++, it will also be sometimes useful for us that a programs have a "nice form", which we can ensure by making some syntactic transformations.
Specifically we will make the following definition:

> # {.definition title="NAND++ normal form" #normalform}
We say that a NAND++ program $P$ is in _normal form_ if it satisfies the following properties:
>
1. $P$ has a variable `indexincreasing` with the code to ensure that `indexincreasing` is $1$ whenever in the next iteration the value of `i` increases and `indexincreasing` is $0$ otherwise.  \
2. $P$ has a variable `zero` with the code to ensure that `zero_i` is equal to $1$ if and only if `i` is zero.
3. There are no absolute numerical indices in $P$. All variables either have the form `foo_i` or `bar`: no `blah_17`. Moreover, every variable identifier that appears with the index `i` never appears without an index and vice versa. \
4. There are no two lines in $P$ that assign a value to the same variable. \
5. $P$ has a variable `halted` which the only line that refers to it is the last line of the program which has the form `halted := loop NAND loop`. \
6. All assignments in $P$ to the `y` variables and `loop` are "guarded" by `halted` which means that any such assignment has the form that the value of `y_i` or `loop` is unchanged if `halted` equals $1$.

It might not be clear at this point why we care about the conditions of  [normalform](){.ref}, but we will see later in this course that they can help make certain proofs easier.
The following theorem shows that we can ensure these conditions at a small cost:

> # {.theorem title="NAND++ normal form" #nandnormalformthm}
For every NAND++ program $P$ there is a NAND++ program $P'$ of normal form that computes the same function as $P$. Moreover, the number of lines in $P'$ is at most $c$ times the number of lines in $P$, where $c \leq 10$ is some absolute constant. Furthermore, for every input $x$, the number of iterations that $P'$ takes on input $x$ is at most a constant additive number than the number of iterations that $P$ takes on the same input.

> # {.proof data-ref="nandnormalformthm"}
We only sketch the proof since it's not so insightful. We will go over the conditions one by one.
For 1 and 2 we discussed above how to add code to a NAND++ program that ensures these conditions, so we can focus on the remaining ones: \
3. We can replace a variable of the form `bar_17` with some unique number name such as `barseventeen`. We can add code to test if `i` is one of the constantly many indices that appeared as absolute numerical instances, and if so then replace variable such as `bar_i` with `barindexvalue`. \
4. If two lines $i<j$ assign a value to the same (indexed or unindexed) variable `foo`, then we can replace all occurrences of `foo` in lines $i,i+1,\ldots,j-1$ with `tempfoo` where `temp` is some unique prefix. \
5. We can ensure this by simply adding that line of code, and replacing any use of `halted` with `uphalted` where `up` stands for some unique prefix. \
6. This can be ensured by replacing each such assignment with a constant  number of lines ensuring this `if` condition. That is, we replace an assignment of the form `y_i := foo NAND bar` or `loop := foo NAND bar`  with the code `if NOT(halted) { y_i := foo NAND bar }` or `if NOT(halted) { loop := foo NAND bar }`, and then use the standard "de-sugaring" transformation to remove the syntactic sugar for `if`.

## NAND++ Programs as tuples

Just like we did with NAND programs, we can represent NAND++ programs as tuples.
A minor difference is that since in NAND++ it makes sense to keep track of indices, we will represent a  variable `foo_`$\expr{j}$ as a pair of numbers $(a,j)$ where $a$ corresponds to the identifier `foo`.
Thus we will use a 6-tuple of the form $(a,j,b,k,c,\ell)$ to represent each line of the form `foo_`$\expr{j}$ ` := ` `bar_`$\expr{k}$ ` NAND ` `baz_`$\expr{\ell}$, where $a,b,c$ correspond to the variable identifiers `foo`, `bar` and `baz` respectively.^[This difference between three tuples and six tuples is made for convenience and is not particularly important. We could have also  represented NAND programs using six-tuples and NAND++ using three-tuples.]
If one of the indices is the special variable `i` then we will use the number $s$ for it where $s$ is the number of lines (as no index is allowed to be this large in a NAND++ program).
We can now define NAND++ programs in a way analogous to [NANDprogram](){.ref}:

> # {.definition title="NAND++" #NANDpp}
A _NAND++ program_ is a 6-tuple $P=(V,x,y,validx,loop,L)$ of the following form:
>
* $V$ (called the _variable identifiers_) is some finite set.
>
* $x\in V$ is called the _input identifier_.
>
* $y\in V$ is called the _output identifier_.
>
* $validx \in V$ is the _input length identifier_.
>
* $loop \in V$ is the _loop variable_.
>
* $L \in (V\times [s+1] \times V \times [s+1] \times V \times [s+1])^*$ is a list of 6-tuples of the form $(a,j,b,k,c,\ell)$ where $a,b,c \in V$ and $j,k,\ell \in [s+1]$ for $s=|L|$.
That is, $L= ( (a_0,j_0,b_0,k_0,c_0,\ell_0),\ldots,(a_{s-1},j_{s-1},b_{s-1},k_{s-1},c_{k-1},\ell_{s-1}))$ where for every $t\in \{0,\ldots, s-1\}$, $a_t,b_t,c_t \in V$ and $j_t,k_t,\ell_t \in [s+1]$.
Moreover $a_t \not\in  \{x,validx\}$ for every $t\in [s]$ and $b_t,c_t \not\in \{ y,loop}$ for every $t \in [s]$.
>

> # { .pause }
This definition is long but ultimately translating a NAND++ program from code to tuples can be done in  a fairly straightforward way. Please read the definition again to see that you can follow this transformation.
Note that there is a difference between the way we represent NAND++ and NAND programs.
In NAND programs, we used a different element of $V$ to represent, for example, `x_17` and `x_35`.
For NAND++ we will represent these two variables by $(x,17)$ and $(x,35)$ respectively where $x$ is the input identifier.
For this reason, in our definition of NAND++, $x$ is a single element of $V$ as opposed to a tuple of elements as in [NANDprogram](){.ref}.
For the same reason, $y$ is a single element and not a tuple as well.

Just like for NAND, we can define a notion of _snapshots_ for NAND++.
Just like it is the case for NAND, we can also define a _canonical form_ for NAND++ programs.
This canonical form somewhat simplifies the definition of snapshots, and hence we will restrict attention to it.

> # {.definition title="Canonical NAND++ program" #NANDppcanonical}
A NAND++ program $P=(V,x,y,validx,loop,L)$ is in _canonical form_ if $V=[t]$ for some $t\in \N$, $x=0$,$y=1$, $validx=2$ and $loop=3$ and every element of $V$ appears in some tuple in $L$.





## Lecture summary

* NAND++ programs introduce the notion of _loops_, and allow us to capture a single algorithm that can evaluate functions of any length.
*

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
