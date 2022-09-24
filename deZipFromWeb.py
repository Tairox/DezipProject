import ftplib
import requests,zipfile,io,filecmp,logging,os
from ourFunctions import formatDate,tgzMyFile
from datetime import date
from ftplib import FTP

logging.basicConfig(filename='scriptStatus.log', format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8',datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)


logging.info("Script started")
filename="Sample-SQL-File-10-Rows.sql"
today=date.today()
finalDate=today.strftime("%Y%d%m") # finalDate est un string AAAADDMM
r = requests.get("https://hdesousa.fr/downloads/Sample-SQL-File-10-Rows.sql.zip", stream=True)
if r.ok:
    logging.info("L'URL de téléchargement existe")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    try:
        z.extract(filename,".") # "filename" est le nom du fichier attendu dans le zip, il sera extrait dans le répertoire commun (.)
        logging.info("L'archive ZIP contient bien le fichier attendu")
        os.rename(filename,finalDate+'.sql')
    except KeyError:
        logging.critical("L'archive ZIP ne contient pas le fichier attendu")
        exit(1) # arrête le programme
else:
    logging.critical("L'URL de téléchargement n'existe pas")
    exit()

dayNumberMinus=today.day-1
dateMinus=today.strftime('%Y'+str(dayNumberMinus)+'%m')
tgzMyFile(finalDate,finalDate+'.sql')

try:
    if filecmp.cmp(finalDate+'.sql',dateMinus+'.sql'): # si les fichiers sont identiques
        logging.error("Le fichier est le même que celui de la veille")
    else:
        logging.info("Le fichier n'est pas le même que celui de la veille")
except FileNotFoundError:
    logging.warning("Le fichier du jour précédent n'existe pas")

username="cuwrmrb"
passwordFile=(open("password.txt","r"))
password=passwordFile.read()
server="ftp.cluster029.hosting.ovh.net"

with FTP(server) as ftp:
    try:
        ftp.login(username,password)
        strdir='/ScriptingSystemS7'
        ftp.cwd(strdir)
        fileToTransfer=open(finalDate+'.tgz',"rb")
        ftp.storbinary(f"STOR {finalDate+'.tgz'}",fileToTransfer,1024)
        ftp.close()
    except ftplib.error_perm as e:
        logging.critical("FTP : "+str(e))
        exit(3)

# à la fin du script on enlèvera le .sql du jour d'avant ainsi que l'archive tgz de celui du jour actuel car on en aura plus besoin

logging.info("Script ended")