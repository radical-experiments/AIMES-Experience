import saga

ctx = saga.Context("ssh")
ctx.user_id = "mha"
#ctx.user_id = "tg829619"
session = saga.Session()
session.add_context(ctx)

js = saga.job.Service("condor+ssh://xd-login.opensciencegrid.org/", session=session)
#js = saga.job.Service("slurm+ssh://stampede.tacc.utexas.edu/", session=session)
jd = saga.job.Description()
jd.executable = "/bin/sleep"
jd.arguments = '60'
jd.total_cpu_count = 1
#jd.queue = "normal"
#jd.project = "TG-MCB090174"
jd.project = "TG-CCR140028"
jd.wall_time_limit = 10
myjob = js.create_job(jd)
myjob.run()
#myjob = js.run_job(jd)
print "myjob type: ", type(myjob)
myjob.wait()

