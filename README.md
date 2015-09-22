# Interoperability Test Harness

[Southampton Provenance Tool Suite](https://provenance.ecs.soton.ac.uk) interoperability test harness framework. This package consists of core classes that are extended by Provenance Tool Suite-specific interoperability test harness packages.

By default, [ProvToolbox](https://github.com/lucmoreau/ProvToolbox) is used as a comparator to validate converted documents.

The test harness runs under Python 2.7+ and Python 3.

[![Build Status](https://travis-ci.org/prov-suite/interop-test-harness.svg)](https://travis-ci.org/prov-suite/interop-test-harness)

---

## Installation

The instructions have been written with reference to the 64-bit [Ubuntu](http://www.ubuntu.com/) 14.04.2 operating system.

Other operating systems, or versions of these, may differ in how packages are istalled, the versions of these packages available from package managers etc. Consult the relevant documentation for your operating system and the products concerned.

Some dependencies require you to have sudo access to install and configure software (or a local system administrator can do this for you).

This page assumes that [pyenv](https://github.com/yyuu/pyenv) is used to manage Python versions.

Install dependencies

* The dependencies required by ProvToolbox must be installed. 
* `ubuntu-dependencies.sh` is a simple shell script which both installs these dependencies, including Java and Python (via pyenv).
* To run the script:

```
$ sudo apt-get install -y git
$ git clone https://github.com/prov-suite/interop-test-harness
$ cd interop-test-harness
$ git checkout package
$ source ubuntu-dependencies.sh 
```

Get and install the latest version of ProvToolbox

```
$ source scripts/install-prov-interop-comparator.sh 
```

Install package

```
$ python setup.py install
```

Run unit tests

```
$ nosetests prov_interop.tests
```

---

## API documentation

To create API documentation in `apidocs/_build/html`:

```
$ pip install sphinx
$ make apidocs
```

---

## Author

Developed by [The Software Sustainability Institute](http://www.software.ac.uk>) and the [Provenance Tool Suite](http://provenance.ecs.soton.ac.uk/) team at [Electronics and Computer Science](http://www.ecs.soton.ac.uk) at the [University of Southampton](http://www.soton.ac.uk).

For more information, see our [document repository](https://github.com/prov-suite/ssi-consultancy/).

---

## License

The code is released under the MIT license.
