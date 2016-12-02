#!/usr/bin/env python
"""This script does x.

Example:

Attributes:

Todo:

"""

import os
import sys
import glob
import numpy as np
import pandas as pd
import radical.analytics as ra


def initialize_entity(ename=None):
    entities = {'session': {'session'      : [],     # RA session objects
                            'experiment'   : [],     # Experiment ID
                            'TTC'          : [],     # Time to completion
                            'nhost'        : [],     # #host for CU execution
                            'nunit'        : [],     # #units
                            'nunit_done'   : [],     # #active units
                            'nunit_failed' : [],     # #failed units
                            'npilot'       : [],     # #pilots
                            'npilot_active': []},    # #active pilots
                'pilot'  : {'pid'          : [],     # Pilot ID
                            'sid'          : [],     # Session ID
                            'hid'          : [],     # Host ID
                            'experiment'   : []},    # Experiment ID
                'unit'   : {'uid'          : [],     # Unit ID
                            'sid'          : [],     # Session ID
                            'hid'          : [],     # Host ID
                            'experiment'   : []}}    # Experiment ID

    # Add the duration label of each state of each entity.
    for duration in pdm.keys():
        entities['session'][duration] = []
        entities['pilot'][duration] = []
    for duration in udm.keys():
        entities['session'][duration] = []
        entities['unit'][duration] = []

    # Return the empty data structure of the requested entity.
    if ename in ['session', 'pilot', 'unit']:
        return entities[ename]
    else:
        error = 'Cannot itialize entity %s' % ename
        print error
        sys.exit(1)


def load_df(ename=None):
    if ename in ['session', 'pilot', 'unit']:
        df = pd.DataFrame(initialize_entity(ename=ename))
        try:
            df = pd.read_csv(csvs[ename], index_col=0)
        except:
            pass
        return df
    else:
        error = 'Cannot itialize entity %s' % ename
        print error
        sys.exit(1)


def store_df(new_df, stored=pd.DataFrame(), ename=None):
    # skip storing if no new data are passed.
    if new_df.empty:
        print 'WARNING: attempting to store an empty DF.'
    else:
        if ename == 'session':
            new_sessions = new_df.drop('session', axis=1)
            if stored.empty:
                print "DEBUG: DF %s appears empty" % stored
                sessions = new_sessions
            else:
                sessions = stored.append(new_sessions)
            sessions.to_csv(csvs[ename])

        elif ename in ['pilot', 'unit']:
            if stored.empty:
                df = new_df
            else:
                df = stored.append(new_df)
            df.reset_index(inplace=True, drop=True)
            df.to_csv(csvs[ename])

        else:
            error = 'Cannot store DF to %s' % ename
            print error
            sys.exit(1)


def parse_osg_hostid(hostid):
    '''
    Heuristic: eliminate node-specific information from hostID.
    '''
    domain = None

    # Split domain name from IP.
    host = hostid.split(':')

    # Split domain name into words.
    words = host[0].split('.')

    # Get the words in the domain name that do not contain
    # numbers. Most hostnames have no number but there are
    # exceptions.
    literals = [l for l in words if not
                any((number in set('0123456789')) for number in l)]

    # Check for exceptions:
    # a. every word of the domain name has a number
    if len(literals) == 0:

        # Some hostname use '-' instead of '.' as word separator.
        # The parser would have returned a single word and the
        # any of that word may have a number.
        if '-' in host[0]:
            words = host[0].split('-')
            literals = [l for l in words if not
                        any((number in set('0123456789')) for number in l)]

            # FIXME: We do not check the size of literals.
            domain = '.'.join(literals)

        # Some hostnames may have only the name of the node. We
        # have to keep the IP to decide later on whether two nodes
        # are likely to belong to the same cluster.
        elif 'nod' in host[0]:
            domain = '.'.join(host)

        # FIXME: ad hoc parsing
        elif 'n0' in host[0]:
            domain = 'n0x.10.2.x.x'

        # The hostname is identified by an alphanumeric string
        else:
            domain = '.'.join(host)

    # Some hostnames DO have numbers in their name.
    elif len(literals) == 1:
        domain = '.'.join(words[1:])

    # Some hostname are just simple to parse.
    else:
        domain = '.'.join(literals)

    # FIXME: When everything else fails, ad hoc manipulations of
    #        domain string.
    if 'its.osg' in domain:
        domain = 'its.osg'
    elif 'nodo' in domain:
        domain = 'nodo'
    elif 'bu.edu' in domain:
        domain = 'bu.edu'

    return domain


