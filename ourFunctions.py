import tarfile,os,logging, smtplib, ssl, csv

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


def sendEmail(smtp_server : str, port : int, sender_email : int, password : int) -> None :
    '''Send an email'''
    message = "test email"
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, password) # Use the gmail account to send the email
        #Send the email
        with open("contacts_file.csv") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for name, email in reader:
                logging.info("Sending email to " + name)
                server.sendmail(sender_email, email, message)
    except Exception as e:
        # Print any error messages to stdout
        logging.critical(e)
    finally:
        server.quit() 