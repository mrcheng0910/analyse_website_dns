# encoding:utf-8
from selenium import webdriver
from multiprocessing import Process
from analysis_dns import extract_capture
from firefoxdriver_config import profile
import time
import os
import datetime

# 不显示浏览器
# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(800, 600))
# display.start()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-application-cache')
# driver = webdriver.Chrome('./chrome_driver/chromedriver',chrome_options=chrome_options)  # chrome浏览器驱动


SITE_LIST = os.path.dirname(__file__) + "/websites.txt"


def visit_url(url=None):
    """
    使用浏览器打开网址
    :param url: 待打开的网址
    """

    print str(datetime.datetime.now()) + " 打开网页: " + url
    driver.get(url)
    # driver.implicitly_wait(10)
    time.sleep(10)

    print str(datetime.datetime.now()) + " 关闭网页: " + url


def main():

    global driver
    driver = webdriver.Firefox(firefox_profile=profile)  # 火狐浏览器驱动，该浏览器较为干净
    if os.path.exists('error_screen'):
        pass
    else:
        os.mkdir('error_screen')

    with open(SITE_LIST) as urls:
        for domain in urls:
            if domain.startswith("#"):
                continue
            url = 'http://www.'+domain.strip()
            try:
                print str(datetime.datetime.now()) + " 开始探测网页: " + url
                np = Process(target=extract_capture,args = [domain.strip(), 20])
                mp = Process(target=visit_url,args=[url])
                np.start()
                time.sleep(2)   # 先打开网卡监控
                mp.start()

                np.join(50)
                mp.join(50)
                print str(datetime.datetime.now()) + " 结束探测网页: " + url
            except:
                print "子进程出错"
                continue

    driver.quit()
        # display.stop()

# if __name__ == '__main__':
#     main()