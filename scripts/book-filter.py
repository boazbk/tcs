"""
Pandoc filter using panflute
Some tools for the intro to theoretical cs book
Boaz Barak
At the moment this is in pretty rough shape, and cannot be used as is for any other project, 
but I am posting it in case anyone else finds it useful.

Some of the main extensions it handles:

1. Add cross-references to HTML using the LaTeX aux file so the two versions are consistent.
2. Handle some custom environments that are written in markdown in the form

::: {.class }

:::

3. Handle pseudocode blocks.

4. Some extensions to tables and figures.

5. Some extensions and transformations to math equations, and in particular handling equation references in HTML,
as well as automatic prettifying of identifiers with more than one letter.

The general philosophy is to try to do everything in this filter so that the markdown source 
contains no latex code outside of math nor any html code.
"""

import panflute as pf
import fractions
import sys
import yaml
import os
import time
import json
import re
import io
import csv
import bibtexparser
import LaTexAccents as latex_accents
import uuid
from matplotlib.cbook import dedent


class MyTable(pf.Table):
    """Some attempt to handle tabular, not successful so far"""
    __slots__ = ["identifier"]

    def __init__(self, *args, **_3to2kwargs):
        if "identifier" in _3to2kwargs:
            self.identifier = _3to2kwargs["identifier"]
            del _3to2kwargs["identifier"]
        super().__init__(*args, **_3to2kwargs)


def pdflink(doc):
    """Link to the PDF version of the document"""
    pdfbase = doc.get_metadata("binarybaseurl", "")
    file = pdfbase + "/" + doc.get_metadata("filename", "nofile") + ".pdf"
    HTML = (
        "\n"
        + fr"""<div><p style="color:#871640;">&#x2605; See also the <a id="pdflink" href='{file}'><b>PDF version of this chapter</b></a> (better formatting/references) &#x2605;</p></div>"""
        + "\n"
    )
    doc.metadata["pdffile"] = pf.MetaString(file)
    doc.metadata["pdflink"] = pf.MetaBlocks(pf.RawBlock(HTML, format="html"))


def writetoc(doc, TOC):
    """Write to the table of content"""
    logstring("\nWriting TOC:\n" + TOC, doc)
    doc.metadata["toc"] = pf.MetaBlocks(pf.RawBlock(TOC, format="html"))


def logstring(s, doc):
    """Log a string to the log file"""
    doc.logfile.write(s + "\n")


def log(d, e, doc):
    """Log an element to the log file"""
    s = "  " * d + str(e)
    doc.logfile.write(s + "\n")


def prepare(doc):
    """Initial function called at the beginning of the filter"""
    file = doc.get_metadata("filename", "")
    doc.sourcedir = doc.get_metadata("sourcedir", "content/")
    bibfile = doc.get_metadata("bibfile", "")
    if bibfile:
        doc.bibfile = os.path.join(doc.sourcedir, bibfile)
    else:
        doc.bibfile = ""
    if doc.bibfile:
        with open(doc.bibfile) as bibtex_file:
            doc.bibentries = bibtexparser.load(bibtex_file).entries_dict
    else:
        doc.bibentries = {}

    logdir = doc.get_metadata("logdir", "log")
    if not os.path.isdir(logdir):
        logdir = ""
    logfilename = (
        os.path.join(logdir, os.path.basename(file) + ".log")
        if file
        else "book-filter.log"
    )

    # logfilename = "log_"+file+".book.log"
    doc.label_descriptions = {}  # eventually handle different files, counters
    doc.searchtext = ""
    doc.logfile = open(logfilename, "w", encoding="utf-8")
    doc.logfile.write("LOG: argv:" + str(sys.argv) + "\n")
    doc.logfile.write("Metadata:\n" + str(doc.metadata) + "\n")
    doc.lastlabel = ""
    doc.counter = 0
    doc.chapternum = doc.get_metadata("chapternum", default="99")
    if doc.format == "html":
        doc.toc = removekeys(loadyaml("toc.yaml"), doc.chapternum + ".")
        pdflink(doc)

    auxfilename = doc.get_metadata("auxfile", "bookaux.yaml")
    doc.labels = loadyaml(auxfilename)
    doc.currentlevel = 1
    doc.currentplace = [doc.chapternum]
    doc.footnotecounter = 1
    doc.footnotecontents = []
    D = doc.get_metadata(
        "latexsectionheaders",
        {
            1: "chapter",
            2: "section",
            3: "subsection",
            4: "subsubsection",
            5: "paragraph",
            6: "subparagraph",
        },
    )
    doc.latex_headers = {int(k): D[k] for k in D}
    logstring("Latex Headers: " + str(doc.latex_headers), doc)
    doc.label_classes = doc.get_metadata(
        "latexsectionheaders", {"solvedex": "Solved Exercise", "bigidea": "Big Idea"}
    )

    # These do all the work
    doc.handlers = [
        h_paragraph,
        h_csvtable,
        h_add_search,
        h_block_header,
        h_link_ref,
        h_latex_headers,
        h_latex_div,
        h_code_block,
        h_pseudocode,
        h_code_inline_draft,
        h_latex_image,
        h_latex_cite,
        h_html_footnote,
        h_html_header,
        h_emph,
        h_math,
        h_html_image,
        h_html_code_block
    ]
    # h_code_inline for nice highlighting in code


