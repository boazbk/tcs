# Physical implementations of NAND programs

> # { .objectives }
* Understand how NAND programs can map to physical processes in a variety of ways.
* Learn the model of _Boolean circuits_ and get proficient in moving between description of a NAND program as a code and as a circuit or _labeled graph_.
* See that NAND is a _universal basis_ for circuits, and examples for universal and non-universal families of gates.
* Understand the _physical extended Church-Turing thesis_ that NAND programs capture _all_ feasible computation in the physical world, and its physical and philosophical implications.


>_"In existing digital computing devices various mechanical or electrical devices have been used as
elements: Wheels, which can be locked ... which on moving from one position to another transmit electric pulses that may cause other similar wheels
to move; single or combined telegraph relays, actuated by an electromagnet and opening or closing
electric circuits; combinations of these two elements;—and finally there exists the plausible and
tempting possibility of using vacuum tubes"_, John von Neumann, first draft of a report on the EDVAC, 1945

We have defined NAND programs as a model for computation, but is this model only a mathematical abstraction, or is it
connected in some way to physical reality?
For example, if a function $F:\{0,1\}^n \rightarrow \{0,1\}$ can be computed by a NAND program of $s$ lines, is it possible, given an actual input $x\in \{0,1\}^n$, to compute $F(x)$ in the real world using an amount of resources that is roughly proportional to $s$?

In some sense, we already know that the answer to this question is __Yes__.
We have seen a _Python_ program that can evaluate NAND programs,
and so if we have a NAND program $P$, we can use any computer with Python installed on it to evaluate $P$ on inputs of our choice.
But do we really need modern computers and programming languages to run NAND programs?
And can we understand more directly how we can map such programs to actual physical processes that produce an output from an input?
This is the content of this lecture.

We will also talk about the following "dual" question.
Suppose we have some way to compute a function $F:\{0,1\}^n \rightarrow \{0,1\}$ using roughly an $s$ amount of "physical resources" such as material, energy, time, etc..
Does this mean that there is also a NAND program to compute $F$ using a number of lines that is not much bigger than $s$?
This might seem like a wishful fantasy, but we will see that the answer to this question might  be (up to some important caveats) essentially __Yes__ as well.

## Physical implementation of computing devices.


