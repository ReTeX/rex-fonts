from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import sys
from collections import OrderedDict

if len(sys.argv) != 3:
    print("usage: glyph_metrics.py font.otf metrics.rs")
    sys.exit(1)

# This snippet will list all glyphs that are not reachable from the cmap
font_file  = sys.argv[1]
rust_file  = sys.argv[2]

font     = TTFont(font_file)
glyphset = font.getGlyphSet()
cmaps    = font['cmap'].tables

# Find all unique GlyphNames that is reachable from a cmap
codes = []
for cmap in cmaps:
    for key, value in cmap.cmap.items():
        if value not in codes:
            codes.append((key, value))

# This list contains each mapped unicode character
codes = sorted(codes)
code_lookup = {}

for key, value in codes:
    code_lookup[value] = key

glyphs = OrderedDict()
for idx, (code, name) in enumerate(codes):
    glyphs[code] = { "name": name, "id": idx }

# Calculate the BoundingBox for each Glyph
pen = BoundsPen(None)
to_delete = []
for code in glyphs:
    glyph = glyphset.get(glyphs[code]["name"])
    glyph.draw(pen)
    if pen.bounds == None:
        print("Unable to get bounds for 0x{:X} ({}).  Deleting from glyphs."
              .format(code, glyphs[code]["name"]))
        to_delete.append(code)
        continue
 
    (xm, ym, xM, yM) = pen.bounds
    glyphs[code]["xm"] = int(xm)
    glyphs[code]["ym"] = int(ym)
    glyphs[code]["xM"] = int(xM)
    glyphs[code]["yM"] = int(yM)
    
    # Clear pen bounds
    pen.bounds = None
    pen._start = None

# for code in to_delete: glyphs.pop(code, None)    

# Get the accent offset for each Glyph
math            = font['MATH'].table
accent_table    = math.MathGlyphInfo.MathTopAccentAttachment
accent_coverage = accent_table.TopAccentCoverage.glyphs
for idx, glyph in enumerate(accent_coverage):
    value = accent_table.TopAccentAttachment[idx].Value
    glyphs[code_lookup[glyph]]["attachment"] = value

italics_table    = math.MathGlyphInfo.MathItalicsCorrectionInfo
italics_coverage = italics_table.Coverage.glyphs
for idx, glyph in enumerate(italics_coverage):
    value = italics_table.ItalicsCorrection[idx].Value
    glyphs[code_lookup[glyph]]["italics_correction"] = value

# TODO: Get the advacnce/lsb from the glyphs found in extended etc..
hor_metrics = font['hmtx'].metrics
for key, value in hor_metrics.items():
    advance = value[0]
    lsb     = value[1]
    glyphs[code_lookup[key]]["advance"] = advance
    glyphs[code_lookup[key]]["lsb"]     = lsb
    

# Render rust code
header = """
// Automatically generated... blah blah blah, you know the deal.

static glyph_metrics = [
"""

template = "  Glyph {{ unicode: {}, bbox: BBox({},{},{},{}), advance: {}, lsb: {}, italics: {}, attachment: {} }},\n"

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

header += "]\n"

with open(rust_file, 'w') as f:
    f.write(header)
