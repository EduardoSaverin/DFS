import logging
from fastapi import File, UploadFile
from ftplib import FTP
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt = '%d/%m/%y %I:%M:%S %p')

class NameSpaceServer(object):
    def __init__(self):
        logging.info("Namespace Server Initialized")

    def savefile(self, file: UploadFile = File(...)) ->  bool:
        pass

    def getfile(self, filename: str) -> None:
        pass


