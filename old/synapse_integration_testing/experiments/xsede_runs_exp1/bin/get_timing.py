#!/usr/bin/env python
"""Extracts timings from the given session.
"""

import os
import sys

import pandas as pd
#import matplotlib.pyplot as plt
import radical.pilot.utils as rpu
import radical.utils as ru

__author__ = "Matteo Turilli"
__copyright__ = "Copyright 2015, The AIMES Project"
__license__ = "MIT"
__credits__ = ["Andre Merzky"]


# -----------------------------------------------------------------------------
#
def usage(msg=None, noexit=False):

    if msg:
        print "\n      Error: %s" % msg

    print """
    usage   : %s <sid> [<timing>] [<n_pilots>]
    example : %s 5490ba7174df926284f8ef48 [Tx] [3]

    arguments
        <sid>        : session id
        [<timing>]   : optional -- type of timing
        [<n_pilots>] : optional -- number of pilots in the session required to
                                   have run at least a unit

    The tool extracts timings from the given session. By default, the tool
    output all the available timings. If a timing is specified, only that
    timing is outputed. Valid timings are:

        - Tx  : time spent from when the first Compute Unit has been scheduled
                for execution on an active pilot to the time when the last
                Compute Unit has finished.

        - Th  : time spent from the start of the session to when the first
                Compute Unit has been executed. Th includes the following
                events:

                0.  creating session;
                1.  creating RP managers;
                2.  describing the pilots;
                3.  describing the units;
                4.  submitting the pilots to the target resources;
                5.  pilot(s) queuing time on the remote resource;
                6.  [staging data, in case of early binding];
                7.  pilot becoming active - i.e. agent bootstrap;
                8.  [staging data, for queuing time < staging time in case of
                    early binding; always for late binding];
                9.  scheduling CUs.

        - TTC : total time to completion of the whole session. TTC includes
                the following events:

                0.  creating session;
                1.  creating RP managers;
                2.  describing the pilots;
                3.  describing the units;
                4.  submitting the pilots to the target resources;
                5.  pilot(s) queuing time on the remote resource;
                6.  [staging data, in case of early binding];
                7.  pilot becoming active - i.e. agent bootstrap;
                8.  [staging data, for queuing time < staging time in case of
                    early binding; always for late binding];
                9.  scheduling CUs;
                10. Executing CUs;
                11. [Staging data out]
                12. [Canceling pilots]
                13. Deleting pilot and unit managers
                14. Closing session

        - Tc  : aggregated time-core available, the sum of #cores * pilot
                duration. Note that pilot duration is different from pilot
                walltime. Walltime = max duration, duration the time during
                which the pilot has been effectively active. Tc includes the
                following events:

                0.  pilot(s) become ACTIVE.
                1.  pilot(s) become DONE/CANCEL.

        - T?  : aggregated time spent staging data in (in the code as Ti).

        - T!  : aggregated time spent staging data out (in the code as To).

        - Ts  : aggregated time spent staging data.

    """ % (sys.argv[0], sys.argv[0])

    if msg:
        sys.exit(1)

    if not noexit:
        sys.exit(0)

# -----------------------------------------------------------------------------
#
def collapse_ranges(ranges):
    """
    given be a set of ranges (as a set of pairs of floats [start, end] with
    'start <= end'. This algorithm will then collapse that set into the
    smallest possible set of ranges which cover the same, but not more nor
    less, of the domain (floats).

    We first sort the ranges by their starting point. We then start with the
    range with the smallest starting point [start_1, end_1], and compare to the
    next following range [start_2, end_2], where we now know that start_1 <=
    start_2. We have now two cases:

    a) when start_2 <= end_1, then the ranges overlap, and we collapse them
       into range_1: range_1 = [start_1, max[end_1, end_2]

    b) when start_2 > end_2, then ranges don't overlap. Importantly, none of
       the other later ranges can ever overlap range_1. So we move range_1 to
       the set of final ranges, and restart the algorithm with range_2 being
       the smallest one.

    Termination condition is if only one range is left -- it is also moved to
    the list of final ranges then, and that list is returned.
    """

    final = []

    # sort ranges into a copy list
    _ranges = sorted (ranges, key=lambda x: x[0])
#    print _ranges
    START = 0
    END = 1

    base = _ranges[0] # smallest range

    for _range in _ranges[1:]:

        if _range[START] <= base[END]:

            # ranges overlap -- extend the base
            base[END] = max(base[END], _range[END])

        else:

            # ranges don't overlap -- move base to final, and current _range
            # becomes the new base
            final.append(base)
            base = _range

    # termination: push last base to final
    final.append(base)
    return final


