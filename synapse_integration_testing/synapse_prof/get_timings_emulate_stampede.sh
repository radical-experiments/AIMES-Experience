#!/usr/bin/env bash

for i in `seq 10`;
do
        { time radical-synapse-emulate -i ~/bin/84.json ; } 2>> ~/bin/time_results_emulate_stampede; 
done

sed -n '/cannot/!p' ~/bin/time_results_emulate_stampede | sed -n '/open/!p' | grep . > time_results_cleaned_emulate_stampede

