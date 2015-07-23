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

## Running under Travis CI

The test harness can be run under [Travis CI](https://travis-ci.org). See, for example, the following repositories, each of which contain a Travis CI test job to run interoperability tests for each component above:

| Component | Travis CI job repository | Travis CI job | Build status |
| --------- | ------------------------ | ------------- | ------------ |
| ProvPy prov-convert | [GitHub](https://github.com/prov-suite/provpy-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provpy-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provpy-interop-job.svg)](https://travis-ci.org/prov-suite/provpy-interop-job) |
| ProvToolbox provconvert | [GitHub](https://github.com/prov-suite/provtoolbox-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provtoolbox-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provtoolbox-interop-job.svg)](https://travis-ci.org/prov-suite/provtoolbox-interop-job) |
| ProvTranslator | [GitHub](https://github.com/prov-suite/provtranslator-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provtranslator-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provtranslator-interop-job.svg)](https://travis-ci.org/prov-suite/provtranslator-interop-job) |
| ProvStore | [GitHub](https://github.com/prov-suite/provstore-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provstore-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provstore-interop-job.svg)](https://travis-ci.org/prov-suite/provstore-interop-job) |

Here we have set up one repository per component so we can have one test job per component. There is no reason, though, why a single test job cannot run all the tests for all the components, to reduce the number of repositories needed.

The test harness also includes unit tests for the harness itself - these are tested under Travis CI using a job configuration file within this repository.

### ProvStore jobs and API keys

Running ProvStore tests require you to:

* Create a ProvStore API Key:
  - Log in to [ProvStore](https://provenance.ecs.soton.ac.uk/
store)
  - Select Account => Developer Area
  - You will see your API key

* Define a Travis CI variable, `PROVSTORE_API_KEY` holding your ProvStore user name and API key:

* Visit your job's settings page in Travis CI
* Select settings
* Click Environment Variables
* Click Add a new variable
* Name: `PROVSTORE_API_KEY`
* Value: `user:qwert12345`
* Ensure Display value in build logs is *not* selected

See [define variables in repository settings](http://docs.travis-ci.com/user/environment-variables/#Defining-Variables-in-Repository-Settings).

## Running under Jenkins

[Jenkins](https://jenkins-ci.org) is a popular, open source continuous integration server that runs under Java.

See [Running the interoperability test harness under Jenkins](./Jenkins.md) which includes an example of running all the interoperability tests from within a single job.

## Running standalone

The interoperability test harness runs under Python. The test harness can be run stand-alone. These instructions assume you have:

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

Edit ``create_local_config.sh``:

* In the following, replace ``$HOME`` with the paths to where you cloned the repositories.

* Update, if required, location of test cases clone:

```
PROV_TEST_CASES=$HOME/provtoolsuite-testcases
```

* Update, if required, location of ProvPy scripts:

```
PROVPY_COMPARE="python $HOME/ProvPy/scripts/prov-compare"
PROVPY_CONVERT="python $HOME/ProvPy/scripts/prov-convert"
```

* Update, if required, location of ProvToolbox provconvert script:

```
PROVTOOLBOX_CONVERT=$HOME/ProvToolbox/toolbox/target/appassembler/bin/provconvert
```

* Update ProvStore API key, to use yours:

```
API_KEY="ApiKey you:12345qwert"
```

Create custom configuration files:

```
source create_local_config.sh
```

Run test harness unit tests:

```
nosetests -v prov_interop/tests
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

[Travis Client](./travis/TravisClient.md) explains how to automatically trigger re-runs of interoperability tests without having to either submit a GitHub pull request on the repository holding the Travis CI configuration file, or going via Travis CI's web interface.

## Author

Developed by [The Software Sustainability Institute](http://www.software.ac.uk>) and the [Provenance Tool Suite](http://provenance.ecs.soton.ac.uk/) team at [Electronics and Computer Science](http://www.ecs.soton.ac.uk) at the [University of Southampton](http://www.soton.ac.uk).

For more information, see our [document repository](https://github.com/prov-suite/ssi-consultancy/).

## License

The code is released under the MIT license.
