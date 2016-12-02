#!/bin/sh

.  /home/merzky/test_synapse/ve/bin/activate

i=0
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
done 2>&1 | tee -a timings.dat 2>&1