#------------------------------------------------------------------------------
#
def get_Toverlap(df, start_state, stop_state):
    '''
    Helper function to create the list of lists from which to calculate the
    overlap of the elements of a DataFrame between the two boundaries passed as
    arguments.
    '''

    overlap = 0
    ranges = []
    tmp = 0.0

#    print start_state, df[start_state].max()
#    print stop_state, df[stop_state].max()
    for index, row in df.iterrows():
        if not pd.isnull(row[start_state]) and not pd.isnull(row[stop_state]):
            ranges.append([row[start_state], row[stop_state]])

    '''
    There have been instances where the individual time arrays in ranges
    appeared out of order. The error was originally suspected to be found
    in only large number of course and lead to negative numbers, but this
    occurs more often than not. Further investigation is required to
    understand how timings are record. The below fix is temporary and
    experimental - Ming
    '''

    for rng in ranges:
       if rng[0] > rng[1]:
            tmp = rng[0]
            rng[0] = rng[1]
            rng[1] = tmp

    for crange in collapse_ranges(ranges):
        overlap += crange[1] - crange[0]
#        print overlap, type(crange[1])

    return overlap


#------------------------------------------------------------------------------
#
def roundup(x, y):
    return x if x % y == 0 else x + y - x % y


#------------------------------------------------------------------------------
#
def plot_overlaps(sf, uf, pilots, pdir):
    '''
    Plot a diagram showing the duration for each state on a single timeline.
    '''

    colors = ['#64B5CD', '#8DAFFD', '#B8CFF8', '#EEEFFF']

    sid = sf.iloc[0]['sid']
    npilots = int(sf.iloc[0]['n_pilots'])
    nunits = int(sf.iloc[0]['n_units'])
    binding = sf.iloc[0]['binding']
    time_distr = sf.iloc[0]['time_distr']

    pdir = pdir+'/'+binding+'_'+time_distr

    title = "Execution Process Session %s" % sid

    stbinding = "Binding: %s; " % binding
    stpilot = "Pilots: %s/%s; " % (len(pilots), npilots)
    stunits = "Units: %s/%s; " %  (len(uf), nunits)

    if time_distr == 'gauss':
        sttdistr = "Time distribution: semi-Gaussian."
    else:
        sttdistr = "Time distribution: %s." % time_distr

    subtitle = stpilot + stunits + stbinding + sttdistr

    ofile = "%s/plot-overlap_pilots-%s_units-%s_sid-%s.pdf" % (
        pdir, npilots, nunits, sid)

    plt.figure(figsize=(17, 10))

    # xlen = roundup(int(sf.iloc[0]['finished']),
    #                10**(len(str(int(sf.iloc[0]['finished'])))-2))
    xlen = roundup(int(sf.iloc[0]['finished']), 10)
    ylen = roundup(len(uf), 10**(len(str(len(uf)))-1))

    plt.axis([0,xlen, 0,ylen])

    plt.ylabel('Number of CUs')
    plt.xlabel('Time (s)')

    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.title(subtitle)

    # Radical.pilot scheduling overhead (??)
    plt.hlines(uf.index.get_values(),
               uf['ExecutingPending'],
               uf['Scheduling'],
               label='PO_sched',
               color='#000000',
               linewidth=2)

    # Radical.pilot scheduling overhead (??)
    plt.hlines(uf.index.get_values(),
               uf['Scheduling'],
               uf['Executing'],
               color='#000000',
               linewidth=2)

    # Radical.pilot wait for executing CU. Setup time + queuing time.
    plt.hlines(uf.index.get_values(),
               uf['New'],
               uf['PendingInputStaging'],
               label='Tw',
               color='#DDDCDB',
               linewidth=10)

    # Queue time for each pilot
    for idx in pilots.index.get_values():
        print pilots.index.get_values()
        c = colors[idx]
        plt.hlines(uf[uf['pid'] == pilots['pid'][idx]].index.get_values(),
                   pilots['PendingLaunch'][idx],
                   pilots['Active'][idx],
                   label="Tq%s" % idx,
                   color=c,
                   linewidth=8)

    # Getting ready to stage data in.
    plt.hlines(uf.index.get_values(),
               uf['PendingInputStaging'],
               uf['StagingInput'],
               label='Ti/To',
               color='#DC5E4B',
               linewidth=4)

    # Ti staging data in.
    plt.hlines(uf.index.get_values(),
               uf['StagingInput'],
               uf['ExecutingPending'],
               color='#DC5E4B',
               linewidth=4)

    # CU execution.
    plt.hlines(uf.index.get_values(),
               uf['Executing'],
               uf['PendingOutputStaging'],
               label='Tx',
               color='#AFDD8A',
               linewidth=2)

    # Getting ready to stage data out.
    plt.hlines(uf.index.get_values(),
               uf['PendingOutputStaging'],
               uf['StagingOutput'],
               color='#DC5E4B',
               linewidth=1)

    # Staging data out.
    plt.hlines(uf.index.get_values(),
               uf['StagingOutput'],
               uf['Done'],
               color='#DC5E4B',
               linewidth=1)

    # Legend outside the diagram
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
    #plt.legend()

    plt.savefig(ofile)


