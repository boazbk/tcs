# Make file for transforming markdown to latex->pdf, html, and ms-word
# Boaz Barak 2019, based on scripts of David Steurer
# This file will not work as is for your application and will need to be tailored
# It is just put here as help to design your own makefile
# It has hardwired in it a certain directory structure which you might want to modify


opts := -f markdown+fenced_divs-auto_identifiers --section-divs --katex

latex-book/%.tex: content/%.md book-filter.py content/metadata.yaml
	@echo "<<<LATEX-BOOK $*>>>"
	@pandoc -f markdown+smart+fenced_divs-auto_identifiers --preserve-tabs --section-divs  --biblatex -F book-filter.py   -o $@ $< content/metadata.yaml

html/%.html: content/%.md book-filter.py content/metadata.yaml book-template.html
		@echo "<<<HTML-BOOK $*>>>"
		@pandoc -f markdown+smart+fenced_divs --preserve-tabs  -F book-filter.py --mathjax --template book-template.html  -o $@ $< content/metadata.yaml

binaries/%.docx: content/%.md
		@echo "<<<WORD $*>>>"
		cd binaries && pandoc -f markdown+smart+fenced_divs+latex_macros   -o  ../$@ ../content/macros.tex ../content/msword.md ../$< ../content/metadata.yaml


lectures := $(patsubst content/%.md,%,$(wildcard content/lec*.md))




book-targets := $(foreach l,$(lectures),latex-book/$(l).tex)


html-targets := $(foreach l,$(lectures),html/$(l).html)

docx-targets := $(foreach l,$(lectures),binaries/$(l).docx)


aux-yaml:
	@echo "Preparing bookaux.yaml"
	python auxtoyaml.py "latex-book/"
	

all-html: aux-yaml $(html-targets) html/index.html

all-tex: $(book-targets)

all-word: $(docx-targets)

latex-book/lnotes_book.pdf: all-tex
	@echo "<<<PDF-BOOK WINDOWS>>>"
	cd latex-book && xelatex -quiet -shell-escape  lnotes_book.tex && Biber lnotes_book && xelatex -quiet -shell-escape  lnotes_book.tex

book: all-html all-tex latex-book/lnotes_book.pdf

rename-book-parts:
	scripts/rename.sh

compress-book:
	  $(GHOSTSCRIPT)  \
	  -sDEVICE=pdfwrite \
	  -dPDFSETTINGS=/ebook \
	  -dDownsampleColorImages=true \
	  -dDownsampleGrayImages=true \
	  -dDownsampleMonoImages=true \
	  -dColorImageResolution=300 \
	  -dGrayImageResolution=300 \
	  -dMonoImageResolution=300 \
	  -dColorImageDownsampleThreshold=1.0 \
	  -dGrayImageDownsampleThreshold=1.0 \
	  -dMonoImageDownsampleThreshold=1.0 \
	  -dNOPAUSE -dQUIET -dBATCH  -dCompatibilityLevel=1.4 \
	  -sOutputFile=binaries/lnotes_book.pdf  latex-book/lnotes_book.pdf


split-book-to-handouts: # write this part - currently hardwired to my own book in my implementation


just-deploy:
	scripts/deploy.sh

deploy: all-word book split-book-to-handouts rename-book-parts
	scripts/deploy.sh
