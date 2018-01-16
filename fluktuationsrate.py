import csv
from bs4 import BeautifulSoup
import urllib.request


"""

onlinemarketingscience.com: Skript für die Fluktuationsraten von Top-Keywords

von Marvin Jörs


"""


# Bitte den Sistrix API Key einfügen
SISTRIX_API_KEY = "KEY_EINGEBEN"


# Keywords eintragen
keywords = ["zeiterfassung"]


def calculateFlu(keyword): 
    
   
    aktuelle_urls = []
    vergangene_urls = []     
    
    # String zusammenkleben
    xml_output_now = "https://api.sistrix.com/keyword.seo?api_key=" + SISTRIX_API_KEY + "&kw=" + keyword + "&date=now&num=10'"
    # XML-auslesen und URLs in Liste speichern 
    
    with urllib.request.urlopen(xml_output_now) as response:
        
        xml = response.read()
        soup_of_now = BeautifulSoup(xml, 'lxml')
        soup_of_now.prettify()
    
        for element in soup_of_now.find_all("answer"):
            for stat in element.find_all("result"):
                aktuelle_urls.append(stat['url'])
    
    
    # String zusammenkleben
    soup_of_last_week = xml_output_last_week = "https://api.sistrix.com/keyword.seo?api_key=" + SISTRIX_API_KEY + "&kw=" + keyword + "&date=last+week&num=10'"
    
    with urllib.request.urlopen(xml_output_last_week) as response:
        
        xml = response.read()
        soup_of_last_week = BeautifulSoup(xml, 'lxml')
        soup_of_last_week.prettify()
    
        for element in soup_of_last_week.find_all("answer"):
            for stat in element.find_all("result"):
                vergangene_urls.append(stat['url'])
    
    
    # UND-Operator auf beide Listen 
    schnittmenge = set(aktuelle_urls).intersection(vergangene_urls)
    
    # Größe des Arrays berechnen 
    groeße = len(schnittmenge)
    
    # Fluktuationsscore = 10 - Größe des Arrays
    fluktuationsscore = 10 - groeße
    

    # Fluktuationsrate = Fluktuationsscore / 10
    fluktuationsrate = (fluktuationsscore / 10)
    
    
    return fluktuationsrate



# Schleife und Funktionsaufruf 
# Für jedes Keyword in keywords

for keyword in keywords: 
    
    tempFlu = calculateFlu(keyword)
    with open('fluktuationsraten.csv', 'w', newline='') as csvfile:
    
        sciencewriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        sciencewriter.writerow([keyword,",", tempFlu])



