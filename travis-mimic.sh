#!/bin/bash

PWD=`pwd`

DOWNLOADS=$PWD/downloads
mkdir $DOWNLOADS

echo "Getting test cases..."
TESTCASES=$DOWNLOADS/testcases
git clone https://github.com/mikej888/provtoolsuite-testcases $TESTCASES

# echo "Installing ProvToolbox dependencies..."
# sudo apt-get -y install libxml2-utils
# sudo apt-get -y install graphviz

echo "Getting ProvToolbox..."
PROVTOOLBOX=$DOWNLOADS/ProvToolbox
git clone https://github.com/lucmoreau/ProvToolbox.git $PROVTOOLBOX
cd $PROVTOOLBOX
mvn clean install
./toolbox/target/appassembler/bin/provconvert -version
cd ../..

# echo "Installing ProvPy dependencies..."
# sudo apt-get -y install zlib1g-dev
# sudo apt-get -y install libxslt1-dev

echo "Getting ProvPy..."
PROVPY=$DOWNLOADS/ProvPy
git clone https://github.com/trungdong/prov $PROVPY
cd $PROVPY
git checkout 1.3.2
python setup.py install
./scripts/prov-convert --version
cd ../..

pip install -r requirements.txt

echo "Creating local configuration files..."
echo "PROV_TEST_CASES_DIR=$TESTCASES" > config.properties
echo "PROVPY_SCRIPTS_DIR=$PROVPY/scripts" >> config.properties
echo "PROVTOOLBOX_SCRIPTS_DIR=$PROVTOOLBOX/toolbox/target/appassembler/bin" >> config.properties
echo "PROV_LOCAL_CONFIG_DIR=$PWD/localconfig" >> config.properties
mkdir localconfig
python prov_interop/customise-config.py config localconfig config.properties
cat localconfig/*

nosetests -v prov_interop.tests
nosetests -v prov_interop.interop_tests.test_provpy
nosetests -v prov_interop.interop_tests.test_provtoolbox
