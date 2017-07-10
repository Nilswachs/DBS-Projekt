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

count = []
for i in range (0, len(days)):
	count.append(0)
k = 0
for i in range (0, len(datearr)):
	if(days[k] == datearr[i]):
		count[k] += 1
	else:
		k += 1

days = days[::-1]
count = count[::-1]


date = []
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

















