import string
import requests
import zipfile
import io
import tarfile
import os
import logging
import smtplib
import smtplib
import ssl
import filecmp
import paramiko
from os.path import basename
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def unzipURL(URL: string, filename: string, finalDate: date) -> None:
    r = requests.get(URL, stream=True)
    if r.ok:
        logging.info("L'URL de téléchargement existe")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        try:
            # "filename" est le nom du fichier attendu dans le zip, il sera extrait dans le répertoire commun (.)
            z.extract(filename, ".")
            logging.info("L'archive ZIP contient bien le fichier attendu")
            os.rename(filename, finalDate+'.sql')
        except KeyError:
            logging.critical(
                "L'archive ZIP ne contient pas le fichier attendu")
            exit(1)  # arrête le programme
        except FileExistsError:
            os.remove(finalDate+'.sql')
            os.rename(filename, finalDate+'.sql')
    else:
        logging.critical("L'URL de téléchargement n'existe pas")
        exit()


def formatDates() -> str:
    '''Returns AAAADDMM date foramt of today and yesterday'''
    today = date.today()
    finalDate = today.strftime("%Y%d%m")
    dateMinus = today-timedelta(days=1)
    dateMinus = dateMinus.strftime("%Y%d%m")
    return finalDate, dateMinus


def tgzMyFile(filenameOfTgz: str, filenameOfSource: str) -> None:
    '''Takes in the desired name of your .tgz file (without extension) and the filename (or path) of your source file, creates the archive in your current directory'''
    with tarfile.open(filenameOfTgz+".tgz", "w:gz") as tar:
        tar.add(os.path.basename(filenameOfSource))
    if os.path.exists(filenameOfTgz+".tgz"):
        logging.info("L'archive .tgz avec le bon nom a bien été créé")
    else:
        logging.critical("L'archive .tgz n'a pas pu être créé")


def unTgzMyFile(filenameSource: str) -> None:
    '''Takes in the tgz file and desired unpacked filename and unpack it'''
    try:
        with tarfile.open(filenameSource) as tar:
            tar.extractall()
            tar.close()
    except Exception as e:
        logging.error(str(e))


def sftpCheckAndUpload(username: string, password: string, server: string, port: int, remotePath: string, localPath: string, finalDate: date, dateMinus: date, daysToDelete: int) -> None:
    transport = paramiko.Transport((server, port))
    # Auth
    transport.connect(None, username, password)  # None est la Hostkey
    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        # DL du jour précédent pour comparaison
        sftp.get(os.path.join(remotePath, dateMinus+".tgz"),
                 os.path.join(localPath, dateMinus+".tgz"))
        unTgzMyFile(os.path.join(dateMinus+".tgz"))
        if filecmp.cmp(finalDate+'.sql', dateMinus+'.sql'):  # si les fichiers sont identiques
            logging.error("Le fichier est le même que celui de la veille")
        else:
            logging.info("Le fichier n'est pas le même que celui de la veille")
    except FileNotFoundError:
        logging.warning("Le fichier du jour précédent n'existe pas")
    except Exception as e:
        logging.error(str(e))

    # Upload : remotepath en chemin absolu ou alors sftp.chdir(dossier) puis chemin relatif à ce dossier
    sftp.put(localpath=finalDate+".tgz",
             remotepath=os.path.join(remotePath, finalDate+".tgz"))
    # utilisation de os.path.join permet de gérer le cas où remotePath finut par / et le cas où il ne finit pas par /

    # SUPPRIME TOUT LES FICHIERS QUI ONT PLUS DE X JOURS
    for entry in sftp.listdir_attr(remotePath):
        timestamp = entry.st_mtime  # timestamp devient le temps de dernière modif du fichier
        createtime = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        delta = now - createtime
        if delta.days > daysToDelete:
            filepath = remotePath + '/' + entry.filename
            # os.path.join permet de mettre un / à la fin de local path s'il n'y en a pas
            sftp.get(filepath, os.path.join(localPath, entry.filename))
            sftp.remove(filepath)
            logging.info("Le fichier "+entry.filename +
                         " a été supprimé (fichier trop ancien).")
    logging.info(
        "La recherche de fichiers obsolètes est terminée (+ de "+str(daysToDelete)+" jours).")

    # Close
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def sendEmail(smtp_server: str, port: int, sender_email: str, password: str, issavegood: bool, data) -> None:
    '''Send an email to email adresses specified in the configuration file.'''

    # Variables
    recipients = []
    subject = ""  # Header of the email
    content = ""  # Body of the email
    filename = "scriptStatus.log"  # Name of the attachment

    # Different message depending on the save
    if issavegood:
        subject = "The backup went well"
        content = "Everything went well - More information in the attached log file"
    else:
        subject = "Error while saving"
        content = "An error has occured - More information in the attached log file"

    # Puts the email of the configuration file in the list recipients

    try:
        '''i = 1
        while i <= len(data['EMAILS']):
            email = 'email' + str(i)
            recipients.append(data['EMAILS'][email])
            i += 1'''
        for x in data['EMAILS'].values():
            recipients.append(x)
    except Exception:
        logging.error(
            "Unable to read the emails specified in the configuration file")

    # Creation of the message (the email)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)

    with open(filename, 'r') as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(
            basename(filename))
        msg.attach(attachment)

    # Server connection & sending
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email,
                                to_addrs=recipients)
    except Exception as e:
        logging.error(e)


def deleteLocalFiles(filesToDelete: list[str]) -> None:
    for i in filesToDelete:
        SQLfilename = i+'.sql'
        TGZfilename = i+'.tgz'
        if (os.path.exists(SQLfilename)):
            os.remove(SQLfilename)
        if (os.path.exists(TGZfilename)):
            os.remove(TGZfilename)

    logging.info("Les fichiers locaux ont été supprimés.")
