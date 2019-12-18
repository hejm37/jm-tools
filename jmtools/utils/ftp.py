import sys
import os
from ftplib import FTP


def read_password(IP='172.20.20.21', username='hejiamin'):
    print("Username:", username)
    from getpass import getpass
    password = getpass()
    return (IP, username, password)


# save_path: local path to store the file including filename
def try_retrbinary(ftp, filename, save_path):
    handle = open(save_path, 'wb')
    try:
        ftp.retrbinary('RETR %s' % filename, handle.write)
    except Exception:
        print("Error:", str(sys.exc_info()[0]))
    handle.close()


def retrLog(exp_ids_list, base_dir, curr_dir):
    IP, username, password = read_password()
    with FTP(IP, username, password) as ftp:
        ftp.cwd(base_dir)
        for exp in exp_ids_list:
            print(exp)
            filename = exp + '.log'
            save_path = os.path.join(curr_dir, 'log', filename)
            try_retrbinary(ftp, filename, save_path)
