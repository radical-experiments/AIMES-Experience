#!/usr/bin/env python

import sys
import pprint
import radical.utils as ru

n = 0
total_1 = 0
total_2 = 0
for f in sys.argv[1:]:
    
    print '%-20s ' % f,
    n    += 1
    flops = 0
    json  = ru.read_json(f)
    for sample in json['cpu']['sequence']:
        flops += sample[1]['flops']
    print '%20.2f | %20.2f' % (flops, json['cpu']['flops'])
    total_1 += flops
    total_2 += json['cpu']['flops']

print '%-20s ' % 'total',
print '%20.2f %20.2f' % (total_1, total_2)

print '%-20s ' % 'average',
print '%20.2f %20.2f' % (total_1/n, total_2/n)


