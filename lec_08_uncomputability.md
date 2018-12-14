% Uncomputability
% Boaz Barak


# Universality and uncomputability {#chapcomputable }

> # { .objectives }
* The universal machine/program - "one program to rule them all"
* See a fundamental result in computer science and mathematics: the existence of uncomputable functions.
* See the canonical example for an uncomputable function: _the halting problem_.
* Introduction to the technique of _reductions_ which will be used time and again in this course to show difficulty of computational tasks.
* Rice's Theorem, which is a starting point for much of research on compilers and programming languages, and marks the difference between _semantic_ and _syntactic_ properties of programs.


>_"A function of a variable quantity is an analytic expression composed in any way whatsoever of the variable quantity and numbers or constant quantities."_,  Leonhard Euler, 1748.


>_"The importance of the universal machine is clear. We do not need to have an infinity of different machines doing different jobs. ... The engineering problem of producing various machines for various jobs is replaced by the office work of 'programming' the universal machine"_, Alan Turing, 1948



One of the most significant results we showed for NAND programs is the notion of _universality_: that a NAND program can evaluate other NAND programs.
However, there was a significant caveat in this notion. To evaluate a NAND program of $s$ lines, we needed to use a bigger number of lines than $s$.
(Equivalently, the function that evaluates a given circuit of $s$ gates on a given input, requires more than $s$ gates to compute.)


It turns out that uniform models such as  NAND++ programs or Turing machines  allow us to "break out of this cycle" and obtain a truly _universal NAND++_ program $U$ that can evaluate all other programs, including programs that have more lines than $U$ itself.
The existence of such a universal program has far reaching applications.
Indeed, it is no exaggeration to say that the existence of a  universal program underlies the information technology revolution that began in the latter half of the 20th century (and is still ongoing).
Up to that point in history, people have produced various special-purpose calculating devices, from the abacus, to the slide ruler, to machines to compute trigonometric series.
But as Turing  (who was perhaps the one to see most clearly the ramifications of universality) observed, a _general purpose computer_ is much more powerful.
That is, we only need to build a device that can compute the single function $U$, and we have the ability, _via software_ to extend it to do arbitrary computations.
If we want to compute a new NAND++ program $P$, we do not need to build a new machine, but rather can represent $P$ as a string (or _code_) and use it as input for the universal program $U$.
Beyond the practical applications, the existence of a universal algorithm also surprising theoretical ramification, and in particular can be used to show the existence of _uncomputable functions_, upending the intuitions of  mathematicians over the centuries from Euler to Hilbert.
In this chapter we will prove the existence of the universal program, as well as show its implications for uncomputability.



## Universality: A NAND++ interpreter in NAND++

Like a NAND program, a NAND++  program (or a Python or Javascript program, for that matter)  is ultimately a sequence of symbols and hence can obviously be represented as a binary string.
We will spell out the exact details of one such  representation later, but as usual, the details are not so important (e.g., we can use the ASCII encoding of the source code).
What is crucial is that we can use such representations to evaluate any program.
That is, we prove the following theorem:




