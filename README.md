# AIMES-Experience
Measuring scatter of task executions across diverse distributions of resources. 

Related paper at: https://bitbucket.org/shantenujha/aimes

* [Experimental Workflow](#experimental-workflow)
* [Data Analysis Workflow](#data-analysis-workflow)

## Experimental Workflow
1. Prerequisites: Python 2.7; pip; git; radical-pilot
1. Clone this repository:

  ```
  git clone https://github.com/radical-experiments/AIMES-Experience.git
  ```

1. Install RADICAL Cybertools:
 
  ```
  virtualenv ~/ve/aimes-experience
  . ~/ve/aimes-experience/bin/activate
  pip install radical-pilot
  ```

1. Move into the ```AIMES-Experience``` directory.
1. Edit the file ```experiment.py``` setting the following global variables to their appropriate value:

  ```
  N_UNITS = 2048
  U_CORES = 1
  U_TIME = 15
  RESOURCE = 'xsede.comet'
  N_PILOTS = 4
  P_CORES = 512
  P_WALLTIME = 75
  PROJECT = 'TG-XXXXXXXXX'
  ```
  
  Note: SSH key-based, passwordless access to the choosen resource(s) is required.

1. Set up your execution environment:

  ```
  . setup.sh
  ```

1. run the experiment:

  ```
  python experiment.py
  ```

1. Download session for the experiment:

  ```
  radicalpilot-close-session -m export -d mongodb://54.221.194.147:24242/aimes-experience -s rp.session.xxxx.xxxx.xxxx.xxxx.xxxx
  ```

1. Upon success of the previous command, create a directory ```runn``` where ```n``` uniquely and incrementally indicates the number of the experiment.
1. Create a file inside ```runn``` called ```metadata.json``` with the following information:

  ```
  {
    "n_tasks": <int>,
    "n_cores": <int>,
    "pilots": [
      [<int n_cores>, <walltime>],
      ...
    ],
    "resources": [
      "resource.tag",
      ...
    ],
    "cores": [
      [<int tasks>, <int n_cores>],
      ...
    ],
    "durations": [
      [<int tasks>, <int duration>],
      ...
    ]
  }
  ```
  
  Example:
  
  ```json
  {
    "n_tasks": 2048,
    "n_cores": 2048,
    "pilots": [
      [512, 75],
      [512, 75],
      [512, 75],
      [512, 75]
    ],
    "resources": [
      "xsede.comet"
    ],
    "cores": [
      [2048, 1]
    ],
    "durations": [
      [2048, 15]
    ]
  }
  ```
  
  Note:
  * Durations are in minutes.
  * ```"cores"``` and ```"durations"``` are used to describe partions of the set of tasks. At the moment, we use just 1 core and 15 minutes duration for each task but we will have to use more complex distributions or cores and durations.

1. Copy the .prof, .json, and log file into the ```runn``` directory:
 
  ```
  cp rp.session.xxxx.xxxx.xxxx.xxxx.xxxx.prof rp.session.xxxx.xxxx.xxxx.xxxx.xxxx.json logs/radical_debug.log runn/
  ```
  
1. Pull and push the repository.

## Data Analysis Workflow
