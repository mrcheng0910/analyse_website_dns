# encoding:utf-8
from selenium import webdriver
from multiprocessing import Process
from analysis_dns import extract_capture
from add import capture_dns
import time
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-application-cache')
# driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)  # chrome浏览器驱动

# 禁止浏览器使用缓存等内容
profile = webdriver.FirefoxProfile()
profile.set_preference("startup.homepage_welcome_url", "")
# browser config
profile.set_preference("browser.safebrowsing.provider.google.updateURL","")
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("browser.safebrowsing.provider.mozilla.gethashURL", "")
profile.set_preference("browser.safebrowsing.provider.mozilla.updateURL", "")
profile.set_preference("browser.safebrowsing.downloads.remote.enabled", False)
profile.set_preference("browser.safebrowsing.downloads.remote.url","")
profile.set_preference("browser.newtabpage.enhanced",False)
profile.set_preference("browser.aboutHomeSnippets.updateUrl","")
profile.set_preference("browser.selfsupport.url", "")
profile.set_preference("browser.safebrowsing.enabled", False)
profile.set_preference("browser.shell.checkDefaultBrowser", False)
profile.set_preference("browser.startup.page", 0)
profile.set_preference("browser.addon-watch.ignore", "")
profile.set_preference("browser.newtabpage.directory.ping", "")
profile.set_preference("browser.newtabpage.directory.source", "")
profile.set_preference("browser.search.geoSpecificDefaults.url", "")
profile.set_preference("browser.search.geoip.url", "")
profile.set_preference("browser.geolocation.warning.infoURL","")
profile.set_preference("browser.usedOnWindows10.introURL","")
# network config
profile.set_preference("network.dns.disablePrefetch",True)
profile.set_preference("network.http.use-cache", False)
profile.set_preference("network.dnsCacheExpiration",0) #禁止使用浏览器dns缓存
profile.set_preference("network.dns.disableIPv6",True) #禁止使用ipv6
#app config
profile.set_preference("app.update.url.details","")
profile.set_preference("app.update.url.manual","")
profile.set_preference("app.update.auto", False)
profile.set_preference("app.update.url","")
# datareporting
profile.set_preference("datareporting.healthreport.infoURL", "")
#devtools
profile.set_preference("devtools.devedition.promo.url", "")
#extensions config
profile.set_preference("extensions.blocklist.detailsURL", "")
profile.set_preference("extensions.update.enabled", False)
profile.set_preference("extensions.update.notifyUser", False)
profile.set_preference("extensions.blocklist.enabled",False)
#loop config
profile.set_preference("loop.feedback.manualFormURL", "")
profile.set_preference("loop.gettingStarted.url", "")
profile.set_preference("loop.legal.ToS_url", "")
profile.set_preference("loop.legal.privacy_url", "")
profile.set_preference("loop.support_url", "")
#app config
profile.set_preference("app.support.e10sAccessibilityUrl","")
profile.set_preference("app.feedback.baseURL","")
profile.set_preference("app.support.baseURL", "")
#plugins config
profile.set_preference("plugins.update.url", "")
#privacy config
profile.set_preference("privacy.trackingprotection.enabled",False)
#services
profile.set_preference("services.sync.termsURL", "")
profile.set_preference("services.sync.syncKeyHelpURL", "")
profile.set_preference("services.sync.statusURL", "")
profile.set_preference("services.sync.serverURL", "")
profile.set_preference("services.sync.privacyURL", "")
profile.set_preference("services.sync.jpake.serverURL", "")
profile.set_preference("services.sync.addons.trustedSourceHostnames", "")
profile.set_preference("breakpad.reportURL","")
profile.set_preference("toolkit.telemetry.infoURL", "")
profile.set_preference("toolkit.crashreporter.infoURL", "")
profile.set_preference("social.shareDirectory", "")
profile.set_preference("social.directories", "")
profile.set_preference("security.ssl.errorReporting.url", "")
profile.set_preference("privacy.trackingprotection.introURL", "")
profile.set_preference("lightweightThemes.getMoreURL","")

driver = webdriver.Firefox(firefox_profile=profile) # 火狐浏览器驱动，该浏览器较为干净


def visit_url(url=None):

    driver.get(url)
    driver.implicitly_wait(10)


def main():
    # urls = ['163.com','weibo.com.cn','hitwh.edu.cn','ifeng.com','hit.edu.cn','sina.com.cn']
    urls = ['hao123.com']
    for i in urls:
        np = Process(target=extract_capture,args=[i,30])
        test = Process(target=capture_dns)
        mp = Process(target=visit_url,args=['http://www.'+i])

        np.start()

        test.start()
        time.sleep(2)   # 先打开网卡监控
        mp.start()
        np.join(100)
        test.join(100)
        mp.join(120)

    driver.quit()
    display.stop()

if __name__ == '__main__':
    main()