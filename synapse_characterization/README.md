
# Characterization of Synapse Accuracy and Consistency

We use Synapse to profile and then emulate a specific simulation performed via
AMBER, a software package that simulates force fields for the dynamics of
biomolecules. We profile and emulate exclusively the amount of FLOPS required by
the specific simulation we choose to perform its computational tasks. We do not
profile and emulate the I/O patterns of the simulation, irrespective of whether
they are performed in memory, on disk, or over the network.

Our approach to profile and emulate correlates the time taken to compute a
certain amount of FLOPS and the speed of the processor on which this computation
is performed. Nonetheless, as we are not able to perform the emulation in
protected mode and directly on the processor, a certain amount of architectural
and software overhead is to be expected.  Further, any concurrent system load
will influence both executed and emulated simulation performance.  For this reason, 
we need to consider both the consistency and the accuracy of these timings.

We consider the profile of an execution of a software package to be accurate
when it measures the effective number of flops that that execution performed.
The profile is consistent when multiple instances of profiling returns the same
amount of flops for the same execution. Analogously, we consider an emulation of
the profiled execution to be accurate when the time taken by the simulation
software to compute that number of flops on any given machine is the same time
as taken by our emulator on that same machine. An emulation is consistent when
multiple runs of the same profile on the same machine require the same amount of
time.

Here the results of our charactererizations of Synapse for the AMBER simulation
of ... steps of the dynamics of a ... moleucule. This simulation is used by the
group ... and, as such, represent a real-life use case.


#  Experiment Setup
## Hardware

Unless noted otherwise, all experiments are performed on an 8-core server with
i7-3770 CPUs (3.7GHz) and 32GB of RAM.  The machine is in concurrent use by
several experiments, which introduces noise in the system load.  

We performed the following experiments:

## (1) Execution Consistency

Both profiling and emulation can only be as consistent as the actually executed
simulation.  We measure the execution time for one specific representative
application configuration, which is part of a typical workload of the user group
listed above.

```
$ cat sander_run_radical/sander_run_radical.csv | cut -f 4 -d , | histogram.py 
# NumSamples = 70; Min = 284.70; Max = 307.98
# Mean = 289.088857; Variance = 19.479727; SD = 4.413584; Median 287.890000
# each ∎ represents a count of 1
  284.7000 -   287.0280 [    19]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  287.0280 -   289.3560 [    29]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  289.3560 -   291.6840 [    13]: ∎∎∎∎∎∎∎∎∎∎∎∎∎
  291.6840 -   294.0120 [     5]: ∎∎∎∎∎
  294.0120 -   296.3400 [     0]: 
  296.3400 -   298.6680 [     0]: 
  298.6680 -   300.9960 [     0]: 
  300.9960 -   303.3240 [     1]: ∎
  303.3240 -   305.6520 [     1]: ∎
  305.6520 -   307.9800 [     2]: ∎∎
```

The outliers are considered to be caused by sporadic system overload.


## (2) Profiler Consistency

We expect the Synapse Profiler to have comparable noise in measured runtime as
the actual execution.  Also, the profiler is expected to have little (if any)
impact on the runtime of the application running under the profiler.

```
$ cat sander_profile_radical/sander_profile_radical.csv | cut -f 4 -d , | histogram.py 
# NumSamples = 70; Min = 285.07; Max = 297.37
# Mean = 288.539134; Variance = 4.472463; SD = 2.114820; Median 288.049164
# each ∎ represents a count of 1
  285.0731 -   286.3029 [     8]: ∎∎∎∎∎∎∎∎
  286.3029 -   287.5327 [    19]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  287.5327 -   288.7626 [    18]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  288.7626 -   289.9924 [     9]: ∎∎∎∎∎∎∎∎∎
  289.9924 -   291.2223 [     7]: ∎∎∎∎∎∎∎
  291.2223 -   292.4521 [     8]: ∎∎∎∎∎∎∎∎
  292.4521 -   293.6820 [     0]: 
  293.6820 -   294.9118 [     0]: 
  294.9118 -   296.1416 [     0]: 
  296.1416 -   297.3715 [     1]: ∎
```

We observe fewer outliers, and thus also a smaller standard deviation.  The
means are comparable as expected.

The Synapse Profiler is also expected to measure a consistent number of flops
for each execution.

