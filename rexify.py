'''
rexify.py

Prepare an OpenType font for use with ReX.  Rexify will look for glyphs that
are not accessible from a CMAP, place those glyphs into a Private Usage Area
and modify the CMAPs to include these glyphs.  This is necessary for when
you want to render math in SVG by referring to glyphs from their usv.
'''

import json
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

# TODO: Deleted undesired glyphs.
# TODO: We need to modify the name/copyright to adhere to SIL license.


def rexify(font, out):
    '''
    Rexify font.

    This will take all inaccessible glyphs from the font,
    place them in a PUA, and modify the CMAPs so that these
    glyphs are publicly accessible.

    This will also generate the metrics for `font` and store
    them at `out`.metrics.
    '''

    ttfont = TTFont(font, recalcBBoxes=False)
    make_accessible(ttfont, font)
    generate_metrics(ttfont, out + ".metrics")
    ttfont.save(out)


def make_accessible(ttfont, font):
    '''
    This will take all inaccessible glyphs from the font,
    place them in a PUA, and modify the CMAPs so that these
    glyphs are publicly accessible.
    '''

    # Generate a map from GlyphNames to a _set_ of CodePoints.
    accessible = set(ttfont['cmap'].buildReversed().keys())
    accessible.add('.notdef')

    # Gather all named glyphs in the font.
    glyphs = ttfont.getGlyphSet().keys()

    # Filter all inaccessible glyphs
    unaccessible = [glyph for glyph in glyphs if glyph not in accessible]
    required = len(unaccessible)

    if required == 0:
        print("All glyphs are accessible! <3")
        return
    else:
        print(required, "glyphs need to be placed into PUA.")

    # Find a suitably long vacant region in the PUA, U+E000–U+F8FF.
    # Currently we only look at cmap(3, 10), a recommended cmap format;
    # however this may not be very robust.
    used = set(ttfont['cmap'].getcmap(3, 10).cmap.keys())
    unused = (usv for usv in range(0xE000, 0xF8FF) if usv not in used)
    start = next(csv for csv, l in ContinuousRegions(unused) if l >= required)
    print("Placing PUA glyphs at", hex(start))

    # To prevent thrashing the CMAPs, we reorder the glyph indices
    # to match the order for which they are placed in PUA
    cache = set(unaccessible)
    old_order = ttfont.getGlyphOrder()
    new_order = [g for g in old_order if g not in cache] + unaccessible

    for cmap in ttfont['cmap'].tables:
        if not cmap.isUnicode():
            print("Skipping", cmap, "as non-unicode table")
            continue

        for offset, glyph in enumerate(unaccessible):
            cmap.cmap[start + offset] = glyph


def generate_metrics(ttfont, out):
    '''
    Generate the metrics for `font` and store them at `out` in json
    '''

    print("Generating glyph metrics.")
    glyph_set = ttfont.getGlyphSet()
    glyphs = ttfont['cmap'].buildReversed()
    metrics = {}

    pen = BoundsPen(None)
    for name, usvs in glyphs.items():
        metric = (0, 0, 0, 0)
        glyph_set.get(name).draw(pen)

        if pen.bounds is not None:
            (xm, ym, xM, yM) = pen.bounds
            metric = (int(xm), int(ym), int(xM), int(yM))

        for usv in iter(usvs):
            metrics[int(usv)] = metric

        pen.bounds = None
        pen._start = None

    with open(out, 'w') as file:
        json.dump(metrics, file)


class ContinuousRegions:
    '''
    Continuous Regions.

    This is an iterator adapter which takes an iterator of numbers
    and returns tupples (start, length) of indicated contiuos regions
    starting at `start` of length `length`.
    '''

    def __init__(self, it):
        self._it = it
        self._peek = next(self._it)

    def __iter__(self):
        return self

    def __next__(self):
        start = self._peek
        count = 1
        for idx, csv in enumerate(self._it):
            self._peek = csv
            if csv - idx == start + 1:
                count += 1
            else:
                break

        return (start, count)

if __name__ == "__main__":
    import sys

    USAGE = "usage: rexify.py in.otf out.otf\n" \
            "`rexify.py` will gather all glyphs from `in.otf` that aren't accessible " \
            "from a CMAP and place them into Private Use Area codepoitns. Then " \
            "`rexify.py` will update the CMAPs to make these glyphs accessible."

    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    FONT = sys.argv[1]
    OUT = sys.argv[2]

    print("Rexifying:", FONT)
    rexify(FONT, OUT)
    print("Finished rexifying:", OUT)
