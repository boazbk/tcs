#  What if P equals NP?

>_"There should be no fear ... we will be protected by God."_, President Donald J. Trump, inauguration speech, 2017

>_"No more half measures, Walter"_, Mike Ehrmantraut in "Breaking Bad", 2010.

>_"The evidence in favor of  \[$\mathbf{P}\neq \mathbf{NP}$\] and \[ its algebraic counterpart \] is so overwhelming, and the consequences of their failure are so grotesque, that their status may perhaps be compared to that of physical laws rather than that of ordinary mathematical conjectures."_,  Volker Strassen, laudation for Leslie Valiant, 1986.

We have mentioned that the question of whether $\mathbf{P}=\mathbf{NP}$, which is equivalent to whether there is a polynomial-time algorithm for $3SAT$, is the great open question of Computer Science.
But why is it so important?
In this lecture, we will try to figure out the implications of such an algorithm.

First, let us get one qualm out of the way.
Sometimes people say, _"What if $\mathbf{P}=\mathbf{NP}$ but the best algorithm for 3SAT takes $n^{100}$ time?"_
Well, $n^{100}$ is much larger than, say, $2^{\sqrt{n}}$ for any input shorter than $10^{60}$ bits which is way way larger than the world's total storage capacity (estimated at a "mere" $10^{21}$ bits or about 200 exabytes at the time of this writing).
So qualitatively, this question can be thought of as "what if the complexity of 3SAT is exponential for all inputs that we will ever encounter, but then grows much smaller than that?"
To me this sounds like the computer science equivalent of asking "what if the laws of physics change completely once they are out of the range of our telescopes?".
Sure, this is a valid  possibility, but wondering about it does not sound like the most productive use of our time.

So, as the saying goes, we'll keep an open mind, but not so open that our brains fall out, and assume from now on that:

 * There is a mathematical god.

and

 * She does not "pussyfoot around" or take "half measures". If she decided to make 3SAT easy then this problem will have an $10^6\cdot n$ (or at worst $10^6 n^2$) time algorithm, and if she decided to make 3SAT hard, then for every $n$, 3SAT on $n$ variables cannot be solved by a NAND program of fewer than $2^{10^{-6}n}$ lines.

So far most of our evidence points to the latter possibility of 3SAT being exponentially hard, but we have not ruled out the former possibility either.
In this lecture we will explore some of its consequences.

## Search to decision reduction

A priori, having a fast algorithm for 3SAT might not seem so impressive. Sure, it will allow us to decide the satisfiability of not just 3CNF formulas but also quadratic equations, as well as find out whether there is a long path in a graph, and solve many other decision problems.
But this is not typically what we want to do.
It's not enough to know _if_ a formula is satisfiable- we want to discover the actual actual satisfying assignment.
Similarly, it's not enough to find out if a graph has a long path- we want to actually find the path.

It turns out that if we can solve these decision problems, we can solve the corresponding search problems as well:

> # {.theorem title="Search vs Decision" #search-dec-thm}
Suppose that $\mathbf{P}=\mathbf{NP}$. Then for every polynomial-time NAND++ program $P$ and $a,b \in \N$,there is a polynomial time NAND++ program $FIND$  such that for every  $x\in \{0,1\}^n$, if there exists $y\in \{0,1\}^{an^b}$ satisfying $P(xy)=1$, then $FIND(x)$ finds some string $y'$ satisfying this condition.

While the theorem's statement is a bit of a mouthful, it in particular implies that if $\mathbf{P}=\mathbf{NP}$ then we can  we can find a satisfying assignment for every satisfiable 3CNF formula, find a simple path of length at least $k$ in any graph that has one, etc..


