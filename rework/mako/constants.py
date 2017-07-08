from mako.template import Template

CONSTANTS = [
    ('AccentBaseHeight', 'accent_base_height', 'i16'),
    ('AxisHeight', 'axis_height', 'i16'),
    ('DelimitedSubFormulaMinHeight', 'delimited_sub_formula_min_height', 'u16'),
    ('DisplayOperatorMinHeight', 'display_operator_min_height', 'u16'),
    ('FlattenedAccentBaseHeight', 'flattened_accent_base_height', 'i16'),
    ('FractionDenomDisplayStyleGapMin', 'fraction_denom_display_style_gap_min', 'i16'),
    ('FractionDenominatorDisplayStyleShiftDown', 'fraction_denominator_display_style_shift_down', 'i16'),
    ('FractionDenominatorGapMin', 'fraction_denominator_gap_min', 'i16'),
    ('FractionDenominatorShiftDown', 'fraction_denominator_shift_down', 'i16'),
    ('FractionNumDisplayStyleGapMin', 'fraction_num_display_style_gap_min', 'i16'),
    ('FractionNumeratorDisplayStyleShiftUp', 'fraction_numerator_display_style_shift_up', 'i16'),
    ('FractionNumeratorGapMin', 'fraction_numerator_gap_min', 'i16'),
    ('FractionNumeratorShiftUp', 'fraction_numerator_shift_up', 'i16'),
    ('FractionRuleThickness', 'fraction_rule_thickness', 'i16'),
    ('LowerLimitBaselineDropMin', 'lower_limit_baseline_drop_min', 'i16'),
    ('LowerLimitGapMin', 'lower_limit_gap_min', 'i16'),
    ('MathLeading', 'math_leading', 'i16'),
    ('OverbarExtraAscender', 'overbar_extra_ascender', 'i16'),
    ('OverbarRuleThickness', 'overbar_rule_thickness', 'i16'),
    ('OverbarVerticalGap', 'overbar_vertical_gap', 'i16'),
    ('RadicalDegreeBottomRaisePercent', 'radical_degree_bottom_raise_percent', 'i16'),
    ('RadicalDisplayStyleVerticalGap', 'radical_display_style_vertical_gap', 'i16'),
    ('RadicalExtraAscender', 'radical_extra_ascender', 'i16'),
    ('RadicalKernAfterDegree', 'radical_kern_after_degree', 'i16'),
    ('RadicalKernBeforeDegree', 'radical_kern_before_degree', 'i16'),
    ('RadicalRuleThickness', 'radical_rule_thickness', 'i16'),
    ('RadicalVerticalGap', 'radical_vertical_gap', 'i16'),
    ('ScriptPercentScaleDown', 'script_percent_scale_down', 'i16'),
    ('ScriptScriptPercentScaleDown', 'script_script_percent_scale_down', 'i16'),
    ('SkewedFractionHorizontalGap', 'skewed_fraction_horizontal_gap', 'i16'),
    ('SkewedFractionVerticalGap', 'skewed_fraction_vertical_gap', 'i16'),
    ('SpaceAfterScript', 'space_after_script', 'i16'),
    ('StackBottomDisplayStyleShiftDown', 'stack_bottom_display_style_shift_down', 'i16'),
    ('StackBottomShiftDown', 'stack_bottom_shift_down', 'i16'),
    ('StackDisplayStyleGapMin', 'stack_display_style_gap_min', 'i16'),
    ('StackGapMin', 'stack_gap_min', 'i16'),
    ('StackTopDisplayStyleShiftUp', 'stack_top_display_style_shift_up', 'i16'),
    ('StackTopShiftUp', 'stack_top_shift_up', 'i16'),
    ('StretchStackBottomShiftDown', 'stretch_stack_bottom_shift_down', 'i16'),
    ('StretchStackGapAboveMin', 'stretch_stack_gap_above_min', 'i16'),
    ('StretchStackGapBelowMin', 'stretch_stack_gap_below_min', 'i16'),
    ('StretchStackTopShiftUp', 'stretch_stack_top_shift_up', 'i16'),
    ('SubSuperscriptGapMin', 'sub_superscript_gap_min', 'i16'),
    ('SubscriptBaselineDropMin', 'subscript_baseline_drop_min', 'i16'),
    ('SubscriptShiftDown', 'subscript_shift_down', 'i16'),
    ('SubscriptTopMax', 'subscript_top_max', 'i16'),
    ('SuperscriptBaselineDropMax', 'superscript_baseline_drop_max', 'i16'),
    ('SuperscriptBottomMaxWithSubscript', 'superscript_bottom_max_with_subscript', 'i16'),
    ('SuperscriptBottomMin', 'superscript_bottom_min', 'i16'),
    ('SuperscriptShiftUp', 'superscript_shift_up', 'i16'),
    ('SuperscriptShiftUpCramped', 'superscript_shift_up_cramped', 'i16'),
    ('UnderbarExtraDescender', 'underbar_extra_descender', 'i16'),
    ('UnderbarRuleThickness', 'underbar_rule_thickness', 'i16'),
    ('UnderbarVerticalGap', 'underbar_vertical_gap', 'i16'),
    ('UpperLimitBaselineRiseMin', 'upper_limit_baseline_rise_min', 'i16'),
    ('UpperLimitGapMin', 'upper_limit_gap_min', 'i16'),
]

def gen_constants(ttfont):
    consts = []
    math_table = ttfont['MATH'].table.MathConstants

    for constant, name, unit in CONSTANTS:
        try:
            value = math_table.__getattribute__(constant).Value
        except AttributeError:
            value = math_table.__getattribute__(constant)
        
        consts.append((name, unit, value))

    upem = ttfont['head'].unitsPerEm
    connector_overlap = ttfont['MATH'].table.MathVariants.MinConnectorOverlap

    template = Template(filename="constants.mako.rs")
    with open("constants.rs", 'w') as file:
        file.write(template.render( \
            constants=consts, \
            upem=upem, \
            connector_overlap=connector_overlap))

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