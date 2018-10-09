import time

from config.context import Context
from libs import sysutil


class AndroidHandler(object):
    def __init__(self, args):
        self.args = args
        if self.args.android_device is not None:
            self.genymotion = self.args.android_device
        else:
            self.genymotion = self.get_genymotion()

    def start_genymotion(self):
        try:
            sysutil.exec_shell("open -a /Applications/Genymotion.app/Contents/MacOS/player.app --args --vm-name '%s'" % self.genymotion)
            self._wait_for_system_booted()
        except Exception:
            raise Exception("可能是由于接入了多台android模拟器导致系统启动检查失败，也可能是模拟器启动失败")
        return True

    def stop_genymotion(self):
        pids = sysutil.get_pids(self.genymotion)
        sysutil.kill_pid(pids)

    def get_genymotion(self):
        config = Context.get_instance().get_android_desired_caps()
        genymotion_dic = sysutil.get_genymotions()
        flag = False
        genymotion = None
        try:
            for key in genymotion_dic.keys():
                if hasattr(config, 'platformVersion') and config.platformVersion in key:
                    genymotion = sysutil.get_genymotions()[key]
                    flag = True
                    break
            if flag:
                return genymotion
            elif len(genymotion_dic) > 0:
                # 如果没有配置genymotion，DesiredCaps也没有platformVersion信息，则默认取第一台
                return list(genymotion_dic.values())[0]
            else:
                raise Exception("没有找到" + config.platformVersion + "的设备")
        except Exception:
            raise Exception("没有找到对应的genymotion")

    def _wait_for_system_booted(self):
        timeout = 20
        while True:
            if sysutil.get_android_pids("com.android.systemui") != []:
                time.sleep(5)
                print("android模拟器启动完毕")
                break
            if timeout < 1:
                raise Exception("android模拟器启动失败")
            time.sleep(5)
            timeout = timeout-1


class IOSHandler(object):
    def __init__(self):
        pass

    def stop_simulator(self):
        lines = sysutil.exec_shell("xcrun simctl list | grep Booted").read().splitlines()
        if len(lines) > 0:
            for line in lines:
                sysutil.exec_shell("xcrun simctl shutdown " + line[line.index("(") + 1:line.index(")")])
