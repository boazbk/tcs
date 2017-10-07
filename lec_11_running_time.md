#  Modeling running time

>"When the measure of the problem-size is reasonable and when the sizes assume values arbitrarily large, an asymptotic estimate of ... the order of difficulty of [an] algorithm .. is theoretically important. It cannot be rigged by making the algorithm artificially difficult for smaller sizes", Jack Edmonds, "Paths, Trees, and Flowers", 1963

>"The computational complexity of a sequence is to be measured by how fast a multitape Turing machine can print out the terms of the sequence. This particular abstract model of a computing device is chosen because much of the work in this area is stimulated by the rapidly growing importance of computation through the use of digital computers, and all digital computers in a slightly idealized form
belong to the class of multitape Turing machines.", Juris Hartmanis and Richard Stearns, "On the computational complexity of algorithms", 1963.




In the last lecture we saw examples of efficient algorithms, and made some claims about their running time, but did not give a mathematically precise definition for this concept.
We do so in this lecture, using our NAND++ and NAND<< models we have seen before.
Since we think of functions that can take as input a string of arbitrary length, we need to measure this number as a function of the length of the input.
For example, if a function $F$ can be computed by a NAND<< (or NAND++) program that on inputs of length $n$ takes $O(n)$ steps then we will think of $F$ as "efficiently computable",  while if any such program  requires $2^{\Omega(n)}$ steps to compute $F$ then we consider $F$ "intractable".

Since running time depends on the length of the input, the formal definition of running time of a function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ is not a _number_ but rather a _function_ $T:\N \rightarrow \N$ such that $T(n)$ is the maximum number of steps that the fastest algorithm to compute $F$ requires on length $n$ inputs.
Formally, the definition is as follows:


> # {.definition title="Running time" #time-def}
Let $T:\N \rightarrow \N$.
We say that a  function $F:\{0,1\}^* \rightarrow \{0,1\}$ is _computable in $T(n)$ NAND<< time_
if there is a NAND<< program $P$ such that for every $x\in \{0,1\}^*$, on input $x$, $P$ runs for at most $T(|x|)$ steps and outputs $F(x)$.
Similarly, we say that $F$ is _computable in $T(n)$ NAND++ time_ if there is a NAND++ program that computes it on $x$ in at most $T(|x|)$ steps.
>
We  $TIME_{<<}(T(n))$ denote the set of Boolean functions that are computable in $T(n)$ NAND<< time, and define  $TIME_{++}(T(n))$.

[time-def](){.ref} above naturally extend to non Boolean and to partial functions as well, and so we will talk about the time complexity of these functions.

__Which model to choose?__ Unlike the notion of computability, the exact running time can be a function of the model we use. However, it turns out that if we care about "coarse enough" resolution (as we will in this course) then the choice of the model,  whether it is NAND<<, NAND++, or Turing or RAM machines of various flavors,  does not matter. (This is known as the _extended_ Church-Turing Thesis). Nevertheless, to be concrete, we will use NAND<< programs as our "default" computational model for measuring time, and so if we say that $F$ is computable in $T(n)$ time without any qualifications, or write $TIME(T(n))$ without any subscript, we mean that this holds with respect to NAND<< machines.


