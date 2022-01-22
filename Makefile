GRAMMAR = pyasdl/static/asdl.gram

VENVDIR ?= ./.venv
VENVPYTHON ?= $(VENVDIR)/bin/python

regen: pyasdl/parser.py pyasdl/grammar.py
	# Note: the unreleased version of pegen requires
	# parser type to generate (c or python) but for now
	# the version on PyPI doesn't require it.
	$(VENVPYTHON) -m pegen -q pyasdl/static/asdl.gram -o pyasdl/parser.py
	sed -i 's/pegen/pyasdl.__pegen/g' pyasdl/parser.py
	$(VENVPYTHON) generators/src/python.py --with-defaults pyasdl/static/grammar.asdl -o pyasdl/grammar.py

venv:
	python -m venv $(VENVDIR)
	$(VENVPYTHON) -m pip install -e .
	$(VENVPYTHON) -m pip install -r requirements.pip
