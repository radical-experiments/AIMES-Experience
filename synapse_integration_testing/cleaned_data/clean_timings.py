import csv

timings = []

with open('timings_emulate.csv', 'r') as csvfile:
    c_file = csv.reader(csvfile)

    for row in c_file:
        timings.append(row)
        print row

timings_cvt = []
time = 0

for resource in range(len(timings)):
    tmp_cvt = []
    tmp_cvt.append(timings[resource][0])
    for time in range(1, len(timings[resource])):
        if timings[resource][time] == '':
            tmp_cvt.append('')

        else:
            minute, s = timings[resource][time].split('m')
            second = s.split('s')[0]
            time = 60.0 * float(minute) + round(float(second))
            tmp_cvt.append(str(time))
    print tmp_cvt
    timings_cvt.append(tmp_cvt)
        
        
with open('timings_emulate_cleaned.csv', 'wib') as csvfile:
    c_write = csv.writer(csvfile, delimiter=',')
    c_write.writerows(timings_cvt)

