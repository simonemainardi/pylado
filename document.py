import subprocess
from os.path import dirname

class document:
    def __init__(self, **docargs):
        if not docargs.has_key("class"):
            docargs["class"] = "article"
        if not docargs.has_key("title"):
            docargs["title"] = "Unspecified Title"
        if not docargs.has_key("author"):
            docargs["author"] = "Unspecified Author"
            
        # it is required to escape \t, \a, \b
        tex = '''\documentclass{%(class)s}
\usepackage{graphicx}
\\title{%(title)s}
\\author{%(author)s}
\date{\\today}
\\begin{document}
\maketitle
''' % docargs
        self._tex = tex

    def append(self, tex):
        self._tex += tex

    def get_tex(self):
        return self._tex

    def write_tex(self, output):
        if not isinstance(output, basestring):
            raise Exception("Specify a valid file name")

        # finalize the document
        self._tex += "\end{document}\n"

        # if the file does not end with ".tex"
        # we add this extension since we like it :)
        if not output.endswith(".tex"):
            output += ".tex"

        # write out the file
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

        params = "-interaction=nonstopmode -output-directory=%s " % dirname(texfile)
        params += texfile
        # now with a subprocess call pdflatex
        subprocess.check_call("pdflatex " + params, shell=True)

