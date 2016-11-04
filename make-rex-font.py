from fontTools.ttLib import TTFont

import os
import sys

if len(sys.argv) != 2:
    print("usage: make-rex-font.py font.otf")
    print("\nThis script will read font.otf, find all glyphs that are " +
          "not accessible by unicode as determined by the CMAP, and will place " +
          "these glyphs into a Private Use Region, starting at 0xE700.  This script " +
          "will then save the new font as out/rex-font.otf")
    sys.exit(1)

# This snippet will list all glyphs that are not reachable from the cmap
font_file = sys.argv[1]
out_file  = "out/rex-" + os.path.basename(font_file)

font   = TTFont(font_file)
cmaps  = font['cmap'].tables
glyphs = font.getGlyphNames()

# Find all unique GlyphNames that is reachable from a cmap
mapped = []
for cmap in cmaps:
    for key, value in cmap.cmap.items():
        if value not in mapped:
            mapped.append(value)

# TODO: Rework this correctly, might need to study how to best
# to remove these symbols from CMAP
# This acts to filter out GlyphNames we don't care about
#def valid(glyph):
#    # ssty glyphs -- may be useful later on for script variants
#    if glyph[-2:] == 'st' or glyph[-2:] == 'ts':
#        return False
#    return True

diff = [ glyph for glyph in glyphs 
            if glyph not in set(mapped) ]

# The CMAPS in XITS is:
# Format 4  in 0 and 4
# Format 12 in 1 and 5
base  = 0xE700
start = base
for glyph in diff:
    #print("Adding {} to code point 0x{:X}".format(glyph, start))
    for table in cmaps:
        if table.format == 4 or table.format == 12:
            table.cmap[start] = glyph
    start += 1

print("Finished.  Added {} glyphs to CMAPs in ranges {:X} to {:X}".format(start - base, base, start))
font.save(out_file)
