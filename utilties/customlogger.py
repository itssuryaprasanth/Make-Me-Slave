import logging
from datetime import datetime

logs_file_location = 'C:\\Windows\\Temp\\'
loggers = {}


def get_current_date_time():
    now = datetime.now()
    current_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    return current_time


def file_logger(name='MakeMeSlave'):
    global loggers
    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        _current_time = get_current_date_time()
        handler = logging.FileHandler(f"{logs_file_location}" + "Slave" + f"_{_current_time}" + ".log")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        loggers[name] = logger
        return logger
