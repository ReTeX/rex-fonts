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
from collections import OrderedDict
import copy
import toml
from fontTools.ttLib import TTFont

class MathFont:
    LENGTH = {
        'Latin': 26,
        'latin': 26,
        'digits': 10,
        'greek': 25,
        'Greek': 25,
    }

    # List of recognized families
    families = [ 'Latin', 'latin', 'digits', 'Greek' ]

    name    = {}              # Mapping from Unicode -> Name
    gid     = OrderedDict()   # Mapping from Unicode -> Glyph ID
    offsets = []              # Lists of (family, style, offset) for Glyph IDs
    
    def __init__(self, font, config):
        self.font = TTFont(font)
        with open(config) as f:
            _config = toml.loads(f.read())
 
        # Obtain Unicode -> Names mapping from CMAPS
        # TODO: We should probably handle Latin better
        for cmap in self.font['cmap'].tables:
            self.name.update(cmap.cmap)
        
        _names = copy.deepcopy(self.name)
        
        # Construct the ID table, Unicode -> ID mapping.
        id_count = 0
        undefined = int(_config['undefined'], 16)
        for family in self.families:
            # Sort for deterministic ID construction
            for style, opts in sorted(_config[family].items(), key=lambda t: t[0]):
                self.offsets.append((family, style, id_count))
                exceptions = opts.get('exceptions', {})
                offset = int(opts['offset'], 16)   # Starting unicode offset
                for code in range(offset, offset + self.LENGTH[family]):
                    if code in exceptions.get('undefined', []):
                        code = undefined
                    elif exceptions.get(str(code), None):
                        code = int(exceptions[str(code)], 16)

                    # we no longer want this in name in _name
                    _names.pop(code, None)
                    self.gid[code] = id_count
                    id_count += 1

        # Construct the rest of the IDs in order by unicode
        _names = sorted(_names.keys())
        self.gid.update([ (code, idx + id_count) for idx, code in enumerate(_names) ])

mf = MathFont('out/rex-xits.otf', 'unicode.toml')

## Assert that mf.gid is order
for l, r in zip(mf.gid.items(), 
         sorted(mf.gid.items(), key=lambda t: t[1])):
    if l != r:
        print(l, r)
