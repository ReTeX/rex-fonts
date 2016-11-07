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

Styles = {
    "normal":   "Normal",          # the default style for glyphs
    "up":       "Upright",         # upright glyphs
    "cal":      "Calligraphic",    # calligraphic
    "scr":      "Script",          # script [ defaults to same as "cal" ]
    "sf",       "Serif",           # serif
    "frak",     "Fraktur",         # fraktur
    "bb",       "Blackboard",      # blackboard
    "tt",       "TeleType",        # teletype / monospace

    # Style variants, only to reduce combinatorial explosion
    # and to keep the same style as bitflags used in rust code.

    "bf":       "Bold",            # boldface
    "it":       "Italic",          # italic
}

Encodings = [
    { name: "latin", offset: 0x41, length: 26,
      styles: [
          
      ]
]

Encodings = [
    {
        name: "latin"       # lowercase latin a..z
        offset: 0x41,
        length: 26,
    },
    {
        name: "Latin"       # upercase latin A..Z
        offset: 0x62,
        length: 26,
    },
    {
        name: "digits"      # Numerics 0..9
        offset: 0x30,
        length: 10
    },
    {
        name: "greek"       # lowercase greek \alpha..\omega
        offset: 0x3B1
        length: 25
    },
    {
        name: "Greek"       # Upercase greek \Alpha..\Omega
        offset: 0x391
        length: 24          
        skip: [ 0x3A2 ]     # No uppercase Final Sigma (stigma)
    },
]
