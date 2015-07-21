# Interoperability Test Harness

Interoperability test harness for the [Southampton Provenance Suite](https://provenance.ecs.soton.ac.uk).

[![Build Status](https://travis-ci.org/prov-suite/interop-test-harness.svg)](https://travis-ci.org/prov-suite/interop-test-harness)

The test harness includes support for:

* Software:
  - [ProvPy](https://github.com/trungdong/prov)
  - [ProvToolbox](https://github.com/lucmoreau/ProvToolbox)
* Services:
  - [ProvTranslator](https://provenance.ecs.soton.ac.uk/validator/view/translator.html)
  - [ProvStore](https://provenance.ecs.soton.ac.uk/store/)

The test harness can be run under:

* [Travis CI](https://travis-ci.org). See, for example:
  - ProvPy prov-convert interoperability testing: [GitHub](https://github.com/prov-suite/provpy-interop-job) and [TravisCI](https://travis-ci.org/prov-suite/provpy-interop-job)
  - ProvToolbox provconvert interoperability testing: [GitHub](https://github.com/prov-suite/provtoolbox-interop-job) and [TravisCI](https://travis-ci.org/prov-suite/provtoolbox-interop-job)
  - ProvTranslator interoperability testing: [GitHub](https://github.com/prov-suite/provtranslator-interop-job) and [TravisCI](https://travis-ci.org/prov-suite/provtranslator-interop-job)
* [Jenkins](https://jenkins-ci.org). See:
  - [Running the interoperability test harness under Jenkins](./Jenkins.md)

## Standalone use

The interoperability test harness runs under Python. You can use the test harness stand-alone. These instructions assume you have:

* Installed ProvPy's dependencies.
* Installed ProvToolbox's dependencies.
* Created a ProvStore API Key:
  - Log in to [ProvStore](https://provenance.ecs.soton.ac.uk/store)
  - Select Account => Developer Area
  - You will see your API key

Get and install the latest version of ProvPy:

```
git clone https://github.com/trungdong/prov.git ProvPy
cd ProvPy
python setup.py install
./scripts/prov-convert --version
./scripts/prov-compare --version
cd ..
```

Get and install the latest version of ProvToolbox:

```
git clone https://github.com/lucmoreau/ProvToolbox.git ProvToolbox
cd ProvToolbox
mvn clean install
./toolbox/target/appassembler/bin/provconvert -version
cd ..
```

Get the interoperability test cases:

```
git clone https://github.com/prov-suite/testcases
```

Get this interoperability test harness:

```
git clone https://github.com/prov-suite/interop-test-harness
cd interop-test-harness
pip install -r requirements.txt
```

Run the test harness unit tests:

```
nosetests prov_interop/tests
```

Create ``localconfig.properties``:

* In the following, replace ``/home/user`` with the paths to where you cloned the repositories.
* Add location of test cases clone:

```
PROV_TEST_CASES_DIR=/home/user/testcases
```

* Add location of a directory that will hold local configuration files e.g.

```
PROV_LOCAL_CONFIG_DIR=/home/user/interop-test-harness/localconfig
```

* Add location of ProvPy scripts:

```
PROVPY_SCRIPTS_DIR=/home/user/ProvPy/scripts
```

* Add ProvPy prov-compare executable name:

```
PROVPY_COMPARE_EXE=python
```

* Add ProvPy prov-convert executable name:

```
PROVPY_CONVERT_EXE=python
```

* Add location of ProvToolbox provconvert script:

```
PROVTOOLBOX_SCRIPTS_DIR=/home/user/toolbox/target/appassembler/bin
```

* Add your ProvStore API key:

```
API_KEY=you:12345qwert
```

Create custom configuration files:

```
mkdir localconfig
python prov_interop/customise-config.py config localconfig config.properties
```

Run interoperability tests for ProvPy, ProvToolbox, ProvTranslator and ProvStore:

```
nosetests -v prov_interop.interop_tests
```

To run tests for a specific component:

```
nosetests -v prov_interop.interop_tests.test_provpy
nosetests -v prov_interop.interop_tests.test_provtoolbox
nosetests -v prov_interop.interop_tests.test_provtranslator
nosetests -v prov_interop.interop_tests.test_provstore
```

## Automatically rerunning interoperability tests in Travis CI

[Travis Client and automatically rerunning interoperability tests](./travis/TravisClient.md) explains how to automatically trigger re-runs of interoperability tests without having to either submit a GitHub pull request on the repository holding the Travis CI configuration file, or going via Travis CI's web interface.

## Author

Developed by [The Software Sustainability Institute](http://www.software.ac.uk>) and the [Provenance Tool Suite](http://provenance.ecs.soton.ac.uk/) team at [Electronics and Computer Science](http://www.ecs.soton.ac.uk) at the [University of Southampton](http://www.soton.ac.uk).

For more information, see our [document repository](https://github.com/prov-suite/ssi-consultancy/).

## License

The code is released under the MIT license.