def finalize(doc):
    """Function called at the end of the filter"""
    doc.metadata["compiletime"] = pf.MetaString(time.strftime("%m/%d/%Y %H:%M:%S"))
    if doc.format == "html":
        dumpyaml(doc.toc, "toc.yaml")
        writetoc(doc, tochtml(doc.toc, doc.get_metadata("booktitle", "")))
        if doc.get_metadata("indexpage", False):
            indexhtml(doc)
        file = doc.get_metadata("filename", "")
        title = doc.get_metadata("title", "")
        searchindex = doc.get_metadata("searchindex", "")
        logstring("Search index " + file + "," + title + "," + searchindex, doc)
        if file and title and searchindex:
            t = re.sub(r"\\\w+", " ", doc.searchtext.lower())
            text = re.sub("[^a-zA-Z -]", "", t)
            updateindex(searchindex, file + ".html", title, text, doc)

    if doc.format == "html" and doc.footnotecontents:
        logstring("inserting " + str(doc.footnotecontents), doc)
        L = (
            [pf.RawBlock("<ol>", format="html")]
            + doc.footnotecontents
            + [pf.RawBlock("</ol>", format="html")]
        )
        footnotes = pf.Div(*L, identifier="footnotediv", classes=["footnotes"])
        doc.content.append(footnotes)

    doc.logfile.close()


def updateindex(filename, page, title, text, doc):
    """Update the file filename with an entry of the form [page,title,text]. Remove entry with page if it exists"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            index = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logstring(filename + " not found", doc)
        index = []
    new_idx = [a for a in index if a[0] != page]
    new_idx.append([page, title, text])
    with open(filename, "w", encoding="utf-8") as f:
        logstring("writing to " + filename, doc)
        json.dump(new_idx, f)


#########################################################
# Handle labels


def getlabel(label, doc):
    """
    Return name (e.g., `Theorem 12.1`) and link (e.g. 'blah.html#mainthm') for a given label.
    use the labels dictionary that is initialized from a yaml file 
    that is updated from the LateX aux file by the script auxtoyaml.py
    """
    name, number, file = get_full_label(label, doc)
    return f"{name} {number}", f"{file}#{label}"


def get_full_label(label, doc):
    """
    Return (name,number,file) given a label
    """
    T = doc.labels.get(label, None)
    if not T:
        return "??", "??", ""
    name = doc.label_classes.get(T["class"], T["class"].capitalize())
    number = T["number"] if T["number"] else ""
    file = T["file"] + ".html" if T["file"] != doc.get_metadata("filename", "") else ""
    return name, number, file


def labelref(e, doc):
    if e.identifier:
        return e.identifier
    regex = re.compile(r"[^a-zA-Z\-]")
    t = regex.sub("", pf.stringify(e).replace(" ", "-"))[:25]
    if t:
        return t
    return "temp"


################################################################
# Handle table of contents


def removekeys(toc, chapnum):
    """Return new dictionary with all keys that don't start with chapnum"""
    newtoc = {}
    l = len(chapnum)
    for key, value in toc.items():
        if key[:l] != chapnum:
            newtoc[key] = value
    return newtoc


def loadyaml(file, default={}):
    """Utility function to load from yaml file"""
    try:
        with open(file, "r", encoding="utf-8") as f:
            t = yaml.load(f)
    except FileNotFoundError:
        t = default
    return t


def dumpyaml(obj, file):
    """Utility function to write object to yaml file"""
    with open(file, "w", encoding="utf-8") as f:
        yaml.dump(obj, f)


def tocentry(title, file, href):
    return {"title": title, "filename": file, "href": href}


def addtocline(toc, place, title, file, href):
    placeasstring = ".".join([str(c) for c in place])
    toc[placeasstring] = tocentry(title=title, file=file, href=href)


def placekey(location):
    """For sorting toc entries"""
    M = 100
    d = 5

    def my(c):
        if c == "p":
            return -1
        try:
            return int(c)
        except ValueError:
            return 0

    L = [my(c) for c in location.split(".")]
    res = 0
    for i in range(len(L)):
        res += (M ** (d - i)) * L[i]
    return res


