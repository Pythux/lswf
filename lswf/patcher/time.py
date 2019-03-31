import math
from datetime import datetime

from lswf.patcher.init import sql


def get_last_update_time():
    last = sql('select files_last_update from patcher_last_update' +
               ' order by files_last_update desc limit 1')
    if last == []:
        return None
    return last[0]


def time_in_mn_since_last_scan():
    now = datetime.now()
    last_scan = get_last_update_time()
    if not last_scan:
        return None
    time_delta = now - last_scan
    return math.ceil(time_delta.seconds / 60)
