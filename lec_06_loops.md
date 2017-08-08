# Loops and infinity

>_"We thus see that when $n=1$, nine operation-cards are used; that when $n=2$, fourteen Operation-cards are used; and that when $n>2$, twenty-five operation-cards are used; but that no more are needed, however great $n$ may be; and not only this, but that these same twenty-five cards suffice for the successive computation of all the numbers"_, Ada Augusta, countess of Lovelace, 1843^[Translation of  "Sketch of the Analytical Engine" by L. F. Menabrea, Note G.]

>_"It is found in practice that (Turing machines) can do anything that could be described as 'rule of thumb' or 'purely mechanical'... (Indeed,) it is  now agreed amongst logicians that 'calculable by means of (a Turing Machine)' is the correct accurate rendering of such phrases."_, Alan Turing, 1948

>_"All problems in computer science can be solved by another level of indirection"_,  attributed to David Wheeler.




The NAND programming language has one very significant drawback: a finite NAND program $P$ can only compute a finite function $F$, and in particular the number of inputs of $F$ is always smaller than the number of lines of $P$.
This does not capture our intuitive notion of an algorithm as a _single recipe_ to compute a potentially infinite function.
For example, the standard elementary school multiplication algorithm is a _single_ algorithm that multiplies numbers of all lengths, but yet we cannot express this algorithm as a single NAND program, but rather need a different NAND program for every input length.


Let us consider the case of the simple _parity_ function  $PARITY:\{0,1\}^* \rightarrow \{0,1\}$ such that $PARITY(x)$ equals $1$ iff the number of $1$'s in $x$ is odd cannot be computed by a NAND program. Rather, for every $n$, we can compute $PARITY_n$ (the restriction of $PARITY$ to $\{0,1\}^n$) using a different NAND program. For example, here is the NAND program to compute $PARITY_5$:

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
Typical programming language use the notion of _loops_ to express such an algorithm, and so we would rather write something like:

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


* We add a special _integer valued_ variable `i`, and allow expressions of the form `foo_i` (for every variable identifier `foo`) which are evaluated to equal `foo_`$\expr{i}$ where $\expr{i}$ denotes the current value of the variable `i`. As usual, `i` is initially assigned the value $0$.^[Note that the variable `i`, like all variables in NAND, is a _global_ variable, and hence  all expressions of the form `foo_i`, `bar_i` etc. refer to the same value of `i`.]

* We add a special variable `loop` with the following semantics: when the program ends, if `loop` is equal to one, then execution goes back to the first line and the variable `i` is either incremented or decremented by 1. In the first iteration of the loop, `i` is incremented, in the second iteration, it is decremented, then in the next two iterations `i` is incremented, and in the next two after that it is decremented, and so on. That is, the variable `i` takes the following sequence of values:

$$
0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots
$$


* Because the input to NAND++ programs can have variable length, we also add a special read-only array `validx` such that `validx_`$\expr{n}$ is equal to $1$ if and only if the $n$ is smaller than the length of the input.

* Like NAND programs, the output of a  NAND++ program is the string `y_`$0$, $\ldots$, `y_`$\expr{k}$  where $k$ is the largest integer such that `y_`$\expr{k}$ was assigned a value.

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

We say that a NAND program completed its _$r$-th round_ when the index variable `i` completed the sequence:

$$
0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots,0,1,\ldots,r,r-1,\ldots,0
$$

This happens when the program completed

$$
1+2+4+6+\cdots+2r =r^2 +r + 1
$$

iterations of its main loop. (The last equality is obtained by applying the formula for the sum of an algebraic progression.)
This means that if we keep a "program counter" $pc$ that is initially set to $0$ and increases by one at the end of any iteration, then  the "round" $r$ is the largest integer such that $r(r+1) \leq pc$, which equals $\floor{\sqrt{pc+1/4}-1/2}$.

Thus the value of `i` in the iteration with counter $pc$ equals:

$$
index(pc) = \begin{cases} pc- r(r+1) & pc \leq (r+1)^2 \\ (r+1)(r+2)-pc & \text{otherwise} \end{cases}
$$

where $r= \floor{\sqrt{pc+1/4}-1/2}$.
(We ask you to prove this in [computeidx-ex](){.ref}.)

### Remark: Inner loops via syntactic sugar

While  NAND+  only has a single "outer loop",  we can use conditionals to implement inner loops as well.
That is, we can replace code such as


~~~~ { .go .numberLines }
preloop_code
while (a) {
 loop_code
}
postloop_code
~~~~


by

~~~~ { .go .numberLines }
// finishedpreloop is initialized to 0
// finishedloop is initalized to 0
if NOT(finishedpreloop)  {
    code1
    finishedpreloop := 1
}
if NOT(finishedloop) {
    if (a) {
        code2
    }
    if NOT(a) {
        finishedloop := 1
    }
}
if (finishedloop) {
    postloop_code
}
~~~~

(Applying the standard syntactic sugar transformations to convert the conditionals into NAND code.)
We can apply this transformation repeatedly to convert programs with multiple loops, and even nested loops, into a standard NAND++  program.



## Uniformity and NAND vs NAND++

While NAND++ adds an extra operation over NAND, it is not exactly accurate to say that NAND++ programs are "more powerful" than NAND programs.
NAND programs, having no loops, are simply not applicable for computing functions with more inputs than they have lines.
The key difference between NAND and NAND++ is that NAND++ allows us to express the fact that the algorithm for computing parities of length-$100$ strings is really the same one as the algorithm for computing parities of length-$5$ strings (or similarly the fact that the algorithm for adding $n$-bit numbers is the same for every $n$, etc.).
That is, one can think of the NAND++ program for general parity as the "seed" out of which we can grow NAND programs for length $10$, length $100$, or length $1000$ parities as needed.
This notion of a single algorithm that can compute functions of all input lengths is known as _uniformity_ of computation and hence we think of NAND++ as  _uniform_ model of computation, as opposed to NAND which is a _nonuniform_ model, where we have to specify a different program for every input length.


Looking ahead, we will see that this uniformity leads to another crucial difference between NAND++ and NAND programs.
NAND++ programs can have inputs and outputs that are longer than the description of the program and in particular we can have a NAND++ program that "self replicates" in the sense that it can print its own code.   
This notion of "self replication", and the related notion of "self reference" is crucial to many aspects of computation, as well  of course to life itself, whether in the form of digital or biological programs.


__Advanced remark:__ This notion of a NAND++ program as a "seed" that can grow a different NAND program for every input length is one that we will come back to later on in this course, when we consider bounding the _time complexity_ of computation.
As we will see, we can think of a NAND++ program $P$ that computes some function $F$ in $T(n)$ steps on input length $n$, as a two phase process.
For any  input $x\in \{0,1\}^*$, the program $P$ can be thought of as first producing a $T(|x|)$-line NAND program $P'$, and then executing this program $P'$ on $x$.
This might not be easy to see at this point, but will become clearer in a few lectures when we tackle the issue of _efficiency_ in computation.


### Infinite loops and computing a function

There is another important difference between NAND and NAND++ programs: looking at a NAND program, we can always tell how many inputs and how many outputs it has (by looking at the number of `x_` and `y_` variables) and are guaranteed that if we invoke it on any input then _some_ output will be produced.  
In contrast, given any particular NAND++ program $P$, we cannot determine a priori the length of the output.
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






## The NAND<< programming language

