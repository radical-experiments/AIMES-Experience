#!/bin/sh

.  ../ve/bin/activate

i=0
while true
do
  echo "$i"
  time -p radical-synapse-emulate -i ../sander_profile_radical/profile_$i.json > /dev/null
  i=$((i+1))
  if test "$i" = '70'
  then
    break
  fi
done 2>&1 | tee -a timings.dat 2>&1

