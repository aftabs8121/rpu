from ftplib import FTP
from zipfile import ZipFile

def download_spy():
    host_name = 'localhost'
    user_name = 'test'
    user_pass = 'test'

    ftp = FTP(host_name, user_name, user_pass)

    # try to login
    reply = 'login failed'
    try:
        reply = ftp.login()
    except:
        print(reply)

    # get file/dir list
    ftp.retrlines("LIST")

    # download the zip archive
    ftp.retrbinary('RETR spy.zip', open('local_spy.zip', 'wb').write)

    # extract the archive
    zip = ZipFile('local_spy.zip')
    zip.extractall()