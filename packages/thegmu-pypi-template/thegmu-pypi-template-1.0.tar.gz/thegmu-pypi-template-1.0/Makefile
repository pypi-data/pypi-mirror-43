###
# The GMU PyPi Template project Makefile
###

#----------------------------------------------------------------------------------------
### USER REQUIRED CONFIGURATION 

PROJECTNAME:=thegmu-pypi-template
# Python  import statements do not accept dashes, '-', instead change to underscore, '_'.
PROJECTDIR:=thegmu_pypi_template
VENVDIR:=${HOME}/workspace/run/py36_gmupy
PYTHON:=python3.6


#----------------------------------------------------------------------------------------
### DEFAULT CONFIGURATION

### INFORMATION

### FILES/DIRECTORIES
DISTCLEANOBJS:=build dist *.egg-info
DOCSCLEANOBJS:=docs/config.py docs/_build docs/_static docs/_template docs/index.*
TOXCLEANOBJS:=.tox
PYLINTDIRS:=${PROJECTDIR} tests
PEP8FILES:=$(foreach dir,${PYLINTDIRS},$(wildcard $(dir)/*.py))


### COMMANDS
PYTHONVENV:=${PYTHON} -m venv
PYTHONPIP:=${PYTHON} -m pip
VENVACTIVATE:=. ${VENVDIR}/bin/activate
TWINE:=${VENVDIR}/bin/twine

### TARGETS

.PHONY: _default clean clean-dist clean-docs clean-pyc clean-tox dist docs help init pep8 pyling test test-dist

_default: help

${VENVDIR}:
	@echo "${PYTHONVENV} ${VENVDIR}"
	${PYTHONVENV} ${VENVDIR}

clean: clean-pyc clean-tox

clean-dist:
	@echo "Removing package files."
	/bin/rm -rf ${DISTCLEANOBJS}

clean-docs:
	@echo "Removing documentation files."
	/bin/rm -rf ${DOCSCLEANOBJS}

clean-pyc:
	@echo "Removing Python run files."
	for i in $$(find . | grep -E -e"\.pytest_cache|pycache|\.pyc"); do echo $$i; /bin/rm -rf $$i; done

clean-tox: 
	@echo "Removing tox package test files."
	/bin/rm -rf ${TOXCLEANOBJS}

dist: clean-dist requirements
	${VENVACTIVATE}; ${PYTHONPIP} install wheel
	${VENVACTIVATE}; ${PYTHON} setup.py sdist bdist_wheel

docs/config.py:
	${VENVACTIVATE}; ${PYTHONPIP} install sphinx
	${VENVACTIVATE}; cd docs; sphinx-quickstart

docs-init: docs/config.py

docs: requirements
	${VENVACTIVATE}; cd docs; make html

init: requirements

pep8:
	${VENVACTIVATE}; for i in ${PEP8FILES}; do autopep8 -i -a -a -a $$i; done

publish: ${TWINE} dist
	${VENVACTIVATE}; ${TWINE} upload dist/*

publish-test: ${TWINE} dist
	${VENVACTIVATE}; ${TWINE} upload --repository-url https://test.pypi.org/legacy/ dist/*

pylint:
	${VENVACTIVATE}; pylint ${PYLINTDIRS}

requirements: ${VENVDIR} requirements.txt
	${VENVACTIVATE}; ${PYTHONPIP} install --upgrade pip
	${VENVACTIVATE}; ${PYTHONPIP} install --upgrade -r requirements.txt
	${VENVACTIVATE}; ${PYTHONPIP} freeze

tag:
	git tag ${TAG} -m "${MSG}"
	git push --tags

test:
	${VENVACTIVATE}; export PYTHONPATH=${PWD}; pytest --verbose tests

test-dist:
	${VENVACTIVATE}; tox

upgrade: requirements
	${VENVACTIVATE}; ${PYTHONPIP} list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 ${PYTHONPIP} install -U


help:
	/bin/cat README.rst

