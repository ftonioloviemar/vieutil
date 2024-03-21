import logging
from pathlib import Path
import sys
from datetime import datetime

logging.root.setLevel(logging.NOTSET)

#def get_viemar_logger(directory, name, when, interval, backupCount, console_level, file_level):
def get_viemar_logger(directory, name, console_level, file_level):
    logger = logging.getLogger(name)
    log_format = logging.Formatter('%(asctime)s; %(lineno)d; %(levelname)s; %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # criar diretorio para log se ainda nao existe
    Path(directory).mkdir(parents=True, exist_ok=True)

    #file_handler = TimedRotatingFileHandler(f'{directory}/{name}.log', when=when, interval=interval, backupCount=backupCount)
    now = datetime.now()
    ymd = now.strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f'{directory}/{name}_{ymd}.log')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger
        
if __name__ == "__main__":
    log = get_viemar_logger('testelog', 'viemarlog', logging.DEBUG, logging.INFO)
    log.warning('This is a warning')
    log.error('This is an error')