::: {.theorem title="Universality of NAND++" #univnandppnoneff}
There is a NAND++ program $U$ that computes the partial function $EVAL:\{0,1\}^* \rightarrow \{0,1\}^*$ defined as follows:
$$
EVAL(P,x)=P(x)
$$
for strings $P,x$ such that $P$ is a valid representation of a NAND++ program which halts and produces an output on $x$.
Moreover, for every input $x\in \{0,1\}^*$  on which $P$ does not halt, $U(P,x)$ does not halt as well.
:::

:::  {.proofidea data-ref="univnandppnoneff"}
Once you understand what the theorem says, it is not that hard to prove. The desired program $U$ is an _interpreter_ for NAND++ program. That is, $U$ gets a representation of the program $P$ (think of the source code), and some input $x$, and needs to simulate the execution of $P$ on $x$.

Think of how you would do that in your favorite programming language.
You would use some data structure, such as a dictionary, to store the values of all the variables and arrays of $P$.
Then, you could simulate $P$ line by line, updating the data structure as you go along.
The interpreter will continue the simulation until  `loop` is equal to $0$.

Once you do that, translating this interpreter from your programming language to NAND++ can be done just as we have seen in [chapequivalentmodels](){.ref}. The end result is what's known as a "meta-circular evaluator": an interpreter for a programming language in the same one. This is a concept that has a long history in computer science starting from the original universal Turing machine. See also [lispinterpreterfig](){.ref}.
:::

![A particularly elegant example of a "meta-circular evaluator" comes from John McCarthy's 1960 paper, where he defined the Lisp programming language and gave a Lisp function that evaluates an arbitrary Lisp program (see above). Lisp was not initially intended as a practical programming language and this  example was merely meant as an illustration that the Lisp universal function is more elegant than the universal Turing machine, but McCarthy's graduate student Steve Russell suggested that it can be implemented. As McCarthy later recalled, _"I said to him, ho, ho, you're confusing theory with practice, this eval is intended for reading, not for computing. But he went ahead and did it. That is, he compiled the eval in my paper into IBM 704 machine code, fixing a bug, and then advertised this as a Lisp interpreter, which it certainly was"._ ](../figure/lispinterpreter.png){#lispinterpreterfig .class width=300px height=300px}

[univnandppnoneff](){.ref} yields a stronger notion than the universality we proved for NAND, in the sense that we show a _single_ universal  NAND++ program $U$ that can evaluate _all_ NAND programs, including those that have more lines than the lines in $U$.^[This also occurs in practice. For example  the `C` compiler can be and is used to execute programs that are more complicated than itself.]
In particular, $U$ can even be used to evaluate itself!
This notion of _self reference_ will appear time and again in this course, and as we will see, leads to several counter-intuitive phenomena in computing.

Because we can transform other computational models, including NAND<<, $\lambda$ calculus, or a C program,  this means that even the seemingly "weak" NAND++ programming language is powerful enough to contain an interpreter for all these models.


To show the full proof of  [univnandppnoneff](){.ref}, we need to make sure $EVAL$ is well defined by specifying a  representation for NAND++ programs.
As mentioned, one perfectly fine choice is the ASCII representation of the source code.
But for concreteness, we can use the following representation:


>_Representing NAND++ programs._ If $P$ is a NAND++ program with $a$ array variables and $b$ scalar variables, then every iteration of $P$ is obtained by computing a NAND program $P'$ with $a+b$ inputs and outputs that updates these variables (where the array variables are read and written to at the special location `i`).^[We  assume that the NAND++ program is _well formed_, in the sense that every array variable is accessed only with the index `i`.]
So, we can use the list-of-triples representation of $P'$ to represent $P$.
That is, we represent $P$ by a tuple $(a,b,L)$ where $L$ is a list of triples of numbers in $\{0,\ldots, a+b-1 \}$.
Each triple $(j,k,\ell)$ in $L$ corresponds to a line of code in $P$ of the form `foo = NAND(bar,blah)`.
The indices $j,k,\ell$ correspond to _array_ variables if they are in $\{0,\ldots,a-1\}$ and to _scalar_ variables if they are in $\{a,\ldots,a+b-1\}$.
We will identify the arrays `X`,`Xvalid`,`Y`,`Yvalid` with the indices $0,1,2,3$ and the scalar `loop` with the index $a$. (Once again, the precise details of the representation do not matter much; we could have used any other.)





::: {.proof data-ref="univnandppnoneff"}
We will only sketch the proof, giving the major ideas.
First, we observe that we can easily write a _Python_ program that, on input a representation $P=(a,b,L)$ of a NAND++ program and an input $X$, evaluates $P$ on $X$.
Here is the code of this program for concreteness, though you can feel free to skip it if you are not familiar (or interested) in Python:

```python
def EVAL(P,X):
    """Get NAND++ prog P represented as (a,b,L) and input X, produce output"""
    a,b,L = *P
    vars = { } # scalar variables: for j in {a..a+b-1}, vars[j] is value of scalar variable j

    arrs = { } # array variables: for j in {0..a-1}, arrs[(j,i)] is -ith position of array j

    # Special variable indices:
    # X:0, Xvalid:1, Y:2, Yvalid:3, loop:a

    def setvar(j,v): # set variable j to value v
        if j>a: vars[j] = v # j is scalar
        else arrs[(j,i)] = v # j is array

    def getvar(j): # get value of var j (if j array then at current index i)
        if j>a: return vars.get(j,0)
        return arrs.get((j,i),0)

    def NAND(a,b): return 1-a*b

    # copy input
    for j in range(len(X)):
        arrs[(0,j)] = X[j]  # X has index 0
        arrs[(1,j)] = 1     # Xvalid has index 1

    maxseen = 0
    i = 0
    dir = 1 # +1: increase, -1: decrease
    while True:
        for (j,k,l) in L:
            setvar(j,NAND(getvar(k),getvar(l)))
        if not getvar(a): break # loop has index a
        i += dir
        if not i: dir= 1
        if i>maxseen:
            dir = -1
            maxseen = i

    # copy output
    i = 0
    res = []
    while getvar(3): # if Yvalid[i]=1
        res += [getvar(2)] # add Y[i] to result
        i += 1
    return Y
```

Translating this _Python_ code to NAND++ code line by line is a mechanical, even if somewhat laborious, process. However, to prove the theorem we don't need to write the code fully, but can use our "eat the cake and have it too" paradigm.
That is, while we can assume that our input program $P$ is written in the lowly NAND++ programming languages, in writing the program $U$ we are allowed to use richer models such as NAND<< (since they are equivalent by [RAMTMequivalencethm](){.ref}).
Translating the above Python code to NAND<< is truly straightforward.
The only issue is that NAND<< doesn't have the dictionary data structure built in, but we can represent a dictionary of the form $\{ key_0:val_0 , \ldots, key_{m-1}:val_{m-1} \}$  by simply a string (stored in an array) which is the list of pairs $(key_0,val_0),\ldots,(key_{m-1},val_{m-1})$ (where each pair is represented as a string in some prefix-free way). To retrieve an element with key $k$ we can scan the list from beginning to end and compare  each $key_i$ with $k$.
Similarly we scan the list to update the dictionary with a new value, either modifying it or appending the $(key,val)$ pair at the end.
The above is a very inefficient way to implement the dictionary data structure in practice, but it suffices for the purpose of proving the theorem.^[Reading and writing to a dictionary of $m$ values in this implementation takes $\Omega(m)$ steps, while it is in fact possible to do this in $O(1)$ steps using a _hash table_. Since NAND<< models a _RAM machine_ which corresponds to modern electronic computers, we can also implement a hash table  in NAND<<.]
:::



## Is every function computable?

We saw that NAND programs can compute every finite function.
A natural guess is that NAND++ programs could compute every infinite function.
However, this turns out to be _false_, even for  functions with $0/1$ output.
That is, there exists a function $F:\{0,1\}^* \rightarrow \{0,1\}$ that is  _uncomputable_!
This is actually quite surprising, if you think about it.
Our intuitive notion of a "function" (and the notion most scholars had until the 20th century) is that a function $f$ defines some implicit or explicit way of computing the output $f(x)$ from the input $x$.^[In the 1800's, with the invention of the  Fourier series and with the systematic study of  continuity and differentiability, people have starting looking at more general kinds of functions, but the modern definition of a function as an arbitrary mapping was not yet universally accepted. For example, in 1899 Poincare wrote "we have seen a mass of bizarre functions which appear to be forced to resemble as little as possible honest functions which serve some purpose. ... they are invented on purpose to show that our ancestor's reasoning was at fault, and we shall never get anything more than that out of them".]
The notion of an "uncomputable function" thus seems to be a contradiction in terms, but yet the following theorem shows that such creatures do exist:

> # {.theorem title="Uncomputable functions" #uncomputable-func}
There exists a function $F^*:\{0,1\}^* \rightarrow \{0,1\}$ that is not computable by any NAND++ program.

> # {.proof data-ref="uncomputable-func"}
The proof is illustrated in [diagonal-fig](){.ref}.
We start by defining the following function $G:\{0,1\}^* \rightarrow \{0,1\}$:
>
For every string $x\in\{0,1\}^*$, if $x$ satisfies __(1)__ $x$ is a valid representation of a NAND++ program $P_x$ and __(2)__ when the program $P_x$ is executed on the input $x$ it  halts and  produces an output,  then we define $G(x)$ as the first  bit of this output.  Otherwise (i.e., if $x$ is not a valid representation of a program, or the program $P_x$  never halts on $x$)  we define $G(x)=0$.
We define $F^*(x) := 1 - G(x)$.
>
We claim that there is no NAND++ program that computes $F^*$.
Indeed, suppose, towards the sake of contradiction,  that there was some program $P$ that computed $F^*$, and let $x$ be the binary string that represents the program $P$.
Then on input $x$, the program $P$ outputs $F^*(x)$.
But by definition, the program should also output $1-F^*(x)$, hence yielding a contradiction.

![We construct an uncomputable function by defining for every two strings $x,y$ the value $1-P_y(x)$ which equals $0$ if the program described by $y$ outputs $1$ on $x$, and $1$ otherwise.  We then define $F^*(x)$ to be the "diagonal" of this table, namely $F^*(x)=1-P_x(x)$ for every $x$. The function $F^*$ is uncomputable, because if it was computable by some program whose string description is $x^*$ then we would get that $P_{x^*}(x^*)=F(x^*)=1-P_{x^*}(x^*)$.](../figure/diagonal_proof.png){#diagonal-fig .class width=300px height=300px}


> # { .pause }
The proof of [uncomputable-func](){.ref} is short but subtle.
I suggest that you pause here and go back to read it again and think about it - this is a proof that  is worth reading at least twice if not three or four times.
It is not often the case that a few lines of mathematical reasoning establish a  deeply profound fact - that there are problems we simply _cannot_ solve and the "firm conviction" that Hilbert alluded to above is simply false.

The type of argument used to prove [uncomputable-func](){.ref} is known as  _diagonalization_ since it can be described as defining a function based on the diagonal entries of a table as in [diagonal-fig](){.ref}.
The proof can be thought of as an infinite version of the  _counting_ argument we used for showing lower bound for NAND progams in [counting-lb](){.ref}.
Namely, we show that it's not possible to compute all functions from $\{0,1\}^* \rightarrow \{0,1\}$ by NAND++ programs simply because there are more functions like that then there are NAND++ programs.



## The Halting problem

[uncomputable-func](){.ref} shows that there is _some_ function that cannot be computed.
But is this function the equivalent of the "tree that falls in the forest with no one hearing it"?
That is, perhaps it is a function that no one actually _wants_ to compute.
It turns out that there are natural uncomputable functions:

> # {.theorem title="Uncomputability of Halting function" #halt-thm}
Let $HALT:\{0,1\}^* \rightarrow \{0,1\}$ be the function such that $HALT(P,x)=1$ if the NAND++ program $P$ halts on input $x$ and equals $0$ if it does not.
Then $HALT$ is not computable.

Before turning to prove [halt-thm](){.ref}, we note that $HALT$ is a very natural function to want to compute.
For example, one can think of $HALT$ as a special case of the task of managing an "App store".
That is,  given the code of some application, the gatekeeper for the store needs  to decide if this code  is safe enough to allow in the store or not.
At a minimum, it seems that we should verify that the code would not go into an infinite loop.



:::  {.proofidea data-ref="halt-thm"}
One way to think about this proof is as follows:
$$
\text{Uncomputability of $F^*$} \;+\; \text{Universality} \;=\; \text{Uncomputability of $HALT$}
$$
That is, we will use the universal program that computes $EVAL$  to derive the uncomputability of $HALT$ from the uncomputability of $F^*$ shown in [uncomputable-func](){.ref}.
Specifically, the proof will be by contradiction.
That is, we will assume towards a contradiction that $HALT$ is computable, and use that assumption, together with the universal program of [univnandppnoneff](){.ref}, to derive that $F^*$ is computable, which will contradict  [uncomputable-func](){.ref}.
:::

![We prove that $HALT$ is uncomputable using a _reduction_ from computing the previously shown uncomputable function $F^*$ to computing $HALT$. We assume that we had an algorithm that computes $HALT$ and use that to obtain an algorithm that computes $F^*$.](../figure/halt-reduction.png){#halt-fig .class width=300px height=300px}

::: {.proof data-ref="halt-thm"}
The proof will use the previously established [uncomputable-func](){.ref} , as illustrated in [halt-fig](){.ref}.
That is, we will assume, towards a contradiction, that there is NAND++ program $P^*$ that can compute the $HALT$ function, and use that to derive that there is some NAND++ program $Q^*$ that computes the function  $F^*$ defined above, contradicting [uncomputable-func](){.ref}. (This is known as a proof by _reduction_, since we reduce the task of computing $F^*$ to the task of computing $HALT$. By the contrapositive, this means the uncomputability of $F^*$ implies the uncomputability of $HALT$.)

Indeed, suppose that  $P^*$ was a NAND++ program that computes $HALT$.
Then we can write a NAND++ program $Q^*$ that does the following on input $x\in \{0,1\}^*$:^[Note that we are using here a "high level" description of NAND++ programs. We know that we can implement the steps below, for example by first writing them in NAND<< and then transforming the NAND<< program to NAND++. Step 1 involves simply running the program $P^*$ on some input.]

>__Program $Q^*(x)$__
>
>1. Compute $z=P^*(x,x)$ \
>2. If $z=0$ then output $1$. \
>3. Otherwise, if $z=1$ then let $y$ be the first bit of $EVAL(x,x)$ (i.e., evaluate the program described by $x$ on the input $x$). If $y=1$ then output $0$. Otherwise output $1$.

We make the following claim about $Q^*$:

__Claim:__ For every $x\in \{0,1\}^*$, if  $P^*(x,x)=HALT(x,x)$ then  the program $Q^*(x)=F^*(x)$ where $F^*$ is the function from the proof of [uncomputable-func](){.ref}.

Note that the claim immediately implies that our assumption that $P^*$ computes $HALT$ contradicts  [uncomputable-func](){.ref}, where we proved that the function $F^*$ is uncomputable.
Hence the claim is sufficient to prove the theorem.

>__Proof of claim:__: Let $x$ be any string.
If the program described by $x$ halts on input $x$ and its first output bit is  $1$ then $F^*(x)=0$ and the output $Q^*(x)$ will also equal $0$ since $z=HALT(x,x)=1$, and hence in step 3 the program $Q^*$ will run in a finite number of steps (since the program described by $x$ halts on $x$), obtain the value $y=1$ and output $0$.
>
Otherwise, there are two cases.
Either the program described by $x$ does not halt on $x$, in which case $z=0$ and $Q^*(x)=1=F^*(x)$.
Or the program halts but its first output bit is not $1$.
In this case $z=1$ but the value $y$ computed by $Q^*(x)$ is not $1$ and so
$Q^*(x)=1=F^*(x)$.

As we discussed above, the desired contradiction is directly implied by the claim.
:::


> # { .pause }
Once again, this is a proof that's worth reading more than once.
The uncomputability of the halting problem is one of the fundamental theorems of computer science, and is the starting point for much of the investigations we will see later.
An excellent way to get a better understanding of [halt-thm](){.ref} is to do [halting-alt-ex](){.ref} which asks you to prove an alternative proof of the same result.


### Is the Halting problem really hard? (discussion)

Many people's first instinct when they see the proof of [halt-thm](){.ref} is to not believe it.
That is, most people  do  believe the mathematical statement, but intuitively it doesn't seem that the Halting problem is really that hard.
After all, being uncomputable only means that $HALT$ cannot be computed by a NAND++ program.
But  programmers seem to solve $HALT$ all the time by informally or formally arguing that their programs halt.
While it does occasionally happen that a program unexpectedly enters an infinite loop, is there really no way to solve the halting problem?
Some people argue that _they_ can, if they think hard enough, determine whether any concrete program that they are given will halt or not.
Some have even [argued](https://en.wikipedia.org/wiki/Roger_Penrose#Physics_and_consciousness) that humans in general have the ability to do that, and hence humans have inherently superior intelligence to computers or anything else modeled by NAND++ programs (aka Turing machines).^[This argument has also  been connected to the issues of consciousness and free will. I am not completely sure of its relevance  but perhaps the reasoning is  that humans have the ability to solve the halting problem but they exercise their free will and consciousness by choosing not to do so.]


The best answer we have so far is that there  truly is no way to solve $HALT$, whether using Macs, PCs, quantum computers, humans,  or any other combination of mechanical and biological devices.
Indeed this assertion is the content of the Church-Turing Thesis.
This of course does not mean that for _every_ possible  program $P$, it is hard to decide if $P$ enters an infinite loop.
Some programs don't even have loops at all (and hence trivially halt), and  there are   many other far less trivial examples of programs that we can certify to never enter an infinite loop  (or programs that we know for sure that _will_ enter such a loop).
However, there is no  _general procedure_ that would determine for an _arbitrary_ program $P$ whether it halts or not.
Moreover, there are some very simple programs for which it not known whether they halt or not.
For example, the following Python program will  halt if and only if [Goldbach's conjecture](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture) is false:



```python
def isprime(p):
    return all(p % i  for i in range(2,p-1))

def Goldbach(n):
    return any( (isprime(p) and isprime(n-p))
           for p in range(2,n-1))

n = 4
while True:
    if not Goldbach(n): break
    n+= 2
```

Given that Goldbach's Conjecture has been open since 1742, it is unclear that humans have any magical ability to say whether this (or other similar programs) will halt or not.

![[XKCD](https://xkcd.com/1266/)'s take on solving the Halting problem, using the principle that "in the long run, we'll all be dead".](../figure/halting_problem_2x.png){#xkcdhaltingfig .class width=300px height=300px}


### Reductions

The Halting problem turns out to be a linchpin of uncomputability, in the sense that [halt-thm](){.ref} has been used to show the uncomputability of a great many interesting functions.
We will see several  examples in such results in this chapter and the exercises, but there are many more such results in the literature (see [haltreductions](){.ref}).


The idea behind such uncomputability results is conceptually simple but can  at first be quite confusing.
If we know that $HALT$ is uncomputable, and we want to show that some other function $BLAH$ is uncomputable, then we can do so via a _contrapositive_ argument (i.e., proof by contradiction).
That is, we show that _if_ we had a NAND++ program that computes $BLAH$ _then_ we could have a NAND++ program that computes $HALT$.
(Indeed, this is exactly how we showed that $HALT$ itself is uncomputable, by showing this follows from  the uncomputability of the function $F^*$ from [uncomputable-func](){.ref}.)

For example, to prove that $BLAH$ is uncomputable,  we could show that there is a  computable function $R:\{0,1\}^* \rightarrow \{0,1\}^*$ such that for every pair $P$ and $x$, $HALT(P,x)=BLAH(R(P,x))$.
Such a function is known as a _reduction_, because we are _reducing_ the task of computing $HALT$ to the task of computing $BLAH$.
The confusing part about reductions is that we are assuming something we _believe_ is false (that $BLAH$ has an algorithm) to derive something that we _know_ is false (that $HALT$ has an algorithm).
For this reason Michael Sipser describes such results as having the form _"If pigs could whistle then horses could fly"_.

A reduction-based proof has two components. For starters, since we need $R$ to be computable, we should describe the algorithm to compute it. This algorithm is known as a _reduction_ since   the transformation  $R$ modifies an input to $HALT$ to an input to $BLAH$, and hence _reduces_ the task of computing $HALT$ to the task of computing $BLAH$.
The second component of a reduction-based proof is the _analysis_.
For example, in the example above, we need to prove $HALT(P,x) = BLAH(R(P,x))$.
The equality $HALT(P,x) = BLAH(R(P,x))$ boils down to proving two implications.
We need to prove that __(i)__ if $P$ halts on $x$ then $BLAH(R(P,x))=1$  and __(ii)__ if $P$ does not halt on $x$ then $BLAH(R(P,x))=0$.
When you're coming up with a reduction based proof, it is useful to separate the two components of _describing_ the reduction and _analyzing_ it.
Furthermore it is often useful to separate the analysis into two components corresponding to the implications __(i)__ and __(ii)__ above.


At the end of the day reduction-based proofs are just like  other proofs by contradiction, but the fact that they involve hypothetical algorithms that don't really exist tends to make such proofs quite confusing.
The one silver lining is that at the end of the day the notion of reductions is mathematically quite simple, and so it's not that bad even if you have to go back to first principles every time you need to remember what is the direction that a reduction should go in.
(If this discussion itself is confusing, feel free to ignore it; it might become clearer after you see an example of a reduction such as the proof of [haltonzero-thm](){.ref} or [spec-thm](){.ref}.)




![Some of the functions that have been proven uncomputable. An arrow from problem X to problem Y means that the proof that Y is uncomputable follows by reducing computing X to computing Y.  Black arrows correspond to proofs that are shown in this text while pink arrows correspond to proofs that are known but not shown here. There are  many other functions that have been shown uncomputable via a reduction from the Halting function $HALT$. ](../figure/reductions_from_halting.png){#haltreductions .class width=300px height=300px}

^[TODO: clean up this figure]


### A direct proof of the uncomputability of $HALT$ (optional)

It turns out that we can combine the ideas of the proofs of [uncomputable-func](){.ref}  and [halt-thm](){.ref} to obtain a short proof of the latter theorem, that does not appeal to the uncomputability of $F^*$.
This short proof appeared in print in a 1965 letter to the editor of Christopher Strachey:^[Christopher Strachey was an English computer scientist and the inventor of the CPL programming language. He was also an early artificial intelligence visionary, programming a computer to play Checkers and even write love letters in the early 1950's, see [this New Yorker article](https://www.newyorker.com/tech/elements/christopher-stracheys-nineteen-fifties-love-machine) and [this website](http://www.alpha60.de/art/love_letters/).]


>To the Editor, The Computer Journal.
>
>An Impossible Program
>
>Sir,
>
>A well-known piece of folk-lore among programmers holds that it is impossible to write a program which can examine any other program and tell, in every case, if it will terminate or get into a closed loop when it is run. I have never actually seen a proof of this in print, and though Alan Turing once gave me a verbal proof (in a railway carriage on the way to a Conference at the NPL in 1953), I unfortunately and promptly forgot the details. This left me with an uneasy feeling that the proof must be long or complicated, but in fact it is so short and simple that it may be of interest to casual readers. The version below uses CPL, but not in any essential way.
>
>Suppose `T[R]` is a Boolean function taking a routine (or program) `R` with no formal or free variables as its arguments and that for all `R`, `T[R] = True` if `R` terminates if run and that `T[R] = False` if `R` does not terminate.
>
>Consider the routine P defined as follows
>
>`  rec routine P` \
>`  §L: if T[P] go to L` \
>`  Return §`
>
>If `T[P] = True` the routine `P` will loop, and it will only terminate if `T[P] = False`. In each case `T[P]`` has exactly the wrong value, and this contradiction shows that the function T cannot exist.
>
>Yours faithfully, \
>C. Strachey
>
>Churchill College,
>Cambridge

::: { .pause }
Try to stop and extract the  argument for proving [halt-thm](){.ref} from the letter above.
:::

Since CPL is not as common today, let us reproduce this proof.
The idea is the following: suppose for the sake of contradiction that there exists a program `T` such that `T(f,x)` equals `True` iff `f` halts on input `x`.^[Strachey's letter considers  the no-input variant of $HALT$, but as we'll see, this is an immaterial distinction.]
Then we can construct a program `P` and an input `x` such that `T(P,x)` gives the wrong answer.
The idea is that on input `x`, the program `P` will do the following: run `T(x,x)`, and if the answer is `True` then go into an infinite loop, and otherwise halt.
Now you can see that `T(P,P)` will give the wrong answer: if `P` halts when it gets its own code as input, then `T(P,P)` is supposed to be `True`, but then `P(P)` will go into an infinite loop. And if `P` does not halt, then `T(P,P)` is supposed to be `False` but then `P(P)` will halt.
We can also code this up in Python:

```python
def CantSolveMe(T):
    """
    Gets function T that claims to solve HALT.
    Returns a pair (P,x) of code and input on which
    T(P,x) ≠ HALT(x)
    """
    def fool(x):
        if T(x,x):
            while True: pass
        return "I halted"

    return (fool,fool)
```

For example, consider the following Naive Python program `T` that guesses that a given function does not halt if its input contains `while` or `for`

```python
def T(f,x):
    """Crude halting tester - decides it doesn't halt if it contains a loop."""
    import inspect
    source = inspect.getsource(f)
    if source.find("while"): return False
    if source.find("for"): return False
    return True
```

If we now set `(f,x) = CantSolveMe(T)`, then `T(f,x)=False` but `f(x)` does in fact halt. This is of course not specific to this particular `T`: for every program `T`, if we run `(f,x) = CantSolveMe(T)` then we'll get an input on which `T` gives the wrong answer to $HALT$.



## Impossibility of general software verification


The uncomputability of the Halting problem turns out to be a special case of a much more general phenomenon.
Namely, that _we cannot certify semantic properties of general purpose programs_.
"Semantic properties" mean properties of the function that the program computes, as opposed to properties that depend on the particular syntax.
For example, we can easily check whether or not  a given C program contains no comments, or whether all function names begin with an upper case letter.
As we've seen, we cannot check whether a given program enters into an infinite loop or not.


But we could still hope to check some other properties of the program.
For example, we could hope to certify that a given  program $M$ correctly computes the multiplication operation, or that no matter what input the program is provided with, it will never reveal some confidential information.
Alas it turns out that the task of checking that a given program conforms with such a specification is uncomputable.
We start by proving a simple generalization of the Halting problem:

> # {.theorem title="Halting without input" #haltonzero-thm}
Let $HALTONZERO:\{0,1\}^* \rightarrow\{0,1\}$ be the function that on input $P\in \{0,1\}^*$, maps $P$ to $1$ if and only if the NAND++ program represented by $P$ halts when supplied the single bit $0$ as input.
Then $HALTONZERO$ is uncomputable.

> # { .pause }
The proof of [haltonzero-thm](){.ref} is below, but before reading it you might want to pause for a couple of minutes and think how you would prove it yourself.
In particular, try to think of what a reduction from $HALT$ to $HALTONZERO$ would look like.
Doing so is an excellent way to get some initial comfort with the notion of proofs by _reduction_, which is a notion that will recur time and again in this course.


:::  {.proof data-ref="haltonzero-thm"}
The proof is by reduction from $HALT$. We will assume, towards the sake of contradiction, that  $HALTONZERO$ is computable by some algorithm $A$, and use this hypothetical algorithm $A$ to construct an algorithm $B$ to compute $HALT$, hence obtaining a contradiction to [halt-thm](){.ref}.

Since this is our first proof by reduction from the Halting problem, we will spell it out in more details than usual. Such a proof by reduction consists of two steps:

1. _Description of the reduction:_ We will describe the operation of our algorithm $B$, and how it makes "function calls" to the hypothetical algorithm $A$.

2. _Analysis of the reduction:_ We will then prove that under the hypothesis that Algorithm $A$ computes $HALTONZERO$,  Algorithm $B$ will compute $HALT$.



Our Algorithm $B$ works as follows:


>__Algorithm $B(P,x)$:__  \
>
>__Input:__ A program $P \in \{0,1\}^*$ and $x\in \{0,1\}^*$ \
>__Assumption:__ Access to an algorithm $A$ such that $H(Q)=HALTONZERO(Q)$ for every program $Q$. \
>
>__Operation:__ \
>1. Let $Q$ denote the program that does the following: _"on input $z\in \{0,1\}^*$, evaluate $P$ on the input $x$ and return the result"_  \
>2. Feed $Q$ into Algorithm $A$ and denote $y = A(Q)$ be the resulting output. \
>3. Output $y$.


That is, on input a pair $(P,x)$ the algorithm  $B$ uses this pair to construct a program $Q$, feeds this program to $A$, and outputs the result. The program $Q$ is one that ignores its input and simply runs $P$ on $x$. Note however that our algorithm $B$ does _not_ actually execute the program $Q$: it merely constructs it and feeds it to $A$.

We now discuss exactly how does  algorithm $B$ performs step 1 of  obtaining the source code of the program $Q$ from the pair $(P,x)$.
In fact, constructing the program $Q$  is  rather simple.
We can do so by modifying $P$  to  ignore its input and use $x$ instead.
Specifically, if $x$ is of length $n$ we can do so by adding $2n$ lines of initialization code that sets arrays `MyX` and `MyXvalid` to the values corresponding to $x$ (i.e., `MyX[`$i$`]`$=x_i$ and `MyXvalid[`$i$`]`$=1$ for every $i \in [n]$).
The rest of the program $Q$ is obtained by replacing all references to `X` and `Xvalid` with references to `MyX` and `MyXvalid` respectively.
One can see that on every input $z\in \{0,1\}^*$, (and in particular for $z=0$) executing $Q$ on input $z$ will correspond to executing $P$ on the input $x$.

The above completes the _description_ of the reduction. The _analysis_ is obtained by proving the following claim:

__CLAIM:__ Define by $Q(P,x)$ the program $Q$ that Algorithm $B$ constructs in step 1 when given as input $P$ and $x$. Then for every program $P$ and input $x$, $Q(P,x)$ halts on the input $0$ if and only if $P$ halts on the input $x$.

__Proof of claim:__  Let $P,x$ be some program and input and let $Q=Q(P,x)$. Since $Q$ ignores its input and simply evaluates $P$ on the input $x$, for every input $z$ for $Q$, and so in particular for the input $z=0$, $Q$ will halt on the input $z$ if and only if $P$ halts on the input $x$.

The claim implies that $HALTONZERO(Q(P,x))=HALT(P,x)$.
Thus if the hypothetical algorithm $A$ satisfies $A(Q)=HALTONZERO(Q)$ for every $Q$ then the algorithm $B$ we construct satisfies $B(P,x)=HALT(P,x)$ for every $P,x$, contradicting the uncomputability of $HALT$.
:::



> # {.remark title="The hardwiring technique" #hardwiringrem}
In the proof of [haltonzero-thm](){.ref} we used the technique of  "hardwiring" an input  $x$ to a program $P$.
That is, modifying a program $P$ that it uses "hardwired constants" for some of all of its input.
This technique is quite common in reductions and elsewhere, and we will often use it again in this course.



Once we show the uncomputability of $HALTONZERO$ we can extend to various other natural functions:

> # {.theorem title="Computing all zero function" #allzero-thm}
Let $ZEROFUNC:\{0,1\}^* \rightarrow \{0,1\}$ be the function that on input $P\in \{0,1\}^*$, maps $P$ to $1$ if and only if the NAND++ program represented by $P$ outputs $0$ on every input $x\in \{0,1\}^*$. Then $ZEROFUNC$ is uncomputable.

> # {.proof data-ref="allzero-thm"}
The proof is by reduction to $HALTONZERO$. Suppose, towards the sake of contradiction, that there was an algorithm $A$ such that $A(P')=ZEROFUNC(P')$ for every $P'\in \{0,1\}^*$. Then we will construct an algorithm $B$ that solves $HALTONZERO$.
Given a program $P$, Algorithm $B$ will construct the following program $P'$: on input $x\in \{0,1\}^*$, $P'$ will first run $P(0)$, and then output $0$.
>
Now if $P$ halts on $0$ then $P'(x)=0$ for every $x$, but if $P$ does not halt on $0$ then $P'$ will never halt on every input and in particular will not compute $ZEROFUNC$. Hence, $ZEROFUNC(P')=1$ if and only if $HALTONZERO(P)=1$. Thus if we  define algorithm  $B$ as $B(P)=A(P')$ (where a program $P$ is mapped to $P'$ as above) then we see that if $A$ computes $ZEROFUNC$ then $B$ computes $HALTONZERO$, contradicting [haltonzero-thm](){.ref} .

Another result along similar lines is the following:


> # {.theorem title="Uncomputability of verifying parity" #paritythm}
The following function is uncomputable
$$
COMPUTES\text{-}PARITY(P) = \begin{cases} 1 & P \text{ computes the parity function } \\ 0 & \text{otherwise} \end{cases}
$$

::: { .pause }
We leave the proof of [paritythm](){.ref} as an exercise ([paritythmex](){.ref}).
I strongly encourage you to stop here and try to solve this exercise.
:::


### Rice's Theorem { #ricethm }

[spec-thm](){.ref} can be generalized far beyond the parity function
and in fact it rules out  verifying any type of semantic specification on programs.
We define a _semantic specification_ on programs to be some property that does not depend on the code of the program but just on the function that the program computes.

For example, consider the following two C programs

```python
int First(int k) {
    return 2*k;
}
```

```python
int Second(int n) {
    int i = 0;
    int j = 0
    while (j<n) {
        i = i + 2;
        j=  j + 1;
    }
    return i;
}
```

`First` and `Second` are two distinct C programs, but they compute the same function.
A _semantic_ property, such  as "computing a function $f:\N \rightarrow \N$ where $f(m) \geq m$ for every $m$", would be either _true_ for both programs or _false_ for both programs, since it depends on the _function_ the programs compute and not on their code.
A _syntactic_ property, such as "containing the variable `k`" or "using a `while` operation" might be true for one of the programs and false for the other, since it can depend on properties of the programs' _code_.^[While we contrast "semantic" with "syntactic" in this informal discussion, we  only formally define the notion of a _semantic_ function in this book. A famous example of a syntactically correct but semantically meaningless sentence in English is Chomsky's ["Colorless green ideas sleep furiously."](https://goo.gl/4gXoiV)]

Often the properties of programs that we are most interested in are the _semantic_ ones, since we want to understand the programs' functionality. Unfortunately, the following theorem shows that such properties are uncomputable in general:


::: {.theorem title="Rice's Theorem (slightly restricted version)" #rice-thm}
We say that two strings $P$ and $Q$ representing NAND++ programs are _functionally equivalent_, denoted by $P \equiv Q$, if for every $x\in \{0,1\}^*$, either both $P$ and $Q$ don't halt on $x$, or $P(x)=Q(x)$. We say that a function $F:\{0,1\}^* \rightarrow \{0,1\}$ is _semantic_ if for every functionally equivalent $P$ and $Q$,  $F(P)=F(Q)$.

Then the only semantic computable total functions $F:\{0,1\}^* \rightarrow \{0,1\}$ are the constant zero function and the constant one function.
:::

> # {.proofidea data-ref="rice-thm"}
The idea behind the proof is to show that  every semantic non-trivial function $F$ is at least as hard to compute as $HALTONZERO$. This will conclude the proof since by [haltonzero-thm](){.ref}, $HALTONZERO$ is uncomputable.
If a function $F$ is non trivial then there are two programs $P_0$ and $P_1$ such that $F(P_0)=0$ and $F(P_1)=1$. So, the goal would be to take a program $P$ and find a way to map it into a program $Q=R(P)$, such that __(i)__ if $P$ halts on zero then $Q$ computes the same partial function as $P_1$ and __(ii)__ if $P$ does not halt on zero then $Q$ computes the same partial function as $P_0$.
Because $F$ is semantic, this would mean that $HALTONZERO(P) = F(R(P))$, and hence would show that if $F$ was computable, then $HALTONZERO$ would be computable as well, contradicting [haltonzero-thm](){.ref}.
The details of how to construct this reductions are given below.


::: {.proof data-ref="rice-thm"}
We will not give the proof in full formality, but rather illustrate the proof idea by considering a particular semantic function $F$.
Define $MONOTONE:\{0,1\}^* \rightarrow \{0,1\}$ as follows: $MONOTONE(P)=1$ if there does not exist  $n\in \N$ and two inputs $x,x' \in \{0,1\}^n$ such that for every $i\in [n]$ $x_i \leq x'_i$ but $P(x)$ outputs $1$ and $P(x')=0$.
That is, $MONOTONE(P)=1$ if it's not possible to find an input $x$ such that flipping some bits of $x$ from $0$ to $1$ will change $P$'s output in the other direction from $1$ to $0$.
We will prove that $MONOTONE$ is uncomputable, but the proof will easily generalize to any semantic function.
For starters we note that $MONOTONE$ is not actually the all zeroes or all one function:

* The program $INF$ that simply goes into an infinite loop satisfies $MONOTONE(INF)=1$, since $INF$ is not defined _anywhere_ and so in particular  there are no two inputs $x,x'$ where $x_i \leq x'_i$ for every $i$ but  $INF(x)=0$ and $INF(x')=1$.

* The program $PAR$  that we've seen, which computes the XOR or parity of its input, is not monotone (e.g., $PAR(1,1,0,0,\ldots,0)=0$ but $PAR(1,0,0,\ldots,0)=0$) and hence $MONOTONE(PAR)=0$.

(It is important to note that in the above we talk about _programs_ $INF$ and $PAR$ and not the corresponding functions that they compute.)

We will now give a reduction from $HALTONZERO$ to $MONOTONE$.
That is, we assume towards a contradiction that there exists an algorithm $A$ that computes $MONOTONE$ and we will build an algorithm $B$ that computes $HALTONZERO$.
Our algorithm $B$ will work as follows:

>__Algorithm $B(P)$:__  \
>
>1. On input a program $P \in \{0,1\}^*$, $B$ will construct the following program $Q$: "on input $z\in \{0,1\}^*$ do: a. Run $P(0)$, b. Return $PAR(z)$". \
>2. $B$ will then return the value $1-A(Q)$.


To complete the proof we need to show that $B$ outputs the correct answer, under our assumption that $A$ computes $MONOTONE$.
In other words, we need to show that $HALTONZERO(P)=1-MONOTONE(Q)$.
However, note that if $P$ does _not_ halt on zero, then the program $Q$ enters into an infinite loop in step a. and will never reach step b.
Hence in this case the program $Q$ is functionally equivalent to $INF$.^[Note that the program $Q$ has different code than $INF$. It is not the same program, but it does have the same behavior (in this case) of never halting on any input.]
Thus, $MONOTONE(Q)=MONOTONE(INF)=1$.
If $P$ _does_ halt on zero, then step a. in $Q$ will eventually conclude and $Q$'s output will be determined by step b., where it simply outputs the parity of its input.
Hence in this case, $Q$ computes the non-monotone parity function (i.e., is functionally equivalent to $PAR$), and so we get that $MONOTONE(Q)=MONOTONE(PAR)=0$.
In both cases we see that $MONOTONE(Q)=1-HALTONZERO(P)$, which is what we wanted to prove.
An examination of this proof shows that we did not use anything about $MONOTONE$ beyond the fact that it is semantic and non-trivial (in the sense that it is not the all zero, nor the all-ones function).
:::

::: {.remark title="Semantic is not the same as uncomputable" #syntacticcomputablefunctions}
Rice's Theorem is so powerful and such a popular way of proving uncomputability that people sometimes get confused and think that it is
the _only_ way to prove uncomputability. In particular, a common misconception is  that if a function $F$ is _not_ semantic then it is _computable_.
This is not at all the case.
For example, consider the following function $HALTNOYALE:\{0,1\}^* \rightarrow \{0,1\}$. This is a function that on input a string that represents a NAND++ program $P$, outputs $1$ if and only if both __(i)__ $P$ halts on the input $0$, and __(ii)__ the program $P$ does not contain a variable with the identifier `Yale`. The function $HALTNOYALE$ is clearly not semantic, as  it will output two different values when given as input one of the following two functionally equivalent programs:

```python
Yale[0] = NAND(X[0],X[0])
Y[0] = NAND(X[0],Yale[0])
```

and

```python
Harvard[0] = NAND(X[0],X[0])
Y[0] = NAND(X[0],Harvard[0])
```

However, $HALTNOYALE$ is uncomputable since  every program $P$ can be transformed into an equivalent (and in fact improved `:)`) program $P'$ that does not contain the variable `Yale`. Hence if we could compute $HALTONYALE$ then we could compute also $HALTONZERO$.

Moreover, as we will see in [godelchap](){.ref}, there are uncomputable functions whose inputs are not programs, and hence for which the adjective "semantic" is not applicable.
:::


### Halting and Rice's Theorem for other Turing-complete models

As we saw before, many natural computational models turn out to be _equivalent_ to one another, in the sense that we can transform a "program" of one  model (such as a $\lambda$ expression, or a game-of-life configurations) into another model (such as a NAND++ program).
This equivalence implies that we can translate the uncomputability of the Halting problem for NAND++ programs into uncomputability for Halting in other models.
For example:

> # {.theorem title="Turing Machine Halting" #halt-tm}
Let $TMHALT:\{0,1\}^* \rightarrow \{0,1\}$ be the function that on input  strings $M\in\{0,1\}^*$ and $x\in \{0,1\}^*$ outputs $1$ if the Turing machine described by $M$ halts on the input $x$ and outputs $0$ otherwise. Then $TMHALT$ is uncomputable.

> # { .pause }
Once again, this is a good point for you to stop and try to prove the result yourself before reading the proof below.

> # {.proof }
We have seen in [TM-equiv-thm](){.ref} that for every NAND++ program $P$ there is an equivalent Turing machine $M_P$ such that for every $x$, that computes the same function.
The machine $M_P$ exactly simulated $P$, in the sense that  $M_P$ halts on $x$ if and only $P$ halts on $x$ (and moreover if they both halt, they produce the same output).
Going back to the proof of [TM-equiv-thm](){.ref}, we can see that the transformation of the program $P$ to the Turing machine $M(P)$ was described in a _constructive_ way.
>
Specifically, we gave explicit instructions how to build the Turing machine $M(P)$ given the description of the program $P$.
Thus, we can view the proof of [TM-equiv-thm](){.ref} as a high level description of an _algorithm_ to obtain $M_P$ from the program $P$, and using our "have your cake and eat it too" paradigm, this means that there exists also a NAND++ program $R$ such  that computes the map $P \mapsto M_P$.
We see that
$$
HALT(P,x)=TMHALT(M_P,x)=TMHALT(R(P),x) \label{eqtmhalt}
$$
and hence if we assume (towards the sake of a contradiction) that $TMHALT$ is computable then [eqtmhalt](){.eqref} implies that $HALT$ is computable, hence contradicting [halt-thm](){.ref}.


The same proof carries over to other computational models such as the _$\lambda$ calculus_, _two dimensional_ (or even one-dimensional) _automata_ etc.
Hence for example, there is no algorithm to decide if a $\lambda$ expression evaluates the identity function, and no algorithm to decide whether an initial configuration of the game of life will result in eventually coloring the cell $(0,0)$ black or not.

We can also generalize Rice's Theorem to any Turing complete model (see [turingcompletedef](){.ref}):

> # {.theorem title="Rice's Theorem for general models (optional)" #genericricethm}
Let $\mathcal{F}$ be the set of all partial functions from $\{0,1\}^*$ to $\{0,1\}^*$ and $\mathcal{M}:\{0,1\}^* \rightarrow \mathcal{F}$ be a Turing complete model.
Then for every function $\mathcal{P}:\mathcal{F} \rightarrow \{0,1\}$ that is not the constant zero or one function, the function
$F_{\mathcal{P}}:\{0,1\}^* \rightarrow \{0,1\}$ defined as $F_{\mathcal{P}}(Q)= \mathcal{P}(\mathcal{M}(Q))$ is uncomputable (by NAND++ programs).

::: { .pause }
The generality of [genericricethm](){.ref} comes at the expense of being cumbersome to state.
However it simply says that Rice's Theorem holds for every Turing complete model, in the sense that every non-trivial semantic property (i.e., a property that is not always true or always false, and depends on the _function_ that a program computes rather than syntactic properties of its code) is uncomputable.
Understanding how the formal statement of [genericricethm](){.ref} captures this is a great exercise.
Once you do so, working out the proof is fairly straightforward.
:::

::: {.proof data-ref="genericricethm"}
We only sketch the proof. This is actually a fairly straightforward corollary of the "standard" Rice's Theorem ([rice-thm](){.ref}).
Any non-trivial property of partial functions $\mathcal{P}:\mathcal{F} \rightarrow \{0,1\}$ gives rise to a semantic and non-trivial function on NAND++ programs $G_{\mathcal{P}}:\{0,1\}^* \rightarrow \{0,1\}$. That  is, $G_{\mathcal{P}}(P)$ equals $\mathcal{P}(F_P)$ whwere $F_P$ is the function computed by the program $P$.
By Rice's Theorem, $G_{\mathcal{P}}$ will be uncomputable.
However, if $\mathcal{M}$ is a Turing-complete model, and we could compute the function $F_{\mathcal{P}}$ defined as $F_{\mathcal{P}}(Q)  = \mathcal{P}(\mathcal{M}(Q))$ then we could compute $G_{\mathcal{P}}$ by simply using
$$
G_{\mathcal{P}}(P) = F_{\mathcal{P}}(ENCODE_{\mathcal{M}}(P))
$$
where $ENCODE_{\mathcal{M}}$ is the function that maps a NAND++ program $P$ into a program in $\mathcal{M}$ that computes the same function. Such computale a function $ENCODE_{\mathcal{M}}$ exists by the definition of Turing completeness ([turingcompletedef](){.ref}).
:::



### Is software verification doomed? (discussion)

Programs are increasingly being used for mission critical purposes, whether it's running our banking system, flying planes, or monitoring nuclear reactors.
If we can't even give a certification algorithm that  a program correctly computes the parity function, how can we ever be assured that a program does what it is supposed to do?
The key insight is that while it is impossible to certify that a _general_ program conforms with a specification, it is possible to write a program in the first place in a way that will make it easier to certify.
As a trivial example, if you write a program without loops, then you can certify that it halts.
Also, while it might not be possible to certify that an _artbirary_ program computes the parity function, it is quite possible to write a particular program $P$ for which we can mathematically _prove_ that $P$ computes the parity.
In fact, writing programs or algorithms and providing proofs for their correctness is what we do all the time in algorithms research.

The field of _software verification_ is concerned with verifying that given programs satisfy certain conditions.
These conditions can be that the program computes a certain function, that it never writes into a dangeours memory location, that is respects certain invariants, and others.
While the general tasks of verifying this may be uncomputable, researchers have managed to do so for many interesting cases, especially if the program is written in the first place in a formalism or programming language that makes verification easier.
That said, verification, especially of large and complex programs, remains a highly challenging task in practice as well, and the number of programs that have been formally proven correct is still quite small.
Moreover, even phrasing the right theorem to prove (i.e., the specification) if often a highly non-trivial endeavor.


::: { .recap }
* There is a _universal_ NAND++ program $U$ such that on input a description of a NAND++ program $P$ and some input $x$,  $U(P,x)$ halts and  outputs $P(x)$ if (and only if) $P$ halts on input $x$. Unlike in the case of finite computation (i.e., NAND programs / circuits), the input to the program $U$ can be a program $P$ that has more lines than $U$ itself.

* Unlike the finite case, there are actually functions that are _inherently uncomputable_ in the sense that they cannot be computed by _any_ NAND++ program.

* These include not only some "degenerate" or "esoteric" functions but also functions that people have deeply cared about and conjectured that could be computed.

* If the Church-Turing thesis holds then a function $F$ that is uncomputable according to our definition cannot  be computed by any finite means.
:::

## Exercises

::: {.remark title="Disclaimer" #disclaimerrem}
Most of the exercises have been written in the summer of 2018 and haven't yet been fully debugged. While I would prefer people do not post online solutions to the exercises, I would greatly appreciate if you let me know of any bugs. You can do so by posting a [GitHub issue](https://github.com/boazbk/tcs/issues) about the exercise, and optionally complement this with an email to me with more details about the attempted solution.
:::


::: {.exercise title="Computing parity" #paritythmex}
Prove [paritythm](){.ref} without using  Rice's Theorem.
:::



> # {.exercise #salil-ex}
For each of the following two functions, say whether it is decidable (computable) or not:
>
1. Given a NAND++ program $P$, an input $x$, and a number $k$, when we run $P$ on $x$, does the index variable `i` ever reach $k$?
>
2. Given a NAND++ program $P$, an input $x$, and a number $k$, when we run $P$ on $x$, does $P$ ever write to an array at index $k$?




## Bibliographical notes

The universal program and uncomputability of $HALT$ was first shown by Turing in 1937, though closely related results were shown by Church a year before.
These works built on Gödel's 1931 _incompleteness theorem_ that we will discuss in [godelchap](){.ref}.

Talk about intuitionistic, logicist, and formalist approaches for the foundations of mathematics.
Perhaps analogy to veganism.
State the full Rice's Theorem and say that it follows from the same proof as in the exercise.]

The diagonlization argument used to prove uncomputability of $F^*$ is of course derived from Cantor's argument for the uncountability of the reals.
In a twist of fate, using  techniques originating from the works  Gödel and Turing,  Paul Cohen showed in 1963 that Cantor's Continuum Hypothesis is independent of the axioms of set theory, which means that neither it nor its negation is provable from these axioms and hence in some sense  can be considered as "neither true nor false".^[The [Continuum Hypothesis](https://goo.gl/9ieBVq) is the conjecture that for every subset $S$ of $\mathbb{R}$, either there is a one-to-one and onto map between $S$ and $\N$ or there is a one-to-one and onto map between $S$ and $\mathbb{R}$. It was conjectured by Cantor and listed by Hilbert in 1900 as one of the most important problems in mathematics.]
See [here](https://gowers.wordpress.com/2017/09/19/two-infinities-that-are-surprisingly-equal/) for recent progress on a related question.



## Further explorations

Some topics related to this chapter that might be accessible to advanced students include: (to be completed)


## Acknowledgements
