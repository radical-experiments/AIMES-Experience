#!/bin/sh

i=0
for time in `grep real timings.dat | cut -f 2 -d ' '`
do
  echo "sander_emulate_profiles,thinkie,$i,$time"
  i=$((i+1))
done > sander_emulate_profiles_thinkie.csv

