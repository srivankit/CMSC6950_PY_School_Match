report: report.tex allocation.pdf StudentApplication.png
	latexmk -pdf report.tex

allocation.pdf: data/schools.csv data/students.csv py-school-match.py
	python3 py-school-match.py
StudentApplication.png: data/schools.csv data/students.csv
	python3 studentapp.py

data/schools.csv: mkdir.data 
	cd data && wget -N https://raw.githubusercontent.com/srivankit/py-school-match-data/master/schools.csv

data/students.csv: mkdir.data
	cd data && wget -N https://raw.githubusercontent.com/srivankit/py-school-match-data/master/students.csv
mkdir.data:
	if [ ! -d "data" ]; then mkdir data ; fi

.PHONY: clean

clean:
	latexmk -c
