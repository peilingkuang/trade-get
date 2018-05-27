# -*- coding: utf-8 -*-
import os

import time


if __name__ == "__main__":
    print type("中文")
    print "中文".decode('utf-8') + "测试".decode('utf-8')

    # # 清理上次结果
    # if not os.path.exists("oldresult"):
    #     os.makedirs("oldresult")
    # command = "mv result* oldresult"
    # os.system(command)

    timestring = "2018-05-27 17:42:37"
    tm = time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))
    print tm
    tm = round(tm / 60) * 60
    print tm
    print time.strftime('%Y%m%d%H%M', time.localtime(tm))
