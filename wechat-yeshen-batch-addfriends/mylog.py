import logging


def get_logger(filename ,logname):
    logger = logging.getLogger(logname)
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(filename=filename)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


if __name__ == '__main__':
    a = get_logger(filename="added.log")
    a.info("1212121   -> 1")
