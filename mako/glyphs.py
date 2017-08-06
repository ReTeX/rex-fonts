from mako.template import Template
from fontTools.pens.boundsPen import BoundsPen
from copy import deepcopy

SHIM = [
    # Calligraphic
    (0x1D49D, 0x212C), # B
    (0x1D4A0, 0x2130), # E
    (0x1D4A1, 0x2131), # F
    (0x1D4A3, 0x210B), # H
    (0x1D4A4, 0x2110), # I
    (0x1D4A7, 0x2112), # L
    (0x1D4A8, 0x2133), # M
    (0x1D4AD, 0x211B), # R
    (0x1D4BA, 0x212F), # e
    (0x1D4BC, 0x210A), # g
    (0x1D4C4, 0x2134), # o

    # Double Struck
    (0x1D53A, 0x2102), # C
    (0x1D53F, 0x210D), # H
    (0x1D545, 0x2115), # N
    (0x1D547, 0x2119), # P
    (0x1D548, 0x211A), # Q
    (0x1D549, 0x211D), # R
    (0x1D551, 0x2124), # Z

    # Fracture
    (0x1D506, 0x212D), # C
    (0x1D50B, 0x210C), # H
    (0x1D50C, 0x2111), # I
    (0x1D515, 0x211C), # R
    (0x1D51D, 0x2128), # Z

    # italic
    (0x1D455, 0x210E), # h
]

def gen_glyphs(ttfont):
    math = ttfont['MATH'].table
    cmap = ttfont['cmap'].getcmap(3, 10).cmap
    glyphs = ttfont.getGlyphSet()
    metrics = { name: {
        "usv": codepoint,
        "xmin": 0,
        "ymin": 0,
        "xmax": 0,
        "ymax": 0,
        "attachment": 0,
        "italics": 0,
        "advance": 0,
        "lsb": 0,
    } for codepoint, name in cmap.items() }

    # Gather bounding box information
    pen = BoundsPen(None)
    for glyph in cmap.values():
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
    for glyph in cmap.values():
        (advance, lsb) = hmtx[glyph]
        metrics[glyph]["advance"] = advance
        metrics[glyph]["lsb"]     = lsb

    # Insert shim
    shim = []
    cmap = ttfont['cmap'].getcmap(3, 10).cmap
    for (new, old) in SHIM:
        name = cmap[old]
        data = deepcopy(metrics[name])
        print(new, old, data, sep='->')
        shim.append((new, data))

    template = Template(filename="glyphs.mako.rs")
    with open("glyphs.rs", 'w') as file:
        file.write(template.render(glyphs=metrics, shim=shim))


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

    print("Generating glyphs.rs")
    FONT = TTFont(sys.argv[1])
    gen_glyphs(FONT)