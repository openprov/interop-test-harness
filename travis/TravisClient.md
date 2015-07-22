# Travis Client and automatically rerunning interoperability tests

The [Travis Client](https://github.com/travis-ci) allows [Travis CI](https://travis-ci.org) jobs to be managed from the command-line. This can be useful for automatically triggering re-runs of interoperability tests without having to either submit a GitHub pull request on the repository holding the Travis CI configuration file, or going via Travis CI's web interface.

The instructions have been written with reference to the 64-bit [Ubuntu](http://www.ubuntu.com/) 14.04.2 operating system.

Other operating systems, or versions of these, may differ in how packages are installed, the versions of these packages available from package managers etc. Consult the relevant documentation for your operating system and the products concerned.

Some dependencies require you to have sudo access to install and configure software (or a local system administrator can do this for you).

## Install RVM and Ruby 2.2

Travis Client runs under Ruby. We will use [Ruby Version Manager](https://rvm.io) to install Ruby.

```
$ gpg --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
$ \curl -sSL https://get.rvm.io | bash -s stable --ruby
```

You may be prompted for a sudo password:

```
Updating system ubuntu password required for 'apt-get --quiet --yes update': 
```

so that dependencies can be installed:

```
Installing required packages: gawk, libyaml-dev, sqlite3, autoconf, libgdbm-dev, libncurses5-dev, automake, libtool, bison............
```

Set up RVM environment:

```
$ source ~/.rvm/scripts/rvm
```

Install Ruby:

```
$ rvm list known
$ rvm install 2.2
$ rvm use 2.2
$ rvm --default use 2.2
$ ruby -v
ruby 2.2.1p85 (2015-02-26 revision 49769) [x86_64-linux]
```

## Install Travis Client gem

```
$ gem install travis
$ travis version
travis version
Shell completion not installed. Would you like to install it now? |y| y
1.8.0
```

## Log in to Travis CI

Use your GitHub username and password to log in to Travis CI:

```
$ travis login
We need your GitHub login to identify you.
This information will not be sent to Travis CI, only to api.github.com.
The password will not be displayed.

Try running with --github-token or --auto if you don't want to enter your password anyway.

Username: USERNAME
Password for USERNAME: PASSWORD
Successfully logged in as USERNAME!
```

## Travis CI identification

Travis Client commands can be run within a Git repository and the client will try and determine the user/project name and repository name to use when interacting with Travis CI. Alternatively, you can provide the user/project name and repository name explicitly in the form USER_OR_PROJECT_NAME/REPOSITORY_NAME e.g.

```
prov-suite/interop-test-harness
prov-suite/provpy-interop-job
user/provtoolsuite-provpy-interop-job
```

## View build history

```
$ travis history -r prov-suite/interop-test-harness
#5 passed:       master Merged in changes from user
#4 passed:       master Merge pull request #1 from user/master
#3 passed:       master (PR #1) Added standalone usage information
#2 passed:       master Runs unit tests correctly
#1 passed:       master user -> prov-suite and removed provtoolsuite- prefix to reflect forking of repository into prov-suite
```

```
$ travis history -r prov-suite/provpy-interop-job
#2 passed:       master Merged in changes from user
#1 passed:       master user -> prov-suite and removed provtoolsuite- prefix to reflect forking of repository into prov-suite
```

## Restart builds

Restart the most recent build for a repository:

```
$ travis restart -r prov-suite/provpy-interop-job
build #2 has been restarted
```

Restart a specific build for a repository:

```
$ travis restart -r prov-suite/provpy-interop-job 2
build #2 has been restarted
```

Restart a job within a specific for a repository (e.g. rerun job 2, the Python 3.4 version, of the build):

```
$ travis restart -r prov-suite/provpy-interop-job 2.2.
build #2 has been restarted
```

## Logout from travis

```
$ travis logout
Successfully logged out!
```

## Create a GitHub token

Instead of having to interactively log in, you can create a GitHub token. This then allows interactions with Travis CI via Travis Client to be scripted and run without human interaction (e.g. as part of an overnight CRON job):

* Log in to https://github.com
* Visit https://github.com/settings/profile
* Click Personal access tokens
* Click Generate new token
* Enter Password
* Click Confirm password
* Token description: TravisCI command-line tool
* Click Generate token
* Copy token and save it somewhere save

## Log into Travis CI using token

```
$ travis login --github-token TOKEN
Successfully logged in as user!
```

## Sample script

[travis-restart.sh](./travis-restart.sh) contains a simple example of a script to automatically trigger a rerun of a Travis CI build of the prov-suite/interop-test-harness build. To use this script:

* Edit it and replace `GITHUB_TOKEN` with your GitHub token
* Run:

```
./travis-restart.sh
```

* You should see output like:

```
Successfully logged in as user!
#5 passed:       master Merged in changes from user
#4 passed:       master Merge pull request #1 from user/master
#3 passed:       master (PR #1) Added standalone usage information
#2 passed:       master Runs unit tests correctly
#1 passed:       master user -> prov-suite and removed provtoolsuite- prefix to reflect forking of repository into prov-suite
build #5 has been restarted
Successfully logged out!
```
