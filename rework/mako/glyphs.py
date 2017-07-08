from mako.template import Template
from fontTools.pens.boundsPen import BoundsPen

def gen_glyphs(ttfont):
    math = ttfont['MATH'].table
    glyphs = ttfont.getGlyphSet()
    metrics = { name: {
        "usv": 0,
        "xmin": 0,
        "ymin": 0,
        "xmax": 0,
        "ymax": 0,
        "attachment": 0,
        "italics": 0,
        "advance": 0,
        "lsb": 0,
    } for name in glyphs.keys() }

    # Gather bounding box information
    pen = BoundsPen(None)
    for glyph in glyphs.keys():
        bbox = (0, 0, 0, 0)
        glyphs.get(glyph).draw(pen)

        if pen.bounds is not None:
            (xmin, ymin, xmax, ymax) = pen.bounds
            bbox = (int(xmin), int(ymin), int(xmax), int(ymax))

        metrics[glyph]['xmin'] = bbox[0]
        metrics[glyph]['ymin'] = bbox[1]
        metrics[glyph]['xmax'] = bbox[2]
        metrics[glyph]['ymax'] = bbox[3]

        pen.bounds = None
        pen._start = None

    # Gather accent attachment
    accent_table = math.MathGlyphInfo.MathTopAccentAttachment
    accent_coverage = accent_table.TopAccentCoverage.glyphs
    for glyph in accent_coverage:
        value = accent_table \
            .TopAccentAttachment[accent_coverage.index(glyph)] \
            .Value
        metrics[glyph]["attachment"] = value

    # Gather italics offsets
    italics_table = math.MathGlyphInfo.MathItalicsCorrectionInfo
    italics_coverage = italics_table.Coverage.glyphs
    for glyph in italics_coverage:
        value = italics_table \
            .ItalicsCorrection[italics_coverage.index(glyph)] \
            .Value
        metrics[glyph]["italics"] = value

    # Gather advance and left side bearing
    hmtx = ttfont['hmtx'].metrics
    for glyph in glyphs.keys():
        (advance, lsb) = hmtx[glyph]
        metrics[glyph]["advance"] = advance
        metrics[glyph]["lsb"]     = lsb

    reverse_map = ttfont.getReverseGlyphMap()
    for glyph, usv in reverse_map.items():
        metrics[glyph]["usv"] = usv

    template = Template(filename="glyphs.mako.rs")
    with open("glyphs.rs", 'w') as file:
        file.write(template.render(glyphs=metrics))


if __name__ == "__main__":
    import sys
    from fontTools.ttLib import TTFont

    USAGE = "usage: python3 constants.py font.otf\n" \
            "`constants.py` will extract the Math table constants " \
            "and generate their correspoding rust constants in " \
            "`constants.rs`."

    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    print("Generating Constants.rs")
    FONT = TTFont(sys.argv[1])
    gen_glyphs(FONT)