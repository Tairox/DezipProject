from re import I
import tarfile,os,logging, smtplib, smtplib, ssl, json
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def formatDate(daynumber : int, monthnumber : int, yearnumber : int) -> str :
    '''Takes in the number of the day,month and year and returns it in a AAAADDMM format
    REPLACED BY built-in function strftime() from datetime'''
    if monthnumber<10 :
        monthnumber="0"+str(monthnumber)

    if daynumber<10 :
        daynumber="0"+str(daynumber)

    final_date=str(yearnumber)+str(daynumber)+str(monthnumber)
    return final_date

def tgzMyFile(filenameOfTgz : str,filenameOfSource : str) -> None :
    '''Takes in the desired name of your .tgz file (without extension) and the filename (or path) of your source file, creates the archive in your current directory'''
    with tarfile.open(filenameOfTgz+".tgz","w:gz") as tar:
        tar.add(os.path.basename(filenameOfSource))
    if os.path.exists(filenameOfTgz+".tgz") :
        logging.info("L'archive .tgz avec le bon nom a bien été créé")
    else :
        logging.critical("L'archive .tgz n'a pas pu être créé")

def unTgzMyFile(filenameSource : str) -> None :
    '''Takes in the tgz file and desired unpacked filename and unpack it'''
    try:
        with tarfile.open(filenameSource) as tar:
            tar.extractall()
            tar.close()
    except Exception as e:
        logging.error(str(e))


def sendEmail(smtp_server : str , port :int, sender_email : str, password : str, issavegood : bool, data) -> None :
    '''Send an email to email adresses specified in the configuration file.'''

    # Variables
    recipients = []
    subject="" # Header of the email
    content="" # Body of the email
    filename = "scriptStatus.log"  # Name of the attachment

    # Different message depending on the save
    if issavegood:
        subject = "The backup went well"
        content="Everything went well - More information in the attached log file"
    else:
        subject = "Error while saving"
        content="An error has occured - More information in the attached log file"

    # Puts the email of the configuration file in the list recipients
    
    try:
        i = 1
        while i <= len(data['EMAILS']):
            email = 'email' + str(i)
            recipients.append(data['EMAILS'][email])
            i += 1
    except Exception:
        logging.info("Unable to read the emails specified in the configuration file")
    
    # Creation of the message (the email)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    body = MIMEText(content,'plain')
    msg.attach(body)

    with open(filename,'r') as f:
        attachment = MIMEApplication(f.read(), Name = basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
        msg.attach(attachment)

    # Server connection & sending
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=recipients)
    except Exception as e:
        logging.info(e)


    
