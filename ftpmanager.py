from ftplib import FTP_TLS
import ftplib
import logging
import os.path as path
import io
import os
from fastapi import UploadFile
from typing import List
from io import StringIO, TextIOWrapper
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt = '%d/%m/%y %I:%M:%S %p')
log = logging.FileHandler(filename='logs.txt',mode='a')

class FTPManager(object):
    """
        This class manages ftp related work to save and retieve files from nodes where they are stored.
    """
    def __init__(self):
        logging.info("FTP Manager Initialized")

    def retrieve_file(self, host: str, dir: str, filename: str) -> str:
        """
            Retrieves file from nodes over ftp, and returns TextIOWrapper 
        """
        if not filename:
            return None
        with FTP_TLS(host, user=os.environ['FTP_USERNAME'], passwd=os.environ['FTP_PASSWORD']) as ftp:
            ftp.cwd(dir)
            ftp.prot_p()
            print(ftp.getwelcome())
            all_files = self.list_files(host, dir, ftp)
            if filename not in all_files:
                logging.warning(f"File {filename} does not exists")
                return
            logging.info("Files %s", all_files)
            s = StringIO()
            try:
                ftp.retrlines('RETR ' + filename, s.write)
            except ftplib.error_perm as resp:
                if '550' in str(resp):
                    logging.info("Failed to open file")
            s.seek(0) # most important line otherwise you will not get any data
            while True:
                data = s.read(1024)
                if not data:
                    logging.info("No more data")
                    break
                yield data
            
    def save_file(self, host: str, dir: str, filepath: str, filename: str) -> bool:
        """Saves file to node over FTP
        Returns:
            [status]: [A bool value to communicate if save file is success or not]
        """
        if filename is None or filename == '':
            return None
        with FTP_TLS(host, user=os.environ['FTP_USERNAME'], passwd=os.environ['FTP_PASSWORD']) as ftp:
            ftp.cwd(dir)
            ftp.prot_p()
            with open(filepath + filename, 'rb') as f:
                try:
                    ftp.storbinary(f'STOR {filename}', f)
                    logging.info("File Saved!")
                except ftplib.all_errors as e:
                    logging.error(e)

    def list_files(self, host:str, dir: str, ftp: FTP_TLS) -> List[str]:
        if ftp is None:
            with FTP_TLS(host, user=os.environ['FTP_USERNAME'], passwd=os.environ['FTP_PASSWORD']) as ftp:
                ftp.prot_p()
                return self._get_file_list(ftp)
        else:
            return self._get_file_list(ftp)

    def _get_file_list(self, ftp: FTP_TLS) -> List[str]:
        files = []
        try:
            files = ftp.nlst()
            return files
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise
        return files


if __name__ == "__main__":
    ftpmanager = FTPManager()
    fileHandle = ftpmanager.retrieve_file(host='127.0.0.1', filename='test.txt', dir="sumit")
    ftpmanager.save_file(host='127.0.0.1',dir='sumit', filepath=os.path.dirname(os.path.abspath(__file__)) + '/', filename='README.md')
    for line in fileHandle:
        print(line)