# -----------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = None
    q_pilots = None
    timing = None
    timings = {}
    #pdir = os.environ['PLOT_DIR']

    cachedir = os.getcwd()
    dburl = 'mongodb://mingtaiha:mingtaiha@ds053838.mongolab.com:53838/hicomb'
    mongo, db, dbname, cname, pname = ru.mongodb_connect(str(dburl))
    
    if len(sys.argv) <= 1:
        usage("insufficient arguments -- need session ID")

    if len(sys.argv) > 4:
        usage("too many arguments -- no more than 3")

    if len(sys.argv[1]) < 20:
        usage("illegal session token -- valid e.g. 54b1c5d523769c2f1b55dffd")
    else:
        session = sys.argv[1]

    if len(sys.argv) > 2:
        timing = sys.argv[2]

    if len(sys.argv) > 3:
        q_pilots = int(sys.argv[3])

#    print session
    s_frame, p_frame, u_frame = rpu.get_session_frames(session, dburl, cachedir)
  
    #print p_frame['n_units'][0]

    # Add metadata to the session DF
    s_frame['binding'] = os.environ['BINDING']
    s_frame['time_distr'] = os.environ['TIME_DISTR']

    # Drop failed CUs
    units = u_frame[u_frame.Done.notnull()]

    # print units.ix[units['Scheduling'].idxmin()]['Scheduling']
    u_first = units.ix[units['Scheduling'].idxmin()]['Scheduling']

    # u_last = units.ix[units['finished'].idxmax()]['finished']
    u_last = units.ix[units['Done']].idxmax()['Done']

    pilots = p_frame[p_frame['n_units'] > 0]
    cores = pilots['cores'].sum()

    # Calculate timings by overlap
#    PO_setup = get_Toverlap(units, 'New',                  'PendingInputStaging')
#    Ti_trsfr = get_Toverlap(units, 'PendingInputStaging',  'StagingInput')
    #PO_setup = get_Toverlap(units, 'New',                  'StagingInput')
    #Ti_trsfr = get_Toverlap(units, 'PendingInputStaging',  'StagingInput')
#    Ti_setup = get_Toverlap(units, 'StagingInput',         'ExecutingPending')
#    PO_exec  = get_Toverlap(units, 'ExecutingPending',     'Scheduling')
#    Tx_sched = get_Toverlap(units, 'Scheduling',           'Executing')
#    Tx_exec  = get_Toverlap(units, 'Executing',            'PendingOutputStaging')
#    To_setup = get_Toverlap(units, 'PendingOutputStaging', 'StagingOutput')
#    To_trsfr = get_Toverlap(units, 'StagingOutput',        'Done')

    # TODO: PendingOutputStaging is not populated by the dataframe module so
    # the overhead of the staging out is mistakenly aggegated into Tx.
    # Tx_exec  = get_Toverlap(units, 'Executing', 'PendingOutputStaging')
    # To_setup = get_Toverlap(units, 'PendingOutputStaging', 'StagingOutput')

    # NOTE: This TTC includes the overlapping among timings - Tx, Ts, Th, ...
    # The difference between TTC and the sum of the timings needs to be
    # normalized. A trivial normalization is to distributed the overalap
    # equally among all the states.

#    print s_frame
#    print p_frame
#    print u_frame.iloc[-1]
#    print Tx_sched, Tx_exec

#    timings['TTC'] = s_frame['finished'][0]

#    timings['T_New'] = get_Toverlap(units, 'New', 'Scheduling')
#    timings['T_USch'] = get_Toverlap(units, 'Scheduling', 'PendingInputStaging')
#    timings['T_USIP'] = get_Toverlap(units, 'PendingInputStaging', 'StagingInput')
#    timings['Tq'] = get_Toverlap(units, 'StagingInput', 'AgentStagingInputPending')
#    timings['T_ASIP'] = get_Toverlap(units, 'AgentStagingInputPending', 'AgentStagingInput')
#    timings['T_ASI'] = get_Toverlap(units, 'AgentStagingInput', 'ExecutingPending')
#    timings['T_EP'] = get_Toverlap(units, 'ExecutingPending', 'Executing')
#    timings['Te'] = get_Toverlap(units, 'Executing', 'AgentStagingOutputPending')
#    timings['T_ASOP'] = get_Toverlap(units, 'AgentStagingOutputPending', 'AgentStagingOutput')
#    timings['T_ASO'] = get_Toverlap(units, 'AgentStagingOutput', 'PendingOutputStaging')
#    timings['T_USOP'] = get_Toverlap(units, 'PendingOutputStaging', 'StagingOutput')
#    timings['T_USO'] = get_Toverlap(units, 'StagingOutput', 'Done') 

