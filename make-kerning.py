import os
import sys

from collections import OrderedDict
from fontTools.ttLib import TTFont

if len(sys.argv) != 2:
    print("usage: make-kerning.py font.otf")
    print("\nThis file will read font.otf, extract the relavent infomration "
          "needed to create a Glyph structure in rust.  This will save the file "
          "as out/font/glyphs.rs.  This file assumes the font has a rex- prefix.")
    sys.exit(1)

font_file  = sys.argv[1]
file_out = "out/" + os.path.splitext(os.path.basename(font_file))[0][4:] + "/glyphs.rs"
font     = TTFont(font_file)

cmap = {}
for c in font['cmap'].tables:
    cmap.update(c.cmap)

header = """\
#![allow(dead_code)]
use std::collections::HashMap;
use super::{ KernRecord, KernTable };

lazy_static! {
pub static ref KERNINGS: HashMap<u32, KernRecord> = {
    let mut k = HashMap::new();
    
"""

record     = "    k.insert(0x{:X}, KernRecord {{ // {}\n"

value_none = "        {}: None,\n"   
value_some = "        {}: Some(KernTable {{\n"

corrections = "            correction_heights: vec![ {} ],\n"
values      = "            kern_values: vec![ {} ],\n"

value_end   = "        }),\n"
record_end  = "    });\n"

end         = """\
    k
};
}"""

coverage = font['MATH'].table.MathGlyphInfo.MathKernInfo.MathKernCoverage
kernings = font['MATH'].table.MathGlyphInfo.MathKernInfo.MathKernInfoRecords

cmap = {}
for c in font['cmap'].tables:
    cmap.update(c.cmap)

codes = dict([ (name, code) for code, name in cmap.items() ])

def listify(l):
    res = ""
    if len(l) == 0:
        return res

    for item in l:
        res += str(item.Value) + ", "

    return res[:-2]

for idx, name in enumerate(coverage.glyphs):
    code = codes[name]
    header += record.format(code, name)
    
    if kernings[idx].TopRightMathKern is not None:
        k = kernings[idx].TopRightMathKern
        header += value_some.format("top_right")
        header += corrections.format(listify(k.CorrectionHeight))
        header += values.format(listify(k.KernValue))
        header += value_end
    else:
        header += value_none.format("top_right")
        
    if kernings[idx].TopLeftMathKern is not None:
        k = kernings[idx].TopLeftMathKern
        header += value_some.format("top_left")
        header += corrections.format(listify(k.CorrectionHeight))
        header += values.format(listify(k.KernValue))
        header += value_end
    else:
        header += value_none.format("top_left")
        
    if kernings[idx].BottomRightMathKern is not None:
        k = kernings[idx].BottomRightMathKern
        header += value_some.format("bottom_right")
        header += corrections.format(listify(k.CorrectionHeight))
        header += values.format(listify(k.KernValue))
        header += value_end
    else:
        header += value_none.format("bottom_right")
        
    if kernings[idx].BottomLeftMathKern is not None:
        k = kernings[idx].BottomLeftMathKern
        header += value_some.format("bottom_left")
        header += corrections.format(listify(k.CorrectionHeight))
        header += values.format(listify(k.KernValue))
        header += value_end
    else:
        header += value_none.format("bottom_left")
    
    header += record_end

header += end

print(header)

#with open(file_out, 'w') as f:
#    f.write(header)

