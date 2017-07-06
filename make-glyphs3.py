import os
import sys
from collections import OrderedDict
import toml
import json

from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

#from generateIds import MathFont

if len(sys.argv) != 2:
    print("usage: make-glyphs.py font.otf")
    print("\nThis file will read font.otf, extract the relavent infomration "
          "needed to create a Glyph structure in rust.  This will save the file "
          "as out/font/glyphs.rs.  This file assumes the font has a rex- prefix.")
    sys.exit(1)

font_file  = sys.argv[1]
file_out = "out/" + os.path.splitext(os.path.basename(font_file))[0][4:] + "/glyphs2.rs"
font     = TTFont(font_file)
glyphset = font.getGlyphSet()

# This depends on the specific font
cmap = font['cmap'].tables[-1].cmap
cmap.update(font['cmap'].tables[3].cmap)

# This provides and ordered -> Unicode mapping with every other attribute initialized
glyphs = OrderedDict([ (name,
             { "unicode": code, "min_x": 0, "min_y": 0, "max_x": 0, "max_y": 0, 
               "attachment": 0, "italics": 0, "advance": 0, "lsb": 0 })
        for code, name in sorted(cmap.items()) ])

###
# Calculating the bounding box for each Glyph
#

pen = BoundsPen(None)
for name in glyphs:
    glyph = glyphset.get(name)
    glyph.draw(pen)
    if pen.bounds == None:
        continue

    (xm, ym, xM, yM) = pen.bounds
    glyphs[name]["min_x"] = int(xm)
    glyphs[name]["min_y"] = int(ym)
    glyphs[name]["max_x"] = int(xM)
    glyphs[name]["max_y"] = int(yM)

    # Clear pen bounds
    pen.bounds = None
    pen._start = None

math = font['MATH'].table

###
# Extract the accent offsets
#

accent_table    = math.MathGlyphInfo.MathTopAccentAttachment
accent_coverage = accent_table.TopAccentCoverage.glyphs
for name in accent_coverage:
    value = accent_table \
        .TopAccentAttachment[accent_coverage.index(name)] \
        .Value
    glyphs[name]["attachment"] = value

###
# Extract the italics offsets
#

italics_table    = math.MathGlyphInfo.MathItalicsCorrectionInfo
italics_coverage = italics_table.Coverage.glyphs
for name in italics_coverage:
    value = italics_table \
        .ItalicsCorrection[italics_coverage.index(name)] \
        .Value
    glyphs[name]["italics"] = value

###
# Extract the advance and left side bearing
#

metrics = font['hmtx'].metrics
for name in glyphs:
    glyphs[name]["advance"] = metrics[name][0]
    glyphs[name]["lsb"]     = metrics[name][1]

glyphs = sorted(list(glyphs.values()), key = lambda s: s['unicode'])
dump = json.dumps(glyphs, indent=4)

with open('test.rs', 'w') as f:
    f.write(dump)
