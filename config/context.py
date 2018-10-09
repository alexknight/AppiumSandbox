
class Context(object):

    instance = None

    def __init__(self):
        self.android_desired_caps = {}
        self.ios_desired_caps = {}
        self.android_serial = None
        self.wd = None
        self.case_path = None

    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        else:
            obj = cls()
            cls.instance = obj
            return obj

    def set_android_desired_caps(self, args):
        self.android_desired_caps = args

    def get_android_desired_caps(self):
        return DictToObject(self.android_desired_caps)

    def set_ios_desired_caps(self, args):
        self.ios_desired_caps = args

    def get_ios_desired_caps(self):
        return DictToObject(self.ios_desired_caps)

    def set_android_serial(self, serial):
        self.android_serial = serial

    def get_android_serial(self):
        return self.android_serial

    def set_wd(self, wd):
        self.wd = wd

    def get_wd(self):
        return self.wd

    def set_case_path(self, path):
        self.case_path = path

    def get_case_path(self):
        return self.case_path


class DictToObject:
    def __init__(self, entries):
        self.__dict__.update(entries)


