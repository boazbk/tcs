% Mathematical background
% Boaz Barak

# Mathematical Background { #chapmath }


> # { .objectives }
* Recall basic mathematical notions such as sets, functions, numbers, logical operators and quantifiers, strings, and graphs.
* Rigorously define Big-$O$ notation.
* Proofs by induction.
* Practice with reading mathematical _definitions_, _statements_, and _proofs_.
* Transform an intuitive argument into a rigorous proof.



>_"When you have mastered numbers, you will in fact no longer be reading numbers, any more than you read words when reading books. You will be reading meanings."_, W. E. B. Du Bois


>_"I found that every number, which may be expressed from one to ten, surpasses the preceding by one unit: afterwards the ten is doubled or tripled  ...  until a hundred; then the hundred is doubled and tripled in the same manner as the units and the tens ... and so forth to the utmost limit of numeration."_,  Muhammad ibn Mūsā al-Khwārizmī, 820, translation by Fredric Rosen, 1831.



<!---
>_"Young man, in mathematics you don't understand things. You just get used to them."_, John von Neumann
--->



In this chapter, we  review some of the mathematical concepts that we will use in this course.
Most of these are not very complicated, but do require some practice and exercise to get comfortable with.
If you have not previously encountered some of these concepts, there are several excellent freely-available resources online that cover them, see the "Bibliographical Notes" section ([notesmathchap](){.ref}).



## A mathematician's apology

