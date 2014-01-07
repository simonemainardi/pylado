import subprocess
from os import sep
from os.path import dirname

available_structures = ["chapter", "section", "subsection"]
available_summaries = ["tableofcontents", "listoffigures", "listoftables"]
available_commands = ["clearpage", "vfill", "null"]

available_sizes=["a4","a3"]

class texdocument(object):
    """
    This is a LaTeX document. You can attach structures,
    figures, images to this class in order to have a final
    latex document
    """
    def __init__(self, size="a4", pagenumbering=True, **docargs):
        if not size in available_sizes:
            raise Exception("Please specify a valid size for the paper")
        if not isinstance(pagenumbering, bool):
            raise Exception("Page numbering must be a bool")

        if not docargs.has_key("class"):
            docargs["class"] = "report"
        if not docargs.has_key("orientation"):
            docargs["orientation"] = "portrait"
        if not docargs.has_key("title"):
            docargs["title"] = "Unspecified Title"
        if not docargs.has_key("titlepage_info"):
            docargs["titlepage_info"] = ""
        if not docargs.has_key("headers_info"):
            docargs["headers_info"] = ""

        # escape possible LaTeX characters
        for k in docargs.keys():
            docargs[k] = docargs[k].replace("_","\_")

        # prepare the tex code for the logo image
        defaultpath = dirname(__file__)
        defaultpath = defaultpath + sep + "images" + sep + "dcns_logo.jpg"
        docargs["logo"] = "\\includegraphics[width=.5\\textwidth]{%s}~\\\\[1em]" % defaultpath
            
        # it is required to escape \t, \a, \b
        tex = '''\documentclass[%(orientation)s]{%(class)s}
''' % docargs
        if size == "a3":
            tex += "\usepackage[a3paper]{geometry}"
        if pagenumbering == False:
            tex += "\pagenumbering{gobble}"
	tex += '''\usepackage{graphicx}
\usepackage[utf8]{inputenc}
\usepackage{epstopdf}
\usepackage{float}
\usepackage[top=1.5in, bottom=1.5in, left=.5in, right=.5in]{geometry}
%%\usepackage[cm]{fullpage}
\usepackage{hyperref} %% to make links in the table of contents
\\hypersetup{
    colorlinks=false, %%set false if you do not want colored links
}

\usepackage{longtable}
\usepackage{rotating}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[table]{xcolor}%% http://ctan.org/pkg/xcolor
\usepackage{multirow}

%% this hack is necessary to obtain cells with text that wraps around,
%% is raggedright (e.g. R{1cm}), centered (e.g. C{1cm}) or raggedleft (e.g. L{1cm})
%% and allows \\newline manual line breaks
%% see here http://tex.stackexchange.com/questions/12703/how-to-create-fixed-width-table-columns-with-text-raggedright-centered-raggedlef
\\usepackage{array}
\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}
\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}
\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}

%% this is for the footers on each page
\\usepackage{lastpage} %% keep track of the last page number
\\usepackage{fancyhdr}
\\pagestyle{fancy}
\\fancyhead{}
\\fancyfoot{}
\\fancyhead[L]{\\nouppercase{\\leftmark}}
\\fancyhead[R]{%(headers_info)s}
\\fancyfoot[R]{Page \\thepage/\\pageref{LastPage}}%%
%%\\fancyfoot[R] {Page \\thepage/\\pageref{LastPage}}
%%\\fancyfoot[C]{DCNS}
%%\\fancyfoot[RO, LE] {\\thepage of \\pageref{LastPage}}
%%\\fancyfoot[RO, RE] {\\thepage}

%% redefine also the fancy plain style to print
%% page numbers also in special pages such as the table
%% of contents
\\fancypagestyle{plain}{%%
  \\fancyhf{}%%
%%  \\renewcommand{\headrulewidth}{0pt}%%
  \\fancyhead[R]{%(headers_info)s}%%
  \\fancyfoot[R]{Page \\thepage/\\pageref{LastPage}}%%
}

\setcounter{tocdepth}{1}

%% Remove Chapter number at the beginning of each chapter
%% but maintain toc consistency
\\makeatletter
\\def\\@makechapterhead#1{%%
  \\vspace*{50\\p@}%%
  {\\parindent \\z@ \\raggedright \\normalfont
   \\interlinepenalty\\@M
   \\Huge \\bfseries #1\\par\\nobreak
   \\vskip 40\\p@
  }}
\\makeatother

\\begin{document}

\\begin{titlepage}
\\vspace*{\\fill}
\\begin{center}

%(logo)s
{\huge {%(title)s}}\\\\[0.5cm]
%%{\large {%%(author)s}}\\\\[0.4cm]
\\today
\\vspace*{\\fill}
\\end{center}
%(titlepage_info)s
\\end{titlepage}

''' % docargs
        self._tex = tex

    def append(self, tex):
        self._tex += tex

    def get_tex(self):
        return self._tex

    def write_tex(self, output):
        """
        Write current LaTeX document to file output.
        Returns the name and the path of the generated file
        """
        if not isinstance(output, basestring):
            raise Exception("Specify a valid file name")

        # finalize the document
        self._tex += "\end{document}\n"

        # if the file does not end with ".tex"
        # we add this extension since we like it :)
        if not output.endswith(".tex"):
            output += ".tex"

        file(output, "w").write(self._tex)
        return output

    def generate_pdf(self, output):
        if not isinstance(output, basestring):
            raise Exception("Specify a valid file name")

        # if output ends with ".pdf"
        # we remove the extension since it is automatically
        # added by the compiler
        if output.endswith(".pdf"):
            output = output[:-4]

        
        # write the tex file removing the extension
        texfile = self.write_tex(output)

        params = "--shell-escape --synctex=1 "
        params += "-interaction=nonstopmode -output-directory=%s " % dirname(texfile)
        params += texfile
        # now call pdflatex TWICE
        # otherwise
        # references and labels numbering will not
        # be displayes
        for i in xrange(2):
            subprocess.check_call("pdflatex " + params, shell=True)


