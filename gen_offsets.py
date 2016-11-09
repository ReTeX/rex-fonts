import toml

familes = [ 
    "Normal", "Roman", "Script", 
    "Calligraphic", "Script", "SansSerif", 
    "Fraktur", "Blackboard", "Teletype" ]

weights = [ "None", "Bold", "Italic", "BoldItalic" ]

encodings = [ "LATIN_UPPER", "LATIN_LOWER", "DIGITS", "GREEK_UPPER", "GREEK_LOWER" ]

encoding_map = {
    'Latin': "LATIN_UPPER",
    'latin': "LATIN_LOWER",
    'Greek': "GREEK_UPPER",
    'greek': "GREEK_LOWER",
    'digits': "DIGIT",
}

weight_map = {
    "it": "Italic",
    "bf": "Bold",
    "bfit": "BoldItalic",
    "None": "None",
}

family_map = {
    "normal": "Normal",
    "rm": "Roman",
    "scr": "Script",
    "cal": "Calligraphic",
    "sf": "SansSerif",
    "frak": "Fraktur",
    "bb": "Blackboard",
    "tt": "Teletype",    
}

encode_template = """\
        {0}_START...{0}_END => {{
            match (family, weight) {{\
"""

style_template = """\
                (Family::{1}, Weight::{2}) => offset::{0}_{3}_{4},\
"""

sty_default_template = """\
                (_, Weight::{}) => offset::{}_NORMAL_{},\
"""

cfg = toml.load('unicode.toml')

for encoding, styles in cfg.items():
    ssty = sorted(styles.keys())
    print(encode_template.format(encoding_map[encoding]))
    for style in ssty:
        family = style.split('_', 1)[0]
        if family == "exceptions": continue
        family = family_map[family]

        weight = style.split('_', 1)[1] if len(style.split('_', 1)) > 1 else "None"
        weight = weight_map[weight]

        print(style_template.format(encoding_map[encoding], family, weight, family.upper(), weight.upper()))

    print(sty_default_template.format("None", encoding_map[encoding], "NONE"))
    print(sty_default_template.format("Bold", encoding_map[encoding], "BOLD"))
    print(sty_default_template.format("Italic", encoding_map[encoding], "ITALIC"))
    print(sty_default_template.format("BoldItalic", encoding_map[encoding], "BOLDITALIC"))    
    print("            }")
    print("        },")

data = {
    "LATIN_UPPER": (26, 65),
    "LATIN_LOWER": (26, 97),
    "DIGIT":       (10, 48),
    "GREEK_UPPER": (24, 0x391),
    "GREEK_LOWER": (25, 0x3B1),
}

for encoding, styles in cfg.items():
    ssty = sorted(styles.keys())
    for style in ssty:
        family = style.split('_', 1)[0]
        if family == "exceptions": continue
        family = family_map[family]

        weight = style.split('_', 1)[1] if len(style.split('_', 1)) > 1 else "None"
        weight = weight_map[weight]
        
        print("    const " + encoding_map[encoding] + "_" + family.upper() + "_" + weight.upper() + ": u32 = " + styles[style])
    