def tochtml(toc, title=""):
    """Generate HTML from toc"""
    keys = sorted(toc.keys(), key=placekey)

    def depth(key):
        return key.count(".")

    d = 0
    HTML = dedent(
        fr"""
        <ul class="summary">
        <li><a href="./">{title}</a></li>
        <li class="divider"></li>
        """
    )
    first = True
    for k in keys:
        e = toc[k]
        title = e["title"]
        file = e["filename"]
        ref = "#" + e["href"] if e["href"] else ""
        entry = ""
        if depth(k) == d and not first:
            entry = r"</li>"
        first = False
        if depth(k) > d:
            entry = r"<ul>" + r"<li><ul>" * (depth(k) - d - 1)
        if depth(k) < d:
            entry = r"</li>" + r"</ul></li>" * (d - depth(k))
        entry += dedent(
            fr"""
            <li class="chapter" data-level="{k}" data-path="{file}"><a href="{file}{ref}"><i class="fa fa-check"></i><b>{k}</b> {title}</a>
            """
        )
        HTML += entry
        d = depth(k)
    entry = r"</li>" + r"</ul></li>" * d
    HTML += entry + dedent(
        r"""
        <li class="divider"></li>
        </ul>
        """
    )
    return HTML


def indexhtml(doc):
    """Generate HTML index for title page"""
    keys = sorted(doc.toc.keys(), key=placekey)

    def depth(key):
        return key.count(".")

    HTML = fr"""<ul>"""
    for k in keys:
        e = doc.toc[k]
        title = e["title"]
        file = os.path.splitext(e["filename"])[0]
        base = doc.get_metadata("binarybaseurl", "")
        if depth(k) > 0:
            continue
        entry = dedent(
            fr"""
                <li><a href="{file+'.html'}"><b>Chapter {k}:</b> {title}</a>
                <small>(<a href="{base+'/'+file+'.pdf'}"><i class="fas fa-file-pdf"></i>PDF: best formatting</a> ,
                <a href="{base+'/'+file+'.docx'}"><i class="fas fa-file-word"></i>Word: buggy</a>)</small>
                </li>
                """
        )
        HTML += entry
    HTML += r"""</ul>"""
    doc.metadata["indexcontents"] = pf.MetaBlocks(pf.RawBlock(HTML, format="html"))


def h_emph(e, doc):
    if isinstance(e, pf.Emph) or isinstance(e, pf.Strong):
        doc.searchtext += " " + pf.stringify(e)
    return None


def h_html_header(e, doc):
    if not isinstance(e, pf.Header) or doc.format != "html":
        return None
    if doc.get_metadata("indexpage", False):
        return None
    if doc.chapternum == "99":
        return None
    logstring(f"--Evaluating header {e} level {e.level} vs {doc.currentlevel}", doc)
    if e.level > 1 and not pf.stringify(e):
        return None

    if e.level > len(doc.currentplace):
        doc.currentplace += ["0"] * (e.level - len(doc.currentplace))
    if e.level > 1:
        doc.currentplace = doc.currentplace[: e.level]
        t = int(doc.currentplace[e.level - 1])
        doc.currentplace[e.level - 1] = str(t + 1)
    href = "" if e.level == 1 else labelref(e, doc)
    if href in doc.labels and doc.labels[href]["number"]:
        place = doc.labels[href]["number"].split(".")
        e.attributes["number"] = doc.labels[href]["number"]
    else:
        place = doc.currentplace
        e.attributes["number"] = ".".join(place)
    place[0] = doc.chapternum
    # title = doc.get_metadata("title","---") if e.level==1 else pf.stringify(e)
    title = pf.stringify(e)
    if not title:
        return e
    addtocline(
        doc.toc,
        place=place,
        title=title,
        file=doc.get_metadata("filename", "") + ".html",
        href=href,
    )
    return e


##################################################
# CSV table
# Code adapted from https://github.com/ickc/pantable/blob/master/pantable/pantable.py
#


def get_width(options, number_of_columns, doc):
    """
    get width: set to `None` when
    1. not given
    2. not a list
    3. length not equal to the number of columns
    4. negative entries
    """
    try:
        # if width not exists, exits immediately through except
        width = options["width"]
        if not width:
            raise KeyError
        assert len(width) == number_of_columns
        custom_float = lambda x: float(fractions.Fraction(x))
        width = [custom_float(x) for x in options["width"]]
        assert all(i >= 0 for i in width)
    except KeyError:
        width = None
    except (AssertionError, ValueError, TypeError):
        width = None
        logstring("pantable: invalid width", doc)
    return width


def get_table_width(options, doc):
    """
    `table-width` set to `1.0` if invalid
    """
    try:
        table_width = float(fractions.Fraction((options.get("table-width", 1.0))), doc)
        assert table_width > 0
    except (ValueError, AssertionError, TypeError):
        table_width = 1.0
        logstring("pantable: invalid table-width", doc)
    return table_width


# end helper functions


def auto_width(table_width, number_of_columns, table_list, doc):
    """
    `width` is auto-calculated if not given in YAML
    It also returns None when table is empty.
    """
    # calculate width
    # The +3 match the way pandoc handle width, see jgm/pandoc commit 0dfceda
    width_abs = [
        3
        + max(
            [
                max([len(line) for line in row[column_index].split("\n")])
                for row in table_list
            ]
        )
        for column_index in range(number_of_columns)
    ]
    try:
        width_tot = sum(width_abs)
        # when all are 3 means all are empty, see comment above
        assert width_tot != 3 * number_of_columns
        width = [each_width / width_tot * table_width for each_width in width_abs]
    except AssertionError:
        width = None
        logstring("pantable: table is empty", doc)
    return width


