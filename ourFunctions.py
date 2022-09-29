import tarfile,os,logging, smtplib, yagmail, json

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


def sendEmail(sender_email : int, password : int, issavegood : bool, data) -> None :
    '''Send an email to email adresses specified in the configuration file.'''

    # Variables
    header=""
    body=""
    filename = "scriptStatus.log"  # In same directory as script

    if issavegood:
        header = "The backup went well"
        body="Everything went well - More information in the attached log"
    else:
        header = "Error while saving"
        body="An error has occured - More information in the attached log"
    
    try:
        # Initializing the server connection
        yag = yagmail.SMTP(user= sender_email, password= password)
        # Sending the email
        yag.send(to=[data['SMTP']['email1'], data['SMTP']['email2'], data['SMTP']['email3']], subject= header, contents=body, attachments='scriptStatus.log')
        logging.info("Email sent successfully")
    except Exception as e:
        logging.critical("The email has not been sent see the exception : " + e)