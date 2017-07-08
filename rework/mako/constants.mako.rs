// DO NOT MODIFY.  This file is automatically generated by `gen_constats.py` 
// in the rex-font repo.
//
// Font: \
<%! from datetime import datetime %>
// Modified: ${datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#![allow(dead_code)]
use dimensions::FontUnit;

pub const UNITS_PER_EM: u16 = ${upem};
pub const MIN_CONNECTOR_OVERLAP: u32 = ${connector_overlap};

% for (name, unit, value) in constants:
pub const ${name.upper()}: FontUnit<${unit}> = FontUnit(${value});
% endfor