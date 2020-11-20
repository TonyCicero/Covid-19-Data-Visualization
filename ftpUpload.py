import ftplib
import os

DOMAIN = 'tcicerodev.com'
USERNAME = 'Covid@tcicerodev.com'
PASSWORD = ''
session = None

def connect():
    global session
    #get password from pass.data
    with open('pass.dat', 'r') as file:
        PASSWORD = file.read().replace('\n', '')
    session = ftplib.FTP(DOMAIN,USERNAME,PASSWORD)
    #print(session.nlst())

def checkDir(path):
    folders = path.split('/')
    for folder in folders[1:-1]:
        if folder in session.nlst():
            session.cwd(folder)
        else:
            session.mkd(folder)
            session.cwd(folder)

def sendFile(filename, path):
    session.cwd('/')
    checkDir(path)
    file = open(filename,'rb')                  # file to send
    session.storbinary('STOR '+os.path.basename(file.name), file)     # send the file

def disconnect():    
    file.close()                                    # close file and FTP
    session.quit()

connect()



