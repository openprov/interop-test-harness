# Running the interoperability test harness standalone

The instructions have been written with reference to the 64-bit [Ubuntu](http://www.ubuntu.com/) 14.04.2 operating system.

Other operating systems, or versions of these, may differ in how packages are installed, the versions of these packages available from package managers etc. Consult the relevant documentation for your operating system and the products concerned.

Some dependencies require you to have sudo access to install and configure software (or a local system administrator can do this for you).

This page assumes that [pyenv](https://github.com/yyuu/pyenv) is used to manage Python versions.

## Install dependencies

The dependencies required by ProvPy and ProvToolbox must already be installed.

`ubuntu-dependencies.sh` is a simple shell script which both installs these dependencies, including Java and Python (via pyenv).

To run the script:

```
$ sudo apt-get install -y git
$ git clone https://github.com/prov-suite/interop-test-harness
$ source interop-test-harness/ubuntu-dependencies.sh 
```

## Get ProvStore API key

* Log in to [ProvStore](https://provenance.ecs.soton.ac.uk/store)
* Select Account => Developer Area
* You will see your API key

## Get and install the latest version of ProvPy

```
$ git clone https://github.com/trungdong/prov.git ProvPy
$ cd ProvPy
$ python setup.py install
$ ./scripts/prov-convert --version
$ ./scripts/prov-compare --version
$ cd ..
```

## Get and install the latest version of ProvToolbox

```
$ git clone https://github.com/lucmoreau/ProvToolbox.git ProvToolbox
$ cd ProvToolbox
$ mvn clean install
$ ./toolbox/target/appassembler/bin/provconvert -version
$ cd ..
```

## Get the interoperability test cases

```
$ git clone https://github.com/prov-suite/testcases
```

## Get this interoperability test harness

```
$ git clone https://github.com/prov-suite/interop-test-harness
$ cd interop-test-harness
$ pip install -r requirements.txt
```

## Run the test harness unit tests

```
$ nosetests prov_interop/tests
```

## Create local configuration files

Edit ``create_local_config.sh``:

* In the following, replace ``$HOME`` with the paths to where you cloned the repositories.

* Update, if required, location of test cases clone:

```
PROV_TEST_CASES=$HOME/testcases
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
API_KEY="ApiKey user:12345qwert"
```

Create local configuration files:

```
source create_local_config.sh
```

## Run interoperability tests for ProvPy, ProvToolbox, ProvTranslator and ProvStore

```
$ nosetests -v prov_interop.interop_tests
```

To run tests for a specific component:

```
$ nosetests -v prov_interop.interop_tests.test_provpy
$ nosetests -v prov_interop.interop_tests.test_provtoolbox
$ nosetests -v prov_interop.interop_tests.test_provtranslator
$ nosetests -v prov_interop.interop_tests.test_provstore
```

If you are running on a multi-processor machine then the tests can run in parallel, using nosetests' support for [parallel testing](http://nose.readthedocs.org/en/latest/doc_tests/test_multiprocess/multiprocess.html). Specify the number of processes you want to use using a `--processes` flag e.g.

```
$ nosetests --processes=4 -v prov_interop.interop_tests
```
