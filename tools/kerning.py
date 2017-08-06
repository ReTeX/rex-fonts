def gen_kerning(font, out):
    header = """\
use font_types::{KernRecord, KernTable};

pub static KERNING_TABLE: [(u32, KernRecord); _] = [
"""
    record = "    (0x{:X}, KernRecord {{ // {}\n"
    value_none = "        {}: None,\n"
    value_some = "        {}: Some(KernTable {{\n"
    corrections = "            correction_heights: &[ {} ],\n"
    values = "            kern_values: &[ {} ],\n"
    value_end = "        }),\n"
    record_end = "    }),\n"
    end = "\n];"

    kern_info = font['MATH'].table.MathGlyphInfo.MathKernInfo
    if not hasattr(kern_info, "MathKernCoverage") or not hasattr(kern_info, "MathKernInfoRecords"):
        print("Unable to find kerning table; skipping.")
        return

    coverage = kern_info.MathKernCoverage
    kernings = kern_info.MathKernInfoRecords
    codes = {name: code for code,
             name in font['cmap'].getcmap(3, 10).cmap.items()}

    skipped = []

    for idx, name in enumerate(coverage.glyphs):
        code = codes[name]

        # Stix2 is weird. It has empty kerning tables? Why?
        if kernings[idx].TopRightMathKern is None \
                and kernings[idx].TopLeftMathKern is None \
                and kernings[idx].BottomRightMathKern is None \
                and kernings[idx].BottomLeftMathKern is None:
            skipped.append(hex(code))
            continue

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

    if len(skipped) != 0:
        print("Skipped", len(skipped), "kerning records:", skipped)

    header += end
    with open(out + "kerning.rs", mode='w') as f:
        f.write(header)


# Here we assume that the maximum size is 2
def listify(xs, size):
    # first extract the values
    xs = ["fontunit!({})".format(x.Value) for x in xs]
    return ', '.join(xs)


if __name__ == "__main__":
    import sys
    from fontTools.ttLib import TTFont

    USAGE = "usage: python3 kerning.py font.otf\n" \
            "`kerning.py` will extract the Math table constants " \
            "and generate their correspoding rust constants in " \
            "`constants.rs`."

    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    print("Generating kerning.rs")
    FONT = TTFont(sys.argv[1])
    gen_kerning(FONT)
