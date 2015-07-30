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

[Travis Client](./docs/TravisClient.md) explains how to automatically trigger re-runs of interoperability tests without having to either submit a GitHub pull request on the repository holding the Travis CI configuration file, or going via Travis CI's web interface.

## Running under Jenkins

[Jenkins](https://jenkins-ci.org) is a popular, open source continuous integration server that runs under Java. See [Running the interoperability test harness under Jenkins](./docs/Jenkins.md) which includes an example of running all the interoperability tests from within a single Jenkins job.

## Running standalone

The test harness can be run stand-alone. See [Running the interoperability test harness standalone](./docs/Standalone.md).

## Writing test jobs

There are a number of options for what versions of tools and services are tested. For example:

* ProvPy
  - pip package
  - GitHub repository stable branch (e.g. 1.3.2)
  - GitHub repository latest version (e.g. master)
  - Running under Python 2.7 or Python 3.4
* ProvToolbox:
  - GitHub repository stable branch (i.e. master)
  - GitHub repository stable branch source code ZIP
  - Maven binary release ZIP
  - rpm package
* ProvStore
  - Live, public service.
  - Development version of service hosted locally.
* ProvTranslator
  - Live, public service.
  - Development version of service hosted locally.

Likewise, it is possible to run the interoperability tests for these tools and services as either a single test job (as the Jenkins example does) or as multiple test jobs (as the Travis CI examples do).

What combination of options is used is purely a configuration issue, relating to how the Travis CI or Jenkins jobs are written and how the test harness is configured (e.g. whether it uses `prov-convert` or `python ProvPy/scripts/prov-convert`, or a public or private service URL).

It is possible (and, indeed, desirable) to set up a Travis CI or Jenkins job for each component to be tested, deploying it and any required comparators, so the test dashboards shows the status of the interoperability testing for that component alone, rather than the status of the tests across all components. 

## Interoperability test harness unit tests

The interoperability test harness includes unit tests for the harness itself. This respository contains a TravisCI, .travis.yml, job configuration file to run these unit tests.

## Design and implementation

For details, see [Interoperability test harness design and implementation](./docs/Design.md).

## API documentation

To create API documentation in `apidocs/_build/html`:

```
$ pip install sphinx
$ make apidocs
```

## Author

Developed by [The Software Sustainability Institute](http://www.software.ac.uk>) and the [Provenance Tool Suite](http://provenance.ecs.soton.ac.uk/) team at [Electronics and Computer Science](http://www.ecs.soton.ac.uk) at the [University of Southampton](http://www.soton.ac.uk).

For more information, see our [document repository](https://github.com/prov-suite/ssi-consultancy/).

## License

The code is released under the MIT license.
