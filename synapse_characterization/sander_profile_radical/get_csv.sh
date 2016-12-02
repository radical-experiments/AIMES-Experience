#!/bin/sh

for p in profile*json
do 
  n=$(echo $p | cut -f 2 -d '_' | cut -f 1 -d '.')
  time=$(grep -e '^        "real": ' $p | head -n 1 | cut -f 2 -d ':' | cut -f 1 -d ',' | cut -f 2 -d ' ')
  echo "sander_profile,radical,$n,$time"
done > sander_profile_radical.csv

