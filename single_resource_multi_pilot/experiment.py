import sys
import math
import radical.pilot as rp

__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"

# N_UNITS = 2048
N_UNITS = 2048
U_CORES = 1
U_TIME = 15
RESOURCE = 'xsede.comet'
N_PILOTS = 4
P_CORES = int(math.ceil(N_UNITS/float(N_PILOTS)))
P_WALLTIME = (U_TIME * N_PILOTS) + 15
PROJECT = 'TG-MCB090174'


# -----------------------------------------------------------------------------
def pilot_state_cb(pilot, state):
    print "Pilot %-13s is %-13s on %s" % (pilot.uid, state, pilot.resource)


# -----------------------------------------------------------------------------
def unit_state_cb(cu, state, pilots):
    resource = None

    for pilot in pilots:
        if pilot.uid == cu.pilot_id:
            resource = pilot.resource
            break

    if not resource:
        print "CU %s is %s" % (cu.uid, state)
    elif not cu.pilot_id:
        print "CU %s is %-25s on %s" % (cu.uid, state, resource)
    else:
        print "CU %s is %-25s on %-14s (%s)" % (cu.uid, state, resource,
                                                cu.pilot_id)

    if state == rp.FAILED:
        print "'%s' stderr: %s." % (cu.uid, cu.stderr)
        print "'%s' stdout: %s." % (cu.uid, cu.stdout)


# -----------------------------------------------------------------------------
def wait_queue_size_cb(umgr, wait_queue_size):

    print "UnitManager (unit-manager-%s) has queue size: %s" % (
        umgr.uid, wait_queue_size)

    # pilots = umgr.get_pilots()
    # for pilot in pilots:
    #     print "pilot %s: %s" % (pilot.uid, pilot.state)

    # if wait_queue_size == 0:
    #     for pilot in pilots:
    #         if pilot.state in [rp.PENDING_LAUNCH,
    #                            rp.LAUNCHING     ,
    #                            rp.PENDING_ACTIVE]:
    #             print "cancel pilot %s" % pilot.uid
    #             umgr.remove_pilot(pilot.uid)
    #             pilot.cancel()


# -----------------------------------------------------------------------------
if __name__ == "__main__":

    session = rp.Session()
    print "session id: %s" % session.uid

    try:

        # Add a Pilot Manager.
        pmgr = rp.PilotManager(session=session)

        # Register our callback with the PilotManager.
        pmgr.register_callback(pilot_state_cb)

        # Describe pilots.
        pds = []
        for p in range(N_PILOTS):
            pd = rp.ComputePilotDescription()
            pd.resource = RESOURCE
            pd.project = PROJECT
            pd.runtime = P_WALLTIME
            pd.cores = P_CORES
            pds.append(pd)

        # Launch the pilots.
        pilots = pmgr.submit_pilots(pds)

        # Combine the ComputePilot, the ComputeUnits and a scheduler via
        # a UnitManager object.
        umgr = rp.UnitManager(session=session, scheduler=rp.SCHED_BACKFILLING)

        # Register our callback with the UnitManager.
        umgr.register_callback(unit_state_cb, rp.UNIT_STATE, pilots)

        # Register also a callback which tells us when all units have been
        # assigned to pilots.
        umgr.register_callback(wait_queue_size_cb, rp.WAIT_QUEUE_SIZE)

        # Add the previously created ComputePilot to the UnitManager.
        umgr.add_pilots(pilots)

        # Create the workload.
        cuds = []
        for unit_count in range(N_UNITS):
            cud = rp.ComputeUnitDescription()
            cud.executable = "/bin/sleep"
            cud.arguments     = [U_TIME*60]
            cud.cores         = U_CORES
            cud.restartable   = True
            cuds.append(cud)

        # Submit the ComputeUnit descriptions.
        units = umgr.submit_units(cuds)

        # Wait for all compute units to reach a terminal state(DONE or FAILED).
        umgr.wait_units()

    except Exception as e:
        # Something unexpected happened in the pilot code above
        print "caught Exception: %s" % e
        raise

    except(KeyboardInterrupt, SystemExit) as e:
        # the callback called sys.exit(), and we can here catch the
        # corresponding KeyboardInterrupt exception for shutdown.  We also catch
        # SystemExit(which gets raised if the main threads exits for some other
        # reason).
        print "need to exit now: %s" % e

    finally:
        # always clean up the session, no matter if we caught an exception or
        # not.
        print "closing session"
        session.close(cleanup=False, terminate=True)
