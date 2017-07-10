import psycopg2
import datetime
from random import randint
from datetime import timedelta
import matplotlib.pyplot as plt

def main(k, stop, radius):
	"""
	Eingabe: Die Datenbank Election muss wie in Aufgabe 2 spezifiziert existieren
	k -> Wert fuer den k-means Algorithmus (int)
	stop -> Wert fuer den k-means Algorithmus (int)
	radius -> Wert fuer find_hashtags (int)
	Ausgabe: Ein Plot, der die Datenpunkte und Clusterpunkte darstellt, die durch den k-means Algorithmus berechnet wurden
	"""
	conn = psycopg2.connect(database="Election", user="postgres", password="postgres", host="localhost") # stellt Verbindung zur Datenbank her
	cur = conn.cursor()
	cur.execute("SELECT time, favorite_count, hashtagid FROM tweets, enthalten WHERE tweetid = tweets.id")
	data = []
	tupel = cur.fetchone()
	while tupel != None: # liest die ausgewaehlten Datenbankzeilen in die Liste data ein.
		tupel_als_liste = list(tupel)
		data.append(tupel_als_liste)
		tupel = cur.fetchone()
	clusters = k_means(data, k, stop) # berechnet die Clusterp 
	clusterpoints = clusters[0] # Liste der Clustermittelpunkte
	clustercontend = clusters[1] # Liste der Datenpunkte aus Data, die zum jeweiligen Clusterpunkt gehoeren
	zeit0 = data[-1][0] # Zeitpunkt des allerersten Hashtags aus dem Datensatz
	hashtags_clusterpoints = find_hashtags(clustercontend, clusterpoints, radius, zeit0) # finde alle Hashtags (alle Datenpunkte) die sich innerhalb des Radius um den Clustermittelpunkt befinden
	hashtags = hashtags_clusterpoints[0] # Liste der aehnlichen Hashtags (hashtags innerhalb einer Subliste sind aehnlich
	clusterp = hashtags_clusterpoints[1] # Liste der zu den Hashtags gehoerenden Datenpunkte
	print(hashtags)
	print(clusterp)
	make_plot(data, clusterp) # erstellt den Plot

def make_plot(data, clusterpoints):
	"""
	Eingabe:
	data -> Liste mit den Zeilentupeln (als Listen) aus der DB, Format: [time (timestamp), favorite_count (int), 	hashtagid (int)]
	clusterpoints -> Die Clustermittelpunkte, die von k_means zurrueckgegeben werden
	Ausgabe: ein Plot der die Datenpunkte in blau und die Clusterpunkte in rot darstellt,
	x-Achse -> Zeit
	y-Achse -> favorite_count
	"""
	x_values = []
	y_values = []
	for i in range(0, len(data)):
		x_values.append(data[i][0]) # fuegt Zeitpunkte aus data ein
		y_values.append(data[i][1]) # fuegt favorite_counts aus data ein
	x_val_cluster = []
	y_val_cluster = []
	for i in range(0, len(clusterpoints)):
		x_val_cluster.append(clusterpoints[i][0]) # fuegt Zeitpunkte der Clusterpunkte ein
		y_val_cluster.append(clusterpoints[i][1]) # fuegt favorite_count der Clusterpunkte ein
	plt.plot(x_values, y_values, marker = '.', linestyle = "None")
	plt.plot(x_val_cluster, y_val_cluster, marker = '.', linestyle = "None", color = "red")
	plt.show()
	
