class structure(object):
    """
    Generate LaTeX-compliant commands to structure
    the document. For example you can ask for the code
    for a section, a subsection, a paragraph and so on
    and so forth.
    """
    @staticmethod
    def section(name="noname", contents="empty", numbered=True):
        """
        The LaTeX \section command.
        You should specify the name of the section and
        its contents as parameters. In addition you can
        choose wheter to make a numbered section or not.
        """
        texcode = "\section*{" + name + "}\n"
        if numbered:
            texcode = texcode.replace("*","")
        texcode += contents
        return texcode + "\n"

    @staticmethod
    def subsection(name="noname", contents="empty", numbered=True):
        """
        The LaTeX \subsection command.
        You should specify the name of the subsection you
        are going to create and its contents. You may also
        choose to make a numbered section or not.
        """
        texcode = "\subsection*{" + name + "}\n"
        if numbered:
            texcode = texcode.replace("*","")
        texcode += contents
        return texcode + "\n"
