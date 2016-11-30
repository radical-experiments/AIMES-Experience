OSG Experiments Log
===================

Execution
---------
```
[64  , 1024, 32  , 256, 256, 16  , 512, 512, 128, 1024, 128, 2048,
 64  , 512 , 128 , 8  , 16 , 2048, 256, 512, 16 , 64  , 32 , 1024,
 2048, 32  , 1024, 8  , 256, 2048, 8  , 32 , 8  , 64  , 128, 16]
```

Experiment Execution Workflow
-----------------------------
```
source setup.sh  # export variables for RADICAL CT logging and debu level
vi store_run.sh  # edit the number of the experiment
vi config.json   # edit BoTs and number of pilots
python experiment.py config.json  # run the experiment
./store_run.sh <session_id> <run-bot-dir> <bot_size>
```

Failed without CU rescheduling
------------------------------

| #  | Session                                 | # Tasks |
|----|-----------------------------------------|---------|
| 1  | rp.session.radical.mturilli.017079.0001 | 64      |
| 2  | rp.session.radical.mturilli.017080.0000 | 1024    |
| 3  | rp.session.radical.mturilli.017080.0001 | 1024    |
| 4  | rp.session.radical.mturilli.017083.0000 | 32      |
| 5  | rp.session.radical.mturilli.017084.0003 | 64      |
| 6  | rp.session.radical.mturilli.017084.0005 | 32      |
| 7  | rp.session.radical.mturilli.017084.0007 | 32      |
| 8  | rp.session.radical.mturilli.017085.0004 | 32      |
| 9  | rp.session.radical.mturilli.017086.0000 | 64      |
| 10 | rp.session.radical.mturilli.017086.0001 | 64      |
| 11 | rp.session.radical.mturilli.017086.0003 | 32      |
| 12 | rp.session.radical.mturilli.017087.0000 | 8       |
| 13 | rp.session.radical.mturilli.017087.0001 | 8       |
| 14 | rp.session.radical.mturilli.017087.0007 | 64      |

Failed with CU rescheduling
---------------------------

| #  | Session                                 | # Tasks |
|----|-----------------------------------------|---------|
| 1  | rp.session.radical.mturilli.017087.0008 | 64      |
| 2  | rp.session.radical.mturilli.017087.0010 | 64      |
| 3  | rp.session.radical.mturilli.017088.0002 | 512     |
| 4  | rp.session.radical.mturilli.017089.0001 | 16      |
| 5  | rp.session.radical.mturilli.017089.0004 | 512     |
| 6  | rp.session.radical.mturilli.017089.0005 | 512     |
| 7  | rp.session.radical.mturilli.017090.0005 | 8       |
| 8  | rp.session.radical.mturilli.017092.0003 | 256     |
| 9  | rp.session.radical.mturilli.017093.0001 | 512     |
| 10 | rp.session.radical.mturilli.017094.0001 | 1024    |
| 11 | rp.session.radical.mturilli.017095.0000 | 1024    |
| 12 | rp.session.radical.mturilli.017095.0002 | 128     | OSG
| 13 | rp.session.radical.mturilli.017095.0004 | 2048    | OSG
| 14 | rp.session.radical.mturilli.017095.0005 | 2048    | OSG
| 15 | rp.session.radical.mturilli.017096.0000 | 512     | OSG
| 16 | rp.session.radical.mturilli.017097.0000 | 512     | RP
| 17 | rp.session.radical.mturilli.017097.0003 | 2048    | RP/OSG
| 18 | rp.session.radical.mturilli.017098.0000 | 2048    | RP
| 19 | rp.session.radical.mturilli.017109.0001 | 2048    | RP
| 20 | rp.session.radical.mturilli.017110.0000 | 2048    |
| 21 | rp.session.radical.mturilli.017110.0001 | 2048    | OSG
| 22 | rp.session.radical.mturilli.017111.0000 | 2048    | OSG
| 23 | rp.session.radical.mturilli.017113.0000 | 2048    |
| 24 | rp.session.radical.mturilli.017113.0001 | 2048    |
| 25 | rp.session.radical.mturilli.017114.0000 | 2048    |
| 26 | rp.session.radical.mturilli.017114.0001 | 2048    |
| 27 | rp.session.radical.mturilli.017114.0002 | 2048    |
| 28 | rp.session.radical.mturilli.017118.0002 | 2048    |
| 29 | rp.session.radical.mturilli.017123.0002 | 512     | OSG
| 30 | rp.session.radical.mturilli.017123.0003 | 512     | RP
| 31 | rp.session.radical.mturilli.017133.0006 | 64      | OSG Broker
