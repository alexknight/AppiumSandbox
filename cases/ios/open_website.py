import time
from cases.base import IOSBaseTest

class IOSOpenWebsite(IOSBaseTest):
    def __init__(self):
        super().__init__()

    def test_scene1(self):
        self.page_util.native2webview()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button').clear()
        time.sleep(3)
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button').clear().send_keys("xxx")
        a = self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button').text()
        assert a == "alex"
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button3').click()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button4').click()
        self.page_util.webview2native()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button5').clear()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button6').click()

    def test_scene2(self):
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button').click()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button2').clear()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button2').clear().send_keys("xxx")
        time.sleep(3)
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button4').click()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button5').clear()
        self.page_util.find_element_by_id('cn.ibona.t1_beta:id/start_button6').click()