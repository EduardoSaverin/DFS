import logging
from fastapi import File, UploadFile, Response
import os, io
from ftpmanager import FTPManager

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                    datefmt='%d/%m/%y %I:%M:%S %p')


class NameSpaceServer(object):
    def __init__(self):
        logging.info("Namespace Server Initialized")
        self.ftpmanager = FTPManager(os.environ['FTP_USERNAME'], os.environ['FTP_PASSWORD'])

    def save_file(self, file: UploadFile = File(...)) -> Response:
        if self.ftpmanager.save_file('127.0.0.1', 'sumit', file):
            return Response(status_code=200)
        else:
            return Response(status_code=500)

    def get_file(self, filename: str) -> io.BytesIO:
        return self.ftpmanager.retrieve_file('127.0.0.1', 'sumit', filename)