> # {.proof data-ref="search-dec-thm"}
The idea behind the proof is simple.
If $\mathbf{P}=\mathbf{NP}$ then for every polynomial-time NAND++ program $P$ and $a,b \in \N$, there is a polynomial-time algorithm $STARTSWITH$ that on input $x\in \{0,1\}^*$ and $z\in \{0,1\}^\ell$, outputs $1$ if and only if there exists some $y\in \{0,1\}^{an^b}$ such that the first $\ell$ bits of $y$ are equal to $z$ and $P(xy)=1$. Indeed, we leave it as an exercise to verify that the $STARTSWITH$ function is in $\mathbf{NP}$ and hence can be solved in polynomial time if $\mathbf{P}=\mathbf{NP}$.
>
Now for any program $P$ and $a,b\in\N$, we can implement $FIND(x)$ as follows: \
1. For $\ell=0,\ldots,an^b-1$ do the following: \
  >a. let $b_0 = STARTSWITH(xz_{0}\cdots z_{\ell-1}0)$ and $b_1 = STARTSWITH(xz_{0}\cdots z_{\ell-1}1)$ \
  >b. If $b_0=1$ then $z_\ell=0$, otherwise $z_\ell=1$.
2. Output $z_0,\ldots,z_{an^b-1}$
>
To analyze the $FIND$ algorithm note that it makes $2an^{b-1}$ invocations to $STARTSWITH$ and hence if the latter is polynomial-time then so is $FIND$.
Now suppose that $x$ is such that there exists _some_ $y$ satisfying $P(xy)=1$.
We claim that at every step $\ell=0,\ldots,an^b-1$, we maintain the invariant that there exists $y\in \{0,1\}^{an^b}$ whose first $\ell$ bits are $z$ s.t. $P(xy)=1$.
Note that this claim implies the theorem, since in particular it means that for $\ell = an^b-1$, $z$ satisfies $P(xz)=1$.
>
We prove the claim by induction.
For $\ell=0$ this holds vacuously.
Now for every $\ell$, if the call $STARTSWITH(xz_0\cdots z_{\ell-1}0)$ returns  $1$ then we are guaranteed the invariant by definition of $STARTSWITH$.
Now under our inductive hypothesis, there is $y_\ell,\ldots,y_{an^b-1}$ such that
$P(xz_0,\ldots,z_{\ell-1}y_\ell,\ldots,y_{an^b-1})=1$.
If the call to  $STARTSWITH(xz_0\cdots z_{\ell-1}0)$ returns $0$ then it must be the case that $y_\ell=1$, and hence when we set $z_\ell=1$ we maintain the invariant.


## Quantifier elimination

So, if $\mathbf{P}=\mathbf{NP}$ then we can solve all $\mathbf{NP}$ _search_ problems in polynomial time. But can we do more? Yes we can!


An $\mathbf{NP}$ decision problem can be thought of the task of deciding the truth of a statement of the form
$$
\exists_x P(x)
$$
for some NAND program $P$.
But we can think of more general statements such as
$$
\exists_x \forall_y P(x,y)
$$
or
$$
\exists_x \forall_y \exists_z P(x,y,z) \;.
$$

