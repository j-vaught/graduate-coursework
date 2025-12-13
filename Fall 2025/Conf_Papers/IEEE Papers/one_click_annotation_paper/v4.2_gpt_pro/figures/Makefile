LATEXMK ?= latexmk
LATEXMKFLAGS ?= -pdf -interaction=nonstopmode

FIG08_TEX := \
	fig08_temporal_coverage.tex \
	fig08_temporal_coverage_aggregated.tex \
	fig08_temporal_coverage_matplotlib.tex \
	fig08_temporal_heatmap_pgfplots.tex \
	fig08_temporal_aggregates_pgfplots.tex

.PHONY: fig08 clean

fig08: $(FIG08_TEX:.tex=.pdf)

%.pdf: %.tex
	$(LATEXMK) $(LATEXMKFLAGS) $<

clean:
	$(LATEXMK) -C