```
$ cat sander_profile_radical/sander_profile_radical.csv | cut -f 5 -d , | histogram.py 
# NumSamples = 70; Min = 1702589739491.00; Max = 1715389342238.00
# Mean = 1710745871365.800049; Variance = 4983903813932869632.000000; SD = 2232465859.522351; Median 1710769736428.000000
# each ∎ represents a count of 1
1702589739491.0000 - 1703869699765.7000 [     1]: ∎
1703869699765.7000 - 1705149660040.3999 [     1]: ∎
1705149660040.3999 - 1706429620315.1001 [     0]: 
1706429620315.1001 - 1707709580589.8000 [     4]: ∎∎∎∎
1707709580589.8000 - 1708989540864.5000 [     6]: ∎∎∎∎∎∎
1708989540864.5000 - 1710269501139.2000 [    14]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎
1710269501139.2000 - 1711549461413.8999 [    18]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
1711549461413.8999 - 1712829421688.6001 [    15]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
1712829421688.6001 - 1714109381963.3000 [     8]: ∎∎∎∎∎∎∎∎
1714109381963.3000 - 1715389342238.0000 [     3]: ∎∎∎
```

While the standard deviation is about 2% of the mean value for the execution
times, it is about 7.5% for the measured number of flops, so spreads somewhat
wider as expected. [synapse.paper] discusses that variance in flop measurements
in some detail.


## (3) Emulation Accuracy

When emulating the workload profiled in experiment 2, we expect that repeated
emulation runs for the same profile results in comparable runtimes.  We
motivated above why I/O operations are excluded from the emulation runs (but see
experiment 5 below!), so the execution times are not expected to be exactly the
same as seen in experiment 1 (excution of simulation), but we do expect
a comparable distribution.  The amount of flops emulated in this experiment is
the average of flops measured in experiment 2.

```
$ cat sample_mean_flops_radical/sander_emulate_meanflops_radical.csv  | cut -f 4 -d , | histogram.py 
# NumSamples = 70; Min = 155.15; Max = 173.06
# Mean = 161.691377; Variance = 9.843512; SD = 3.137437; Median 161.437264
# each ∎ represents a count of 1
  155.1526 -   156.9435 [     2]: ∎∎
  156.9435 -   158.7343 [    10]: ∎∎∎∎∎∎∎∎∎∎
  158.7343 -   160.5252 [    12]: ∎∎∎∎∎∎∎∎∎∎∎∎
  160.5252 -   162.3161 [    20]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  162.3161 -   164.1070 [    10]: ∎∎∎∎∎∎∎∎∎∎
  164.1070 -   165.8979 [    11]: ∎∎∎∎∎∎∎∎∎∎∎
  165.8979 -   167.6888 [     3]: ∎∎∎
  167.6888 -   169.4796 [     1]: ∎
  169.4796 -   171.2705 [     0]: 
  171.2705 -   173.0614 [     1]: ∎
```

Ignoring the I/O operations results in alower overall execution time, as one
would expect.  The observed standard deviation is comparable to the actual
execution times from experiment 1.


## (4) Emulation consistency

To ensure that the results of experiment 3 are not a fluke for this specific
flop number, we also measure the emulation for the *individual* profiled flop
numbers from experiment 2.  We expect the resulting distribution to have
a somewhat larger standard deviation, as we are folding several statistical
distributions (execution, profiling and emulation) into one measurement.

```
$ cat sample_flops_radical/sander_emulate_flops_radical.csv  | cut -f 4 -d , | histogram.py 
# NumSamples = 70; Min = 155.24; Max = 177.15
# Mean = 164.424608; Variance = 28.632547; SD = 5.350939; Median 164.113376
# each ∎ represents a count of 1
  155.2434 -   157.4338 [     3]: ∎∎∎
  157.4338 -   159.6241 [    12]: ∎∎∎∎∎∎∎∎∎∎∎∎
  159.6241 -   161.8145 [    16]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  161.8145 -   164.0049 [     4]: ∎∎∎∎
  164.0049 -   166.1952 [    11]: ∎∎∎∎∎∎∎∎∎∎∎
  166.1952 -   168.3856 [     3]: ∎∎∎
  168.3856 -   170.5759 [    12]: ∎∎∎∎∎∎∎∎∎∎∎∎
  170.5759 -   172.7663 [     3]: ∎∎∎
  172.7663 -   174.9567 [     5]: ∎∎∎∎∎
  174.9567 -   177.1470 [     1]: ∎
```

