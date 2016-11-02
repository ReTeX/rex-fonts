from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import sys

if len(sys.argv) != 3:
    print("usage:   generate_glyph_map.py <FONT> <OUTPUT SVG>")
    print("example: make_metrics.py font.otf font-table.svg\n")
    print("This script will create a single svg with all the symbols with"
          " their corresponding bounding boxes, and advance widths")
    sys.exit(1)

in_font  = sys.argv[1]
out_font = sys.argv[2]
font = TTFont(in_font)
glyphset = font.getGlyphSet()

# Find all unique glyphs by unicode
cmaps  = font['cmap'].tables
glyphs = {}
for cmap in cmaps:
    for key, value in cmap.cmap.items():
        if key not in glyphs:
            glyphs[key] = value

header="""\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="80ex" height="500ex" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @font-face {
        font-family: rex;
        src: url('dist/rex-xits.otf');
      }
    </style>
  </defs>
  <g font-family="rex">
"""

rect_template  = '<rect x="{}ex" y="{}ex" width="{}ex" height="{}ex" fill="none" stroke="blue" stroke-width="0.2px"/>\n'
glyph_template = '<text x="{}ex" y="{}ex">{}</text>\n'    

# Get the bounding box
bbox_pen = BoundsPen(None)
def get_bbox(glyph):
    glyph.draw(bbox_pen)
    if bbox_pen.bounds == None:
        return None
    (xmin, ymin, xmax, ymax) = bbox_pen.bounds
    bbox_pen.bounds = None
    bbox_pen._start = None
    return (xmin/450, ymin/450, xmax/450, ymax/450)

# Draw glyphs
y  = 3
lh = 0


count = 0

for code, name in glyphs.items():
    if code < 100: continue
    if count > 16: break
    bounds = get_bbox(glyphset.get(name))
    if bounds == None: continue
    (xmin, ymin, xmax, ymax) = bounds
    header += glyph_template.format(
        5*count + 2.5 - (xmax-xmin)/2, 
        y, 
        chr(code))
    header += rect_template.format(
        5*count + 2.5 - (xmax-xmin)/2 + xmin, 
        y - ymax, 
        xmax-xmin, 
        ymax-ymin)
    count += 1

header += "</g></svg>"
with open(out_font, 'w') as f:
    f.write(header)