def load_new_session(sid, sra, experiment, pdm, udm):

    # Initialize data structures for session DF when a session ID
    # is found that has not yet been stored.
    s = initialize_entity(ename='session')

    # Session properties: pilots and units.
    sp = sra.filter(etype='pilot', inplace=False)
    su = sra.filter(etype='unit', inplace=False)
    s['session'].append(sra)
    s['experiment'].append(experiment)
    s['TTC'].append(sra.ttc)
    s['nhost'].append(None)
    s['nunit'].append(len(su.get()))
    s['npilot'].append(len(sp.get()))
    s['npilot_active'].append(len(sp.timestamps(state='PMGR_ACTIVE')))
    s['nunit_done'].append(len(su.timestamps(state='DONE')))
    s['nunit_failed'].append(len(su.timestamps(state='FAILED')))

    # Pilots total durations.  NOTE: s initialization guarantees
    # the existence of duration keys.
    for duration in pdm.keys():
        s[duration].append(sp.duration(pdm[duration]))

    # Units total durations. NOTE: s initialization guarantees the
    # existence of duration keys.
    for duration in udm.keys():
        s[duration].append(su.duration(udm[duration]))

    # Return session as DF.
    session = pd.DataFrame(s, index=[sid])
    return session


def add_session_unique_hosts(sessions, pilots, stored_sessions):
    print '\n\nAdding number of unique hosts to sessions:'
    for sid in sessions.index:
        if pd.isnull(sessions.loc[sid]['nhost']):
            sessions.loc[sid, 'nhost'] = len(
                pilots[pilots['sid'] == sid]['hid'].unique())
            store_df(sessions, stored_sessions, ename='session')
            print '%s: %s hosts, stored in %s.' % \
                (sid, sessions.loc[sid]['nhost'], csvs['pilot'])

        else:
            print '%s: %s hosts already stored in %s' % \
                (sid, sessions.loc[sid]['nhost'], csvs['pilot'])
    return sessions


def add_unit_hosts(units, pilots, sessions, stored_units):
    print '\n\nAdding host and pilot IDs to units:'
    counter = 0
    for sid in sessions.index:
        sra = sessions.loc[sid]['session']
        pu_rels = sra.describe('relations', ['pilot', 'unit'])
        uids = units[units['sid'] == sid]['uid']
        for uid in uids:
            uix = units[(units['sid'] == sid) & (units['uid'] == uid)].index[0]
            if pd.isnull(units.loc[uix]['hid']):
                punit = [key[0] for key in pu_rels.items() if uid in key[1]][0]
                hid = pilots[(pilots['sid'] == sid) &
                             (pilots['pid'] == punit)]['hid'].tolist()[0]
                units.loc[uix, 'pid'] = punit
                units.loc[uix, 'hid'] = hid
                counter += 1
            else:
                print '%s:%s host ID already stored in %s' % \
                    (sid, uid, csvs['unit'])

        if counter:
            store_df(units, stored_units, ename='unit')
            print '%s: %s host and pilot IDs stored in %s.' % \
                (sid, counter, csvs['unit'])

    return units


def load_new_pilots(pdm, sessions):
    print '\nLoading pilots:'
    stored_pids = []

    # Calculate the duration for each state of each pilot of each run and
    # Populate the DataFrame  structure.
    for sid in sessions.index:
        sys.stdout.write('\n%s --- %s' %
                         (sessions.loc[sid, 'experiment'], sid))

        ps = initialize_entity(ename='pilot')
        stored_pilots = load_df(ename='pilot')

        # Did we already stored pilots of this session?
        if not stored_pilots['sid'].empty:
            stored_pids = stored_pilots[
                stored_pilots['sid'] == sid]['pid'].values.tolist()

        # Derive properties of each session's pilot.
        s = sessions.loc[sid, 'session'].filter(etype='pilot', inplace=False)
        for pid in sorted(s.list('uid')):
            # Skip session if its pilots have been already stored.
            if pid in stored_pids:
                sys.stdout.write('\n%s already stored in %s' %
                                 (pid, csvs['pilot']))
                continue

            sys.stdout.write('\n' + pid + ': ')
            ps['pid'].append(pid)
            ps['sid'].append(sid)
            ps['experiment'].append(sessions.loc[sid, 'experiment'])

            # Derive host ID for each pilot.
            pentity = s.get(uid=pid)[0]
            if pentity.cfg['hostid']:
                ps['hid'].append(parse_osg_hostid(pentity.cfg['hostid']))
            else:
                ps['hid'].append(None)

            # Derive durations of each session's pilot.
            for duration in pdm.keys():
                if duration not in ps.keys():
                    ps[duration] = []
                try:
                    ps[duration].append(pentity.duration(pdm[duration]))
                    sys.stdout.write(' %s' % duration)
                except:
                    print '\nWARNING: Failed to calculate duration %s' % \
                        duration
                    ps[duration].append(None)

        # Store session DF to csv.
        if ps['pid']:
            pilots = pd.DataFrame(ps)
            store_df(pilots, stored=stored_pilots, ename='pilot')
            print '\nstored in %s.' % csvs['pilot']

    # Returns everything we have stored. Worse case scenario, we reload what we
    # already have.
    stored_pilots = load_df(ename='pilot')
    # We need 'pid', 'sid' and 'hid'. Save memory.
    return stored_pilots.loc[:, ['pid', 'sid', 'hid']]


