extern crate phf_codegen;

use std::fs::File;
use std::io::{BufWriter, Write};
use std::path::Path;
use std::env;

fn main() {
    let out_dir = Path::new(&env::var_os("OUT_DIR").expect("OUT_DIR"))
        .join("font
}



shim = [
    # Calligraphic
    (0x1D49D, 0x212C), # B
    (0x1D4A0, 0x2130), # E
    (0x1D4A1, 0x2131), # F
    (0x1D4A3, 0x210B), # H
    (0x1D4A4, 0x2110), # I
    (0x1D4A7, 0x2112), # L
    (0x1D4A8, 0x2133), # M
    (0x1D4AD, 0x211B), # R
    (0x1D4BA, 0x212F), # e
    (0x1D4BC, 0x210A), # g
    (0x1D4C4, 0x2134), # o
    
    # Double Struck
    (0x1D53A, 0x2102), # C
    (0x1D53F, 0x210D), # H
    (0x1D545, 0x2115), # N
    (0x1D547, 0x2119), # P
    (0x1D548, 0x211A), # Q
    (0x1D549, 0x211D), # R
    (0x1D551, 0x2124), # Z
    
    # Fracture
    (0x1D506, 0x212D), # C
    (0x1D50B, 0x210C), # H
    (0x1D50C, 0x2111), # I
    (0x1D515, 0x211C), # R
    (0x1D51D, 0x2128), # Z
    
    # italic 
    (0x1D455, 0x210E), # h
]
