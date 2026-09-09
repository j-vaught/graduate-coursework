TYPST ?= typst
TYPST_FLAGS ?= --ignore-system-fonts
SOURCE_DATE_EPOCH ?= 0
PALETTE ?= homework
OUTPUT_DIR ?= generated

export SOURCE_DATE_EPOCH

.PHONY: all figure

all:
	@find src -type f -name '*.typ' -print | sort | while IFS= read -r source; do \
		$(MAKE) --no-print-directory figure FIGURE="$$source" || exit $$?; \
	done

figure:
	@set -eu; \
	source="$(FIGURE)"; \
	case "$$source" in src/*.typ) ;; src/*) source="$$source.typ" ;; *) echo "Use FIGURE=src/figure-name"; exit 2 ;; esac; \
	test -f "$$source"; \
	output="$(OUTPUT_DIR)/$${source#src/}"; \
	output="$${output%.typ}.pdf"; \
	mkdir -p "$$(dirname "$$output")"; \
	$(TYPST) compile --root ../.. $(TYPST_FLAGS) --input palette=$(PALETTE) "$$source" "$$output"
