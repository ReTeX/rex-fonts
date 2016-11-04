from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

import os
import sys
from collections import OrderedDict

if len(sys.argv) != 2:
    print("usage: make-glyphs.py font.otf")
    print("\nThis file will read font.otf, extract the relavent infomration " +
          "needed to create a Glyph structure in rust.  This will save the file "
          "as out/font/glyphs.rs.  This file assumes the font has a rex- prefix.")
    sys.exit(1)

###
# Obtain UNICODE -> { Name, GeneratedID } map
#

font_file  = sys.argv[1]
file_out = "out/" + os.path.splitext(os.path.basename(font_file))[0][4:] + "/glyphs.rs"

font     = TTFont(font_file)
glyphset = font.getGlyphSet()
cmaps    = font['cmap'].tables

# Find all unique GlyphNames that is reachable from a cmap
codes = []
for cmap in cmaps:
    for code, name in cmap.cmap.items():
        if code not in codes:
            codes.append((code, name))

# This provides Name -> Unicode mapping
codes = sorted(codes)
code_lookup = {}
for code, name in codes:
    code_lookup[name] = code

# This provides the UNICODE -> { Name, GeneratedID } map.
glyphs = OrderedDict()
for idx, (code, name) in enumerate(codes):
    glyphs[code] = { "name": name, "id": idx }

###
# Calculating the bounding box for each Glyph
#

pen = BoundsPen(None)
for code, _ in codes:
    glyph = glyphset.get(glyphs[code]["name"])
    glyph.draw(pen)
    if pen.bounds == None:
        #print("Unable to get bounds for 0x{:X} ({}).  Deleting from glyphs."
        #      .format(code, glyphs[code]["name"]))
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
for idx, glyph in enumerate(accent_coverage):
    value = accent_table.TopAccentAttachment[idx].Value
    glyphs[code_lookup[glyph]]["attachment"] = value
    
###
# Calculate the italics offsets
#

italics_table    = math.MathGlyphInfo.MathItalicsCorrectionInfo
italics_coverage = italics_table.Coverage.glyphs
for idx, glyph in enumerate(italics_coverage):
    value = italics_table.ItalicsCorrection[idx].Value
    glyphs[code_lookup[glyph]]["italics_correction"] = value

###
# Calculate the advance and left side bearing
#

# TODO: Get the advacnce/lsb from the glyphs found in extended etc..
for name, values in font['hmtx'].metrics.items():
    advance = values[0]
    lsb     = values[1]
    glyphs[code_lookup[key]]["advance"] = advance
    glyphs[code_lookup[key]]["lsb"]     = lsb

###
# Build rust objects from the collected metrics
#

header = """
// Automatically generated... blah blah blah, you know the deal.
use font::{{ Glyph, BBox }};

#[allow(dead_code)]
pub static GLYPHS: [Glyph; {}] = [
""".format(len(glyphs))

template = "  Glyph {{ unicode: {}, bbox: BBox({},{},{},{}), advance: {}, lsb: {}, italics: {}, attachment: {} }},\n"

print(glyphs)
for code in glyphs:
    xm = glyphs[code].get("xm", 0)
    ym = glyphs[code].get("ym", 0)
    xM = glyphs[code].get("xM", 0)
    yM = glyphs[code].get("yM", 0)
    attachment = glyphs[code].get("attachment", 0)
    italics = glyphs[code].get("italics_correction", 0)
    advance = glyphs[code].get("advance", 0)
    lsb = glyphs[code].get("lsb", 0)
    
    header += template.format(
        code, xm, ym, xM, yM, advance, lsb, italics, attachment)

header += "];\n"
with open(file_out, 'w') as f:
    f.write(header)
