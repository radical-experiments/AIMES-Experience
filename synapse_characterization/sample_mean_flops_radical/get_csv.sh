#!/bin/sh

i=0
for time in `grep real timings.dat  | cut -f 5 -d ' '| cut -f 1 -d ','`
do
  echo "sander_emulate_meanflops,radical,$i,$time"
  i=$((i+1))
done > sander_emulate_meanflops_radical.csv

