#!/bin/bash

deactivate || true

cwd=`pwd`
base=$HOME/radical/
exp=experiments/AIMES-Experience

cd $base/$exp
rm -rf ve/
virtualenv ve/
. ve/bin/activate

install()
{
    dir=$1
    branch=$2

    echo
    printf "--------------------------------------------\n"
    printf "INSTALL  %-20s @ %s\n" $dir $branch
    printf "--------------------------------------------\n"

    builtin cd $base/$dir
    git co $branch
    git pull
    pip install .
}


install  radical.utils        experiment/aimes
install  radical.saga         experiment/aimes
install  radical.pilot.aimes  experiment/aimes
install  aimes.skeleton       feature/task_flops
install  aimes.bundle         master
install  aimes.emgr           feature/osg_run

cd $cwd

echo "RP: `radicalpilot-version`"
echo "RS: `sagapython-version`"
echo "RU: `radical-utils-version`"

