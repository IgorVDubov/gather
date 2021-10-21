
from loguru import logger as logger
import os.path

def loggerInit(loggerLevel):
    print (os.curdir+os.sep)
    if not os.path.isdir('logs'):
        logger.info('dir .\logs not exist, creating...')
        try:
            os.mkdir('logs')
        except OSError  as e:
            logger.error(e)
            logger.error('Cant create logs files. Access denied...')
            return
    logsPath=os.curdir+os.sep+'logs'+os.sep
    #logger.add(logsPath+loggerLevel.lower()+'.log',format="{time:HH:mm:ss} {message}",level=loggerLevel.upper(), rotation='500 kb')
