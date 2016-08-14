import os
import radical.pilot as rp

UNITS = 4
TIME = 60 * 24
pdesc_stampede = {
    'resource'      : 'xsede.stampede',
    'cores'         : 16,
    'runtime'       : TIME,
    'project'       : "TG-MCB090174",
    'queue'         : "development"
    #'queue'         : 'normal'
}

pdesc_comet_compute = {
    'resource'      : 'xsede.comet',
    'cores'         : 24,
    'runtime'       : TIME,
    'project'       : 'unc100',
    'queue'         : 'compute'
}

pdesc_comet_shared = {
    'resource'      : 'xsede.comet',
    'cores'         : 1,
    'runtime'       : TIME,
    'project'       : 'unc100',
    'queue'         : 'shared'
}

pdesc_gordon = {
    'resource'      : 'xsede.gordon',
    'cores'         : 1024,
    'runtime'       : TIME,
    'project'       : "TG-MCB090174",
    'queue'         : 'normal'
}

pdesc_supermic = {
    'resource'      : 'xsede.supermic',
    'cores'         : 20,
    'runtime'       : TIME,
    'project'       : 'TG-MCB090174',
    'queue'         : 'workq'
}

pdesc_bw = {
    'resource'      : 'ncsa.bw',
    'cores'         : 32,
    'runtime'       : TIME,
    'project'       : 'gkd',
    'queue'         : 'normal'
}

pdesc_osg = {
    'resource'      : 'osg.xsede-virt-clust',
    'cores'         : 1,
    'runtime'       : TIME,
    'project'       : 'TG-CCR140028'
#    'queue'         : 'normal'
}

pdesc_localhost = {
    'resource'      : 'local.localhost',
    'cores'         : 1,
    'runtime'       : TIME,
}
session = rp.Session()
try:

    pmgr = rp.PilotManager(session)

    pdescs = list()

    #pdescs.append(rp.ComputePilotDescription(pdesc_stampede))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_compute))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_shared))
    #pdescs.append(rp.ComputePilotDescription(pdesc_gordon))
    #pdescs.append(rp.ComputePilotDescription(pdesc_supermic))
    #pdescs.append(rp.ComputePilotDescription(pdesc_bw))
    #pdescs.append(rp.ComputePilotDescription(pdesc_osg))
    #pdescs.append(rp.ComputePilotDescription(pdesc_osg))
    #pdescs.append(rp.ComputePilotDescription(pdesc_osg))
    #pdescs.append(rp.ComputePilotDescription(pdesc_osg))

    pdescs.append(rp.ComputePilotDescription(pdesc_localhost))

    pilots = pmgr.submit_pilots(pdescs)


    cuds = list()
    for i in range(UNITS):
        cud = rp.ComputeUnitDescription()
        """
        cud.pre_exec = [#'module load python',
                        #'export LMOD_CMD=/opt/apps/lmod/lmod/libexec/lmod',
                        #'export LMOD_SYSTEM_DEFAULT_MODULES=TACC',
                        #'module load TACC',
                        #'module load intel',
                        #'module load python',
                        #'source $HOME/bin/ve.synapse/bin/activate'
                        #'module load intel'
                        #'echo $PWD',
                        #'whoami'
                       ]
        """
        
        
        cud.pre_exec = [
                        ('echo $HOME ; '
                        'if test ! -d $HOME/ve.synapse; ' 
                        'then virtualenv $HOME/ve.synapse ; '
                        'source $HOME/ve.synapse/bin/activate ; '
                        'wget -qO- https://github.com/radical-cybertools/radical.utils/archive/v0.41.1.tar.gz | tar -xzv -C $HOME/ ;'
                        'pip install $HOME/radical.utils-0.41.1/. ; '
                        'wget -qO- https://github.com/applicationskeleton/Skeleton/archive/v1.2.tar.gz | tar -xzv -C $HOME/ ; '
                        'pip install $HOME/Skeleton-1.2/. ; '
                        'wget -qO- https://github.com/radical-cybertools/radical.synapse/archive/v0.44.tar.gz | tar -xzv -C $HOME/ ; '
                        'pip install $HOME/radical.synapse-0.44/. ; '
                        'wget -P $HOME/ https://raw.githubusercontent.com/applicationskeleton/Skeleton/feature/task_flops/bin/aimes-skeleton-synapse.py ; '
                        'chmod u+x $HOME/aimes-skeleton-synapse.py ; '
                        'PATH=$PATH:$HOME ; '
                        'export PATH ; '
                        'else source $HOME/ve.synapse/bin/activate ; '
                        'PATH=$PATH:$HOME ; '
                        'export PATH ; '
                        'fi ; '
                        )
                       ]
        
        #cud.executable = 'echo'
        #cud.arguments = ['$PATH']
        #cud.arguments = ['-l', '$HOME/aimes-skeleton-synapse.py']
        cud.executable = 'aimes-skeleton-synapse.py'
        cud.arguments = ['serial', 'flops', '1', '1715750072310', '65536', '65536', '0', '0', '0']
        #cud.executable = 'echo $PATH; echo $LD_LIBRARY_PATH'
        #cud.executable = '/bin/sleep'
        #cud.arguments = ['30']
        #cud.executable = 'radical-synapse-version'
        #cud.executable = '/bin/date'
        cuds.append(cud)

    umgr = rp.UnitManager(session=session, scheduler='backfilling')
    umgr.add_pilots(pilots)
    units = umgr.submit_units(cuds)
    umgr.wait_units()

except Exception as e:
    print e

finally:
    session.close(cleanup=False)
    os.system('radicalpilot-close-session -m export -s %s' %session.uid)
