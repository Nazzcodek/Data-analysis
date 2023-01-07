install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black main.py

lint:
	pylint --disable=R,C main.py

all: install lint test