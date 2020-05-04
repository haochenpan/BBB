#!/usr/bin/env bash
# $1: num of miners

if [[ -z $1 ]]; then
  echo "please enter num of miners as the first parameter"
else
    python3 ./v2/analysis.py $1
fi
