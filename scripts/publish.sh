#!/bin/bash

# Exit if any command fails
set -e

# Build the package
echo "Building the package..."
python3 setup.py sdist bdist_wheel

# Upload the package to PyPI
echo "Uploading the package to PyPI..."
twine upload dist/* -u __token__ -p $PYPI_API_TOKEN

echo "Package uploaded successfully."