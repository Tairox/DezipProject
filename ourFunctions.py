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


def change_shell_path_to_script_folder() -> None:
    scriptdir =  os.path.dirname(os.path.abspath(__file__))
    os.chdir(scriptdir)

def unzipURL(URL: string, filename: string, finalDate: date) -> None:
    r = requests.get(URL, stream=True)
    if r.ok:
        logging.info("The download URL exists")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        try:
            # "filename" is the name of the file expected in the zip, it will be extracted in the common directory (.)
            z.extract(filename, ".")
            logging.info("The ZIP archive contains the expected file")
            os.rename(filename, finalDate+'.sql')
        except KeyError:
            logging.critical(
                "The ZIP archive does not contain the expected file")
            exit(1)  # stops program
        except FileExistsError:
            os.remove(finalDate+'.sql')
            os.rename(filename, finalDate+'.sql')
    else:
        logging.critical("The download URL does not exist")
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
        logging.info("The .tgz archive with the correct name has been created")
    else:
        logging.critical("The .tgz archive could not be created")


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
    transport.connect(None, username, password)  # None is the Hostkey
    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        # Previous day's DL for comparison
        sftp.get(os.path.join(remotePath, dateMinus+".tgz"),
                 os.path.join(localPath, dateMinus+".tgz"))
        unTgzMyFile(os.path.join(dateMinus+".tgz"))
        if filecmp.cmp(finalDate+'.sql', dateMinus+'.sql'):  # if both files are the same
            logging.error("The file is the same as the one from yesterday")
        else:
            logging.info("The file is not the same as the one from yesterday")
    except FileNotFoundError:
        logging.warning("The previous day's file does not exist")
    except Exception as e:
        logging.error(str(e))

    # Upload : remotepath as absolute path or sftp.chdir(folder) then relative path to this folder
    sftp.put(localpath=finalDate+".tgz",
             remotepath=os.path.join(remotePath, finalDate+".tgz"))
    # use of os.path.join allows to manage the case where remotePath ends with / and the case where it does not end with /

    # Delete all files that are older that X days
    for entry in sftp.listdir_attr(remotePath):
        timestamp = entry.st_mtime  # timestamp becomes the time of last modification of the file
        createtime = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        delta = now - createtime
        if delta.days > daysToDelete:
            filepath = remotePath + '/' + entry.filename
            # os.path.join allows to put a / at the end of local path if there is none
            sftp.get(filepath, os.path.join(localPath, entry.filename))
            sftp.remove(filepath)
            logging.info("The file "+entry.filename +
                         " has been deleted (file too old).")
    logging.info(
        "The search for obsolete files is over (+ than "+str(daysToDelete)+" days).")

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

    logging.info("Local files have been deleted.")
