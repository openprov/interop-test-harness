.PHONY: help
help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "apidocs - generate Sphinx HTML API documentation"

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: apidocs
apidocs:
	rm -f apidocs/prov_interop.rst
	rm -f prov_interop.interop_tests.rst
	rm -f prov_interop.provpy.rst
	rm -f prov_interop.provstore.rst
	rm -f prov_interop.provtoolbox.rst
	rm -f prov_interop.provtranslator.rst
	rm -f prov_interop.rst
	rm -f prov_interop.tests.provpy.rst
	rm -f prov_interop.tests.provstore.rst
	rm -f prov_interop.tests.provtoolbox.rst
	rm -f prov_interop.tests.provtranslator.rst
	rm -f prov_interop.tests.rst
	rm -f apidocs/modules.rst
	rm -rf apidocs/_build
	sphinx-apidoc -o apidocs/ prov_interop
	$(MAKE) -C apidocs clean
	$(MAKE) -C apidocs html
