from log.logger import logger


def analyze(element):
    res = element * 2
    logger.debug('result is %d', res)
    return res
