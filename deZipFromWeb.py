import requests,zipfile,io,filecmp,logging,os,paramiko,json
from ourFunctions import formatDate,tgzMyFile, sendEmail
from datetime import date, timedelta, datetime
from ftplib import FTP

logging.basicConfig(filename='scriptStatus.log', format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8',datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

with open("databaseconfig.json") as json_data_file:
    data = json.load(json_data_file)

logging.info("Script started")
filename=data['FileRequest']['filename']
today=date.today()
finalDate=today.strftime("%Y%d%m") # finalDate est un string AAAADDMM

URLtoRequest=data['FileRequest']['URLtoRequest']

r = requests.get(URLtoRequest, stream=True)
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
    except FileExistsError :
        os.remove(finalDate+'.sql')
        os.rename(filename,finalDate+'.sql')
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

username=data['SFTP']['username']
password=data['SFTP']['password']
server=data['SFTP']['server']

'''with FTP(server) as ftp:
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
        '''
port=data['SFTP']['port'] #port SFTP
transport = paramiko.Transport((server,port))

# Auth
transport.connect(None,username,password) # None est la Hostkey

# Go!    
sftp = paramiko.SFTPClient.from_transport(transport)

remotePath=data['SFTP']['remotePath']
localPath=data['SFTP']['localPath']

# Upload : remotepath en chemin absolu ou alors sftp.chdir(dossier) puis chemin relatif à ce dossier
sftp.put(localpath=finalDate+".tgz",remotepath=os.path.join(remotePath,finalDate+".tgz"))
#utilisation de os.path.join permet de gérer le cas où remotePath finut par / et le cas où il ne finit pas par /

##SUPPRIME TOUT LES FICHIERS QUI ONT PLUS DE X JOURS
daysToDelete=30
for entry in sftp.listdir_attr(remotePath):
    timestamp = entry.st_mtime # timestamp devient le temps de dernière modif du fichier
    createtime = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    delta = now - createtime
    if delta.days > daysToDelete:
        filepath = remotePath + '/' + entry.filename
        sftp.get(filepath, os.path.join(localPath, entry.filename))  #os.path.join permet de mettre un / à la fin de local path s'il n'y en a pas
        sftp.remove(filepath)

# Close
if sftp: sftp.close()
if transport: transport.close()

# Sending emails :
serverSMTP=data['SMTP']['server']
senderEmail=data['SMTP']['senderEmail']
senderPassword=data['SMTP']['password']
senderPort=data['SMTP']['port']

sendEmail(serverSMTP, senderPort, senderEmail, senderPassword)


# à la fin du script on enlèvera le .sql du jour d'avant ainsi que l'archive tgz de celui du jour actuel car on en aura plus besoin


logging.info("Script ended")