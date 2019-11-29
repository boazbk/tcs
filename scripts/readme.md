# Markdown book scripts

__Boaz Barak__

This is a set of scripts that I use in combination with pandoc to produce the book 
"Introduction To Theoretical Computer Science" ( https://introtcs.org )

It builds on pandoc and panflute.

THIS IS NOT A WORKING PACKAGE. It is a snapshot of part of my setup at this current point in time.
Some parts of it are hardwired to this particular book and my particular Windows setup.

However, if you are proficient in Python and other tools, you should be able to adapt it to yours.

At the moment I am using an HTML template that is an adaptation of the Bookdown template (itself adapted from the Gitbook project) and a LaTeX template that is an adaptation of the Tufte Latex template. However, the scripts can be modified to work with other templates as well.

These scripts are based on an original version written by David Steurer and used for our  lecture notes on the Sum of Squares algorithm https://sumofsquares.org

__ChristianMay21__

I have begun trying to generalize these scripts to:
a) allow it to be utilized by any windows user with little if any customization
b) do so in such a way as to avoid editing currently existing files - everything else, for now, will be "layered on top" of Professor Barak's working implementation. This is so that increased utility is available for new users without forcing Professor Barak to change his implementation - I doubt he'd enjoy having to do that.

So far, it appears I have gotten the latex rendering to work correctly - I'm currently working on the html, so that I can render the html and then hopefully tackle some html rendering bugs.

I documented all of the dependencies I had to add - there may be a handful which were already on my system and therefore are not included here. Where possible, I have used .gitignore files and a python script (setup.py) to add file dependencies dynamically).

## Getting up and running (kind of)
* Install [pandoc](https://pandoc.org/installing.html). I used [Chocolatey](https://chocolatey.org/). This is used everywhere. `choco install pandoc`
* Install [MiKTeX](https://miktex.org/download), following [these instructions](http://www.texts.io/support/0002/) (but using the first link in this bullet to get the executable). This will install XeLaTeX, which is used by the book filter script. 
* Install the python module bibtexparser: `pip install bibtexparser`. This is uesed by book-filter.py. 
* Run `setup.py` in the root directory - this copies files into the content folder to be used in rendering. `python setup.py`

Currently, what should be functioning is the rendering of the markdown files into LaTeX. After doing the above, simply navigate your command-line interface of choice to the scripts folder and run `make all-tex`. This should output the rendered tex files to the `latex-book` directory in `scripts`. Note that these files will not show in git changes, as git has been instructed to ignore all files in the `latex-book` folder as they are the result of a build process. 