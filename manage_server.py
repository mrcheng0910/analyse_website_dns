#!/usr/bin/python
#encoding:utf-8

import sys
import schedule
import time
try:
    import schedule
except ImportError:
    sys.exit("无schedul模块,请安装 easy_install schedule")


from visit_websites import main

if __name__ == "__main__":

    # schedule.every(2).hours.do(main)
    schedule.every(15).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
