import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime





datearr = []
text = open("/home/nils/Uni/DBS/Timestamps","r")
for line in text.readlines():
	datearr.append((line[0]+line[1]+line[2]+line[3]+line[5]+line[6]+line[8]+line[9]))

days = []
for i in range (0, len(datearr)-1):
	if(datearr[i] != datearr[i+1]):
			days.append(datearr[i]) 
if(datearr[len(datearr)-2] != datearr[len(datearr)-1]):
	days.append(datearr[len(datearr)-1])

count = [58, 7, 0, 1, 1, 3, 3, 0, 7, 3, 1, 2, 2, 8, 2, 2, 2, 1, 4, 1, 1, 2, 2, 3, 5, 2, 3, 1, 1, 2, 2, 5, 0, 0, 0, 1, 0, 1, 10, 1, 2, 6, 1, 1, 2, 4, 2, 0, 4, 1, 7, 10, 24, 6, 4, 9, 17, 9, 5, 2, 2, 0, 2, 3, 3, 1, 0, 3, 0, 0, 3, 3, 0, 0, 2, 2, 3, 0, 2, 23, 1, 0, 0, 2, 3, 2, 0, 5, 1, 3, 2, 0, 5, 0, 0, 0, 3, 2, 6, 0, 0, 0, 0, 2, 2, 2, 1, 0, 7, 4, 0, 1, 0, 0, 0, 2, 11, 2, 0, 1, 1, 9, 5, 4, 1, 3, 1, 4, 16, 2, 0, 5, 3, 2, 5, 20, 0, 3, 6, 0, 1, 0, 4, 1, 3, 3, 1, 6, 4, 6, 15, 0, 2, 3, 0, 0, 0, 0, 1, 5, 28, 8, 17, 2, 12, 3, 4, 3, 4, 4, 0, 0, 3, 8, 5, 3, 10, 13, 3, 4, 3, 6, 4, 1, 9, 2, 0, 5, 7, 2, 5, 4, 1, 1, 12, 1, 1, 0, 9, 1, 7, 2, 7, 0, 2, 1, 1, 2, 9, 5, 0, 6, 23, 4, 3, 19, 2, 7, 2, 1, 0, 0, 0, 1, 16, 1, 3, 3, 3, 0]

days = days[::-1]
count = count[::-1]
date = []
x_pos = np.arange(len(days))

for i in days:
	date.append(datetime.datetime.strptime(i,"%Y%m%d"))

plt.style.use('ggplot')

fig, ax = plt.subplots()
ax.bar(date, count, align='center')

ax.xaxis.set_major_locator(mdates.DayLocator(interval=12))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

ax.set_title('Graph 3')
ax.set_ylabel('Count')
ax.set_xlabel('Date')

plt.show()

















