###Setup Instructions

Setting up virtual environment
```
virtualenv ~/ve.xdmod
source ~/ve.xdmod/bin/activate
```

Making directory to hold all the repos
```
mkdir ~/aimes_exp_repos
cd ~/aimes_exp_repos/
```

Install RP, branch experiment/aimes
```
git clone https://github.com/radical-cybertools/radical.pilot.git
cd radical.pilot/
git checkout experiment/aimes
git pull
pip install -U .
cd ~/aimes_exp_repos/
```

Install SAGA, branch experiment/aimes
```
git clone https://github.com/radical-cybertools/saga-python.git
cd saga-python/
git checkout experiment/aimes
git pull
pip install -U --no-deps .
cd ~/aimes_exp_repos/
```

Install RU, branch experiment/aimes
```
git clone https://github.com/radical-cybertools/radical.utils.git
cd radical.utils/
git checkout experiment/aimes 
git pull
pip install -U --no-deps .
cd ~/aimes_exp_repos/
```

Installing Skeleton, branch feature/task_prof
```
git clone https://github.com/radical-cybertools/Skeleton.git
cd Skeleton/
git checkout feature/task_prof
git pull
pip install -U --no-deps .
cd ~/aimes_exp_repos/
```

Installing aimes.bundle, branch master. Note: bundles requires paramiko that requires in turn the openssl headers to be available in a reachable path at compilation time. On OSX, these headers can be installed via the OSX development tools or (better) brew. If the compilation fails to find the openssl headers, the following may help:
```
brew install openssl
export LDFLAGS=-L/usr/local/opt/openssl/lib
export CPPFLAGS=-I/usr/local/opt/openssl/include
```
To install aimes.bundle:
```
git clone https://github.com/Francis-Liu/aimes.bundle.git
cd aimes.bundle/
pip install -U .
cd ~/aimes_exp_repos/
```

Installing aimes.emgr, branch feature/osg_run
```
git clone https://github.com/radical-cybertools/aimes.emgr.git
cd aimes.emgr/
git checkout feature/osg_run
git pull
pip install -U --no-deps .
cd ~/aimes_exp_repos/
```

Set the MongoDB URL in `experiment.osg.json`
The experiment setup can also be changed in `experiment.osg.json`

Exporting env variables
```
export RADICAL_PILOT_PROFILE=TRUE
export SAGA_PTY_SSH_TIMEOUT=300
```

Running the experiment
```
python aimes_only.py experiment.osg.json
```

