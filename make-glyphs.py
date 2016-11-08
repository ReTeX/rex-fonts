import os
import sys
from collections import OrderedDict

from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

from generateIds import MathFont

if len(sys.argv) != 2:
    print("usage: make-glyphs.py font.otf")
    print("\nThis file will read font.otf, extract the relavent infomration "
          "needed to create a Glyph structure in rust.  This will save the file "
          "as out/font/glyphs.rs.  This file assumes the font has a rex- prefix.")
    sys.exit(1)

font_file  = sys.argv[1]
file_out = "out/" + os.path.splitext(os.path.basename(font_file))[0][4:] + "/glyphs.rs"
font     = TTFont(font_file)
glyphset = font.getGlyphSet()

mf = MathFont(font_file, "unicode.toml")

# This provides and ordered -> Unicode mapping with every other attribute initialized
glyphs = OrderedDict([ (code, 
             { "unicode": code, "xm": 0, "ym": 0, "xM": 0, "yM": 0, 
               "attachment": 0, "italics": 0, "advance": 0, "lsb": 0 })
        for code in mf.gid.keys() ])

###
# Calculating the bounding box for each Glyph
#

pen = BoundsPen(None)
for code, name in mf.name.items():
    if name not in glyphset.keys():
        print(name, 'not in glyphs')
        continue
    glyph = glyphset.get(name)
    glyph.draw(pen)
    if pen.bounds == None:
        continue

    (xm, ym, xM, yM) = pen.bounds
    glyphs[code]["xm"] = int(xm)
    glyphs[code]["ym"] = int(ym)
    glyphs[code]["xM"] = int(xM)
    glyphs[code]["yM"] = int(yM)
    
    # Clear pen bounds
    pen.bounds = None
    pen._start = None

math = font['MATH'].table

###
# Calculate the accent offsets
#

accent_table    = math.MathGlyphInfo.MathTopAccentAttachment
accent_coverage = accent_table.TopAccentCoverage.glyphs
for code, name in mf.name.items():
    if name in accent_coverage:
        value = accent_table \
            .TopAccentAttachment[accent_coverage.index(name)] \
            .Value
        glyphs[code]["attachment"] = value
    
###
# Calculate the italics offsets
#

italics_table    = math.MathGlyphInfo.MathItalicsCorrectionInfo
italics_coverage = italics_table.Coverage.glyphs
for code, name in mf.name.items():
    if name in italics_coverage:
        value = italics_table \
            .ItalicsCorrection[italics_coverage.index(name)] \
            .Value
        glyphs[code]["italics"] = value

###
# Calculate the advance and left side bearing
#

metrics = font['hmtx'].metrics
for code, name in mf.name.items():
    if name in metrics:
        glyphs[code]["advance"] = metrics[name][0]
        glyphs[code]["lsb"]     = metrics[name][1]

###
# Build rust objects from the collected metrics
#

header = """
// Automatically generated... blah blah blah, you know the deal.
use font::{{ Glyph, BBox }};

#[allow(dead_code)]
pub static GLYPHS: [Glyph; {}] = [
""".format(len(glyphs))

TEMPLATE = "  Glyph {{ unicode: {unicode}, bbox: BBox({xm},{ym},{xM},{yM}), " \
           "advance: {advance}, lsb: {lsb}, italics: {italics}, attachment: {attachment} }},\n"

for values in glyphs.values():
    header += TEMPLATE.format(**values)

header += "];\n"
with open(file_out, 'w') as f:
    f.write(header)

