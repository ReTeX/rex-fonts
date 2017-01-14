import os
import sys
from collections import OrderedDict
import toml

from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

#from generateIds import MathFont

if len(sys.argv) != 2:
    print("usage: make-unicodes.py font.otf\n")
    print("This program will construct a list of all the unicode "
          "values in the given font.  This can be used for benchmarking")
    sys.exit(1)

font_file  = sys.argv[1]
file_out = "out/" + os.path.splitext(os.path.basename(font_file))[0][4:] + "/unicodes.rs"
font     = TTFont(font_file)

cmap = {}
for c in font['cmap'].tables:
    cmap.update(c.cmap)

header = """
// Automatically generated... blah blah blah, you know the deal.

#[allow(dead_code)]
pub static unicodes: [u32: 1] = [
"""


for (idx, code) in enumerate(sorted(cmap.keys())):
    if idx % 10 == 0:
        header += "\n    "
    header += hex(idx) + ", "

header += "];\n"
with open(file_out, 'w') as f:
    f.write(header)
