###
# The GMU PyPi Template project Makefile
###

#----------------------------------------------------------------------------------------
### USER REQUIRED CONFIGURATION 

# Activate a configuration in bin:
# Example . bin/activate-fun-stuff


#----------------------------------------------------------------------------------------
### DEFAULT CONFIGURATION

### INFORMATION

### FILES/DIRECTORIES
DISTCLEANOBJS:=build dist *.egg-info
DOCSCLEANOBJS:=docs/config.py docs/_build docs/_static docs/_template docs/index.*
TOXCLEANOBJS:=.tox
PYLINTDIRS:=${PYPIPROJECTDIRBASENAME} tests
PEP8FILES:=$(foreach dir,${PYLINTDIRS},$(wildcard $(dir)/*.py))
VENVACTIVATEFILE:=${PYPIVENVDIR}/bin/activate

### COMMANDS
VENVPYTHONVENV:=${PYPIVENVPYTHON} -m venv
VENVPYTHONPIP:=${PYPIVENVPYTHON} -m pip
VENVACTIVATE:=. ${VENVACTIVATEFILE}
TWINE:=${PYPIVENVDIR}/bin/twine

### TARGETS

.PHONY: _default _require_activation clean clean-dist clean-docs clean-pyc clean-tox deactivate dist docs help init pep8 project-init publish publish-test pylint test test-dist tox-init

_default: help

_require_activation:
ifeq (${PYPIPROJECTNAME},)
	@echo ""
	@echo "$@ FAILED: activate the PYPI environment before running 'make'."
	@echo ""
	@echo "Sample PYPI environment installed thegmu-pypi-template:"
	@echo ""
	@echo ". bin/activate-fun-stuff"
	@echo ""
	@false
endif


${VENVDIR}: _require_activation
	@echo "${VENVPYTHONVENV} ${VENVDIR}"
	${VENVPYTHONVENV} ${VENVDIR}

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

deactivate:
	@echo ""
	@echo "It is not possible to deactivate within the Makefile itself."
	@echo ""
	@echo "To decactivate then source the deactivate-pypi shell script."
	@echo ""
	@echo ". bin/deactivate-pypi"
	@echo ""

dist: _require_activation clean-dist requirements
	${VENVACTIVATE}; ${VENVPYTHONPIP} install wheel
	${VENVACTIVATE}; ${PYPIVENVPYTHON} setup.py sdist bdist_wheel

docs/config.py: _require_activation
	${VENVACTIVATE}; ${VENVPYTHONPIP} install sphinx
	${VENVACTIVATE}; cd docs; sphinx-quickstart

docs-init: docs/config.py

docs: requirements _require_activation
	${VENVACTIVATE}; cd docs; make html

init: requirements project-init

pep8: _require_activation
	${VENVACTIVATE}; for i in ${PEP8FILES}; do autopep8 -i -a -a -a $$i; done

project-init: _require_activation tox-init
	@echo "Moving project directory"
	@if [ -d "${PYPIPROJECTDIRBASENAME}" ]; then echo "${PYPIPROJECTDIRBASENAME} already exists."; else mv thegmu_pypi_template ${PYPIPROJECTDIRBASENAME}; echo "${PYPIPROJECTDIRBASENAME} created"; fi
	@echo ""
	@echo "Setting 'SCRIPTS' in setup.py to empty."
	@if grep -q '^SCRIPTS = \[\] ' setup.py; then echo "SCRIPTS already disabled." ; else sed -i 's/^SCRIPTS =.*/SCRIPTS = \[\]/g' setup.py; fi
	@echo "Setting 'NAME' in setup.py to ${PYPIPROJECTNAME}."
	@sed -i 's/^NAME =.*/NAME = \"${PYPIPROJECTNAME}\"/g' setup.py; fi
	@echo "Setting AUTHOR, AUTHOR_EMAIL, DESCRIPTION, and URL blank in setup.py"
	@sed -i 's/^AUTHOR =.*/AUTHOR = \"\"/g' setup.py; fi
	@sed -i 's/^AUTHOR_EMAIL =.*/AUTHOR_EMAIL = \"\"/g' setup.py; fi
	@sed -i 's/^DESCRIPTION =.*/DESCRIPTION = \"\"/g' setup.py; fi
	@sed -i 's/^URL =.*/URL = \"\"/g' setup.py; fi
	@echo ""
	@echo "Updating tests/sample.py with this project name for import."
	@sed -ir 's/from .*/from ${PYPIPROJECTDIRBASENAME}.sample import Sample/g' tests/sample_test.py
	@grep 'from ' tests/sample_test.py
	@echo ""

publish: _require_activation ${TWINE} dist
	${VENVACTIVATE}; ${TWINE} upload dist/*

publish-test: _require_activation ${TWINE} dist
	${VENVACTIVATE}; ${TWINE} upload --repository-url https://test.pypi.org/legacy/ dist/*

pylint: _require_activation
	${VENVACTIVATE}; pylint ${PYLINTDIRS}

requirements: _require_activation ${VENVDIR} requirements.txt
	${VENVACTIVATE}; ${VENVPYTHONPIP} install --upgrade pip
	${VENVACTIVATE}; ${VENVPYTHONPIP} install --upgrade -r requirements.txt
	${VENVACTIVATE}; ${VENVPYTHONPIP} freeze

tag:
	git tag ${TAG} -m "${MSG}"
	git push --tags

test: _require_activation
	${VENVACTIVATE}; export PYTHONPATH=${PWD}; pytest --verbose tests

test-dist: _require_activation
	${VENVACTIVATE}; tox

tox-init: _require_activation
	@echo "Updating tox.ini, envlist."
	@sed -i 's/envlist .*/envlist = ${PYPIVENVTOXLIST}/g' tox.ini
	@grep -H envlist tox.ini
	@echo ""

upgrade: _require_activation requirements
	${VENVACTIVATE}; ${VENVPYTHONPIP} list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 ${VENVPYTHONPIP} install -U


help:
	/bin/cat README.rst

