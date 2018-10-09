import unittest

from appium import webdriver

from config.context import Context
from libs.finder import By
from libs.pageutil import AndroidPageUtil, IOSPageUtil


class AndroidBaseTest(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        android_config = Context.get_instance().get_android_desired_caps()
        desired_caps['platformVersion'] = getattr(android_config, 'platformVersion', '7.1')
        desired_caps['deviceName'] = getattr(android_config, 'deviceName', 'Genymotion')
        desired_caps['platformName'] = getattr(android_config, 'platformName', 'Android')
        desired_caps['noReset'] = getattr(android_config, 'noReset', False)
        desired_caps['app'] = getattr(android_config, 'app', '/Users/qingge/Downloads/example-debug.apk')
        desired_caps["unicodeKeyboard"] = getattr(android_config, 'noReset', True)
        desired_caps['browser'] = getattr(android_config, 'browser', 'Chrome')
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.wd.implicitly_wait(60)
        Context.get_instance().set_android_wd(self.wd)
        By.set_wd(self.wd)
        self.page_util = AndroidPageUtil(self.wd)

    def tearDown(self):
        self.wd.quit()


class IOSBaseTest(unittest.TestCase):

    def setUp(self):
        # try:
        #     self.wd.quit()
        # except Exception:
        #     pass
        desired_caps = {}
        ios_config = Context.get_instance().get_android_desired_caps()
        desired_caps['platformName'] = getattr(ios_config, 'platformName', 'IOS')
        desired_caps['platformVersion'] = getattr(ios_config, 'platformVersion', '11.4')
        desired_caps['deviceName'] = getattr(ios_config, 'deviceName', 'iPhone Simulator')
        desired_caps['app'] = getattr(ios_config, 'app', '/Users/qingge/Downloads/PlanckDemoExample.app')
        desired_caps['noReset'] = getattr(ios_config, 'noReset', False)
        desired_caps["unicodeKeyboard"] = getattr(ios_config, 'unicodeKeyboard', True)
        desired_caps['autoAcceptAlerts'] = getattr(ios_config, 'autoAcceptAlerts', True)
        desired_caps['connectHardwareKeyboard'] = getattr(ios_config, 'connectHardwareKeyboard', False)
        desired_caps['showXcodeLog'] = getattr(ios_config, 'showXcodeLog', True)

        self.wd = webdriver.Remote('http://127.0.0.1:3274/wd/hub', desired_caps)
        self.wd.implicitly_wait(60)
        Context.get_instance().set_ios_wd(self.wd)
        By.set_wd(self.wd)

        self.page_util = IOSPageUtil(self.wd)

    def tearDown(self):
        self.wd.quit()
