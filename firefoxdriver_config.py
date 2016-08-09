# encoding:utf-8
"""
火狐浏览器配置参数，使浏览器尽可能的干净，不会造成多余dns查询
"""
from selenium import webdriver


def get_profile():

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
    profile.set_preference("browser.safebrowsing.provider.google.gethashURL","")
    profile.set_preference("browser.safebrowsing.provider.google.reportURL","")
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
    profile.set_preference("gecko.handlerService.schemes.mailto.1.uriTemplate","")
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
    profile.set_preference("extensions.systemAddon.update.url","")
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
    profile.set_preference("app.update.url","")
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

    #media
    profile.set_preference("media.gmp-eme-adobe.enabled",False)
    profile.set_preference("media.gmp-manager.cert.checkAttributes",False)
    profile.set_preference("media.gmp-manager.cert.requireBuiltIn", False)
    profile.set_preference("media.gmp-manager.certs.1.commonName", "")
    profile.set_preference("media.gmp-manager.certs.2.commonName", "")
    profile.set_preference("media.gmp-manager.url", "")
    profile.set_preference("media.gmp-provider.enabled", False)
    profile.set_preference("media.gmp-widevinecdm.enabled", False)

    # 禁止证书，ocsp.digicert.com？待验证 ss.symcd.com?
    profile.set_preference("services.sync.prefs.sync.security.OCSP.require",False)
    profile.set_preference("services.sync.prefs.sync.security.OCSP.enabled",False)
    profile.set_preference("security.ssl.enable_ocsp_stapling",False)
    profile.set_preference("security.ssl.enable_ocsp_must_staple",False)
    profile.set_preference("security.OCSP.enabled",0)



    return profile