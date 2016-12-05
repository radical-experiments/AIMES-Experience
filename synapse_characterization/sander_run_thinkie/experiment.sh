#!/bin/sh

SANDER="/home/merzky/experiments/AIMES-Swift/viveks_workflow/profiling/amber16/bin/sander"

i=69
while true
do
  echo $i
  time $SANDER -O -i mdshort.in -o md1.out -inf md1.inf -x md1.ncdf -r md1.rst -p ace_ala_nme.top -c md1.crd 
  i=$((i+1))
  if test "$i" = '70'
  then
    break
  fi
  break
done 2>&1 | tee -a timings.dat 2>&1