# TODO: Repeated code.
def load_new_units(udm, sessions):
    print '\n\nLoading units:'
    stored_uids = []

    # Calculate the duration for each state of each pilot of each run and
    # Populate the DataFrame  structure.
    for sid in sessions.index:
        sys.stdout.write('\n%s --- %s' %
                         (sessions.loc[sid, 'experiment'], sid))

        us = initialize_entity(ename='unit')
        stored_units = load_df(ename='unit')

        if not stored_units['sid'].empty:
            stored_uids = stored_units[
                stored_units['sid'] == sid]['uid'].values.tolist()

        # Derive properties of each session's pilot.
        s = sessions.loc[sid, 'session'].filter(etype='unit', inplace=False)
        for uid in sorted(s.list('uid')):

            # Skip session if its pilots have been already stored.
            if uid in stored_uids:
                sys.stdout.write('\n%s already stored in %s' %
                                 (uid, csvs['unit']))
                continue

            sys.stdout.write('\n' + uid + ': ')
            us['uid'].append(uid)
            us['sid'].append(sid)
            us['hid'].append(None)
            us['experiment'].append(sessions.loc[sid, 'experiment'])

            # Derive durations of each session's pilot.
            # sf = s.filter(uid=uid, inplace=False)
            uentity = s.get(uid=uid)[0]
            for duration in udm.keys():
                if duration not in us.keys():
                    us[duration] = []
                try:
                    if duration == 'U_AGENT_EXECUTING':
                        if 'AGENT_STAGING_OUTPUT_PENDING' in \
                                uentity.states.keys() and \
                           'FAILED' in uentity.states.keys():
                                us[duration].append(None)
                                continue
                    us[duration].append(uentity.duration(udm[duration]))
                    sys.stdout.write(' %s' % duration)
                except:
                    print '\nWARNING: Failed to calculate duration %s' % \
                        duration
                    us[duration].append(None)

        # Store session DF to csv.
        if us['uid']:
            units = pd.DataFrame(us)
            store_df(units, stored=stored_units, ename='unit')
            print '\nstored in %s.' % csvs['unit']

    # Returns everything we have stored. Worse case scenario, we reload what we
    # already have.
    stored_units = load_df(ename='unit')
    return stored_units


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    datadir = '../test/'
    experiment_tag = 'exp'

    # Global constants
    # File names where to save the DF of each entity of each session.
    csvs = {'session': '%ssessions.csv' % datadir,
            'pilot'  : '%spilots.csv' % datadir,
            'unit'   : '%sunits.csv' % datadir}

    # Model of pilot durations.
    pdm = {'P_PMGR_SCHEDULING': ['NEW',
                                 'PMGR_LAUNCHING_PENDING'],
           'P_PMGR_QUEUING'   : ['PMGR_LAUNCHING_PENDING',
                                 'PMGR_LAUNCHING'],
           'P_LRMS_SUBMITTING': ['PMGR_LAUNCHING',
                                 'PMGR_ACTIVE_PENDING'],
           'P_LRMS_QUEUING'   : ['PMGR_ACTIVE_PENDING',
                                 'PMGR_ACTIVE'],
           'P_LRMS_RUNNING'   : ['PMGR_ACTIVE',
                                 ['DONE', 'CANCELED', 'FAILED']]}

    # Model of unit durations.
    udm = {'U_UMGR_SCHEDULING'   : ['NEW',
                                    'UMGR_SCHEDULING_PENDING'],
           'U_UMGR_BINDING'      : ['UMGR_SCHEDULING_PENDING',
                                    'UMGR_SCHEDULING'],
           #    'I_UMGR_SCHEDULING'   : ['UMGR_SCHEDULING',
           #                             'UMGR_STAGING_INPUT_PENDING'],
           #    'I_UMGR_QUEING'       : ['UMGR_STAGING_INPUT_PENDING',
           #                             'UMGR_STAGING_INPUT'],
           #    'I_AGENT_SCHEDULING'  : ['UMGR_STAGING_INPUT',
           #                             'AGENT_STAGING_INPUT_PENDING'],
           #    'I_AGENT_QUEUING'     : ['AGENT_STAGING_INPUT_PENDING',
           #                             'AGENT_STAGING_INPUT'],
           #    'I_AGENT_TRANSFERRING': ['AGENT_STAGING_INPUT',
           #                             'AGENT_SCHEDULING_PENDING'],
           'U_AGENT_QUEUING'     : ['AGENT_SCHEDULING_PENDING',
                                    'AGENT_SCHEDULING'],
           'U_AGENT_SCHEDULING'  : ['AGENT_SCHEDULING',
                                    'AGENT_EXECUTING_PENDING'],
           'U_AGENT_QUEUING_EXEC': ['AGENT_EXECUTING_PENDING',
                                    'AGENT_EXECUTING'],
           'U_AGENT_EXECUTING'   : ['AGENT_EXECUTING',
                                    'AGENT_STAGING_OUTPUT_PENDING']}
    #    'O_AGENT_QUEUING'     : ['AGENT_STAGING_OUTPUT_PENDING',
    #                             'AGENT_STAGING_OUTPUT'],
    #    'O_UMGR_SCHEDULING'   : ['AGENT_STAGING_OUTPUT',
    #                             'UMGR_STAGING_OUTPUT_PENDING'],
    #    'O_UMGR_QUEUING'      : ['UMGR_STAGING_OUTPUT_PENDING',
    #                             'UMGR_STAGING_OUTPUT'],
    #    'O_UMGR_TRANSFERRING' : ['UMGR_STAGING_OUTPUT',
    #                             ['DONE', 'CANCELED', 'FAILED']]}

    # Load stored sessions, pilots and units csv files.
    stored_sessions = load_df(ename='session')
    stored_pilots = load_df(ename='pilot')
    stored_units = load_df(ename='unit')

    # Get sessions ID, experiment number and RA object. Assume:
    # datadir/exp*/sessiondir/session.json.
    print '\nLoading sessions:\n'
    for path in glob.glob('%s/%s*' % (datadir, experiment_tag)):
        experiment = path.split('/')[-1:][0]
        for sdir in glob.glob('%s/*' % path):
            sid = glob.glob('%s/*.json' % sdir)[0].split('/')[-1:][0][:-5]

            # Check whether SID of json file name is the same SID of
            # directory name.
            if sid == sdir.split('/')[-1:][0]:

                # RA objects cannot be serialize: every RA session object need
                # to be constructed at every run. TODO: Maybe make RA session
                # objects serializable in msgpack format?
                sra = ra.Session(sid, 'radical.pilot', src=sdir)

                # Skip session if we have already saved it on disk. No need to
                # recompute all the durations and properties for the session
                # but we need to add the RA session object back to the stored
                # sessions DF.
                if sid in stored_sessions.index.tolist():
                    stored_sessions.loc[sid, 'session'] = sra
                    stored_sessions.loc[sid, 'experiment'] = experiment

                    # Session is a DF.
                    session = stored_sessions.loc[[sid]].copy()
                    session.loc[sid, 'session'] = sra
                    print '%s --- %s already stored in %s' % \
                        (experiment, sid, csvs['session'])

                else:
                    # Initialize data structures for session DF when a session
                    # ID is found that has not yet been stored.
                    session = load_new_session(sid, sra, experiment, pdm, udm)

                    # Store session DF to csv and make it available in
                    # stored_sessions.
                    store_df(session, stored=stored_sessions, ename='session')
                    stored_sessions = load_df(ename='session')
                    print '%s --- %s stored in %s' % \
                        (experiment, sid, csvs['session'])

                pilots = load_new_pilots(pdm, session)
                units = load_new_units(udm, session)
                session = add_session_unique_hosts(session, pilots, stored_sessions)
                units = add_unit_hosts(units, pilots, session, stored_units)

            else:
                error = 'ERROR: session folder and json file name differ'
                print '%s: %s != %s' % (error, sdir, sid)

    sys.exit(0)

    # stored_sessions = load_df(sessions_csv, ss)
    pilots = load_new_pilots(pdm, sessions)
    units = load_new_units(udm, sessions)

    # Add values across DFs.
    sessions = add_session_unique_hosts(sessions, pilots)
    units = add_unit_hosts(units, pilots, sessions)