#  Cryptography

>_"Human ingenuity cannot concoct a cipher which human ingenuity cannot resolve."_, Edgar Allen Poe, 1841

>_"I hope my handwriting, etc. do not give the impression I am just a crank or circle-squarer....  a logical way to classify enciphering processes is by the way in which the computation [of key recovery attack]... increases with increasing length of the key. This is at best exponential and at worst probably at most a relatively small power of [the key length]... The significance of this conjecture [that certain encryption schemes are exponentially secure against key recovery attacks] .. is that it is  quite feasible to design ciphers that are effectively unbreakable. "_, John Nash, [letter to the NSA](https://www.nsa.gov/news-features/declassified-documents/nash-letters/assets/files/nash_letters1.pdf), 1955.

>_"“Perfect Secrecy” is defined by requiring of a system
that after a cryptogram is intercepted by the enemy the a posteriori
probabilities of this cryptogram representing various messages be
identically the same as the a priori probabilities of the same
messages before the interception. It is shown that perfect secrecy
is possible but requires, if the number of messages is finite, the
same number of possible keys."_, Claude Shannon, 1945

>_"We stand today on the brink of a revolution in cryptography."_, Whitfeld Diffie and Martin Hellman, 1976



Cryptography - the art or science of "secret writing" - has been around for
several millenia, and for almost all of that time Edgar Allan Poe's quote above
held true. Indeed, the history of cryptography is littered with the figurative
corpses of cryptosystems believed secure and then broken, and sometimes with the
actual corpses of those who have mistakenly placed their faith in these
cryptosystems.

Yet, something changed in the last few decades, which is the "revolution" alluded to (and to a large extent initiated by) Diffie and Hellman's 1976 paper quoted above.
New cryptosystems have been found that have not been broken despite being subjected to immense
efforts involving both human ingenuity and computational power on a scale that
completely dwarves the "crypto breakers" of Poe's time. Even more amazingly,
these cryptosystem are not only seemingly unbreakable, but they also achieve
this under much harsher conditions. Not only do today's attackers have more
computational power but they also have more data to work with. In Poe's age, an
attacker would be lucky if they got access to more than a few ciphertexts with
known plaintexts. These days attackers might have massive amounts of data-
terabytes or more - at their disposal. In fact, with *public key* encryption,
an attacker can generate as many ciphertexts as they wish.

The key to this success has been a clearer understanding of both how to _define_ security for cryptographic tools and how to relate this security to _concrete computational problems_.
Cryptography is a vast and continuously changing topic, but we will touch on some of these issues in this paper.

## Classical cryptosystems

A great many cryptosystems have been devised and broken throughout the ages.
Let us recount just one such story.
In 1587, Mary the queen of Scots, and the heir to the throne of England, wanted to arrange the assasination of her cousin, queen Elisabeth I of
England, so that she could ascend to the throne and finally escape the house arrest under which she has been for the last 18 years.
As part of this complicated plot, she sent a coded letter to Sir Anthony Babington. It is what's known as a _substitution cipher_ where each letter is transformed into a different symbol, and so
the resulting letter looks something like [maryscottletterfig](){.ref}.

![Snippet from encrypted communication between queen Mary and Sir Babington](../figure/encrypted_letter.jpg){#maryscottletterfig .class width=300px height=300px}



At a first look, such a letter might seem rather inscrutable- a meaningless sequence of strange symbols. However, after some thought, one might recognize that these symbols _repeat_ several
times and moreover that different symbols repeat with different frequencies. Now it doesn't take a large leap of faith to assume that perhaps each symbol corresponds to a different letter
and the more frequent symbols correspond to letters that occur in the alphabet with higher frequency. From this observation, there is a short gap to completely breaking the cipher,
which was in fact done by queen Elisabeth's spies who used the decoded letters to learn of all the co-conspirators and to convict queen Mary of treason, a crime for which she was executed.

Trusting in superficial security measures (such as using "inscrutable" symbols) is a trap that users of cryptography have been falling into again and again over the years.
(As in many things, this is the subject of a great XKCD cartoon, see [XKCDnavajofig](){.ref}.)


![On the added security of using uncommon symbols](../figure/code_talkers.png){#XKCDnavajofig .class width=300px height=300px}

## Defining encryption

Many of the troubles that cryptosystem designers faced over history (and still face!) can be attributed to not properly defining or understanding what are the goals they want to achieve in the first place.
Let us focus on the setting of _private key encryption_.^[If you don't know what "private key" means, you can ignore this adjective for now. For thousands of years, "private key encryption" was synonymous with encryption. Only in the 1970's was the concept of _public key encryption_ invented.]
A _sender_ (traditionally called "Alice") wants to send a message (known also as a _plaintext_) $x\in \{0,1\}^\*$ to a _receiver_ (traditionally called "Bob").
They would like their message to be kept secret from an _adversary_ who listens in or "eavesdrops" on the communication channel (and is traditionally called "Eve").

Alice and Bob share a _secret key_ $k \in \{0,1\}^*$.
Alice uses the key $k$ to "scramble" or _encrypt_ the plaintext  $x$ into a _ciphertext_ $y$, and Bob uses the key $k$ to "unscramble" or _decrypt_ the ciphertext $y$ back into the plaintext $x$.
This motivates the following definition:

> # {.definition title="Valid encryption scheme" #encryptiondef}
Let $\ell:\N \rightarrow \N$ be some function.
A pair of polynomial-time computable functions $(E,D)$ mapping strings to strings is a _valid private key encryption scheme_ (or _encryption scheme_ for short) with plaintext length $\ell(\cdot)$ if
for every $k\in \{0,1\}^n$ and $x \in \{0,1\}^{\ell(n)}$,
$$
D(k,E(k,x))=x \;. \label{eqvalidenc}
$$

We will sometimes write the first input (i.e., the key) to the encryption and decryption as a subscript and so can write [eqvalidenc](){.eqref} also as  $D_k(E_k(x))=x$.

## Defining security of encryption

[encryptiondef](){.ref} says nothing about the _security_ of $E$ and $D$, and even allows the trivial encryption scheme that ignores the key altogether and sets $E_k(x)=x$ for every $x$.
Defining security is not a trivial matter.

> # { .pause }
You would appreciate the subleties of defining security of encryption if at this point you take a five minute break from reading, and try (possibly with a partner) to brainstorm on how you would mathematically define the notion that an encryption scheme is _secure_, in the sense that it protects the secrecy of the plaintext $x$.


Throuhgout history, many attacks on  cryptosystems  are rooted in the cryptosystem designers' reliance on  "security through obscurity"---
trusting that the fact their _methods_ are not known to their enemy will
protect them from being broken.
This is a faulty assumption - if you reuse a
method again and again (even with a different key each time) then eventually
your adversaries will figure out what you are doing.
And if Alice and Bob meet frequently in a secure location to decide on a new method, they might as
well take the opportunity to exchange their secrets.
These considerations led  Auguste Kerchoffs in 1883 to state the following principle:

>_A cryptosystem should be secure even if everything about the system, except
the key, is public knowledge._ ^[The actual quote is "Il faut qu’il n’exige pas le secret, et qu’il puisse sans inconvénient tomber entre les mains de l’ennemi"  loosely translated as
"The system must not require secrecy and can be stolen by the enemy without
causing trouble". According to Steve Bellovin the NSA version is "assume that the first
copy of any device we make is shipped to the Kremlin".]

Why is it OK to assume the key is secret and not the algorithm? Because we can always choose a fresh key.
But of course that won't help us much if our key is if we choose our key to be "1234" or "passw0rd!".
In fact, if you use _any_ deterministic algorithm
to choose the key then eventually your adversary will figure this out.
Therefore for security we must choose the key at _random_ and can restate Kerchkoffs's principle as follows:


>_There is no secrecy without randomness_

This is such a crucial point that is worth repeating:

>_There is no secrecy without randomness_

At the heart of every cryptographic scheme there is a secret key, and the secret key is always chosen at random.
A corollary of that is that to understand cryptography, you need to know  probability theory.

## Perfect secrecy

If you think about encryption scheme security for a while, you might come up with the following principle for defining security: _"An encryption scheme is secure if it is not possible to recover the key $k$ from $E_k(x)$"_.
However,  a moment's thought shows that the key is not really what we're trying to protect.
After all, the whole point of an encryption is to protect the confidentiality of the _plaintext_ $x$.
So, we can try to define  that _"an encryption scheme is secure if it is not possible to recover the plaintext $x$ from $E_k(x)$"_.
Yet it is not clear that it means.
Suppose that an encryption scheme reveals the first 10 bits of the plaintext $x$.
It might still not be possible to recover $x$ completely, but on an intuitive level, this seems like it would be extremely unwise to use it in practice.
Indeed, often even _partial information_ about the plaintext is enough for the adversary to achieve its goals.

The above thinking led Shannon in 1945 to formalize the notion of _perfect secrecy_, which is that an encryption reveals absolutely nothing about the message.
There are several equivalent ways to define it, but perhaps the cleanest one is the following:

> # {.definition title="Perfect secrecy" #perfectsecrecy}
A valid encryption scheme $(E,D)$ with length $\ell(\cdot)$ is _perfectly secrect_ if for every $n\in \N$ and plaintexts $x,x' \in \{0,1\}^{\ell(n)}$, the following two distributions $Y$ and $Y'$ over $\{0,1\}^*$ are identical:
>
* The distribution $Y$ is obtained by sampling a random $k\sim \{0,1\}^n$ and outputting $E_k(x)$.
>
* The distribution $Y$ is obtained by sampling a random $k\sim \{0,1\}^n$ and outputting $E_k(x')$.

> # { .pause }
This definition might take more than one reading to parse. Try to think of how this condition would correspond to your intuitive notion of "learning no information" about $x$ from observing $E_k(x)$.
In particular, suppose that you knew ahead of time that Alice sent either an encryption of $x$ or an encryption of $x'$. Would you learn anything new from observing the encryption of the message that Alice actually sent? It may help you to look at [perfectsecfig](){.ref}.

![For any key length $n$, we can visualize an encryption scheme $(E,D)$ as a graph where we put a vertex for every one of the $2^{\ell(n)}$ possible plaintexts and for every one of the ciphertexts in $\{0,1\}^*$ that can be output by $E$ on a length $n$ key and length $\ell(n)$ plaintext. We connect a plaintext $x$ and a ciphertext $y$ by an edge if there is some key $k$ such that $E_k(x)=y$, and in this case we label the edge by $k$.  By the validity condition, if we pick any fixed key $k$, the map $x \mapsto E_k(x)$ must be one-to-one. If we make the (mild) assumption that any two distinct keys map $x$ to distinct ciphertext, each plaintext vertex will have degree $2^n$ in this graph. In such a case the condition of perfect secrecy simply corresponds to the condition that every two    plaintexts $x$ and $x'$, the set of neighbors of $x$ is the same as the set of neighbors of $x'$.](../figure/perfectsecrecy.png){#perfectsecfig .class width=300px height=300px}

### Example: Perfect secrecy in the battlefield

To understand [perfectsecrecy](){.ref}, suppose that Alice sends only one of two possible messages: "attack" or "retreat", which we denote by $x_0$ and $x_1$ respectively, and that she sends each one of those messages with probability $1/2$.
Let us put ourselves in the shoes of _Eve_, the eavesdropping adversary.
A priori we would have guessed that Alice sent either $x_0$ or $x_1$ with probability $1/2$.
Now we observe $y=E_k(x_i)$ where $k$ is a uniformly chosen key in $\{0,1\}^n$.
How does this new information cause us to update our beliefs on whether Alice sent $x_0$ or $x_1$?

> # { .pause }
Before reading the next paragraph, you might want to try the analysis yourself.
You may find it useful to  look at the [Wikipedia entry on Bayesian Inference](https://en.wikipedia.org/wiki/Bayesian_inference) or [these MIT lecture notes](https://ocw.mit.edu/courses/mathematics/18-05-introduction-to-probability-and-statistics-spring-2014/readings/MIT18_05S14_Reading11.pdf).

Let us define $p_0(y)$ to be the probability (taken over $k\sim \{0,1\}^n$) that $y=E_k(x_0)$ and similarly $p_1(y)$ to be $\Pr_{k \sim \{0,1\}^n}[y=E_k(x_1)]$.
Note that, since Alice chooses the message to send at random, our a priori probability for observing $y$ is $\tfrac{1}{2}p_y(0) + \tfrac{1}{2}p_y(1)$.
However, as per [perfectsecrecy](){.ref},   the perfect secrecy condition guarantees that $p_y(0)=p_y(1)$!
Let us denote the number $p_y(0)=p_y(1)$ by $p$.
By the formula for conditional probability, the probability that Alice sent the message $x_0$ conditioned on our observation $y$ is simply^[The equation [bayeseq](){.eqref} is a special case of [Bayes' rule](https://en.wikipedia.org/wiki/Bayes%27_theorem) which, although a simple restatement of the formula for conditional probability, is an extremely important and widely used tool in statistics and data analysis.]
$$
\Pr[i=0 | y=E_k(x_i)] = \frac{\Pr[i=0 \wedge y = E_k(x_i)]}{\Pr[y = E_k(x)]} \;. \label{bayeseq}
$$

Since the probability that $i=0$ and $y$ is the cyphtertext $E_k(0)$ is equal to $\tfrac{1}{2}\cdot p_y(0)$, and the a priori probability of observing $y$ is $\tfrac{1}{2}p_y(0) + \tfrac{1}{2}p_y(1)$,
we can rewrite [bayeseq](){.eqref} as
$$
\Pr[i=0 | y=E_k(x_i)] = \frac{\tfrac{1}{2}p_y(0)}{\tfrac{1}{2}p_y(0)+\tfrac{1}{2}p_y(1)}  =  \frac{p}{p +p}  = \frac{1}{2}
$$
using the fact that $p_y(0)=p_y(1)=p$.
This means that observing the ciphertext $y$ did not help us at all! We still would not be able to guess whether Alice sent "attack" or "retreat" with better than 50/50 odds!

This example can be vastly generalized to show that perfect secrecy is indeed "perfect" in the sense that observing a ciphertext gives Eve _no additional information_ about the plaintext beyond her apriori knowledge.

### Constructing perfectly secret encryption

_Perfect security_ is an extremely strong condition, and implies that an eavesdropper does not learn _any_ information from observing the ciphertext.
You might think that an encryption scheme satisfying such a strong condition will be impossible, or at least extremely complicated, to achieve.
However it turns out we can in fact obtain perfectly secure encryption scheme fairly easily.
In particular, the following  table details a perfectly secure encryption scheme for encrypting two bit messages:



+---------+-------+-------+-------+-------+-------+
| Plain:  |       | __00__| __01__| __10__| __11__|
+---------+-------+-------+-------+-------+-------+
| Cipher: |       |       |       |       |       |
+---------+-------+-------+-------+-------+-------+
|         | __00__|     00|     01|     10|     11|
+---------+-------+-------+-------+-------+-------+
|         | __01__|     01|     00|     11|     10|
+---------+-------+-------+-------+-------+-------+
|         | __10__|     10|     11|     00|     01|
+---------+-------+-------+-------+-------+-------+
|         | __11__|     11|     10|     01|     00|
+---------+-------+-------+-------+-------+-------+

  : A perfectly secret encryption scheme with $2$ bit keys, plaintexts, and ciphertexts; the rows are indexed by possible ciphertexts, the columns indexed
  by possible plaintexts, and the $(y,x)$ location of the matrix corresponds to the key   that maps $x$ to $y$.


In fact, this can be generalized to any number of bits:

__Theorem (One time pad, Vernam 1917):__ For every $n$, there is a perfectly secret encryption $(E,D)$ with plaintexts of $n$ bits, where the key size and the ciphertext size is also $n$.



## Lecture summary


## Exercises




## Bibliographical notes

Much of this text is taken from  my lecture notes on cryptography.

Shannon's manuscript was written in 1945 but was classified, and a partial version was only published in 1949. Still it has revolutionized cryptography, and is the forerunner to much of what followed.


John Nash made seminal contributions in mathematics and game theory, and was awarded both the Abel Prize in mathematics and the  Nobel Memorial Prize in Economic Sciences.
However, he hus struggled with mental illness throughout his life.
His biography, [A Beautiful Mind](https://en.wikipedia.org/wiki/A_Beautiful_Mind_(book)) was made into a popular movie.
It is natural to compare Nash's 1955 letter to the NSA to Gödel's letter to von Neumann we mentioned before.
From the theoretical computer science point of view, the crucial difference is that while Nash informally talks about exponential vs polynomial computation time, he does not mention the word "Turing Machine" or other models of computation, and it is not clear if he is aware or not that his conjecture can be made mathematically precise (assuming a formalization of "sufficiently complex types of enciphering").


## Further explorations

Some topics related to this lecture that might be accessible to advanced students include: (to be completed)



## Acknowledgements
