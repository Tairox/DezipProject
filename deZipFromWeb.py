import logging
import json
from ourFunctions import deleteLocalFiles, formatDates, sftpCheckAndUpload, tgzMyFile, sendEmail, unzipURL

logging.basicConfig(filename='scriptStatus.log', format='%(asctime)s:%(levelname)s:%(message)s',
                    encoding='utf-8', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

with open("databaseconfig.json") as json_data_file:
    data = json.load(json_data_file)

logging.info("Script started")
filename = data['FileRequest']['filename']

finalDate, dateMinus = formatDates()

URLtoRequest = data['FileRequest']['URLtoRequest']
unzipURL(URLtoRequest, filename, finalDate)

tgzMyFile(finalDate, finalDate+'.sql')

username = data['SFTP']['username']
password = data['SFTP']['password']
server = data['SFTP']['server']
port = data['SFTP']['port']  # port SFTP
remotePath = data['SFTP']['remotePath']
localPath = data['SFTP']['localPath']
daysToDelete = data['SFTP']['daysOfPersistence']
sftpCheckAndUpload(username, password, server, port, remotePath,
                   localPath, finalDate, dateMinus, daysToDelete)

# Sending emails :
server = data['SMTP']['server']
port = data['SMTP']['port']
senderEmail = data['SMTP']['senderEmail']
senderPassword = data['SMTP']['password']

sendEmail(server, port, senderEmail, senderPassword, True, data)

# à la fin du script on enlèvera le .sql du jour d'avant ainsi que l'archive tgz de celui du jour actuel car on en aura plus besoin
filesToDelete = [dateMinus, finalDate]
deleteLocalFiles(filesToDelete)

logging.info("Script ended")
