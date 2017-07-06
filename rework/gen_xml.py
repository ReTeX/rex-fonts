from fontTools.ttLib import TTFont

def make_xml(font, out):
    font = TTFont(font)
    font.saveXML(out)

if __name__ == "__main__":
    import os
    import sys

    def usage():
        print("usage: gen_xml.py font.otf")
        print("`gen_xml` will convert the font.otf into font.xml")

    if len(sys.argv) < 2:
        usage()
        sys.exit(2)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit(0)

    font = sys.argv[1]
    file, ext = os.path.splitext(font)
    out = file + ".xml"

    print("Generating XML:", out)
    make_xml(font, out)
    print("Finished generating xml.")