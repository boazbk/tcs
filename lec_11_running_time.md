---
title: " Modeling running time"
filename: "lec_11_running_time"
chapternum: "12"
---

# Modeling running time { #chapmodelruntime }

> ### { .objectives }
* Formally modeling running time, and in particular notions such as $O(n)$ or $O(n^3)$ time algorithms. \
* The classes $\mathbf{P}$ and $\mathbf{EXP}$ modelling polynomial and exponential time respectively. \
* The _time hierarchy theorem_, that in particular says that for every $k \geq 1$ there are functions we _can_ compute in $O(n^{k+1})$ time but _can not_ compute in $O(n^k)$ time.
* The class $\mathbf{P_{/poly}}$ of _non uniform_ computation and the result that $\mathbf{P} \subseteq \mathbf{P_{/poly}}$


>"When the measure of the problem-size is reasonable and when the sizes assume values arbitrarily large, an asymptotic estimate of ... the order of difficulty of [an] algorithm .. is theoretically important. It cannot be rigged by making the algorithm artificially difficult for smaller sizes", Jack Edmonds, "Paths, Trees, and Flowers", 1963

>"The computational complexity of a sequence is to be measured by how fast a multitape Turing machine can print out the terms of the sequence. This particular abstract model of a computing device is chosen because much of the work in this area is stimulated by the rapidly growing importance of computation through the use of digital computers, and all digital computers in a slightly idealized form belong to the class of multitape Turing machines.", Juris Hartmanis and Richard Stearns, "On the computational complexity of algorithms", 1963.




In [chapefficient](){.ref} we saw examples of efficient algorithms, and made some claims about their running time, but did not give a mathematically precise definition for this concept.
We do so in this chapter, using the models of Turing machines and RAM machines (or equivalently NAND-TM and NAND-RAM) we have seen before.
The running time of an algorithm is not a fixed number since any non-trivial algorithm will take longer to run on longer inputs. 
Thus, what we want to measure is the _dependence_ between the number of steps the algorithms takes and the length of the input.
In particular we care about the distinction between algorithms that take at most _polynomial time_ (i.e., $O(n^c)$ time for some constant $c$) and problems for which every algorithm requires at least _exponential time_ (i.e., $\Omega(2^{n^c})$ for some $c$).
As mentioned in Edmond's quote above, the difference between these two can sometimes be as important as the difference between being computable and uncomputable.



_Other measures of complexity._ Because we are interested in the _maximum_ number of steps for inputs of a given length, this concept is often known as _worst case complexity_. The _minimum_ number of steps (or "best case" complexity) to compute a function on length $n$ inputs is typically not a meaningful quantity since essentially every natural problem will have some trivially easy instances. However, the _average case complexity_ (i.e., complexity on a "typical" or "random" input) is an interesting concept which we'll return to when we discuss _cryptography_. That said, worst-case complexity is the most standard and basic of the complexity measures, and will be our focus in most of this book.

## Formally defining running time

Our models of computation such Turing Machines, NAND-TM and NAND-RAM programs and others all operate by executing a sequence of instructions on an input one step at a time.
The running time is defined by measuring the number of steps as a function of the length of the input.
We start by defining running time with respect to Turing Machines:

