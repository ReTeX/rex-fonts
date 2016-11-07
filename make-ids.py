# make_ids.py <font.otf>
# 
# The purpose of this file is to generate a map from Unicode -> ID.
# There are some properties that this ID value system must satisfy:
#
#   1. For FontStyle selection, we need to ensure that successive unicode points
#      have successive IDs.  The unicode standard has a few exceptions to this
#      that we need to account for.
#
#   2. Unicode characters that are not accessible from the CMAP require an 
#      unicode and ID.

 
# The following table contains the unicode characters that are recognized when 
#   1. Direct input (ie: inputting unicode characters 0x3B1 for greek \Alpha)
#   2. Impacted by font selection algorithm [ie: \Alpha..\Omega, \alpha..\omega, etc.]

#Styles = {
    #"normal":   "Normal",          # the default style for glyphs
    #"up":       "Upright",         # upright glyphs
    #"cal":      "Calligraphic",    # calligraphic
    #"scr":      "Script",          # script [ defaults to same as "cal" ]
    #"sf",       "Serif",           # serif
    #"frak",     "Fraktur",         # fraktur
    #"bb",       "Blackboard",      # blackboard
    #"tt",       "TeleType",        # teletype / monospace

    ## Style variants, only to reduce combinatorial explosion
    ## and to keep the same style as bitflags used in rust code.

    #"bf":       "Bold",            # boldface
    #"it":       "Italic",          # italic
#}

import toml
from fontTools.ttLib import TTFont

font = TTFont('out/rex-xits.otf')

with open('unicode.toml') as f:
    tml = toml.loads(f.read())

names = {}
for cmap in font['cmap'].tables:
    names.update(cmap.cmap)
    
id_list = [ ]  # unicode

length = {
    'Latin': 26,
    'latin': 26,
    'digits': 10,
    'greek': 25,
    'Greek': 24,
}

offsets = {}
families = [ 'Latin', 'latin', 'digits', 'Greek']

# First align desired regions
Latin = tml['Latin']

for family in families:
    cfg = tml[family]
    for style, opts in cfg.items():
        offset = int(opts['offset'], 16)
        exceptions = opts.get('exceptions', {})
        print(exceptions)
        offsets[style] = len(id_list)

        count=0
        idx = offset
        while count < length[family]:
            if idx in exceptions.get('undefined', []):
                id_list.append(35) # which is .notdef glyph? Find first?
                idx += 1
            elif exceptions.get(idx, None):
                id_list.append(int(exceptions[idx],16))
                idx += 1
                count += 1
            else:
                id_list.append(idx)
                idx += 1
                count += 1
            
print(id_list, len(id_list), offsets)
