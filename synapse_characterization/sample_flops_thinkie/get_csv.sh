#!/bin/sh

i=0
for time in `grep real timings.dat  | cut -f 5 -d ' '| cut -f 1 -d ','`
do
  flops=$(../get_flop_average.py ../sander_profile_radical/profile_$i.json | tail -n 1 | xargs echo | cut -f 2 -d ' ' | cut -f 1 -d .) 
  echo "sander_emulate_flops,thinkie,$i,$time,$flops"
  i=$((i+1))
done > sander_emulate_flops_thinkie.csv

