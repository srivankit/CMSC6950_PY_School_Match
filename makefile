report: report.tex allocation.pdf
	latexmk  -pdf report.tex

allocation.pdf: data/schools.csv data/students.csv py-school-match.py
	python3 py-school-match.py

data/schools.csv: 
	cd data && wget https://raw.githubusercontent.com/srivankit/py-school-match-data/master/schools.csv

data/students.csv:
	cd data && wget https://raw.githubusercontent.com/srivankit/py-school-match-data/master/students.csv


.PHONY: clean almost_clean

clean: almost_clean
	rm report.pdf
	rm plot.pdf

almost_clean:
	latexmk -c
