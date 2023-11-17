#!/bin/bash

# Exit if any command fails
set -e

# Uninstall existing verbomate package
echo "Attempting to uninstall verbomate..."
echo "Y" | pip3 uninstall verbomate

# Install verbomate from the current directory
echo "Installing verbomate from the current directory..."
pip3 install .

echo "Installation complete."