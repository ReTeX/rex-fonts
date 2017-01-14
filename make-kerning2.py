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
file_out = "out/" + os.path.splitext(os.path.basename(font_file))[0][4:] + "/kerning_table2.rs"
font     = TTFont(font_file)

cmap = {}
for c in font['cmap'].tables:
    cmap.update(c.cmap)

header = """\
#![allow(dead_code)]
use std::collections::HashMap;
use super::{ KernRecord, KernTable };

pub static KERNING_TABLE: [(u32, KernRecord)] = [
"""

record     = "    (0x{:X}, KernRecord {{ // {}\n"

value_none = "        {}: None,\n"   
value_some = "        {}: Some(KernTable {{\n"

corrections = "            correction_heights: [ {} ],\n"
values      = "            kern_values: [ {} ],\n"

value_end   = "        }),\n"
record_end  = "    }),\n"

end         = "\n];"

coverage = font['MATH'].table.MathGlyphInfo.MathKernInfo.MathKernCoverage
kernings = font['MATH'].table.MathGlyphInfo.MathKernInfo.MathKernInfoRecords

cmap = {}
for c in font['cmap'].tables:
    cmap.update(c.cmap)

codes = dict([ (name, code) for code, name in cmap.items() ])

# Here we assume that the maximum size is 2
def listify(xs, size):
    # first extract the values
    xs  = [ x.Value for x in xs ]
    # pad the list with trailing zeros
    xs += [ 0 ] * (size - len(xs))
    xs  = [ str(x) for x in xs ]
    return ', '.join(xs)

for idx, name in enumerate(coverage.glyphs):
    code = codes[name]
    header += record.format(code, name)
    
    if kernings[idx].TopRightMathKern is not None:
        k = kernings[idx].TopRightMathKern
        header += value_some.format("top_right")
        header += corrections.format(listify(k.CorrectionHeight, 1))
        header += values.format(listify(k.KernValue, 2))
        header += value_end
    else:
        header += value_none.format("top_right")
        
    if kernings[idx].TopLeftMathKern is not None:
        k = kernings[idx].TopLeftMathKern
        header += value_some.format("top_left")
        header += corrections.format(listify(k.CorrectionHeight, 1))
        header += values.format(listify(k.KernValue, 2))
        header += value_end
    else:
        header += value_none.format("top_left")
        
    if kernings[idx].BottomRightMathKern is not None:
        k = kernings[idx].BottomRightMathKern
        header += value_some.format("bottom_right")
        header += corrections.format(listify(k.CorrectionHeight, 1))
        header += values.format(listify(k.KernValue, 2))
        header += value_end
    else:
        header += value_none.format("bottom_right")
        
    if kernings[idx].BottomLeftMathKern is not None:
        k = kernings[idx].BottomLeftMathKern
        header += value_some.format("bottom_left")
        header += corrections.format(listify(k.CorrectionHeight, 1))
        header += values.format(listify(k.KernValue, 2))
        header += value_end
    else:
        header += value_none.format("bottom_left")
    
    header += record_end

header += end

#print(header)
with open(file_out, 'w') as f:
    f.write(header)
