#!/bin/bash

set -e -x

pip install --upgrade pip
pip install https://github.com/bigchaindb/bigchaindb-hs/releases/download/0.1.0.1/bigchaindb-shared-0.1.0.1.tar.gz

if [[ -n ${TOXENV} ]]; then
    pip install --upgrade tox
else
    pip install -e .[test]
    pip install --upgrade codecov
fi
