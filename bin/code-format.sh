##!/bin/bash

cd $(dirname $0)/../
python -m yapf -vv -i --style google -r src