Even the program to compute parities in NAND++ is somewhat tedious, and hence we will now define a seemingly more powerful programming language: NAND<<.
NAND<< has some  additional operators, but as we will see, it can ultimately be implemented by applying certain "syntactic sugar" constructs on top of NAND++.
Nonetheless, NAND<<  will still serve (especially later in the course) as a useful computational model.^[If you have encountered computability or computational complexity before, we can already "let you in on the secret". NAND++ is equivalent to the model known as _single tape oblivious Turing machines_, while NAND<< is (essentially) equivalent to the model known as _RAM machines_. For the purposes of the current lecture, these two models are indistinguishable (due to a notion known as "Turing completeness") but the difference between them can matter if one is interested in a fine enough resolution of computational efficiency.]
There are two key differences between NAND<< and NAND:

1. The NAND<< programming language works with _integer valued_ as opposed to _binary_ variables.

2. NAND<< allows _indirection_ in the sense of accessing the `bar`-th location of an array `foo`. Specifically, since we use _integer valued_ variables, we can assign the value of `bar` to the special index `i` and then use `foo_i`.  

We will allow the following operations on variables:^[Below `foo`, `bar` and `baz` are indexed or non-indexed variable identifiers (e.g., they can have the form `blah` or `blah_12` or `blah_i`), as usual, we identify an indexed identifier `blah` with `blah_0`. Except for the assignment, where `i` can be on the lefthand side, the special index variable `i` cannot be involved in these operations.]

* `foo := bar` or `i := bar` (assignment)
* `foo := bar  + baz` (addition)
* `foo := bar - baz` (subtraction)
* `foo := bar >> baz` (right shift: $idx \leftarrow \floor{foo 2^{-bar}}$)
* `foo := bar << baz` (left shift: $idx \leftarrow foo 2^{bar}$)
* `foo := bar % baz`  (modular reduction)
* `foo := bar * baz` (multiplication)
* `foo := bar / baz` (integer division: $idx \leftarrow \floor{\tfrac{foo}{bar}}$)
* `foo := bar bAND baz` (bitwise AND)
* `foo := bar bXOR baz` (bitwise XOR)
* `foo := bar > baz` (greater than)
* `foo := bar < baz` (smaller than)
* `foo := bar == baz` (equality)

The semantics of these operations are as expected except that we maintain the invariant that all  variables  always take values between $0$ and the current value of the program counter (i.e., number of iterations of the program that have been  completed).
If an operation would result in assigning to a variable `foo` a number that is smaller than $0$, then we assign $0$ to `foo`, and if it assigns to `foo` a number that is larger than the program counter, then we assign the value of the program counter to `foo`.
Just like C, we interpret any nonzero value as "true"  or $1$, and hence `foo := bar NAND baz` will assign to `foo` the value $0$ if both `bar` and `baz` are not zero, and $1$ otherwise.

Apart from those operations, NAND<< is identical to NAND++.
For consistency, we still treat the variable `i` as special, in the sense that we only allow it to be used as an index, even though the other variables contain integers as well, and so we don't allow variables such as `foo_bar` though we can simulate it by first writing `i := bar` and then `foo_i`.
We also maintain the invariant that at the beginning of each iteration, the value of `i` is set to the same value that it would have in a NAND++ program (i.e., the function of the program counter stated in [computeidx-ex](){.ref}), though this can be of course overwritten by explicitly assigning a value to `i`.
Once again, see the appendix for a more formal specification of NAND<<.

> # {.remark title="Computing on integers" #integers-rem}
Most of the time we will be interested in applying NAND<< programs on bits, and hence we will assume that both inputs and outputs are bits. We can enforce the  latter condition by not allowing `y_` variables to be on the lefthand side of any operation other than NAND.
However, the same model can be used to talk about functions that map tuples of integers to tuples of integers, and so we may very occasionally abuse notation and talk about NAND<< programs that compute on integers.

### Simulating NAND<< in NAND++


The most important fact we need to know about NAND<< is that it can be implemented by mere "syntactic sugar" and hence does not give us more computational power than NAND++, as stated in the following theorem:

