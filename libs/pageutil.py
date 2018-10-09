import time


class PageUtil(object):
    def __init__(self, platform, wd):
        self.platform = platform
        self.wd = wd

    def element_exist(self, elements, retry=3):
        try:
            source = self.wd.page_source
            if isinstance(elements, list):
                for element in elements:
                    if not element in source:
                        return False
            else:
                if elements in source:
                    return True
                else:
                    return False
        except Exception as e:
            if retry > 0:
                self.element_exist(elements, retry-1)
            print(str(e))
            return False

    def native2webview(self):
        try:
            for context in self.wd.contexts[::-1]:
                if "WEBVIEW" in context:
                    self.wd.switch_to.context(context)
                    break
        except Exception:
            pass
        finally:
            time.sleep(1)

    def webview2native(self):
        try:
            self.wd.switch_to.context("NATIVE_APP")
        except Exception:
            pass
        finally:
            time.sleep(1)

    def find_element_by_id(self, element):
        if not self.element_exist(element):
            raise Exception("没有找到元素：" + element)
        if self.platform == "ios":
            self.wd.find_element_by_accessibility_id(element)
        else:
            self.wd.find_element_by_id(element)


class AndroidPageUtil(PageUtil):
    def __init__(self, wd):
        super(AndroidPageUtil, self).__init__("Android", wd)


class IOSPageUtil(PageUtil):
    def __init__(self, wd):
        super(IOSPageUtil, self).__init__("IOS", wd)
