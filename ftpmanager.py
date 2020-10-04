from ftplib import FTP
import logging
import os.path as path
import io
from fastapi import UploadFile
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt = '%d/%m/%y %I:%M:%S %p')


class FTPManager(object):
    """
        This class manages ftp related work to save and retieve files from nodes where they are stored.
    """
    def __init__(self):
        logging.info("FTP Manager Initialized")

    def retrieve_file(self, host: str, fileabspath: str) -> io.TextIOWrapper | None:
        """
            Retrieves file from nodes over ftp, and returns TextIOWrapper 
        """
        filepath = path.dirname(fileabspath)
        filename = path.basename(fileabspath)
        if filename is None or filename == '':
            return None
        with FTP(host) as ftp:
            ftp.cwd(filepath)
            handle = open(filename, 'w+')
            ftp.retrbinary(f'RETR {filename}', handle.write)
            yield handle
            
    def save_file(self, host: str, fileabspath: str, partfile: UploadFile) -> bool | None:
        """Saves file to node over FTP
        Returns:
            [status]: [A bool value to communicate if save file is success or not]
        """
        filepath = path.dirname(fileabspath)
        filename = path.basename(fileabspath)
        if filename is None or filename == '':
            return None
        with FTP(host) as ftp:
            ftp.cwd(filepath)
            ftp.storbinary(f'STOR {filename}', partfile.read)