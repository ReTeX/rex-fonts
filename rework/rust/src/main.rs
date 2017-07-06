// Read through XML file and do the following:
//  1. Construct a static hashmap for Commands -> Glyphs
//     Source: unicode-math-table.tex, commands.toml
//     - commands.toml will provide additional commands not included
//       in commands.toml.
//     - commands.toml will overwrite any unicode-math-table.tex commands.
//     - commands.toml will provide operator limits context.
//  2. Construct Glyphs information static hashmap.
//     Source: glyph_metrics.json
//  3. Construct Kerning array.
//  4. Construct Variations array.
//  5. Construct Math Constants array.

fn main() {
    println!("Hello, world!");
}
