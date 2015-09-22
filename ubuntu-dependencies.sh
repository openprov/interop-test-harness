#!/bin/bash
# Install prerequisites for running interoperability test 
# harness, and default ProvToolbox comparator. 

sudo apt-get -qq update
# ProvToolbox dependencies 
sudo apt-get -y install openjdk-7-jdk
java -version
javac -version
sudo apt-get -y install maven
mvn -v
sudo apt-get -y install graphviz
dot -V
sudo apt-get -y install libxml2-utils
xmllint --version
sudo apt-get -y install rpm
sudo apt-get -y install genisoimage

# Test harness dependencies
sudo apt-get -y install git
git --version
sudo apt-get -y install curl
curl --version
# pyenv dependencies
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
# pyenv
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
echo "export PATH=\"\$HOME/.pyenv/bin:\$PATH\"" >> ~/.bash_profile
echo "eval \"\$(pyenv init -)\"" >> ~/.bash_profile
echo "eval \"\$(pyenv virtualenv-init -)\"" >> ~/.bash_profile

echo "export PATH=\"\$HOME/.pyenv/bin:\$PATH\"" >> ~/.bashrc
echo "eval \"\$(pyenv init -)\"" >> ~/.bashrc
echo "eval \"\$(pyenv virtualenv-init -)\"" >> ~/.bashrc

source ~/.bash_profile
pyenv update
pyenv install -l
pyenv install 2.7.6
pyenv install 3.4.0
pyenv local 2.7.6
