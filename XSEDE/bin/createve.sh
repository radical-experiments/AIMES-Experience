cd ~/github

deactivate
rm -r ~/ve/AIMES-EXPERIENCE-XSEDE
virtualenv ~/ve/AIMES-EXPERIENCE-XSEDE
. ~/ve/AIMES-EXPERIENCE-XSEDE/bin/activate

# Avoid error about setuptools
pip install --upgrade pip
pip install --upgrade setuptools

# Install RU, branch experiment/aimes
cd radical.utils/
git checkout devel
git pull
pip install .
cd ..

# Install SAGA, branch experiment/aimes
cd saga-python/
git checkout devel
git pull
pip install .
cd ..

# Install RP, branch experiment/aimes
cd radical.pilot/
git checkout devel
git pull
pip install .
cd ..

# Installing Skeleton, branch feature/task_prof
cd radical.skeleton/
git checkout feature/task_prof
git pull
pip install .
cd ..

# install aimes.bundle:
cd aimes.bundle/
pip install .
cd ..

# Installing aimes.emgr, branch feature/osg_run
cd aimes.emgr/
git checkout feature/osg_run
git pull
pip install .
cd ..

# Go back to the initial directory
cd /home/mturilli/experiments/AIMES-Experience/XSEDE/bin

radical-stack
