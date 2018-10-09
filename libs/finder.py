import time


class By(object):
    wd = None

    @classmethod
    def set_wd(cls, wd):
        cls.wd = wd

    @classmethod
    def id(cls, id):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                    source = cls.wd.page_source
                    if id in source:
                        if "com." in id:
                            return cls.wd.find_element_by_id(id)
                        else:
                            return cls.wd.find_element_by_accessibility_id(id)
                    else:
                        time.sleep(2)
                        return cls.wd.find_element_by_id(id)
                except Exception as e:
                    raise Exception("当前id：" + id + "\n" + str(e))
            return wrapper
        return decorator

    @classmethod
    def web_id(cls, id):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                    source = cls.wd.page_source
                    if id in source:
                        return cls.wd.find_element_by_id(id)
                    else:
                        time.sleep(2)
                        return cls.wd.find_element_by_id(id)
                except Exception as e:
                    raise Exception("当前id：" + id + "\n" + str(e))
            return wrapper
        return decorator

    @classmethod
    def webview(cls, func):
        def wrapper(*args, **kwargs):
            for context in cls.wd.contexts[::-1]:
                if "WEBVIEW" in context:
                    cls.wd.switch_to.context(context)
                    break
            result = func(*args, **kwargs)
            cls.wd.switch_to.context("NATIVE_APP")
            return result
        return wrapper

    @classmethod
    def xpath(cls, xpath):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                    return cls.wd.find_element_by_xpath(xpath)
                except Exception:
                    raise Exception("当前id：" + xpath)
            return wrapper
        return decorator


class WebElement(object):

    @classmethod
    def click(cls):
        def decorator(func):
            def wrapper():
                return func.click()
            return wrapper
        return decorator


