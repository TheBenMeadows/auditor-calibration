PYTHON ?= python3
TEX ?= tectonic

.PHONY: reproduce check paper provenance

# Recompute the analysis from the raw run rows, regenerate every number and
# table the paper prints, and fail if any of them differs from the committed copy.
reproduce:
	$(PYTHON) -I scripts/analyze-p1.py
	$(PYTHON) -I scripts/paper-numbers.py
	$(MAKE) check

check:
	git diff --exit-code -- paper/numbers.tex paper/tables

provenance:
	$(PYTHON) -I scripts/run-provenance.py

paper:
	cd paper && $(TEX) main.tex
