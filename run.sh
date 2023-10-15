#! /bin/bash
set -e

# Get the path to the source directory
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

# Load the env vars
eval $(sed -e '/^\s*$/d' -e '/^\s*#/d' -e 's/=/="/' -e 's/$/"/' -e 's/^/export /' "${SCRIPT_DIR}/.env")

# Run the application, passing the first argument as --digest-type
cd "${SCRIPT_DIR}"; python3 -m daily-digest --digest-type "$1"
