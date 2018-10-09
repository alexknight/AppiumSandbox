PAGE_IMPORT_TEMPLATE = "from libs.finder import By\n"

ANDROID_PAGE_CLASS_TEMPLATE = "\n\nclass Android$CLASS_NAME$(object):"

IOS_PAGE_CLASS_TEMPLATE = "\n\nclass IOS$CLASS_NAME$(object):"

H5_PAGE_CLASS_TEMPLATE = "\n\nclass Web$CLASS_NAME$(object):"

PAGE_FUNCTION_TEMPLATE = """
    @By.$LOCATE$($ELEMENT$)
    def $FUNCTION_NAME$(self): pass
"""
ANDROID_CASE_IMPORT_TEMPLATE = "import time\nfrom cases.base import AndroidBaseTest\n"

IOS_CASE_IMPORT_TEMPLATE = "import time\nfrom cases.base import IOSBaseTest\n"

ANDROID_PAGE_IMPORT = "from cases.pages.$FILE_NAME$ import Android$CLASS_NAME$()"

IOS_PAGE_IMPORT = "from cases.pages.$FILE_NAME$ import IOS$CLASS_NAME$()"

WEB_PAGE_IMPORT = "from cases.pages.$FILE_NAME$ import Web$CLASS_NAME$()"


KEY_WORDS_CASES = ["cases", "platform"]

KEY_WORDS_SCENES = ["context", "extends"]

KEY_WORDS_STEPS = ["id", "wid", "action", "sleep", "clear"]

KEY_WORDS_ACTIONS = ["click", "clear", "send_keys", "text", "assert"]

ANDROID_CASE_CLASS_TEMPLATE = """
class Android$CLASS_NAME$(AndroidBaseTest):
    def __init__(self):
        super().__init__()"""

IOS_CASE_CLASS_TEMPLATE = """
class IOS$CLASS_NAME$(IOSBaseTest):
    def __init__(self):
        super().__init__()"""

ANDROID_CASE_FUNCTION_TEMPLATE = """\n
    def $FUNCTION_NAME$(self):"""

ANDROID_CASE_LOCATE_ELEMENT_TEMPLATE = """
        self.page_util.find_element_by_$WAY$('$ELEMENT$')"""

NATIVE_TO_WEBVIEW = """
        self.page_util.native2webview()"""

WEBVIEW_TO_NATIVE = """
        self.page_util.webview2native()"""

NTT = """\n        """
