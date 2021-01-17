import csv
import re
import sys
import random
from matplotlib import pyplot as plt
import numpy as np

# the name of the txt file in this directory that contains data in this format:
#   pid,priority,start,duration,end
target_file = sys.argv[1]

# list of unique processes
listPIDS = []
# 3 separate entries for the q0, q1, and q2 records of each unique process in listPIDS
listPIDSx = []
# heights at which to place the q0, q1, and q2 blocks in the Gantt chart
listPIDSy = [(0,1),(1,1),(2,1)]

with open(target_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # if a new process, create entries in listPIDS and listPIDSx
        if not row[0] in listPIDS:
    	    listPIDS.append(row[0])
    	    listPIDSx.append([])
    	    listPIDSx.append([])
    	    listPIDSx.append([])
        # so that processes that are scheduled for 0 ticks show up as a line in the chart    
        dur = int(row[3])
        if (dur == 0):
            dur = .1
        # insert record of this scheduling round into listPIDSx at the entry for this pid and priority
        index = listPIDS.index(row[0]) * 3 + int(row[1])    
        listPIDSx[index].append((int(row[2]),dur))
        print(f'{row[0]} of priority {row[1]} ran at {row[2]} for {row[3]} ticks, finishing at {row[4]}.')
        line_count += 1
    print(f'Processed {line_count} lines.')
    print(f'Found {len(listPIDS)} processes.')

fig, ax = plt.subplots()
ax.grid(True)

count = 0
# for every unique process to show in the chart
for pid in listPIDS:
    # generate a random color for this process
    color = np.random.rand(3,)
    # access the records for this process in q0, q1, & q2 and insert into the chart w appropriate height & color
    pri0Index = listPIDS.index(pid) * 3 + 0
    pri1Index = listPIDS.index(pid) * 3 + 1
    pri2Index = listPIDS.index(pid) * 3 + 2
    ax.broken_barh(listPIDSx[pri0Index],(0,1),facecolors = color)
    ax.broken_barh(listPIDSx[pri1Index],(1,1),facecolors = color)
    ax.broken_barh(listPIDSx[pri2Index],(2,1),facecolors = color)
    count = count + 1
 
ax.set_ylim(0, 3)
ax.set_yticklabels(("Q0", "Q1", "Q2"))
ax.set_yticks(np.arange(3))
ax.invert_yaxis()
  
plt.title(target_file)
plt.show()
plt.savefig("graph.pdf")