class structure(object):
    """
    Generate LaTeX-compliant commands to structure
    the document. For example you can ask for the code
    for a section, a subsection, a paragraph and so on
    and so forth.
    """
    def __init__(self):
        # dynamically attach some methods generating
        # latex code for given structure names

        # dynamic methods for structues such as sections and subsections...
        for struct in available_structures:
            def texify(self, structname, structcontents, numbered=False, struct=struct):
                texcode = "\\" + struct + "*{" + structname + "}\n"
                if not numbered:
                    texcode = texcode.replace("*", "")
                texcode += structcontents + "\n"
                return texcode
            texify.__doc__ = '''
                Generate tex code for a LaTeX %s.
                The %s will be named structname and will contain contents specified in 
                structcontents. You may also specify whether you need a numbered
                %s, but you should not override the last parameter to avoid unwanted
                funection behaviour.

                The output will be, if numbered=False:
                \%s{structname}
                structcontents

                Else, if numbered=True:
                \%s*{structname}
                structcontents
                ''' % tuple([struct] * 5)
            texify.__name__ = struct
            # attach an attribute named struct pointing to the
            # function texify with the right default parameters
            setattr(self.__class__, struct, texify)

        # dynamic  methods for summaries such as the table of contents
        for summ in available_summaries:
            def texify(self, summ=summ):
                tex = "\\" + summ + "\n"
                tex = tex.replace("\t","\\t")
                return tex
            texify.__doc__ = '''
                Generate tex code for a LaTeX %s.

                The output will be, if numbered=False:
                \%s
                ''' % tuple([summ] * 2)
            texify.__name__ = summ
            # dynamically attach texify method to the class
            setattr(self.__class__, summ, texify)

        # dynamic methods for other LaTeX commands
        for comm in available_commands:
            def texify(self, comm=comm):
                tex = "\\" + comm + "\n"
                return tex
            texify.__doc__ = '''
                Generate tex code for a LaTeX %s.

                The output will be
                \%s
                ''' % tuple([comm] * 2)
            texify.__name__ = comm
            # dynamically attach texify method to the class
            setattr(self.__class__, comm, texify)

    def abstract(self, contents=""):
        return "\\begin{abstract}\n%s\n\end{abstract}\n" % contents

    def image(self, imgfile, caption=None, includegraphicsopts="", placement_specifier="H"):
        """
        Generate LaTeX code for an image. The image
        included in the code
        """
        # check if the file exists and can be opened
        # otherwise raise an exception
        file(imgfile, "r")

        # check if the placement_specifier is valid
        if not placement_specifier in ["H","h","t"]:
            raise Exception("Please specify a valid placement specifier")

        tex = "\\begin{figure}[%s]\n\centering\n" % placement_specifier

        # include the graphics file and possibly its options
        tex += "\includegraphics[%s]{%s}\n" % (includegraphicsopts, imgfile)
        
        # determine if we have to add a caption
        if caption and isinstance(caption, basestring):
            tex += "\caption{%s}\n" % caption

        tex += "\end{figure}"
        return tex

    def table(self, justs, rows, headers=False, caption=None, size=""):
        """
        Produce LaTeX code for tables.
        justs: specify the alignment of the columns
        headers: specify column headers
        rows: is a list of lists containing values for each row
        caption: the name of the table
        """
        if not isinstance(justs, basestring):
            raise Exception("justs must speficy alignment characters")
        if not isinstance(headers, bool):
            raise Exception("headers must be a a boolean")
        if not isinstance(rows, list):
            raise Exception("rows must be a list")
        for r in rows:
            if not isinstance(r, list):
                raise Exception("rows must be a list of lists")

        if caption and not isinstance(caption, basestring):
            raise Exception("caption must be a valid string")

        if not size in ["", "scriptsize", "tiny", "large"]:
            raise Exception("size must be a valid specifier")

        # determine the number of columns the current table has
        # by taking the maximum of the lenght of all the lists passed in rows
        nb_cols = 0
        for row in rows:
            if len(row) > nb_cols:
                nb_cols = len(row)

        tex = "\\begin{center}\n"

        if size:
            tex += "\\begin{%s}\n" % size

        # and now begin with table contents
        tex += "\\begin{longtable}{%s}\n" % justs

        # possibly add a caption
        if caption:
            tex += "\\caption{%s}\\\\\n" % caption

        tex += "\hline\n" # an horizontal line

        # add headers and use a bold font if LaTeX math environment
        # is not present
        if headers:
            for h in rows[0]:
                if '$' in h:
                    tex += "%s & " % str(h)
                else:
                    tex += "\\textbf{%s} & " % str(h)
            # remove the last & and add a \\ and an hline
            tex = tex[:-2] + "\\endhead\n\hline\n"
            rows = rows[1:]

        for row in rows:
            # write out each row separating columns with the &
            # if row is an empty list, then we simply add an hline and continue
            if row == []:
                tex += "\\multicolumn{%i}{c}{}" % nb_cols
                tex += "\\\\[-1em] \\hline \n"
                continue
            for el in row:
                # if el is a float, we round it to the 2nd
                # decimal digit
                if type(el) == float:
                    el = "%.2f" % el
                # if el is a tuple, then we have to create a multicolumn
                if type(el) == tuple:
                    el = "\\multicolumn{%i}{c|}{%s}" % (el[0],el[1])
                tex += "%s & " % str(el)
            # remove the last & and add a \\ and an horizontal line
            tex = tex[:-2] + "\\\\\n\hline\n"
        tex += "\end{longtable}\n"

        if size:
            tex += "\\end{%s}\n" % size

        # close the center
        tex += "\end{center}\n"

        print tex
        return tex




structure = structure()

