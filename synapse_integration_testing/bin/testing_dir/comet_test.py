import os
import radical.pilot as rp

TIME = 10
pdesc_stampede = {
    'resource'      : 'xsede.stampede',
    'cores'         : 256,
    'runtime'       : TIME,
    'project'       : "TG-MCB090174",
    'queue'         : 'normal'
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
    'cores'         : 16,
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
    'project'       : 'TG-CCR140028',
    'queue'         : 'normal'
}

session = rp.Session()
try:

    pmgr = rp.PilotManager(session)

    pdescs = list()

    #pdescs.append(rp.ComputePilotDescription(pdesc_stampede))
    pdescs.append(rp.ComputePilotDescription(pdesc_comet_compute))
    #pdescs.append(rp.ComputePilotDescription(pdesc_comet_shared))
    #pdescs.append(rp.ComputePilotDescription(pdesc_gordon))
    #pdescs.append(rp.ComputePilotDescription(pdesc_supermic))
    #pdescs.append(rp.ComputePilotDescription(pdesc_bw))
    #pdescs.append(rp.ComputePilotDescription(pdesc_osg))

    pilots = pmgr.submit_pilots(pdescs)


    cuds = list()
    for i in range(1):
        cud = rp.ComputeUnitDescription()
        #cud.pre_exec = ['pip install radical.synapse']
        cud.pre_exec = ['module load python', 
                        'source $HOME/bin/ve.timings/bin/activate'
                       ]
        cud.executable = 'aimes-skeleton-synapse.py'
        cud.arguments = ['serial', 'flops', '1', '1715750072310', '65536', '65536', '0', '0', '0']
        cuds.append(cud)

    umgr = rp.UnitManager(session=session, scheduler='round_robin')
    umgr.add_pilots(pilots)
    units = umgr.submit_units(cuds)
    umgr.wait_units()

except Exception as e:
    print e

finally:
    session.close(cleanup=False)
    os.system('radicalpilot-close-session -m export -s %s' %session.uid)