> # {.theorem title="NAND++ and NAND<< are equivalent" #NANDequiv-thm}
For every (partial) function $F:\{0,1\}^* \rightarrow \{0,1\}^*$,
$F$ is computable by a NAND++ program if and only if $F$ is computable by a NAND<< program.


The rest of this section is devoted to outlining the proof of  [NANDequiv-thm](){.ref}.
The "only if" direction of the theorem  is immediate.
After all, every NAND++ program $P$ is in particular also a NAND<< program, and hence if $F$ is computable by a NAND++ program then it is also computable by a NAND<< program.
To show the "if" direction, we need to show how we can implement all the operations of NAND<< in NAND++.

Note that it's quite easy to store integers as bit-arrays, and so we can also simulate an array of integers using a two-dimensional array of bits(which we have seen how to embed in a the standard single-dimensional arrays supplied by NAND++).
That is, if in NAND<< the variable `foo_`$\expr{i}$ corresponded to an integer, then we can simulate this in NAND++ by having  `foo_`$PAIR(i,j)$ correspond to the $j$-th bit in the representation of  the integer `foo_`$\expr{i}$ where $PAIR:\N^2 \rightarrow \N$ is some easily computable one-to-one embedding of $\N^2$ in $\N$.

We can in principle use the standard algorithms for addition, multiplication, division, etc.. to perform the arithmetic operations on these arrays.
The key difficulty is in actually controlling the index variable `i`, which in NAND++ moves obliviously according to the set schedule $0,1,0,1,2,1,0,1,2,3,2,1,0,\ldots$.
To achieve control of `i` we use the well known observation that a bus is just like a taxi if you are willing to wait long enough.
That is, instead of moving `i` to where we want, we wait until it eventually gets there on its own.

One useful observation is that in  a NAND++ program we can know whether the index is increasing or decreasing using the Hansel and Gretel technique of "breadcrumbs".
We create an array `atstart` such that `atstart_0` equals $1$ but `atstart_`$\expr{j}$ equals $0$ for all $j>0$, and an array `breadcrumb` where we set `breadcrumb_i` to $1$ in every iteration.
Then we can setup a variable `indexincreasing` and set it to $1$ when we reach the zero index (i.e., when `atstart_i` is equal to $1$) and set it to $0$ when we reach the end point (i.e., when we see an index for which `breadcrumb_i` is $0$ and hence we have reached it for the first time).
We can also maintain an array `arridx` that contains $0$ in all positions except the current value of `i`.
Now we can simulate incrementing and decrementing `i` by one as follows.
If we want to increment `i` and `indexincreasing` then we simply wait one step.
Otherwise (if `indexincreasing` is $0$) then we enter into a special state in which we do nothing until we reach again the point when `arridx_i` is $1$ and  `indexincreasing` is equal to $1$.
Decrementing `i` is done in the analogous way.

Once we can increment and decrement `i`, we can use this, together with the notion of inner loops, to perform all the operations needed on the representations of integers as bits.
We can also simulate an  operation such as `i := foo` by creating a temporary array that contains $0$ except for a single $1$ in the location corresponding to the integer represented by `foo` and waiting until we reach the point where `foo_i` equals $1$.

