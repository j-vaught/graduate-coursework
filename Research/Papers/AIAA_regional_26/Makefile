TEMPLATE_DIR := $(CURDIR)/template
export TEXINPUTS := $(TEMPLATE_DIR):$(TEXINPUTS)
export BSTINPUTS := $(TEMPLATE_DIR):$(BSTINPUTS)

PAPERS := cancilla kirk vaught wang

.PHONY: all $(PAPERS) clean

all: $(PAPERS)

cancilla:
	cd Cancilla_ST-DBSCAN && pdflatex -interaction=nonstopmode Cancilla_ST-DBSCAN.tex && pdflatex -interaction=nonstopmode Cancilla_ST-DBSCAN.tex
	cd Cancilla_ST-DBSCAN && rm -f *.aux *.bbl *.blg *.log *.out *.nav *.snm *.toc *.fls *.fdb_latexmk missfont.log

kirk:
	cd Kirk_CFAR_Autotuning && pdflatex -interaction=nonstopmode Kirk_CFAR-Autotuning.tex && pdflatex -interaction=nonstopmode Kirk_CFAR-Autotuning.tex
	cd Kirk_CFAR_Autotuning && rm -f *.aux *.bbl *.blg *.log *.out *.nav *.snm *.toc *.fls *.fdb_latexmk missfont.log

vaught:
	cd Vaught_Synthetic_Radar && pdflatex -interaction=nonstopmode Vaught_Synthetic-Radar.tex && pdflatex -interaction=nonstopmode Vaught_Synthetic-Radar.tex
	cd Vaught_Synthetic_Radar && rm -f *.aux *.bbl *.blg *.log *.out *.nav *.snm *.toc *.fls *.fdb_latexmk missfont.log

wang:
	cd Wang_Active_Acquisition && pdflatex -interaction=nonstopmode Wang_Active-Acquisition.tex && pdflatex -interaction=nonstopmode Wang_Active-Acquisition.tex
	cd Wang_Active_Acquisition && rm -f *.aux *.bbl *.blg *.log *.out *.nav *.snm *.toc *.fls *.fdb_latexmk missfont.log

clean:
	find . -name "*.aux" -o -name "*.bbl" -o -name "*.blg" -o -name "*.log" -o -name "*.out" -o -name "*.nav" -o -name "*.snm" -o -name "*.toc" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "missfont.log" | xargs rm -f
