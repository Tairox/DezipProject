import requests,zipfile,io,filecmp
from datetime import date
from ourFunctions import formatDate,tgzMyFile

r = requests.get("https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-zip-file.zip", stream=True)
if r.ok:
    print("L'URL de téléchargement existe.")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    try:
        z.extract("sample.txt",".") # sample.txt est le nom du fichier attendu dans le zip
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

tgzMyFile(finalDate,"sample.txt")

if filecmp.cmp("sample.txt","monfichierdiff.txt"): # si les fichiers sont identiques
    print("Erreur : Le fichier est le même que celui de la veille")
else:
    print("Le fichier n'est pas le même que celui de la veille")