We omit the full details of the proofs.
However, the webpage [nandpl.org](http://nandpl.org) contains  an OCaml program that transform a NAND<< program into an equivalent NAND++ program.

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


## Example

Here is a program that computes the function $PALINDROME:\{0,1\}^* \rightarrow \{0,1\}$ that outputs $1$ on $x$ if and only if $x_i = x_{|x|-i}$ for every $i\in \{0,\ldots, |x|-1\}$.
This program uses NAND<< with the syntactic sugar we described before, but as discussed above, we can transform it into a NAND++ program.

~~~~ { .go }
// A sample NAND<< program that computes the language of palindromes
// By Juan Esteller
def a := NOT(b) {
  a := b NAND b
}
o := NOT(z)
two := o + o
if(NOT(seen_0)) {
  cur := z
  seen_0 := o
}
i := cur
if(validx_i) {
 cur := cur + o  
 loop := o
}
if(NOT(validx_i)) {
  computedlength := o
}
if(computedlength) {
  if(justentered) {
    justentered := o
    iter := z
  }
  i := iter
  left := x_i
  i := (cur - iter) - o
  right := x_i
  if(NOT(left == right)) {   
    loop := z
    y_0 := z
  }
  halflength := cur / two
  if(NOT(iter < halflength)) {
   y_0 := o
   loop := z
  }  
  iter := iter + o  
}

~~~~






## Universality: A NAND++ interpreter in NAND++

Like a NAND program, a NAND++ or a NAND<< program is ultimately a sequence of symbols and hence can obviously be represented as a binary string.
We will spell out the exact details of representation later, but as usual, the details are not so important (e.g., we can use the ASCII encoding of the source code).
What is crucial is that we can use such representation to evaluate any program.
That is, we prove the following theorem:


> # {.theorem title="Universality of NAND++" #univ-nandpp}
There is a NAND++ program that computes the partial function $EVAL:\{0,1\}^* \rightarrow \{0,1\}^*$ defined as follows:
$$
EVAL(P,x)=P(x)
$$
for strings $P,x$ such that $P$ is a valid representation of a NAND++ program which produces an output on $x$.


This is a stronger notion than the universality we proved for NAND, in the sense that we show a _single_ universal  NAND++ program $U$ that can evaluate _all_ NAND programs, including those that have more lines than the lines in $U$.
In particular, $U$ can even be used to evaluate itself!
This notion of _self reference_ will appear time and again in this course, and as we will see, leads to several counterintuitive phenomena in computing.  

Because we can easily transform a NAND<< program into a NAND++ program, this means that even the seemingly "weaker" NAND++ programming language is powerful enough to simulate NAND<< programs.
Indeed, as we already alluded to before, NAND++ is powerful enough to simulate also all other standard programming languages such as  Python, C, Lisp, etc..

### Representing NAND++ programs as string

Before we prove  [univ-nandpp](){.ref} formal, we need to make its statement precise by specifying a representation scheme for NAND++ programs.
As mentioned above,  simply representing the program as a string using ASCII or UTF-8 encoding  will work just fine, but we will use a somewhat more convenient and concrete representation, which is the natural generalization of the "list of tuples" representation for NAND programs.
We will assume that all variables are of the form `foo_##` where `##` is some number or the index `i`.  If a variable `foo` does not have an index then we add the index zero to it.
We represent an instruction of the form

`foo_`$\expr{j}$ `:= bar_`$\expr{k}$  ` NAND baz_`$\expr{\ell}$

as a $6$ tuple $(a,j,b,k,c,\ell)$ where $a,b,c$ are numbers corresponding to the labels `foo`,`bar`,and `baz` respectively, and $j,k,\ell$ are the corresponding indices.
We let $L$ be the number of lines in the program, and set the index to be  $L+1$ if instead of a number the variable is indexed by   the special  variable `i`.
(There is no risk of conflict since we did not allow numerical indices larger than the number of lines in the program.)
We will set the identifiers of `x`,`y`,`validx` and `loop` to $0,1,2,3$ respectively.
Therefore the representation of the parity program

~~~~ { .go .numberLines }
tmp_1 := seen_i NAND seen_i
tmp_2 := x_i NAND tmp_1
val := tmp_2 NAND tmp_2
ns := s NAND s
y_0 := ns NAND ns
u := val NAND s
v := s NAND u
w := val NAND u
s := v NAND w
seen_i := z NAND z
stop := validx_i NAND validx_i
loop := stop NAND stop
~~~~

will be

```
[[4, 1, 5, 61, 5, 61],
 [4, 2, 0, 61, 4, 1],
 [6, 0, 4, 2, 4, 2],
 [7, 0, 8, 0, 8, 0],
 [1, 0, 7, 0, 7, 0],
 [9, 0, 6, 0, 8, 0],
 [10, 0, 8, 0, 9, 0],
 [11, 0, 6, 0, 9, 0],
 [8, 0, 10, 0, 11, 0],
 [5, 61, 12, 0, 12, 0],
 [13, 0, 2, 61, 2, 61],
 [3, 0, 13, 0, 13, 0]]
```

__Binary encoding:__ The above is a way to represent any NAND++ program as a list of numbers. We can of course encode such a list as a binary string in a number of ways. For concreteness, since all the numbers involved are between $0$ and $L+1$ (where $L$ is the number of lines),  we can simply use a string of length $6\ceil{\log (L+1)}$ to represent them, starting with the prefix $0^{L+1}1$ to encode $L$. For convenience we will assume that any string that is not formatted in this way encodes the single line program `y_0 := x_0 NAND x_0`. This way we can assume that every string $P\in\bits^*$ represents _some_ program.


### A NAND++ interpreter in NAND<<

Here is the "pseudocode"/"sugar added" version of an  interpreter for NAND++ programs (given in the list of 6 tuples representation) in NAND<<.
We assume below that the input is given as integers `x_0`,\ldots,`x_`$\expr{6\cdot lines-1}$ where $lines$ is the number of lines in the program.
We also assume that `NumberVariables` gives some upper bound on the total number of distinct non-indexed identifiers used in the program (we can also simply use $lines$ as this bound).

~~~~ { .go .numberLines }
simloop := 3
totalvars := NumberVariables(x)
maxlines  := Length(x) / 6
currenti := 0
currentround := 0
increasing := 1
pc := 0
while (true) {
    line := 0
    foo    :=  x_{6*line + 0}
    fooidx :=  x_{6*line + 1}
    bar    :=  x_{6*line + 2}
    baridx :=  x_{6*line + 3}
    baz    :=  x_{6*line + 4}
    bazidx :=  x_{6*line + 5}
    if (fooidx == maxlines) {
        fooidx := currenti
    }
    ... // similar for baridx, bazidx

    vars_{totalvars*fooidx+foo} := vars_{totalvars*baridx+bar} NAND vars_{totalvars*bazidx+baz}
    line++

    if line==maxlines {
        if not avars[simloop] {
            break
        }
        pc := pc+1
        if (increasing) {
            i := i + 1
        } else
        {
            i := i - 1
        }
        if i>r {
            increasing := 0
            r := r+1
        }
        if i==0 {
            increasing := 1
        }

    }
    // keep track in loop above of largest m that y_{m-1} was assigned a value
    // add code to move vars[0*totalvars+1]...vars[(m-1)*totalvars+1] to y_0..y_{m-1}
}
~~~~

Since we can transform _every_ NAND<< program to a NAND++ one, we can also implement this interpreter in NAND++.



### A  Python interpreter in NAND++

At this point you probably can guess that it is possible to write an interpreter for  languages such as  C or Python in NAND<< and hence in NAND++ as well.
After all, with NAND++ / NAND<< we have access to an unbounded array of memory, which we can use to simulate memory allocation and access, and can do all the basic computation steps offered by modern CPUs.
Writing such an interpreter is nobody's idea of a fun afternoon, but the fact it can be done gives credence to the belief that NAND++ _is_ a good model for general-purpose computing.



## Lecture summary

* NAND++ programs introduce the notion of _loops_, and allow us to capture a single algorithm that can evaluate functions of any length.
* NAND<< programs include more operations, including the ability to use indirection to obtain random access to memory, but they are computationally equivalent to NAND++ program.
* We can translate many (all?)  standard algorithms into NAND<< and hence NAND++ programs.
* There is a _universal_ NAND++ program $U$ such that on input a description of a NAND++ program $P$ and some input $x$,  $U(P,x)$ halts and  outputs $P(x)$ if (and only if) $P$ halts on input $x$.

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
