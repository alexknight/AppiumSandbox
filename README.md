# 环境安装
## 1. `Python`依赖库安装
### （1）执行环境
Python3
### （2）第三方库
```bash
pip install -r requirements.txt
```

## 2.其他预装环境
运行环境目前只支持`Mac`，因为也只有`Mac`才能同时跑`Appium`的`Android`跟`IOS`用例
### （1）`Android`环境
- 安装`genymotion`以及一个`genymotion`的`android`模拟器，优先`android 7.0`
- 自行安装`Appium server`，测试过的版本是`1.9.1`

### （2）`IOS`环境
- `Xcode`以及`Simulator`

## 3.运行用例
### （1）参数说明
```bash
    parser.add_argument('--case-file', dest='case_file', help="case的json文件")
    parser.add_argument('--android-device', dest='android_device', help="android模拟器设备号，此项如果不输入，"
                                                                        + "脚本会自动按照desired-caps的platformVersion"
                                                                        + "参数来匹配服务器上的模拟器")
    parser.add_argument('--android-serial', dest='android_serial', help="android serial，如果有多台android设备时，请指定此参数")
    parser.add_argument('--ios-device', dest='ios_device', help="ios模拟器设备号")
    parser.add_argument('--platform', dest='platform', default='android', choices=('android', 'ios', 'all'), help="执行android/ios用例")
    parser.add_argument('--android-desired-caps', dest='android_desired_caps', help="android appium配置字典")
    parser.add_argument('--ios-desired-caps', dest='ios_desired_caps', help="ios appium配置字典")
```


### （2）用例运行
```bash
python run_cases.py 
    --case-file=open_website.json
    --platform=all
    --android-desired-caps={
        "platformVersion": "7.1",
        "deviceName": "Nexus",
        "platformName": "Android",
        "noReset": "False",
        "app": ".../example-debug.apk",
        "unicodeKeyboard": "True"}
    --ios-desired-caps={
        "platformVersion":"11.4",
        "deviceName":"iPhone Simulator",
        "platformName":"IOS",
        "app":".../PlanckDemoExample.app",
        "noReset":"False",
        "unicodeKeyboard":"True",
        "autoAcceptAlerts":"True",
        "connectHardwareKeyboard":"False"}
```
### （3）只运行android用例
```bash
python run_cases.py 
    --case-file=open_website.json
    --platform=android 
    --android-desired-caps={
        "platformVersion": "7.1",
        "deviceName": "Nexus",
        "platformName": "Android",
        "noReset": "False",
        "app": ".../example-debug.apk",
        "unicodeKeyboard": "True"}
```

### （3）只运行ios用例
```bash
python run_cases.py 
    --case-file=open_website.json
    --platform=ios 
    --ios-desired-caps={
        "platformVersion":"11.4",
        "deviceName":"iPhone Simulator",
        "platformName":"IOS",
        "app":".../PlanckDemoExample.app",
        "noReset":"False",
        "unicodeKeyboard":"True",
        "autoAcceptAlerts":"True",
        "connectHardwareKeyboard":"False"}
```

## 编写用例
怎么编写用例
```json
{
    "case": "OpenWebsite",    // 测试用例名
    "platform": "ios",        // 用例指定的平台
    "test_scene1":{           // 测试子用例，以test_开头
      "open_website":{        // 子用例操作步骤名，目前没有使用，但后续会支持步骤复用的功能
          "steps":[           // 子用例操作步骤，以list为载体，list的元素支持str跟map类型，目前支持的操作有clear，sleep，send_keys, swipe, click, assert, text操作
                {
                    "wid": "cn.ibona.t1_beta:id/start_button",
                    "action": [
                    "clear", {"sleep": "3"},
                    {"send_keys":"xxx"}, {"text":"a"}, {"assert": {"$a": "alex"}}
                  ]
                },
                {
                    "wid": "cn.ibona.t1_beta:id/start_button3",
                    "action": "click"
                }
            ]
      },

      "open_website2":{
            "steps":[
                {
                    "wid": "cn.ibona.t1_beta:id/start_button4",
                    "action": "click"
                },
                {
                    "id": "cn.ibona.t1_beta:id/start_button5",
                    "action": ["clear", {"send_key": "xxxx"}]
                },
                {
                    "id": "cn.ibona.t1_beta:id/start_button6",
                    "action": "click"
                }
            ]
        }
    },

  "test_scene2":{
      "open_website":{
          "steps":[
              {
                "id": "cn.ibona.t1_beta:id/start_button",
                "action": "click"
              },
              {
                "id": "cn.ibona.t1_beta:id/start_button2",
                "action": [
                  "clear", {"send_keys":"xxx"}
                ]
              },
              {
                "sleep": "3"
              }
            ]
      },

      "open_website2":{
            "steps":[
                {
                    "id": "cn.ibona.t1_beta:id/start_button4",
                    "action": "click"
                },
                {
                    "id": "cn.ibona.t1_beta:id/start_button5",
                    "action": "clear",
                    "send_key": "xxxx"
                },
                {
                    "id": "cn.ibona.t1_beta:id/start_button6",
                    "send_key": "xxxx",
                    "action": "click"
                }
            ]
        }
    }

}
```
用例转换结果：
```python
import time
from cases.base import AndroidBaseTest

class AndroidOpenWebsite(AndroidBaseTest):
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
```
