'''
rexify.py

Prepare an OpenType font for use with ReX.  Rexify will look for glyphs that
are not accessible from a CMAP, place those glyphs into a Private Usage Area
and modify the CMAPs to include these glyphs.  This is necessary for when
you want to render math in SVG by referring to glyphs from their usv.
'''

from fontTools.ttLib import TTFont

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
