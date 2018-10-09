import os

from multiprocessing import Process
from config.context import Context


def get_genymotions():
    try:
        genymotions = {}
        resp = exec_shell("VBoxManage list vms", True)
        print("设备列表：\n" + resp)
        for line in resp.splitlines():
            genymotions[line.split(" ")[2]] = line.split(" ")[-1][1:-1]
        return genymotions
    except Exception:
        raise Exception("没有找到模拟器设备")


def get_pids(process):
    pids = []
    try:
        lines = exec_shell("ps -ef | grep " + process + " | grep -v grep").read().splitlines()
        if len(lines) > 0:
            for line in lines:
                pids.append(line.split(" ")[3])
    except Exception:
        pass
    return pids


def get_android_pids(process):
    pids = []
    try:
        lines = exec_android_shell("shell ps | grep " + process, rst=True).splitlines()
        if len(lines) > 0:
            for line in lines:
                pids.append(line.split(" ")[4])
    except Exception:
        pass
    return pids


def kill_pid(pids):
    if isinstance(pids, list):
        for pid in pids:
            os.kill(pid, 9)
    else:
        os.kill(pids, 9)


def exec_shell(command, rst=False, throw=True):
    try:
        if rst:
            return os.popen(command).read()
        else:
            os.popen(command)
    except Exception as e:
        if throw is False:
            print(command+"执行失败\n" + str(e))
        else:
            raise Exception(command+"执行失败\n" + str(e))


def exec_android_shell(command, rst=False):
    serial = Context.get_instance().get_android_serial()
    if serial is not None:
        cmd = "adb -s " + serial + " " + command
    else:
        cmd = "adb " + command

    return exec_shell(cmd, rst)


def _start(port):
    exec_shell("appium --port=" + port)


def start_appium_server(port):
    p = Process(target=_start, args=(str(port),))
    p.start()
    p.join()
    # os.system("appium --port=" + str(port) + " &")
    # print("appium: " + str(port) + "启动成功")


def stop_appium_server():
    pids = get_pids("appium")
    kill_pid(pids)


def run_appium_server(func):
    def wrapper(args):
        if args.platform == "all":
            start_appium_server("4723")
            start_appium_server("3274")
        elif args.platform == "android":
            start_appium_server("4723")
        else:
            start_appium_server("3274")
        result = func(args)
        stop_appium_server()
        return result
    return wrapper


if __name__ == '__main__':
    get_genymotions()
