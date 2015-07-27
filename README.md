# Interoperability Test Harness

Interoperability test harness for the [Southampton Provenance Suite](https://provenance.ecs.soton.ac.uk).

The test harness includes support for:

* Software:
  - [ProvPy](https://github.com/trungdong/prov)
  - [ProvToolbox](https://github.com/lucmoreau/ProvToolbox)
* Services:
  - [ProvTranslator](https://provenance.ecs.soton.ac.uk/validator/view/translator.html)
  - [ProvStore](https://provenance.ecs.soton.ac.uk/store/)

The test harness runs under Python 2.7+ and Python 3.

[![Build Status](https://travis-ci.org/prov-suite/interop-test-harness.svg)](https://travis-ci.org/prov-suite/interop-test-harness)

## Running under Travis CI

The test harness can be run under [Travis CI](https://travis-ci.org). See, for example, the following repositories, each of which contain a Travis CI test job to run interoperability tests for each component above:

| Component | Travis CI job repository | Travis CI job | Build status |
| --------- | ------------------------ | ------------- | ------------ |
| ProvPy prov-convert | [GitHub](https://github.com/prov-suite/provpy-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provpy-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provpy-interop-job.svg)](https://travis-ci.org/prov-suite/provpy-interop-job) |
| ProvToolbox provconvert | [GitHub](https://github.com/prov-suite/provtoolbox-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provtoolbox-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provtoolbox-interop-job.svg)](https://travis-ci.org/prov-suite/provtoolbox-interop-job) |
| ProvTranslator | [GitHub](https://github.com/prov-suite/provtranslator-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provtranslator-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provtranslator-interop-job.svg)](https://travis-ci.org/prov-suite/provtranslator-interop-job) |
| ProvStore | [GitHub](https://github.com/prov-suite/provstore-interop-job) | [TravisCI](https://travis-ci.org/prov-suite/provstore-interop-job) | [![Build Status](https://travis-ci.org/prov-suite/provstore-interop-job.svg)](https://travis-ci.org/prov-suite/provstore-interop-job) |

Here we have set up one repository per component so we can have one test job per component. There is no reason, though, why a single test job cannot run all the tests for all the components, to reduce the number of repositories needed.

Running the interoperability tests under Travis CI require you to:

* Create a ProvStore API Key:
  - Log in to [ProvStore](https://provenance.ecs.soton.ac.uk/store)
  - Select Account => Developer Area
  - You will see your API key
* Define a Travis CI variable, `PROVSTORE_API_KEY` holding your ProvStore user name and API key:
  - Visit your job's settings page in Travis CI
  - Select settings
  - Click Environment Variables
  - Click Add a new variable
  - Name: `PROVSTORE_API_KEY`
  - Value: `user:qwert12345`
  - Ensure Display value in build logs is *not* selected
  - See [define variables in repository settings](http://docs.travis-ci.com/user/environment-variables/#Defining-Variables-in-Repository-Settings).

## Automatically rerunning interoperability tests in Travis CI

[Travis Client](./travis/TravisClient.md) explains how to automatically trigger re-runs of interoperability tests without having to either submit a GitHub pull request on the repository holding the Travis CI configuration file, or going via Travis CI's web interface.

## Running under Jenkins

[Jenkins](https://jenkins-ci.org) is a popular, open source continuous integration server that runs under Java. See [Running the interoperability test harness under Jenkins](./Jenkins.md) which includes an example of running all the interoperability tests from within a single Jenkins job.

## Running standalone

The test harness can be run stand-alone. See [Running the interoperability test harness standalone](./Standalone.md).

## Interoperability test harness unit tests

The interoperability test harness includes unit tests for the harness itself. This respository contains a TravisCI, .travis.yml, job configuration file to run these unit tests.

## Author

Developed by [The Software Sustainability Institute](http://www.software.ac.uk>) and the [Provenance Tool Suite](http://provenance.ecs.soton.ac.uk/) team at [Electronics and Computer Science](http://www.ecs.soton.ac.uk) at the [University of Southampton](http://www.soton.ac.uk).

For more information, see our [document repository](https://github.com/prov-suite/ssi-consultancy/).

## License

The code is released under the MIT license.
