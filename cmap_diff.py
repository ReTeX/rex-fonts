from fontTools.ttLib import TTFont

# This snippet will list all glyphs that are not reachable from the cmap
font   = TTFont('XITS-Math.otf')
cmaps  = font['cmap'].tables
glyphs = font.getGlyphNames()

mapped = []
for cmap in cmaps:
    for key, value in cmap.cmap.items():
        if value not in mapped:
            mapped.append(value)

diff = [glyph for glyph in glyphs 
            if glyph not in set(mapped) ] # and glyph[-2:] != 'st' and glyph[-2:] != 'ts']
print(diff)
