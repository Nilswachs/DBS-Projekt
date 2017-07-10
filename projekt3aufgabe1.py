import psycopg2
import datetime
from random import randint
from datetime import timedelta
import matplotlib.pyplot as plt

def main(k, stop, radius):
	
	conn = psycopg2.connect(database="Election", user="postgres", password="postgres", host="localhost") # stellt Verbindung zur Datenbank her
	cur = conn.cursor()
	cur.execute("SELECT time, favorite_count, hashtagid FROM tweets, enthalten WHERE tweetid = tweets.id")
	data = []
	while cur.fetchone() != None:
		tupel = cur.fetchone()
		tupel_als_liste = list(tupel)
		data.append(tupel_als_liste)
	#print(data)
	clusters = k_means(data, k, stop)
	clusterpoints = clusters[0]
	clustercontend = clusters[1]
	#print(clusterpoints)
	#print(clustercontend)
	zeit0 = data[-1][0]
	hashtags_clusterpoints = find_hashtags(clustercontend, clusterpoints, radius, zeit0)
	hashtags = hashtags_clusterpoints[0]
	clusterp = hashtags_clusterpoints[1]
	print(hashtags)
	print(clusterp)
	make_plot(data, clusterp)

def make_plot(data, clusterpoints):
	"""
	Eingabe:
	Ausgabe:
	"""
	x_values = []
	y_values = []
	for i in range(0, len(data)):
		#print(data[i])
		x_values.append(data[i][0])
		y_values.append(data[i][1])
	x_val_cluster = []
	y_val_cluster = []
	for i in range(0, len(clusterpoints)):
		x_val_cluster.append(clusterpoints[i][0])
		y_val_cluster.append(clusterpoints[i][1])
	plt.plot(x_values, y_values, marker = '.', linestyle = "None")
	plt.plot(x_val_cluster, y_val_cluster, marker = '.', linestyle = "None", color = "red")
	plt.show()
	

def k_means(data, k, stop):
	"""
	Eingabe:
	data -> Liste mit den Zeilentupeln (als Listen) aus der DB, Format: [time (timestamp), favorite_count (int), 	hashtagid (int)]
	k -> Parameter k (int)
	stop -> 
	Ausgabe: Liste der Clustermittelpunkte, Format: [[time, favorite_count], .. ]
	"""
	# Schritt 1: Initialisierung (waehle k zufaellige Mittelwerte aus dem Datensatz)
	laenge = len(data)
	means = []
	zaehler = 0
	for i in range(0, k):
		zufallszahl = randint(0, laenge-1)
		means += [data[zufallszahl]]
	#print(means)
	# Schritt 2:
	zeit0 = data[-1][0] # ist ein timestamp
	#print(means)
	#print( zeit0)
	while True:
		zaehler = zaehler + 1
		clusters = [[]]
		for l in range(1, k):
			clusters.append([])
		#print(clusters)
		for i in range(0, laenge):
			index = 0
			zeit_i = data[i][0] - zeit0
			x_i = zeit_i.total_seconds()
			y_i = data[i][1]
			zeit_k = means[0][0] - zeit0
			x_k = zeit_k.total_seconds()
			y_k = means[0][1]
			
			min_dist = get_distance((x_i, y_i), (x_k, y_k)) # Euklidische Distanz

			for j in range(1, k):
				zeit_k = means[j][0] - zeit0
				x_k = zeit_k.total_seconds()
				y_k = means[j][1]
				dist = get_distance((x_i, y_i), (x_k, y_k))
				if dist < min_dist:
					min_dist = dist
					index = j
			clusters[index].append(data[i])
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
			#print(dist)
			if dist > change:
				change = dist
			means[i] = list(point)
		if change <= stop:
			break
	#print (clusters)
	#print(len(clusters[0]))
	#print(means)
	#print(zaehler)
	#print([means, clusters])
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
	for l in range(1, len(clusterpoints)):
		hashtags.append([])
	for i in range(0, len(clusterpoints)):
		zeit_i = clusterpoints[i][0] - zeit0
		x_i = zeit_i.total_seconds()
		y_i = clusterpoints[i][1]
		for j in range(0, len(clusters[i])):
			zeit_j = clusters[i][j][0] - zeit0
			x_j = zeit_j.total_seconds()
			y_j = clusters[i][j][1]
			dist = get_distance((x_i, y_i), (x_j, y_j))
			#print(dist)
			if dist <= radius:
				if clusters[i][j][2] not in hashtags[i]:
					hashtags[i].append(clusters[i][j][2])
	hashtags2 = []
	clusterpoints2 = []
	for i in range(0, len(hashtags)):
		if len(hashtags[i]) > 1:
			clusterpoints2.append(clusterpoints[i])
			hashtags2.append(hashtags[i])
	return [hashtags2, clusterpoints2]

if __name__ == "__main__":
	main(200, 0, 3000)
			