This is indeed the case -- but the distribition mean remains consistent with
experiment 3, and the standard deviation is not growing beyond what one would
naively expect.


## (5) Full Emulation Accuracy and Consistency

Unrelated to this specific paper, we also performed the same experiment as (4),
but now *included* I/O emulation (disk and memory).  We expect the mean runtime
to be closer to what we measured as actual simulation runtime in experiment 1.

```
$ cat sample_profiles_radical/sander_emulate_profiles_radical.csv  | cut -f 4 -d , | histogram.py 
# NumSamples = 70; Min = 285.99; Max = 377.99
# Mean = 299.200286; Variance = 350.859797; SD = 18.731252; Median 290.990000
# each ∎ represents a count of 1
  285.9900 -   295.1900 [    45]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  295.1900 -   304.3900 [     8]: ∎∎∎∎∎∎∎∎
  304.3900 -   313.5900 [     9]: ∎∎∎∎∎∎∎∎∎
  313.5900 -   322.7900 [     4]: ∎∎∎∎
  322.7900 -   331.9900 [     0]: 
  331.9900 -   341.1900 [     0]: 
  341.1900 -   350.3900 [     0]: 
  350.3900 -   359.5900 [     2]: ∎∎
  359.5900 -   368.7900 [     0]: 
  368.7900 -   377.9900 [     2]: ∎∎
  ```

This is indeed the case: the measured mean is very close to the expected value.
At the same time we see that the variationj increases significantly, which we
interprete as the emulation being more sensitive to noise in the system load.


## (6) Emulation Portability

The AIMES related experiments execute the Synapse Emulation on a variety of
machines.  This requires us to confirm that the emulation behaves consistent
over different machine configurations.  We will not discuss if the emulation on
other machines than the profiling one is truthful to the application execution
on those machines -- for that discussion, please refer to [synapse.paper].
Instead, we limit this experiment to ensure that a repetition of experiment
3 (repeated emulation of mean flop number) results in a similar runtime
distribution as on the original machine.

These experiments have been performed on:

 * Andre's  laptop 1 (Linux)
 * Matteo's laptop   (Mac)

** TODO **


## Experiment Limitations

We want to stress again that all experiments above have been performed for *one*
specific application configuration, and as such cannot support any claims on
synapse  behaviour for other configurations.  For a discussion of synapse
profiling and behavior under varying workloads, please refer to [synapse.paper].


## Experiment Details

### Pre-requisites
 
  * Python 2.7.x
  * `perf stat` available and configured (permissions!)
  * `amber16` installed

```
$ git clone git@github.com:radical-experiments/AIMES-Experience.git
$ cd AIMES-Experience/synapse_characterization
$ virtualenv ve
$ source ve/bin/activate
$ pip install radical.synapse data-hacks

$ cd sander_run_radical
$ ./experiment.sh
$ ./get_csv.sh
$ cat sander_run_radical.csv | cut -f 4 -d , | histogram.py
$ cd ../

$ cd sander_profile_radical
$ ./experiment.sh
$ ./get_csv.sh
$ cat sander_profile_radical.csv | cut -f 4 -d , | histogram.py
$ cat sander_profile_radical.csv | cut -f 5 -d , | histogram.py
$ cd ../

$ cd sample_mean_flops_radical
$ ./experiment.sh
$ ./get_csv.sh
$ cat sander_emulate_meanflops_radical.csv | cut -f 4 -d , | histogram.py
$ cd ../

$ cd sample_flops_radical
$ ./experiment.sh
$ ./get_csv.sh
$ cat sander_emulate_flops_radical.csv | cut -f 4 -d , | histogram.py
$ cd ../

$ cd sample_profiles_radical
$ ./experiment.sh
$ ./get_csv.sh
$ cat sander_emulate_profiles_radical.csv | cut -f 4 -d , | histogram.py
$ cd ../
```

Each experiment will run for about 6 hours.


---

### previous text


## Profiler Accuracy and Consistency

We measure the accuracy of the Synapse profiler against the behavior of an AMBER
simulation: the more accurate the profiling, the more similar are the number of
FLOPS performed by AMBER and the number of FLOPS returned by the profiler.

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