Before explaining the math background, perhaps I should explain why is this course so "mathematically heavy".
After all, this is supposed to be a course about _computation_; one might think we should be talking mostly about  _programs_, rather than more "mathematical" objects such as  _sets_, _functions_, and _graphs_, and doing more _coding_ on an actual computer than writing mathematical proofs with pen and paper.
So, why are we doing so much math in this course?
Is it just some form of hazing? Perhaps a revenge of the ["math nerds" against the "hackers"](https://blog.smartbear.com/careers/math-nerds-vs-code-monkeys-should-computer-science-classes-be-more-practical/)?

At the end of the day, mathematics is simply a language for modeling concepts in a precise and unambiguous way.
In this course,  we will be mostly interested in the concept of _computation_.
For example, we will look at questions such as  _"is there an efficient algorithm to find the prime factors of a given integer?"_.^[Actually, scientists currently do not know the answer to this question, but we will see that settling it in either direction has very interesting applications touching on areas as far apart as Internet security and quantum mechanics.]
To even _phrase_ such a question, we need to give a precise _definition_ of the notion of an _algorithm_, and of what it means for an algorithm to be _efficient_.
Also, if the answer to this or similar questions turns out to be _negative_, then this cannot be shown by simply writing and executing some code.
After all, there is no empirical experiment that will prove the _nonexistence_ of an algorithm.
Thus, our only way to show this type of _negative result_ is to use _mathematical proofs_.
So you can  see why our main tools in this course will be mathematical proofs and definitions.

##  This chapter: a reader's manual   { #manualbackground}

Depending on your background, you can approach this chapter in two different ways:

* If you already have taken some proof-based courses, and are very familiar with the notions of discrete mathematics, you can take a quick look at [secmathoverview](){.ref} to see the main tools we will use, [notationsec](){.ref} for our notation and conventions, and then skip ahead to the rest of this book. Alternatively, you can  sit back, relax, and read this chapter just to get familiar with our notation, as well as to enjoy (or not) my philosophical musings and attempts at humor. You might also want to start brushing up on _discrete probability_, which we'll use later in this course.



* If your background is not as extensive, you should lean forward, and read this chapter with a pen and paper handy, making notes and working out derivations as you go along. We cannot fit a semester-length discrete math course in a single chapter, and hence will be necessarily brief in our discussions. Thus you might want to occasionally pause to watch some discrete math lectures, read some of the resources mentioned in [notesmathchap](){.ref}, and do some exercises to make sure you internalized the material.






## A quick overview of mathematical prerequisites { #secmathoverview }



The main notions we will use in this course are the following:

* __Proofs:__ First and foremost, this course will involve a heavy dose of formal mathematical reasoning, which includes mathematical _definitions_, _statements_, and _proofs_.

* __Sets:__ The basic set _relationships_ of membership ($\in$), containment ($\subseteq$), and set _operations_, principally union, intersection, set difference and Cartesian product ($\cup,\cap,\setminus$ and $\times$).

* __Tuples and strings:__ The set $\Sigma^k$ of length-$k$ strings/lists over elements in $\Sigma$, where $\Sigma$ is some finite set which is called the _alphabet_ (quite often $\Sigma = \{0,1\}$). We use $\Sigma^*$ for the set of all strings of finite length.

* __Some special sets:__ The set $\N$ of natural numbers. We will index from zero in this course and so write $\N = \{0,1,2,\ldots \}$. We will use $[n]$ for the set $\{0,1,2,\ldots,n-1\}$. We use $\{0,1\}^*$ for the set of all binary strings and $\{0,1\}^n$ for the set of strings of length $n$. If $x$ is a string of length $n$, then we refer to its coordinate by $x_0,\ldots,x_{n-1}$.

* __Functions:__ The _domain_ and _codomain_ of a function, properties such as being _one-to-one_ (also known as _injective_) or _onto_ (also known as _surjective_) functions, as well as  _partial functions_ (that, unlike standard or "total" functions, are not necessarily defined on all elements of their domain).

* __Logical operations:__ The operations AND, OR, and NOT ($\wedge,\vee,\neg$) and the quantifiers "there exists" and "for all" ($\exists$,$\forall$).

* __Basic combinatorics:__ Notions such as $\binom{n}{k}$ (the number of $k$-sized subsets of a set of size $n$).

* __Graphs:__ Undirected and directed graphs, connectivity, paths, and cycles.

* __Big-$O$ notation:__ $O,o,\Omega,\omega,\Theta$ notation for analyzing asymptotic growth of functions.

* __Discrete probability:__ Later on in we will use _probability theory_, and specifically probability over _finite_ samples spaces such as tossing $n$ coins, including notions such as _random variables_, _expectation_, and _concentration_.  We will only use  probability theory in the second half of this text, and will review it  beforehand. However, probabilistic reasoning is a subtle (and extremely useful!) skill, and it's always good to start early in acquiring it.


In the rest of this chapter we briefly review the above notions.
This is partially to remind the reader and reinforce material that might not be fresh in your mind, and partially to introduce our notation and conventions which might occasionally differ from those you've encountered before.



## Reading mathematical texts

Mathematical texts, such as this book, can often be intimidating at first, as they use a lot of mathematical jargon that can seem dense and confusing to the uninitiated.
Mathematicians use jargon for the same reason that it is used in many other professions such engineering, law, medicine, etc.
We want to make terms _precise_ and introduce shorthand for concepts that are frequently reused.
Mathematical text tends to "pack a lot of punch" per sentence, and so the key is to read it slowly and carefully, parsing each symbol at a time.

::: {.remark title="Don't be scared of Jargon!" #jargon}
Mathematical Jargon can be kind of scary initially. A  statement such as $\forall_{x\in \mathbb{R}, \epsilon>0} \exists_{a,b \in \N} |x - \tfrac{a}{b}| < \epsilon$ might be quite frightening to the uninitiated.
But as you get more experience in reading mathematical texts, you will see that the jargon is no longer an issue, and you spend most of your time grappling with the actual ideas in the text.

This is no different than programming. For example, even the code of the simple "Hello World" program in Java can be quite intimidating to newcomers, containing great many terms that look scary and inscrutable, but as you work in Java, you  quickly get used  to these quirks of jargon.

```java
public class HelloWorld
{
	public static void main(String[] args) {
		System.out.println("Hello World!");
	}
}
```
:::

Dealing with mathematical text is in many ways not so different from dealing with any other complex text, whether it's a legal argument, a philosophical treatise, an English Renaissance play, or even the source code of an operating system.
You should not expect it to be clear in a first reading, but you need not despair.
Rather you should engage with the text, trying to figure out both the high level intentions as well as the underlying details.
Luckily, compared to philosophers or even programmers, mathematicians have a greater discipline of introducing definitions in linear order,  making sure that every new concept is defined only in terms of  previously defined notions.


The basic components of a mathematical text are __definitions__, __assertions__ and __proofs__.

### Definitions

Mathematicians often define new concepts in terms of old concepts.  Here is an example of a definition:

> # {.definition title="Perfect Square" #perfectsquaredef}
A natural number $n$ is  a _perfect square_ if there exists a natural number $k$ such that $n = k\cdot k$.

[perfectsquaredef](){.ref} uses the concept  of a natural number, and the concept of multiplication, to define the new term "perfect square".

When you see a new definition or concept, always ask yourself the following questions:

1. What is the intuitive notion that this definition aims at modeling?

2. How is the new concept  defined in terms of other concepts?

3. Which of these prior concepts am I already familiar with, and which ones do I still need to look up?

4. Can I come up with examples of objects that satisfy this definition? and examples of objects that do not?

As you read through the rest of this chapter and this text, try to ask yourself  the questions 1-4 above every time that you encounter a new definition.


::: { .pause }
You can try this out for the definition of a "perfect square". Can you come up with examples of numbers that are perfect squares, and examples of numbers that are not perfect squares? How do you _prove_ that a number is _not_ a perfect square.

You can also try to consider more refined questions such as finding out if there exists a perfect square that is the sum of two other perfect squares. You can also try to see how you would define notions such as being a "perfect cube". (Can you try to think if  there is a perfect cube which is the sum of two other perfect cubes?)
:::


::: {.remark title="Ifs and equalities in definitions" #ifindef}
The meaning of "if" is subtly different in the context of a _definition_ than it is in the context of a standalone mathematical statement. When we say that we define $n$ to be a perfect square if $n=k^2$ for some $k\in \N$, we are _defining_ the new property "perfect square" to be equivalent to the property that $n=k^2$ for some $k\in \N$.
Since this is the _definition_ of this property, it means that $n$ is in fact a perfect square  _if and only if_  $m=k^2$ for some $k\in \N$.
We could have also said that we define $n$ to be a perfect square _if and only if_ (or use the abbreviation _iff_) $n=k^2$ for some $k\in \N^2$. We will sometimes use "iff" instead of "if" in definitions when it helps clarity, but since mathematicians  typically use "if" in such cases, we will often follow this convention as well.

Similarly, the equality symbol "$=$" plays a subtly different role in the context of a definition than it does elsewhere. When we say something like "we define $y= \sqrt{x}$" what we really mean is that we are _assigning_ the value $\sqrt{x}$ to $y$, as opposed to _asserting_ that $y$ equals $\sqrt{x}$. To compare with programming languages, in the context of a definition, the equality sign $=$ plays the role analogous to the assignment operator `=` in languages such as C, Python, or Javascript, while in other contexts it plays the role analogous to the "equal to" operator `==`.

A definition does not have to occur only in the context of a formal "Definition" environment. Whenever you see text such as "we define X as", "let Y be", or "we denote by Z", this is a sign that a new term is being defined.
:::

### Assertions: Theorems, lemmas, claims

These are true statements about the concepts that we defined. For example, here is a true statement:

> # {.lemma #perfectsquarelem}
For every perfect square $a$ and perfect square $b$, $a\cdot b$ is a perfect square.

Deciding whether to call a particular statement a "Theorem", a "Lemma" or a "Claim" is a judgement call, and does not make a mathematical difference. All three correspond to true statements which can be proven. The difference is that a _Theorem_ refers to a significant result, that we would want to remember and highlight.  A _Lemma_ often refers to a  technical result, that is not necessarily important in its own right, but can be often very useful in proving other theorems. A _Claim_ is a "throw away" statement, that we need to use in order to prove some other bigger results, but do not care so much about for its own sake.

### Proofs

These are the justifications that demonstrates that our theorems. We discuss proofs more in [proofsbackgroundsec](){.ref} below, but the mathematical standard of proof is very high. Namely we need an "airtight" argument that demonstrates that the statement is true beyond a shadow of a doubt.
For example, just checking that [perfectsquarelam](){.ref} is true for the $a=25$ and $b=4$ (in which case $a\cdot b  =100$ is indeed a perfect square) doesn't cut it. In contrast, here is a valid proof for [perfectsquarelam](){.ref}:


::: {.proof data-ref="perfectsquarelem"}
Let $a$ and $b$ be perfect squares. Then by the definition of a perfect square, there exist natural numbers $a',b'$ such that $a=a' \cdot a'$ and $b= b' \cdot b'$.
Define $c = a\cdot b$. Then by the above

$$
c = (a' \cdot a')\cdot(b' \cdot b') = (a' \cdot b') \cdot (a' \cdot b') \label{eqcommutativeperfectsquare}
$$
.^[The last inequality follows from the associativity and commutativity of multiplication; i.e., the fact that $(x \cdot y) \cdot z = x\cdot (y \cdot z)$ and $x\cdot y = y \cdot x$ for every numbers $x,y,z$). These are the kind of properties that in a course of this level we can assume that the reader knows and can "fill in the blank", and hence do not need to state explicitly. However, if you have any doubt, always err on the side of supplying more, rather than less, detail.]

Since $a',b'$ are natural numbers, $c' = a'\cdot b'$ is a natural number as well and hence [eqcommutativeperfectsquare](){.eqref} implies that $c = c' \cdot c'$ is a perfect square.
:::

As mentioned in the preface, as a general rule, it is more important you understand the  __definitions__ than the __theorems__, and it is more important you understand  a __theorem statement__  than its __proof__.



### Example: Defining a one to one function

Here is a mathematical definition which you may have encountered in the past (and will encounter again shortly):


> # {.definition title="One to one function" #onetoonedef}
A function $f:S \rightarrow T$ is _one to one_ if for every two elements $x,x' \in S$, if $x \neq x'$ then  $f(x) \neq f(x')$.

This definition captures a simple concept, but even so it uses quite a bit of notation.
When reading this definition, or any other piece of mathematical text, it is often useful to annotate it with a pen as you're going through it, as in [onetoonedefannotatedef](){.ref}.
For every identifier you encounter (for example $f,S,T,x,x'$ in this case), make sure that you realize what sort of object is it: is it a set, a function, an element, a number, a gremlin?
Make sure you understand how  the identifiers are _quantified_.
For example, in [onetoonedef](){.ref} there is a _universal_ or "for all" (sometimes denotes by $\forall$) quantifier over pairs $(x,x')$ of distinct elements in $S$.
Finally, and most importantly, make sure that aside from being able to parse the definition formally, you also have an intuitive understanding of what is it that the text  is actually saying.
For example, [onetoonedef](){.ref} says that a one to one function is a function where every output is obtained by a unique input.



![An annotated form of [onetoonedef](){.ref}, marking which type is every object, and with a doodle explaining what the definition says.](../figure/onetoonedef.png){#onetoonedefannotatedef .class width=300px height=300px}

Reading mathematical texts in this way takes time, but it gets easier with practice.
Moreover, this is one of the most transferable skills you could take from this course.
Our world is changing rapidly, not just in the realm of technology, but also in many other human endeavors, whether it is medicine, economics, law or even culture.
Whatever your future aspirations, it is likely that you will encounter texts that use new concepts that you have not seen before (for semi-random recent examples from current "hot areas", see [alphagozerofig](){.ref} and [zerocashfig](){.ref}).
Being able to internalize and then apply new definitions can be hugely important.
It is a skill that's much easier to acquire in the relatively safe and stable  context of a mathematical course, where one at least has  the guarantee that the concepts are fully specified, and you have access to your teaching staff for questions.


![A snippet from the "methods" section of the  ["AlphaGo Zero" paper](https://goo.gl/k8pVpL) by Silver et al, _Nature_, 2017. ](../figure/alphagozero.png){#alphagozerofig .class width=300px height=300px}

![A snippet from the ["Zerocash" paper](http://zerocash-project.org/paper) of Ben-Sasson et al, that forms the basis of the cryptocurrency startup Zcash.](../figure/zerocash.png){#zerocashfig .class width=300px height=300px}




## Basic discrete math objects

We now quickly review some of the mathematical objects (the "basic data structures" of mathematics, if you will) we use  in this course.

### Sets

A _set_ is an unordered collection of objects.
For example, when we write $S = \{ 2,4, 7 \}$, we mean that $S$ denotes the set that contains the numbers $2$, $4$, and $7$.
(We use the notation "$2 \in S$" to denote that $2$ is an element of $S$.)
Note that the set $\{ 2, 4, 7 \}$ and $\{ 7 , 4, 2 \}$ are identical, since they contain the same elements.
Also, a set either contains an element or does not contain it -- there is no notion of containing it  "twice" -- and so we could even write the same set $S$ as  $\{ 2, 2, 4, 7\}$ (though that would be a little weird).
The _cardinality_ of a finite set $S$, denoted by $|S|$, is the number of  elements it contains.^[Later in this course we  will discuss how to extend the notion of cardinality to _infinite_ sets.]
So, in the example above, $|S|=3$.
A set $S$ is a _subset_ of a set $T$, denoted by $S \subseteq T$, if every element of $S$ is also an element of $T$. (We can also describe this by saying that  $T$ is a _superset_ of $S$.)
For example, $\{2,7\} \subseteq \{ 2,4,7\}$.
The set that contains no elements is known as the _empty set_ and it is denoted by $\emptyset$.


We can define sets by either listing all their elements or by writing down a rule that they satisfy such as
$$
\text{EVEN} = \{ x  \;:\; \text{ $x=2y$ for some non-negative integer $y$} \} \;.
$$

Of course there is more than one way to write the same set, and often we will use intuitive notation listing a few examples that illustrate the rule.
For example,  we can also define $\text{EVEN}$ as

$$
\text{EVEN} = \{ 0,2,4, \ldots \} \;.
$$

Note that a set can be either finite  (such as the set $\{2,4,7\}$ ) or infinite (such as the set $\text{EVEN}$).
Also, the elements of a set don't have to be numbers.
We can talk about the sets such as the set $\{a,e,i,o,u \}$ of all the vowels in the English language, or the  set $\{$ `New York`, `Los Angeles`, `Chicago`, `Houston`, `Philadelphia`, `Phoenix`, `San Antonio`, `San Diego`, `Dallas` $\}$  of all cities in the U.S. with population more than  one million  per the 2010 census.
A set can even have other sets as elements, such as the set $\{ \emptyset, \{1,2\},\{2,3\},\{1,3\} \}$ of all even-sized subsets of $\{1,2,3\}$.

__Operations on sets:__ The _union_ of two sets $S,T$, denoted by $S \cup T$, is the set that contains all elements that are either in $S$ _or_ in $T$. The _intersection_ of $S$ and $T$, denoted by $S \cap T$, is the set of elements that are both in $S$ _and_ in $T$. The _set difference_ of $S$ and $T$, denoted by $S \setminus T$ (and in some texts  also by $S-T$), is the set of elements that are in $S$ but _not_ in $T$.

__Tuples, lists, strings, sequences:__ A _tuple_ is an _ordered_ collection of items. For example $(1,5,2,1)$ is a tuple with four elements (also known as a $4$-tuple or quadruple).
Since order matters, this is not the same tuple as the $4$-tuple $(1,1,5,2)$ or the $3$-tuple $(1,5,2)$. A $2$-tuple is also known as a _pair_.
We use the terms _tuples_ and _lists_ interchangeably.
A tuple where every element comes from some finite set $\Sigma$ (such as $\{0,1\}$) is also known as a _string_.
Analogously to sets, we denote the _length_ of a tuple $T$ by $|T|$.
Just like sets, we can also think of infinite analogues of tuples, such as the ordered collection $(1,2,4,9,\ldots )$ of all perfect squares.
Infinite ordered collections are known as _sequences_; we might sometimes use the term "infinite sequence" to emphasize this, and use "finite sequence" as a synonym for a tuple.^[We can identify a sequence $(a_0,a_1,a_2,\ldots)$ of elements in some set $S$ with a _function_ $A:\N \rightarrow S$ (where $a_n = A(n)$ for every $n\in \N$). Similarly, we can identify a $k$-tuple $(a_0,\ldots,a_{k-1})$ of elements in $S$ with a function $A:[k] \rightarrow S$.]


__Cartesian product:__ If $S$ and $T$ are sets, then their _Cartesian product_, denoted by $S \times T$, is the set of all ordered pairs $(s,t)$ where $s\in S$ and $t\in T$.
For example, if $S = \{1,2,3 \}$ and $T = \{10,12 \}$, then $S\times T$ contains the $6$ elements $(1,10),(2,10),(3,10),(1,12),(2,12),(3,12)$.
Similarly if $S,T,U$ are sets then $S\times T \times U$ is the set of all ordered triples $(s,t,u)$ where $s\in S$, $t\in T$, and $u\in U$.
More generally, for every positive integer $n$ and sets $S_0,\ldots,S_{n-1}$, we denote by $S_0 \times S_1 \times \cdots \times S_{n-1}$ the set of ordered $n$-tuples $(s_0,\ldots,s_{n-1})$ where $s_i\in S_i$ for every $i \in \{0,\ldots, n-1\}$.
For every set $S$, we  denote the set $S\times S$ by $S^2$, $S\times S\times S$ by $S^3$, $S\times S\times S \times S$ by $S^4$, and so on and so forth.

### Sets in Python (optional)

To get more comfortable with sets, one can also play with the `set` data structure in Python:^[The `set` data structure only corresponds to _finite_ sets; infinite sets are much  more cumbersome to handle in programming languages, though mechanisms such as [Python generators](https://wiki.python.org/moin/Generators) and [lazy evaluation](https://goo.gl/EJV4L3) in general can be helpful.]

```python
A = { 7 , 10 , 12}
B = {12 , 8 , 5 }
print(A==B)
# False
print(A=={10,7,7,12})
# True

def intersect(S,T):
    return {x for x in S if x in T}

print(intersect(A,B))
# {12}

def contains(S,T):
    return all({x in T for x in S})

print(contains(A,B))
# False

print(contains({2,8,8,12},{12,8,2,34}))
# True

def product(S,T):
    return {(s,t) for s in  S for t in  T}

print(product(A,B))
# {(10, 8), (10, 5), (7, 12), (12, 12), (10, 12), (12, 5), (7, 5), (7, 8), (12, 8)}
```


### Special sets { #specialsets }

There are several sets that we will use in this course time and again, and so find it useful to introduce explicit notation for them.
For starters we define

$$
\N = \{ 0, 1,2, \ldots \}
$$
to be the set of all _natural numbers_, i.e., non-negative integers.
For any natural number $n$, we define the set $[n]$ as $\{0,\ldots, n-1\} = \{ k\in \N : k < n \}$.^[We start our indexing of both $\N$ and $[n]$ from $0$, while many other  texts index  those sets from $1$. Starting from zero or one is simply a convention that doesn't make much difference, as long as one is consistent about it.]

We will also occasionally use the set $\Z=\{\ldots,-2,-1,0,+1,+2,\ldots \}$ of (negative and non-negative) _integers_,^[The letter Z stands for the German word "Zahlen", which means _numbers_.] as well as the set $\R$ of _real_ numbers. (This is the set that includes not just the integers, but also fractional and even irrational numbers; e.g., $\R$ contains numbers  such as $+0.5$, $-\pi$, etc.)
We denote by $\R_+$  the set $\{ x\in \R : x > 0 \}$ of _positive_  real numbers.
This set is sometimes also denoted as $(0,\infty)$.

__Strings:__ Another set we will use time and again is

$$
\{0,1\}^n = \{ (x_0,\ldots,x_{n-1}) \;:\; x_0,\ldots,x_{n-1} \in \{0,1\}  \}
$$
which is the set of all $n$-length binary strings for some natural number $n$.
That is $\{0,1\}^n$ is the set of all $n$-tuples  of zeroes and ones.
This is consistent with our notation above: $\{0,1\}^2$ is the Cartesian product $\{0,1\} \times \{0,1\}$, $\{0,1\}^3$ is the product $\{0,1\} \times \{0,1\} \times \{0,1\}$ and so on.


We  will write the string $(x_0,x_1,\ldots,x_{n-1})$ as simply $x_0x_1\cdots x_{n-1}$ and so for example

$$
\{0,1\}^3 = \{ 000 , 001, 010 , 011, 100, 101, 110, 111 \} \;.
$$

For every string $x\in \{0,1\}^n$ and $i\in [n]$, we write $x_i$ for the $i^{th}$ coordinate of $x$.
If $x$ and $y$ are strings, then $xy$  denotes their _concatenation_.
That is, if $x \in \{0,1\}^n$ and $y\in \{0,1\}^m$, then $xy$ is equal to the string $z\in \{0,1\}^{n+m}$ such that for $i\in [n]$, $z_i=x_i$ and for $i\in \{n,\ldots,n+m-1\}$, $z_i = y_{i-n}$.

We will also often talk about the set of binary strings of _all_ lengths, which is

$$
\{0,1\}^* = \{ (x_0,\ldots,x_{n-1}) \;:\; n\in\N \;,\;, x_0,\ldots,x_{n-1} \in \{0,1\} \} \;.
$$

Another way to write this set is as
$$
\{0,1\}^* = \{0,1\}^0 \cup \{0,1\}^1 \cup \{0,1\}^2 \cup \cdots
$$
or more concisely as

$$
\{0,1\}^* = \cup_{n\in\N} \{0,1\}^n \;.
$$

The set $\{0,1\}^*$ contains also the "string of length $0$" or "the empty string", which we will denote by $\mathtt{""}$.^[In using this notation we follow the convention of many  programming languages. Other texts sometimes use $\epsilon$ or $\lambda$ to denote the empty string. However, this doesn't matter much since we will rarely encounter this "edge case".]


__Generalizing the star operation:__ For every set $\Sigma$, we define

$$\Sigma^* = \cup_{n\in \N} \Sigma^n \;.$$
For example, if $\Sigma = \{a,b,c,d,\ldots,z \}$ then $\Sigma^*$ denotes the set of all finite length strings over the alphabet a-z.

__Concatenation:__ As mentioned in [specialsets](){.ref}, the _concatenation_ of two strings $x\in \Sigma^n$ and $y\in \Sigma^m$ is the $(n+m)$-length string $xy$ obtained by writing $y$ after $x$.


### Functions {#functionsec }

If $S$ and $T$ are nonempty sets, a _function_ $F$ mapping $S$ to $T$, denoted by $F:S \rightarrow T$, associates with every element $x\in S$ an element $F(x)\in T$.
The set $S$ is known as the _domain_ of $F$ and the set $T$ is known as the  _codomain_ of $F$.
The _image_ of a function $F$ is the set $\{ F(x) \;|\; x\in S\}$ which is the subset of $F$'s codomain consisting of all  output elements that are mapped from some input.^[Some texts use _range_ to denote the image of a function, while other texts use _range_ to denote the codomain of a function. Hence we will avoid using the term "range" altogether.]
As in the case of  sets, we can write a function either by listing the table of all the values it gives for elements in $S$ or by using a rule.
For example if $S = \{0,1,2,3,4,5,6,7,8,9 \}$ and $T = \{0,1 \}$, then the table below defines a function $F: S \rightarrow T$.
Note that this function is the same as the function defined by the rule $F(x)= (x \mod 2)$.^[For two natural numbers $x$ and $a$, $x \mod a$ (where $\mod$ is shorthand for ["modulo"](https://goo.gl/b7Fdzm)) denotes the _remainder_ of $x$ when it is divided by $a$. That is, it is the number $r$ in $\{0,\ldots,a-1\}$ such that $x = ak +r$ for some integer $k$. We sometimes also use the notation $x = y (\mod a)$ to denote the assertion that $x \mod a$ is the same as $y \mod a$.]

| Input | Output |
|:------|:-------|
| 0     | 0      |
| 1     | 1      |
| 2     | 0      |
| 3     | 1      |
| 4     | 0      |
| 5     | 1      |
| 6     | 0      |
| 7     | 1      |
| 8     | 0      |
| 9     | 1      |

\



If $F:S \rightarrow T$ satisfies that $F(x)\neq F(y)$ for all $x \neq y$ then we say that $F$ is _one-to-one_ (also known as an _injective_ function or simply an _injection_).
If $F$ satisfies that for every $y\in T$ there is some $x\in S$ such that $F(x)=y$ then we say that $F$ is _onto_ (also known as a _surjective_ function or simply a _surjection_).
A  function that is both one-to-one and onto is known as a _bijective_ function or simply a _bijection_.
A bijection from a set $S$ to itself is also known as a _permutation_ of $S$.
If  $F:S \rightarrow T$ is a bijection  then  for every $y\in T$ there is a unique $x\in S$ s.t. $F(x)=y$.
We denote this value $x$ by $F^{-1}(y)$.
Note that $F^{-1}$ is itself a bijection from $T$ to $S$ (can you see why?).


Giving a bijection between two sets is often a good way to show they have  the same size.
In fact, the standard mathematical definition of the notion that "$S$ and $T$ have the same cardinality" is that there exists a bijection $f:S \rightarrow T$.
In particular, the cardinality of a set $S$ is defined to be $n$ if there is a bijection from $S$ to the set $\{0,\ldots,n-1\}$.
As we will see later in this course, this is a definition that can  generalizes to defining the cardinality of _infinite_ sets.



__Partial functions:__ We will sometimes be interested in _partial_ functions from $S$ to $T$.
A partial function is allowed to be undefined on some subset of $S$.
That is, if $F$ is a partial function from $S$ to $T$, then for every $s\in S$, either there is (as in the case of standard functions) an element $F(s)$ in $T$, or $F(s)$ is undefined.
For example, the partial function $F(x)= \sqrt{x}$ is only defined on non-negative real numbers.
When we want to distinguish between partial functions and  standard (i.e., non-partial) functions, we will call the latter _total_ functions.
When we say "function" without any qualifier then we mean a _total_ function.

The notion of partial functions is a strict generalization of functions, and so every function is a partial function, but not every  partial function is a function. (That is, for every nonempty $S$ and $T$, the set of partial functions from $S$ to $T$ is a proper superset of the set of total functions from $S$ to $T$.) When we want to emphasize that a function $f$ from $A$ to $B$ might not be total, we will write $f: A \rightarrow_p B$.
We can think of a partial function $F$ from $S$ to $T$ also as a total function from $S$ to $T \cup \{ \bot \}$ where $\bot$ is some special "failure symbol", and so instead of saying that $F$ is undefined at $x$, we can say that $F(x)=\bot$.

__Basic facts about functions:__
Verifying that you can prove the following results is an excellent way to brush up on functions:

* If $F:S \rightarrow T$ and $G:T \rightarrow U$ are one-to-one functions, then their _composition_ $H:S \rightarrow U$ defined as $H(s)=G(F(s))$ is also one to one.

* If $F:S \rightarrow T$ is one to one, then there exists an onto function $G:T \rightarrow S$ such that $G(F(s))=s$ for every $s\in S$.

* If $G:T \rightarrow S$ is onto then there exists a one-to-one function $F:S \rightarrow T$ such that $G(F(s))=s$ for every $s\in S$.

* If $S$ and $T$ are finite sets then the following conditions are equivalent to one another: __(a)__ $|S| \leq |T|$, __(b)__ there is a one-to-one function $F:S \rightarrow T$, and __(c)__ there is an onto function $G:T \rightarrow S$.^[This is actually true even for _infinite_ $S$ and $T$: in that case __(b)__ is the commonly accepted _definition_ for $|S| \leq |T|$.]

![We can represent finite functions as a directed graph where we put an edge from $x$ to $f(x)$. The _onto_ condition corresponds to requiring that every vertex in the codomain of the function has in-degree _at least_ one. The _one-to-one_ condition  corresponds to requiring that every vertex in the codomain of the function has in-degree _at most_ one. In the examples above $F$ is an onto function, $G$ is one to one, and $H$ is neither onto nor one to one.](../figure/functionsdiagram.png){#functionsdiagrampng .class width=300px height=300px}

> # { .pause }
You can find the proofs of these results in many discrete math texts, including for example, Section 4.5 in the [Lehman-Leighton-Meyer notes](https://cs121.boazbarak.org/LLM_data_types.pdf).
However, I strongly suggest you try to prove them on your own, or at least convince yourself that they are true by proving special cases of those for small sizes (e.g., $|S|=3,|T|=4,|U|=5$).

Let us prove one of these facts as an example:

> # {.lemma #onetooneimpliesonto}
If $S,T$ are non-empty sets and $F:S \rightarrow T$ is one to one, then there exists an onto function $G:T \rightarrow S$ such that $G(F(s))=s$ for every $s\in S$.


> # {.proof data-ref="onetooneimpliesonto"}
Let $S$, $T$ and  $F:S \rightarrow T$ be as in the Lemma's statement, and choose some $s_0 \in S$.
We will define the function $G:T \rightarrow S$ as follows: for every $t\in T$, if there is some $s\in S$ such that $F(s)=t$ then set $G(t)=s$ (the choice of $s$ is well defined since by the one-to-one property of $F$, there cannot be two distinct $s,s'$  that both map to $t$).
Otherwise, set $G(t)=s_0$.
Now for every $s\in S$, by the definition of $G$, if $t=F(s)$ then $G(t)=G(F(s))=s$.
Moreover, this also shows that $G$ is _onto_, since it means that for every $s\in S$ there is some $t$ (namely $t=F(s)$) such that $G(t)=s$.



### Graphs { #graphsec }

_Graphs_ are ubiquitous in Computer Science, and  many other fields as well.
They are used to model a variety of data types including social networks, scheduling constraints, road networks, deep neural nets, gene interactions, correlations between observations, and a great many more.
The formal definitions of graphs are below for the sake of completeness, but if you have not seen graphs before in a course, I urge you to read up on them in one of the sources mentioned in [notesmathchap](){.ref}.^[One such recommended resource is [this lecture of Berkeley CS70](http://www.eecs70.org/static/notes/n5.html).]

Graphs come in two basic flavors: _undirected_ and _directed_.^[It is possible, and sometimes useful, to think of an undirected graph as the special case of an  directed graph  that has  the special property that for every pair $u,v$ either both the edges $(u,v)$ and $(v,u)$   are present or neither of them is. However, in many settings there is  a significant difference between  undirected and directed graphs, and so it's typically best to think of them as separate categories.]

![An example of an undirected and a directed graph. The undirected graph has vertex set $\{1,2,3,4\}$ and edge set $\{ \{1,2\},\{2,3\},\{2,4\} \}$. The directed graph has vertex set $\{a,b,c\}$ and the edge set $\{ (a,b),(b,c),(c,a),(a,c) \}$.](../figure/graphsexampe.png){#graphsexampefig .class width=300px height=300px}


> # {.definition title="Undirected graphs" #undirgraph}
An _undirected graph_ $G = (V,E)$ consists of a set $V$ of _vertices_ and a set $E$ of edges.
Every edge is a size two subset of $V$.
We say that two vertices $u,v \in V$ are _neighbors_, if the edge $\{u,v\}$ is in $E$.

Given this definition, we can define several other properties of graphs and their vertices.
We define the _degree_ of $u$ to be the number of neighbors $u$ has.
A _path_ in the graph is a tuple $(u_0,\ldots,u_k) \in V^k$, for some $k>0$ such that $u_{i+1}$ is a neighbor of $u_i$ for every $i\in [k]$.
A _simple path_ is a path $(u_0,\ldots,u_{k-1})$ where all the $u_i$'s are distinct.
A _cycle_ is a path $(u_0,\ldots,u_k)$ where $u_0=u_{k}$.
We say that two vertices $u,v\in V$ are _connected_ if either $u=v$ or there is a path from $(u_0,\ldots,u_k)$ where $u_0=u$ and $u_k=v$.
We say that the graph $G$ is _connected_ if every  pair of vertices in it is connected.

Here are some basic facts about undirected graphs. We give some informal arguments below, but leave the full proofs as exercises. (The proofs can also be found in most basic texts on  graph theory.)

> # {.lemma #degreesegeslem}
In any undirected graph $G=(V,E)$, the sum of the degrees of all vertices is equal to twice the number of edges.

[degreesegeslem](){.ref} can be shown by seeing that every edge $\{ u,v\}$ contributes twice to the sum of the degrees (once for $u$ and the second time for $v$.)

> # {.lemma #conntranslem}
The connectivity relation is _transitive_, in the sense that if $u$ is connected to $v$, and $v$ is connected to $w$, then $u$ is connected to $w$.

[conntranslem](){.ref} can be shown by simply attaching a path of the form $(u,u_1,u_2,\ldots,u_{k-1},v)$ to a path of the form $(v,u'_1,\ldots,u'_{k'-1},w)$ to obtain the path $(u,u_1,\ldots,u_{k-1},v,u'_1,\ldots,u'_{k'-1},w)$ that connects $u$ to $w$.


> # {.lemma #simplepathlem}
For every undirected graph $G=(V,E)$ and connected pair $u,v$, the shortest path from $u$ to $v$ is simple.
In particular, for every connected pair there exists a simple path that connects them.

[simplepathlem](){.ref} can be shown by "shortcutting" any non simple path of the form $(u,u_1,\ldots,u_{i-1},w,u_{i+1},\ldots,u_{j-1},w,u_{j+1},\ldots,u_{k-1},v)$ where the same vertex $w$ appears in both the $i$-th and $j$-position, to obtain the shorter path $(u,u_1,\ldots,u_{i-1},w,u_{j+1},\ldots,u_{k-1},v)$.

> # { .pause }
If you haven't seen these proofs before, it is indeed a great exercise to transform the above informal argument into fully rigorous proofs.


> # {.definition title="Directed graphs" #directedgraphdef}
A _directed graph_ $G=(V,E)$ consists of a set $V$ and a set $E \subseteq V\times V$  of _ordered pairs_ of $V$. We sometimes denote the edge $(u,v)$ also as $u \rightarrow v$.
If the edge $u \rightarrow v$ is present in the graph then we say that $v$ is an _out-neighbor_ of $u$ and $u$ is an _in-neighbor_ of $v$.

A directed graph might contain both $u \rightarrow v$ and $v \rightarrow u$  in which case $u$ will be both an in-neighbor and an out-neighbor of $v$ and vice versa.
The _in-degree_ of $u$ is the number of in-neighbors it has, and the _out-degree_ of $v$ is the number of out-neighbors it has.
A _path_ in the graph is a tuple $(u_0,\ldots,u_k) \in V^k$, for some $k>0$ such that $u_{i+1}$ is an out-neighbor of $u_i$ for every $i\in [k]$.
As in the undirected case, a _simple path_ is a path $(u_0,\ldots,u_{k-1})$ where all the $u_i$'s are distinct and a  _cycle_ is a path $(u_0,\ldots,u_k)$ where $u_0=u_{k}$.
One type of directed graphs we often care about is _directed acyclic graphs_ or _DAGs_, which, as their name implies, are directed graphs without any cycles:

> # {.definition title="Directed Acyclic Graphs" #DAGdef}
We say that $G=(V,E)$ is a _directed acyclic graph (DAG)_ if it is a directed graph and there does not exist a list of vertices $u_0,u_1,\ldots,u_k \in V$ such that $u_0=u_k$ and for every $i\in [k]$, the edge $u_i \rightarrow u_{i+1}$ is  in $E$.

The lemmas we mentioned above have analogs for directed graphs.
We again leave the proofs (which are essentially identical to their undirected analogs) as exercises for the reader:

> # {.lemma #diredgreesegeslem}
In any directed graph $G=(V,E)$, the sum of the in-degrees  is equal to the sum of the out-degrees, which is equal to the number of edges.


> # {.lemma #dirconntranslem}
In any directed graph $G$, if there is a path from $u$ to $v$ and a path from $v$ to $w$, then there is a path from $u$ to $w$.


> # {.lemma #dirsimplepathlem}
For every directed graph $G=(V,E)$ and a  pair $u,v$ such that there is a path from $u$ to $v$, the _shortest path_ from $u$ to $v$ is simple.


::: {.remark title="Graph terminology" #graphsname}
The word _graph_ in the sense above was coined by the mathematician Sylvester in 1878 in analogy with the chemical graphs used to visualize molecules.
There is an unfortunate confusion between this tern and the more common usage of the  word "graph" as a way to plot  data, and in particular a plot of some function $f(x)$ as a function of $x$.
One way to relate these two notions is to identify every function $f:A \rightarrow B$ with the  directed graph $G_f$ over the vertex set $V= A \cup B$ such that $G_f$  contains the  edge $x \rightarrow f(x)$ for every $x\in A$.

In a graph $G_f$ constructed in this way, every vertex in $A$ has out-degree equal to one.
If the function $f$ is _one to one_ then every vertex in $B$ has in-degree at most one.
If the function $f$ is _onto_ then every vertex in $B$ has in-degree at least one.
if $f$ is a bijection then every vertex in $B$ has in-degree exactly equal to one.
:::




### Logic operators and quantifiers.

If $P$ and $Q$ are some statements that can be true or false, then $P$ AND $Q$ (denoted as $P \wedge Q$) is the statement that is true if and only if both $P$ _and_ $Q$ are true, and $P$ OR $Q$ (denoted as $P \vee Q$) is the statement that is true if and only if either $P$ _or_ $Q$ is true.
The _negation_ of $P$, denoted as $\neg P$ or $\overline{P}$, is the statement that is true if and only if $P$ is false.

Suppose that $P(x)$ is a statement that depends on some _parameter_  $x$ (also sometimes known as an _unbound_ variable) in the sense that for every instantiation of $x$ with a value from some set $S$, $P(x)$ is either true or false.
For example, $x>7$ is a statement that is not a priori true or false, but does become true or false whenever we instantiate $x$ with some real number.
In such case we denote by  $\forall_{x\in S} P(x)$  the statement that is true if and only if $P(x)$ is true _for every_ $x\in S$.^[In this book,  we  place the variable that is bound by a quantifier in a subscript and so write $\forall_{x\in S}P(x)$. Some other texts  do not use this subscript notation and so will write the same statement as  $\forall x\in S \; P(x)$.]
We denote by  $\exists_{x\in S} P(x)$  the statement that is true if and only if _there exists_ some $x\in S$ such that $P(x)$ is true.

For example, the following is a formalization of the true statement that there exists a natural number $n$ larger than $100$ that is not divisible by $3$:

$$
\exists_{n\in \N} (n>100) \wedge \left(\forall_{k\in N} k+k+k \neq n\right) \;.
$$


__"For sufficiently large $n$."__ One expression that we will see come up time and again in this book is the claim that some statement $P(n)$ is true "for sufficiently large $n$".
What this means is that there exists an integer $N_0$ such that $P(n)$ is true for every $n>N_0$.
We can formalize this as $\exists_{N_0\in \N} \forall_{n>N_0} P(n)$.



### Quantifiers for summations and products { #secquantifiers }

The following shorthands for summing up or taking products of several numbers are often convenient.
If $S = \{s_0,\ldots,s_{n-1} \}$ is a finite set and  $f:S \rightarrow \R$ is a function, then we write $\sum_{x\in S} f(x)$ as shorthand for

$$
f(s_0) + f(s_1) + f(s_2) + \ldots + f(s_{n-1}) \;,
$$

and $\prod_{x\in S} f(x)$ as shorthand for

$$
f(s_0) \cdot f(s_1) \cdot f(s_2) \cdot \ldots \cdot f(s_{n-1}) \;.
$$

For example, the sum of the squares of all numbers from $1$ to $100$ can be written as

$$
\sum_{i\in \{1,\ldots,100\}} i^2 \;. \label{eqsumsquarehundred}
$$

Since summing up over intervals of integers is so common, there is  a special notation for it, and for every two integers $a \leq b$,  $\sum_{i=a}^b f(i)$ denotes $\sum_{i\in S} f(i)$ where $S =\{ x\in \Z : a \leq x \leq b \}$.
Hence we can write the sum [eqsumsquarehundred](){.eqref} also as

$$
\sum_{i=1}^{100} i^2 \;.
$$

### Parsing formulas: bound and free variables {#boundvarsec }

In mathematics, as in coding, we often have symbolic "variables" or "parameters".
It is important to be able to understand, given some formula, whether a given variable is _bound_ or _free_ in this formula.
For example, in the following statement $n$ is free but $a$ and $b$ are bound by the $\exists$ quantifier:

$$
\exists_{a,b \in \N} (a \neq 1) \wedge (a \neq n) \wedge (n = a \times b) \label{aboutnstmt}
$$

Since $n$ is free, it can be set to any value, and the truth of the statement [aboutnstmt](){.eqref} depends on the value of $n$.
For example, if $n=8$ then [aboutnstmt](){.eqref} is true, but for $n=11$ it is false. (Can you see why?)

The same issue appears when parsing code.
For example, in the following snippet from the C++ programming language

```clang
for (int i=0 ; i<n ; i=i+1) {
    printf("*");
}
```

the variable `i` is bound to the `for` operator but the variable `n` is free.

The main property of bound variables is that we can _rename_ them (as long as the new name doesn't conflict with another used variable)  without changing the meaning of the statement.
Thus for example the statement

$$
\exists_{x,y \in \N} (x \neq 1) \wedge (x \neq n) \wedge (n = x \times y) \label{aboutnstmttwo}
$$

is _equivalent_ to [aboutnstmt](){.eqref} in the sense that it is true for exactly the same set of $n$'s.

Similarly, the code

```clang
for (int j=0 ; j<n ; j=j+1) {
    printf("*");
}
```

produces the same result as the code above that used `i` instead of `j`.

::: {.remark title="Aside: mathematical vs programming notation" #notationrem}
Mathematical notation has a lot of similarities with programming language, and for the same reasons.
Both are formalisms meant to convey complex concepts in a precise way.
However, there are some cultural differences.
In programming languages, we often try to use meaningful variable names such as `NumberOfVertices` while in math we often use short identifiers such as $n$.
(Part of it might have to do with the tradition of mathematical proofs as being handwritten and verbally presented, as opposed to typed up and compiled.)

One consequence of that is that in mathematics we often end up reusing identifiers, and also "run out" of letters and hence use Greek letters too, as well as distinguish between small and capital letters.
Similarly, mathematical notation tends to use quite a lot of "overloading", using operators such as $+$ for a great variety of objects (e.g., real numbers, matrices, finite field elements, etc..), and assuming that the meaning can be inferred from the context.

Both fields have a notion of "types", and in math we often try to reserve certain letters for variables of a particular type.
For example, variables such as $i,j,k,\ell,m,n$ will often denote integers, and $\epsilon$ will often denote a small positive real number
(see [notationsec](){.ref} for more on these conventions).
When reading or writing mathematical texts, we usually don't have the advantage of a "compiler" that will check type safety for us. Hence it is important to keep track of the type of each variable, and see that the operations that are performed on it "make sense".

Kun's book [@Kun18] contains an extensive discussion on the similarities and  differences between the cultures of mathematics and programming.
:::


### Asymptotics and Big-$O$ notation

>_"$\log\log\log n$ has been proved to go to infinity, but has never been observed to do so."_, Anonymous, quoted by Carl Pomerance (2000)

It is often very cumbersome to describe precisely  quantities such as running time and is also not needed, since we are typically mostly interested in the "higher order terms".
That is, we want to understand the _scaling behavior_ of the quantity as the input variable grows.
For example, as far as running time goes, the difference between an $n^5$-time algorithm and an $n^2$-time one is much more significant than the difference between an $100n^2 + 10n$ time algorithm and an $10n^2$ time algorithm.
For this purpose, $O$-notation is extremely useful as a way to "declutter" our text and focus our attention on what really matters.
For example, using $O$-notation, we can say that both $100n^2 + 10n$ and $10n^2$ are simply $\Theta(n^2)$ (which informally means "the same up to constant factors"), while $n^2 = o(n^5)$ (which informally means that $n^2$ is "much smaller than" $n^5$).^[While Big-$O$ notation is often used to analyze running time of algorithms, this is by no means the only application. At the end of the day, Big-$O$ notation is just a way to express asymptotic inequalities between functions on integers. It can be used regardless of whether these functions are a measure of running time, memory usage, or any other quantity that may have nothing to do with computation.]


Generally (though still informally), if $F,G$ are two functions mapping natural numbers to non-negative reals,  then "$F=O(G)$" means that  $F(n) \leq G(n)$ if we don't care about constant factors, while  "$F=o(G)$" means that $F$ is much smaller than $G$, in the sense that no matter by what constant factor we multiply $F$, if we take $n$ to be large enough then  $G$ will be bigger (for this reason, sometimes $F=o(G)$ is written as $F \ll G$).
We will write $F= \Theta(G)$ if $F=O(G)$ and $G=O(F)$, which one can think of as saying that $F$ is the same as $G$ if we don't care about constant factors.
More formally, we define Big-$O$ notation as follows:


:::  {.definition title="Big-$O$ notation" #bigohdef}
For $F,G: \N \rightarrow \R_+$, we define $F=O(G)$ (sometimes also written as $F \leq O(G)$) if there exist numbers $a,N_0 \in \N$ such that $F(n) \leq a\cdot G(n)$ for every $n>N_0$.^[Recall that $\R_+$, which is also sometimes denoted as $(0,\infty)$, is the set of positive real numbers, so the above is just a way of saying that $F$ and $G$'s outputs are always positive numbers.]
We define $F=\Omega(G)$ (sometimes also writtenas $F \leq \Omega(G$)) if $G=O(F)$.

We write $F =o(G)$ if for every $\epsilon>0$ there is some $N_0$ such that $F(n) <\epsilon G(n)$ for every $n>N_0$.
We write $F =\omega(G)$ if $G=o(F)$.
We write $F= \Theta(G)$ if $F=O(G)$ and $G=O(F)$.
:::

We can also use the notion of _limits_ to define Big- and Little-$O$ notation.
You can verify that $F=o(G)$ (or, equivalently, $G=\omega(F)$) if and only if $\lim\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)} = 0$.
Similarly, if the limit $\lim\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)}$ exists and is a finite number then $F=O(G)$.
If you are familiar with the notion of _supremum_, then you can verify that $F=O(G)$ if and only if $\limsup\limits_{n\rightarrow\infty} \tfrac{F(n)}{G(n)} < \infty$.

![If $F(n)=o(G(n))$ then for sufficiently large $n$, $F(n)$ will be smaller than $G(n)$. For example, if Algorithm $A$ runs in time $1000\cdot n+10^6$ and Algorithm $B$ runs in time $0.01\cdot n^2$ then even though $B$ might be more efficient for smaller inputs, when the inputs get sufficiently large, $A$ will run _much_ faster than $B$. ](../figure/nvsnsquared.png){#nvsnsquaredfig .class width=300px height=300px}



::: {.remark title="Big-$O$ and equality" #equalitybighohrem}
Using the equality sign for $O$-notation is extremely common, but is somewhat of a misnomer, since a statement such as $F = O(G)$ really means that $F$ is in the set $\{ G' : \exists_{N,c} \text{ s.t. } \forall_{n>N} G'(n) \leq c G(n) \}$.

If anything, it would have made more sense use _inequalities_ and  write $F \leq O(G)$ and $F \geq \Omega(G)$, reserving equality for $F = \Theta(G)$,  and so we will sometimes use this notation, but since the equality notation is quite firmly entrenched we will often stick to it as well. (Some texts use the notation  $F \in O(G)$ instead of $F = O(G)$, but we will not use this notation in this book.)

Despite the misleading equality sign, you should remember that a statement such as $F = O(G)$ means that $F$ is "at most" $G$ in some rough sense when we ignore constants, and a statement such as $F = \Omega(G)$ means that $F$ is "at least" $G$ in the same rough sense.
:::

It's often convenient to use "anonymous functions" in the context of $O$-notation, and also  to emphasize the input parameter to the function.
For example, when we write a statement such as $F(n) = O(n^3)$, we mean that  $F=O(G)$ where $G$ is the function defined by $G(n)=n^3$.
Chapter 7 in [Jim Apsnes' notes on discrete math](http://www.cs.yale.edu/homes/aspnes/classes/202/notes.pdf) provides a good summary of $O$ notation; see also [this tutorial](http://discrete.gr/complexity/) for a gentler and more programmer-oriented introduction.



### Some "rules of thumb" for Big-$O$ notation

There are some simple heuristics that can help when trying to compare two functions $F$ and $G$:

* Multiplicative constants don't matter in $O$-notation, and so if $F(n)=O(G(n))$ then $100F(n)=O(G(n))$.

* When adding two functions, we only care about the larger one. For example, for the purpose of $O$-notation, $n^3+100n^2$ is the same as $n^3$, and in general in any polynomial, we only care about the larger exponent.

* For every two constants $a,b>0$, $n^a = O(n^b)$ if and only if $a \leq b$, and $n^a = o(n^b)$ if and only if $a<b$. For example, combining the two observations above, $100n^2 + 10n + 100 = o(n^3)$.

* Polynomial is always smaller than exponential: $n^a = o(2^{n^\epsilon})$ for every two constants $a>0$ and $\epsilon>0$ even if $\epsilon$ is much smaller than $a$. For example, $100n^{100} = o(2^{\sqrt{n}})$.

* Similarly, logarithmic is always smaller than polynomial: $(\log n)^a$ (which we write as $\log^a n$) is $o(n^\epsilon)$ for every two constants $a,\epsilon>0$. For example, combining the observations above, $100n^2 \log^{100} n = o(n^3)$.

In most (though not all!) cases we use $O$-notation, the constants hidden by it are not too huge and so on an intuitive level, you can think of $F=O(G)$ as saying something like $F(n) \leq 1000 G(n)$ and $F=\Omega(G)$ as saying something $F(n) \geq 0.001 G(n)$.


## Proofs { #proofsbackgroundsec }



Many people think of mathematical proofs as a sequence of logical deductions that starts from some axioms and ultimately arrives at a conclusion.
In fact, some dictionaries [define](http://www.thefreedictionary.com/mathematical+proof) proofs that way.
This is not entirely wrong, but in reality a mathematical proof of a statement X is simply an argument  that convinces the reader that X is true beyond a shadow of a doubt.

To produce such a proof you need to:

1. Understand precisely what X means.

2. Convince  _yourself_ that X is true.

3. Write your reasoning down in plain, precise and concise English (using formulas or notation only when they help clarity).

In many cases, Step 1 is the most important one. Understanding what a statement means is often more than halfway towards understanding why it is true.
In Step 3, to convince the reader beyond a shadow of a doubt, we will often want to  break down the reasoning to "basic steps", where each basic step is simple enough to be "self evident". The  combination of all steps yields the desired statement.

### Proofs and programs

There is a great deal of similarity between the process of writing _proofs_ and that of writing _programs_, and both require a similar set of skills.
Writing a _program_ involves:

1. Understanding what is the _task_ we want the program to achieve.

2. Convincing _yourself_ that the task can be achieved by a computer, perhaps by planning on a whiteboard or notepad how you will break it up to simpler tasks.

3. Converting this plan into code that a compiler or interpreter can understand, by breaking up each task into a sequence of the basic operations of some programming language.

In programs as in proofs, step 1 is often the most important one.
A key difference is that the reader for proofs is a human being and for programs is a compiler.^[This difference might be eroding with time, as more proofs are being written in a _machine verifiable form_ and progress in artificial intelligence allows expressing programs in more human friendly ways, such as "programming by example". Interestingly, much of the progress in automatic proof verification and proof assistants relies on a [much deeper correspondence](http://homepages.inf.ed.ac.uk/wadler/papers/propositions-as-types/propositions-as-types.pdf) between _proofs_ and _programs_, see [chapproofs](){.ref}.]
Thus our emphasis is on _readability_ and having a _clear logical flow_ for the proof (which is not a bad idea for programs as well...).
When writing a proof, you should think of your audience as an intelligent but highly skeptical and somewhat petty reader, that will "call foul" at every step that is not well justified.





### Proof writing style

A mathematical proof is a piece of writing, but it is a specific genre of writing with certain conventions and preferred styles.
As in any writing, practice makes perfect, and it is also important to revise your drafts for clarity.

In a proof for the statement $X$, all the text between the words __"Proof:"__ and __"QED"__ should be focused on establishing that $X$ is true.
Digressions, examples, or ruminations should be kept outside these two words, so they do not confuse the reader.
The proof should have a clear logical flow in the sense that every sentence or equation in it should have some purpose and it should be crystal-clear to the reader what this purpose is.
When you write a proof, for every equation or sentence you include, ask yourself:

1. Is this sentence or equation stating that some statement is true?

2. If so, does this statement   follow from the previous steps,  or are we going to establish it in the next step?

3. What is the _role_ of this sentence  or equation? Is it one step towards proving the original statement, or is it a step towards proving some intermediate claim that you have stated before?

4. Finally, would the answers to questions 1-3 be clear to the reader? If not, then you should reorder, rephrase or add explanations.


Some helpful resources on mathematical writing include [this handout by Lee](https://sites.math.washington.edu/~lee/Writing/writing-proofs.pdf), [this handout by Hutching](https://math.berkeley.edu/~hutching/teach/proofs.pdf), as well as several of the excellent handouts in [Stanford's CS 103 class](http://web.stanford.edu/class/cs103/).


### Patterns in proofs

>_"If it was so, it might be; and if it were so, it would be; but as it isn’t, it ain’t. That’s logic."_, Lewis Carroll, _Through the looking-glass_.


Just like in programming, there are several common patterns of proofs that occur time and again.
Here are some examples:

__Proofs by contradiction:__ One way to prove that $X$ is true is to show that if $X$ was false then we would get a contradiction as a result. Such proofs often start with a sentence such as "Suppose, towards a contradiction, that $X$ is false" and end with deriving some contradiction (such as a violation of one of the assumptions in the theorem statement).
Here is an example:

> # {.lemma }
There are no natural numbers $a,b$ such that $\sqrt{2} = \tfrac{a}{b}$.

> # {.proof }
Suppose, towards the sake of contradiction that this is false, and so let $a\in \N$ be the smallest number such that there exists some $b\in\N$ satisfying $\sqrt{2}=\tfrac{a}{b}$.
Squaring this equation we get that $2=a^2/b^2$ or $a^2=2b^2$ $(*)$. But this means that $a^2$ is _even_, and since the product of two odd  numbers is odd, it means that $a$ is even as well, or in other words, $a = 2a'$ for some $a' \in \N$. Yet plugging this into $(*)$ shows  that $4a'^2 = 2b^2$ which means  $b^2 = 2a'^2$ is an even number as well. By the same considerations as above we gat that $b$ is even and hence $a/2$ and $b/2$ are two natural numbers  satisfying $\tfrac{a/2}{b/2}=\sqrt{2}$, contradicting the minimality of $a$.


__Proofs of a universal statement:__ Often we want to prove a statement $X$ of the form "Every object of type $O$ has property $P$." Such proofs often start with a sentence such as "Let $o$ be an object of type $O$" and end by showing that $o$ has the property $P$.
Here is a simple example:

> # {.lemma }
For every natural number $n\in N$, either $n$ or $n+1$ is even.


> # {.proof}
Let $n\in N$ be some number.
If $n/2$ is a whole number then we are done, since then $n=2(n/2)$ and hence it is even.
Otherwise, $n/2+1/2$ is a whole number, and hence $2(n/2+1/2)=n+1$ is even.

__Proofs of an implication:__ Another common case is that the statement $X$ has the form "$A$ implies $B$". Such proofs often start with a sentence such as "Assume that $A$ is true" and end with a derivation of $B$ from $A$.
Here is a simple example:

> # {.lemma }
If $b^2 \geq 4ac$ then there is a solution to the quadratic equation $ax^2 + bx + c =0$.

> # {.proof }
Suppose that $b^2 \geq 4ac$.
Then $d = b^2 - 4ac$ is a non-negative number and hence it has a square root $s$.
Thus $x = (-b+s)/(2a)$ satisfies
$$
\begin{aligned}
ax^2 + bx + c &= a(-b+s)^2/(4a^2) + b(-b+s)/(2a) + c \\
&= (b^2-2bs+s^2)/(4a)+(-b^2+bs)/(2a)+c \;. \label{eq:quadeq}
\end{aligned}
$$

Rearranging the terms of [eq:quadeq](){.eqref} we get
$$
s^2/(4a)+c- b^2/(4a) = (b^2-4ac)/(4a) + c - b^2/(4a) = 0
$$

__Proofs of equivalence:__  If a statement has the form "$A$  if and only if $B$" (often shortened as "$A$ iff $B$") then we need to prove both that $A$ implies $B$ and that $B$ implies $A$.
We call the implication that $A$ implies $B$ the "only if" direction, and the implication that $B$ implies $A$ the "if" direction.


__Proofs by combining intermediate claims:__
When a proof is more complex, it is often helpful to break it apart into several steps.
That is, to prove the statement $X$, we might first prove statements $X_1$,$X_2$, and $X_3$ and then prove that $X_1 \wedge X_2 \wedge X_3$ implies $X$.^[As mentioned below, $\wedge$ denotes the logical AND operator.]


__Proofs by case distinction:__ This is a special case of the above, where to prove a statement $X$ we split into several cases $C_1,\ldots,C_k$, and prove that __(a)__ the cases are _exhaustive_, in the sense that _one_ of the cases $C_i$  must happen and __(b)__ go one by one and prove that each one of the cases $C_i$ implies the result $X$ that we are after.

__Proofs by induction:__ We discuss induction and give an example in [inductionsec](){.ref} below. We can think of such proofs as a variant of the above, where we have an unbounded number of intermediate claims $X_0,X_2,\ldots,X_k$, and we prove that $X_0$ is true, as well that $X_0$ implies $X_1$, and that $X_0  \wedge X_1$ implies $X_2$, and so on and so forth.
The website for CMU course 15-251 contains a [useful handout](http://www.cs.cmu.edu/~./15251/notes/induction-pitfalls.pdf) on potential pitfalls when making proofs by induction.


__"Without loss of generality (w.l.o.g)":__ This term can be initially quite confusing to students. It is essentially a way to simplify proofs by case distinctions. The idea is that if Case 1 is equal to Case 2 up to a change of variables or a similar transformation, then the proof of Case 1 will also imply the proof of case 2.
It is always a statement that should be viewed with suspicion.
Whenever you see it in a proof, ask yourself if you understand _why_ the assumption made is truly without loss of generality, and when you use it, try to see if the use is indeed justified.
When writing a proof, sometimes  it might be easiest to simply repeat the proof of the second case (adding a remark that the proof is very similar to the first one).


::: {.remark title="Hierarchical Proofs (optional)" #lamportrem}
Mathematical proofs are ultimately written in English prose.
The well-known computer scientist [Leslie Lamport](https://en.wikipedia.org/wiki/Leslie_Lamport) argues that this is a problem, and proofs should be written in a more formal and rigorous way.
In his [manuscript](https://lamport.azurewebsites.net/pubs/proof.pdf) he proposes an approach for _structured hierarchical proofs_, that have the following form:

* A proof for a statement of the form "If $A$ then $B$" is a sequence of numbered claims, starting with the assumption that $A$ is true, and ending with the claim that $B$ is true.

* Every claim is followed by a proof showing how it is derived from the previous assumptions or claims.

* The proof for each claim is itself a sequence of subclaims.

The advantage of Lamport's format is that it is very clear for every sentence in the proof what is the role that it plays.
It is also much easier to transform such proofs into machine-checkable forms.
The disadvantage is that such proofs can be more tedious to read and write, with less differentiation between the important parts of the arguments versus the more routine ones.
:::

## Extended example: Topological Sorting

In this section we will prove the following: every directed acyclic graph (DAG, see [DAGdef](){.ref}) can be arranged in layers so that for all directed edges $u \rightarrow v$, the layer of $v$ is larger than the layer of $u$.
This result is known as [topological sorting](https://goo.gl/QUskBc) and is used in many applications, including task scheduling, build systems, software package management, spreadsheet cell calculations, and many others (see [topologicalsortfig](){.ref}).
In fact, we will also use it ourselves later on in this book.

![An example of _topological sorting_. We consider a directed graph corresponding to a  prerequisite graph of the courses in some Computer Science program. The edge $u \rightarrow v$ means that the course $u$ is a prerequisite for the course $v$. A _layering_ or "topological sorting" of this  graph is the same as mapping the courses to semesters so that if we decide to take the course $v$ in semester $f(v)$, then we have already taken all the prerequisites for $v$ (i.e., its in-neighbors) in prior semesters.](../figure/topologicalsort.png){#topologicalsortfig .class width=300px height=300px}

We start with the following definition. A _layering_ of a directed graph is a way to assign for every vertex $v$ a natural number (corresponding to its layer), such that $v$'s in-neighbors are in lower-numbered layers than $v$, and $v$'s out-neighbors are in higher-numbered layers.
The formal definition is as follows:

> # {.definition title="Layering of a DAG" #layeringdef}
Let $G=(V,E)$ be a directed graph. A _layering_ of $G$ is a function $f:V \rightarrow \N$ such that for every edge $u \rightarrow v$ of $G$, $f(u) < f(v)$.

In this section we prove that a directed graph is acylic if and only if it has a valid layering.

> # {.theorem title="Topological Sort" #topologicalsortthm}
Let $G$ be a directed graph. Then $G$ is acyclic if and only if there exists a  layering $f$ of $G$.

To prove such a theorem, we need to first understand what it means. Since it is an "if and only if" statement, [topologicalsortthm](){.ref} corresponds to two statements:

> # {.lemma #acyclictosortlem}
For every directed graph $G$, if $G$ is acyclic then it has a layering.

> # {.lemma #sorttoacycliclem}
For every directed graph $G$, if $G$ has a layering, then it is acyclic.

To prove [topologicalsortthm](){.ref} we need to prove both [acyclictosortlem](){.ref} and [sorttoacycliclem](){.ref}.
[sorttoacycliclem](){.ref} is actually not that hard to prove.
Intuitively, if $G$ contains a _cycle_, then it cannot be the case that all edges on the cycle increase in layer number, since if we travel along the cycle at some point we must come back to the place we started from.
The formal proof is as follows:

::: {.proof data-ref="sorttoacycliclem"}
Let $G=(V,E)$ be a directed graph and let $f:\N \rightarrow \N$ be a layering of $G$ as per [layeringdef](){.ref} . Suppose, towards the sake of contradiction, that $G$ is not acyclic, and hence there exists some cycle $u_0,u_1,\ldots,u_k$ such that $u_0=u_k$ and for every $i\in [k]$ the edge $u_i \rightarrow u_{i+1}$ is present in $G$.
Since $f$ is a layering, for every $i \in [k]$, $f(u_i) < f(u_{i+1})$, which means that
$$
f(u_0) < f(u_1)  < \cdots  < f(u_k)
$$
but this is a contradiction since $u_0=u_k$ and hence $f(u_0)=f(u_k)$.
:::

[acyclictosortlem](){.ref} corresponds to the more difficult (and useful) direction. To prove it, we need to show how given an arbitrary DAG $G$, we can come up with a layering of the vertices of $G$ so that all edges "go up".

> # { .pause }
If you have not seen the proof of this theorem before (or don't remember it), this would be an excellent point to pause and try to prove it yourself.
One way to do it would be to describe an _algorithm_ that on input a directed acyclic graph $G$ on $n$ vertices and $n-2$ or fewer edges, constructs  an array $F$ of length $n$ such that for every edge $u \rightarrow v$ in the graph $F[u] < F[v]$.










### Mathematical induction  { #inductionsec }

There are several ways to prove [acyclictosortlem](){.ref}.
One approach to do is to start by proving it for small graphs, such as graphs with 1,2 or 3 vertices  (see [see [topsortexamplesfig](){.ref}](){.ref}), for which we can check all the cases, and then try to extend the proof for larger graphs.
The technical term for this proof approach is _proof by induction_.



![Some examples of DAGs of one, two and three vertices, and valid ways to assign layers to the vertices.](../figure/topologicalsortexamples.png){#topsortexamplesfig .class width=300px height=300px}


_Induction_ is simply an application of the self-evident  [Modus Ponens rule](https://en.wikipedia.org/wiki/Modus_ponens) that says that if

__(a)__ $P$ is true

and

__(b)__ $P$ implies $Q$

then $Q$ is true.

In the setting of proofs by induction we typically have a statement $Q(k)$ that is parameterized by some integer $k$, and we prove that  __(a)__ $Q(0)$ is true, and __(b)__ For every $k>0$, if $Q(0),\ldots,Q(k-1)$ are all true then $Q(k)$ is true.^[Usually proving __(b)__ is the hard part, though there are examples where the "base case" __(a)__ is quite subtle.]
By  applying Modus Ponens, we can deduce from __(a)__ and __(b)__ that $Q(1)$ is true.
Once we did so, since we now know that both $Q(0)$ and $Q(1)$ are true, then we can use this and __(b)__ to deduce (again using Modus Ponens) that $Q(2)$ is true.
We can repeat the same reasoning again and again to obtain that  $Q(k)$ is true for every $k$.
The statement __(a)__ is called the "base case", while __(b)__ is called the "inductive step".
The assumption in __(b)__ that $Q(i)$ holds for $i<k$ is called the "inductive hypothesis".^[The form of induction described here is sometimes called "strong induction" as opposed to "weak induction" where we replace __(b)__ by the statement __(b')__ that if $Q(k-1)$ is true then $Q(k)$ is true. Weak induction can be thought of as the special case of strong induction where we don't use the assumption that $Q(0),\ldots,Q(k-2)$ are true.]

> # {.remark title="Induction and recursion" #inducrecrem}
Proofs by inductions are closely related to algorithms by recursion.
In both cases we reduce solving a larger problem to solving a smaller instance of itself. In a recursive algorithm to solve some problem P on an input of length $k$  we ask ourselves "what if someone handed me a way to solve P on instances smaller than $k$?". In an inductive proof to prove a statement Q parameterized by a number $k$, we ask ourselves "what if I already knew that $Q(k')$ is true for $k'<k$".
Both induction and recursion are crucial concepts for this course and Computer Science at large (and even other areas of inquiry, including not just mathematics but other sciences as well). Both can be initially (and even post-initially) confusing, but with time and practice they become clearer.
For more on proofs by induction and recursion, you might find the  following [Stanford CS 103 handout](https://cs121.boazbarak.org/StanfordCS103Induction.pdf), [this MIT 6.00 lecture](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-1/lecture-6-recursion/) or [this excerpt of the Lehman-Leighton book](https://cs121.boazbarak.org/LL_induction.pdf) useful.




### Proving the result by induction

There are several ways to use induction to prove  [acyclictosortlem](){.ref} by induction.
We will use induction on the number $n$ of vertices, and so we  will define the statement $Q(n)$ as follows:

>$Q(n)$ is _"For every DAG  $G=(V,E)$ with $n$ vertices, there is a layering of $G$."_

The statement $Q(1)$ is trivial, since in this case $G$ contains no edge, and we can simply use the layering $f(v)=0$ (where $v$ is the single vertex of $G$). Thus it will suffice to prove the following: _for every $n>1$, if $Q(n-1)$ is true then $Q(n)$ is true._

To do so, we need to somehow find a way, given a graph $G$ of $n$ vertices, to reduce the task of finding a layering for $G$ into the task of finding a layering for some other graph $G'$ of $n-1$ vertices.
The idea is that we will find a _source_ of $G$: a vertex $v$ that has no in-neighbors. We can then assign to $v$ the layer $0$, and layer the remaining vertices using the inductive hypothesis in layers $1,2,\ldots$.

The above is  the intuition behind the proof, but when writing the proof,   we use the benefit of hindsight, and try to streamline what was a messy journey into a linear and easy-to-follow flow of logic that starts with the word __"Proof:"__ and ends with  __"QED"__ or the symbol $\blacksquare$.^[QED stands for "quod erat demonstrandum", which is "What was to be demonstrated." or  "The very thing it was required to have shown." in Latin.]
All our discussions, examples and digressions can be very insightful, but we keep them outside the space delimited between these two words, where (as described by this [excellent handout](http://web.stanford.edu/class/cs103/handouts/120%20Proofwriting%20Checklist.pdf)) "every sentence must be load bearing".
Just like we do in programming, we can break the proof into little "subroutines" or "functions" (known as _lemmas_ or _claims_ in math language), which will be smaller statements that help us prove the main result.
However, it should always be crystal-clear to the reader in what stage we are of the proof.
Just like it should always be clear to which function a line of code belongs to, it should always be clear whether an individual sentence  is part of a  proof of some intermediate result, or is part of the argument showing that this intermediate result implies the theorem.
Sometimes we highlight this partition by noting after each occurrence of  __"QED"__ to which lemma or claim it belongs.

We now present the formal proof.


::: {.proof data-ref="acyclictosortlem"}
Let $G=(V,E)$ be a DAG and $n=|V|$ be the number of its vertices.
We prove the lemma by induction on $n$.
The base case is $n=1$. In this case $V = \{ v \}$ for a single vertex $v$, and we can use the layering defined as $f(v)=0$.
For the case of $n>1$, we make the inductive hypothesis that every DAG $G'$ of at most $n-1$ vertices has a layering.

We make the following claim:

__Claim:__ $G$ must contain a vertex $v$ of in-degree zero.

__Proof of Claim:__ Suppose otherwise that every vertex $v\in V$ has an in-neighbor. Let $v_0$ be some vertex of $G$, let $v_1$ be an in-neighbor of $v_0$, $v_2$ be an in-neighbor of $v_1$, and continue in this way for $n$ steps until we construct a list $v_0,v_1,\ldots,v_n$ such that for every $i\in [n]$, $v_{i+1}$ is an in-neighbor of $v_i$, or in other words the edge $v_{i+1} \rightarrow v_i$ is present in the graph. Since there are only $n$ vertices in this graph, one of the $n+1$ vertices in this sequence must repeat itself, and so there exists $i<j$ such that $v_i=v_j$. But then the sequence $v_j \rightarrow v_{j-1} \rightarrow \cdots \rightarrow v_i$ is a cycle in $G$, contradicting our assumption that it is acyclic. __(QED Claim)__

Given the claim, we can let $v_0$ be some vertex of in-degree zero in $G$, and let $G'$ be the graph obtained by removing $v_0$ from $G$.
$G'$ has $n-1$ vertices and hence per the inductive hypothesis has a layering $f':(V \setminus \{v_0\}) \rightarrow \N$.
We define $f:V \rightarrow \N$ as follows:

$$f(v) = \begin{cases}f'(v)+1 & v \neq v_0 \\ 0 & v=v_0 \end{cases}\;.$$

We claim that $f$ is a valid layering, namely that for every edge $u \rightarrow v$, $f(u) < f(v)$. To prove this, we split into cases:

* __Case 1:__ $u \neq v_0$, $v \neq v_0$. In this case the edge $u \rightarrow v$ exists in the graph $G'$ and hence by the inductive hypothesis $f'(u) < f'(v)$ which implies that $f'(u)+1 < f'(v)+1$.

* __Case 2:__ $u=v_0$, $v \neq v_0$. In this case $f(u)=0$ and $f(v) = f'(v)+1>0$.

* __Case 3:__ $u \neq v_0$, $v=v_0$. This case can't happen since $v_0$ does not have in-neighbors.

Thus $f$ is a valid layering for $G$ which completes the proof.^[If we were being really pedantic we would have a fourth case for $u=v_0$ and $v=v_0$ but that would correspond to a self loop and we always assume our graphs do not have those unless explicitly stated otherwise.]
:::


> # { .pause }
Reading a proof is no less of an important skill than producing one.
In fact, just like understanding code, it is a highly non-trivial skill in itself.
Therefore I strongly suggest that you re-read the above proof, asking yourself at every sentence whether the assumption it makes are justified, and whether this sentence truly demonstrates what it purports to achieve.
Another good habit is to ask yourself when reading a proof for every variable you encounter (such as $u$, $i$, $G'$, $f'$ etc. in the above proof) the following questions: __(1)__ What _type_ of variable is it? is it a number? a graph? a vertex? a function? and __(2)__ What do we know about it? Is it an arbitrary member of the set? Have we shown some facts about it?, and __(3)__ What are we _trying_ to show about it?.



## Notation and conventions { #notationsec }

Most of the notation we use in this book is standard and is used in most mathematical texts. The main points where we diverge are:

* We index the natural numbers $\N$ starting with $0$ (though many other texts, especially in computer science, do the same).

* We also index the set $[n]$ starting with $0$, and hence define it as $\{0,\ldots,n-1\}$. In other texts it is often defined as $\{1,\ldots, n \}$. Similarly, we index coordinates of our strings starting with $0$, and hence a string $x\in \{0,1\}^n$ is written as $x_0x_1\cdots x_{n-1}$.

* If $n$ is a natural number then $1^n$ does _not_ equal the number $1$ but rather this is  the length $n$ string $11\cdots 1$ (that is a string of $n$ ones). Similarly, $0^n$ refers to the length $n$ string $00 \cdots 0$.

* _Partial_ functions  are functions that are not necessarily  defined on all inputs. When we write $f:A \rightarrow B$ this means that $f$ is  a _total_ function unless we say otherwise. When we want to emphasize that $f$ can be  a partial function, we will sometimes write $f: A \rightarrow_p B$.

* As we will see later on in the course, we will mostly describe our computational problems in the terms of computing a _Boolean function_ $f: \{0,1\}^* \rightarrow \{0,1\}$. In contrast, many other  textbooks refer to the same task as  _deciding a language_ $L \subseteq \{0,1\}^*$. These two viewpoints are equivalent, since for every set $L\subseteq \{0,1\}^*$ there is a corresponding  function $F$ such that $F(x)=1$ if and only if $x\in L$. Computing _partial functions_ corresponds to the task known in the literature as a solving a _promise problem_.^[Because the language notation is so prevalent in other textbooks, we will occasionally remind the reader of this correspondence.]

* We use $\ceil{x}$ and $\floor{x}$ for the "ceiling" and "floor" operators that correspond to "rounding up" or "rounding down" a number to the nearest integer. We use $(x \mod y)$ to denote the "remainder" of $x$ when divided by $y$. That is, $(x \mod y) = x - y\floor{x/y}$. In context when an integer is expected we'll typically "silently round" the quantities to an integer. For example, if we say that $x$ is a string of length $\sqrt{n}$ then this means that $x$ is  of length $\lceil \sqrt{n} \rceil$. (We round up for the sake of convention, but in most such cases, it will not make a difference  whether we round up or down.)


* Like most Computer Science texts, we default to the logarithm in base two. Thus, $\log n$ is the same as $\log_2 n$.

* We will also use the notation $f(n)=poly(n)$ as a short hand for $f(n)=n^{O(1)}$ (i.e., as shorthand for saying that there are some constants $a,b$ such that $f(n) \leq a\cdot n^b$ for every sufficiently large $n$). Similarly, we will use $f(n)=polylog(n)$ as shorthand for $f(n)=poly(\log n)$ (i.e., as shorthand for saying that there are some constants $a,b$ such that $f(n) \leq a\cdot (\log n)^b$ for every sufficiently large $n$).

* As in often the case in mathematical literature, we use the apostrophe character to enrich our set of identifier. Typically if $x$ denotes some object, then $x'$, $x''$, etc. will denote other objects of the same type.

* To save on "cognitive load" we will often use round constants such as $10,100,1000$ in the statements of both theorems and problem set questions. When you see such a "round" constant, you can typically assume that it has no special significance and was just chosen arbitrarily. For example, if you see a theorem of the form "Algorithm $A$ takes at most $1000\cdot n^2$ steps to compute function $F$ on inputs of length $n$" then probably the number $1000$ is an abitrary sufficiently large constant, and one could prove the same theorem with a bound of the form $c \cdot n^2$ for a constant $c$ that is smaller than $1000$. Similarly, if a problem-set question asks you to prove that some quantity is at least $n/100$, it is quite possible that in truth the quantity is at least $n/d$ for some constant $d$ that is smaller than $100$.


### Conventions

Mathematics (as is coding)  is full of variables. Whenever you see a variable, it is always important to keep track of what is its _type_: is it a number, a function, a string, a graph, a program? To make this easier, we try to stick to certain conventions by which we use certain identifiers for variables of the same type.
Some of these conventions are listed in the following table.
Note that these are conventions and not immutable laws. Sometimes we might deviate from them.
Also, such conventions do not replace the need to explicitly declare for each new variable the type of object that it denotes.



| *Identifier*      | *Is often used to denote an object of the type*                                                                                                                                                                                                                                         |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $i,j,k,\ell,m,n$  | Natural numbers (i.e., in $\mathbb{N} = \{0,1,2,\ldots \}$)                                                                                                                                                                                                                             |
| $\epsilon,\delta$ | Small positive real numbers  (very close to $0$)                                                                                                                                                                                                                                        |
| $x,y,z,w$         | Strings in $\{0,1\}^*$, though sometimes we will use these identifiers numbers or other objects. We will often identify an object with its representation as a string.                                                                                                                  |
| $G$               | A _graph_. The set of vertices of $G$ is often denoted by $V$, and often it is simply the set $[n]=\{0,\ldots, n\}$. The set of edges of $G$ is often denoted by $E$.                                                                                                                   |
| $S$               | Sets                                                                                                                                                                                                                                                                                    |
| $f,g,h$           | Functions. We will often (though not always) use lowercase identifiers for _finite functions_, which map  $\{0,1\}^n$ to $\{0,1\}^m$ (often $m=1$).                                                                                                                                      |
| $F,G,H$           | Infinite (unbounded input) functions mapping $\{0,1\}^*$ to $\{0,1\}^*$ or $\{0,1\}^*$ to $\{0,1\}^m$ for some $m$. Note that the identifiers $G,H$ are sometimes used to denote a function and sometimes a graph. It will always be clear from the context which of these is the case. |
| $A,B,C$           | Boolean circuits                                                                                                                                                                                                                                                                        |
| $M$               | Turing machines                                                                                                                                                                                                                                                                         |
| $P,Q$             | Programs                                                                                                                                                                                                                                                                                |
| $T$               | A function mapping $\mathbb{N}$ to $\mathbb{N}$ that corresponds to a time bound.                                                                                                                                                                                                       |
| $c$               | A positive number (often an unspecified constant: for example if $T(n)=O(n)$ then there is some number $c$ such that $T(n) \leq c \cdot n$ every $n>0$). We sometimes use $a,b$ in a similar way.                                                                                       |
| $\Sigma$          | Finite set (often used as the _alphabet_ for a set of strings).                                                                                                                                                                                                                            |




> # { .recap }
* The basic "mathematical data structures" we'll need are _numbers_, _sets_, _tuples_, _strings_, _graphs_ and _functions_.
* We can use basic objects to define more complex notions. For example, _graphs_ can be defined as a list of _pairs_.
* Given precise _definitions_ of objects, we can state unambiguous and precise _statements_. We can then use mathematical _proofs_ to determine whether these statements are true or false.
* A mathematical proof is not a formal ritual but rather a clear, precise and "bulletproof" argument certifying the truth of a certain statement.
* Big-$O$ notation is an extremely useful formalism to suppress less significant details and allow us to focus on the high level behavior of quantities of interest.
* The only way to get comfortable with mathematical notions is to apply them in the contexts of solving problems. You should expect to need to go back time and again to the definitions and notation in this lecture as you work through problems in this course.


## Exercises



::: {.exercise title="Logical expressions" #logicalex}
a. Write a logical expression $\varphi(x)$ involving the variables $x_0,x_1,x_2$ and the operators $\wedge$ (AND), $\vee$ (OR), and $\neg$ (NOT), such that $\varphi(x)$ is true if the majority of the inputs are _True_.

b. Write a logical expression $\varphi(x)$ involving the variables $x_0,x_1,x_2$ and the operators $\wedge$ (AND), $\vee$ (OR), and $\neg$ (NOT), such that $\varphi(x)$ is true if the sum $\sum_{i=0}^{2} x_i$ (identifying "true" with $1$ and "false" with $0$)  is _odd_.
:::

::: {.exercise title="Quantifiers" #quantifiersex}
Use the logical quantifiers $\forall$ (for all), $\exists$ (there exists), as well as $\wedge,\vee,\neg$ and the arithmetic operations $+,\times,=,>,<$ to write the following:

a. An expression $\varphi(n,k)$ such that for every natural numbers $n,k$, $\varphi(n,k)$ is true if and only if $k$  divides $n$.

b. An expression $\varphi(n)$ such that for every natural number $n$, $\varphi(n)$ is true if and only if $n$ is a power of three.

:::


> # {.exercise }
Describe the following statement in English words: $\forall_{n\in\N} \exists_{p>n} \forall{a,b \in \N} (a\times b \neq p) \vee (a=1)$.



::: {.exercise title="Set construction notation" #setsdescription}
Describe in words the following sets:

a. $S = \{ x\in \{0,1\}^{100} : \forall_{i\in \{0,\ldots, 99\}} x_i = x_{99-i} \}$

b. $T = \{ x\in \{0,1\}^* : \forall_{i,j \in \{2,\ldots,|x|-1 \} } i\cdot j \neq |x| \}$

:::


::: {.exercise title="Existence of one to one mappings" #cardinalitiesex}
For each one of the following pairs of sets $(S,T)$, prove or disprove the following statement: there is a one to one function $f$ mapping $S$ to $T$.

a. Let $n>10$. $S = \{0,1\}^n$ and $T= [n] \times [n] \times [n]$.

b. Let $n>10$. $S$ is the set of all functions mapping $\{0,1\}^n$ to $\{0,1\}$. $T = \{0,1\}^{n^3}$.

c. Let $n>100$. $S = \{k \in [n]  \;|\; k \text{ is prime} \}$, $T = \{0,1\}^{\ceil{\log n -1}}$.
:::

::: {.exercise title="Inclusion Exclusion" #inclex }
a. Let $A,B$ be finite sets. Prove that $|A\cup B| = |A|+|B|-|A\cap B|$.

b. Let $A_0,\ldots,A_{k-1}$ be finite sets. Prove that $|A_0 \cup \cdots \cup A_{k-1}| \geq \sum_{i=0}^{k-1} |A_i| - \sum_{0 \leq i < j < k} |A_i \cap A_j|$.

c. Let $A_0,\ldots,A_{k-1}$ be finite subsets of $\{1,\ldots, n\}$, such that $|A_i|=m$ for every $i\in [k]$. Prove that if $k>100n$, then there exist two distinct sets $A_i,A_j$ s.t. $|A_i \cap A_j| \geq m^2/(10n)$.
:::


::: {.exercise }
Prove that if $S,T$ are finite and $F:S \rightarrow T$ is one to one then $|S| \leq |T|$.
:::

> # {.exercise }
Prove that if $S,T$ are finite and $F:S \rightarrow T$ is onto then $|S| \geq |T|$.


> # {.exercise }
Prove that for every finite $S,T$, there are $(|T|+1)^{|S|}$ partial functions from $S$ to $T$.




> # {.exercise }
Suppose that $\{ S_n \}_{n\in \N}$ is a sequence such that $S_0 \leq 10$ and for $n>1$ $S_n \leq 5 S_{\lfloor \tfrac{n}{5} \rfloor} + 2n$.
Prove by induction that  $S_n \leq 100 n \log n$ for every $n$.

> # {.exercise }
Prove that for every undirected graph $G$ of $100$ vertices, if every vertex has degree at most $4$, then there exists a subset $S$ of at $20$ vertices such that no two vertices in $S$ are neighbors of one another.



::: {.exercise title="$O$-notation" #ohnotationex}
For every pair of functions $F,G$ below, determine which of the following relations holds: $F=O(G)$, $F=\Omega(G)$, $F=o(G)$ or $F=\omega(G)$.

a. $F(n)=n$, $G(n)=100n$.

b. $F(n)=n$, $G(n)=\sqrt{n}$.

c. $F(n)=n\log n$, $G(n)=2^{(\log (n))^2}$.

d. $F(n)=\sqrt{n}$, $G(n)=2^{\sqrt{\log n}}$

e. $F(n) = \binom{n}{\ceil{0.2 n}}$ ,  $G(n) = 2^{0.1 n}$ (where $\binom{n}{k}$ is the number of $k$-sized subsets of a set of size $n$) and $g(n) = 2^{0.1 n}$.^[_Hint:_ one way to do this is to use [Stirling's approximation for the factorial function.](https://goo.gl/cqEmS2).]
:::

> # {.exercise}
Give an example of a pair of functions $F,G:\N \rightarrow \N$ such that neither $F=O(G)$ nor $G=O(F)$ holds.


::: {.exercise  #graphcycleex}
Prove that for every undirected graph $G$ on $n$ vertices, if $G$ has at least $n$ edges then $G$ contains a cycle.
:::

::: {.exercise #indsetex}
Prove that for every undirected graph $G$ of $1000$ vertices, if every vertex has degree at most $4$, then there exists a subset $S$ of at least $200$ vertices such that no two vertices in $S$ are neighbors of one another.
:::

## Bibliographical notes { #notesmathchap }

The section heading "A Mathematician's Apology", refers of course to Hardy's classic book [@Hardy41].
Even when Hardy is wrong, he is very much worth reading.

There are many online sources for the mathematical background needed for this book. In particular, the lecture notes for MIT 6.042 "Mathematics for Computer Science" [@LehmanLeightonMeyer] are extremely comprehensive, and videos and assignments for this course are available online.
Similarly, [Berkeley CS 70: "Discrete Mathematics and Probability Theoru"](http://www.eecs70.org/) has extensive lecture notes online.
The book of Rosen [@Rosen19discrete] also covers much of this  material.
See also Jim Aspens' online book [@AspensDiscreteMath].

The book by Lewis and Zax [@LewisZax19], as well as the online book of Fleck [@Fleck], give a more gentle overview of the much of the same material. Solow's book [@Solow14] is a good gentle introduction to proof reading and writing. Kun's book [@Kun18] gives an introduction to mathematics aimed at readers with programming background.
Stanford's [CS 103 course](https://cs103.stanford.edu)  has a wonderful collections of handouts on mathematical proof techniques and discrete mathematics.
