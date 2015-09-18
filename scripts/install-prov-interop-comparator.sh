#!/bin/bash

echo "Installing ProvToolbox comparator..."
wget https://repo1.maven.org/maven2/org/openprovenance/prov/toolbox/0.7.1/toolbox-0.7.1-release.zip
unzip toolbox-0.7.1-release.zip
export PATH=$PATH:$PWD/ProvToolbox/bin/