def parse_alignment(alignment_string, number_of_columns, doc):
    """
    `alignment` string is parsed into pandoc format (AlignDefault, etc.).
    Cases are checked:
    - if not given, return None (let panflute handle it)
    - if wrong type
    - if too long
    - if invalid characters are given
    - if too short
    """
    # alignment string can be None or empty; return None: set to default by
    # panflute
    if not alignment_string:
        return None

    # prepare alignment_string
    try:
        # test valid type
        if not isinstance(alignment_string, str):
            raise TypeError
        number_of_alignments = len(alignment_string)
        # truncate and debug if too long
        assert number_of_alignments <= number_of_columns
    except TypeError:
        logstring("pantable: alignment string is invalid", doc)
        # return None: set to default by panflute
        return None
    except AssertionError:
        alignment_string = alignment_string[:number_of_columns]
        logstring("pantable: alignment string is too long, truncated instead.", doc)

    # parsing alignment
    align_dict = {
        "l": "AlignLeft",
        "c": "AlignCenter",
        "r": "AlignRight",
        "d": "AlignDefault",
    }
    try:
        alignment = [align_dict[i.lower()] for i in alignment_string]
    except KeyError:
        logstring(
            "pantable: alignment: invalid character found, default is used instead.",
            doc,
        )
        return None

    # fill up with default if too short
    if number_of_columns > number_of_alignments:
        alignment += [
            "AlignDefault" for __ in range(number_of_columns - number_of_alignments)
        ]

    return alignment


def list_from_csv(csvfile, doc):
    dialect = None
    try:
        dialect = csv.Sniffer().sniff(
            csvfile.read(1024), delimiters=[",", "\t", "|", ";", ":"]
        )
    except Exception as e:
        logstring("Error in detecting csv data: " + str(e), doc)
        return []
    csvfile.seek(0)
    return list(csv.reader(csvfile, dialect))


def read_data(include, data, doc):
    """
    read csv and return the table in list.
    Return None when the include path is invalid.
    """
    if include is None:
        with io.StringIO(data) as file:
            raw_table_list = list_from_csv(file, doc)
    else:
        try:
            with io.open(str(include)) as file:
                raw_table_list = list_from_csv(file, doc)
        except IOError:  # FileNotFoundError is not in Python2
            raw_table_list = None
            logstring("pantable: file not found from the path" + include, doc)
    return raw_table_list


def regularize_table_list(raw_table_list, doc):
    """
    When the length of rows are uneven, make it as long as the longest row.
    """
    length_of_rows = [len(row) for row in raw_table_list]
    number_of_columns = max(length_of_rows)
    try:
        assert all(i == number_of_columns for i in length_of_rows)
        table_list = raw_table_list
    except AssertionError:
        table_list = [
            row + ["" for __ in range(number_of_columns - len(row))]
            for row in raw_table_list
        ]
        logstring(
            "pantable: table rows are of irregular length. Empty cells appended.", doc
        )
    return (table_list, number_of_columns)


def parse_table_list(markdown, table_list, doc):
    """
    read table in list and return panflute table format
    """
    # make functions local
    to_table_row = pf.TableRow
    if markdown:
        to_table_cell = lambda x: pf.TableCell(*pf.convert_text(x))
    else:
        to_table_cell = lambda x: pf.TableCell(pf.Plain(pf.Str(x)))
    return [to_table_row(*[to_table_cell(x) for x in row]) for row in table_list]


def h_csvtable(e, doc):
    f = pf.yaml_filter(
        element=e, doc=doc, tag="table", function=convert2table, strict_yaml=True
    )
    if f:
        logstring("Found table " + str(f), doc)
    return f


def convert2table(options, data, doc, element):
    """
    provided to pf.yaml_filter to parse its content as pandoc table.
    """
    logstring("convert2table: received " + str(options) + ":" + str(data), doc)
    # prepare table in list from data/include
    raw_table_list = read_data(options.get("include", None), data, doc)
    # delete element if table is empty (by returning [])
    # element unchanged if include is invalid (by returning None)
    try:
        assert raw_table_list and raw_table_list is not None
    except AssertionError:
        logstring("pantable: table is empty or include is invalid", doc)
        # [] means delete the current element; None means kept as is
        return raw_table_list
    # regularize table: all rows should have same length
    table_list, number_of_columns = regularize_table_list(raw_table_list, doc)

    # Initialize the `options` output from `pf.yaml_filter`
    # parse width
    width = get_width(options, number_of_columns, doc)
    # auto-width when width is not specified
    if width is None:
        width = auto_width(
            get_table_width(options, doc), number_of_columns, table_list, doc
        )
    # delete element if table is empty (by returning [])
    # width remains None only when table is empty
    try:
        assert width is not None
    except AssertionError:
        logstring("pantable: table is empty", doc)
        return []
    # parse alignment
    alignment = parse_alignment(options.get("alignment", None), number_of_columns, doc)
    header = options.get("header", True)
    markdown = options.get("markdown", True)  # Boaz: change default to True

    # get caption: parsed as markdown into panflute AST if non-empty.
    caption_ = options.get("caption", "")
    caption = pf.convert_text(caption_)[0].content if caption_ else None
    # parse list to panflute table
    table_body = parse_table_list(markdown, table_list, doc)
    # extract header row
    header_row = table_body.pop(0) if (len(table_body) > 1 and header) else None
    T = pf.Table(
        *table_body,
        caption=caption,
        alignment=alignment,
        width=width,
        header=header_row,
    )
    id = options.get("identifier", options.get("id", ""))
    if not id:
        return T
    if doc.format == "latex":
        return [T, pf.Para(pf.RawInline(fr"\label{{{id}}}", format="latex"))]
    if doc.format == "html":
        return [pf.Para(pf.RawInline(fr'<a name="{id}"></a>', format="html")), T]
    return T


