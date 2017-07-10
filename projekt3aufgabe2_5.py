rom Tkinter import *
import psycopg2
import ttk
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
	
conn = psycopg2.connect(database="Election", user="postgres", password="postgres", host="localhost")
cur = conn.cursor()
cur.execute("SELECT name FROM hashtags")
data = []
tupel = cur.fetchone()
while tupel != None:
	tupel = list(tupel)
	#print(tupel)
	data += tupel
	tupel = cur.fetchone()

data.sort() # data = sortierte Liste mit den Namen aller Hashtags

min_datum = datetime.datetime(2016, 1, 5,0,0,0)
max_datum = datetime.datetime(2016, 9, 28,0,0,0)

anzahl_tage = max_datum - min_datum

def zaehle_hashtags(hashtag):
	"""
	Eingabe:
	hashtag -> der Name des gewaehlten hashtags
	Ausgabe: Liste tage mit den Vorkommen des Hashtags pro Tag
	"""
	tage = []
	for i in range(0, anzahl_tage.days):
		tage.append(0)
	daten = []
	cur.execute("SELECT time FROM hashtags, enthalten, tweets WHERE hashtags.id = hashtagid and tweets.id = tweetid and name = (%s);", (hashtag,))
	datum = cur.fetchone()
	while datum != None:
		datum = list(datum)
		daten += datum
		datum = cur.fetchone()

	for i in range(0, len(daten)):
		zeit = daten[i] - min_datum
		tage[zeit.days] = tage[zeit.days] + 1
	return tage

def make_plot(count, hashtag):
	date = []
	for i in range(0, anzahl_tage.days):
		tag = timedelta(days = i)
		datum = min_datum + tag
		date.append(datum)
	
	plt.style.use('ggplot')

	fig, ax = plt.subplots()
	ax.bar(date, count, align='center')

	ax.xaxis.set_major_locator(mdates.DayLocator(interval=12))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

	ax.set_title(hashtag)
	ax.set_ylabel('Count')
	ax.set_xlabel('Date')

	plt.show()
	
	

def button_action():
	wahl = variable.get()
	#print(wahl)
	wahl = str(wahl)
	days = zaehle_hashtags(wahl)
	make_plot(days, wahl)

	

fenster = Tk()
fenster.title("Hashtags")

info = Label(fenster, justify = LEFT, font=("Helvetica", 16), text=""" Bitte Hashtag auswaehlen: """)
info.pack()

variable = StringVar(fenster)
variable.set(data[0])

optionen = ttk.Combobox(fenster, textvariable=variable, values=data)
optionen.pack()

run_button = Button(fenster,text="Los!", font=("Helvetica", 16), command = button_action)
run_button.pack()


fenster.mainloop()
