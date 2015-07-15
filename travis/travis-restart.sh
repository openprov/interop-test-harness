#!/bin/bash
# Simple script to automatically trigger a Travis CI rebuild using
# Travis Client.
#
# Replace GITHUB_TOKEN with your GitHub token:
# * Log in to https://github.com
# * Visit https://github.com/settings/profile
# * Click Personal access tokens
# * Click Generate new token
# * Enter Password
# * Click Confirm password
# * Token description: TravisCI command-line tool
# * Click Generate token
# * Copy token and save it somewhere save

travis login --github-token GITHUB_TOKEN
travis history -r prov-suite/interop-test-harness
travis restart -r prov-suite/interop-test-harness
travis logout
