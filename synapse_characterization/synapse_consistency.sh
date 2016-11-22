#!/bin/sh

flops=1715750072310
i=0

mv -v synapse.dat synapse.dat.bak

while test $i -lt 100
do
    i=$((i+1))
    echo $i
    radical-synapse-sample -f $flops 2>&1 | tee -a synapse.dat
done

