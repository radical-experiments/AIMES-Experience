#!/bin/sh

i=0
for t in `grep user timings.dat  | cut -f 1 -d u`
do 
  echo "sander_run,radical,$i,$t"
  i=$((i+1))
done > sander_run_radical.csv