##################################################################


def h_paragraph(e, doc):
    """Make lines starting with bold become paragraphs."""
    if not isinstance(e, pf.Strong) or doc.format != "latex":
        return None
    if (
        isinstance(e.parent, pf.Para)
        and e.parent.parent == doc
        and e.parent.content.index(e) == 0
    ):
        return pf.RawInline(r"\paragraph{" + pf.stringify(e) + "}", format="latex")
    return None


def h_math(e, doc):
    r"""Make multiletter identifiers mathit{..}
    For now just handle uppercase identifiers.
    Also format better the empty string.

    For HTML we also change \label{blah} to (1.1)
    """
    if not isinstance(e, pf.Math):
        return None
    text = e.text
    reg = r"\\label\{([a-zA-Z\:\_\-0-9]+)\}"
    eqlabel = ""

    def _tmp(m):
        nonlocal eqlabel
        l = m.groups()[0]
        eqlabel = l
        if l in doc.labels:
            return fr"\;\;({doc.labels[l]['number']})"
        return ""

    if doc.format == "html":
        text = re.sub(reg, _tmp, text)
    reg = r"(?<=[^\\A-Z\{\:a-z\-])([A-Z][A-Z]+)"
    text = re.sub(reg, r"\\ensuremath{\\mathit{\1}}", text)
    reg2 = r"\A([A-Z][A-Z]+)"
    text = re.sub(reg2, r"\\ensuremath{\\mathit{\1}}", text)
    e.text = text.replace('""', r'\ensuremath{\text{\texttt{""}}}')
    if doc.format != "html":
        return e
    p = e.parent
    after = rf"<a id='{eqlabel}'></a>" if  eqlabel else ""
    before = ""
    if e.format == "DisplayMath":
        before += "\n"+r"<div class='myequationbox'>"
        after  += r"</div>" 
    before_ = pf.RawInline(before, format="html")
    after_ = pf.RawInline(after, format="html")
    return pf.Span(before_,e,after_)
    return e


def h_add_search(e, doc):
    """Add text to search index"""
    if isinstance(e, pf.Header):
        doc.searchtext += " " + pf.stringify(e)
        return None
    if isinstance(e, pf.Div):
        t = e.attributes.get("title", "")
        doc.searchtext += " " + t
    return None


def h_html_footnote(e, doc):
    """Handle footnotes with bigfoot"""
    if not isinstance(e, pf.Note) or doc.format != "html":
        return None
    htmlref = rf'<sup id="fnref:{doc.footnotecounter}"><a href="#fn:{doc.footnotecounter}" rel="footnote">{doc.footnotecounter}</a></sup>'
    htmlcontent_before = rf'<li class="footnote" id="fn:{doc.footnotecounter}"><p>'
    htmlcontent_after = rf'<a href="#fnref:{doc.footnotecounter}" title="return to article"> ↩</a><p></li>'
    doc.footnotecounter += 1
    conts = pf.Div(*e.content)
    doc.footnotecontents += (
        [pf.RawBlock(htmlcontent_before, format="html")]
        + [conts]
        + [pf.RawBlock(htmlcontent_after, format="html")]
    )
    return pf.RawInline(htmlref, format="html")


def h_latex_cite(e, doc):
    """Handle cite. Just feed it to a cite command and hope for the best. This is pretty hacky and should be changed."""

    if not isinstance(e, pf.Cite):
        return None
    logstring(f"I am {e} and my parent is {e.parent}", doc)
    if isinstance(e.parent, pf.Citation):
        return []
    s = pf.stringify(e).replace("[", "").replace("]", "").replace("@", "").strip()
    if s[-1] == ",":
        s = s[:-1]
    if doc.format == "latex":
        tex = f"\\cite{{{s}}}"
        return pf.RawInline(tex, format="latex")
    if doc.format == "html":
        html = ""
        for a in s.split(","):
            a = a.strip()
            if a in doc.bibentries:
                D = doc.bibentries[a]
                authors, title, year = D["author"], D["title"], D["year"]
                authors = bibtexparser.customization.getnames(
                    [i.strip() for i in authors.replace("\n", " ").split(" and ")]
                )
                author = ", ".join([a.split(",")[0] for a in authors])
                T_encode = latex_accents.LaTexAccents_to_UTF8()
                author = T_encode.decode_Tex_Accents(author)
                title = T_encode.decode_Tex_Accents(title)
                q = f"{author} {title}".replace(" ", "+")

                html += rf' (<a href="https://scholar.google.com/scholar?hl=en&q={q}" target="_blank">{author}, {year}</a>) '
        if not html:
            html = s
        return pf.RawInline(html, format="html")


