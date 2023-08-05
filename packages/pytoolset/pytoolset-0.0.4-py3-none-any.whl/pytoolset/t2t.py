"""
time 2 time

date: 2019.03.06
"""
import pandas as pd
import datetime
import time


def pd_t2t(pd_time):
    """
    pandas Timestamp 2 datetime.datetime
    """
    time_stamp = pd_time.value // (1000*1000*1000)
    return datetime.datetime.utcfromtimestamp(time_stamp)
