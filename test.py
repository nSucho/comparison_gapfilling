"""
Created on January 2021

pure test-file to check if parts of new code run correctly before including it into the main code.

@author: Niko Suchowitz
"""
import time


def versuchsCode():
    """

    :return:
    """
    start_time = time.time()
    time.sleep(0.1231231)
    end_time = time.time()
    time_lapsed = end_time-start_time
    time_convert(time_lapsed)


def time_convert(sec):
    """

    :param sec: time passed in seconds
    :return:
    """
    mins = sec//60
    secs = sec%60
    hours = mins//60
    mins = mins%60

    print("Time needed for FEDOT = {0}:{1}:{2}".format(int(hours), int(mins), int(secs)))


if __name__ == '__main__':
    versuchsCode()