::: {.definition title="Running time (Turing Machines)" #time-TM-def}
Let $T:\N \rightarrow \N$ be some function mapping natural numbers to natural numbers.
We say that a function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ is _computable in $T(n)$ Single-Tape-Turing-Machine time (TM-time for short)_ 
if there exists a Turing Machine $M$ such that for every sufficiently large $n$ and every $x\in \{0,1\}^n$, when given input $x$, the machine $M$ halts after executing at most $T(n)$ steps and outputs $F(x)$.

We define  $TIME_{\mathsf{TM}}(T(n))$ to be the set of Boolean functions (functions mapping $\{0,1\}^*$ to $\{0,1\}$) that are computable in $T(n)$ TM time.
:::

::: { .pause }
[time-def](){.ref}  is not very complicated but is one of the most important definitions of this book. As usual,   $TIME_{\mathsf{TM}}(T(n))$ is  a class of _functions_, not of _machines_. If $M$ is a Turing Machine then a statement such as "$M$ is a member of $TIME_{\mathsf{TM}}(n^2)$" does not make sense.
:::

The relaxation of considering only "sufficiently large" $n$'s is not very important but it is convenient since it allows us to avoid dealing explicitly with un-interesting "edge cases". In most cases we will anyway be interested in determining running time only up to constant and even polynomial factors. Note that we can always compute a function on a finite number of inputs using a lookup table.

While the notion of being computable within a certain running time is defined for every function, the class $TIME_{\mathsf{TM}}(T(n))$ is a class of _Boolean functions_ that have a single bit of output.
This choice is not very important, but is made for simplicity and convenience later on.
In fact, every non-Boolean function has a computationally equivalent Boolean variant, see [boolex](){.ref}.






### Polynomial and Exponential Time

Unlike the notion of computability, the exact running time can be a function of the model we use. However, it turns out that if we only care about "coarse enough" resolution (as will most often be the case) then the choice of the model, whether  Turing Machines, RAM machines, NAND-TM/NAND-RAM programs, or C/Python programs, does not matter. 
This is known as the _extended_ Church-Turing Thesis.
Specifically we will mostly care about the difference between _polynomial_ and _exponential_ time.


The two main time complexity classes we will be interested in are the following:

* __Polynomial time:__ A function $F:\{0,1\}^* \rightarrow \{0,1\}$ is _computable in polynomial time_ if it is in the class $\mathbf{P} = \cup_{c\in \{1,2,3,\ldots \}} TIME(n^c)$. That is, $F\in \mathbf{P}$ if there is an algorithm to compute $F$ that runs in time at most _polynomial_ (i.e.,  at most $n^c$ for some constant $c$) in the length of the input.

* __Exponential time:__ A function $F:\{0,1\}^* \rightarrow \{0,1\}$ is _computable in exponential time_ if it is in the class $\mathbf{EXP} = \cup_{c\in \{1,2,3,\ldots \}} TIME(2^{n^c})$. That is, $F\in \mathbf{EXP}$ if there is an algorithm to compute $F$ that runs in time at most _exponential_ (i.e., at most $2^{n^c}$ for some constant $c$) in the length of the input.

In other words, these are defined as follows:

::: {.definition title="$\mathbf{P}$ and $\mathbf{EXP}$" #PandEXPdef}
Let $F:\{0,1\}^* \rightarrow \{0,1\}$. We say that $F\in \mathbf{P}$ if there is a polynomial $p:\N \rightarrow \R$ and a Turing Machine $M$ such that for every $x\in \{0,1\}^*$, $M(x)$ runs in at most $p(|x|)$ steps and outputs $F(x)$.

We say that $F\in \mathbf{EXP}$ if there is a polynomial $p:\N \rightarrow \R$ and a Turing Machine $M$ such that for every $x\in \{0,1\}^*$, $M(x)$ runs in at most $2^{p(|x|)}$ steps and outputs $F(x)$.
:::

::: { .pause }
Please make sure you understand why  [PandEXPdef](){.ref} and the bullets above define the same classes.

Sometimes students think of the class $\mathbf{EXP}$ as corresponding to functions that are _not_ in $\mathbf{P}$. However, this is not the case. If $F$ is in $\mathbf{EXP}$ then it _can_ be computed in exponential time. This does not mean that it cannot be computed in polynomial time as well.
:::

Since exponential time is much larger than polynomial time,  $\mathbf{P}\subseteq \mathbf{EXP}$.
All of the  problems we listed in [chapefficient](){.ref} are in $\mathbf{EXP}$, but as we've seen, for some of them there are much better algorithms that demonstrate that they are in fact in the smaller class $\mathbf{P}$.


| $\mathbf{P}$  | $\mathbf{EXP}$ (but not known to be in $\mathbf{P}$) |
|--------------------------|---------------------------|
| Shortest path            | Longest Path              |
| Min cut                  | Max cut                   |
| 2SAT                     | 3SAT                      |
| Linear eqs               | Quad. eqs                 |
| Zerosum                  | Nash                      |
| Determinant              | Permanent                 |
| Primality                | Factoring                 |

A table of the examples from [chapefficient](){.ref}.
All these problems are in $\mathbf{EXP}$ but the only the ones on the left column are currently known to be in $\mathbf{P}$ as well (i.e., they have a polynomial-time algorithm).


::: {.remark title="Boolean versions of problems" #booleanversion}
Many of the problems defined in [chapefficient](){.ref}]() correspond to _non Boolean_ functions (functions with more than one bit of output) while $\mathbf{P}$ and $\mathbf{EXP}$ are sets of Boolean functions. However, for every non-Boolean function $F$ we can always define an equivalent Boolean function $G$ by letting $G(x,i)$ be the $i$-th bit of $F(x)$ (see [boolex](){.ref}).
Hence the table above refers to the computationally-equivalent Boolean variants of these problems.
:::



## Modeling running time using RAM Machines / NAND-RAM

Turing Machines are a clean theoretical model of computation, but do not closely correspond to real-world computing architectures.
The discrepancy between Turing Machines and actual computers does not matter much when we consider the question of which functions are _computable_, but can make a difference in the context of _efficiency_.
Even a basic staple of undergraduate algorithms such as  "merge sort" cannot be implemented on a Turing Machine in $O(n\log n)$ time (see [bibnotesrunningtime](){.ref}).
_RAM machines_ (or equivalently, NAND-RAM programs) more closely match actual computing architecture and what we mean when we say $O(n)$ or $O(n \log n)$ algorithms in algorithms courses or whiteboard coding interviews.
We can define running time with respect to NAND-RAM programs just as we did for Turing Machines.



::: {.definition title="Running time (RAM)" #time-def}
Let $T:\N \rightarrow \N$ be some function mapping natural numbers to natural numbers.
We say that a function $F:\{0,1\}^* \rightarrow \{0,1\}^*$ is _computable in $T(n)$ RAM  time (RAM-time for short)_ 
if there exists a NAND-RAM program $P$ such that for every sufficiently large $n$ and every $x\in \{0,1\}^n$, when given input $x$, the program $P$ halts after executing at most $T(n)$ iterations and outputs $F(x)$.

We define  $TIME_{\mathsf{RAM}}(T(n))$ to be the set of Boolean functions (functions mapping $\{0,1\}^*$ to $\{0,1\}$) that are computable in $T(n)$ TM time.
:::

Because NAND-RAM programs correspond more closely to our natural notions of running time, we will use NAND-RAM as our "default" model of running time, and hence use $TIME(T(n))$ (without any subscript) to denote $TIME_{\mathsf{RAM}}(T(n))$.
However, it turns out that as long as we only care about the difference between exponential and polynomial time,  this does not make much difference.
The reason is that Turing Machines can simulate NAND-RAM programs with at most a polynomial overhead:


::: {.theorem title="Relating RAM and Turing machines" #polyRAMTM-thm}
Let $T:\N \rightarrow \N$ be a function such that $T(n) \geq n$ for every $n$ and the map $n \mapsto T(n)$ can be computed by a Turing machine in time $O(T(n)^2)$.^[All non pathological time bound functions such as $T(n)=n$, $T(n)n\log n$, $T(n)=2^n$ etc. satisfy these conditions, see also [niceboundssec](){.ref}  below.]
Then 
$$
TIME_{\mathsf{TM}}(T(n)) \subseteq TIME_{\mathsf{RAM}}(T(n)) \subseteq TIME_{\mathsf{TM}}(T(n)^4) \;.
$$
:::

::: { .bigidea #polyvsnot}
While the precise definition of running time can depend on the computational model, as long as we only care about the distinction between polynomial and exponential, all the models we considered are equivalent to each other. 
:::


The constant $4$ can be improved to a smaller value, though this will not be important for us.
[polyRAMTM-thm](){.ref} implies that the  $\mathbf{P}$ and $\mathbf{EXP}$ could have been equivalently defined using NAND-RAM programs instead of Turing Machines, as they would have contained the exact same set of functions. 
Similar equivalence results are known for many models including cellular automata, C/Python/Javascript programs, parallel computers,   and a great many other models, which justifies the choice of $\mathbf{P}$ as capturing a technology-independent notion of tractability.
This equivalence between Turing machines and NAND-RAM  (as well as other models) allows us to pick our favorite model depending on the task at hand (i.e., "have our cake and eat it too").
When we want to _design_ an algorithm, we can use the extra power and convenience afforded by NAND-RAM.
When we want to _analyze_ a program or prove a _negative result_, we can restrict attention to   Turing machines.


> ### {.proofidea data-ref="polyRAMTM-thm"}
The direction $TIME_{\mathsf{TM}}(T(n)) \subseteq TIME_{\mathsf{RAM}}(T(n))$ is not hard to show, since a NAND-RAM program  can simulate a Turing Machine so that each step of the machine is captured by one iteration of the main loop of the program.
Thus the heart of the theorem is to prove that $TIME_{\mathsf{RAM}}(T(n)) \subseteq TIME_{\mathsf{TM}}(T(n)^4)$. This proof closely follows the proof of  [RAMTMequivalencethm](){.ref}, where we have shown that every function $F$ that is computable by a NAND-RAM program $P$ is computable by a Turing Machine (or equivalently a NAND-TM program) $M$.  To prove [polyRAMTM-thm](){.ref}, we follow the exact same proof but just check that the overhead of the simulation of $P$ by $M$ is polynomial.
The proof has many details, but is not deep. It is therefore much more important that you understand the _statement_ of this theorem than its proof.

::: {.proof data-ref="polyRAMTM-thm"}
We only focus on the non-trivial direction $TIME_{\mathsf{RAM}}(T(n)) \subseteq TIME_{\mathsf{TM}}(T(n)^4)$.
Let $F\in TIME_{\mathsf{RAM}}(T(n))$. 
$F$ can be computed in time $T(n)$ by some NAND-RAM program $P$ and we need to show that it can also be computed in time $T(n)^4$ by a Turing Machine $M$.
This will follow from showing  that $F$ can be computed in time $T(n)^4$ by a NAND-TM program, since for every NAND-TM program $Q$ there is a Turing Machine $M$ simulating it such that each iteration of $Q$ corresponds to a single step of $M$.


As mentioned above, we follow the proof of [RAMTMequivalencethm](){.ref} (simulation of NAND-RAM programs using NAND-TM programs) and use the exact same simulation, but with a more careful accounting of the number of steps that the simulation costs.
Recall, that the simulation of NAND-RAM works by "peeling off" features of NAND-RAM one by one, until we are left with NAND-TM.

We will not provide the full details but will present the main ideas used in showing that every feature of NAND-RAM can be simulated by NAND-TM with at most a polynomial overhead:

1. Recall that every NAND-RAM variable or array element can contain an integer between $0$ and $T$ where $T$ is the number of lines that have been executed so far. Therefore if  $P$ is a NAND-RAM program that computes $F$ in $T(n)$ time, then on inputs of length $n$, all integers used by $P$ are of magnitude at most $T(n)$. This means that the largest value `i` can ever reach is at most $T(n)$ and so each one of $P$'s variables can be thought of as an array of at most $T(n)$ indices, each of which holds a natural number of magnitude at most $T(n)$. We let $\ell = \ceil{\log T(n)}$ be the number of bits needed to encode such numbers. (We can start off the simulation by computing $T(n)$ and $\ell$.) 


2. We can encode a NAND-RAM array of length $\leq T(n)$ containing numbers in $\{0,\ldots, T(n)-1 \}$ as an Boolean (i.e., NAND-TM) array of  $T(n)\ell =O(T(n)\log T(n))$ bits, which we can also think of as a _two dimensional array_ as we did in the proof of [RAMTMequivalencethm](){.ref}. We encode a NAND-RAM scalar containing a number in $\{0,\ldots, T(n)-1 \}$ simply by a shorter NAND-TM array of $\ell$ bits. 

3. We can simulate the two dimensional arrays  using one-dimensional arrays of length $T(n)\ell = O(T(n) \log T(n)$.  All the arithmetic operations on integers use the grade-school algorithms, that take time that is polynomial in the number $\ell$ of bits of the integers, which is  $poly(\log T(n))$ in our case.  Hence we can simulate $T(n)$ steps of NAND-RAM with $O(T(n)poly(\log T(n))$ steps of a model that uses random access memory but only _Boolean-valued_ one-dimensional arrays.

4. The most expensive step is to translate from random access memoery to the sequential memory model of NAND-TM/Turing Machines. As we did in the proof of [RAMTMequivalencethm](){.ref} (see [nandtmgorydetailssec](){.ref}), we can simulate accessing an array `Foo` at some location encoded in an array `Bar` by:

   a. Copying `Bar` to some temporary array `Temp`
   b. Having an array `Index`  which is initially all zeros except $1$ at the first location.
   c. Repeating the following until `Temp` encodes the number $0$: _(Number of repetitions is at most $T(n)$.)_
      - Decrease the number encoded temp by $1$. _(Take number of steps polynomial in $\ell = \ceil{\log T(n)}$.)_
      - Decrease `i` until it is equal to $0$. _(Take $O(T(n)$ steps.)_
      - Scan `Index` until we reach the point in which it equals $1$ and then change this $1$ to $0$ and go one step further and write $1$ in this location. _(Takes $O(T(n))$ steps.)_
   d. When we are done we know that if we  scan `Index` until we reach the point in which `Index[i]`$=1$ then `i` contains the value that was encoded by `Bar` _(Takes $O(T(n)$ steps.)_

  The total cost for each such operation is $O(T(n)^2 + T(n)poly(\log T(n))) = O(T(n)^2)$ steps.

In sum, we simulate a single step of NAND-RAM using $O(T(n)^2 poly(\log T(n)))$ steps of NAND-TM, and hence the total simulation time is $O(T(n)^3 poly(\log T(n)))$ which is smaller than $T(n)^4$ for sufficiently large $n$.
:::






[polyRAMTM-thm](){.ref} shows that the classes $\mathbf{P}$ and $\mathbf{EXP}$ are _robust_ with respect to variation in the choice of the computational model.
They are also robust with respect to our choice of the representation of the input.
For example, whether we decide to represent graphs as adjacency matrices or adjacency lists will not make a difference as to whether a function on graphs is in $\mathbf{P}$ or $\mathbf{EXP}$.
The reason is that changing from one representation to another at most squares the size of the input, and a quantity is polynomial in $n$ if and only if it is polynomial in $n^2$.

More generally, for every function $F:\{0,1\}^* \rightarrow \{0,1\}$, the answer to the question of whether $F\in \mathbf{P}$ (or whether $F\in \mathbf{EXP}$) is unchanged by switching representations, as long as transforming one representation to the other can be done in polynomial time (which essentially holds for all reasonable representations).





::: {.remark title="Nice time bounds" #nicefunctionsrem}
When considering general time bounds such we need to make sure to rule out some "pathological" cases such as functions $T$ that don't give enough time for the algorithm to read the input, or functions where the time bound itself is uncomputable. We say that a function $T:\N \rightarrow \N$ is a  _nice time bound function_ (or nice function for short) if for every $n\in \N$, $T(n) \geq n$ (i.e., $T$ allows enough time to read the input), for every $n' \geq n$, $T(n') \geq T(n)$ (i.e., $T$ allows more time on longer inputs), and the map $F(x) = 1^{T(|x|)}$  (i.e., mapping a string of length $n$ to a sequence of $T(n)$ ones) can be computed by a NAND-RAM program in $O(T(n))$ time.

All the "normal" time complexity bounds we encounter in applications such as $T(n)= 100 n$, $T(n) =  n^2 \log n$,$T(n) = 2^{\sqrt{n}}$, etc.  are "nice".
Hence from now on we will only care about the class $TIME(T(n))$   when $T$ is a "nice" function.
The computability condition is in particular typically easily satisfied.
For example, for arithmetic functions such as $T(n) = n^3$, we can typically compute the binary representation of $T(n)$ in time polynomial _in the number of bits_ of $T(n)$ and hence poly-logarithmic in $T(n)$.
Hence the time to write the string $1^{T(n)}$ in such cases will be $T(n) + poly(\log T(n)) = O(T(n))$.
:::






## Efficient universal machine: a NAND-RAM interpreter in NAND-RAM

We have seen in [universaltmthm](){.ref} the "universal Turing Machine".
Examining that proof, and combining it with  [polyRAMTM-thm](){.ref} , we can see that the program $U$ has a _polynomial_ overhead, in the sense that it can simulate $T$ steps of a given NAND-TM (or NAND-RAM) program $P$ on an input $x$ in $O(T^4)$ steps.
But in fact, by directly simulating NAND-RAM programs we can do better with only a _constant_ multiplicative overhead.
That is, there is a _universal NAND-RAM program_ $U$ such that for every NAND-RAM program $P$, $U$ simulates $T$ steps of $P$ using only $O(T)$ steps.


::: {.theorem title="Efficient universality of NAND-RAM" #univ-nandpp}
There exists a NAND-RAM program $U$ satisfying the following:

1. _($U$ is a universal NAND-RAM program.)_ For every NAND-RAM program $P$ and input $x$,  $U(P,x)=P(x)$ where by $U(P,x)$ we denote the output of $U$ on a string encoding the pair $(P,x)$.

2. _($U$ is efficient.)_ For every NAND-RAM program $P$ there is some constant $C$  such that if $P$ halts on input $x$ after most $T$ iterations of its loop, then $U(P,x)$ halts after at most $C\cdot T$ iterations of its loop.
:::


> ### { .pause }
Before reading the proof of [univ-nandpp](){.ref}, try to think how you would try to write such a interpreter for NAND-RAM in your favorite programming language.
You will likely find that your program requires $O(T)$ steps to perform this simulation.
As in the case of [polyRAMTM-thm](){.ref}, the proof of [univ-nandpp](){.ref} is not very deep and it more important to understand its _statement_.
If you understand how you would go about writing an interpreter for NAND-RAM using a modern programming language such as Python, then you know everything you need to know about this theorem.


::: {.proof data-ref="univ-nandpp"}
To present a universal NAND-RAM program in full we would need to describe a precise representation scheme, as well as the full NAND-RAM instructions for the program.
While this can be done, it is more important to focus on the main ideas, and so we just sketch the proof here.
A specification of NAND-RAM is given in the Appendix, and for the purposes of this simulation, we can simply use the representation of the code NAND-RAM as an ASCII string.

The program $U$ gets as input a NAND-RAM program $P$ and an input $x$ and simulates $P$ one step at a time.
To do so, $U$ will do the following:

1. $U$ will maintain variables  `current_line`, and `number_steps` for the current line to be executed and the number of steps executed so far.

2. $U$ will scan the code of $P$ to find the number $t$ of unique variable names that $P$ uses. If we denote these names by $var_0,\ldots,var_{t-1}$  then $U$ maintains an array `Var_numbers` that contains a list of pairs of the form $(var_s,s)$ for $s\in [t]$. Using `Var_numbers` we can translate the name of a variable to a number in $[t]$ that corresponds to its index.

3. $U$ will maintain an array `Var_values` that will contain the current values of all $P$'s variables. If the $s$-th variable of $P$ is a scalar variable, then its value will be stored in location `Var_values[`$s$`]`.
If it is an array variable then the value of its $i$-th element will be stored in location `Var_values[`$t\cdot i + s$`]`.

4. To simulate a single step of $P$, the program $U$ will recover the line corresponding to `line_counter`  and execute it. Since NAND-RAM has a constant number of arithmetic operations, we can simulate choosing which operation to execute with a sequence of a constantly many if-then-else's.  When executing these operations, $U$ will use the variable `step_counter` that keeps track of the iteration counter of $P$.


Simulating a single step of $P$ will take $O(|P|)$ steps for the program $U$ where $|P|$ is the length of the description of $P$ as a string (which in particular is an upper bound on the number $t$ of variable $P$ uses). Hence the total running time will be $O(|P|T)$  which is $O(T)$ when suppressing constants that depend on the program $P$.

To be a little more concrete, here is some "pseudocode" description of the program $U$:^[We use Python-like syntax in this pseudocode, but it is not valid Python code.]

```python
def U(P,x):
    t = number_variable_identifiers(P) # number of distinct identifiers used in P

    L = number_lines(P)

    # denote names of P's variables as var_0,..., var_(t-1)
    Var_numbers = array encoding list [ (var_0,0),...,(var_(t-1),t-1)]
    # Var_numbers: encode variable identifiers as number 0...t-1

    Var_values = unbounded array initialized to 0
    # if s in [t] corresponds to scalar then Var_values[s] is value of variable corresponding to s.
    # if s corresponds to array then Var_values[t*i+s] is value of variable corresponding to s at position i

    def varid(name):
        # scan the array Var_numbers and
        # return the number between 0 and t-1
        ...

    def get_scalar_value(name):
        return Var_values[varid(name)]

    def get_array_value(name,i):
        return Var_values[t*i+varid(name)]

    def set_scalar_value(name,val):
        Var_values[varid(name)] = val

    def set_array_value(name,i,val):
        Var_values[t*i+varid(name)] = val

    for i=0..|x|-1:
        set_array_value("X",i,x[i])
        set_array_value("X_nonblank",i,1)

    current_line = 0
    number_steps = 0

    do {
        line = P[current_line] # extract current line of P

        # code to execute line
        # We use get/set procedures above to update vars
        ...
        # Update counters
        current_line = current_line + 1 (mod L)
        number_steps = number_steps + 1

    } until get_scalar_value("loop")==0 

    # Produce output:
    if get_scalar_value("loop")==1: return "FAIL"
    m = smallest m s.t. get_array_value("Y_nonblank",m)=0
    return [get_array_value("Y",i) for i=0..m-1]
```
:::



## Time hierarchy theorem

We have seen that there are uncomputable functions, but are there functions that can be computed, but only at an exorbitant cost? For example, is there a function that _can_ be computed in time $2^n$, but _can not_ be computed in time $2^{0.9 n}$?
It turns out that the answer is __Yes__:

> ### {.theorem title="Time Hierarchy Theorem" #time-hierarchy-thm}
For every nice function $T$, there is a function $F:\{0,1\}^* \rightarrow \{0,1\}$
in $TIME(T(n)\log n) \setminus TIME(T(n))$.^[There is nothing special about $\log n$, and we could have used any other efficiently computable function that tends to infinity with $n$.]

Note that in particular this means that $\mathbf{P}$ is _strictly contained_ in $\mathbf{EXP}$.

> ### {.proofidea data-ref="time-hierarchy-thm"}
In the proof of [halt-thm](){.ref} (the uncomputability of the Halting problem), we have shown that the function $HALT$ cannot be computed in any finite time. An examination of the proof shows that it gives something stronger.
Namely, the proof shows that if we fix our computational budget to be $T$ steps, then not only we can't distinguish between programs that halt and those that do not, but cannot even distinguish between programs that halt within at most $T'$ steps and those that take more than that (where $T'$ is some number depending on $T$).
Therefore, the proof of [time-hierarchy-thm](){.ref} follows the ideas of the uncomputability of the halting problem, but again with a more careful accounting of the running time.


If you fully understand the proof of [halt-thm](){.ref}, then reading the following proof should not be hard.
If you don't, then this is an excellent opportunity to review this reasoning.


::: {.proof data-ref="time-hierarchy-thm"}
Recall the Halting function $HALT:\{0,1\}^* \rightarrow \{0,1\}$ that was defined as follows:
$HALT(P,x)$ equals $1$ for every program $P$ and input $x$ s.t.  $P$ halts on input $x$, and is equal to $0$ otherwise.
We cannot use the Halting function of course, as it is uncomputable and hence not in $TIME(T'(n))$ for any function $T'$. However, we will use the following variant of it:

We define the _Bounded Halting_ function $HALT_T(P,x)$ to equal $1$ for every NAND-RAM program $P$ such that $|P| \leq \log \log |x|$, and such that $P$ halts on the input $x$ within $100 T(|x|)$ steps. $HALT_T$ equals $0$ on all other inputs.^[The constant $100$ and the function $\log \log n$ are rather arbitrary, and are chosen for convenience in this proof.]

[time-hierarchy-thm](){.ref} is an immediate consequence of the following two claims:

__Claim 1:__ $HALT_T \in TIME(T(n)\ log n)$

and

__Claim 2:__ $HALT_T \not\in TIME(T(n))$.

Please make sure you understand why indeed the theorem follows directly from the combination of these two claims. We now turn to proving them.

__Proof of claim 1:__ We can easily check in linear time whether an input has the form $P,x$ where $|P| \leq \log\log |x|$.
Since $T(\cdot)$ is a nice function, we can evaluate it in $O(T(n))$ time. Thus, we can perform the check above, compute $T(|P|+|x|)$ and use the universal NAND-RAM program of [univ-nandpp](){.ref} to evaluate $HALT_T$ in at most $poly(|P|) T(n)$ steps.^[Recall that we use $poly(m)$ to denote a quantity that is bounded by $am^b$ for some constants $a,b$ and every sufficiently large $m$.]
Since $(\log \log n)^a = o(\log n)$ for every $a$, this will be smaller than $T(n)\log n$ for every sufficiently large $n$, hence completing the proof.


__Proof of claim 2:__ This proof is the heart of [time-hierarchy-thm](){.ref}, and is very reminiscent of the proof that $HALT$ is not computable.
Assume, toward the sake of contradiction, that there is some NAND-RAM program $P^*$ that computes $HALT_T(P,x)$ within $T(|P|+|x|)$ steps. We are going to show a contradiction by creating a program $Q$ and showing that under our assumptions, if $Q$ runs for less than $T(n)$ steps when given (a padded version of)  its own code as input then it actually runs for more than $T(n)$ steps and vice versa. (It is worth re-reading the last sentence twice or thrice to make sure you understand this logic. It is very similar to the direct proof of the uncomputability of the halting problem where we obtained a contradiction by using an assumed "halting solver" to construct a program that, given its own code as input, halts if and only if it does not halt.)


We will define $Q$ to be the program that on input a string $z$   does the following:

1. If $z$ does not have the form $z=P1^m$ where $P$ represents a NAND-RAM program and $|P|< 0.1 \log\log m$ then return $0$.

2. Compute $b= P^*(P,z)$ (at a cost of at most $T(|P|+|z|)$ steps, under our assumptions).

3. If $b=1$ then $Q$ goes into an infinite loop, otherwise it halts.

We chose $m$ sufficiently large so that $|Q| < 0.001\log\log m$ where $|Q|$ denotes the length of the description of $Q$ as a string. We will reach a contradiction by splitting into cases according to whether or not $HALT_T(Q,Q1^m)$ equals $0$ or $1$.


On the one hand, if $HALT_T(Q,Q1^m)=1$, then under our assumption that $P^*$ computes $HALT_T$, $Q$ will go into an infinite loop on input $z=Q1^m$, and hence in particular $Q$ does _not_ halt within $100 T(|Q|+m)$ steps on the input $z$. But this contradicts our assumption that $HALT_T(Q,Q1^m)=1$.

This means that it must hold that $HALT_T(Q,Q1^m)=0$. But in this case, since we assume $P^*$ computes $HALT_T$, $Q$ does not do anything in phase 3 of its computation, and so the only computation costs come in phases 1 and 2 of the computation.
It is not hard to verify that Phase 1 can be done in linear and in fact less than $5|z|$ steps.
Phase 2 involves executing $P^*$, which under our assumption requires $T(|Q|+m)$ steps.
In total we can perform both phases in less than $10 T(|Q|+m)$ in steps, which by definition means that $HALT_T(Q,Q1^m)=1$, but this is of course a contradiction. This completes the proof of Claim 2 and hence of [time-hierarchy-thm](){.ref}.
:::



The time hierarchy theorem tells us that there are functions we can compute in $O(n^2)$ time but not $O(n)$, in $2^n$ time, but not $2^{\sqrt{n}}$, etc..
In particular there are most definitely functions that we can compute in time $2^n$ but not $O(n)$.
We have seen that we have no shortage of natural functions for which the best _known_ algorithm requires roughly $2^n$ time, and that many people have invested significant effort in trying to improve that.
However,  unlike in the finite vs. infinite case, for all of the examples above at the moment we do not know how to rule out even an $O(n)$ time algorithm.
We will however see that there is a single unproven conjecture that would imply such a result for most of these problems.

![Some complexity classes and some of the functions we know (or conjecture) to be contained in them.](../figure/time_complexity_map.png){#complexityclassinclusionfig .margin  }



The time hierarchy theorem relies on the existence of an efficient universal NAND-RAM program, as proven in [univ-nandpp](){.ref}. For other models, such as Turing Machines we have similar time hierarchy result showing that there are functions computable in time $T(n)$ and not in time $T(n)/f(n)$ where $f(n)$ corresponds to the overhead in the corresponding universal machine. (For multitape Turing machines $f(n)$ is logarithmic.)


## Unrolling the loop: Uniform vs non uniform computation



We have now seen two measures of "computation cost" for functions.
For a finite function $G:\{0,1\}^n \rightarrow \{0,1\}^m$,  we said that $G\in SIZE(T)$ if there is a $T$-line NAND-CIRC program that computes $G$.
We saw that _every_ function mapping $\{0,1\}^n$ to $\{0,1\}^m$ can be computed using at most $O(m2^n)$ lines.
For infinite functions $F:\{0,1\}^* \rightarrow \{0,1\}^*$, we can define the "complexity" by the smallest $T$ such that $F \in TIME(T(n))$.
Is there a relation between the two?

For simplicity, let us restrict attention to Boolean (i.e., single-bit output) functions $F:\{0,1\}^* \rightarrow \{0,1\}$.
For every such function, define $F_{\upharpoonright n} : \{0,1\}^n \rightarrow \{0,1\}$ to be the restriction of $F$ to inputs of size $n$.
We have seen two ways to define that $F$ is computable within a roughly $T(n)$ amount of resources:

1. There is a _single algorithm_ $P$ that computes $F$ within $T(n)$ steps on all inputs of length $n$. In such a case we say that  $F$ is _uniformly_ computable (or more often, simply "computable") within $T(n)$ steps.

2. For every $n$, there is a $T(n)$ NAND-CIRC program $Q_n$ that computes $F_{\upharpoonright n}$. In such a case we say that $F$ can be computed via a _non uniform_ $T(n)$ bounded sequence of algorithms.

Unlike the first condition, where there is a single algorithm or "recipe" to compute $F$ on all possible inputs, in the second condition we allow the restriction $F_{\upharpoonright n}$ to be computed by a completely different program $Q_n$ for every $n$.
One can see that the second condition is much more relaxed, and hence we might expect that every function satisfying the first condition satisfies the second one as well (up to a small overhead in the bound $T(n)$).
This indeed turns out to be the case:


> ### {.theorem title="Nonuniform computation contains uniform computation" #non-uniform-thm}
There is some $c\in \N$ s.t. for every nice $T:\N \rightarrow \N$ and  $F:\{0,1\}^* \rightarrow \{0,1\}$ in  $TIME_{\mathsf{TM}}(T(n))$ and every sufficiently large $n\in N$,  $F_{\upharpoonright n}$ is in $SIZE(c T(n))$.

::: {.proofidea data-ref="non-uniform-thm"}
To prove [non-uniform-thm](){.ref} we use the technique of "unraveling the loop". That is, we can use "copy paste" to replace a program $P$ that uses a loop that iterates for at most $T$ times with a "loop free" program that has about $T$ times as many lines as $P$.

Let us give an example using C-like syntax.
Suppose we had a program of the form:

```clang
do {
    // some code
} while (loop==1)
```

and we had the guarantee that the program would iterate the loop for at most $4$ times before it breaks.

Then we could change it to an equivalent loop-free program of the following form:

```clang
// some code
if (loop) {
    // some code
    }
if (loop) {
    // some code
}
if (loop) {
    // some code
}
```

That is all there is to the proof of [non-uniform-thm](){.ref}
:::


::: {.proof data-ref="non-uniform-thm"}
The proof follows by the argument of "unraveling the loop".
If $P$ is a NAND-TM program of $L$ lines and $T:\N \rightarrow \N$ is a function such that for every input $x\in \{0,1\}^n$, $P$ halts after executing at most $T(n)$ lines (and hence iterating at most $\floor{T(n)/L}$ times) then we can obtain a NAND-CIRC program $Q$ on $n$ inputs as follows:

```python
P{i<-0}
IF (loop) P〈i<-1〉
IF (loop) P〈i<-0〉
IF (loop) P〈i<-1〉
IF (loop) P〈i<-2〉
IF (loop) P〈i<-1〉
IF (loop) P〈i<-0〉
IF (loop) P〈i<-1〉
...
IF (loop) P〈i<-R〉
```
where for every number $j$, we denote by `P〈i<-`$j$`〉` the NAND-CIRC program that is obtained by replacing all references of the form `Foo[i]` (which are allowed in NAND-TM, but illegal in NAND that has no index variable `i`) with references of the form `Foo[`$j$`]` (which are allowed in NAND, since $j$ is simply a number).
Whenever we see a reference to the variable `X_nonblank[`$i$`]` in the program we will replace it with `one` or `zero` depending on whether $i<n$.
Similarly, we will replace all references to `X[`$i$`]` for $i \geq n$ with `zero`. (We can use our standard syntactic sugar to create the constant `zero` and `one` variables.)

We simply repeat the lines of the form `IF (loop) P〈i<-`$j$`〉` for $\floor{T(n)/L}-1$ times, replacing each time $j$ by $0,1,0,1,2,\ldots$ as in the definition of (standard or "vanilla") NAND-TM in [vanillanandpp](){.ref}.
We replace `IF` with the appropriate syntactic sugar, which will incur a multiplicative overhead of at most $4$ in the number of lines.
After this replacement, each line of the form `IF (loop) P〈i<-`$j$`〉` corresponds to at most $4L$ lines of standard sugar-free NAND.
Thus the total cost is at most $4L \cdot (\tfrac{T(n)}{L}) \leq 4 \cdot T(n)$ lines.^[The constant $4$ can be improved, but this does not really make much difference.]
:::


By combining [non-uniform-thm](){.ref}  with [polyRAMTM-thm](){.ref}, we get that if $F\in TIME(T(n))$ then there are some constants $a,b$ such that for every large enough $n$, $F_{\upharpoonright n} \in SIZE(aT(n)^b)$. (In fact, by direct inspection of the proofs we can see that $a=b=5$  would work.)


### Algorithmic transformation of NAND-TM to NAND and "Proof by Python" (optional)


The proof of [non-uniform-thm](){.ref} is _algorithmic_, in the sense that the proof yields a polynomial-time algorithm that given a NAND-TM program $P$ and parameters $T$ and $n$, produces a NAND-CIRC program $Q$ of $O(T)$ lines that agrees with $P$ on all inputs $x\in \{0,1\}^n$ (as long as $P$ runs for less than $T$ steps these inputs.)
Thus the same proof gives the following theorem:


::: {.theorem title="NAND-TM to NAND compiler" #nand-compiler}
There is an $O(n)$-time NAND-RAM program $COMPILE$ such that on input a NAND-TM program $P$,  and strings of the form $1^n,1^m,1^T$  outputs a NAND-CIRC program $Q_P$ of at most $O(T)$ lines with $n$ bits of inputs and $m$ bits of output satisfying the following property.

For every $x\in\{0,1\}^n$, if $P$ halts on input $x$ within fewer than $T$ steps and outputs some string $y\in\{0,1\}^m$, then $Q_P(x)=y$.
:::

We omit the proof of the [nand-compiler](){.ref}  since it follows in a fairly straightforward way from the proof of [non-uniform-thm](){.ref}.
However, for the sake of concreteness, here is a _Python_ implementation of the function $COMPILE$.
(The reader can feel free to skip it.)

For starters, let us consider an imperfect but very simple program that unrolls the loop.
The following program will work correctly for the case that $m=1$ and that the underlying NAND-TM program had the property that it only modifies the value of the `Y[0]` variable once. (A property that can be ensured by adding appropriate flag variables and some `IF` syntactic sugar.)

```python
def COMPILE(P,T,n):
    '''
    Gets P = NAND-TM program
    T - time bound, n - number of inputs, single output
    Produces NAND-CIRC program of T lines that computes
    the restriction of P to inputs of length n and T steps.

    assumes program contains "one" and "zero" variables and that Y[0] is never modified after the correct value is
    written, so it is safe to run for an additional number of loops.
    '''
    numlines = P.count("\n")

    result = ""
    for t in range(T // numlines):
        i = index(t) # value of i in T-th iteration
        X_nonblank_i = ('one' if i < n else 'zero' )
        X_i = ('X[i]' if i< n else 'zero')
        Q = P.replace('Validx[i]',X_nonblank_i).replace('X[i]',X_i)
        result += Q.replace('[i]',f'[{i}]')
    return result
```

The `index` function takes a number $t$ and returns the value of the index variable `i` in the $t$-th iteration. Recall that this value in NAND-TM follows the sequence $0,1,0,1,2,1,0,1,2,\ldots$ and it can be computed in Python as follows:

```python
from math import sqrt
def index(k):
    return min([abs(k-int(r)*(int(r)+1)) for r in [sqrt(k)-0.5,sqrt(k)+0.5]])
```

Below is a more "robust" implementation of `COMPILE`, that works for an arbitrarily large number of outputs, and makes no assumptions on the structure of the input program.

```python
def COMPILE(P,T,n,m):
    '''
    Gets P = NAND PP program
    T - time bound, n - number of inputs, m - number of outputs
    Produces NAND-CIRC program of O(T) lines that computes
    the restriction of P to inputs of length n and T steps
    '''
    lines = [l for l in P.split('\n') if l] # lines of P

    # initialization
    result = r'''
temp = NAND(X[0],X[0])
one = NAND(X[0],temp)
zero = NAND(one,one)
nothalted = NAND(X[0],temp)
halted = NAND(one,one)
'''[1:]

    # assign_to = IF(halted,assign_to,new_value)
    IFCODE = r'''
iftemp_0 = NAND(new_value,nothalted)
iftemp_1 = NAND(assign_to,halted)
assign_to = NAND(iftemp_0,iftemp_1)
'''[1:]

    UPDATEHALTED = r'''
halted = NAND(nothalted,loop)
nothalted = NAND(halted,halted)
    '''[1:]

    for t in range(T // len(lines)):
        j = index(t)
        for line in lines:
            if j>= m:
                line = line.replace('Y[i]','temp')
            if j< n:
                line = line.replace('X_nonblank[i]','one')
            else:
                line = line.replace('X_nonblank[i]','zero')
                line = line.replace('X[i]','zero')

            line = line.replace('[i]',f'[{j}]')
            idx = line.find("=")
            lefthand = line[:idx].strip()
            righthand = line[idx+1:].strip()
            result += "new_value = " + righthand + "\n"
            result += IFCODE.replace("assign_to",lefthand)
        result += UPDATEHALTED

    return result
```

Since NAND-RAM programs can be simulated by NAND-TM programs with polynomial overhead, we see that we can simulate a $T(n)$ time NAND-RAM program on length $n$ inputs with a $poly(T(n))$ size NAND-CIRC program.

> ### { .pause }
To make sure you understand this transformation, it is an excellent exercise to verify the following equivalent characterization of the class $\mathbf{P}$ (see [Palternativeex](){.ref}). Prove that for every $F:\{0,1\}^* \rightarrow \{0,1\}$, $F\in \mathbf{P}$ if and only if there is a polynomial-time NAND-TM (or NAND-RAM, it doesn't matter) program $P$ such that for every $n\in \N$, $P(1^n)$ outputs a description of an $n$ input NAND-CIRC program $Q_n$ that computes the restriction $F_{\upharpoonright n}$ of $F$ to inputs in $\{0,1\}^n$. (Note that since $P$ runs in polynomial time and hence has an output of at most polynomial length, $Q_n$ has at most a polynomial number of lines.)

### The class $\mathbf{P_{/poly}}$

We can define the "non uniform" analog of the class $\mathbf{P}$ as follows:

> ### {.definition title="$\mathbf{P_{/poly}}$" #Ppoly}
For every $F:\{0,1\}^* \rightarrow \{0,1\}$, we say that $F\in \mathbf{P_{/poly}}$ if there is some polynomial $p:\N \rightarrow \R$ such that for every $n\in \N$, $F_{\upharpoonright n} \in SIZE(p(n))$ where $F_{\upharpoonright n}$ is the restriction of $F$ to inputs in $\{0,1\}^n$.

[non-uniform-thm](){.ref} implies that $\mathbf{P} \subseteq \mathbf{P_{/poly}}$.

::: { .pause }
Please make sure you understand why this is the case.
:::


Using the equivalence of NAND-CIRC programs and Boolean circuits, we can also define $\mathbf{P_{/poly}}$ as the class of functions $F:\{0,1\}^* \rightarrow \{0,1\}$  such that the restriction of $F$ to $\{0,1\}^n$ is computable by a Boolean circuit of $poly(n)$ size (say with gates in the set $\wedge,\vee,\neg$ though any universal gateset will do); see [Ppolyfig](){.ref}.

![We can think of an infinite function $F:\{0,1\}^* \rightarrow \{0,1\}$ as a collection of finite functions $F_0,F_1,F_2,\ldots$ where $F_{\upharpoonright n}:\{0,1\}^n \rightarrow \{0,1\}$ is the restriction of $F$ to inputs of length $n$. We say $F$ is in $\mathbf{P_{/poly}}$ if for every $n$, the function $F_{\upharpoonright n}$  is computable by a polynomial size NAND-CIRC program, or equivalently, a polynomial sized Boolean circuit. (We drop in this figure the "edge case" of $F_0$ though as a constant function, it can always be computed by a constant sized NAND-CIRC program.)](../figure/Ppoly.png){#Ppolyfig .margin  }

The notation $\mathbf{P_{/poly}}$ is used for historical reasons.
It was introduced by Karp and Lipton, who considered this class as corresponding to functions that can be computed by polynomial-time Turing Machines (or equivalently, NAND-TM programs) that are given for any input length $n$ a polynomial in $n$ long _advice string_.
That this is an equivalent characterization is shown in the following theorem:

::: {.theorem title="$\mathbf{P_{/poly}}$ characterization by advice" #ppolyadvice}
Let $F:\{0,1\}^* \rightarrow \{0,1\}$. Then $F\in\mathbf{P_{/poly}}$ if and only if there exists a polynomial $p:\N \rightarrow \N$, a polynomial-time NAND-TM program $P$ and a sequence $\{ a_n \}_{n\in \N}$ of strings, such that for every $n\in \N$:

* $|a_n| \leq p(n)$  \
* For every $x\in \{0,1\}^n$, $P(a_n,x)=F(x)$.
:::

::: {.proof data-ref="ppolyadvice"}
We only sketch the proof.
For the "only if" direction, if $F\in \mathbf{P_{/poly}}$ then we can use for $a_n$  simply the description of the corresponding NAND-CIRC program $Q_n$, and for $P$ the program that computes in polynomial time the $NANDEVAL$ function that on input an $n$-input NAND-CIRC program $Q$ and a string $x\in \{0,1\}^n$, outputs $Q(n)$.

For the "if" direction, we can use the same "unrolling the loop" technique of [non-uniform-thm](){.ref} to show that if $P$ is a polynomial-time NAND-TM program, then for every $n\in \N$, the map $x \mapsto P(a_n,x)$ can be computed by a polynomial size NAND-CIRC program $Q_n$.
:::

> ### { .pause }
To make sure you understand the definition of $\mathbf{P_{/poly}}$, I highly encourage you to work out fully the details of the proof of [ppolyadvice](){.ref}.


### Simulating NAND with NAND-TM?

[non-uniform-thm](){.ref} shows that every function in $TIME(T(n))$ is in $SIZE(poly(T(n)))$.
One can ask if there is an inverse relation.
Suppose that $F$ is such that $F_{\upharpoonright n}$ has a "short" NAND-CIRC program for every $n$.
Can we say that it must be in $TIME(T(n))$ for some "small" $T$?
The answer is an emphatic __no__.
Not only is $\mathbf{P_{/poly}}$ not contained in $\mathbf{P}$, in fact $\mathbf{P_{/poly}}$ contains functions that are _uncomputable_!


> ### {.theorem title="$\mathbf{P_{/poly}}$ contains uncomputable functions" #Ppolyuncomputable}
There exists an _uncomputable_ function $F:\{0,1\}^* \rightarrow \{0,1\}$ such that $F \in \mathbf{P_{/poly}}$.


> ### {.proofidea data-ref="PnewPpoly"}
Since $\mathbf{P_{/poly}}$ corresponds to non uniform computation, a function $F$ is in $\mathbf{P_{/poly}}$ if for every $n\in \N$, the restriction $F_{\upharpoonright n}$ to inputs of length $n$ has a small circuit/program, even if the circuits for different values of $n$ are completely different from one another. In particular, if $F$ has the property that for every equal-length inputs $x$ and $x'$, $F(x)=F(x')$ then this means that $F_{\upharpoonright n}$ is either the constant function zero or the constant function one for every $n\in \N$.
Since the constant function has a (very!) small circuit, such a function $F$ will always be in $\mathbf{P_{/poly}}$ (indeed even in smaller classes).
Yet by a reduction from the Halting problem, we can obtain a function with this property that is uncomputable.

::: {.proof data-ref="PnewPpoly"}
Consider the following "unary halting function" $UH:\{0,1\}^* \rightarrow \{0,1\}$ defined as follows.
We let $S:\N \rightarrow \{0,1\}^*$ be the function that on input $n\in \N$, outputs the string that corresponds to the binary representation of the number $n$ without the most significant $1$ digit.
Note that $S$ is _onto_.
For every $x\in \{0,1\}$, we define $UH(x)=HALTONZERO(S(|x|))$.
That is, if $n$ is the length of $x$, then $UH(x)=1$ if and only if the string $S(n)$ encodes a NAND-TM program that halts on the input $0$.


$UH$ is uncomputable, since otherwise we could compute $HALTONZERO$ by transforming the input program $P$ into the integer $n$ such that $P=S(n)$ and then running $UH(1^n)$ (i.e., $UH$ on the string of $n$ ones).
On the other hand, for every $n$, $UH_n(x)$ is either equal to $0$ for all inputs $x$ or equal to $1$ on all inputs $x$, and hence can be computed by a NAND-CIRC program of a _constant_ number of lines.
:::


The issue here is of course _uniformity_.
For a function $F:\{0,1\}^* \rightarrow \{0,1\}$, if $F$ is in $TIME(T(n))$ then we have a _single_ algorithm that can compute $F_{\upharpoonright n}$ for every $n$.
On the other hand,  $F_{\upharpoonright n}$ might be in  $SIZE(T(n))$ for every $n$ using a completely different algorithm for every input length.
For this reason we typically use $\mathbf{P_{/poly}}$ not as a model of _efficient_ computation but rather as a way to model _inefficient computation_.
For example, in cryptography people often define an encryption scheme to be secure if breaking it for a key of length $n$ requires more than a polynomial number of NAND lines.
Since $\mathbf{P} \subseteq \mathbf{P_{/poly}}$, this in particular precludes a polynomial time algorithm for doing so, but there are technical reasons why working in a non uniform model makes more sense in cryptography.
It also allows to talk about security in non asymptotic terms such as a scheme having "$128$ bits of security".

> ### {.remark title="Non uniformity in practice" #nonunif}
While it can sometimes be a real issue, in many natural settings the difference between uniform and non-uniform computation does not seem to so important.
In particular, in all the examples of problems not known to be in $\mathbf{P}$ we discussed before: longest path, 3SAT, factoring, etc., these problems are also not known to be in $\mathbf{P_{/poly}}$ either.
Thus, for "natural" functions, if you pretend that $TIME(T(n))$  is roughly the same as $SIZE(T(n))$, you will be right more often than wrong.





### Uniform vs. Nonuniform computation: A recap

To summarize, the two models of computation we have described so far are:

* NAND-CIRC programs, which have no loops, can only compute finite functions, and the time to execute them is exactly the number of lines they contain. These are also known as _straight-line programs_ or _Boolean circuits_.

* NAND-TM programs, which include loops, and hence a single program can compute a function with unbounded input length. These are equivalent (up to polynomial factors) to _Turing Machines_ or (up to polylogarithmic factors) to _RAM machines_.

For a function $F:\{0,1\}^* \rightarrow \{0,1\}$ and some nice time bound $T:\N \rightarrow \N$, we know that:

* If $F$ is computable in time $T(n)$ then there is a sequence $\{ P_n \}$ of NAND-CIRC programs with $|P_n| = poly(T(n))$ such that $P_n$ computes $F_{\upharpoonright n}$ (i.e., restriction of $F$ to $\{0,1\}^n$) for every $n$.

* The reverse direction is not necessarily true - there are examples of functions $F:\{0,1\}^n \rightarrow \{0,1\}$ such that $F_{\upharpoonright n}$ can be computed by even a constant size NAND-CIRC program but $F$ is uncomputable.

This means that non uniform complexity is more useful to establish _hardness_ of a function than its _easiness_.

## Extended Church-Turing Thesis { #ECTTsec }

We have mentioned the Church-Turing thesis, that posits that the definition of computable functions using NAND-TM programs captures the definition that would be obtained by all physically realizable computing devices.
The _extended_ Church Turing is the statement that the same holds for _efficiently computable_ functions, which is typically interpreted as saying that NAND-TM programs can simulate every physically realizable computing device with polynomial overhead.

In other words, the extended Church Turing thesis says that for every _scalable computing device_ $C$ (which has a finite description but can be in principle used to run computation on arbitrarily large inputs),  there are some constants $a,b$ such that for every function $F:\{0,1\}^* \rightarrow \{0,1\}$ that $C$ can compute on $n$ length inputs using an $S(n)$ amount of physical resources, $F$ is in $TIME(aS(n)^b)$.

All the current constructions of scalable computational models and programming language conform to the Extended Church-Turing Thesis, in the sense that they can be with polynomial overhead by Turing Machines (and hence also by NAND-TM or NAND-RAM programs).
consequently, the classes $\mathbf{P}$ and $\mathbf{EXP}$ are robust to the choice of model, and we can use the programming language of our choice, or high level descriptions of an algorithm, to determine whether or not a problem is in $\mathbf{P}$.

Like the Church-Turing thesis itself, the extended Church-Turing thesis is in the asymptotic setting and does not directly yield an experimentally testable prediction.
However, it can be instantiated with more concrete bounds on the overhead, which would yield predictions such as the _Physical Extended Church-Turing Thesis_   we mentioned before, which would be experimentally testable.

In the last hundred+ years of studying and mechanizing computation, no one has yet constructed a scalable computing device (or even gave a convincing blueprint) that violates the extended Church Turing Thesis.
However,    _quantum computing_, if realized, will pose a serious challenge to this thesis.^[Large scale quantum computers have not yet been built, and even if they are constructed, we have no _proof_ that they would offer super polynomial advantage over "classical" computing devices. However, there seems to be no fundamental physical obstacle to constructing them, and there are strong reasons to conjecture that they do in fact offer such an advantage.]
However, even if the promises of quantum computing are fully realized, the extended Church-Turing thesis is  "morally" correct, in the sense that, while we do need to adapt the thesis to account for the possibility of quantum computing, its broad outline remains unchanged.
We are still able to model computation mathematically, we can still treat programs as strings and have a universal program,  and we still have hierarchy and uncomputability results.^[Quantum computing is _not_ a challenge to the (non extended) Church Turing thesis, as a function is computable by a quantum computer if and only if it is computable by a "classical" computer or a NAND-TM program. It is only the running time of computing the function that can be affected by moving to the quantum model. ]
Moreover, for most (though not all!) concrete problems we care about, the prospect of quantum computing does not seem to change their time complexity.
In particular, out of all the example problems mentioned in [chapefficient](){.ref}, as far as we know, the complexity of only one--- integer factoring--- is affected by modifying our model to include quantum computers as well.



::: { .recap }
* We can define the time complexity of a function using NAND-TM programs, and similarly to the notion of computability, this appears to capture the inherent complexity of the function.

* There are many natural problems that have polynomial-time algorithms, and other natural problems that we'd love to solve, but for which the best known algorithms are exponential.

* The definition of polynomial time, and hence the class $\mathbf{P}$, is robust to the choice of model, whether it is Turing machines, NAND-TM, NAND-RAM, modern programming languages, and many other models.

* The time hierarchy theorem shows that there are _some_ problems that can be solved in exponential, but not in polynomial time. However, we do not know if that is the case for the natural examples that we described in this lecture.

* By "unrolling the loop" we can show that every function computable in time $T(n)$ can be computed by a sequence of NAND-CIRC programs (one for every input length) each of size at most $poly(T(n))$
:::


## Exercises


::: {.exercise title="Equivalence of different definitions of $\mathbf{P}$ and $\mathbf{EXP}$." #definitionofP}
Prove that the classes $\mathbf{P}$ and $\mathbf{EXP}$ defined in [PandEXPdef](){.ref} are equal to $\cup_{c\in \{1,2,3,\ldots \}} TIME(n^c)$ and $\cup_{c\in \{1,2,3,\ldots \}} TIME(2^{n^c})$ respectively.
(If $S_1,S_2,S_3,\ldots$ is a collection of sets then the set $S = \cup_{c\in \{1,2,3,\ldots \}} S_c$ is the set of all elements $e$ such that there exists some $c\in \{ 1,2,3,\ldots \}$ where $e\in S_c$.)
:::





::: {.exercise title="Boolean functions" #boolex}
For every function $F:\{0,1\}^* \rightarrow \{0,1\}^*$, define $Bool(F)$ to be the function mapping $\{0,1\}^*$ to $\{0,1\}$ such that on input a (string representation of a) triple $(x,i,\sigma)$ with $x\in \{0,1\}^*$, $i \in \N$ and $\sigma \in \{0,1\}$,

$$
Bool(F)(x,i,\sigma) = \begin{cases} F(x)_i & \sigma =0, i<|F(x)| \\
                                    1      & \sigma = 1,i<|F(x)| \\
                                 0   & \text{otherwise} \end{cases}
$$
where $F(x)_i$ is the $i$-th bit of the string $F(x)$.

Prove that $F \in \overline{\mathbf{P}}$ if and only if $Bool(F) \in \mathbf{P}$.
:::


> ### {.exercise title="Composition of polynomial time" #poly-time-comp-ex}
Prove that if $F,G:\{0,1\}^* \rightarrow \{0,1\}^*$ are in $\overline{\mathbf{P}}$ then their _composition_ $F\circ G$, which is the function $H$ s.t. $H(x)=F(G(x))$, is also in $\overline{\mathbf{P}}$.


> ### {.exercise title="Non composition of exponential time" #exp-time-comp-ex}
Prove that there is some $F,G:\{0,1\}^* \rightarrow \{0,1\}^*$ s.t. $F,G \in \overline{\mathbf{EXP}}$ but $F\circ G$ is not in $\mathbf{EXP}$.


> ### {.exercise title="Oblivious program" #oblivious-ex}
We say that a NAND-TM program $P$ is oblivious if there is some functions $T:\N \rightarrow \N$ and $i:\N\times \N \rightarrow \N$ such that for every input $x$ of length $n$, it holds that:\
* $P$ halts when given input $x$  after exactly $T(n)$ steps. \
* For $t\in \{1,\ldots, T(n) \}$, after $P$ executes the $t^{th}$ step of the execution the value of the index `i` is equal to $t(n,i)$. In particular this value does _not_ depend on $x$ but only on its length.^[An oblivious program $P$ cannot compute functions whose output length is not a function of the input length, though this is not a real restriction, as we can always embed variable output functions in fixed length ones using some special "end of output" marker.]
Let $F:\{0,1\}^* \rightarrow \{0,1\}^*$ be such that there is some function $m:\N \rightarrow \N$ satisfying $|F(x)|=m(|x|)$ for every $x$, and let $P$ be a NAND-TM program that computes $F$ in $T(n)$ time for some nice $T$.
Then there is an _oblivious_ NAND-TM program $P'$ that computes $F$ in time $O(T^2(n) \log T(n))$.

> ### {.exercise title="Alternative characterization of $\mathbf{P}$" #Palternativeex}
Prove that for every $F:\{0,1\}^* \rightarrow \{0,1\}$, $F\in \mathbf{P}$ if and only if there exists a polynomial time NAND-TM program $P$ such that $P(1^n)$ outputs a NAND-CIRC program  $Q_n$ that computes the restriction of $F$ to $\{0,1\}^n$.

::: {.exercise  #graphedgeex}
Let $EDGE:\{0,1\}^* \rightarrow \{0,1\}$ be the function such that on input a string representing a triple $(L,i,j)$, where $L$ is the adjacency list representation of an $n$ vertex graph $G$, and $i$ and $j$ are numbers in $[n]$, $EDGE(L,i,j)=1$ if the edge $\{i,j \}$ is present in the graph. $EDGE$ outputs $0$ on all other inputs.

1. Prove that $EDGE \in \mathbf{P}$.


2. Let $PLANARMATRIX:\{0,1\}^* \rightarrow \{0,1\}$ be the function that on input an adjacency matrix $A$ outputs $1$ if and only if the graph represented by $A$ is _planar_ (that is, can be drawn on the plane without edges crossing one another). For this question, you can use without proof the fact that $PLANARMATRIX \in \mathbf{P}$. Prove that $PLANARLIST \in \mathbf{P}$ where $PLANARLIST:\{0,1\}^* \rightarrow \{0,1\}$ is the function that on input an adjacency list $L$ outputs $1$ if and only if $L$ represents a planar graph.
:::


::: {.exercise title="Evaluate NAND circuits" #evalnandcircuit}
Let $NANDEVAL:\{0,1\}^* \rightarrow \{0,1\}$ be the function such that for every string representing a pair $(Q,x)$ where $Q$ is an $n$-input $1$-output
NAND-CIRC (not NAND-TM!) program  and $x\in \{0,1\}^n$, $NANDEVAL(Q,x)=Q(x)$.  On all other inputs $NANDEVAL$ outputs $0$.

Prove that $NANDEVAL \in \mathbf{P}$.
:::

::: {.exercise title="Find hard function" #hardfunc}
Let $NANDHARD:\{0,1\}^* \rightarrow \{0,1\}$ be the function such that on input a string representing a  pair $(f,s)$ where

* $f \in \{0,1\}^{2^n}$ for some $n\in \mathbb{N}$
* $s\in \mathbb{N}$

$NANDHARD(f,s)=1$ if there is no NAND-CIRC program $Q$ of at most $s$ lines that computes the function $F:\{0,1\}^n \rightarrow \{0,1\}$ whose truth table is the string $f$.
That is, $NANDHARD(f,s)=1$ if for every NAND-CIRC program $Q$ of at most $s$ lines, there exists some $x\in \{0,1\}^{n}$ such that $Q(x) \neq f_x$ where $f_x$ denote the $x$-the coordinate of $f$, using the binary representation to identify $\{0,1\}^n$ with the numbers $\{0,\ldots,2^n -1 \}$.

1. Prove that $NANDHARD \in \mathbf{EXP}$.

2. (Challenge) Prove that there is an algorithm $FINDHARD$ such that if $n$ is sufficiently large, then $FINDHARD(1^n)$ runs in time $2^{2^{O(n)}}$ and outputs a string $f \in \{0,1\}^{2^n}$ that is the truth table of a function that is not contained in  $SIZE(2^n/(1000n))$. (In other words, if $f$ is the string output by $FINDHARD(1^n)$ then if we let $F:\{0,1\}^n \rightarrow \{0,1\}$ be the function such that $F(x)$ outputs the $x$-th coordinate of $f$, then $F\not\in SIZE(2^n/(1000n))$.^[__Hint:__ Use Item 1, the existence of functions requiring exponentially hard NAND programs, and the fact that there are only finitely many functions mapping $\{0,1\}^n$ to $\{0,1\}$.]
:::





::: {.exercise  #scheduleprogex}
Suppose that you are in charge of scheduling courses  in computer science in University X. In University X, computer science students wake up late, and have to work on their startups in the afternoon, and take long weekends with their investors. So you only have two possible slots: you can schedule a course either Monday-Wednesday 11am-1pm or Tuesday-Thursday 11am-1pm.


Let $SCHEDULE:\{0,1\}^* \rightarrow \{0,1\}$ be the function that takes as input a list of courses $L$ and a list of _conflicts_ $C$ (i.e., list of pairs of courses that cannot share the same time slot) and outputs  $1$ if and only if there is a "conflict free" scheduling of the courses in $L$, where no pair in $C$ is scheduled in the same time slot.

More precisely, the list $L$ is a list of strings $(c_0,\ldots,c_{n-1})$ and the list $C$ is a list of pairs of the form $(c_i,c_j)$. $SCHEDULE(L,C)=1$ if and only if there exists partition of $c_0,\ldots,c_{n-1}$ into two parts so that there is no pair $(c_i,c_j) \in C$ such that both $c_i$ and $c_j$ are in the same part.

Prove that $SCHEDULE \in \mathbf{P}$.  As usual, you do not have to provide the full code to show that this is the case, and can describe operations as a high level, as well as appeal to any data structures or other results mentioned in the book or in lecture. Note that to show that a function $F$ is in $\mathbf{P}$ you need to both __(1)__ present an algorithm $A$ that computes $F$ in polynomial time, __(2)__ _prove_ that $A$ does indeed run in polynomial time, and does indeed compute the correct answer.

Remark also whether or not your algorithm easily extends to the case where there are _three_ possible time slots.
:::




## Bibliographical notes {#bibnotesrunningtime }

Some lower bounds for single-tape Turing machines are given in [@maass1985combinatorial].

For defining efficiency in the  $\lambda$ calculus, one needs to be careful about the order of application of the reduction steps, which can matter for computational efficiency, see for example [this paper](https://lmcs.episciences.org/1627).



## Further explorations

Some topics related to this chapter that might be accessible to advanced students include: (to be completed)


## Acknowledgements

<!---
## Appendix: Making NAND-TM programs oblivious

^[TODO: possibly remove this]

> ### {.proof data-ref="oblivious-thm"}
We start by ensuring that the time at which the program halts does not depend on the input but only its length. To do so, we can transform a program running in $T(n)$ time to a "clocked" version that will always takes $T(n)$ steps regardless of the input.
We achieve this by adding a `noop` variable and modify the program to do nothing if `noop` equals $1$.
Hence, when the original program would assign $0$ to `loop`, we modify `noop` to $1$, and only halt after $T(|x|)$ steps when $x$ is the input.
>
The heart of the proof of [oblivious-thm](){.ref} is to ensure that movements of the index `i` only depend on the input length.
Our approach is analogous to replacing a taxi by a bus.
Instead of the program controlling to where `i` goes, the index will go obliviously on its route, and we will wait until it reaches the desired location.
That is, regardless of the input the index `i` will progress between every iteration of the main loop according to the sequence
$$
0,1,0,1,2,1,0,1,2,3,2,1,0,1,\ldots \label{eq:pattern}
$$
>
>![We simulate a NAND-TM program by an oblivious program in which the index moves according to the pattern of [eq:pattern](){.eqref}.](../figure/oblivious_simulation.png){#oblivious-fig .margin  }
>
That is, `i` will sweep back and forth from index $0$ till the current last index $n$, which will be incremented every round, see [oblivious-fig](){.ref}.
In the worst case, in every step we want to decrease `i`  when we are at an "upward sweep", and increase `i` when we are in a "downward sweep", but because the value of `i` is always between $0$ and the current step $t$, we can always achieve the desired value within the next sweep. This means that to make $t$ steps, at the worst case we will need to complete $t$ full back-and-forth sweeps. The total number of movements in these sweeps will be  $2 + 4 + 6 + \ldots + 2t = O(t^2)$ steps, and with an $O(\log t)$ overhead, we can keep track of which step we are in at the computation, and compare the current value of `i` with the desired value.

### Getting to $O(T \log T)$.

^[TODO: To be completed, use the appropriate data structure]
---->
