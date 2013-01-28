from copy import deepcopy

available_structures = ["section", "subsection"]

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
        for struct in available_structures:
            def texify(self, structname, structcontents, numbered=False, struct=struct):
                texcode = "\\" + struct + "*{" + structname + "}\n"
                if not numbered:
                    texcode = texcode.replace("*", "")
                texcode += structcontents
                return texcode
            texify.__doc__ = """ Generate tex code for a LaTeX %s.
                The %s will be named structname and will contain contents specified in 
                structcontents. You may also specify whether you need a numbered
                %s, but you should not override the last parameter to avoid unwanted
                function behaviour.
                """ % (struct, struct, struct)
            texify.__name__ = struct
            # attach an attribute named struct pointing to the
            # function texify with the right default parameters
            setattr(self.__class__, struct, texify)

structure = structure()
