.PHONY: smoke test figures verify paper reproduce

smoke:
	python scripts/smoke_test.py

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

figures:
	python scripts/generate_figures.py

verify:
	python scripts/verify_integrity.py

paper:
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd paper && bibtex main
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex

reproduce:
	python scripts/reproduce_all.py
