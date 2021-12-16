from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name",metavar='name', type=str, help="Choisis un champion")
args = parser.parse_args()

#Récupération des données
request_text = requests.get('https://leagueoflegends.fandom.com/wiki/List_of_champions/Base_statistics')

#Mise en format des données
soup = BeautifulSoup(request_text.content, 'html.parser')

#On récupère les données de type table
dt = soup.find('table')
sleep: 1

#On affiche nos 50 premiers td
champs = dt.find_all('td')[:50]
#print(champs)
#for champ in champs:
#    print(champ.get_text())

#On récupère les URL des champions
URLChamps = dt.find_all('a')[:20]
#print(URLChamps)
#for url in URLChamps:
#    if url.find_all('img'):
#        continue
#    else:
#        print(url.get('href'))

#On définit les futurs colonnes de notre dataframe
columns=["Champions","HP","HP/LVL","HPReg","HPReg/LVL","Mana","Mana/LVL","ManaReg","ManaReg/LVL","AD","AD/LVL","AS","AS/LVL","Armor","Arm/LVL","MR","MR/LVL","MS","Range"]

print("\n ------- \n DATA \n ---------- \n")

#On se place sur le tbody, on définit un tableau vide que l'on va remplir avec les valeurs présentes dans le tableau html
table_body = dt.find('tbody')
data=[]
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

#On affecte nos valeurs à notre DataFrame
df = pd.DataFrame(data=data, columns=columns)

#print(df.head())

def getChamps(df : pd.DataFrame, name):

    #Sélectionner seulement la ligne avec le champion entrer en paramètre
    df = df.loc[df['Champions'] == name]

    print(df.head())

if __name__=="__main__":
    #On récupère dans une variable notre fonction avec son argument
    tab = getChamps(df, args.name)
    #Si un argument est entré, on print notre variable DataFrame filtré
    if args.name:
        print(tab)
    #Sinon on print tout le DataFrame    
    else:
        print(df)