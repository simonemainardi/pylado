import os,sys
import random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from texifier import structure as s
from document import document

if not os.path.exists("output"):
    os.makedirs("output")

# instantiate a new document, specifying its title and the name
# of the author
d = document(author="Simone Mainardi", title="Yet Another \LaTeX{} report")

# generate some random content
randomcontent = ''.join(random.choice(' asd.,') for i in xrange(1000))

# create a section named "One section" containing the previously
# generated random content
d.append(s.section("One section", randomcontent))

# create another section
d.append(s.section("Another Section", randomcontent))

# write the pdf file
d.generate_pdf("output/simple_report.pdf")
