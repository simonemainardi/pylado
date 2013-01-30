import os,sys
import random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from texifier import structure as s
from texifier import texdocument

if not os.path.exists("output"):
    os.makedirs("output")

# instantiate a new document, specifying its title and the name
# of the author
d = texdocument(author="Simone Mainardi", title="Yet Another \LaTeX{} not-so-simple Report")

# generate some random content
randomcontent = ''.join(random.choice(' asd.,') for i in xrange(1000))

# create an abstract
d.append(s.abstract(randomcontent))

# add the table of contents
d.append(s.tableofcontents())

# add the table of figures
d.append(s.listoffigures())

# create five sections, each one with and image and three subsections
for sec in xrange(5):
    # add the section ...
    d.append(s.section("Senseless Section %i" % (sec + 1), randomcontent))

    # ... the image
    d.append(s.image("images/a_graph.eps",
                     "This is the senseless graph of Section %i" % (sec+1),
                     "width=.96\\textwidth"))

    # and the subsections
    for sub in xrange(3):
        d.append(s.subsection("Senseless Subsection %i" % (sub+1), randomcontent))

# write the pdf file
# be careful that sometimes pdflatex requires to compile twice
# prior to show up references and table of contents
for i in xrange(2):
    d.generate_pdf("output/less_simple_report.pdf")
