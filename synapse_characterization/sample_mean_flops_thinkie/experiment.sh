#!/bin/sh

.  ../ve/bin/activate

mean=$(../get_flop_average.py ../sander_profile_radical/profile_*.json | tail -n 1 | xargs echo | cut -f 2 -d ' ' | cut -f 1 -d '.')
echo $mean

i=45
while true
do
  echo $i
  time radical-synapse-sample -f $mean
  i=$((i+1))
  if test "$i" = '70'
  then
    break
  fi
  break
done 2>&1 | tee -a timings.dat 2>&1

