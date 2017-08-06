## Modifying fonts for ReX

This assumes that the font is an OpenType math font with a Math table.

- Run `python3 rexify.py` on the font.  This will:
  - Place inacessible glyphs in a CMAP table.
  - Generate glyph metrics for each glyph required for ReX.

- Open FontForge, and re-encode to ISO 10646-1 (Unicode, Full).  This will
  modify the glyph indices, optimzing the CMAP tables.

- Do codegen.

## Open issues

Some work that sitll needs to be done:
- Generate a whitelist of symbols needed for ReX.  This would require 
  keeping track of all the glyphs required in the variants table.
