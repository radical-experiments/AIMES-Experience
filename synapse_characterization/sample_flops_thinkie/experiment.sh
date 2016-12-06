#!/bin/sh

.  ../ve/bin/activate

i=16
while true
do
  flops=$(../get_flop_average.py ../sander_profile_radical/profile_$i.json | tail -n 1 | xargs echo | cut -f 2 -d ' ' | cut -f 1 -d .) 
  echo "flops: $i $flops"
  time radical-synapse-sample -f $flops
  i=$((i+1))
  if test "$i" = '70'
  then
    break
  fi
  break
done 2>&1 | tee -a timings.dat 2>&1

