import utils
import os.path
import web
def check_if_servable(filepath):
    '''
    Raise 406 NOTACCEPTABLE if filepath is not mentioned in servable list
    '''
    absFilePath = utils._get_local_path(filepath)
    if(os.path.isdir(absFilePath) or os.path.dirname(filepath) not in utils.get_configs()):
        raise web.notacceptable('File or directory access not allowed.')
    
def check_if_exists(filepath):
    '''
    Raise 404 if file not found
    '''
    absFilePath = utils._get_local_path(filepath)
    if not os.path.exists(absFilePath):
        raise web.notfound('File not found')