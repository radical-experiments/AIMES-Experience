# Characterization of Synapse Accuracy and Consistency

We use Synapse to profile and then emulate a specific simulation performed via
AMBER, a software package that simulates force fields for the dynamics of
biomolecules. We profile and emulate exclusively the amount of FLOPS required by
the specific simulation we choose to perform its computational tasks. We do not
profile and emulate the I/O patterns of the simulation, irrespective of whether
they are performed in memory, on disk, or over the network.

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

We measure the accuracy of the Synapse profiler against the behavior of an AMBER simulation: the more accurate the profiling, the more similar are the number of FLOPS performed by AMBER and the number of FLOPS returned by the profiler.

We measure the consistency of the profiler against repeated profiling. We
profile the same AMBER simulation multiple times on a machine and calculate the
standard deviation (STD) of the obtained set of number of FLOPS. The lower the
STD, the more consistent the profiling.

We also compare both accuracy and consistency across machines. The more similar
the accuracy across machine, the more architecture+environment independent the
accuracy of the profiler. Note: this does not mean that the value of MIPS
returned by the profiler is the same on each machine but that the difference
between that value and the one measured for AMBER is (ideally) invariant across
machines. We use the same reasoning with the STD of multiple profilings on
multiple machines: the distribution can be different but (ideally) the STD is
the same.


| # Execution | FLOPS Amber M1 | FLOPS Synapse M1 | FLOPS Amber M2 | FLOPS Synapse M2  | FLOPS Amber M3 | FLOPS Synapse M3 |
| ----------- | -------------- | ---------------- | -------------- | ----------------- | -------------- | ---------------- |
| 1           |       N        |        N         |     N          |           N       |        N       |         N        |
| 2           |       N        |        N         |     N          |           N       |        N       |         N        |
| 3           |       N        |        N         |     N          |           N       |        N       |         N        |
| 4           |       N        |        N         |     N          |           N       |        N       |         N        |
| 5           |       N        |        N         |     N          |           N       |        N       |         N        |
| 6           |       N        |        N         |     N          |           N       |        N       |         N        |
| 7           |       N        |        N         |     N          |           N       |        N       |         N        |


## Emulation Accuracy and Consistency
