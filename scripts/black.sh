#!/bin/bash

set -vxeuo pipefail

black --line-length=79 . ${1:-}
