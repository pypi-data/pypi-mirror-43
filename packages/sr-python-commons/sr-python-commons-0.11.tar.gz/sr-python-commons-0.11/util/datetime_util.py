import time

HALF_DAY = 12 * 60 * 60
DATE_FORMAT = "%Y--%d-%m %H:%M:%S"


def format(epoch_time):
    return time.strftime(DATE_FORMAT, time.gmtime(epoch_time))
