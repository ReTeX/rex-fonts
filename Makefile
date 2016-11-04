FONT_FOLDER := master
FONTS := $(wildcard $(FONT_FOLDER)/*.otf)

.PHONY: all ${FONTS}
all: ${FONTS}; 
	@echo "Finished compiling fonts."

${FONTS}: %:;
	@echo "Rexifying $*"
	@python make-rex-font.py $*
	$(eval $*REX := $(notdir $*))
	@echo "Making symbols and offset table for $*"
	@python make-symbols.py out/rex-$($*REX)
	@echo "Making glyphs table for $*"
	@python make-glyphs.py out/rex-$($*REX)
	@echo "Making constants table for $*"
	@python make-constants.py $*