__Nice time bounds.__ When considering time bounds, we want to restrict attention to "nice" bounds such as $O(n)$, $O(n\log n)$, $O(n^2)$, $O(2^{\sqrt{n}})$, $O(2^n)$, etc. and avoid pathological examples such as non-monotone functions (where the time to compute a function on inputs of size $n$ could be smaller than the time to compute it on inputs of size $n'<n$) or other degenerate cases.
Thus we make the following definition:

> # {.definition title="Nice functions" #nice-def}
A function $T:\N \rightarrow \N$ is a _nice time bound function_ (or nice function for short) if: \
* $T(n) \geq n$ \
* $T(n) \geq T(n')$ whenever $n \geq n'$ \
* The function $F_T:\{0,1\}^* \rightarrow \{0,1\}^*$ such that $F_T(x)$ is the binary representation of $T(|x|)$ is in $\overline{TIME}(T(n))$.

All the functions mentioned above are "nice" per [nice-def](){.ref}, and from now on we will only care about the class $TIME(T(n))$ or $\overline{TIME}(T(n))$  when $T$ is a "nice" function.


The two main time complexity classes we will be interested in are the following:

* __Polynomial time:__ We say that a total Boolean function is _computable in polynomial time_ if it is in the class $\mathbf{P} = \cup_{c\in\N} TIME(n^c)$.

* __Exponential time:__ We say that a Boolean total function is computable in exponential time if it is in the class $\mathbf{EXP} = \cup_{c\in\N} TIME(2^{n^c})$.

Since exponential time is much larger than polynomial time, clearly $\mathbf{P}\subseteq \mathbf{EXP}$.
All of the problems we listed in the last lecture are in $\mathbf{EXP}$,^[Strictly speaking, many of these problems correspond to _non Boolean_ functions, but we will sometimes "abuse notation" and refer to non Boolean functions as belonging to $\mathbf{P}$ or $\mathbe{EXP}$. We can easily extend the definitions of these classes to non Boolean and partial functions. Also, for every non-Boolean function $F$, we can define a Boolean variant $\Hat{F}$ such that $F$ can be computed in polynomial time if and only if  $\Hat{F}$ is.] but as we've seen, for some of them there are much better algorithms that demonstrate that they are in fact in $\mathbf{P}$.


| $\mathbf{P}$  | $\mathbf{EXP}$ |
|--------------------------|---------------------------|
| Shortest path            | Longest Path              |
| Min cut                  | Max cut                   |
| 2SAT                     | 3SAT                      |
| Linear eqs               | Quad. eqs                 |
| Zerosum                  | Nash                      |
| Determinant              | Permanent                 |
| Primality                | Factoring                 |

A table of the  examples from the previous lecture.
All these problems are in $\mathbf{EXP}$ but the only the ones on the left column are currently known to be in $\mathbf{P}$ (i.e., have a polynomial-time algorithm).


## NAND<< vs NAND++

We have seen that for every NAND<< program $P$ there is a NAND++ program $P'$ that computes the same function as $P$.
It turns out that the $P'$ is not much slower than $P$.
That is, we can prove the following theorem:

> # {.theorem title="Efficient simulation of NAND<< with NAND++" #NANDpp-thm}
There are absolute constants $a,b$ such that for every  function $F$ and nice  function  $T:\N \rightarrow \N$,  if $F \in TIME_{<<}(T(n))$ then there is a NAND++ program $P'$ that computes $F$ in $T'(n)=a\cdot T(n)^b$.
That is, $TIME_{<<}(T(n)) \subseteq TIME_{++}(aT(n)^b)$


(The constant $b$ can be easily shown to be at most five, and with more effort can be optimized further.)

> # {.proof data-ref="NANDpp-thm"}
The idea is to follow the proof of [NANDequiv-thm](){.ref} (simulation of NAND<< programs using NAND++ programs) and use the exact same simulation, but with a more careful accounting of the number of steps that the simulation costs.
Recall, that the simulation of NAND<< works by "peeling off" features of NAND<< one by one, until we are left with NAND++.
We now sketch the main observations we use to show that this "peeling off" costs at most a polynomial overhead:
>
1. If $P$ is a NAND<< program that computes $F$ in $T(n)$ time, then on inputs of length $n$, all integers used by $P$ are of magnitude at most $T(n)$. This means that the largest value `i` can ever reach is at most $T(n)$ and so each one of $P$'s variables can be thought of as an array of at most $T(n)$ indices, each of which holds a  natural number of magnitude at most $T(n)$ (and hence one that can be encoded using $O(\log T(n))$ bits). Such an array can be encoded by a bit array of length $O(T(n)\log T(n))$. \
2. All the arithmetic operations on integers use the gradeschool algorithms, that take time that is polynomial in the number of bits of the integers, which is  $poly(\log T(n))$ in our case. \
3. Using the `i++` and `i--` operations we can load an integer (represented in binary) from the variable `foo` into the index `i` using a cost of $O(T(n)^2)$. The idea is that we create an array `marker` that contains a single $1$ coordinate and all the rest are zeroes. We will repeat the following for at most $T(n)$ steps: at each step we decrease `foo` by one (at a cost of $O(\log T(n))$) and move the $1$ in `marker` one step to the right (at a cost of $O(T(n))$). We stop when `foo` reaches $0$, at which point `marker` has $1$ in the location  encoded by the number that was in `foo`, and so if we move `i` until `marker_i` equals to $1$ then we reach our desired location. \
4. Once that is done, all that is left is to simulate `i++` and `i--` in NAND++ using our "breadcrumbs" and "wait for the bus"  technique. To simulate $T$ steps of increasing and decreasing the index, we will need at most $O(T^2)$ steps of NAND++  (see [obliviousfig](){.ref}). In the worst case for every increasing or decreasing step we will need to wait a full round until `i` reaches $0$ and gets back to the same location, in which case the total cost will be $O(1+2+3+4+\cdots+T)=O(T^2)$ steps. \
>
Together these observations imply that the simulation of $T$ steps of NAND<< can be done in $poly(T)$ step. (In fact the cost is  $O(T^4 polylog(T))= O(T^5)$ steps, and can even be improved further though this does not matter much.)




![The path an index variable takes in a NAND++ program](../figure/oblivious_simulation.png){#obliviousfig .class width=300px height=300px}




[NANDpp-thm](){.ref} means that we could have defined
$\mathbf{EXP}$ and $\mathbf{P}$ equally well using NAND++ instead of NAND<<, as these are the same up to polynomial factors.
More generally, the equivalence between NAND++ and NAND<< (as well as other models, such as Turing machines) allows us to pick our favorite one depending on the task at hand.
When we want to design an algorithm, we can use the extra power and convenience afforded by NAND<<.
When we want to _analyze_ a program, we can describe it in the simpler form of NAND++.




## Efficient universal machine: a NAND<< interpreter in NAND<<

We have seen before the NAND<< or "interpreter" for NAND++.
Examining this program, we can see that it has polynomial (in fact linear) overhead, and hence, combining this with [NANDpp-thm](){.ref} , we get that we have a universal NAND<< program with polynomial overhead.
But in fact, by directly simulating NAND<< programs, we can do better with only polylogarithmic overhead:


> # {.theorem title="Efficient universality of NAND<<" #univ-nandpp}
There is  an $O(n \log n)$-step NAND<< program that computes the  partial function $TIMEDEVAL:\{0,1\}^* \rightarrow \{0,1\}^*$ defined as follows:
$$
TIMEDEVAL(P,x,1^T)=P(x)
$$
if $P$  is a valid representation of a NAND<< program which produces an output on $x$ within at most $T$ steps.

> # {.proof data-ref="univ-nandpp"}
Once again we only sketch the proof. The definition of executing a NAND<< program is given in Appendix A.
It involves maintaining variables `ic`  and `i` for the iteration  counter and index variable, as well as an index for the current line that is being executed. If a program involves $L$ different variable identifiers, we can store all the variables in a single array `vars` such that if `foo` is the $\ell$-th identifier then the value of `foo_`$\expr{j}$ will be stored in `vars_`$\expr{Lj+\ell}$.
Evaluating every line can be done in  about  $O(L)$ operators which is a constant independent of the input length.





## Time hierarchy theorem

We have seen that there are uncomputable functions, but are there functions that  can be computed, but only at an exorbitant cost? For example, is there a function that _can_ be computed in time $2^n$, but _can not_ be computed in time $2^{0.9 n}$?
It turns out that the answer is __Yes__:

> # {.theorem title="Time Hierarchy Theorem" #time-hierarchy-thm}
For every nice function $T$, there is a function $F:\{0,1\}^* \rightarrow \{0,1\}$
in $TIME(T(n)\log^2 n) \setminus TIME(T(n))$.

> # {.proof data-ref="time-hierarchy-thm"}
Recall the Halting function $HALT:\{0,1\}^* \rightarrow \{0,1\}$ that was defined as follows:
$HALT(P,x)$ equals $1$ for every program $P$ and input $x$ s.t.  $P$ halts on input $x$, and is equal to $0$ otherwise.
We cannot use the  Halting function  of course, as it is uncomputable and hence  not in $TIME(T'(n))$ for any function $T'$. However, we will use the following variant of it:
>
We define the _Bounded Halting_ function $HALT_T(P)$ to equal $1$ for every program $P$  s.t. $P$ halts when given _its own string representation_ as input within $100 T(|P|)$ steps.
>
On one hand, using the universal NAND++ program, we can evaluate $HALT_T(P)$ in $O(T(|P|)\log T(|P|))$ steps.
On the other hand, we claim that $HALT_T \not\in TIME(T(n))$.
The proof is very reminiscent of the proof that $HALT$ is not computable.
Assume, toward the sake of contradiction, that there is some program $P^*$ that computes $HALT_T(P)$ within $T(|P|)$ steps.
Then, define $Q$ to be the program that on input a program $P$ does the following: \
1. Computes $b= P^*(Q)=HALT_T(Q)$ (at a cost of at most $T(|P|)$ steps, under our assumptions). \
2. If $b=1$ then it goes into an infinite loop, otherwise it halts.
>
We reach a contradiction by splitting into cases according to whether or not $Q$ halts when given itself as input within $2T(|Q|)$ steps.
On the one hand, if $Q$ does halt, then $HALT_T(Q)=1$, and hence under our assumption that $P^*$ computes $HALT_T$ then $Q$ will not halt.
On the other hand, if $Q$ does not halt, then $HALT_T(Q)=0$, and hence under our assumption that $P^*$ computes  $HALT_T(Q)$ in $T(|Q|)$ steps, then $Q$ will halt within $2T(|Q|)$ steps.
In either case we get a contradiction.



The time hierarchy theorem tells us that there are functions we can compute in $O(n^2)$ time but not $O(n)$, in $2^n$ time, but not $2^{\sqrt{n}}$, etc..
In particular there are most definitely functions that we can compute in time $2^n$ but not $O(n)$.
We have seen that we have no shortage of natural functions for which the best _known_ algorithm requires roughly $2^n$ time, and that many people have invested significant effort in trying to improve that.
However,  unlike in the finite vs. infinite case, for all of the examples above at the moment we do not know how to rule out even an $O(n)$ time algorithm.
We will however see that there is a single unproven conjecture that would imply such a result for most of these problems.

![Some complexity classes and some of the functions we know (or conjecture) to be contained in them.](../figure/time_complexity_map.png){#figureid .class width=300px height=300px}


### Note: Oh-tilde or a "Baker's Oh"

The choice of what to take as "elementary operations" can sometimes make a difference as to the asymptotic running time.
For example, the set of arithmetic operations we allowed in NAND<< was inherited from C and is somewhat arbitrary.
What if we wanted to add another operation?
A "reasonable" operation on integers of size at most $T$ can be computed in a number of steps that is polynomial in their representation which is $\log T$ bits.
Fortunately, as $T$ grows, $\log T$, and even polynomial factors in it, is extremely tiny compared to it, and hence we can think of such logarithmic terms as negligible and ignore them, at least in the context of this course.
Hence, just as we drop constant terms with the Big-Oh notation, it  often makes sense to ignore polylogarithmic terms as well.

> # {.definition title="Oh Tilde" #ohtilde}
Let $f,g:\N \rightarrow \N$, we say that $f =\tilde{O}(g)$ if there are some constant $a,b,N_0>0$ such that for every $n>N_0$, $f(n) \leq a g(n)(\log g(n))^b$.
We say that $f = \tilde{\Omega}(g)$ if $g=\tilde{O}(f)$.

We will often use the $\tilde{O}$ notation to suppress the differences between the NAND++ model and other, somewhat more permissive, models.
Assuming you don't mind a little cheating, when you see an $\tilde{O}(\cdot)$, you won't suffer much in understanding if you pretend that it is the same as the "regular" $O(\cdot)$.
Indeed, in most settings in this course we won't even care so much about the difference between $O(n)$ and $O(n^3)$, let alone the difference between $O(n)$ and $O(n\log n)$.

Needless to say, when one is implementing actual algorithms on actual machines, constant and logarithmic factors could make all the difference in the world, and having a model that is faithful to the actual architecture we execute it on can be very important.
However, at the coarse resolution we are mostly interested here, the differences between these models will not be so important.




## Simulating NAND<< or NAND++ programs with NAND programs

We have seen two measures of "computation cost" for functions.
For a finite function $G:\{0,1\}^n \rightarrow \{0,1\}^m$,  we said that $G\in SIZE(T)$ if there is a $T$-line NAND program that computes $G$.
We saw that _every_ function mapping $\{0,1\}^n$ to $\{0,1\}^m$ can be computed using at most $O(m2^n)$ lines.
For infinite functions $F:\{0,1\}^* \rightarrow \{0,1\}^*$, we can define the "complexity" by the smallest $T$ such that $F \in TIME(T(n))$.
Is there a relation between the two?

For simplicity, let  us restrict attention to  functions $F:\{0,1\}^* \rightarrow \{0,1\}$.
For every such function, define $F_n : \{0,1\}^n \rightarrow \{0,1\}$ to be the restriction of $F$ to inputs of size $n$.
It turns out that we do have at least one relation between the NAND++ complexity of $F$ and the NAND complexity of the functions $\{ F_n \}$.

> # {.theorem  title="Nonuniform computation contains uniform computation" #non-uniform}
There is some $c\in \N$ s.t. for every $F:\{0,1\}^* \rightarrow \{0,1\}$ in  $\overline{TIME_{++}}(T(n))$ and every $n\in N$,  $F_n$ is in $SIZE(10\cdot T(n))$.

> # {.proof data-ref="non-uniform"}
The proof follows by the "unraveling" argument that we've already seen in the proof of Godel's Theorem.
Given a NAND++ program $P$ and some function $T(n)$, we can construct a NAND program on $n$ inputs and with less than $10T(n)$ lines by simply putting "unraveling the main loop" of $P$ and hance putting $T(n)/L$  copies of $P$ one after the other, where $L$ is the number of lines in $P$, replacing any instance of `i` with the numerical value of `i` for that iteration.
The only thing left is to check for the case that the `loop` value is assigned a value. We do this by adding special variable `noop` which is initialized to $0$. If `loop` is ever equal to $0$ at the end of an iteration, then we assign $1$ to `noop`.
Also, we replace any assignment of a value to `y_`$\expr{j}$ with a conditional statement that only applies it  if `noop` equals $1$.


__Algorithmic version: the "NAND++ to NAND compliler":__
The transformation of the NAND++ program $P$ to the NAND program $Q_P$ is itself algorithmic.
Thus we can also phrase this result as follows:


> # {.theorem title="NAND++ to NAND compiler" #nand-compiler}
There is an $\tilde{O}(n)$-time NAND++ program $COMPILE$ such that on input a NAND++ program $P$,  and strings of the form $1^n,1^m,1^T$  outputs a NAND program $Q_P$ of at most $O(T \log T)$ lines with $n$ bits of inputs and $m$ bits of output, such that: For every $x\in\bits^n$, if $P$ halts on input $x$ within fewer than $T$ steps and outputs some string $y\in\bits^m$, then $Q_P(x)=y$.  

Since NAND<< programs can be simulated by NAND++ programs with polynomial overhead, we see that we can simulate a $T(n)$ time NAND<< program on length $n$ inputs with a $poly(T(n))$ size NAND program.




## Simulating NAND with NAND++?

We have seen that every function in $\overline{TIME}(T(n))$ is in $SIZE(poly(T(n)))$.
One can ask if  there is an inverse relation.
Suppose that $F$ is such that $F_n$ has a "short" NAND program for every $n$.
Can we say that it must be in $\overline{TIME}(T(n))$ for some "small" $T$?

The answer is __no__.
Indeed, consider the following "unary halting function" $UH:\{0,1\}^* \rightarrow \{0,1\}$ defined as follows: $UH(x)=1$ if and the binary representation of $|x|$ corresponds to a program $P$ such that $P$ halts on input $P$.
$UH$ is uncomputable, since otherwise we could compute the halting function by transforming the input program $P$ into the integer $n$ whose representation is the string $P$, and then running $UH(1^n)$ (i.e., $UH$ on the string of $n$ ones).
On the other hand, for every $n$, $UH_n(x)$ is either equal to $0$ for all inputs $x$ or equal to $1$ on all inputs $x$, and hence can be computed by a NAND program of a _constant_ number of lines.

The issue here is _uniformity_. For a function $F:\{0,1\}^* \rightarrow \{0,1\}$, if $F$ is in $TIME(T(n))$ then we have a _single_ algorithm that can compute $F_n$ for every $n$.
On the other hand,  $F_n$ might be in  $SIZE(T(n))$ for every $n$ using a completely different algorithm for every input length.
While this can be a real issue, in most natural settings the difference between uniformity and non-uniformity does not seem to arise.
In particular, in all the example problems in this lecture, as the input size $n$ grows, we do not know of NAND programs that are significantly smaller than what would be implied by the best known algorithm (i.e., NAND++ program).
Thus, if you pretend that $TIME(T(n))$  (or $\overline{TIME}(T(n))$) is roughly the same as $SIZE(T(n))$, you will be right more often than wrong.


### Uniform vs. Nonuniform computation: A recap

To summarize, the two models of computation we have described so far are:

* NAND programs, which have no loops, can only compute finite functions, and the time to execute them is exactly the number of lines they contain. These are also known as _straightline programs_ or _Boolean circuits_.

* NAND++ programs, which include loops, and hence a single program can compute a function with unbounded input length. These are equivalent (up to polynomial factors) to _Turing Machines_ or (up to polylogarithmic factors) to _RAM machines_.

For a function $F:\{0,1\}^* \rightarrow \{0,1\}$ and some nice time bound $T:\N \rightarrow \N$, we know that:

* If $F$ is computable in time $T(n)$ then there is a sequence $\{ P_n \}$ of NAND programs with $|P_n| = \tilde{O}(T(n))$ such that $P_n$ computes $F_n$ (i.e., restriction of $F$ to $\{0,1\}^n$) for every $n$.

* The reverse direction is not necessarily true - there are examples of functions $F:\{0,1\}^n \rightarrow \{0,1\}$ such that $F_n$ can be computed by even a constant size NAND program but $F$ is uncomputable.

Note that the $EVAL$ function, that takes as input a NAND program $P$ and an input $x$, and outputs $P(x)$, can be computed by a NAND++ program in $\tilde{O}(|P|)$ time.
Hence if $F$ has the property that it is computable by a sequence $\{ P_n \}$ of programs of $T(n)$ size, then there is a in fact an $\tilde{O}(T(n))$ time NAND++ program $P^*$ that can can compute $F$ if it is only given for every $n$ the  program $P_n$ as "advice".
For this reason, nonuniform computation is sometimes known as _computation with advice_.
The class $SIZE(poly(n))$ is sometimes denoted as $\mathbf{P}_{/poly}$, where the $/poly$ stands for giving the polynomial time algorithm a polynomial amount of "advice" - some string of information that depends only on the input length but not on the particular input.

## Extended Church-Turing Thesis

We have mentioned the Church-Turing thesis, that posits that the definition of computable functions using NAND++ programs captures the definition that would be obtained by all physically realizable computing devices.
The _extended_ Church Turing is the statement that the same holds for _efficiently computable_ functions, which is typically interpreted as saying that NAND++ programs can simulate  every physically realizable computing device with polynomial overhead.
Like the Church-Turing thesis itself, the extended Church-Turing thesis is in the asymptotic setting and does not directly yield an experimentally testable prediction.
However, it can be instantiated with more concrete bounds on the overhead, which would yield predictions such as the Physical Extended Church-Turing Thesis   we mentioned before, that are experimentally testable.
As we mentioned, quantum computing poses a serious challenge to the extended Church-Turing thesis.
However, it still seems that the extended Church-Turing thesis is fundamentally correct, in the sense that, while we do need to adapt it to account for the possibility of quantum computing, its broad outline remains unchanged.
In particular, out of all the example problems mentioned in the previous lecture, as far as we know, the complexity of only one--- integer factoring--- is affected by modifying our model to include quantum computers as well.

## Lecture summary

* We can define the time complexity of a function  using NAND++ programs, and similarly to the notion of computability, this appears to capture the inherent complexity of the function.

* There are many natural problems that have polynomial-time  algorithms, and other natural problems that we'd love to solve, but for which the best known algorithms are exponential.

* The time hierarchy theorem shows that there are _some_ problems that can be solved in exponential, but not in polynomial time. However, we do not know if that is the case for the natural examples that we described in this lecture.


## Exercises


> # {.exercise title="Composition of polynomial time" #poly-time-comp-ex}
Prove that if $F,G:\{0,1\}^* \rightarrow \{0,1\}^*$ are in $\overline{\mathbf{P}}$ then their _composition_ $F\circ G$, which is the function $H$ s.t. $H(x)=F(G(x))$, is also in $\overline{\mathbf{P}}$.


> # {.exercise title="Non composition of exponential time" #exp-time-comp-ex}
Prove that there is some $F,G:\{0,1\}^* \rightarrow \{0,1\}^*$ s.t. $F,G \in \overline{\mathbf{EXP}}$ but $F\circ G$ is not in $\mathbf{EXP}$.^[TODO: check that this works, idea is that we can do bounded halting.]


> # {.exercise title="Oblivious program" #oblivious-ex}
We say that a NAND++ program $P$ is oblivious if there is some functions $T:\N \rightarrow \N$ and $i:\N\times \N \rightarrow \N$ such that for every input $x$ of length $n$, it holds that:\
* $P$ halts when given input $x$  after exactly $T(n)$ steps. \
* For $t\in \{1,\ldots, T(n) \}$, after $P$ executes the $t^{th}$ step of the execution the value of the index `i` is equal to $t(n,i)$. In particular this value does _not_ depend on $x$ but only on its length.^[An oblivious program $P$ cannot compute functions whose output length is not a function of the input length, though this is not a real restriction, as we can always embed  variable output functions in fixed length ones using some special "end of output" marker.]
Let $F:\{0,1\}^* \rightarrow \{0,1\}^*$ be such that there is some function $m:\N \rightarrow \N$ satisfying $|F(x)|=m(|x|)$ for every $x$, and let $P$ be a NAND++ program that computes $F$ in $T(n)$ time for some nice $T$.
Then there is an _oblivious_ NAND++ program $P'$ that computes $F$ in time $O(T^2(n) \log T(n))$.

^[TODO: Add exercise showing NAND is like NAND++ with advice. Mention the definition of $\mathbf{P}_{/poly}$.]

> # {.exercise title="Evaluating NAND programs" #nandeval}
Let $NANDEVAL:\{0,1\}^* \rightarrow \{0,1\}$ be the function that maps an $n$-input NAND++ program $P$ and a string $x\in \{0,1\}^n$ to $P(x)$.
1. Prove that $NANDEVAL \in \overline{TIME}(\tilde{O}(T(n)^2))$. For extra credit prove that $NANDEVAL \in \overline{TIME}(\tilde{O}(T(n)))$. \
2. Let $COMPILE$ be the function from   [nand-compiler](){.ref} that  maps a NAND++ program $P$ and strings $1^n,1^m,1^T$  to an $n$-input $m$-output NAND program $Q_P$ such that for every $x\in \{0,1\}^n$, if $P(x)$ outputs $y\in \{0,1\}^m$ within $T$ steps then $Q_P(x)=y$. We saw that $COMPILE \in \overline{TIME}(\tilde{O}(n))$. Use that to show that $TIMEDEVAL \in \overline{TIME}(\tilde{O}(n))$.

## Bibliographical notes

^[TODO: add reference to best algorithm for longest path - probably the Bjorklund algorithm]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements

<!---
## Appendix: Making NAND++ programs oblivious

^[TODO: possibly remove this]

> # {.proof data-ref="oblivious-thm"}
We start by ensuring that the time at which the program halts does not depend on the input but only its length. To do so, we can transform a program running in $T(n)$ time to a "clocked" version that will always takes $T(n)$ steps regardless of the input.
We achieve this by adding a `noop` variable and modify the program to do nothing if `noop` equals to $1$.
Hence, when the original program would assign $0$ to `loop`, we modify `noop` to $1$, and only halt after $T(|x|)$ steps when $x$ is the input.
>
The heart of the proof of [oblivious-thm](){.ref} is to ensure that movements of the  index `i` only depend on the input length.  
Our approach is analogous to replacing a taxi by a bus.
Instead of  the program controlling  to where `i` goes, the index will go obliviously on its route, and we will wait until it reaches the desired location.
That is, regardless of the input the  index `i` will progress between every iteration of the main loop according to the sequence
$$
0,1,0,1,2,1,0,1,2,3,2,1,0,1,\ldots \label{eq:pattern}
$$
>
>![We simulate a NAND++ program by an oblivious program in which the index moves according to the pattern of [eq:pattern](){.eqref}.](../figure/oblivious_simulation.png){#oblivious-fig .class width=300px height=300px}
>
That is, `i` will sweep back and forth from index $0$ till the current last index $n$, which will be incremented every round, see [oblivious-fig](){.ref}.
In the worst case, in every step we want to decrease `i`  when we are at an "upward sweep", and increase `i` when we are in a "downward sweep", but because the value of `i` is always between $0$ and the current step $t$, we can always achieve the desired value within the next sweep. This means that to make $t$ steps, at the worst case we will need to complete $t$ full back-and-forth sweeps. The total number of movements in these sweeps will be  $2 + 4 + 6 + \ldots + 2t = O(t^2)$ steps, and with an $O(\log t)$ overhead, we can  keep track of which step we are in at the computation, and  compare the current value of `i` with the desired value.

### Getting to $O(T \log T)$.

^[TODO: To be completed, use the appropriate data structure]
---->
