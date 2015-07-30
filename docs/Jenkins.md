# Running the interoperability test harness under Jenkins

The instructions have been written with reference to the 64-bit [Ubuntu](http://www.ubuntu.com/) 14.04.2 operating system.

Other operating systems, or versions of these, may differ in how packages are installed, the versions of these packages available from package managers etc. Consult the relevant documentation for your operating system and the products concerned.

Some dependencies require you to have sudo access to install and configure software (or a local system administrator can do this for you).

This page assumes that [pyenv](https://github.com/yyuu/pyenv) is used to manage Python versions.

## Install dependencies

The dependencies required by ProvPy and ProvToolbox must already be installed. Jenkins runs under the same version of Java as used for ProvToolbox.

`ubuntu-dependencies.sh` is a simple shell script which both installs these dependencies, including Java and Python (via pyenv) as well as downloading Jenkins. 

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

## Install Jenkins

[Jenkins](https://jenkins-ci.org/) is available as an executable Java archive. If you ran the script above then you will already have ``jenkins.war``, otherwise, run:

```
$ wget http://mirrors.jenkins-ci.org/war/latest/jenkins.war
```

To start Jenkins, run:

```
$ java -jar jenkins.war
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

These steps create a Jenkins job to run the interoperability tests. If you do not want to execute these manually, there is one we have prepared earlier in `jenkins/config-interop.xml` - to use this see "Importing a Jenkins job" below.

* Click create new jobs
* Item name: PTS-Interop
* Select freestyle project
* Click OK

Set build configuration:

* Source Code Management: None (for now)
* Build Triggers: leave unchecked (for now)
* Check Build Environment Delete workspace before build starts

Add step to set Python version:

* Select Add build step => Execute shell
* Enter:

```
pyenv local 2.7.6
```

* If you want to run using Python 3.4.0 then change `2.7.6` to `3.4.0`

Add step to get test cases:

* Select Add build step => Execute shell
* Enter:

```
git clone https://github.com/prov-suite/testcases testcases
```

Add step to get ProvToolbox:

* Select Add build step => Execute shell
* Enter:

```
git clone https://github.com/lucmoreau/ProvToolbox.git ProvToolbox
cd ProvToolbox
mvn clean install
./toolbox/target/appassembler/bin/provconvert -version
```

Add step to get ProvPy:

* Select Add build step => Execute shell
* Enter:

```
git clone https://github.com/trungdong/prov ProvPy
cd ProvPy
python setup.py install
./scripts/prov-convert --version
./scripts/prov-compare --version
```

Add step to get interoperability test harness:

* Select Add build step => Execute shell
* Enter:

```
git clone https://github.com/prov-suite/interop-test-harness test-harness
cd test-harness
pip install -r requirements.txt
```

Ad step to configure test harness:

* Select Add build step => Execute shell
* Enter the following, replacing `user:12345qwert` with your ProvStore API key:

```
cd test-harness
CONFIG_DIR=localconfig
rm -rf $CONFIG_DIR
cp -r config/ $CONFIG_DIR
python prov_interop/set_yaml_value.py $CONFIG_DIR/harness.yaml test-cases="$WORKSPACE/testcases"
python prov_interop/set_yaml_value.py $CONFIG_DIR/harness.yaml comparators.ProvPyComparator.executable="python $WORKSPACE/ProvPy/scripts/prov-compare"
python prov_interop/set_yaml_value.py $CONFIG_DIR/provpy.yaml ProvPy.executable="python $WORKSPACE/ProvPy/scripts/prov-convert"
python prov_interop/set_yaml_value.py $CONFIG_DIR/provtoolbox.yaml ProvToolbox.executable="$WORKSPACE/ProvToolbox/toolbox/target/appassembler/bin/provconvert"
cat localconfig/*
python prov_interop/set_yaml_value.py $CONFIG_DIR/provstore.yaml ProvStore.authorization="ApiKey user:12345qwert"
```

Add step to run all interoperability tests:

* Select Add build step => Execute shell

```
cd test-harness
nosetests -v --with-xunit prov_interop.interop_tests
```

* Click Save
* Project PTS-Interop page appears
* Click Build Now
* Click #NNNN build number
* Build #NNNN page appears
* Click Console Output

The Execute shell steps can, alternatively, be done within a single Execute shell entry.

If you are only interested in running interoperability tests for a specific omponent then use the relevant line from:

```
nosetests -v --with-xunit prov_interop.interop_tests.test_provpy
nosetests -v --with-xunit prov_interop.interop_tests.test_provtoolbox
nosetests -v --with-xunit prov_interop.interop_tests.test_provtranslator
nosetests -v --with-xunit prov_interop.interop_tests.test_provstore
```

## Publish xUnit test results

nosetests, with the ``--with-xunit`` option set, outputs test results in xUnit-compliant XML. By default, this file is called `nosetests.xml`. Jenkins can parse and present this informationy.

* Go to Project PTS-Interop page
* Click Configure
* Scroll down to Post-build Action
* Select Add post-build action => Publish JUnit test result report
* Test report XMLs: test-harness/nosetests.xml
  - If you get a warning that nosetests.xml doesn't match anything you can ignore this as the file hasn't been created yet
* Click Save
* Click Build Now
* Click #NNNN build number
* Build #NNNN page appears

## View nosetests test results

You can browse the nosetests test results. These are hierarchically organised by Python module, class and method name.

* EITHER On the Project PTS-Interop page
  - Click the Latest Test Result link
  - If all went well, should say (no failures)
* OR On the Jenkins dashboard/front-page
  - Hover over the build number #NNNN
  - Click drop-down arrow
  - Select Test Result
* Click Python package names to browse down to test classes
* Click Python class names to browse down to test functions

## Start builds manually

* EITHER On the Project PTS-Interop page
  - Click Build Now
* OR On the Jenkins dashboard/front-page
  - Click green "run" icon
* Click #NNNN build number
* Build #NNNN page appears
* Click Console Output to see commands being run by Jenkins

## Importing a Jenkins job

`jenkins/config-interop.xml` contains the Jenkins configuration file for the job written following the above instructions. Assuming you have already done:

* Install dependencies
* Get ProvStore API key
* Install Jenkins
* Install workspace cleanup plugin

Edit jenkins/config-interop.xml and in the line:

```
python prov_interop/set_yaml_value.py $CONFIG_DIR/provstore.yaml ProvStore.authorization=&quot;ApiKey user:12345qwert&quot;
```

replace `user:12345qwert` with your ProvStore username and API key.

Import configuration into Jenkins:

```
$ mkdir $HOME/.jenkins/jobs/PTS-Interop/
$ cp jenkins/config-interop.xml $HOME/.jenkins/jobs/PTS-Interop/config.xml
```

On the Jenkins dashboard:

* Click Manage Jenkins
* Click Reload configuration from disk
* You should see PTS-Interop
* Click green "run" icon

## Jenkins and interoperability test harness unit tests

`jenkins/config-unit.xml` contains the Jenkins configuration file for a simpe job written to run only the interoperability test harness unit tests.

Import configuration into Jenkins:

```
$ mkdir $HOME/.jenkins/jobs/PTS-Unit/
$ cp jenkins/config-unit.xml $HOME/.jenkins/jobs/PTS-Unit/config.xml
```

On the Jenkins dashboard:

* Click Manage Jenkins
* Click Reload configuration from disk
* You should see PTS-Unit
* Click green "run" icon

## Jenkins directories

Jenkins stores its files in `$HOME/.jenkins`.

Jenkins does the build in job-specific workspace directory, `.jenkins/workspace/JOB`, e.g. `.jenkins/workspace/PTS-Interop/`.

Jenkins job configuration, ``config.xml``, and logs and xUnit test results from all the builds, and the previous workspace, are stored in a job-specific jobs directory, `.jenkins/jobs/JOB`, e.g. `.jenkins/jobs/PTS-Interop/`.

## Jenkins and Apache

Jenkins is also available as an Ubuntu package and can be exposed via Apache web server.See [Installing Jenkins on Ubuntu](https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu) and [Running Jenkins behind Apache](https://wiki.jenkins-ci.org/display/JENKINS/Running+Jenkins+behind+Apache).
