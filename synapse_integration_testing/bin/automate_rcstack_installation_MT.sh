# OSX only with brew
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

cd ~/Projects/RADICAL/github

deactivate
rm -r ~/Virtualenvs/AIMES-EXPERIENCE
virtualenv ~/Virtualenvs/AIMES-EXPERIENCE
. ~/Virtualenvs/AIMES-EXPERIENCE/bin/activate

# Install RU, branch experiment/aimes
cd radical.utils/
git checkout experiment/aimes
git pull
pip install .
cd ..

# Install SAGA, branch experiment/aimes
cd saga-python/
git checkout experiment/aimes
git pull
pip install .
cd ..

# Install RP, branch experiment/aimes
cd radical.pilot/
git checkout experiment/aimes
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
cd ~/Projects/RADICAL/github/experiments/AIMES-Experience/synapse_integration_testing/bin

