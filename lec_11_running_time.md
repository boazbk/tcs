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



![Overview of the results of this chapter.](../figure/runtimeoverview.png){#runtimeoverviewfig}

In this chapter we formally define the notion of a function being computable in $T(n)$ time where $T$ is some function mapping the length of the input to a bound on the number of computation steps.
We then do the following (see also [runtimeoverviewfig](){.ref}):

* Define the class $\mathbf{P}$ of Boolean functions that can be computed in polynomial time and its superset $\mathbf{EXP}$ of functions that can be computed in exponential time. 

* Show that the time to compute a function using a Turing Machine and using a RAM machine (or NAND-RAM program) is _polynomially related_ which in particular means that the classes $\mathbf{P}$ and $\mathbf{EXP}$ can be equivalently defined using either Turing Machines or RAM machines / NAND-RAM programs.

* Give an _efficient_ universal NAND-RAM program and use this to establish the _time hierarchy theorem_ that in particular implies that $\mathbf{P} \subsetneq \mathbf{EXP}$. 

* We relate the notions defined here to the _non uniform_ models of  Boolean circuits and NAND-CIRC programs defined in [compchap](){.ref}. We define $\mathbf{P_{/poly}}$ to be the class of functins computed by a _sequence_ of polynomial-sized circuits. We prove that $\mathbf{P} \subseteq \mathbf{P_{/poly}}$ and that $\mathbf{P_{/poly}}$ contains _uncomputable_ functions.





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



::: {.solvedexercise title="Example of time bounds" #timeboundexample}
Prove that $TIME_{\mathsf{TM}}(10\cdot n^3) \subseteq TIME_{\mathsf{TM}}(2^n)$.
:::

![Comparing $T(n)=10n^3$ with $T'(n) = 2^n$ (on the right figure the Y axis is in log scale). Since for every large enough $n$, $T'(n) \geq T(n)$, $TIME_{\mathsf{TM}}(T(n)) \subseteq TIME_{\mathsf{TM}}(T'(n))$.](../figure/exampletimebounds.png){#examplefimeboundsfig .margin}

::: {.solution data-ref="timeboundexample"}
The proof is illustrated in [examplefimeboundsfig](){.ref}.
Suppose that $F\in TIME_{\mathsf{TM}}(10\cdot n^3)$ and hence there some number $N_0$ and a machine $M$ such that for every $n> N_0$,  and $x\in \{0,1\}^*$, $M(x)$ outputs $F(x)$ within at most $10\cdot n^3$ steps.
Since $10\cdot n^3 = o(2^n)$, there is some number $N_1$ such that for every $n>N_1$, $10\cdot n^3 < 2^n$.
Hence for every $n > \max\{ N_0, N_1 \}$, $M(x)$ will output $F(x)$ within at most $2^n$ steps, just demonstrating that $F \in TIME_{\mathsf{TM}}(2^n)$.
:::






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


| $\mathbf{P}$             | $\mathbf{EXP}$ (but not known to be in $\mathbf{P}$) |
|--------------------------|---------------------------|
| Shortest path            | Longest Path              |
| Min cut                  | Max cut                   |
| 2SAT                     | 3SAT                      |
| Linear eqs               | Quad. eqs                 |
| Zerosum                  | Nash                      |
| Determinant              | Permanent                 |
| Primality                | Factoring                 |

Table : A table of the examples from [chapefficient](){.ref}. All these problems are in $\mathbf{EXP}$ but the only the ones on the left column are currently known to be in $\mathbf{P}$ as well (i.e., they have a polynomial-time algorithm). See also [PvsEXPfig](){.ref}.


![Some examples of problems that are known to be in $\mathbf{P}$ and problems that are known to be in $\mathbf{EXP}$ but not known whether or not they are in $\mathbf{P}$. Since both $\mathbf{P}$ and $\mathbf{EXP}$ are classes of Boolean functions, in this figure we always refer to the _Boolean_ (i.e., Yes/No) variant of the problems.](../figure/PvsEXP.png){#PvsEXPfig .margin}

::: {.remark title="Boolean versions of problems" #booleanversion}
Many of the problems defined in [chapefficient](){.ref}]() correspond to _non Boolean_ functions (functions with more than one bit of output) while $\mathbf{P}$ and $\mathbf{EXP}$ are sets of Boolean functions. However, for every non-Boolean function $F$ we can always define a computationally-equivalent Boolean function $G$ by letting $G(x,i)$ be the $i$-th bit of $F(x)$ (see [boolex](){.ref}).
Hence the table above, as well as [PvsEXPfig](){.ref}, refer to the computationally-equivalent Boolean variants of these problems.
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
The reason is that Turing Machines can simulate NAND-RAM programs with at most a polynomial overhead (see also [RAMTMsimulationfig](){.ref}):


::: {.theorem title="Relating RAM and Turing machines" #polyRAMTM-thm}
Let $T:\N \rightarrow \N$ be a function such that $T(n) \geq n$ for every $n$ and the map $n \mapsto T(n)$ can be computed by a Turing machine in time $O(T(n)^3)$.
Then 
$$
TIME_{\mathsf{TM}}(T(n)) \subseteq TIME_{\mathsf{RAM}}(T(n)) \subseteq TIME_{\mathsf{TM}}(T(n)^4) \;.
$$
:::

![The proof of [polyRAMTM-thm](){.ref} shows that we can simulate $T$ steps of a Turing Machine with $T$ steps of a NAND-RAM program, and can simulate $T$ steps of a NAND-RAM program with $o(T^4)$ steps of a Turing Machine. Hence $TIME_{\mathsf{TM}}(T(n)) \subseteq TIME_{\mathsf{RAM}}(T(n)) \subseteq TIME_{\mathsf{TM}}(T(n)^4)$.](../figure/RAMTMsimulation.png){#RAMTMsimulationfig .margin}

::: { .bigidea #polyvsnot}
While the precise definition of running time can depend on the computational model, as long as we only care about the distinction between polynomial and exponential, all the models we considered are equivalent to each other. 
:::


All non pathological time bound functions such as $T(n)=n$, $T(n)n\log n$, $T(n)=2^n$ etc. satisfy the conditions of  [polyRAMTM-thm](){.ref}, see also [nicefunctionsrem](){.ref}.
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










::: {.remark title="Nice time bounds" #nicefunctionsrem}
When considering general time bounds such we need to make sure to rule out some "pathological" cases such as functions $T$ that don't give enough time for the algorithm to read the input, or functions where the time bound itself is uncomputable. We say that a function $T:\N \rightarrow \N$ is a  _nice time bound function_ (or nice function for short) if for every $n\in \N$, $T(n) \geq n$ (i.e., $T$ allows enough time to read the input), for every $n' \geq n$, $T(n') \geq T(n)$ (i.e., $T$ allows more time on longer inputs), and the map $F(x) = 1^{T(|x|)}$  (i.e., mapping a string of length $n$ to a sequence of $T(n)$ ones) can be computed by a NAND-RAM program in $O(T(n))$ time.

All the "normal" time complexity bounds we encounter in applications such as $T(n)= 100 n$, $T(n) =  n^2 \log n$,$T(n) = 2^{\sqrt{n}}$, etc.  are "nice".
Hence from now on we will only care about the class $TIME(T(n))$   when $T$ is a "nice" function.
The computability condition is in particular typically easily satisfied.
For example, for arithmetic functions such as $T(n) = n^3$, we can typically compute the binary representation of $T(n)$ in time polynomial _in the number of bits_ of $T(n)$ and hence poly-logarithmic in $T(n)$.
Hence the time to write the string $1^{T(n)}$ in such cases will be $T(n) + poly(\log T(n)) = O(T(n))$.
:::


## Extended Church-Turing Thesis (discussion) { #ECTTsec }

[polyRAMTM-thm](){.ref} shows that the computational models of _Turing Machines_ and _RAM Machines / NAND-RAM programs_ are equivalent up to polynomial factors in the running time.
Other examples of polynmially equivalent models include:

* All standard programming languages, including C/Python/JavaScript/Lisp/etc.

* The $\lambda$ calculus (see also [bibnotesrunningtime](){.ref}).

* Cellular automata

* Parallel computers

* Biological computing devices such as DNA-based computers.


The _Extended Church Turing Thesis_ is the statement this is true for all physically realizable computing models. 
In other words, the extended Church Turing thesis says that for every _scalable computing device_ $C$ (which has a finite description but can be in principle used to run computation on arbitrarily large inputs),  there is some constant $a$  such that for every function $F:\{0,1\}^* \rightarrow \{0,1\}$ that $C$ can compute on $n$ length inputs using an $S(n)$ amount of physical resources, $F$ is in $TIME(S(n)^a)$.
This is a strengthening of the ("plain") Church-Turing Thesis, discussed in [churchturingdiscussionsec](){.ref}, which states that the set of computable functions is the same for all physically realizable models, but without requiring the overhead in the simulation between different models to be at most polynomial.

All the current constructions of scalable computational models and programming language conform to the Extended Church-Turing Thesis, in the sense that they can be with polynomial overhead by Turing Machines (and hence also by NAND-TM or NAND-RAM programs).
consequently, the classes $\mathbf{P}$ and $\mathbf{EXP}$ are robust to the choice of model, and we can use the programming language of our choice, or high level descriptions of an algorithm, to determine whether or not a problem is in $\mathbf{P}$.

Like the Church-Turing thesis itself, the extended Church-Turing thesis is in the asymptotic setting and does not directly yield an experimentally testable prediction.
However, it can be instantiated with more concrete bounds on the overhead, yielding experimentally-testable predictions such as the _Physical Extended Church-Turing Thesis_   we mentioned in [PECTTsec](){.ref}.

In the last hundred+ years of studying and mechanizing computation, no one has yet constructed a scalable computing device (or even gave a convincing blueprint) that violates the extended Church Turing Thesis.
However,    _quantum computing_, if realized, will pose a serious challenge to the extended Church-Turing Thesis (see [quantumchap](){.ref}).
However, even if the promises of quantum computing are fully realized, the extended Church-Turing thesis is  "morally" correct, in the sense that, while we do need to adapt the thesis to account for the possibility of quantum computing, its broad outline remains unchanged.
We are still able to model computation mathematically, we can still treat programs as strings and have a universal program,   we still have hierarchy and uncomputability results, and there is still no reason to doubt the ("plain") Church-Turing thesis.
Moreover,  the prospect of quantum computing does not seem to make a difference for the time complexity of many  (though not all!) of the concrete problems that we care about.
In particular, out of all the example problems mentioned in [chapefficient](){.ref}, as far as we know, the complexity of only one--- integer factoring--- is affected by modifying our model to include quantum computers as well.












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

To be a little more concrete, here is some "pseudocode" description of the program $U$:

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



## The time hierarchy theorem

Some functions are _uncomputable_,  but are there functions that can be computed, but only at an exorbitant cost?
For example, is there a function that _can_ be computed in time $2^n$, but _can not_ be computed in time $2^{0.9 n}$?
It turns out that the answer is __Yes__:

> ### {.theorem title="Time Hierarchy Theorem" #time-hierarchy-thm}
For every nice function $T$, there is a function $F:\{0,1\}^* \rightarrow \{0,1\}$
in $TIME(T(n)\log n) \setminus TIME(T(n))$.

There is nothing special about $\log n$, and we could have used any other efficiently computable function that tends to infinity with $n$.



![The _Time Hierarchy Theorem_ ([time-hierarchy-thm](){.ref}) states that all of these classes are _distinct_.](../figure/timehierarchythm.png){#timehierarchythmfig}


> ### {.proofidea data-ref="time-hierarchy-thm"}
In the proof of [halt-thm](){.ref} (the uncomputability of the Halting problem), we have shown that the function $HALT$ cannot be computed in any finite time. An examination of the proof shows that it gives something stronger.
Namely, the proof shows that if we fix our computational budget to be $T$ steps, then not only we can't distinguish between programs that halt and those that do not, but cannot even distinguish between programs that halt within at most $T'$ steps and those that take more than that (where $T'$ is some number depending on $T$).
Therefore, the proof of [time-hierarchy-thm](){.ref} follows the ideas of the uncomputability of the halting problem, but again with a more careful accounting of the running time.



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

1. If $z$ does not have the form $z=P1^m$ where $P$ represents a NAND-RAM program and $|P|< 0.1 \log\log m$ then return $0$. (Recall that $1^m$ denotes the string of $m$ ones.)

2. Compute $b= P^*(P,z)$ (at a cost of at most $T(|P|+|z|)$ steps, under our assumptions).

3. If $b=1$ then $Q$ goes into an infinite loop, otherwise it halts.

We chose $m$ sufficiently large so that $|Q| < 0.001\log\log m$ where $|Q|$ denotes the length of the description of $Q$ as a string. We will reach a contradiction by splitting into cases according to whether or not $HALT_T(Q,Q1^m)$ equals $0$ or $1$.


On the one hand, if $HALT_T(Q,Q1^m)=1$, then under our assumption that $P^*$ computes $HALT_T$, $Q$ will go into an infinite loop on input $z=Q1^m$, and hence in particular $Q$ does _not_ halt within $100 T(|Q|+m)$ steps on the input $z$. But this contradicts our assumption that $HALT_T(Q,Q1^m)=1$.

This means that it must hold that $HALT_T(Q,Q1^m)=0$. But in this case, since we assume $P^*$ computes $HALT_T$, $Q$ does not do anything in phase 3 of its computation, and so the only computation costs come in phases 1 and 2 of the computation.
It is not hard to verify that Phase 1 can be done in linear and in fact less than $5|z|$ steps.
Phase 2 involves executing $P^*$, which under our assumption requires $T(|Q|+m)$ steps.
In total we can perform both phases in less than $10 T(|Q|+m)$ in steps, which by definition means that $HALT_T(Q,Q1^m)=1$, but this is of course a contradiction. This completes the proof of Claim 2 and hence of [time-hierarchy-thm](){.ref}.
:::

::: {.solvedexercise title="$\mathbf{P}$ vs $\mathbf{EXP}$" #PvsEXPexercise}
Prove that $\mathbf{P} \subsetneq \mathbf{EXP}$.
:::

::: {.solution data-ref="PvsEXP"}
We need to show that there exists $F \in \mathbf{EXP} \setminus \mathbf{P}$.
Let $T(n) = n^{\log n}$ and $T'(n) = n^{\log n / 2}$.
Both are nice functions.
Since $T(n)/T'(n) = \omega(\log n)$, by the time hierarchy theorem, there exists some $F$ in $TIME(T'(n)) \subsetneq TIME(T(n))$.
Since for sufficiently large $n$, $2^n > n^{\log n}$,  $F \in TIME(2^n) \subseteq \mathbf{EXP}$.
On the other hand, $F \not\in \mathbf{P}$. Indeed, suppose otherwise that there was a constant $c>0$ and a  Turing Machine computing $F$ on $n$-length input in at most $n^c$ steps for all sufficiently large $n$. Then since for $n$ large enough $n^c < n^{\log n/2}$, it would have followed that $F \in TIME(n^{\log n /2})$ contradicting our choice of $F$.
:::



The time hierarchy theorem tells us that there are functions we can compute in $O(n^2)$ time but not $O(n)$, in $2^n$ time, but not $2^{\sqrt{n}}$, etc..
In particular there are most definitely functions that we can compute in time $2^n$ but not $O(n)$.
We have seen that we have no shortage of natural functions for which the best _known_ algorithm requires roughly $2^n$ time, and that many people have invested significant effort in trying to improve that.
However,  unlike in the finite vs. infinite case, for all of the examples above at the moment we do not know how to rule out even an $O(n)$ time algorithm.
We will however see that there is a single unproven conjecture that would imply such a result for most of these problems.

![Some complexity classes and some of the functions we know (or conjecture) to be contained in them.](../figure/time_complexity_map.png){#complexityclassinclusionfig .margin  }



The time hierarchy theorem relies on the existence of an efficient universal NAND-RAM program, as proven in [univ-nandpp](){.ref}.
For other models such as Turing Machines we have similar time hierarchy results showing that there are functions computable in time $T(n)$ and not in time $T(n)/f(n)$ where $f(n)$ corresponds to the overhead in the corresponding universal machine. 


## Non uniform computation {#nonuniformcompsec }



We have now seen two measures of "computation cost" for functions.
In [secdefinesizeclasses](){.ref} we defined the complexity of computing _finite_ functions using circuits / straightline programs.
Specifically,  for a finite function $g:\{0,1\}^n \rightarrow \{0,1\}$ and number $T\in \N$,  $g\in SIZE(T)$ if there is circuit of at most $T$ NAND gates (or equivalently  a $T$-line NAND-CIRC program) that computes $g$.
To relate this to the classes $TIME(T(n))$ defined in this chapter we first need to extend the class $SIZE(T(n))$ from finite functions to functions with unbounded input length.

::: {.definition title="Non uniform computation" #nonuniformdef}
Let $F:\{0,1\}^* \rightarrow \{0,1\}$ and $T:\N \rightarrow \N$ be a nice time bound.
For every $n\in \N$, define $F_{\upharpoonright n} : \{0,1\}^n \rightarrow \{0,1\}$ to be the _restriction_ of $F$ to inputs of size $n$. That is, $F_{\upharpoonright n}$ is the function mapping $\{0,1\}^n$ to $\{0,1\}$ such that for every $x\in \{0,1\}^n$, F_{\upharpoonright n}(x)=F(x)$.

We say that $F$ is _non-uniformly computable in at most $T(n)$ size_, denoted by $F \in SIZE(T(n))$ if there exists a sequence $(C_0,C_1,C_2,\ldots)$ of NAND circuits such that:

* For every $n\in \N$, $C_n$ computes the function $F_{\upharpoonright n}$

* For every sufficiently large $n$, $C_n$ has at most $T(n)$ gates.
:::

The non uniform analog to the class $\mathbf{P}$ is the class $\mathbf{P_{/poly}}$ defined as 

$$
\mathbf{P_{/poly}} = \cup_{c\in \N} SIZE(n^c)  \; . \label{eqppolydef}
$$
There is a big difference between non uniform computation and uniform complexity classes such as $TIME(T(n))$ or $\mathbf{P}$.
The condition $F\in \mathbf{P}$ means that there is a _single_ Turing machine $M$ that computes $F$ on all inputs in polynomial time.
The condition $F\in \mathbf{P_{/poly}}$ only means that for every input length $n$ there can be a _different_ circuit $C_n$ that computes $F$ using polynomially many gates on inputs of these lengths.
As we will see, $F\in \mathbf{P_{/poly}}$ does not necessarily imply that $F\in \mathbf{P}$.
However, the other direction is true:

![We can think of an infinite function $F:\{0,1\}^* \rightarrow \{0,1\}$ as a collection of finite functions $F_0,F_1,F_2,\ldots$ where $F_{\upharpoonright n}:\{0,1\}^n \rightarrow \{0,1\}$ is the restriction of $F$ to inputs of length $n$. We say $F$ is in $\mathbf{P_{/poly}}$ if for every $n$, the function $F_{\upharpoonright n}$  is computable by a polynomial size NAND-CIRC program, or equivalently, a polynomial sized Boolean circuit.](../figure/Ppoly.png){#Ppolyfig .margin  }


::: {.theorem title="Nonuniform computation contains uniform computation" #non-uniform-thm}
There is some $a\in \N$ s.t. for every nice $T:\N \rightarrow \N$ and  $F:\{0,1\}^* \rightarrow \{0,1\}$,
$$TIME(T(n)) \subseteq SIZE(T(n)^a)\;.$$
:::

In particular,  [non-uniform-thm](){.ref} shows that for every $c$, $TIME(n^c) \subseteq SIZE(n^{ca})$ and hence $\mathbf{P} \subseteq \mathbf{P_{/poly}}$.



::: {.proofidea data-ref="non-uniform-thm"}
The idea behind the proof is to "unroll the loop".
Specifically, we will use the programming language variants of non-uniform and uniform computation: namely NAND-CIRC and NAND-TM. 
The main difference between the two is that NAND-TM has _loops_. However, for every fixed $n$, if we know that a NAND-TM program runs in at most $T(n)$ steps, then we can replace its loop by simply "copying and pasting" its code $T(n)$ times, similar to how in Python we can replace code such as

```python
for i in range(4):
    print(i)
```

with the "loop free" code

```python
print(0)
print(1)
print(2)
print(3)
```

To make this idea into an actual proof we need to tackle one technical difficulty, and this is to ensure that the NAND-TM program is _oblivious_ in the sense that the value of the index variable `i`  in the $j$-th iteration of the loop will depend only on $j$ and not on the contents of the input. We make a digression to do just that in [obliviousnandtm](){.ref} and then complete the proof  of [non-uniform-thm](){.ref}.
:::


### Oblivious NAND-TM programs  {#obliviousnandtm }

Our idea to prove [non-uniform-thm](){.ref} involves "unrolling the loop". 
That is, suppose that $P$ is a NAND-TM program of $k$ lines of the form

```python
line_1
...
line_(k-1)
MODANDJMP(dir1,dir2)
```

and such that on every input $x\in \{0,1\}^n$, $P$ runs for at most $T(n)$ iterations and returns the value $F(x)$.

We would want to transform it into a NAND-CIRC program for computing the finite  function $F_{\upharpoonright n}$ by simply dropping the last line "copying and pasting" $T(n)$ copies of the first $k-1$ lines.
However, we still need to decide what to do with arrays.
Since  the index variable `i` can move at most one step per iteration, it will never reach more than $T(n)-1$ on inputs of length $n$.
Hence we can replace an array `Foo` with $T=T(n)$ scalar variables `foo_0` , $\ldots$, `foo_`$(T-1)$.
Now we would want to replace references to `Foo[i]` in the original NAND-TM program with references to a variable of the form `foo_`$k$ for some number $k$ in the new NAND-CIRC program.
We could do that if the original NAND-TM program $P$ had the property that in its $j$-th iteration, the value of the index variable `i` is always equal to the same number $k$, regardless of what was the input.
This would mean that when we obtain a NAND-CIRC program by taking  $T(n)-1$ copies  of $P$, we can replace all references of the form `Foo[i]` in the $j$-th copy with references to `foo_`$k$.
A NAND-TM program with this property is called _oblivious_ and we now show that it is possible to transform every NAND-TM program into one that is oblivious.

> ### {.theorem title="Making NAND-TM oblivious" #obliviousnandtmthm}
Let $T:\N \rightarrow \N$ be a nice function and let $F\in TIME_{\mathsf{TM}}(T(n))$.
Then there is a NAND-TM program  $P$ that computes $F$ in $O(T(n)^2)$ steps and satisfying the following.
For every $n\in \N$ there is  a sequence $i_0,i_1,\ldots, i_{m-1}$ such that for every $x\in \{0,1\}^n$, if $P$ is executed on input $x$ then in the  $j$-th iteration  the variable `i` is equal to $i_j$.

In other words, [obliviousnandtmthm](){.ref} implies that if we can compute $F$ in $T(n)$ steps, then we can compute it in $O(T(n)^2)$ steps with a program $P$ in which the position of `i` in the $j$-th iteration depends only on $j$ and the length of the input, and not on the contents of the input.
Such a program can be easily translated into a NAND-CIRC program of $O(T(n)^2)$ lines by "unrolling the loop".

> ### {.proofidea data-ref="obliviousnandtmthm"}
We can translate any NAND-TM program $P'$ into an oblivious program $P$ by making $P$ "sweep" its arrays. That is, the index `i` in $P$ will always move all the way from position $0$ to position $T(n)-1$ and back again.
We can then simulate the program $P'$ with at most $T(n)$ overhead: if $P'$ wants to move `i` left when we are in a rightward sweep then we simply wait the at most $2T(n)$ steps until the next time we are back in the same position while sweeping to the left. 


![We simulate a $T(n)$-time NAND-TM program $P'$ with an _oblivious_ NAND-TM program $P$ by adding special arrays `Atstart` and `Atend` to mark positions $0$ and $T-1$ respectively. The program $P$ will simply "sweep" its arrays from right to left and back again. If the original program $P'$ would have moved `i` in a different direction then we wait $O(T)$ steps until we reach the same point back again, and so $P$ runs in $O(T(n)^2)$ time.](../figure/obliviousnandtm.png){#obliviousnandtmfig  .margin }


::: {.proof data-ref="obliviousnandtmthm"}
Let $P'$ be a NAND-TM program computing $F$ in $T(n)$ steps.
We construct an oblivious NAND-TM program $P$ for computing $F$ as follows (see also [obliviousnandtmfig](){.ref}).

1. On input $x$, $P$ will compute $T=T(|x|)$ and set up arrays `Atstart` and `Atend` satisfying 
 `Atstart[`$0$`]`$=1$ and `Atstart[`$i$`]`$=0$ for $i>0$ and `Atend[`$T-1$`]`$=1$ and `Atend[`i`]`$=0$ for all $i \neq T-1$.  We can do this because $T$ is a nice function. Note that since this computation does not depend on $x$ but only on its length, it is oblivious. 

 2. $P$ will also have a special array `Marker` initialized to all zeroes.

2. The index variable of $P$ will change direction of movement to the right whenever `Atstart[i]`$=1$ and to the left whenever `Atend[i]`$=1$. 

3. The program $P$  simulates the execution of $P'$. However, if the `MODANDJMP` instruction in $P'$ attempts to move to the right when $P$ is moving left (or vice versa) then $P$ will set `Marker[i]` to $1$ and  enter into a special "waiting mode". In this mode $P$ will wait until the next time in which `Marker[i]`$=1$ (at the next sweep) at which points $P$ zeroes `Marker[i]` and continues with the simulation. In the worst case this will take $2T(n)$ steps (if $P$ has to go all the way from one end to the other and back again.)
   
4. We also modify $P$ to ensure it ends the computation after simulating exactly $T(n)$ steps of $P'$, adding "dummy steps" if $P'$ ends early.

We see that $P$ simulates  the execution of $P'$ with an overhead of $O(T(n))$ steps of $P$ per one step of $P'$, hence completing the proof.
:::


[obliviousnandtmthm](){.ref} implies [non-uniform-thm](){.ref}. Indeed, if $P$ is a $k$-line oblivious NAND-TM program computing $F$ in time $T(n)$ then for every $n$ we can obtain a NAND-CIRC program of $(k-1)\cdot T(n)$ lines by simply making $T(n)$ copies of $P$ (dropping the final `MODANDJMP` line).
In the $j$-th copy we replace all references of the form `Foo[i]`  to `foo_`$i_j$ where $i_j$ is the value of `i` in the $j$-th iteration.

### Algorithmic transformation of NAND-TM to NAND 

The proof of [non-uniform-thm](){.ref} is _algorithmic_, in the sense that the proof yields a polynomial-time algorithm that given a Turing Machine $M$ and parameters $T$ and $n$, produces a circuit  of $O(T^2)$ gates that agrees with $M$ on all inputs $x\in \{0,1\}^n$ (as long as $M$ runs for less than $T$ steps these inputs.)
We record this fact in the following theorem, since it will be useful for us later on:

::: {.theorem title="Turing-machine to circuit compiler" #nand-compiler}
There is algorithm $UNROLL$ such that for every Turing Machine $M$ and numbers $n,T$, 
$UNROLL(M,T,n)$ runs for $poly(T)$ steps and outputs a NAND circuit $C$ with  $O(T^2)$ gates satisfying
$$C(x) = M(x)$$
for every $x\in \{0,1\}^n$ on which $M$  halts within at most $T$ steps.
:::

![We can transform a Turing Machine $M$, input length parameter $n$, and time bound $T$ into an $O(T^2)$ sized NAND circuit that agrees with $M$ on all inputs $x\in \{0,1\}^n$ on which $M$ halts in at most $T$ steps. The transformation is obtained by first using the equivalence of Turing Machines and NAND-TM programs $P$, then turning $P$ into an equivalent _oblivious_ NAND-TM program $P'$ via [obliviousnandtmthm](){.ref}, then "unrolling" $O(T^2)$ iterations of the loop of $P'$ to obtain an $O(T^2)$ line  NAND-CIRC program  that agrees with $P'$ on length $n$ inputs, and finally translating this program into an equivalent circuit.](../figure/unrolldescription.png){#unrolldescriptionfig }


::: {.proof data-ref="nand-compiler"}
We only sketch the proof  since it follows by directly translating the proof of [non-uniform-thm](){.ref into an algorithm together with the simulation of Turing machines by NAND-TM programs (see also [unrolldescriptionfig](){.ref}).
Specifically, $UNROLL$ does the following:

1. Transform the Turing Machine $M$ into an equivalent NAND-TM program $P$. 

2. Transform the NAND-TM program $P$ into an equivalent oblivious program $P'$ following the proof of [obliviousnandtmthm](){.ref}. The program $P'$ takes $T' = O(T^2)$ steps to simulate $T$ steps of $P$.

3. "Unroll the loop" of $P'$ by obtaining a NAND-CIRC program of $O(T')$ lines (or equivalenty a NAND circuit with $O(T^2)$ gates)  corresponding to the execution of $T'$ iterations of $P'$.
:::



::: { .pause }
Reviewing the transformations described in [unrolldescriptionfig](){.ref}, as well as solving the following two exercises is a great way to get more comfort with non-uniform complexity and in particular with $\mathbf{P_{/poly}}$ and its relation to $\mathbf{P}$.
:::


::: {.solvedexercise title="Alternative characterization of $\mathbf{P}$" #characterizationofp}
Prove that for every $F:\{0,1\}^* \rightarrow \{0,1\}$, $F\in \mathbf{P}$ if and only if there is a polynomial-time Turing Machine $M$ such that  for every $n\in \N$, $M(1^n)$ outputs a description of an $n$ input circuit $C_n$ that computes the restriction $F_{\upharpoonright n}$ of $F$ to inputs in $\{0,1\}^n$.
:::

::: {.solution data-ref="characterizationofp"}
We start with the "if" direction.
Suppose that there is a polynomial-time Turing Machine $M$ that on input $1^n$ outputs a circuit $C_n$ that computes $F_{\upharpoonright n}$. Then the following is a polynomial-time Turing Machine $M'$ to compute $F$. On input $x\in \{0,1\}^*$, $M'$ will:

1. Let $n=|x|$ and compute $C_n = M(1^n)$.

2. Return the evaluation of $C_n$ on $x$.

Since we can evaluate a Boolean circuit on an input in polynomial time, $M'$ runs in polynomial time and computes $F(x)$ on every input $x$.

For the "only if" direction, if $M'$ is a Turing Machine that computes $F$ in polynomial-time, then (applying the equivalence of Turing Machines and NAND-TM as well as [obliviousnandtmthm](){.ref}) there is also an oblivious NAND-TM program $P$ that computes $F$ in  time $p(n)$ for some polynomial $p$.
We can now define $M$ to be the Turing Machine that on input $1^n$ outputs the NAND circuit obtained by "unrolling the loop" of $P$ for $p(n)$ iterations.
The resulting NAND circuit computes $F_{\upharpoonright n}$ and  has $O(p(n))$ gates.
It can also be transformed to a Boolean circuit with $O(p(n))$ AND/OR/NOT gates.
:::


::: {.solvedexercise title="$\mathbf{P_{/poly}}$ characterization by advice" #adviceppoly}
Let $F:\{0,1\}^* \rightarrow \{0,1\}$. Then $F\in\mathbf{P_{/poly}}$ if and only if there exists a polynomial $p:\N \rightarrow \N$, a polynomial-time Turing Machine  $M$ and a sequence $\{ a_n \}_{n\in \N}$ of strings, such that for every $n\in \N$:

* $|a_n| \leq p(n)$  \
* For every $x\in \{0,1\}^n$, $M(a_n,x)=F(x)$.
:::

::: {.solution data-ref="adviceppoly"}
We only sketch the proof.
For the "only if" direction, if $F\in \mathbf{P_{/poly}}$ then we can use for $a_n$  simply the description of the corresponding circuit $C_n$ and for $M$ the program that computes in polynomial time the evaluation of a circuit on its input. 

For the "if" direction, we can use the same "unrolling the loop" technique of [non-uniform-thm](){.ref} to show that if $P$ is a polynomial-time NAND-TM program, then for every $n\in \N$, the map $x \mapsto P(a_n,x)$ can be computed by a polynomial size NAND-CIRC program $Q_n$.
:::




### Can uniform algorithms  simulate non uniform ones?

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

While it can sometimes be a real issue, in many natural settings the difference between uniform and non-uniform computation does not seem to so important.
In particular, in all the examples of problems not known to be in $\mathbf{P}$ we discussed before: longest path, 3SAT, factoring, etc., these problems are also not known to be in $\mathbf{P_{/poly}}$ either.
Thus, for "natural" functions, if you pretend that $TIME(T(n))$  is roughly the same as $SIZE(T(n))$, you will be right more often than wrong.


![Relations between $\mathbf{P}$, $\mathbf{EXP}$, and $\mathbf{P_{/poly}}$. It is known that $\mathbf{P} \subseteq \mathbf{EXP}$, $\mathbf{P} \subseteq \mathbf{P_{/poly}}$ and that $\mathbf{P_{/poly}}$ contains uncomputable functions (which in particular are outside of $\mathbf{EXP}$). It is not known whether or not $\mathbf{EXP} \subseteq \mathbf{P_{/poly}}$ though it is believed that $\mathbf{EXP} \not\subseteq \mathbf{P_{/poly}}$.](../figure/PEXPPpolyrelations.png){#PEXPPpolyrelationsfig}



### Uniform vs. Nonuniform computation: A recap

To summarize, the two models of computation we have described so far are:


* **Uniform models:** _Turing machines_, _NAND-TM programs_,  _RAM machines_, _NAND-RAM programs_, _C/JavaScript/Python_, etc.  These model include loops and unbounded memory  hence a single program can compute a function with unbounded input length. 


* **Non-uniform models:** _Boolean Circuits_ or _straightline programs_  have no loops and can only compute finite functions. The time to  execute them is exactly the number of lines or gates they contain. 

For a function $F:\{0,1\}^* \rightarrow \{0,1\}$ and some nice time bound $T:\N \rightarrow \N$, we know that:

* If $F$ is uniformly computable in time $T(n)$ then there is a sequence of circuits $C_1,C_2,\ldots$ where $C_n$ has $poly(T(n))$ gates and computes $F_{\upharpoonright n}$ (i.e., restriction of $F$ to $\{0,1\}^n$) for every $n$.

* The reverse direction is not necessarily true - there are examples of functions $F:\{0,1\}^n \rightarrow \{0,1\}$ such that $F_{\upharpoonright n}$ can be computed by even a constant size circuit but  $F$ is uncomputable.

This means that non uniform complexity is more useful to establish _hardness_ of a function than its _easiness_.




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


::: {.exercise title="Robustness to representation" #robsutrepresex }
[polyRAMTM-thm](){.ref} shows that the classes $\mathbf{P}$ and $\mathbf{EXP}$ are _robust_ with respect to variations in the choice of the computational model.
This exercise shows that these classes are also robust with respect to our choice of the representation of the input.

Specifically, let $F$ be a function mapping graphs to $\{0,1\}$, and let $F', F'':\{0,1\}^* \rightarrow \{0,1\}$ be the functions defined as follows. For every $x\in \{0,1\}^*$:

* $F'(x)=1$ iff $x$ represents a graph $G$ via the adjacency matrix representation such that $F(G)=1$.

* $F''(x)=1$ iff $x$ represents a graph $G$ via the adjacency list representation such that $F(G)=1$.

Prove that $F' \in \mathbf{P}$ iff $F'' \in \mathbf{P}$.


More generally, for every function $F:\{0,1\}^* \rightarrow \{0,1\}$, the answer to the question of whether $F\in \mathbf{P}$ (or whether $F\in \mathbf{EXP}$) is unchanged by switching representations, as long as transforming one representation to the other can be done in polynomial time (which essentially holds for all reasonable representations).
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

Try to think whether or not your algorithm extends to the case where there are _three_ possible time slots.
:::




## Bibliographical notes {#bibnotesrunningtime }

Because we are interested in the _maximum_ number of steps for inputs of a given length, running-time as we defined it is often known as _worst case complexity_. The _minimum_ number of steps (or "best case" complexity) to compute a function on length $n$ inputs is typically not a meaningful quantity since essentially every natural problem will have some trivially easy instances.
However, the _average case complexity_ (i.e., complexity on a "typical" or "random" input) is an interesting concept which we'll return to when we discuss _cryptography_.
That said, worst-case complexity is the most standard and basic of the complexity measures, and will be our focus in most of this book.




Some lower bounds for single-tape Turing machines are given in [@maass1985combinatorial].

For defining efficiency in the  $\lambda$ calculus, one needs to be careful about the order of application of the reduction steps, which can matter for computational efficiency, see for example [this paper](https://lmcs.episciences.org/1627).



The notation $\mathbf{P_{/poly}}$ is used for historical reasons.
It was introduced by Karp and Lipton, who considered this class as corresponding to functions that can be computed by polynomial-time Turing Machines that are given for any input length $n$ an _advice string_ of length polynomial in $n$.





