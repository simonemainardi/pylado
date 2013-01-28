from copy import deepcopy

available_structures = ["section", "subsection"]
available_summaries = ["tableofcontents", "listoffigures", "listoftables"]

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
                texcode += structcontents
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

    def abstract(self, contents=""):
        return "\\begin{abstract}\n%s\n\end{abstract}\n" % contents

    def image(self, imgfile, caption=None, includegraphicsopts=""):
        """
        Generate LaTeX code for an image. The image
        included in the code
        """
        # check if the file exists and can be opened
        # otherwise raise an exception
        file(imgfile, "r")
        tex = "\\begin{figure}[t]\n\centering\n"

        # include the graphics file and possibly its options
        tex += "\includegraphics[%s]{%s}\n" % (includegraphicsopts, imgfile)
        
        # determine if we have to add a caption
        if caption and isinstance(caption, basestring):
            tex += "\caption{%s}\n" % caption

        tex += "\end{figure}"
        return tex

structure = structure()
