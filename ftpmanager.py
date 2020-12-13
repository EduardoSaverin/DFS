import ftplib
import logging
from ftplib import FTP_TLS, FTP
from io import BytesIO
from typing import List, Union

from fastapi import File, UploadFile

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                    datefmt='%d/%m/%y %I:%M:%S %p')
log = logging.FileHandler(filename='logs.txt', mode='a')
ftplib.FTP.maxline = 200000000


class FTPManager(object):
    """
        This class manages ftp related work to save and retieve files from nodes where they are stored.
    """

    def __init__(self, username: str, password: str):
        logging.info("FTP Manager Initialized")
        self.username = username
        self.password = password

    def retrieve_file(self, host: str, directory: str, filename: str) -> BytesIO:
        """
            Retrieves file from nodes over ftp, and returns TextIOWrapper 
        """
        if not filename:
            return None
        with FTP(host, user=self.username, passwd=self.password) as ftp:
            ftp.cwd(directory)
            # ftp.prot_p()
            print(ftp.getwelcome())
            all_files = self.list_files(host, ftp)
            if filename not in all_files:
                logging.warning(f"File {filename} does not exists")
                return
            logging.info("Files %s", all_files)
            s = BytesIO()
            try:
                ftp.retrbinary('RETR ' + filename, s.write)
            except ftplib.error_perm as resp:
                if '550' in str(resp):
                    logging.info("Failed to open file")
            s.seek(0)  # most important otherwise you will not get any data
            # while True:
            #     data = s.read(1024)
            #     if not data:
            #         logging.info("No more data")
            #         break
            #     yield data
            return s

    def save_file(self, host: str, directory: str, request_file: UploadFile = File(...)) -> Union[bool, None]:
        """Saves file to node over FTP
        Returns:
            [status]: [A bool value to communicate if save file is success or not]
        """
        if not request_file.filename:
            return None
        with FTP(host, user=self.username, passwd=self.password) as ftp:
            ftp.cwd(directory)
            # ftp.prot_p()  # switch to secure data connection
            try:
                ftp.storbinary(f'STOR {request_file.filename}', request_file.file)
                logging.info("File Saved!")
            except ftplib.all_errors as e:
                logging.error(e)

    def list_files(self, host: str, ftp: FTP_TLS) -> List[str]:
        if ftp is None:
            with FTP(host, user=self.username, passwd=self.password) as ftp:
                # ftp.prot_p()  # switch to secure data connection
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
