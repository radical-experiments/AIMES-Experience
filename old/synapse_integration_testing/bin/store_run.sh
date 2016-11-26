#!/bin/sh

set -e

ROOT='/home/mturilli/experiments/AIMES-Experience/synapse_integration_testing/bin'
TMP='/tmp/profiles'
STORE='/home/mturilli/experiments/AIMES-Experience/synapse_integration_testing/experiments'
EXP='osg_runs_exp9'

sid=$1
run=$2
bot=$3

cd $TMP
echo $PWD

echo "radicalpilot-fetch-profiles -c $ROOT $sid"
radicalpilot-fetch-profiles -c $ROOT $sid

echo "cp $ROOT/$run/$sid.json $sid/"
cp $ROOT/$run/$sid.json $sid/

echo "mv $sid $STORE/$EXP/$bot/"
mv $sid $STORE/$EXP/$bot/

ls -altr $STORE/$EXP/$bot/
ls $STORE/$EXP/$bot/$sid/
cd $ROOT
