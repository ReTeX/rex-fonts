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
    
    names = {}      # Mapping from Unicode -> Name
    ids = []        # List of consecutive Glyph IDs 
    id_map = {}     # Mapping from Name -> ID
    offsets = []    # Lists of (family, style, offset) for Glyph IDs 
    families = [    # List of recognized families
        'Latin', 'latin', 'digits', 'Greek'
    ]
    
    def __init__(self, font, config):
        self.font = TTFont(font)
        with open(config) as f:
            _config = toml.loads(f.read())
        
        self.undefined = int(_config['undefined'], 16)
        
        # TODO: We should probably handle Latin better
        for cmap in self.font['cmap'].tables:
            self.names.update(cmap.cmap)
        
        # Temporary names dictionary which we will modify
        _names = copy.deepcopy(self.names)
        
        # Construct the IDs table
        for family in self.families:
            # Sort for deterministic ID construction
            for style, opts in sorted(_config[family].items(), key=lambda t: t[0]):
                self.offsets.append((family, style, len(self.ids)))
                exceptions = opts.get('exceptions', {})
                offset = int(opts['offset'], 16)   # Starting unicode offset
                for idx in range(offset, offset + self.LENGTH[family]):
                    if idx in exceptions.get('undefined', []):
                        self.ids.append(self.undefined)
                    elif exceptions.get(str(idx), None):
                        self.ids.append(int(exceptions[str(idx)], 16))
                    else:
                        self.ids.append(idx)
                        
                    # we no longer need this in names
                    self.id_map[_names.pop(idx, None)] = idx

        # Construct the rest of the IDs by simply placing them in order
        # First reverse the dictionary, and update
        __names = sorted(_names.items(), key = lambda  t: t[0])
        self.id_map.update({ name: idx for idx, (_, name) in enumerate(__names) })
