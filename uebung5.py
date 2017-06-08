from bs4 import BeautifulSoup
import requests
import csv

def getPage(url):
	r = requests.get(url)
	data = r.text
	spobj = BeautifulSoup(data, "html.parser")
	return spobj

def main():
	textliste = [] # speichert alle Ueberschriften
	fobj = open('heise-data.csv', 'w')
	csvw = csv.writer(fobj, delimiter = ';')

	heise_url = "https://www.heise.de/thema/https"

	content = getPage(heise_url).find("div", {"class":"keywordliste"})

	div = content.findAll("div")
	for c in div:
		c = c.findAll("header")
		txt = ""
		for t in c:
			txt += t.text.encode('utf-8')
		txt = txt.strip(' ') # entfernt Leerzeichen am Anfang und Ende
		txt = txt.strip('\n') # entfernt Zeilenumbrueche
		if txt != "":
			textliste += [txt]
			csvw.writerow([txt])
			

	for i in range(1,4):
		heise_url = "https://www.heise.de/thema/https?seite=" + str(i)

		content = getPage(heise_url).find("div", {"class":"keywordliste"})

		div = content.findAll("div")
		for c in div:
			c = c.findAll("header")
			txt = ""
			for t in c:
				txt += t.text.encode('utf-8')
			txt = txt.strip(' ')
			txt = txt.strip('\n')
			if txt != "":
				textliste += [txt]
				csvw.writerow([txt])

	fobj.close()


	words = [] # alle Woerter
	words2 = [] # alle Woerter + # der Vorkommen: [wort, anzahl]
	for text in range(0, len(textliste)): # geht durch alle Texte
		word = ""
		i = 0 # Zaehlvariable
		txt = textliste[text]
		while i < len(txt): # geht durch die chars im Text
			if txt[i] != ' ' and txt[i] != ":" and txt[i] != "," and txt[i] != '-':
				word += txt[i]
				i = i+1
			elif txt[i] == ' ' or txt[i] == '-':
				if word not in words and word != "": # ueberprüeft, ob Wort schon einmal vorkam
					words.append(word)
					words2 += [[word, 1]]
				else:
					for e in range(0, len(words2)): # erhoeht # der Vorkommen
						if word == words2[e][0]:
							words2[e][1] = words2[e][1] + 1
				i = i+1
				word = ""
			else:
				i = i+1

	benutzt = [] # speichert schon gefundene Maxima
	for top in range(1,4): # Anzahl der Maxima, die gesucht werden
		ak_max = words2[0][1]
		ak_word = words2[0][0]
		pos = 0
		for i in range(1, len(words2)): # findet ein Maximum
			if words2[i][1] > ak_max and words2[i][0] not in benutzt:
				ak_max = words2[i][1]
				ak_word = words2[i][0]
				pos = i
		benutzt.append(ak_word)
		print("TOP " + str(top) + ": " + str(ak_word) + ", " + str(ak_max) + " mal") 
	
			


if __name__=="__main__":
	main()
