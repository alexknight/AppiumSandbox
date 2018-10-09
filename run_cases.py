import unittest
import os
import time
import argparse
import shutil

from multiprocessing import Process

from config.context import Context
from libs import htmlrunner, sysutil
from libs.handler import AndroidHandler, IOSHandler
from libs.sysutil import run_appium_server
from parser.parser import JsonParser


def run_test(platform="all"):
    if platform != "all":
        exec_test(platform)
    else:
        android_process = Process(target=exec_test, args=("android",))
        ios_process = Process(target=exec_test, args=("ios",))
        android_process.start()
        ios_process.start()
        android_process.join()
        ios_process.join()


def exec_test(platform):
    exec_suite = unittest.defaultTestLoader.discover(os.path.join(os.getcwd(), "uitests/" + platform), pattern='*_test.py')
    # 测试套件组合在一起
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    result_dir = os.path.join(os.getcwd(), r'report/', platform)  # 根据时间生成文件名
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)
    result_name = now + r'_result.html'
    fp = open(os.path.join(result_dir, result_name), 'wb')
    r = htmlrunner.HTMLTestRunner(stream=fp, title='报告标题', description='报告说明')
    r.run(exec_suite)


def android_test_prepare(args):
    global android_handler
    android_handler = AndroidHandler(args)
    if not android_handler.start_genymotion():
        raise Exception("没有找到android模拟器或者模拟器启动失败")


def ios_test_prepare():
    global ios_handler
    ios_handler = IOSHandler()


def android_test_finish():
    if android_handler is not None:
        android_handler.stop_genymotion()


def ios_test_finish():
    ios_handler.stop_simulator()


def str2dict(content):
    config = {}
    elements = content[1:-1].split(",")
    for element in elements:
        element.split(":")
        config[element.split(":")[0]] = element.split(":")[1]
    return config


@run_appium_server
def start(args):
    if args.platform == "ios":
        ios_test_prepare()
        run_test("ios")
        sysutil.stop_appium_server()
    elif args.platform == "android":
        android_test_prepare(args)
        run_test("android")
        android_test_finish()
    else:
        android_test_prepare(args)
        ios_test_prepare()
        run_test()
        android_test_finish()
        ios_test_finish()


def main():
    parser = argparse.ArgumentParser(description='自动化用例执行')
    parser.add_argument('--case-file', dest='case_file', help="case的json文件")
    parser.add_argument('--android-device', dest='android_device', help="android模拟器设备号，此项如果不输入，"
                                                                        + "脚本会自动按照desired-caps的platformVersion"
                                                                        + "参数来匹配服务器上的模拟器")
    parser.add_argument('--android-serial', dest='android_serial', help="android serial，如果有多台android设备时，请指定此参数")
    parser.add_argument('--ios-device', dest='ios_device', help="ios模拟器设备号")
    parser.add_argument('--platform', dest='platform', default='all', choices=('android', 'ios', 'all'), help="执行android/ios用例")
    parser.add_argument('--android-desired-caps', dest='android_desired_caps', help="android appium配置字典")
    parser.add_argument('--ios-desired-caps', dest='ios_desired_caps', help="ios appium配置字典")

    args = parser.parse_args()

    if args.android_desired_caps is not None:
        Context.get_instance().set_android_desired_caps(str2dict(args.android_desired_caps))
    if args.ios_desired_caps is not None:
        Context.get_instance().set_ios_desired_caps(str2dict(args.ios_desired_caps))
    if args.android_serial is not None:
        Context.get_instance().set_android_serial(args.android_serial)
    JsonParser(case_file=args.case_file).read().generate_cases()
    start(args)


if __name__ == '__main__':
    main()

