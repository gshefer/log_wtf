import logging


class LevelFilter(logging.Filter):
    """Filter records according to the level"""

    def __init__(self, level):
        super(LevelFilter, self).__init__()
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level