def h_block_header(e, doc):
    """Change block starting with header to a Div"""
    if not isinstance(e, pf.BlockQuote):
        return None
    if not isinstance(e.content[0], pf.Header) or not e.content[0].classes:
        return None
    h = e.content[0]
    f = pf.Div(
        *e.content[1:],
        identifier=h.identifier,
        classes=h.classes,
        attributes=h.attributes,
    )
    e = action(f, doc)
    return e if e else f


def h_link_ref(e, doc):
    """Change links of class .ref to latex labels"""
    if not isinstance(e, pf.Link):
        return None
    if not e.classes:
        return None
    label = "".join(pf.stringify(a) for a in e.content)
    if label[0] == "#":
        label = label[1:]
    if not label:
        label = "???"
    if doc.format == "latex":
        if "ref" in e.classes:
            return pf.RawInline(f"\\cref{{{label}}}", format="latex")
        elif "eqref" in e.classes:
            return pf.RawInline(f"\\eqref{{{label}}}", format="latex")
        else:
            e.url = e.url.replace("_", "%5F")
            return e
    if doc.format == "html":
        name, link = getlabel(label, doc)
        if "ref" in e.classes or "eqref" in e.classes:
            return pf.RawInline(fr"<a href='{link}'>{name}</a>", format="html")
    return e


def h_latex_headers(e, doc):
    """make headers correspond to names in latex_headers (chapter, section, subsection, etc.)"""
    if not isinstance(e, pf.Header):
        return None
    if isinstance(e.parent, pf.BlockQuote):
        return None

    label = labelref(e, doc)

    if label and e.level in doc.latex_headers:
        doc.label_descriptions[label] = doc.latex_headers[e.level].capitalize
    if doc.format != "latex":
        return None
    labeltext = f"\\label{{{label}}}" if label else ""
    h = e.level
    if not h in doc.latex_headers:
        raise Exception(f"Invalid header level {h} in {e}")
    header = "\\" + doc.latex_headers[h]
    return pf.Para(
        pf.RawInline(header + "{", format="latex"),
        *e.content,
        pf.RawInline("}" + labeltext, format="latex"),
    )


def h_latex_div(e, doc):
    r"""make every div with class=foo to begin{foo} ... end{foo}
    if there is title then it is begin{foo}[title] instead
    if there is an identifier then we add \label[foo]{id}"""
    if not isinstance(e, pf.Div):
        return None
    if not len(e.classes):
        return None

    c = e.classes[0]
    title = e.attributes.get("title", "")
    label = labelref(e, doc)
    if label in doc.labels:
        name = getlabel(label, doc)[0]
    else:
        name = c.capitalize()
    if title:
        name += f" ({title}) "
    e.attributes["name"] = name

    if e.identifier:
        doc.label_descriptions[e.identifier] = c.capitalize()
    if doc.format == "html" and c == "quote":
        return pf.BlockQuote(e)
    if doc.format != "latex":
        return None
    dref = e.attributes.get("data-ref", None)
    if not title and c == "proof" and dref and dref != doc.lastlabel:
        title = fr"Proof of \cref{{{dref}}}"
    label = labelref(e, doc)
    doc.lastlabel = label
    before = rf"\begin{{{c}}}[{title}]" if title else rf"\begin{{{c}}}"
    if label:
        before += rf" \label[{c}]{{{label}}}"
    if c == "algorithm":
        before += r"~ \\ \noindent" + "\n"
    after = rf"\end{{{c}}}"
    _before = pf.RawBlock(before, format="latex")
    _after = pf.RawBlock(after, format="latex")
    e.content = [_before] + list(e.content) + [_after]
    return e


def findparen(s, beg=0, op="(", cl=")"):
    beg = s.find(op, beg)
    if beg == -1:
        return beg, -1
    end = beg + 1
    level = 1
    while level and end < len(s):
        if s[end] == op:
            level += 1
        if s[end] == cl:
            level -= 1
        end += 1
    return beg, end - 1


def expand_commands(tex):
    """
    Expand out latex commands. Currently hardwired into few macros, eventually should
    get it from the configuration file.
    """
    with_args = {r"\floor": r"\lfloor #1 \rfloor"}
    no_args = {r"\N": r"\mathbb{N}", r"\Z": r"\mathbb{Z}"}
    for c, rep in with_args.items():
        c = c.replace("\\", "\\\\")
        rep = rep.replace("\\", "\\\\").replace("#1", r"\g<1>")
        tex = re.sub(c + r"\{([^\}]+)\}", rep, tex)
    for c, rep in no_args.items():
        c = c.replace("\\", "\\\\")
        rep = rep.replace("\\", "\\\\")
        tex = re.sub(rf"{c}(?!\w)", rep, tex)
    return tex