_Computation_ is an abstract notion, that is distinct from its physical _implementations_.
While most modern computing devices are obtained by mapping logical gates to semi-conductor based transistors, over history people have computed using a huge variety of mechanisms,  including mechanical systems, gas and liquid (known as _fluidics_), biological and chemical processes, and even living creatures (e.g., see [crabfig](){.ref} or  [this video](https://www.youtube.com/watch?v=czk4xgdhdY4) for how crabs or slime mold can be used to do computations).


In this lecture we review some of these implementations, both so  you can get an appreciation of how it is possible to directly translate NAND programs to the physical world, without going through the entire stack of architecture, operating systems, compilers, etc... as well as to emphasize that silicon-based processors are by no means the only way to perform computation.
Indeed, as we will see much later in this course, a very exciting recent line of works involves using different media for computation that would allow us to take advantage of _quantum mechanical effects_ to enable different types of algorithms.

![Crab-based logic gates from the paper "Robust soldier-crab ball gate" by Gunji, Nishiyama and Adamatzky. This is an example of an AND gate that relies on the tendency of two swarms of crabs arriving from different directions to combine to a single swarm that continues in the average of the directions.](../figure/crab-gate.jpg){#crabfig .class width=200px height=200px}



## Transistors and physical logic gates

A _transistor_ can be thought of as an electric circuit with two inputs, known as _source_ and _gate_ and an output, known as the _sink_.
The gate controls whether current flows from the source to the sink.
In a _standard transistor_, if the gate is "ON" then current can flow from the source to the sink and if it is "OFF" then it can't.
In a _complimentary transistor_ this is reversed: if the gate is "OFF" then current can flow from the source to the sink and if it is "ON" then it can't.  

![We can implement the logic of transistors using water. The water pressure from the gate closes or opens a faucet between the source and the sink.](../figure/transistor_water.png){#transistor-water-fig .class width=300px height=300px}

There are several ways to implement the logic of a transistor.
For example, we can use faucets to implement it using water pressure (e.g. [transistor-water-fig](){.ref}).^[This might seem as curiosity but there is a field known as [fluidics](https://en.wikipedia.org/wiki/Fluidics) concerned with implementing logical operations using liquids or gasses. Some of the motivations include operating in extreme environmental conditions such as in space or  a battlefield, where standard electronic equipment would not survive.]
However, the standard implementation uses electrical current.
One of the original implementations used   _vacuum tubes_.
As its name implies, a vacuum tube is a tube containing nothing (i.e., vacuum) and where a priori electrons could freely flow from source (a wire) to the sink (a plate). However, there is a gate (a grid)  between the two, where modulating its voltage  can block the  flow of electrons.

Early vacuum tubes were roughly the size of lightbulbs (and looked very much like them too).
In the 1950's they were supplanted by _transistors_, which implement the same logic using _semiconductors_ which are materials that normally do not conduct electricity but whose conductivity can be modified and controlled by inserting impurities ("doping") and an external electric field (this is known as the _field effect_).
In the 1960's computers were started to be implemented using _integrated circuits_ which enabled much greater density.
In 1965, Gordon Moore predicted that the number of transistors per circuit would double every  year (see [moorefig](){.ref}), and that this would lead to "such wonders as home computers —or at least terminals connected to a central computer— automatic controls for automobiles, and personal portable communications equipment".
Since then, (adjusted versions of) this so-called "Moore's law" has been running strong, though exponential growth cannot be sustained forever, and some physical limitations are already [becoming apparent](http://www.nature.com/news/the-chips-are-down-for-moore-s-law-1.19338).

![The number of transistors per integrated circuits from 1959 till 1965 and a prediction that exponential growth will continue at least another decade. Figure taken from "Cramming More Components onto Integrated Circuits", Gordon Moore, 1965](../figure/gordon_moore.png){#moorefig .class width=300px height=300px}

![Gordon Moore's cartoon "predicting" the implications of radically improving transistor density.](../figure/moore_cartoon.png){#moore-cartoon-fig .class width=300px height=300px}

![The exponential growth in computing power over the last 120 years. Graph by Steve Jurvetson, extending a prior graph of Ray Kurzweil.](../figure/1200px-Moore's_Law_over_120_Years.png){#kurzweil-fig .class width=300px height=300px}




##  Gates and circuits

We can use transistors to implement a _NAND gate_, which would be a system with two input wires $x,y$ and one output wire $z$, such that if we identify high voltage with "$1$" and low voltage with "$0$", then the wire  $z$ will equal to "$1$" if and only if the NAND of the values of the wires $x$ and $y$ is $1$ (see [transistor-nand-fig](){.ref}).

![Implementing a NAND gate using transistors.](../figure/nand_transistor.png){#transistor-nand-fig .class width=300px height=300px}


More generally, we can use transistors to implement the model of _Boolean circuits_.
We list the formal definition below, but let us start with the informal one:

>Let $B$ be some set of functions (known as "gates") from $\bits^k$ to $\{0,1\}$.  A _Boolean circuit_ with the basis $B$ is obtained by connecting "gates" which compute functions in $B$ together by "wires" where each gate has $k$ wires going into it and one wire going out of it. We have $n$ special wires known as the "input wires" and $m$ special wires known as the "output wires".
To compute a function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ using a circuit, we feed the bits of $x$ to the $n$ input wires, and then each gate computes the corresponding function, and we "read off" the output $y\in \{0,1\}^m$  from the $m$ output wires.

The number $k$ is known as the _arity_ of the basis $B$.
We think of $k$ as a small number (such as $k=2$ or $k=3$) and so the idea behind a Boolean circuit is that we can compute complex functions by combining together the simple components which are the functions in $B$.
It turns out that NAND programs correspond to circuits where the basis is the single function $NAND:\{0,1\}^2 \rightarrow \{0,1\}$.
We now show this more formally.

## Representing programs as graphs


We now define NAND programs as circuits, using the notion of _directed acyclic graphs_ (DAGs).



> # { .pause }
If you are not comfortable with the definitions of graphs, and in particular directed acyclic graphs (DAGs), now would be a great time to go back to the "mathematical background" lecture, as well as some of the resources [here](http://www.boazbarak.org/cs121/background/), and review these notions.

> # {.definition title="NAND circuit" #NANDcircdef}
A _NAND circuit_ with $n$ inputs and $m$ outputs is a labeled directed acyclic graph (DAG) in which every vertex has in-degree at most two. We require that there  are $n$ vertices with in-degree zero, known  as _input variables_, that are labeled with  `x_`$\expr{i}$ for $i\in [n]$.
Every vertex apart from the input variables is known as a _gate_. We require that there are $m$  vertices of out-degree zero, denoted as the _output gates_, and that are labeled with `y_`$\expr{j}$ for $j\in [m]$.
While not all vertices are labeled, no two vertices get the same label.
We denote the circuit  as $C=(V,E,L)$ where $V,E$ are the vertices and edges of the circuit, and $L:V \rightarrow_p S$ is the (partial) one-to-one labeling function that maps vertices into the set $S=\{$ `x_0`,$\ldots$,`x_`$\expr{n-1}$,`y_0`,$\ldots$, `y_`$\expr{m-1}$,$\}$.
The _size_ of a circuit $C$, denoted by $|C|$, is the number of gates that it contains.

The definition of NAND circuits is not ultimately that complicated, but may take  a second or third read  to fully parse.
It might help to look at [XORcircuitfig](){.ref}, which describes the NAND circuit that corresponds to the 4-line NAND program we presented above for the $XOR_2$ function.



![A NAND circuit for computing the $XOR_2$ function. Note that it has exactly four gates, corresponding to the four lines of the NAND program we presented above. The green labels $u,v,w$ for non-output gates are just for illustration and comparison with the NAND program, and are not formally part of the circuit.](../figure/XORcircuit.png){#XORcircuitfig .class width=300px height=300px}

A NAND circuit corresponds to computation in the following way.
To compute some output on an input $x\in \{0,1\}^n$, we start by assigning to the input vertex labeled with `x_`$\expr{i}$ the value $x_i$, and then proceed by assigning for every gate $v$ the value that is   the NAND of the values assigned to its in-neighbors (if it has less than two in-neighbors, we replace the value of the missing neighbors by zero).
The output $y\in \{0,1\}^m$  corresponds to the value assigned to the output gates, with $y_j$ equal to the value assigned to the value assigned to the gate labeled `y_`$\expr{j}$ for every $j\in [m]$.
Formally, this is defined as follows:

> # {.definition title="Computing a function by a NAND circuit" #NANDcirccomputedef}
Let $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and let $C=(V,E,L)$ be a NAND circuit with $n$ inputs and $m$ outputs.
We say that _$C$ computes $F$_ if there is a map $Z:V \rightarrow \{0,1\}$, such that for every $x\in \{0,1\}^n$, if $y=F(x)$ then: \
* For every $i\in [n]$, if $v$ is labeled with `x_`$\expr{i}$ then $Z(v)=x_i$. \
* For every $j\in[m]$, if $v$ is labeled with `y_`$\expr{j}$ then $Z(v)=y_j$. \
* For every gate $v$ with in-neighbors $u,w$, if $a=Z(u)$ and $b=Z(w)$, $Z(v)=NAND(a,b)$. (If $v$ has fewer than two neighbors then we replace either $b$ or both $a$ and $b$ with zero in the condition above.)

> # { .pause }
You should make sure you understand _why_ [NANDcirccomputedef](){.ref} captures the informal description above. This might require reading the definition a second or third time, but would be crucial for the rest of this course.

The following theorem says that these two notions of computing a function are actually equivalent: we can transform a NAND program into a NAND circuit computing the same function, and vice versa.

> # {.theorem title="Equivalence of circuits and straightline programs" #circuitprogequivthm}
For every $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $S\in \N$, $F$ can be computed by an $S$-line NAND program if and only if $F$ can be computed by an $n$-input $m$-output NAND circuit of $S$ gates.

The idea behind the proof is simple.
Just like we did to the XOR program, if we have a NAND program $P$ of $S$ lines, $n$ inputs, and $m$ outputs, we can transform it into a NAND circuit with $n$ inputs and $m$ gates, where each gate corresponds to a line in the program $P$. If  line $\ell$ involves the NAND of two variables assigned to in lines $\ell'$ and $\ell''$, then we will have edges to the gate corresponding to $\ell$ from the gates correspnding to $\ell',\ell''$.
In the other direction, we can transform a NAND circuit $C$ of  $n$ inputs, $m$ outputs and $S$ gates to an $S$-line program by essentially inverting this process.
For every gate in the program, we will have a line in the program which assigns to a variable the NAND of the variables corresponding to the in-neighbors of this gate.
If the gate is an output gate labeled with `y_`$\expr{j}$ then the  corresponding line will assign the value to the variable `y_`$\expr{j}$.
Otherwise we will assign the value to a fresh "workspace" variable.
We now show the formal proof.

> # {.proof data-ref="circuitprogequivthm"}
We start with the "only if" direction.
That is, we show how to transform a NAND program to a circuit.
Suppose that $P$ is an $S$ line program that computes $F$.
We will build a NAND circuit $C=(V,E,L)$ that computes $F$ as follows.
The vertex set $V$ will have the $n+S$ elements $\{ (0,0), \ldots, (0,n-1),(1,0),\ldots,(1,S-1) \}$.
That is, it will have $n$ vertices of the form $(0,i)$ for $i\in [n]$ (corresponding to the $n$ inputs), and $S$ vertices of the form $(1,\ell)$ (corresponding to the lines in the program).
For every line $\ell$ in the program $P$ of the form `foo := bar NAND baz`, we put edges in the graph of the form $\overrightarrow{(1,\ell')\;(1,\ell)}$ and $\overrightarrow{(1,\ell'')\;(1,\ell)}$ where  $\ell'$ and $\ell'$ are the last lines before $\ell$ in which the variables `bar` and `baz` were assigned a value.
If the variable `bar` and/or `baz` was not assigned a value prior to the $\ell$-th line and is not an input variable then we don't add a corresponding edge.
If the variable `bar` and/or `baz` is an input variable `x_`$\expr{i}$ then we add the edge $\overrightarrow{(0,i)\;(1,\ell)}$.
We label the vertices of the form $(0,i)$ with `x_`$\expr{i}$ for every $i\in [n]$.
For every $j\in[m]$, let $\ell$ be the last line in which the variable `y_`$\expr{j}$ is assigned a value,^[As noted in the appendix, valid NAND programs must assign a value to all their output variables.] and label the vertex $(1,\ell)$ with `y_`$\expr{j}$.
Note that the vertices of the form $(0,i)$ have  in-degree zero, and all edges of the form $\overrightarrow{(1,\ell')\;(1,\ell)}$ satisfy $\ell>\ell'$.
Hence this graph is a DAG, as in any cycle there would have to be at least on edge going from a vertex of the form $(1,\ell)$ to a vertex of the form $(1,\ell')$ for $\ell'<\ell$ (can you see why?).
Also, since we don't allow a variable of the form `y_`$\expr{j}$ on the right-hand side of a NAND operation, the output vertices have out-degree zero.
>
To complete the proof of the "only if" direction, we need to show that the circuit $C$ we constructed computes the same function $F$ as the program $P$ we were given.
Indeed, let $x\in \{0,1\}^n$ and $y = F(x)$.
For every $\ell$, let $z_\ell$ be the value that is assigned by the $\ell$-th line in the execution of $P$ on input $x$.
Now, as per [NANDcirccomputedef](){.ref}, define the map $Z:V \rightarrow \{0,1\}$ as follows: $Z((0,i))=x_i$ for $i\in [n]$ and $Z((1,\ell))=z_\ell$ for every $\ell \in [S]$.
Then, by our construction of the circuit, the map satisfies the condition that for vertex $v$ with in-neighbors $u$ and $w$, the value $Z(v)$ is the NAND of $Z(u)$ and $Z(w)$ (replacing missing neighbors with the value $0$), and hence in particular for every $j\in [m]$, the value assigned in the last line that touches `y_`$\expr{j}$ equals $y_j$.
Thus the circuit $C$ does compute the same function $F$.
>
For the "if" direction, we need to transform an $S$-gate circuit $C=(V,E,L)$ that computes $F:\{0,1\}^n \rightarrow \{0,1\}^m$ into an $S$-line NAND program $P$ that computes the same function.
We start by doing a [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) of the graph $C$.
That is we sort the vertex set $V$ as $\{v_0,\ldots,v_{n+S-1} \}$ such that  $\overrightarrow{v_i v_j} \in E$, $v_i < v_j$.
Such a sorting can be found for every DAG.
Moreover, because the input vertices of $C$ are "sources" (have in-degree zero), we can ensure they are placed first in this sorting and moreover for every $i\in [n]$, $v_i$ is the input vertex labeled with `x_`$\expr{i}$.
>
Now for $\ell=0,1,\ldots,n+S-1$ we will define a variable  $var(\ell)$  in our resulting program as follows:
If $\ell<n$ then $var(\ell)$ equals `x_`$\expr{i}$.
If $v_\ell$ is an output gate  labeled with `y_`$\expr{j}$ then $var(\ell)$ equals `y_`$\expr{j}$.
otherwise  $var(\ell)$ will be a temporary workspace variable `temp_`$\expr{\ell-n}$.
Our program $P$ will have $S$ lines, where for every $k\in [S]$, if the in-neighbors of $v_{n+k}$ are $v_i$ and $v_j$ then the $k$-th line in the program will be $var(n+k)$ ` := ` $var(i)$ ` NAND ` $var(j)$.
If $v_k$ has fewer  than two in-neighbors then we replace the corresponding variable with the variable `zero` (which is never set to any value and hence retains its default value of $0$.
>
To complete the proof of the "if" direction we need to show that the program $P$ we constructed computes the function $F$ as the circuit $C$ we were given.
Indeed, let $x\in \{0,1\}^n$ and $y=F(x)$.
Since $C$ computes $F$, there is a map $Z:V \rightarrow \{0,1\}$ as per  [NANDcirccomputedef](){.ref}.
We claim that if we run the program $P$ on input $x$, then for every $k\in [S]$ the value assigned by the $k$-th line corresponds to $Z(v_{n+k})$.
Indeed by construction the value assigned in the $k$-th line corresponds to the NAND of the value assigned to the in-neighbors of $v_{n+k}$.
Hence in particular if $v_{n+k}$ is the output gate labeled `y_`$\expr{j}$ then this value will equal $y_j$, meaning that on input $x$ our program will output $y=F(x)$.



## Composition from graphs

Given [circuitprogequivthm](){.ref}, we can reprove our composition theorems  in the circuit formalism, which has the advantage of making them more intuitive.
That is, we can prove [seqcompositionthm](){.ref} and [parcompositionthm](){.ref} by showing how to transform a circuits for $F$ and $G$ into circuits for $F \circ G$ and $F \oplus G$.
This is what we do now:

> # {.theorem title="Sequential composition, circuit version" #seqcompositioncircthm}
If $C,D$ are NAND circuits such that $C$ computes $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $D$ computes $G:\{0,1\}^m \rightarrow \{0,1\}^k$  then there is a circuit $E$ of size $|C|+|D|$ computing  the function $G\circ F:\{0,1\}^n \rightarrow \{0,1\}^k$.

![Given a circuit $C$ computing $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and a circuit $D$ computing $G:\{0,1\}^m \rightarrow \{0,1\}^k$, we obtain a circuit $E$ computing $G\circ F$ by identifying the inputs of $D$ with the outputs of $C$. That is, the resulting circuit consists of the gates of both $C$ and $D$, where we replace every in-neighbor of $D$ that was an input gate with the corresponding output gate of $C$.](../figure/serial_comp.png){#serialcompfig .class width=300px height=300px}

> # {.proof data-ref="seqcompositioncircthm"}
Let $C$ be the $n$-input $m$-output circuit computing $F$ and $D$ be the $m$-input $k$-output circuit computing $G$.
The circuit to compute $G \circ F$ is illustrated in [serialcompfig](){.ref}.
We simply "stack" $D$ after $C$, by obtaining a combined circuit with $n$ inputs and $|C|+|D|$ gates. The gates of $C$ remain the same, except that we identify the output gates of $C$ with the input gates of $D$. That is, for every edge that connected the $i$-th input of $D$ to a gate $v$ of $D$, we now connect to $v$ the output gate of $C$ corresponding to `y_`$\expr{i}$ instead.
After doing so, we remove the output labels from $C$ and keep only the outputs of $D$.
For every input $x$, if we execute the composed circuits on $x$ (i.e., compute a map $Z$ from the vertices to $\{0,1\}$ as per [NANDcirccomputedef](){.ref}), then the output gates of $C$ will get the values corresponding to $F(x)$ and hence the output gates of $D$ will have the value $G(F(x))$.


> # {.theorem title="Parallel composition, circuit versions" #parcompositioncircthm}
If $C,D$ are NAND circuits such that $C$ computes $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $D$ computes $G:\{0,1\}^{n'} \rightarrow \{0,1\}^{m'}$  then there is a circuit $E$ of size $|C|+|D|$ computing  the function $G\oplus F : \{0,1\}^{n+n'} \rightarrow \{0,1\}^{m+m'}$.

![Given a circuit $C$ computing $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and a circuit $D$ computing $G:\{0,1\}^{n'}\rightarrow \{0,1\}^{m'}$ we obtain a circuit $E$ computing $F \oplus G$ be simply putting the circuits "side by side", and renaming the labels of the inputs and outputs of $D$ to `x_`$n$,..,`x_`$n+n'-1$ and `y_`$m$,..,`y_`$m+m'-1$.](../figure/parallel_composition_circ.png){#parallelcompositioncircfig .class width=300px height=300px}


> # {.proof data-ref="parcompositioncircthm"}
If $C,D$ are circuits that compute $F,G$ then we can transform them to a circuit $E$ that computes $F \oplus G$ as in [parallelcompositioncircfig](){.ref}.
The circuit $E$ simply consists of two disjoint copies of the circuits $C$ and $D$, where we modify the labelling of the inputs of $D$ from `x_`$0$,$\ldots$,`x_`$n'-1$ to `x_`$n$,$\ldots$,`x_`$n+n'-1$ and the labelling of the outputs of $D$ from `y_`$0$,$\ldots$,`y_`$m'-1$ to `y_`$m$,$\ldots$,`y_`$m+m'-1$.
By the fact that $C$ and $D$ compute $F$ and $G$ respectively, we see that $E$ computes the function $F \oplus G: \{0,1\}^{n+n'}\rightarrow \{0,1\}^{m+m'}$ that on input $x \in \{0,1\}^{n+n'}$ outputs $F(x_0,\ldots,x_{n-1})G(x_n,\ldots,x_{n+n'-1})$.






## General Boolean circuits: a formal definition

We now define the notion of  _general_ Boolean circuits  that can use any set of gates and not just the NAND gate. 

> # {.definition title="Boolean circuits" #circuits-def}
Let $k$ be some number and $B$ be a subset of the functions from $\{0,1\}^k \rightarrow \{0,1\}$.
For every $n,m \in \N$, an $n$ input, $m$ output  _Boolean circuit_ with $B$-gates is a directed acyclic graph (DAG) $G$ over the vertex set $[t] = \{0,1\ldots,t-1\}$ and a labelling function $L:\{n,\ldots,t-1\} \rightarrow B$ such that: \
* Vertices $\{0,\ldots,n-1\}$ are _sources_: have no incoming edges.
* Vertices $\{t-m,\ldots,t-1 \}$ are _sinks_: have no out-going edges.
* Every non source vertex has exactly $k$ incoming edges.



![A Boolean circuit to compute the XOR function with NAND gates. In red are the corresponding variable names in the NAND program. (Figure needs to be updated to remove special output gates) /](../figure/NAND_circuit.png){#circuit-xor .class width=300px height=300px}


An $n$-input $m$-output circuit $C=(G,L)$ computes a function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ as follows.
For every input $x\in \{0,1\}^n$, we inductively define  the _value_ of every vertex based on its incoming edges:

1. For the  source vertices $\{0,\ldots,i-1\}$ we define $val(i) =x_i$ for all $i\in [n]$.

2. For a non source  vertex  $v$ and is labeled with $f\in B$, if its incoming neighbors are vertices $v_1,\ldots,v_k$
(sorted in order) and their values have all been set  then we let $\val(v)=f(\val(v_1),\ldots,\val(v_k))$.

3. Go back to step 2 until all vertices have values.



The _output_ of the circuit $C$ on input $x$, denoted by $C(x)$, is the string $y\in \{0,1\}^m$ such that for every $i\in \{0,\ldots,m-1\}$, $y_i$ is the value of the vertex $t-m+1$ where $t$ is the number of vertices.
We say that the circuit $C$ _computes the function $F$_ if for every $x\in \{0,1\}^n$,  $C(x)=F(x)$.


We have seen that  _every_ function $f:\{0,1\}^k \rightarrow \{0,1\}$ has a NAND program with at most $4\cdot 2^k$ lines, and hence [NAND-circ-thm](){.ref} implies the following theorem (see [NAND-all-circ-thm-ex](){.ref}):

> # {.theorem title="NAND programs simulate all circuits" #NAND-all-circ-thm}
For every function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ and $B$ a subset of the functions from $\{0,1\}^k$ to $\{0,1\}$, if we let $S(f)$ denote the smallest number of lines in a NAND program that computes $F$ and $S_B(f)$ denote the smallest number of vertices in a Boolean circuit with the basis $B$, then
$$
S(f) \leq (4\cdot 2^k)S_B(f)
$$

One can ask whether there is an equivalence here as well.
However, this is not the case.
For example if the set $B$ only consists of constant functions, then clearly a circuit whose gates are in $B$ cannot compute any non-constant function.
A slightly less boring example is if $B$ is the $\wedge$ (i.e. AND) function (as opposed to the $NAND$ function).
One can show that such a circuit will always output $0$ on the all zero inputs, and hence it  can never compute the simple negation function $\neg:\{0,1\} \rightarrow \{0,1\}$ such that $\neg(x)=1-x$.

We say that a subset $B$ of functions from $k$ bits to a single bit is a _universal basis_ if there is a "$B$-circuit" (i.e., circuit all whose gates are labeled with functions in $B$) that computes the $NAND$ function.
[universal-basis](){.ref} asks you to explore some examples of universal and non-universal bases.

## Neural networks

One particular basis we can use are _threshold gates_.
Given any vector $w= (w_0,\ldots,w_{k-1})$ of integers  and some integer $t$ (some or all of whom  could be negative),
the _threshold function corresponding to $w,t$_ is the function
$T_{w,t}:\{0,1\}^k \rightarrow \{0,1\}$ that maps $w$ to $1$ if and only if $\sum_{i=0} w_i x_i \geq t$.

The NAND function is of course itself a threshold gate, since $NAND(x,y)=1$ if and only if $-x-y \geq -1$. Threshold gates can be thought of as an approximation for    _neuron cells_ that make up the core of human and animal brains. To a first approximation, a neuron has $k$ inputs and a single output and the neurons  "fires" or "turns on" its output when those signals pass some threshold.^[Typically we think of an input to neurons as being a real number rather than a binary string, but  we can reduce to the binary case by  representing a real number in the binary basis, and multiplying the weight of the bit corresponding to the $i^{th}$ digit by $2^i$.]
Hence circuits with threshold gates are sometimes known as _neural networks_.
Unlike the cases above, when we considered $k$ to be a small constant, in such  neural networks we often do not put any bound on the number of inputs.
However, since any threshold function can be computed by a NAND program of $poly(k)$  lines (see [threshold-nand-ex](){.ref}), the  power of NAND programs and neural networks is not much different.



## Biological computing

Computation can be based on [biological  or chemical systems]((http://www.nature.com/nrg/journal/v13/n7/full/nrg3197.html)).
For example the [_lac_ operon](https://en.wikipedia.org/wiki/Lac_operon) produces the enzymes needed to digest lactose only if the conditions $x \wedge (\neg y)$ hold where $x$ is "lactose is present" and $y$ is "glucose is present".
Researchers have managed to [create transistors](http://science.sciencemag.org/content/340/6132/554?iss=6132), and from them the NAND function and other logic gates, based on DNA molecules (see also [transcriptorfig](){.ref}).
One motivation for DNA computing is to achieve  increased parallelism or storage density; another is to create "smart biological agents" that could perhaps be injected into bodies, replicate themselves, and fix or kill cells that were damaged by a disease such as cancer.
Computing in biological systems is not restricted of course to DNA.
Even larger systems such as [flocks of birds](https://www.cs.princeton.edu/~chazelle/pubs/cacm12-natalg.pdf) can be considered as computational processes.  

![Performance of DNA-based logic gates. Figure taken from paper of [Bonnet et al](http://science.sciencemag.org/content/early/2013/03/27/science.1232758.full), Science, 2013.](../figure/transcriptor.jpg){#transcriptorfig .class width=300px height=300px}

## Cellular automata and the game of life

As we will discuss later, cellular automata such as Conway's "Game of Life" can be used to simulate computation gates, see [gameoflifefig](){.ref}.

![An AND gate using a "Game of Life" configuration. Figure taken from [Jean-Philippe Rennard's paper](http://www.rennard.org/alife/CollisionBasedRennard.pdf).](../figure/game_of_life_and.png){#gameoflifefig .class width=300px height=300px}


## Circuit evaluation algorithm

A Boolean circuit is a labeled graph, and hence we can use the _adjacency list_ representation to represent an $s$-vertex circuit over an arity-$k$ basis $B$ by $s$ elements of $B$ (that can be identified with numbers in $[|B|]$) and $s$ lists of $k$ numbers in $[s]$.
Hence we can represent such a circuit by a string of length $O(s\log |B| + s \log s)$.
We can define  $CIRCEVAL_{B,s,n,m}$ to be the function  that takes as input a pair $(C,x)$ where $C$ is string describing an $s$-size  $n$-input $m$-output circuit over $B$, and $x\in \{0,1\}^n$, and returns the evaluation of $C$ over $n$.

[NAND-all-circ-thm](){.ref} implies that every circuit $C$ of $s$ gates over a $k$-ary basis $B$ can be transformed into a NAND program of $O(s\cdot 2^k)$ lines, and hence we can combine this transformation with last lecture's evaluation procedure for NAND programs to conclude that $CIRCEVAL$ can be evaluated in time $O(2^k s^3 poly(\log s))$.

### Advanced note: evaluating circuits in quasilinear time.

We can improve the evaluation procedure, and evaluate $s$-size constant arity circuits (or NAND programs) in time $O(s polylog(s))$.^[TODO: add details here, use the notion of oblivious routing to embed any graph in a universal graph.]



## The physical extended Church-Turing thesis

We've seen that  NAND gates can be implemented using very different systems in the physical world.
What about the reverse direction?
Can NAND programs simulate any physical computer?  


We can take a leap of faith and stipulate that NAND programs do actually encapsulate _every_ computation that we can think of.
Such a statement (in the realm of infinite functions, which we'll encounter in a couple of lectures) is typically attributed to Alonzo Church and Alan Turing, and in that context is  known as the _Church Turing Thesis_.
As we will discuss in future lectures, the Church-Turing Thesis is not a mathematical theorem or conjecture.
Rather, like theories in physics, the Church-Turing Thesis is about mathematically modelling the real world.
In the context of finite functions, we can make the following informal hypothesis or prediction:

>_If a function $F:\{0,1\}^n \rightarrow \{0,1\}^m$ can be computed in the physical world using $s$ amount of "physical resources" then it can be computed by a NAND program of roughly $s$ lines._

We call this hypothesis the **"Physical Extended Church-Turing Thesis"** or _PECTT_ for short.


There is no single universally-agreed-upon formalization of "$s$ physical resources",  but
we can approximate this notion by considering the size of any  physical computing device and the time it takes to compute the output.
That is we can stipulate that any function that can be computed by a device of volume $V$ and time $t$, must be computable by a NAND program that has at most $\alpha(Vt)^\beta$ lines for some constants $\alpha,\beta$.
The exact values for $\alpha,\beta$ are not so clear, but it is generally accepted that if $F:\{0,1\}^n \rightarrow \{0,1\}$ is an exponentially hard function, in the sense that it has not NAND program of fewer than, say, $2^{n/2}$ lines, then a demonstration of a physical device that can compute $F$ for moderate input lengths (e.g., $n=500$) would be a violation of the PECTT.

>__Advanced note: making things concrete:__
We can attempt at a more exact phrasing of the PECTT as follows.
Suppose that $Z$ is a physical system that accepts $n$ binary stimuli and has a binary output, and can be enclosed in a sphere of volume $V$.
We say that the system $Z$ _computes_ a function $F:\{0,1\}^n \rightarrow \{0,1\}$ within $t$ seconds if whenever we set the stimuli to some value  $x\in \{0,1\}^n$,  if we measure the output after $t$ seconds.
We can phrase the PECTT as stipulating  that whenever there exists such a system $Z$  computes $F$ within $t$ seconds,  there exists  a NAND program that computes $F$ of at most $\alpha(Vt)^2$ lines, where $\alpha$ is some normalization constant.^[We can also consider variants where we use [surface area](https://en.wikipedia.org/wiki/Holographic_principle) instead of volume, or use a different power than $2$.  However, none of these choices makes a qualitative difference  to the discussion below.]
In particular, suppose that $F:\{0,1\}^n \rightarrow \{0,1\}$ is a function that requires $2^n/(100n)>2^{0.8n}$ lines for any NAND program (we have seen that such functions exist in the last lecture).
Then the PECTT would imply that either the volume or the time of a system that computes $F$ will have to be at least $2^{0.2 n}/\sqrt{\alpha}$.
To fully make it  concrete, we need to decide on the units for measuring time and volume, and the normalization constant $\alpha$.
One  conservative choice is to assume that we could squeeze computation to the absolute physical limits (which are many orders of magnitude beyond current technology).
This corresponds to setting $\alpha=1$ and using the [Planck units](https://en.wikipedia.org/wiki/Planck_units) for volume and time.
The _Planck length_ $\ell_P$ (which is, roughly speaking, the shortest distance that can theoretically be measured) is roughly $2^{-120}$ meters.
The _Planck time_ $t_P$ (which is the time it takes for light to travel one Planck length) is about $2^{-150}$ seconds.
In the above setting, if a function $F$ takes, say, 1KB of input (e.g., roughly $10^4$ bits, which can encode a $100$ by $100$ bitmap image), and requires at least $2^{0.8 n}= 2^{0.8 \cdot 10^4}$ NAND lines to compute, then any physical system that computes it would require either volume of $2^{0.2\cdot  10^4}$ Planck length cubed, which is more than $2^{1500}$ meters cubed or take at least $2^{0.2 \cdot 10^4}$ Planck Time units, which is larger than $2^{1500}$ seconds.
To get a sense of how big that number is, note that the universe is only about $2^{60}$ seconds old, and its observable radius is only roughly $2^{90}$ meters.
This suggests that it is possible to _empirically falsify_ the PECTT by presenting a smaller-than-universe-size system that solves such a function.^[There are of course several hurdles to refuting the PECTT in this way, one of which is that we can't actually test the system on all possible inputs. However,  it turns we can get around this issue using notions such as  _interactive proofs_ and _program checking_ that we will see later in this course. Another, perhaps more salient problem, is that while we know many hard functions exist, at the moment there is _no single explicit function_ $F:\{0,1\}^n \rightarrow \{0,1\}$ for which we can _prove_ an $\omega(n)$ (let alone  $\Omega(2^n/n)$) lower bound  on the number of lines that a NAND program needs to compute it.]

### Attempts at refuting  the PECTT

One of the admirable traits of mankind is the refusal to accept limitations.
In the best case this is manifested by people achieving longstanding "impossible" challenges such as heavier-than-air flight, putting a person on the moon, circumnavigating the globe, or even resolving Fermat's Last Theorem.
In the worst-case it is manifested by people continually following the footsteps of previous failures to try to do proven-impossible tasks such as build a perpetual motion machine, trisect an angle with a compass and straightedge, or refute Bell's inequality.
The Physical Extended Church Turing thesis (in its various forms) has attracted both types of people.
Here are some physical devices that have been speculated to  achieve computational tasks that cannot be done by not-too-large  NAND programs:

* **Spaghetti sort:** One of the first lower bounds that Computer Science students encounter is that sorting $n$ numbers requires making $\Omega(n \log n)$ comparisons. The "spaghetti sort" is a description of a proposed "mechanical computer" that would do this faster. The idea is that to sort $n$ numbers $x_1,\ldots,x_n$, we could cut $n$ spaghetti noodles into lengths $x_1,\ldots,x_n$, and then if we simply hold them together in our hand and bring them down to a flat surface, they will emerge in sorted order. There are a great many reasons why this is not truly a challenge to the PECTT hypothesis, and I will not ruin the reader's fun in finding them out by her or himself.

* **Soap bubbles:** One function $F:\{0,1\}^n \rightarrow \{0,1\}$ that is conjectured to require a large number of NAND lines to solve is the _Euclidean Steiner Tree_ problem. This is the problem where one is given $m$ points in the plane $(x_1,y_1),\ldots,(x_m,y_m)$ (say with integer coordinates ranging from $1$ till $m$, and hence the list can be represented as a string of $n=O(m \log m)$ size) and some number $K$.  The goal is to figure out whether it is possible to connect all the points by line segments of total length at most $K$. This function is conjectured to be hard because it is _NP complete_ - a concept that we'll encounter later in this course - and it is in fact reasonable to conjecture that as $m$ grows, the number of NAND lines required to compute this function grows _exponentially_ in $m$, meaning that the PECTT would predict that if $m$ is sufficiently large (such as few hundreds or so) then no physical device could compute $F$.
Yet, some people claimed that there is in fact a very simple physical device that could solve this problem, that can be constructed using some wooden pegs and soap. The idea is that if we take two glass plates, and put $m$ wooden pegs between them in the locations $(x_1,y_1),\ldots,(x_m,y_m)$ then bubbles will form whose edges touch those pegs in the way that will minimize the total energy which turns out to be a function of the total length of the line segments.
The problem with this device of course is that nature, just like people, often gets stuck in "local optima". That is, the resulting configuration will not be one that achieves the  absolute minimum of the total energy but rather one that can't be improved with local changes.
[Aaronson](http://www.scottaaronson.com/papers/npcomplete.pdf) has carried out actual experiments (see [aaronsonsoapfig](){.ref}), and  saw that while this device often is successful for three or four pegs, it starts yielding suboptimal results once the number of pegs grows beyond that.

![Scott Aaronson [tests](http://www.scottaaronson.com/blog/?p=266) a candidate device for computing Steiner trees using soap bubbles.](../figure/aaronsonsoapbubble.jpg){#aaronsonsoapfig .class width=300px height=300px}

* **DNA computing.** People have suggested using the properties of DNA to do hard computational problems. The main advantage of DNA is the ability to potentially encode a lot of information in relatively small physical space, as well as operate on this information in a highly parallel manner. At the time of this writing, it was [demonstrated](http://science.sciencemag.org/content/337/6102/1628.full) that one can use DNA to store about $10^{16}$ bits of information in a region of radius about milimiter, as opposed to about $10^{10}$ bits with the best known hard disk technology. This does not posit a real challenge to the PECTT but does suggest that one should be conservative about the choice of constant and not assume that current hard disk + silicon technologies are the absolute best possible.^[We were extremely conservative in the suggested parameters for the PECTT, having assumed that as many as $\ell_P^{-2}10^{-6} \sim 10^{61}$ bits could potentially be stored in a milimeter radius region.]

* **Continuous/real computers.** The physical world is often described using continuous quantities such as time and space, and people have suggested that analog devices might have direct access to computing with real-valued quantities and would be inherently more powerful than discrete models such as NAND machines.
Whether the "true" physical world is continuous or discrete is an open question.
In fact, we do not even know how to precisely _phrase_ this question, let alone answer it. Yet, regardless of the answer, it seems clear that the effort to measure a continuous quantity grows with the level of accuracy desired, and so there is no "free lunch" or way to bypass the PECTT using such machines (see also [this paper](http://www.cs.princeton.edu/~ken/MCS86.pdf)). Related to that are proposals  known as "hypercomputing" or  "Zeno's computers" which attempt to use the continuity of time by doing the first operation in one second, the second one in half a second, the third operation in a quarter second and so on..  These fail for a  similar reason to the one guaranteeing that Achilles will eventually catch the tortoise despite the  original Zeno's paradox.

* **Relativity computer and time travel.** The formulation above assumed the notion of time, but under the theory of relativity time is in the eye of the observer. One approach to solve hard problems is to leave the computer to run for a lot of time from _his_ perspective, but to ensure that this is actually a short while from _our_ perspective. One approach to do so is for the user to start the computer and then go for a quick jog at close to the speed of light before checking on its status. Depending on how fast one goes, few seconds from the point of view of the user might correspond to centuries in computer time (it might even finish updating its Windows operating system!). Of course the catch here is that the energy required from  the user is proportional to how close one needs to get to the speed of light. A more interesting proposal is to use time travel via _closed timelike curves (CTCs)_. In this case we could run an arbitrarily long computation by doing some calculations, remembering  the current state, and the travelling back in time to continue where we left off. Indeed, if CTCs exist then we'd probably have to revise the PECTT (though in this case I will simply travel back in time and edit these notes, so I can claim I never conjectured it in the first place...)


* **Humans.** Another computing system that has been proposed as a counterexample to the PECTT is a 3 pound computer of  about 0.1m radius, namely the human brain. Humans can walk around, talk, feel, and do others things that are not commonly  done by NAND programs, but can they compute partial functions that NAND programs cannot?
There are certainly computational tasks that _at the moment_  humans do better than computers (e.g., play some [video games](http://www.theverge.com/2016/11/4/13518210/deepmind-starcraft-ai-google-blizzard), at the moment), but based on our current understanding of the brain, humans (or other animals) have no _inherent_ computational advantage over computers.
The brain has about $10^{11}$ neurons, each operating in a speed of about $1000$ operations per seconds. Hence a rough first approximation is that a NAND program of about $10^{14}$ lines could simulate one second of a brain's activity.^[This is a very rough approximation that could be wrong to a few orders of magnitude in either direction. For one, there are other structures in the brain apart from neurons that one might need to simulate, hence requiring higher overhead. On ther other hand, it is by no mean clear that we need to fully clone the brain in order to achieve the same computational tasks that it does.]
Note that the fact that such a NAND program (likely) exists does not mean it is easy to _find_ it.
After all, constructing this program took evolution billions of years.
Much of the recent efforts in artificial intelligence research is focused on finding programs that replicate some of the brain's capabilities and they take massive computational effort to discover, these programs often turn out to be much smaller than the pessimistic estimates above. For example, at the time of this writing, Google's [neural network for machine translation](https://arxiv.org/pdf/1609.08144.pdf) has about $10^4$ nodes (and can be simulated by a NAND program of comparable size). Philosophers, priests and many others have since time immemorial argued that there is something about humans that cannot be captured by  mechanical devices such as computers; whether or not that is the case, the evidence is thin that humans can perform computational tasks that are inherently impossible to achieve by computers of similar complexity.^[There are some well known scientists that have [advocated](http://www.telegraph.co.uk/science/2017/03/14/can-solve-chess-problem-holds-key-human-consciousness/) that humans have inherent computational advantages over computers. See also [this](https://arxiv.org/abs/1508.05929).]


* **Quantum computation.** The most compelling attack on the Physical Extended Church Turing Thesis comes from the notion of _quantum computing_.
The idea was initiated by the observation that systems with strong quantum effects are very hard to simulate on a computer.
Turning this observation on its head, people have proposed using such systems to perform computations that we do not know how to do otherwise.
We will discuss quantum computing in much more detail later in this course.
Modeling it will  essentially involve extending the NAND programming language to the "QNAND" programming language that has one more (very special) operation.
However, the main take away is that while quantum computing does suggest we need to amend the PECTT, it does _not_ require a complete revision of our worldview. Indeed, almost all of the content of this course remains the same whether the underlying computational model is the "classical" model of NAND programs or the quantum model of QNAND programs (also known as _quantum circuits_).

## Lecture summary

* NAND gates can be implemented by a variety of physical means.

* NAND programs are equivalent (up to constants) to Boolean circuits using any finite universal basis.

* By a leap of faith, we could hypothesize that the number of lines in the smallest NAND program for a function $F$ captures roughly the amount of physical resources required to compute $F$. This statement is known as the _Physical Extended Church-Turing Thesis (PECTT)_.

* NAND programs capture a surprisingly wide array of computational models. The strongest currently known challenge to the PECTT comes from the potential for using quantum mechanical effects to speed-up computation, a model known as _quantum computers_.

## Exercises

> # {.exercise title="Relating NAND circuits and NAND programs" #nand-circuits-thm-ex}
Prove [NAND-circ-thm](){.ref}.

> # {.exercise title="Simulating all circuits with NAND programs" #NAND-all-circ-thm-ex}
Prove [NAND-all-circ-thm](){.ref}


> # {.exercise title="Universal basis" #universal-basis}
For every one of the following sets, either prove that it is a universal basis or prove that it is not.
1. $B = \{ \wedge, \vee, \neg \}$. (To make all of them be function on two inputs, define $\neg(x,y)=\overline{x}$.) \
2. $B = \{ \wedge, \vee \}$. \
3. $B= \{ \oplus,0,1 \}$ where $\oplus:\{0,1\}^2 \rightarrow \{0,1\}$ is the XOR function and $0$ and $1$ are the constant functions that output $0$ and $1$. \
4. $B = \{ LOOKUP_1,0,1 \}$ where $0$ and $1$ are the constant functions as above and  $LOOKUP_1:\{0,1\}^3 \rightarrow \{0,1\}$ satisfies $LOOKUP_1(a,b,c)$ equals $a$ if $c=0$ and equals $b$ if $c=1$.

> # {.exercise title="Bound on universal basis size (challenge)" #universal-bound}
Prove that for every subset $B$ of the functions from $\{0,1\}^k$ to $\{0,1\}$,
if $B$ is universal then there is a $B$-circuit of at most $O(2^k)$ gates to compute the $NAND$ function.^[TODO: verify it's true, and check how to do this.]

> # {.exercise title="Threshold using NANDs" #threshold-nand-ex}
Prove that for every $w,t$, the function $T_{w,t}$ can be computed by a NAND program of at most $O(k^3)$ lines.^[TODO: check the right bound, and give it as a challenge program. Also say the conditions under which this can be improved to $O(k)$ or $\tilde{O}(k)$.]

## Bibliographical notes

Scott Aaronson's blog post on how [information is physical](http://www.scottaaronson.com/blog/?p=3327) is a good discussion on issues related to the physical extended Church-Turing Physics.
Aaronson's [survey on  NP complete problems and physical reality](http://www.arxiv.org/abs/quant-ph/0502072) is also a great source for some of these issues, though might be easier to read after we reach the lectures on NP and NP completeness.

## Further explorations

Some topics related to this lecture that might be accessible to advanced students include:

* The notion of the fundamental limits for information and their interplay with physics, is still not well understood.

## Acknowledgements
