def make_accessible(ttfont):
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
