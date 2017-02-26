# OSX only with brew
#export LDFLAGS="-L/usr/local/opt/openssl/lib"
#export CPPFLAGS="-I/usr/local/opt/openssl/include"

cd ~/github

deactivate
rm -r ~/ve/AIMES-EXPERIENCE
virtualenv ~/ve/AIMES-EXPERIENCE
. ~/ve/AIMES-EXPERIENCE/bin/activate

# Avoid error about setuptools
pip install --upgrade pip
pip install --upgrade setuptools

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
cd /home/mturilli/experiments/AIMES-Experience/old/synapse_integration_testing/bin

echo "RP: `radicalpilot-version`"
echo "RS: `sagapython-version`"
echo "RU: `radical-utils-version`"