def k_means(data, k, stop):
	"""
	Eingabe:
	data -> Liste mit den Zeilentupeln (als Listen) aus der DB, Format: [time (timestamp), favorite_count (int), 	hashtagid (int)]
	k -> Parameter k (int)
	stop -> Algorithmus soll beendet werden, wenn sich die Clusterpunkte um weniger als diesen Wert bewegen
	Ausgabe: Liste der Clustermittelpunkte, Format: [[time, favorite_count], .. ] und Liste der Punkte die zum Cluster gehoeren
	"""
	# Schritt 1: Initialisierung (waehle k zufaellige Mittelwerte aus dem Datensatz)
	laenge = len(data)
	means = []
	zaehler = 0
	for i in range(0, k):
		zufallszahl = randint(0, laenge-1)
		means += [data[zufallszahl]]
	# Schritt 2: Ordne alle Datenpunkte dem naechsten Cluster zu
	zeit0 = data[-1][0] # ist ein timestamp
	while True:
		zaehler = zaehler + 1
		clusters = [[]]
		for l in range(1, k): # erzeugt k leere Listen um die Cluster zu speichern
			clusters.append([])
		for i in range(0, laenge): # ermittelt x und y Wert des aktuellen Datenpunktes (x in Sekunden (int), y ist favorite_count (int)
			index = 0
			zeit_i = data[i][0] - zeit0
			x_i = zeit_i.total_seconds()
			y_i = data[i][1]
			zeit_k = means[0][0] - zeit0
			x_k = zeit_k.total_seconds()
			y_k = means[0][1]
			
			min_dist = get_distance((x_i, y_i), (x_k, y_k)) # Euklidische Distanz

			for j in range(1, k): # berechner kleinste Dinstanz des aktuellen Datenpunktes zu einem Clustermittelpunkt
				zeit_k = means[j][0] - zeit0
				x_k = zeit_k.total_seconds()
				y_k = means[j][1]
				dist = get_distance((x_i, y_i), (x_k, y_k))
				if dist < min_dist:
					min_dist = dist
					index = j
			clusters[index].append(data[i]) # ordnet aktuellen Datenpunkt dem entsprechenden Cluster zu
		# Schritt 3: neue Mittelpunkte berechenen
		change = 0
		for i in range(0, len(clusters)):
			sum_x = 0
			sum_y = 0
			len_j = 1
			for j in range(0, len(clusters[i])):
				sum_x = sum_x + (clusters[i][j][0] - zeit0).total_seconds()
				len_j = len_j + 1 
				sum_y = sum_y + clusters[i][j][1]
			if len_j > 1:
				len_j = len_j -1
			x = int(sum_x/len_j)
			y = int(sum_y/len_j)
			zeitdiff = timedelta(seconds = x)
			zeit = zeit0 + zeitdiff
			point = (zeit, y)
			zeit_i = means[i][0] - zeit0
			x_i = zeit_i.total_seconds()
			y_i = means[i][1]
			dist = get_distance((x_i, y_i), (x, y))
			if dist > change:
				change = dist
			means[i] = list(point)
		if change <= stop: # Abbruchbedingung
			break
	return [means, clusters]

def get_distance(p1,p2):
	"""
	Eingabe: Punkte p1, p2;  p -> (x, y)
	Ausgabe: Entfernung zw. den Punkten; float
	"""
	distance = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
	return distance

def find_hashtags(clusters, clusterpoints, radius, zeit0):
	"""
	Eingabe:
	clusterpoints -> Liste der Clustermittelpunkte, Format: [[time, favorite_count] .. ]
	radius -> int, Suchradius fuer aehnliche Hashtags um einen Clusterpunkt
	clusters -> Liste der Clusterpunkte aus der k-means Funktion
	zeit0 -> kleinster Zeitpunkt aus Data
	Ausgabe: Liste mit aehnlichen hashtags in einer Liste
	"""
	hashtags = [[]]
	for l in range(1, len(clusterpoints)): # erzeugt eine Liste mit leeren Listen fuer die Hashtags
		hashtags.append([])
	for i in range(0, len(clusterpoints)): # geht durch die Clustermittelpunkte
		zeit_i = clusterpoints[i][0] - zeit0
		x_i = zeit_i.total_seconds()
		y_i = clusterpoints[i][1]
		for j in range(0, len(clusters[i])): # geht durch die Datenpunkte eines Clustermittelpunktes
			zeit_j = clusters[i][j][0] - zeit0
			x_j = zeit_j.total_seconds()
			y_j = clusters[i][j][1]
			dist = get_distance((x_i, y_i), (x_j, y_j))
			if dist <= radius: # findet alle Datenpunkte innerhalb des Radius
				if clusters[i][j][2] not in hashtags[i]:
					hashtags[i].append(clusters[i][j][2]) # fuegt entsprechenden Hashtag an richtiger Stelle ein
	hashtags2 = []
	clusterpoints2 = []
	for i in range(0, len(hashtags)): # Eliminiert alle Cluster mit weniger als 2 Datenpunkten
		if len(hashtags[i]) > 1:
			clusterpoints2.append(clusterpoints[i])
			hashtags2.append(hashtags[i])
	return [hashtags2, clusterpoints2]

if __name__ == "__main__":
	main(200, 0, 3000)
			
