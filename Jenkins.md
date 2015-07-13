# Running the interoperability test harness under Jenkins

The instructions have been written with reference to the 64-bit [Ubuntu](http://www.ubuntu.com/) 14.04.2 operating system.

Other operating systems, or versions of these, may differ in how packages are installed, the versions of these packages available from package managers etc. Consult the relevant documentation for your operating system and the products concerned.

Some dependencies require you to have sudo access to install and configure software (or a local system administrator can do this for you).

This page assumes that [pyenv](https://github.com/yyuu/pyenv) is used to manage Python versions.


## Install dependencies

The dependencies required by ProvPy and ProvToolbox must already be installed. Jenkins runs under the same version of Java as used for ProvToolbox.

[ubuntu-dependencies.sh](./jenkins/ubuntu-dependencies.sh) is a simple shell script which both installs these dependencies, including Java and Python (via pyenv)
as well as downloading Jenkins. 

To run the script:

```
sudo apt-get install -y git
git clone https://github.com/prov-suite/interop-test-harness
source interop-test-harness/jenkins/ubuntu-dependencies.sh 
```

## Install Jenkins

[Jenkins](https://jenkins-ci.org/) is available as an executable Java archive. If you ran the script above then you will already have ``jenkins.war``, otherwise, run:

```
wget http://mirrors.jenkins-ci.org/war/latest/jenkins.war
```

To start Jenkins, run:

```
java -jar jenkins.war
```

* Open a web browser and go to to http://localhost:8080

## Install workspace cleanup plugin

Jenkins uses a "workspace" directory to store any build artefacts. This plugin allows jobs to be configured to clear this directory between build runs.

* Click Manage Jenkins
* Click Manage Plugins
* Click Available tab
* Filter: workspace cleanup
* Check Workspace Cleanup Plugin
* Click Install without restart
* Click go back to top page

## Create job to run interoperability tests

These steps create a Jenkins job to run the interoperability tests. If you do not want to execute these manually, there is one we have prepared earlier in [config.xml](./jenkins/config.xml) - to use this see "Importing a Jenkins job" below.

* Click create new jobs
* Item name: PTS
* Select freestyle project
* Click OK

* Source Code Management: None (for now)
* Build Triggers: leave unchecked (for now)
* Check Build Environment Delete workspace before build starts
* Select Add build step => Execute shell
* Enter:

```
git clone https://github.com/prov-suite/testcases testcases
```

* Select Add build step => Execute shell
* Enter:

```
git clone https://github.com/lucmoreau/ProvToolbox.git ProvToolbox
cd ProvToolbox
mvn clean install
./toolbox/target/appassembler/bin/provconvert -version
```

* Select Add build step => Execute shell
* Enter:

```
pyenv local 2.7.6
git clone https://github.com/trungdong/prov ProvPy
cd ProvPy
git checkout 1.3.2
python setup.py install
./scripts/prov-convert --version
```

* Select Add build step => Execute shell
* Enter:

```
pyenv local 2.7.6
git clone https://github.com/prov-suite/interop-test-harness test-harness
cd test-harness
pip install -r requirements.txt
```

* Select Add build step => Execute shell
* Enter:

```
cd test-harness
echo "PROV_TEST_CASES_DIR=$WORKSPACE/testcases" > config.properties
echo "PROVPY_SCRIPTS_DIR=$WORKSPACE/ProvPy/scripts" >> config.properties
echo "PROVPY_CONVERT_EXE=python" >> config.properties
echo "PROVPY_COMPARE_EXE=python" >> config.properties
echo "PROVTOOLBOX_SCRIPTS_DIR=$WORKSPACE/ProvToolbox/toolbox/target/appassembler/bin" >> config.properties
echo "PROV_LOCAL_CONFIG_DIR=$WORKSPACE/test-harness/localconfig" >> config.properties
cat config.properties
mkdir localconfig
python prov_interop/customise-config.py config localconfig config.properties
cat localconfig/*
```

* Enter:
* The above Execute shell steps can, alternatively, be done within a single Execute shell entry
* Select Add build step => Execute shell

```
cd test-harness
nosetests -v --with-xunit prov_interop.interop_tests
```

* Click Save
* Project PTS page appears
* Click Build Now
* Click #NNNN build number
* Build #NNNN page appears
* Click Console Output

## Publish xUnit test results

nosetests, with the ``--with-xunit`` option set, outputs test results in xUnit-compliant XML. By default, this file is called nosetests.xml. Jenkins can parse and present this informationy.

* Go to Project PTS page
* Click Configure
* Scroll down to Post-build Action
* Select Add post-build action => Publish JUnit test result report
* Test report XMLs: test-harness/nosetests.xml.
  - If you get a warning that nosetests.xml doesn't match anything you can ignore this as the file hasn't been created yet
* Click Save
* Click Build Now
* Click #NNNN build number
* Build #NNNN page appears

## View nosetests test results

You can browse the nosetests test results. These are hierarchically organised by Python module, class and method name.

* EITHER On the Project PTS page
  - Click the Latest Test Result link
  - If all went well, should say (no failures)
* OR On the Jenkins dashboard/front-page
  - Hover over the build number #NNNN
  - Click drop-down arrow
  - Select Test Result
* Click Python package names to browse down to test classes
  - prov_interop.interop_tests.test_provpy
  - prov_interop.interop_tests.test_provtoolbox
* Click Python class names to browse down to test functions
  - ProvPyTestCase
  - ProvToolboxTestCase

## Start builds manually

* EITHER On the Project PTS page
  - Click Build Now
* OR On the Jenkins dashboard/front-page
  - Click green "run" icon
* Click #NNNN build number
* Build #NNNN page appears
* Click Console Output to see commands being run by Jenkins

## Importing a Jenkins job

[config.xml](./jenkins/config.xml) contains the Jenkins configuration file for the job written following the above instructions. Assuming you have already done:

* Install dependencies
* Install Jenkins
* Install workspace cleanup plugin

You can import this into Jenkins as follows:

```
mkdir $HOME/.jenkins/jobs/PTS/
cp jenkins/config.xml $HOME/.jenkins/jobs/PTS/
```

On the Jenkins dashboard:

* Click Manage Jenkins
* Click Reload configuration from disk
* You should see PTS
* Click green "run" icon

## Jenkins directories

Jenkins stores its files in `$HOME/.jenkins`.

Jenkins does the build in job-specific workspace directory, `.jenkins/workspace/JOB`, e.g. `.jenkins/workspace/PTS/`.

Jenkins job configuration, ``config.xml``, and logs and xUnit test results from all the builds are stored in a job-specific jobs directory, `.jenkins/jobs/JOB`, e.g. `.jenkins/jobs/PTS/`.