For example, given an $n$-input NAND program $P$, we might want to find the _smallest_ NAND program $P'$ that is computes the same function as $P$. The question of whether there is such $P'$ of size at most $k$ can be phrased as
$$
\exists_{P'} \forall_x   |P'| \leq k \wedge P(x)=P'(x) \;.
$$

It turns out that if $\mathbf{P}=\mathbf{NP}$ then we can solve these kinds of problems as well.

> # {.theorem title="Polynomial hierarchy collapse" #PH-collapse-thm}
If $\mathbf{P}=\mathbf{NP}$ then for every  $a\in \N$ there is a polynomial-time algorithm
that on input a NAND program $P$ on $an$ inputs, returns $1$ if and only if
$$
\exists_{x_1\in \{0,1\}^n} \forall_{x_2\in \{0,1\}^n} \cdots  Q_{x_a\in \{0,1\}^n} P(x_1,\ldots,x_a) \label{eq:QBF}
$$
where $Q$ is either $\exists$ or $\forall$ depending on whether $a$ is odd or even respectively.

> # {.proof data-ref="PH-collapse-thm"}
We prove the theorem by induction. We assume that there is a polynomial-time algorithm $SOLVE_{a-1}$ that can solve the problem [eq:QBF](){.eqref} for $a-1$ and use that to solve the problem for $a$.
On input a NAND program $P$, we will create the NAND program $S_P$ that on input $x_1\in \{0,1\}^n$, outputs $1-SOLVE_{a-1}(1-P_{x_1})$ where $P_{x_1}$ is a NAND program that on input $x_2,\ldots,x_a \in \{0,1\}^n$ outputs $P(x_1,\ldots,x_n)$.
Now note that by the definition of $SOLVE$
$$
\begin{aligned}
\exists_{x_1\in \{0,1\}^n} S_P(x_1) &= \\
\exists_{x_1} \overline{SOLVE_{a-1}(\overline{P_{x_1}})} &= \\
\exists_{x_1} \overline{\exists_{x_2}\cdots Q'_{x_a} \overline{P(x_1,\ldots,x_a)}} &= \\
\exists_{x_1} \forall_{x_2} \cdots Q_{x_a} P(x_1,\ldots,x_a)
\end{aligned}
$$
>
Hence we see that if we can solve the satisfiability problem for $S_P$ then we can solve [eq:QBF](){.eqref}.

This algorithm can also solve the search problem as well: find the value $x_1$ that certifies the truth of [eq:QBF](){.eqref}.
We note that while this algorithm is polynomial time, the exponent of this polynomial blows up quite fast.
If the original NANDSAT algorithm required $\Omega(n^2)$ solving $a$ levels of quantifiers  would require time $\Omega(n^{2^a})$.^[We do not know whether such loss is inherent. As far as we can tell, it's possible that the _quantified boolean formula_ problem has a linear-time algorithm. We will however see later in this course  that it satisfies a notion known as $\mathbf{PSPACE}$-hardness which is even stronger than $\mathbf{NP}$-hardness.]




### Approximating counting problems


Given a NAND program $P$, if $\mathbf{P}=\mathbf{NP}$ then we can find an input $x$ (if one exists) such that $P(x)=1$, but what if there is more than one $x$ like that?
Clearly we can't efficiently output all such $x$'s: there might be exponentially many.
But we can get an arbitrarily good multiplicative  approximation (i.e., a $1\pm \epsilon$ factor for arbitrarily small $\epsilon>0$) for the  number of such $x$'s as well as output a (nearly) uniform member of this set.
We will defer the details to later in this course, when we learn about _randomized computation_.

## What does all of this imply?

So, what will happen if we have a $10^6n$ algorithm for $3SAT$?
We have mentioned that $\mathbf{NP}$ hard problems arise in many contexts, and indeed scientists, engineers, programmers and others routinely encounter such problems in their daily work.
A better $3SAT$ algorithm will probably make their life easier, but that is the wrong place to look for the most foundational consequences.
Indeed, while the invention of electronic computers did of course make it easier to do calculations that people were already doing with mechanical devices and pen and paper, the main applications computers are used for today were not even imagined before their invention.

An exponentially faster algorithm for all $\mathbf{NP}$ problems would be no less radical improvement (and indeed, in some sense more) than the computer itself, and it is as hard for us to imagine what it would imply, as it was for Babbage to envision today's world.
For starters, such an algorithm would completely change the way we program computers.
Since we could automatically find the "best" (in any measure we chose) program that achieves a certain task, we will not need to define _how_ to achieve a task, but only specify tests as to what would be a good solution, and could also ensure that a program satisfies an exponential number of tests without actually running them.



The possibility that  $\mathbf{P}=\mathbf{NP}$ is often described as "automating creativity" and there is something to that analogy, as we often think of a creative solution, as a solution that is  hard to discover, once that "spark" hits, is easy to verify.
But there is also an element of hubris to that statement, implying that the most impressive consequence of such an algorithmic breakthrough will be that computers would succeed in doing something that humans already do today.
Indeed, as the manager of any mass-market film or music studio will tell you, creativity already is to a large extent automated, and as in most professions, we should expect to see  the need for humans in this process diminish with time even if $\mathbf{P}\neq \mathbf{NP}$.

Nevertheless, artificial intelligence, like many other fields, will clearly be greatly impacted by an efficient 3SAT algorithm.
For example, it is clearly much easier to find a better Chess-playing algorithm, when given any algorithm $P$, you can find the smallest algorithm $P'$ that plays Chess better than $P$.
Moreover, much of machine learning (and statistical reasoning in general) is about finding "simple" concepts that explain the observed data, and with $\mathbf{NP}=\mathbf{P}$, we could search for such concepts automatically for any notion of "simplicity" we see fit.
In fact, we could even "skip the middle man" and do an automatic search for the learning algorithm with smallest generalization error.
Ultimately the  field of Artificial Intelligence is about trying to "shortcut" billions of years of evolution to obtain artificial programs that match (or beat) the performance of natural ones, and a fast algorithm for $\mathbf{NP}$ would provide the ultimate shortcut.^[Some people might claim that, if it  indeed holds  $\mathbf{P}=\mathbf{NP}$, then  evolution should have  already discovered the efficient 3SAT  algorithm and perhaps we _have_ to discover this algorithm too if we want  to match evolution's performance. At the moments there seems to be very little evidence for such a scenario. In fact we have some partial results showing that, regardless of whether $\mathbf{P}=\mathbf{NP}$,  many types of  "local search" or "evolutionary"  algorithms require exponential time to solve 3SAT and other $\mathbf{NP}$-hard problems.]

More generally, a faster algorithm for $\mathbf{NP}$- problems would be immensely useful in any field where one is faced with computational or quantitative problems, which is basically all fields of science, math, and engineering.
This will not only help with  concrete problems such as designing a better bridge, or finding a better drug, but also with addressing basic mysteries such as trying to find  scientific theories or "laws of nature".
In a [fascinating talk](http://www.cornell.edu/video/nima-arkani-hamed-morality-fundamental-physics) physicist Nima Harkani Hamed discusses the effort of finding scientific theories in much the same language as one would describe solving an $\mathbf{NP}$ problem, where the solution is easy-to-verify, or  seems "inevitable", once you see it, but to reach it you need to search through a huge landscape of possibilities, and often can get "stuck" at local optima:

>_"the laws of nature have this amazing feeling of inevitability... which is associated with  local perfection."_

>_"The classical picture of the world is the top of a local mountain in the space of ideas. And you go up to the top and it looks amazing up there and absolutely incredible. And you learn that there is a taller mountain out there. Find it, Mount Quantum.... they're not smoothly connected ... you've got to make a jump to go from classical to  quantum ... This also tells you why we have such major challenges in trying to extend our understanding of physics. We don't have these knobs, and little wheels, and twiddles that we can turn. We have to learn how to make these jumps. And it is a tall order. And that's why things are difficult."_

Finding an efficient algorithm for $\mathbf{NP}$ amounts to always being able to search through an exponential space and find not just the "local" mountain, but the tallest peak.




But perhaps more than any computational speedups, a fast algorithm for $\mathbf{NP}$ problems would bring about a _new type of understanding_.
In many of the areas where $\mathbf{NP}$ completeness arises, it is not as much a barrier for solving computational problems as a barrier for obtaining "closed form formulas" or other types of a more constructive descriptions of the behavior of natural, biological, social and other systems.
A better algorithm for $\mathbf{NP}$, even if it is "merely" only $2^{\sqrt{n}}$ time, seems to require obtaining a new way to understand these types of systems, whether it is characterizing Nash equilibria, spin-glass configurations, entangled quantum states, of any of the  other questions where $\mathbf{NP}$ is currently a barrier for analytical understanding.
Such new insights would be very fruitful regardless of their computational utility.



## Can $\mathbf{P} \neq \mathbf{NP}$ be neither true nor false?

The _Continuum Hypothesis_, was a conjecture made by Georg Cantor in 1878, positing the non-existence of a certain type of infinite cardinality.^[One way to phrase it is that for every infinite subset $S$ of the real numbers $\R$, either there is a one-to-one and onto function $f:S \rightarrow \R$ or there is a one-to-one and onto function $f:S \rightarrow \N$.]
This was considered one of the most important open problems in set theory, and settling its truth or falseness was the first problem put forward by Hilbert in his 1900 address we made before.
However, using the developed by Gödel and Turing, in 1963 Paul Cohen proved that both the Continuum Hypothesis and its negation are consistent with the standard axioms of set theory (i.e., the Zermelo-Fraenkel axioms + the Axiom of choice, or  "ZFC" for short).^[Formally, what he proved is that if ZFC is consistent, then so is ZFC when we assume either the continuum hypothesis or its negation.]

Today many (though not all) mathematicians interpret this result as saying that the Continuum Hypothesis is neither true nor false, but rather is an axiomatic choice that we are free to make one way or the other.
Could the same hold for $\mathbf{P} \neq \mathbf{NP}$?

In short, the answer is _No_.
For example, suppose that we are trying to decide between the "3SAT is easy" conjecture (there is an $10^6n$ time algorithm for 3SAT) and the "3SAT is hard" conjecture (for every $n$, any NAND program that solves $n$ variable 3SAT takes $2^{10^{-6}n}$ lines), then, since for  $n = 10^8$, $2^{10^{-6}n} > 10^6 n$, this boils down to the finite question of deciding whether or not there is $10^{13}$ line NAND program deciding 3SAT on formulas with $10^8$ variables.  
If there is such a program then there is a finite proof of that, namely the proof is the ~1TB file describing the program, and the verification is the (finite in principle though infeasible in practice) process of checking that it succeeds on all inputs.^[This inefficiency is not necessarily inherent. Later in this course we will discuss results in program checking, interactive proofs, and average-case complexity, that can be used for efficient verification of  proofs of related statements. In contrast, the  inefficiency of verifying  _failure_ of all programs could well be inherent.]
If there isn't such a program then there is also a finite proof of that, though that would take longer since we would need to enumerate over all _programs_ as well.
Ultimately, since it boils down to a finite statement about bits and numbers, either the statement or its negation must follow from the standard axioms of arithmetic in a finite number of arithmetic steps.
Thus we cannot justify our ignorance in distinguishing between the "3SAT easy" and "3SAT hard" cases by claiming that this might be an inherently ill-defined question.
Similar reasoning (with different numbers) applies to  other variants of the $\mathbf{P}$ vs $\mathbf{NP}$ question.
We note that  in the case that 3SAT is hard, it may well be that there is no _short_ proof of this fact using the standard axioms, and this is a question that people have been studying in various restricted forms of proof systems.

## Is $\mathbf{P}=\mathbf{NP}$ "in practice"?

The fact that a problem is $\mathbf{NP}$ hard means that we believe there is no  efficient algorithm that solve it in the _worst case_.
It of course does not mean that every single instance of the problem is hard.
For example, if all the clauses in a  3SAT instance $\varphi$ contain the same variable $x_i$ (possibly in negated form) then by guessing a value to $x_i$ we can reduce $\varphi$ to a 2SAT instance which can then be efficiently solved.
Generalizations of this simple idea are used in "SAT solvers" which are algorithms that have solved certain specific interesting SAT formulas with thousands of variables, despite the fact that we believe SAT to be exponentially hard in the worst case.
Similarly, a lot of problems arising in machine learning and economics are $\mathbf{NP}$ hard.
And yet people manage to figure out prices (as economists like to point out, there is milk on the shelves) and  distinguish cats from dogs.
Hence people (and machines) seem to regularly succeed in solving interesting instances of $\mathbf{NP}$-hard problems, typically by using some combination of guessing while making local improvements.

It is  also true that there are many interesting instances of  $\mathbf{NP}$ hard problems that we do _not_ currently know how to solve.
Across all application areas, whether it is scientific computing, optimization, control or more, people often encounter hard instances of $\mathbf{NP}$ problems on which our current algorithms fail.
In fact, as we will see, all of our  digital security infrastructure relies on the fact that some concrete and easy-to-generate instances of, say, 3SAT (or, equivalently, any other $\mathbf{NP}$ hard problem) are exponentially hard to solve.

Thus it would be wrong to say that $\mathbf{NP}$ is easy "in practice", nor would it be correct to take $\mathbf{NP}$-hardness as the "final word" on the complexity of a problem, particularly when we have more information on where our instances arise from.
Understanding both the "typical complexity" of $\mathbf{NP}$ problems, as well as the power and limitations of certain  heuristics (such as various local-search based algorithms)  is a very active area of research.
We will see more on  these topics later in this course.

^[Talk more about coping with NP hardness. Main two approaches are _heuristics_ such as SAT solvers that succeed on _some_ instances, and _proxy measures_ such as mathematical relaxations that instead of solving problem $X$ (e.g., an integer program) solve program $X'$ (e.g., a linear program) that is related to that. Maybe give compressed sensing as an example, and least square minimization as a proxy for maximum apostoriori probability.]

## What if $\mathbf{P} \neq \mathbf{NP}$?

So $\mathbf{P}=\mathbf{NP}$ would give us all kinds of fantastical outcomes.
But we strongly suspect that $\mathbf{P} \neq \mathbf{NP}$, and in fact that there is no much-better-than-brute-force algorithm for 3SAT.
If indeed that is the case, is it all bad news?

One might think that impossibility results, telling you that you _can not_ do something, is the kind of cloud that does not have a silver lining.
But in fact, as we already alluded to before, it does.
A hard (in a sufficiently strong sense) problem in $\mathbf{NP}$ can be used to create a code that _cannot be broken_,  a task that for thousands of years has been the dream of not just spies but many  scientists and  mathematicians over the generations.
But the complexity viewpoint turned out to yield much more than simple codes, achieving tasks that people have not even dared to dream about.
These include the notion of _public key cryptography_, allowing two people to communicate securely without ever having exchanged a secret key, _electronic cash_, allowing private secure transaction without a central authority, and _secure multiparty computation_, enabling parties to compute a joint function on private inputs without revealing any extra  information about it.
Also, as we will see, computational hardness can be used to replace the role of _randomness_ in many settings.

Furthermore, while it is often convenient to pretend that computational problems are simply handed to us, and our job as computer scientists is to find the most efficient algorithm for them, this is not how things work in most computing applications.
Typically even formulating the problem to solve is a highly non-trivial task.
When we discover that the problem we want to solve is NP-hard, this might be a useful sign that we used the wrong formulation for it.

Beyond all these, the quest to understand computational hardness, including the discoveries of lower bounds for restricted computational models, as well as new types of reductions (such as those arising from "probabilistically checkable proofs"), already had surprising _positive_ applications to problems in algorithm design, as well as coding for both communication and storage.
This is not surprising since, as we mentioned before, from group theory to the theory of relativity, the pursuit of impossibility results has often been  one of the most fruitful enterprises of mankind.


## Lecture summary

* The question of whether $\mathbf{P}=\mathbf{NP}$ is one of the most important and fascinating questions of computer science and science at large, touching on all fields of the natural and social sciences, as well as mathematics and engineering.

* Our current evidence and understanding supports the "SAT hard" scenario that there is no much-better-than-brute-force algorithm for 3SAT and many other $\mathbf{NP}$-hard problems.

* We are very far from _proving_ this however, and we will discuss some of the efforts in this direction later in this course.

* Understanding how to cope with this computational intractability, and even benefit from it, comprises much of the research in theoretical computer science.

## Exercises



## Bibliographical notes

^[TODO: Scott's two surveys]

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)


## Acknowledgements
