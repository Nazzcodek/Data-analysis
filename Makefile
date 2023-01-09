install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black main.py
	black export.py

lint:
	pylint --disable=R,C main.py
	pylint --disable=R,C export.py

all: install lint test