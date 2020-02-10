import logging

#********************************************************************#
def InitMyLog(myFolder):
    try:
        global logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        log_path = myFolder + '//mylog.log'
        fh = logging.FileHandler(log_path,mode='a')

        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        logger.debug('InitMyLog start')
    except:
        print 'InitMyLog except fail'
#********************************************************************#


InitMyLog("/Users/huyujian")
logger.debug('InitMyLog start')
logger.debug('InitMyLog start')
logger.debug('InitMyLog start')
logger.debug('InitMyLog start')