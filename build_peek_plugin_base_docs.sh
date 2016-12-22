#!/usr/bin/env bash
PACKAGE="peek_plugin_base"

set -o nounset
set -o errexit

echo "Retrieving latest version tag"
VER=$(git describe --tags `git rev-list --tags --max-count=1`)

echo "Setting version to $VER"
sed -i "s;.*version.*;__version__ = '${VER}';" ${PACKAGE}/__init__.py

echo "==========================================="
echo "Building Sphinx documentation for '${PACKAGE}'!"
echo "==========================================="

echo "Removing old documentation in build folder."
rm -fr dist/docs/*

echo "Updating module rst files.  This will overwrite old rst files."
sphinx-apidoc -f -e -o docs ${PACKAGE} '*Test.py'

echo "Build HTML files."
sphinx-build -b html docs dist/docs

echo "Opening created documentation..."
start dist/docs/index.html