#!/bin/sh

for p in profile*json
do 
  n=$(echo $p | cut -f 2 -d '_' | cut -f 1 -d '.')
  flops=$(../get_flop_average.py $p | tail -n 1 | xargs echo | cut -f 2 -d ' ' | cut -f 1 -d '.')
  time=$(grep -e '^        "real": ' $p | head -n 1 | cut -f 2 -d ':' | cut -f 1 -d ',' | cut -f 2 -d ' ')
  echo "sander_profile,radical,$n,$time,$flops"
done > sander_profile_radical.csv

