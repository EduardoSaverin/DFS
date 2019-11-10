'''
Import Lobby
'''
import logging
import os.path
import time
import utils
import web
import errorcheck

class FileServer:
    '''
    This is a fileserver which work as interface for holding files and sharing
    them on request.
    '''
    
    def GET(self, filepath):
        '''
        Return the requested file and raise error if one of following :
        1. File is not servable
        2. If file does not exits
        3. If file is locked by someone else
        '''
        # Here UTF-8 is necessary otherwise each platform may assume something else
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        errorcheck.check_if_servable(filepath)
        errorcheck.check_if_exists(filepath)
        absFilePath = utils._get_local_path(filepath)
        web.header('Last-Modified', time.ctime(os.path.getctime(absFilePath)))
        with open(absFilePath) as file:
            return file.read()
    
    def PUT(self, filepath):
        '''
        Replace file by the data in the request
        '''
        errorcheck.check_if_servable(filepath)
        absFilePath = utils._get_local_path(filepath)
        with open(absFilePath,'w') as file:
            file.write(web.data())
            
        web.header('Last-Modified',time.ctime(os.path.getctime(absFilePath)))
        web.created()
        return ''
    
    def DELETE(self,filepath):
        