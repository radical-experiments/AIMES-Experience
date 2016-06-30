#!/usr/bin/env bash

for j in `seq 10`;
do
    { time python ~/bin/Skeleton/bin/aimes-skeleton-synapse.py serial flops 1 1715750072310 65536 65536 0 0 0 ; } 2>> ~/bin/time_results_skeleton_comet;
done
sed -n '/cannot/!p' ~/bin/time_results_skeleton_comet | sed -n '/open/!p' | grep . > ~/bin/time_results_cleaned_skeleton_comet
