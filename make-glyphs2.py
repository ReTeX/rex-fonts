import os
import sys
from collections import OrderedDict
import toml

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

cmap = {}
for c in font['cmap'].tables:
    cmap.update(c.cmap)

# This provides and ordered -> Unicode mapping with every other attribute initialized
glyphs = OrderedDict([ (name,
             { "unicode": code, "xm": 0, "ym": 0, "xM": 0, "yM": 0, 
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
    glyphs[name]["xm"] = int(xm)
    glyphs[name]["ym"] = int(ym)
    glyphs[name]["xM"] = int(xM)
    glyphs[name]["yM"] = int(yM)

    # Clear pen bounds
    pen.bounds = None
    pen._start = None

math = font['MATH'].table

###
# Calculate the accent offsets
#

accent_table    = math.MathGlyphInfo.MathTopAccentAttachment
accent_coverage = accent_table.TopAccentCoverage.glyphs
for name in accent_coverage:
    value = accent_table \
        .TopAccentAttachment[accent_coverage.index(name)] \
        .Value
    glyphs[name]["attachment"] = value

###
# Calculate the italics offsets
#

italics_table    = math.MathGlyphInfo.MathItalicsCorrectionInfo
italics_coverage = italics_table.Coverage.glyphs
for name in italics_coverage:
    value = italics_table \
        .ItalicsCorrection[italics_coverage.index(name)] \
        .Value
    glyphs[name]["italics"] = value

###
# Calculate the advance and left side bearing
#

metrics = font['hmtx'].metrics
for name in glyphs:
    glyphs[name]["advance"] = metrics[name][0]
    glyphs[name]["lsb"]     = metrics[name][1]

###
# Build rust objects from the collected metrics
#

header = """
// Automatically generated... blah blah blah, you know the deal.
use fnv::FnvHashMap;
use font::{ Glyph, BBox };

static GLYPHS_DATA: [Glyph; 1] = [
"""

TEMPLATE = "    Glyph {{ unicode: {unicode}, "\
           "bbox: BBox({xm},{ym},{xM},{yM}), " \
           "advance: {advance}, lsb: {lsb}, "\
           "italics: {italics}, attachment: {attachment} }},\n"

REPLACE_TEMPLATE = "    Glyph {{ unicode: {new}, "\
           "bbox: BBox({xm},{ym},{xM},{yM}), " \
           "advance: {advance}, lsb: {lsb}, "\
           "italics: {italics}, attachment: {attachment} }},\n"

hashmap = []
array   = [ TEMPLATE.format(**glyphs[cmap[code]]) for code in cmap.keys() ]
size    = len(array)

header += "    // Replacement UNICODE values from unicode.toml exceptions\n"
    
# Handle exceptions from unicode.toml
t = toml.load('unicode.toml')
for family in t.values():
    if family.get('exceptions', None):
        for old, new in family['exceptions'].items():
            z = glyphs[cmap[int(new,0)]].copy()
            z['old'] = int(old, 0)
            z['new'] = int(new, 0)
            array.append(REPLACE_TEMPLATE.format(**z))
            hashmap.append(old)
            
header += "".join(array)
header += "];\n\n"
header += """
lazy_static! {
    pub static ref GLYPHS: FnvHashMap<u32, &'static Glyph> = {
        let mut h = FnvHashMap::default();
        
        for (idx, glyph) in GLYPHS_DATA.iter().enumerate() {
            h.insert(glyph.unicode, &GLYPHS_DATA[idx])
        }

"""

for (idx, code) in enumerate(hashmap):
    header += "        h.insert({}, &GLYPHS_DATA[{}]);\n".format(code, idx + size)

header += """
        h
    };
}"""

#print(header)
with open(file_out, 'w') as f:
    f.write(header)
