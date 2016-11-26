import os
import sys
import pandas as pd
import radical.utils as ru
import radical.pilot.utils as rpu
# import matplotlib.pylab as plt


if len(sys.argv) == 2:
        session = sys.argv[1]
else:
    print("insufficient arguments -- need session ID")

cachedir = os.getcwd()
dburl = os.environ['RADICAL_PILOT_DBURL']
mongo, db, dbname, cname, pname = ru.mongodb_connect(str(dburl))
sf, pf, uf = rpu.get_session_frames(session, db, cachedir)

sctr = uf[['pid', 'PendingInputStaging', 'Done']]

print sctr

sctr.pid.replace({'pilot.0000': '1'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0001': '2'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0002': '3'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0003': '4'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0004': '5'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0005': '6'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0006': '7'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0007': '8'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0008': '9'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0009': '10'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0010': '11'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0011': '12'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0012': '13'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0013': '14'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0014': '15'}, inplace=True, regex=True)
sctr.pid.replace({'pilot.0015': '16'}, inplace=True, regex=True)
sctr.pid = pd.to_numeric(sctr.pid)

sctr.to_csv('cus.csv')

# sctr.plot(kind='scatter', x='pid', y='PendingInputStaging');
# plt.show()

# USELESS CRAP.

# def printdf(x, rows=None):
#     pd.set_option('display.max_rows', len(x),
#                   'display.max_columns', 10000)
#     if rows:
#         print x[0:rows]
#     else:
#         print(x)
#     pd.reset_option('display.max_rows')

# if __name__ == '__main__':

#     # we use a reporter class for nicer output
#     report = ru.LogReporter(name='radical.pilot')

#     # use the sid specified as argument, otherwise run a test
#     if len(sys.argv) == 2:
#         sid = sys.argv[1]
#     else:
#         report.exit('Usage:\t%s [sid]\n\n' % sys.argv[0])

#     # fetch profiles for all pilots
#     profiles = ['/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentExecutingComponent_POPEN.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentExecutingComponent_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentExecutingWatcher_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentHeartbeatWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentHeartbeatWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentStagingInputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentStagingInputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentStagingOutputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentStagingOutputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentUpdateWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentUpdateWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.AgentWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.bootstrap_3.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.SchedulerContinuous.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/agent_0.SchedulerContinuous.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0000/bootstrap_1.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentExecutingComponent_POPEN.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentExecutingComponent_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentExecutingWatcher_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentHeartbeatWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentHeartbeatWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentStagingInputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentStagingInputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentStagingOutputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentStagingOutputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentUpdateWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentUpdateWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.AgentWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.bootstrap_3.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.SchedulerContinuous.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/agent_0.SchedulerContinuous.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0001/bootstrap_1.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentExecutingComponent_POPEN.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentExecutingComponent_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentExecutingWatcher_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentHeartbeatWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentHeartbeatWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentStagingInputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentStagingInputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentStagingOutputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentStagingOutputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentUpdateWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentUpdateWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.AgentWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.bootstrap_3.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.SchedulerContinuous.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/agent_0.SchedulerContinuous.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0002/bootstrap_1.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentExecutingComponent_POPEN.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentExecutingComponent_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentExecutingWatcher_POPEN.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentHeartbeatWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentHeartbeatWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentStagingInputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentStagingInputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentStagingOutputComponent.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentStagingOutputComponent.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentUpdateWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentUpdateWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentWorker.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.AgentWorker.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.bootstrap_3.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.SchedulerContinuous.0.child.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/agent_0.SchedulerContinuous.0.prof', u'/tmp/rp.session.Matteos-MacBook-Pro.local.mturilli.016780.0000//pilot.0003/bootstrap_1.prof']

#     # combine into a single profile
#     profile = rpu.combine_profiles(profiles)

#     # derive a global data frame
#     frame = rpu.prof2frame(profile)

#     # split into session / pilot / unit frames
#     sf, pf, uf = rpu.split_frame(frame)

#     # derive some additional 'info' columns, which contains some commonly used
#     # tags
#     rpu.add_info(uf)

#     # add a 'state_from' columns which signals a state transition
#     rpu.add_states(uf)

#     print uf.columns.tolist()

#     css = uf.dropna()
#     cstart = css[(css.state == 'PendingInputStaging')]
#     cdone = css[(css.state == 'Done')]
#     cstart = cstart[['uid', 'time']]
#     cdone = cdone[['uid', 'time']]

#     cstart.columns = ['uid', 'start']
#     cdone.columns = ['uid', 'done']

#     cus = pd.merge(left=cstart, right=cdone, left_on='uid', right_on='uid')

#     cstart.to_csv('cu_start.csv')
#     cdone.to_csv('cu_done.csv')
#     cus.to_csv('cus.csv')

    # print "Start"

    # for index, row in cu_start.iterrows():
    #         print "uid: %-20s | state: %-25s | time: %-20s" % \
    #                 (row['uid'], row['state'], row['time'])

    # print "Finish"

    # for index, row in cu_finish.iterrows():
    #         print "uid: %-20s | state: %-25s | time: %-20s" % \
    #                 (row['uid'], row['state'], row['time'])


    # print printdf(sf, 100)
    # print printdf(pf, 100)
    # print printdf(uf, 100)
    # print pf[0:10]
    # print uf[0:10]

    # plt.scatter(cu_start.time, cu_done.time)

    # cu_start.plot(kind='scatter', x='uid', y='start');