def format_pseudocode(code):
    keywords = [
        "PROCEDURE",
        "ENDPROCEDURE",
        "END\\\\PROCEDURE",
        "WHILE",
        "ENDWHILE",
        "END\\\\WHILE",
        "FOR",
        "ENDFOR",
        "END\\\\FOR",
        "INPUT",
        "OUTPUT",
        "ELSE",
        "ELSIF",
        "FUNCTION",
        "ENDFUNCTION",
        "END\\\\FUNCTION",
        "IF",
        "ENDIF",
        "END\\\\IF",
        "RETURN",
    ]

    for k in keywords:
        k_ = k.replace("\\", "")
        code = re.sub(fr"(?i)(?<![\w\\\-]){k}(?!\w)", fr"\\{k_}", code)
        code = re.sub(fr"(?i)(?<![\w\\])\-({k})(?!\w)", r"\g<1>", code)

    code = expand_commands(code)

    code = code.replace("\\INPUT:", "\\INPUT ").replace("\\OUTPUT:", "\\OUTPUT ")

    lines = code.split("\n")
    res = ""
    functions = []
    for l in lines:
        if not l:
            continue

        for f in functions:
            i = l.find(f+"(")
            if i > -1:
                beg, end = findparen(l, i + 1)
                if beg > -1:
                    # calling functions should always happen in math mode
                    suffix = l[end + 1 :].lstrip() if l[end + 1 :] else "$"
                    suffix = suffix[1:] if suffix[0] == "$" else " $" + suffix
                    prefix =  l[:i].rstrip()
                    if prefix and prefix[-1]=="$":
                        prefix = prefix[:-1]
                    else:
                        prefix += "$ "
                    l = (
                        prefix
                        + "\\CALL{"
                        + f
                        + "}{$"
                        + l[beg + 1 : end]
                        + "$} "
                        + suffix
                    )
        m = re.search(r"\S+", l)
        if m:
            i = m.start()
            if l[i] != "\\":
                l = l[:i] + "\\STATE " + l[i:]
        l = re.sub(r"`([^`]+)`", lambda m: fr"\texttt{{{latexescape(m.group(1))}}}", l)
        i = l.find("#")
        if i > 0:
            l = l[:i] + "\\COMMENT{" + l[i + 1 :] + "}"
        res += l + "\n"
        m = re.match(r"\\FUNCTION\{([^\}]+)\}.*", l)
        if m:
            functions.append(m.group(1))
        m = re.match(r"\\PROCEDURE\{([^\}]+)\}.*", l)
        if m:
            functions.append(m.group(1))
    return res


def h_pseudocode(e, doc):
    if not isinstance(e, pf.CodeBlock) or not "algorithm" in e.classes:
        return None
    content = e.text
    if e.identifier:
        doc.label_descriptions[e.identifier] = "Algorithm"
    label = labelref(e, doc)
    _, number_, _ = get_full_label(label, doc)
    if number_ and number_ != "??":
        i = number_.rfind(".")
        number = int(number_[i + 1 :]) if i > -1 else int(number_)
    else:
        number = 0
    title = e.attributes.get("title", "")
    if doc.format == "latex":
        textitle = f"[{title}]" if title else ""
        result = (
            dedent(
                rf"""
        \begin{{algorithm}}{textitle}
        \label[algorithm]{{{label}}} ~ \\ \noindent
        \begin{{algorithmic}}[1]
        """
            )
            + "\n"
            + format_pseudocode(content)
            + dedent(
                fr"""
        \end{{algorithmic}}
        \end{{algorithm}}
        """
            )
        )
        return pf.RawBlock(result, format="latex")
    if doc.format == "html":
        textitle = f"\caption{{{title}}}" if title else ""
        uid = str(uuid.uuid4())
        content = (
            format_pseudocode(content)
            .replace("\\INPUT", "\\REQUIRE")
            .replace("\\OUTPUT", "\\ENSURE")
        )
        result = (
            dedent(
                rf"""
            <pre id="{uid}" class="pseudocodetext" style="display:none;">
            \begin{{algorithm}}
            {textitle}
            \begin{{algorithmic}}
            """
            )
            + "\n"
            + content
            + dedent(
                fr"""
            \end{{algorithmic}}
            \end{{algorithm}}
            </pre>
            <div id="{uid}result" class="pseudocodeoutput" ></div>

            <script>
            document.addEventListener('readystatechange', event => {{
            if (event.target.readyState === "complete") {{
                var code = document.getElementById('{uid}').textContent;
                var resultEl = document.getElementById('{uid}result');
                resultEl.innerHTML = '';
                var options = {{
                    captionCount: {number-1},
                    lineNumber: true
                }};
                pseudocode.render(code, resultEl, options);
            }}
            }});
            </script>
            """
            )
        )
        return pf.RawBlock(result, format="html")
    return None

