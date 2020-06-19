GRAMMAR = pyasdl/static/asdl.gram

VENVDIR ?= ./.venv
VENVPYTHON ?= $(VENVDIR)/bin/python

regen: pyasdl/parser.py
	# Note: the unreleased version of pegen requires
	# parser type to generate (c or python) but for now
	# the version on PyPI doesn't require it.
	$(VENVPYTHON) -m pegen -q pyasdl/static/asdl.gram -o pyasdl/parser.py

venv:
	python -m venv $(VENVDIR)
	$(VENVPYTHON) -m pip install .
	$(VENVPYTHON) -m pip install -r requirements-dev.pip