#    print p_frame.columns
#    print units.columns

    timings['TTC'] = s_frame['finished'][0]
    timings['Tq'] = get_Toverlap(p_frame, 'PendingActive', 'Active')
    timings['Ti'] = get_Toverlap(units, 'AgentStagingInputPending', 'AgentStagingInput') - timings['Tq']
    timings['To'] = get_Toverlap(units, 'AgentStagingOutputPending', 'PendingOutputStaging')
    timings['Tx'] = get_Toverlap(units, 'Executing', 'AgentStagingOutputPending')
    timings['Ts'] = timings['Ti'] + timings['To']

#
#   The following code was used to investigate the state diagram of RP 0.40. This has since been resolved
#

    '''
    pilot_timings = []
    units_timings = []
    pilot_stages = ['New', 'Launching', 'PendingActive', 'Active']
    units_stages = ['New', 'Scheduling', 'PendingInputStaging', 'StagingInput', 'AgentStagingInputPending', 'AgentStagingInput', \
                'ExecutingPending', 'Executing', 'AgentStagingOutputPending', 'AgentStagingOutput', 'PendingOutputStaging', 'StagingOutput', 'Done']

    for pilot_stage in pilot_stages:
        pilot_timings.append([str(pilot_stage), p_frame[pilot_stage].min(), p_frame[pilot_stage].max()])

    for unit_stage in units_stages:
        units_timings.append([unit_stage, units[unit_stage].min(), units[unit_stage].max()])

    
    import csv
    
    pilot_name = session + "_pilots.csv"
    unit_name = session + "_units.csv"

    print pilot_timings
    print units_timings

    with open(pilot_name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(pilot_timings)

    with open(unit_name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(units_timings)
    '''

#    timings['Th'] = units.ix[units['Scheduling'].idxmin()]['Scheduling']
#    timings['Tc'] = (pilots['finished'] - pilots['started']).sum() / len(pilots)
   
#    timings['Tx'] = Tx_sched + Tx_exec
#    timings['Tx'] = Tx_exec

    #timings['Ti'] = Ti_setup + Ti_trsfr
    #timings['Ti'] = Ti_setup
#    timings['Ti'] = get_Toverlap(units, 'PendingInputStaging',  'ExecutingPending')

    #timings['To'] = To_setup + To_trsfr
#    timings['To'] = get_Toverlap(units, 'PendingOutputStaging',  'Done')
    
#    timings['Ts'] = timings['Ti'] + timings['To']

    # TODO: Once PandingOutputStaging will be available, calculate To by sum.
    #timings['To'] = To_setup + To_trsfr

    # NOTE: this measure the average staging time for each CU, not the total
    # amount of time spent doing staging during a run. As such, these values
    # cannot be used in a comparison with the TTC of the run. For that
    # comparison, the total overlap of the staging times for each CU need to be
    # calculated.
    #timings['Tx'] = u_last - u_first
    #timings['To'] = (units['Done'] - units['StagingOutput']).sum() / len(units)
    #timings['Ti'] = (units['ExecutingPending'] - units['StagingInput']).sum() / len(units)
    #timings['Ts'] = timings['Ti'] + timings['To']

    # TODO: calculate the intersection between Ti and Tc for early binding when
    # the two timings are indipendent.
    #PO = PO_setup + PO_exec
    #Tq = p_frame['Active'].sum() - p_frame['PendingLaunch'].sum()

    # Write a plot for the session with the state overlaps
    # plot_overlaps(s_frame, units, pilots, pdir)

    #print timings['Ti']
    #print timings['To']
    #print timings['Tx']

    if timing:

        if not q_pilots:
            print timings[timing]

        elif q_pilots == len(pilots):
            print timings[timing]

    else:

        ts = ["%s:%s" % (k, v) for k, v in timings.iteritems()]
        out = ",".join(str(e) for e in ts)
        out += ";p%s" % len(pilots)

        if not q_pilots:
            print out

        elif q_pilots == len(pilots):
            print out
