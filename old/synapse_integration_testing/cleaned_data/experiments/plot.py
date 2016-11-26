import csv
import sys
import matplotlib.pyplot as plt


if sys.argv[1] == 'TTC':
    filename = 'TTC.csv'
elif sys.argv[1] == 'Tq':
    filename = 'Tq.csv'
elif sys.argv[1] == 'Tx':
    filename = 'Tx.csv'
else:
    print "Only TTC, Tq, Tx can be plot"
    sys.exit()


metric = sys.argv[1]
cores = list()
avg = list()
std = list()

with open(filename) as csvfile:
    c_file = csv.reader(csvfile)

    tmp_timings = list()
    
    for row in c_file:
        tmp_timings.append(row)

    cores = tmp_timings[0]
    avg = map(float, tmp_timings[1])
    std = map(float, tmp_timings[2])

cores.insert(0, 'bump')

fig = plt.figure()
ax = fig.add_subplot(111)

x_value = [i for i in range(len(avg))]

ax.set_title(r'$'+metric+'$ by Cores', fontsize=20)
ax.set_xlabel('Cores', fontsize=20)
ax.set_ylabel(r'$'+metric+'$ (s)', fontsize=20)
ax.set_xlim(-0.1, len(avg) - 1 + 0.1)
ax.set_ylim(-0.1, 15000)
ax.set_xticklabels(cores, fontsize=20)
ax.tick_params(axis='y', labelsize=20)

ax.errorbar(x_value, avg, yerr=std, c='b', marker='o', lw=2, label='XSEDE - 4 Resource')

ax.legend(loc='upper left', fontsize=16)
ax.grid(True)
plt.show()
