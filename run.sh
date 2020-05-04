#!/usr/bin/env bash
# $1: num of miners

if [[ -z $1 ]]; then
  echo "please enter num of miners as the first parameter"
else
  chmod 700 prerun2.sh
  chmod 700 analysis.sh
  . prerun2.sh $1
  python3 ./v2/v2_start.py $1
  killall geth
  . analysis.sh $1
fi
