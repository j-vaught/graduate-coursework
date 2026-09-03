TYPST ?= typst
TYPST_FLAGS ?= --root . --ignore-system-fonts
SOURCE_DATE_EPOCH ?= 0

export SOURCE_DATE_EPOCH

.PHONY: help figure reference-figures specimen-figures homework-figures figures

help:
	@echo "make figure FIGURE=src/ch01/ch01_cs_closed_loop"
	@echo "make reference-figures"
	@echo "make specimen-figures"
	@echo "make homework-figures"
	@echo "make figures"

figure:
	@if [ -z "$(FIGURE)" ]; then \
		echo "FIGURE is required. Example. make figure FIGURE=src/homework/HW02/pendulum"; \
		exit 2; \
	fi; \
	source="$(FIGURE)"; \
	case "$$source" in *.typ) ;; *) source="$$source.typ" ;; esac; \
	if [ ! -f "$$source" ]; then \
		echo "Figure source does not exist. $$source"; \
		exit 2; \
	fi; \
	case "$$source" in \
		src/ch01/*|src/ch02/*) output="generated/$${source#src/}" ;; \
		src/homework/*) output="generated/homework/$${source#src/homework/}" ;; \
		tests/specimens/*) output="generated/specimens/$${source#tests/specimens/}" ;; \
		*) echo "Figure must be under src/ch01, src/ch02, src/homework, or tests/specimens. $$source"; exit 2 ;; \
	esac; \
	output="$${output%.typ}.pdf"; \
	mkdir -p "$$(dirname "$$output")"; \
	$(TYPST) compile $(TYPST_FLAGS) "$$source" "$$output"; \
	echo "Built $$source -> $$output"

reference-figures:
	@find src/ch01 src/ch02 -type f -name '*.typ' -print | sort | while IFS= read -r source; do \
		$(MAKE) --no-print-directory figure FIGURE="$$source" || exit $$?; \
	done

specimen-figures:
	@find tests/specimens -type f -name '*.typ' -print | sort | while IFS= read -r source; do \
		$(MAKE) --no-print-directory figure FIGURE="$$source" || exit $$?; \
	done

homework-figures:
	@find src/homework -type f -name '*.typ' -print | sort | while IFS= read -r source; do \
		$(MAKE) --no-print-directory figure FIGURE="$$source" || exit $$?; \
	done

figures: reference-figures specimen-figures homework-figures
