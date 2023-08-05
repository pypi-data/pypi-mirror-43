import logging


logger = logging.getLogger("example")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("default.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)-15s] [%(levelname)s] [%(filename)s] [line:%(lineno)d] [pid:%(process)d] %(message)s",
    "%a %d %b %Y %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)
