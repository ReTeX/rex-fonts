#!/bin/python
import os
import sys

# Fixme: This should be sorted, use a list instead.
additional_symbols = {
    "Alpha":   0x391,
    "Beta":    0x392,
    "Gamma":   0x393,
    "Delta":   0x394,
    "Epsilon": 0x395,
    "Zeta":    0x396,
    "Eta":     0x397,
    "Theta":   0x398,
    "Iota":    0x399,
    "Kappa":   0x39A,
    "Lambda":  0x39B,
    "Mu":      0x39C,
    "Nu":      0x39D,
    "Xi":      0x39E,
    "Omicron": 0x39F,
    "Pi":      0x3A0,
    "Rho":     0x3A1,
    "Sigma":   0x3A3,
    "Tau":     0x3A4,
    "Upsilon": 0x3A5,
    "Phi":     0x3A6,
    "Chi":     0x3A7,
    "Psi":     0x3A8,
    "Omega":   0x3A9,
    "alpha":   0x3B1,
    "beta":    0x3B2,
    "gamma":   0x3B3,
    "delta":   0x3B4,
    "epsilon": 0x3B5,
    "zeta":    0x3B6,
    "eta":     0x3B7,
    "theta":   0x3B8,
    "iota":    0x3B9,
    "kappa":   0x3BA,
    "lambda":  0x3BB,
    "mu":      0x3BC,
    "nu":      0x3BD,
    "xi":      0x3BE,
    "omicron": 0x3BF,
    "pi":      0x3C0,
    "rho":     0x3C1,
    "sigma":   0x3C3,
    "tau":     0x3C4,
    "upsilon": 0x3C5,
    "phi":     0x3C6,
    "chi":     0x3C7,
    "psi":     0x3C8,
    "omega":   0x3C9,
}

symbols = {}
with open('unicode-math-table.tex', 'r') as f:
    for line in f:
        code = int("0x" + line[20:25], 16)
        cmd  = line[28:53].strip()
        symbols[cmd] = code

symbols.update(additional_symbols)

# Write '.../syc/symbols.rs'
import json
with open('symbols.json', 'w') as outfile:
    json.dump(symbols, outfile, indent=4)
