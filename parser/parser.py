import json
import os
from config import template


class BaseParser(object):
    def __init__(self, config, path, case_file):
        self.config = config
        self.path = path
        self.case_file = case_file

    @staticmethod
    def execute_env(cls, debug):
        cls.debug = debug


class JsonParser(BaseParser):
    def __init__(self, config=None, file=None, case_file=None):
        super(JsonParser, self).__init__(config, file, case_file)
        self.scenes = []
        self.file = file
        # self.file_name = file.split("/")[-1].split(".")[0]
        if self.file is None:
            self.file_name = None
        else:
            self.file_name = file.split("/")[-1].split(".")[0]
        self.jf = None
        self.cjf = None
        self.page_content = ""
        self.case_content = ""
        self.page_android_import = []
        self.page_ios_import = []
        self.page_h5_import = []
        self.test_var = None
        self.locator = ""

        self.context = "native"

        self.case_file = case_file
        self.case_file_name = case_file.split("/")[-1].split(".")[0]

    def read(self):
        if self.file is not None:
            with open(self.file, "r") as f:
                self.jf = json.load(f)
        if self.case_file is not None:
            with open(self.case_file, "r") as g:
                self.cjf = json.load(g)
        return self

    def generate_pages(self):
        self.page_content += template.PAGE_IMPORT_TEMPLATE
        for platform in self.jf.keys():
            page = self.jf[platform]
            for cls_name in page.keys():
                if "android" == platform:
                    self.page_content += template.ANDROID_PAGE_CLASS_TEMPLATE.replace("$CLASS_NAME$", cls_name.capitalize())
                    self.page_android_import.append(template.ANDROID_PAGE_IMPORT
                                                    .replace("$FILE_NAME$", self.file_name)
                                                    .replace("$CLASS_NAME$", cls_name.capitalize()))
                elif "ios" == platform:
                    self.page_content += template.IOS_PAGE_CLASS_TEMPLATE.replace("$CLASS_NAME$", cls_name.capitalize())
                    self.page_ios_import.append(template.IOS_PAGE_IMPORT
                                                .replace("$FILE_NAME$", self.file_name)
                                                .replace("$CLASS_NAME$", cls_name.capitalize()))
                else:
                    self.page_content += template.H5_PAGE_CLASS_TEMPLATE.replace("$CLASS_NAME$", cls_name.capitalize())
                    self.page_h5_import.append(template.WEB_PAGE_IMPORT
                                               .replace("$FILE_NAME$", self.file_name)
                                               .replace("$CLASS_NAME$", cls_name.capitalize()))
                bys = page[cls_name]
                self.page_content = self._generate_page_function(self.page_content, bys)
        # print(self.page_content)
        self._write(self.file.replace(".json", ".py"), self.page_content)
        return self

    def generate_cases(self):
        self.generate_cases_direct()
        # if self.file is None:
        #     self.generate_cases_direct()
        # else:
        #     if self.page_content == "":
        #         self.generate_pages()
        # self.generate_cases_by_page()

    def generate_cases_by_page(self):
        pass

    def generate_cases_direct(self):
        platform = self.cjf['platform']
        case_name = self.cjf['case']
        if platform == "android":
            self.case_content += template.ANDROID_CASE_IMPORT_TEMPLATE + template.ANDROID_CASE_CLASS_TEMPLATE.replace("$CLASS_NAME$", case_name)
        if platform == "ios":
            self.case_content += template.IOS_CASE_IMPORT_TEMPLATE + template.IOS_CASE_CLASS_TEMPLATE.replace("$CLASS_NAME$", case_name)
        for top_key, top_value in self.cjf.items():
            if top_key.startswith("test_"):
                self.scenes.append(top_value)
                self.case_content += template.ANDROID_CASE_FUNCTION_TEMPLATE.replace("$FUNCTION_NAME$", top_key)
                for key, value in top_value.items():
                    if key == "context":
                        continue
                    self._generate_with_steps(value["steps"])
                if self.context == "webview":
                    self.case_content += template.WEBVIEW_TO_NATIVE

        self._write(os.path.join(os.path.dirname(os.path.dirname(__file__)), "cases", platform, self.case_file_name + ".py"), self.case_content)
        print(self.case_content)

    def _generate_with_steps(self, steps):
        for step in steps:
            self._generate_with_step(step)

    def _generate_with_step(self, step_dic):
        """
        :param step_dic:
        "steps":[
                {
                  "id": "cn.ibona.t1_beta:id/start_button2",
                  "action": [
                    "clear",
                    {"send_keys":"xxx"},{"text":"a"},{"assert": {"$a": "alex"}},
                  ]
                },
                {"sleep": "3"}
              ]
        :return:
        """
        if "sleep" in step_dic:
            self.case_content += template.NTT + "time.sleep(" + step_dic['sleep'] + ")"
            return
        self._generate_with_context(step_dic)

        a_step = ""
        if "id" in step_dic:
            a_step += template.ANDROID_CASE_LOCATE_ELEMENT_TEMPLATE.replace("$WAY$", "id").replace("$ELEMENT$",
                                                                                                   step_dic['id'])
            self.locator = a_step.strip()
        elif "wid" in step_dic:
            a_step += template.ANDROID_CASE_LOCATE_ELEMENT_TEMPLATE.replace("$WAY$", "id").replace("$ELEMENT$",
                                                                                                   step_dic['wid'])
            self.locator = a_step.strip()

        if "action" not in step_dic:
            return
        if isinstance(step_dic['action'], str):
            a_step += "." + step_dic['action'] + "()"
            self.case_content += a_step
        elif isinstance(step_dic['action'], list):
            for act in step_dic['action']:
                if isinstance(act, dict):
                    if "send_keys" in act:
                        self.case_content += a_step + ".send_keys(\"%s\")" % act['send_keys']
                    if "text" in act:
                        self.case_content += template.NTT + act['text'] + " = " + self.locator + ".text()"
                        self.test_var = act['text']
                    if "assert" in act:
                        for k, v in act["assert"].items():
                            if k == "$" + self.test_var:
                                self.case_content += template.NTT + "assert " + self.test_var + " == \"%s\"" % v
                            else:
                                self.case_content += template.NTT + "assert " + k + " " + v
                    if "sleep" in act:
                        self.case_content += template.NTT + "time.sleep(" + act['sleep'] + ")"
                    # for k, v in act.items():
                    #     a_step += ".%s(\"%s\")\n" % (k, v)
                elif isinstance(act, str):
                    a_step += "." + act + "()"
                    self.case_content += a_step

    def _generate_with_context(self, step_dic):
        if "id" in step_dic:
            if self.context == "webview":
                self.case_content += template.WEBVIEW_TO_NATIVE
                self.context = "native"
            # context = "native"
        elif "wid" in step_dic:
            if self.context == "native":
                self.case_content += template.NATIVE_TO_WEBVIEW

                self.context = "webview"

    @staticmethod
    def _generate_page_function(res, bys):
        for id_or_xpath, elements in bys.items():
            for func_name, element in elements.items():
                cur_func = template.PAGE_FUNCTION_TEMPLATE.replace("$LOCATE$", id_or_xpath) \
                    .replace("$ELEMENT$", "\"" + element + "\"") \
                    .replace("$FUNCTION_NAME$", func_name)
                res += cur_func
        return res

    @staticmethod
    def _write(path, content):
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'wb') as f:
            f.write(content.encode("utf-8"))

