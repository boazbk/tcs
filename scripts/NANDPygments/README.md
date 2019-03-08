# pygments-custom-nand



A custom NAND-lexer for [Pygments](http://pygments.org/), for extra keyword highlighting when using the package [minted](https://github.com/gpoore/minted) in LaTeX. Adds some extra keywords like *NAND*, *loop*

Based on [this CPP Lexer](https://github.com/FSund/pygments-custom-cpplexer.git)

## Install

    $ (sudo) python setup.py install

### Verify

Verify that the package installed correctly by looking for the lexer "nand" in the output of

    $ pygmentize -L lexers

## Using the lexer in latex

Just use the **nand** "language". In LaTeX this means something like this

    \begin{minted}{nand}
    x = NAND(a,b)
    \end{minted}

See the minted package at https://github.com/gpoore/minted for more information.