def h_html_code_block(e, doc):
    """HTML code block"""
    if not isinstance(e, pf.CodeBlock) or doc.format != "html":
        return None
    if "algorithm" in e.classes:
        return None
    if not "full" in e.classes:
        return None
    label = labelref(e, doc)
    name, number, file = get_full_label(label, doc)
    title = e.attributes.get("title", "")
    before = rf"<p><i>Figure {number}: {title}</i></p>"+"\n"
    after = r"<p></p>"
    return pf.Div(pf.RawBlock(before,format='html'),e,pf.RawBlock(after,format='html'))


def h_code_block(e, doc):
    """code blocks use code environment
    at the moment ignore the particular programming language"""
    if not isinstance(e, pf.CodeBlock) or doc.format != "latex":
        return None
    if "algorithm" in e.classes:
        return None
    before = "\\begin{code}\n"
    after = "\n\\end{code}\n"
    if "full" in e.classes:
        label = labelref(e, doc)
        labeltext = f"\n\\label{{{label}}}" if label else ""
        title = e.attributes.get("title", "")
        titletext = f"\n\\classiccaptionstyle\n\\caption{{{title}}}" if title else ""
        before = (
            "\\begin{figure*}\n"
            + titletext
            + labeltext
            + "\n\n"
            + r"\begin{framedcode}"
            + "\n"
        )
        after = "\n" + r"\end{framedcode}" + "\n" + r"\end{figure*}"
    return pf.RawBlock(before + e.text + after, format="latex")


def h_html_image(e, doc):
    """
    Add figure number for html images
    """
    if not isinstance(e, pf.Image) or doc.format != "html":
        return None
    if not e.identifier:
        return None
    name, number, file = get_full_label(e.identifier, doc)
    if number:
        e.content = pf.ListContainer(pf.Str(number + ": "), *e.content)
    return e


def h_latex_image(e, doc):
    """
    Handle images with automatic scaling.
    Image classes: (for tufte)
    full : full page  - figure*
    margin: margin figure - marginfigure
    """
    if not isinstance(e, pf.Para) or doc.format != "latex":
        return None
    if not len(e.content) == 1:
        return None
    if not isinstance(e.content[0], pf.Image):
        return None
    img = e.content[0]
    capoffset = ""
    figoffset = ""
    preamble = ""
    if "offset" in img.attributes:
        capoffset = f"[][{img.attributes['offset']}]"
    if "full" in img.classes:
        fig = "figure*"
        preamble = "\n" + r"\classiccaptionstyle"
        scale = "width=0.9\\paperwidth, height=0.3\\paperheight, keepaspectratio"
    elif "margin" in img.classes:
        fig = "marginfigure"
        figoffset = capoffset[2:] if capoffset else ""
        capoffset = ""
        scale = r"width=\linewidth, height=1.5in, keepaspectratio"
    else:
        fig = "figure"
        scale = "width=\\textwidth, height=0.25\\paperheight, keepaspectratio"
    before = f"\n\\begin{{{fig}}}{figoffset}\n{preamble}\\centering\n"
    label = img.identifier
    end = f"\n\\end{{{fig}}}\n"
    graphic = f"\\includegraphics[{scale}]{{{img.url}}}\n"
    if label:
        end = fr"\label{{{label}}}" + end
    _before = pf.RawInline(before + graphic + f"\\caption{capoffset}{{", format="latex")
    _after = pf.RawInline("}\n" + end, format="latex")
    return pf.Para(_before, *img.content, _after)


def latexescape(s):
    # & % $ # _ { } ~ ^ \
    # Outside \verb, the first seven of them can be typeset by prepending a backslash; for the other three, use the macros \textasciitilde, \textasciicircum, and \textbackslash.
    t = ""
    special = {
        "&": r"\&",
        "#": r"\#",
        "%": r"\%",
        "$": r"\$",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde",
        "^": r"\textasciicircum",
        "\\": r"\textbackslash",
    }

    for i in range(len(s)):
        c = s[i]
        if c in special:
            t += special[c]
        else:
            t += c
    return t


def h_code_inline_draft(e, doc):
    """inline code uses codeinline command"""
    if not isinstance(e, pf.Code) or doc.format != "latex":
        return None
    return pf.RawInline(f"\\texttt{{{latexescape(e.text)}}}", format="latex")


def h_code_inline(e, doc):
    """inline code uses codeinline command"""
    if not isinstance(e, pf.Code) or doc.format != "latex":
        return None
    return pf.RawInline(f"\\codeinline{{{e.text}}}", format="latex")


def action(e, doc):
    d = 0
    t = e
    while t.parent:
        t = t.parent
        d += 1
    log(d, e, doc)
    for h in doc.handlers:
        f = h(e, doc)
        if f is not None:
            return f

    return e
    # return None -> element unchanged
    # return [] -> delete element
    # Boaz: hopefully return e is also the same as not changing


def main(doc=None):
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
