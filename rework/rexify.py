# The purpose of this script is to place all glyphs that aren't accessible from
# the various CMAPs to PUA.  Then to modify the CMAPs to make the glyphs accessible.
#
# TODO: GlyphIDs should be a continuous region with respect to PUA usv.
# TODO: Deleted glyphs included here.

from fontTools.ttLib import TTFont
from itertools import takewhile
from operator import itemgetter

def rexify(font, out):
    font = TTFont(font)
    cmap = set(font['cmap'].buildReversed().keys())
    glyphs = sorted(font.getGlyphSet().keys())

    # All glyph indices that are not accessible via cmap
    diff = [ glyph for glyph in glyphs if glyph not in cmap ]

    # First find a suitable region in the PUA, U+E000–U+F8FF
    # We will do this by calculating the empty regions in codepoints and find the first
    # region is is large enough to fit the `diff` list.
    required = len(diff)
    used_usv = font['cmap'].getcmap(3,1).cmap.keys()
    unused = ( usv for usv in range(0xE000, 0xF8FF) if usv not in used_usv )

    start = next(csv for csv, l in ContinuousRegions(unused) if l >= required)
    print("Placing glyphs at", hex(start))

# Helper class.  Takes an iterator of numbers, and returns a
# tuple of (start, length) for continuous regions.
class ContinuousRegions:
    def __init__(self, it):
        self.it = it

    def __iter__(self):
        return self

    def __next__(self):
        start = next(self.it)
        count = 1 + sum(1 for _ in
            takewhile(lambda t: t[1] - t[0] == start + 1, enumerate(self.it)))
        return (start, count)

if __name__ == "__main__":
    import os
    import sys

    def usage():
        print("usage: rexify.py in.otf out.otf")
        print("`rexify.py` will gather all glyphs from `in.otf` that aren't accessible "
              "from a CMAP and place them into Private Use Area codepoitns. Then "
              "`rexify.py` will update the CMAPs to make these glyphs accessible.")

    if len(sys.argv) < 3:
        usage()
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit(0)

    font = sys.argv[1]
    out = sys.argv[2]

    print("Rexifying: ", font)
    rexify(font, out)
    print("Finished rexifying.")