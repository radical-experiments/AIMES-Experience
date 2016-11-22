# Characterization of Synapse Accuracy and Consistency

We use Synapse to profile and then emulate a specific simulation performed via
AMBER, a software package that simulates force fields for the dynamics of
biomolecules. We profile and emulate exclusively the amount of FLOPS required by
the specific simulation we choose to perform its computational tasks. We do not
profile and emulate the I/O patterns distinguishing the execution of the chosen
simulation, irrespective of whether they are performed in memory, on disk, or
over the network.

Our approach to profile and simulation correlates the time taken to compute a
certain amount of FLOPS and the speed of the processor on which this computation
is performed. Nonetheless, as we are not able to perform the emulation in
protected mode and directly on the processor, a certain amount of architectural
and software overheads is to be expected. For this reason, we need to consider
both the consistency and the accuracy of both our profiling and simluation.

We consider the profile of an execution of a software package to be accurate
when it cacluates the effective number of flops that that execution requires.
The profile is consistent when multiple instances of profiling returns the same
amount of flops for the same execution. Analogously, we consider an emulation of
the profiled execution to be accurate when the time taken by the software
package to compute a number of flops on a given machine is the same time taken
by our emulator on that same machine. An emulation is consistent when multiple
runs of the same profile on the same machine require the same amount of time.

Here the results of our charactererizations of Synapse for the AMBER simulation
of ... steps of the dynamics of a ... molucule. This simulation is used by the
group ... and, as such, represent a real-life use case.

## Profiler Accuracy and Consistency

*   Accuracy:
    1.  &#916; #FLOPS AMBER and Synapse
    2.  &#916; #FLOPS AMBER machine *n* and *m* == &#916; #FLOPS Synapse machine *n* and *m* 
*   Consistency:
    1.  &#916; #FLOPS Synapse runs on machine *n*
    2.  &#916; #FLOPS Synapse runs on machine *n* and machine *m*

| # Execution | FLOPS Amber M1 | FLOPS Synapse M1 | FLOPS Amber M2 | FLOPS Synapse M2  | FLOPS Amber M3 | FLOPS Synapse M3 |
| ----------- | -------------- | ---------------- | -------------- | ----------------- | -------------- | ---------------- |
| 1           |       N        |        N         |     N          |           N       |        N       |         N        |
| 2           |       N        |        N         |     N          |           N       |        N       |         N        |
| 3           |       N        |        N         |     N          |           N       |        N       |         N        |
| 4           |       N        |        N         |     N          |           N       |        N       |         N        |
| 5           |       N        |        N         |     N          |           N       |        N       |         N        |
| 6           |       N        |        N         |     N          |           N       |        N       |         N        |
| 7           |       N        |        N         |     N          |           N       |        N       |         N        |

*   Relative error of profile accuracy Machine 1:
*   Relative error of profile accuracy Machine 2:
*   Relative error of profile accuracy Machine 3:
