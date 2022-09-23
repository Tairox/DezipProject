import requests,zipfile,io,filecmp,logging
from datetime import date
from ourFunctions import formatDate,tgzMyFile

logging.basicConfig(filename='scriptStatus.log', format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8',datefmt='%m/%d/%Y %I:%M:%S', level=logging.DEBUG)


logging.info("Script started")
filename="Sample-SQL-File-10-Rows.sql"
r = requests.get("https://hdesousa.fr/downloads/Sample-SQL-File-10-Rows.sql.zip", stream=True)
if r.ok:
    logging.info("L'URL de téléchargement existe")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    try:
        z.extract(filename,".") # "filename" est le nom du fichier attendu dans le zip, il sera extrait dans le répertoire commun (.)
        logging.info("Le fichier .zip contient bien le fichier attendu")
    except KeyError:
        logging.critical("Le fichier .zip ne contient pas le fichier attendu")
        exit() # arrête le programme
else:
    logging.critical("L'URL de téléchargement n'existe pas")

today=date.today()
finalDate=today.strftime("%Y%d%m") # finalDate est un string AAAADDMM
tgzMyFile(finalDate,filename)

try:
    if filecmp.cmp(filename,"monfichierdiff.sql"): # si les fichiers sont identiques
        logging.error("Erreur : Le fichier est le même que celui de la veille")
    else:
        logging.info("Le fichier n'est pas le même que celui de la veille")
except FileNotFoundError:
    logging.warning("Le fichier du jour précédent n'existe pas.")

logging.info("Script ended")