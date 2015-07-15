# Interoperability Test Harness

Interoperability test harness for the [Southampton Provenance Suite](https://provenance.ecs.soton.ac.uk).

[![Build Status](https://travis-ci.org/mikej888/provtoolsuite-interop-test-harness.svg)](https://travis-ci.org/mikej888/provtoolsuite-interop-test-harness)

The test harness includes support for:

* [ProvPy](https://github.com/trungdong/prov)
* [ProvToolbox](https://github.com/lucmoreau/ProvToolbox)

The test harness can be run under:

* [Travis CI](https://travis-ci.org). See, for example:
  - ProvPy prov-convert interoperability testing: [GitHub](https://github.com/mikej888/provtoolsuite-provpy-interop-job) and [TravisCI](https://travis-ci.org/mikej888/provtoolsuite-provpy-interop-job)
  - ProvToolbox provconvert interoperability testing: [GitHub](https://github.com/mikej888/provtoolsuite-provtoolbox-interop-job) and [TravisCI](https://travis-ci.org/mikej888/provtoolsuite-provtoolbox-interop-job)
* [Jenkins](https://jenkins-ci.org). See:
  - [Running the interoperability test harness under Jenkins](./Jenkins.md)

## Standalone use

The interoperability test harness runs under Python. You can use the test harness stand-alone. This requires you to have installed all the packages and dependencies required to run both ProvPy and ProvToolbox.

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

Get the PROV test cases:

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

Create ``localconfig.properties``, replacing ``/home/user`` with the paths to where you cloned the repositories:

```
PROV_TEST_CASES_DIR=/home/user/testcases
PROVPY_CONVERT_EXE=python
PROVPY_COMPARE_EXE=python
PROVPY_SCRIPTS_DIR=/home/user/ProvPy/scripts
PROVTOOLBOX_SCRIPTS_DIR=/home/user/toolbox/target/appassembler/bin
PROV_LOCAL_CONFIG_DIR=/home/user/interop-test-harness/localconfig
```

Create custom configuration files:
```
mkdir localconfig
python prov_interop/customise-config.py config localconfig config.properties
```

Run interoperability tests for ProvPy and ProvToolbox:

```
nosetests -v prov_interop.interop_tests.test_provpy
nosetests -v prov_interop.interop_tests.test_provtoolbox
```

## Automatically rerunning interoperability tests in Travis CI

[Travis Client and automatically rerunning interoperability tests](./travis/TravisClient.md) explains how to automatically trigger re-runs of interoperability tests without having to either submit a GitHub pull request on the repository holding the Travis CI configuration file, or going via Travis CI's web interface.

## Author

Developed by [The Software Sustainability Institute](http://www.software.ac.uk>) and the [Provenance Tool Suite](http://provenance.ecs.soton.ac.uk/) team at [Electronics and Computer Science](http://www.ecs.soton.ac.uk) at the [University of Southampton](http://www.soton.ac.uk).

For more information, see our [document repository](https://github.com/prov-suite/ssi-consultancy/).

## License

The code is released under the MIT license.
