#!/bin/bash
set -e

./main.py | dot -Tpng > hello.png && eog hello.png
