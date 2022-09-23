import requests,zipfile,io,filecmp
from datetime import date
from ourFunctions import formatDate,tgzMyFile

filename="Sample-SQL-File-10-Rows.sql"
r = requests.get("https://hdesousa.fr/downloads/Sample-SQL-File-10-Rows.sql.zip", stream=True)
if r.ok:
    print("L'URL de téléchargement existe.")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    try:
        z.extract(filename,".") # "filename" est le nom du fichier attendu dans le zip, il sera extrait dans le répertoire commun (.)
        print("Le fichier .zip contient bien le fichier attendu.")
    except KeyError:
        print("Le fichier .zip ne contient pas le fichier attendu")
        exit() # arrête le programme
else:
    print("Erreur : L'URL de téléchargement n'existe pas.")

today=date.today()
daynumber=today.day
monthnumber=today.month
yearnumber=today.year

finalDate=formatDate(daynumber,monthnumber,yearnumber)

tgzMyFile(finalDate,filename)

if filecmp.cmp(filename,"monfichierdiff.sql"): # si les fichiers sont identiques
    print("Erreur : Le fichier est le même que celui de la veille")
else:
    print("Le fichier n'est pas le même que celui de la veille")