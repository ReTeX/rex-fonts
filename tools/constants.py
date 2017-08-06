from mako.template import Template

PERCENTAGES = [
    ('ScriptPercentScaleDown', 'script_percent_scale_down'),
    ('ScriptScriptPercentScaleDown', 'script_script_percent_scale_down'),
]

CONSTANTS = [
    ('AccentBaseHeight', 'accent_base_height'),
    ('AxisHeight', 'axis_height'),
    ('DelimitedSubFormulaMinHeight', 'delimited_sub_formula_min_height'),
    ('DisplayOperatorMinHeight', 'display_operator_min_height'),
    ('FlattenedAccentBaseHeight', 'flattened_accent_base_height'),
    ('FractionDenomDisplayStyleGapMin', 'fraction_denom_display_style_gap_min'),
    ('FractionDenominatorDisplayStyleShiftDown',
     'fraction_denominator_display_style_shift_down'),
    ('FractionDenominatorGapMin', 'fraction_denominator_gap_min'),
    ('FractionDenominatorShiftDown', 'fraction_denominator_shift_down'),
    ('FractionNumDisplayStyleGapMin', 'fraction_num_display_style_gap_min'),
    ('FractionNumeratorDisplayStyleShiftUp',
     'fraction_numerator_display_style_shift_up'),
    ('FractionNumeratorGapMin', 'fraction_numerator_gap_min'),
    ('FractionNumeratorShiftUp', 'fraction_numerator_shift_up'),
    ('FractionRuleThickness', 'fraction_rule_thickness'),
    ('LowerLimitBaselineDropMin', 'lower_limit_baseline_drop_min'),
    ('LowerLimitGapMin', 'lower_limit_gap_min'),
    ('MathLeading', 'math_leading'),
    ('OverbarExtraAscender', 'overbar_extra_ascender'),
    ('OverbarRuleThickness', 'overbar_rule_thickness'),
    ('OverbarVerticalGap', 'overbar_vertical_gap'),
    ('RadicalDegreeBottomRaisePercent', 'radical_degree_bottom_raise_percent'),
    ('RadicalDisplayStyleVerticalGap', 'radical_display_style_vertical_gap'),
    ('RadicalExtraAscender', 'radical_extra_ascender'),
    ('RadicalKernAfterDegree', 'radical_kern_after_degree'),
    ('RadicalKernBeforeDegree', 'radical_kern_before_degree'),
    ('RadicalRuleThickness', 'radical_rule_thickness'),
    ('RadicalVerticalGap', 'radical_vertical_gap'),
    ('SkewedFractionHorizontalGap', 'skewed_fraction_horizontal_gap'),
    ('SkewedFractionVerticalGap', 'skewed_fraction_vertical_gap'),
    ('SpaceAfterScript', 'space_after_script'),
    ('StackBottomDisplayStyleShiftDown', 'stack_bottom_display_style_shift_down'),
    ('StackBottomShiftDown', 'stack_bottom_shift_down'),
    ('StackDisplayStyleGapMin', 'stack_display_style_gap_min'),
    ('StackGapMin', 'stack_gap_min'),
    ('StackTopDisplayStyleShiftUp', 'stack_top_display_style_shift_up'),
    ('StackTopShiftUp', 'stack_top_shift_up'),
    ('StretchStackBottomShiftDown', 'stretch_stack_bottom_shift_down'),
    ('StretchStackGapAboveMin', 'stretch_stack_gap_above_min'),
    ('StretchStackGapBelowMin', 'stretch_stack_gap_below_min'),
    ('StretchStackTopShiftUp', 'stretch_stack_top_shift_up'),
    ('SubSuperscriptGapMin', 'sub_superscript_gap_min'),
    ('SubscriptBaselineDropMin', 'subscript_baseline_drop_min'),
    ('SubscriptShiftDown', 'subscript_shift_down'),
    ('SubscriptTopMax', 'subscript_top_max'),
    ('SuperscriptBaselineDropMax', 'superscript_baseline_drop_max'),
    ('SuperscriptBottomMaxWithSubscript', 'superscript_bottom_max_with_subscript'),
    ('SuperscriptBottomMin', 'superscript_bottom_min'),
    ('SuperscriptShiftUp', 'superscript_shift_up'),
    ('SuperscriptShiftUpCramped', 'superscript_shift_up_cramped'),
    ('UnderbarExtraDescender', 'underbar_extra_descender'),
    ('UnderbarRuleThickness', 'underbar_rule_thickness'),
    ('UnderbarVerticalGap', 'underbar_vertical_gap'),
    ('UpperLimitBaselineRiseMin', 'upper_limit_baseline_rise_min'),
    ('UpperLimitGapMin', 'upper_limit_gap_min'),
]


def gen_constants(ttfont, out):
    consts = []
    percents = []
    math_table = ttfont['MATH'].table.MathConstants

    for constant, name in CONSTANTS:
        try:
            value = math_table.__getattribute__(constant).Value
        except AttributeError:
            value = math_table.__getattribute__(constant)

        consts.append((name, value))

    for constant, name in PERCENTAGES:
        try:
            value = math_table.__getattribute__(constant).Value
        except AttributeError:
            value = math_table.__getattribute__(constant)
        percents.append((name, value))

    upem = ttfont['head'].unitsPerEm
    connector_overlap = ttfont['MATH'].table.MathVariants.MinConnectorOverlap

    template = Template(filename="tools/mako/constants.mako.rs")
    with open(out + "constants.rs", 'w') as file:
        file.write(template.render(
            upem=upem,
            connector_overlap=connector_overlap,
            percents=percents,
            constants=consts
        ))


if __name__ == "__main__":
    import sys
    from fontTools.ttLib import TTFont

    USAGE = "usage: python3 constants.py font.otf\n" \
            "`constants.py` will extract the Math table constants " \
            "and generate their correspoding rust constants in " \
            "`constants.rs`."

    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(USAGE)
        sys.exit(0)

    print("Generating Constants.rs")
    FONT = TTFont(sys.argv[1])
    gen_constants(FONT)
