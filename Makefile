GRAMMAR = pyasdl/static/asdl.gram

VENVDIR ?= ./.venv
VENVPYTHON ?= $(VENVDIR)/bin/python

regen: pyasdl/parser.py pyasdl/grammar.py
	$(VENVPYTHON) -m pegen -q pyasdl/static/asdl.gram -o pyasdl/parser.py
	$(VENVPYTHON) generators/src/python.py --with-defaults pyasdl/static/grammar.asdl -o pyasdl/grammar.py

venv:
	python -m venv $(VENVDIR)
	$(VENVPYTHON) -m pip install -e .
