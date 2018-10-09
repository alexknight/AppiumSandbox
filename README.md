# 环境安装
## 1. `Python`依赖库安装
### （1）执行环境
Python3
### （2）第三方库
```bash
pip install -r requirements.txt
```

## 2.其他预装环境
### （1）`Android`环境
- `genymotion`以及一个`genymotion`的`android`模拟器，优先`android 7.0`
- `Appium server`，测试过的版本是`1.9.1`

### （2）`IOS`环境

## 3.运行用例
### （1）参数说明
```angular2html
    parser.add_argument('--android-device', dest='android_device', help="android模拟器设备号，此项如果不输入，"
                                                                        + "脚本会自动按照desired-caps的platformVersion"
                                                                        + "参数来匹配服务器上的模拟器")
    parser.add_argument('--android-serial', dest='android_serial', help="android serial，如果有多台android设备时，请指定此参数")
    parser.add_argument('--ios-device', dest='ios_device', help="ios模拟器设备号")
    parser.add_argument('--platform', dest='platform', default='android', choices=('android', 'ios', 'all'), help="执行android/ios用例")
    parser.add_argument('--android-desired-caps', dest='android_desired_caps', help="android appium配置字典")
    parser.add_argument('--ios-desired-caps', dest='ios_desired_caps', help="ios appium配置字典")
```


### （2）默认运行所有用例
```bash
python run_cases.py 
    --android-desired-caps={"platformVersion":"7.1","deviceName":"Nexus"}
    --ios-desired-caps={"platformVersion":"7.1","deviceName":"Nexus"}
```
### （3）运行所有android用例
```bash
python run_cases.py --platform=android --android-desired-caps={"platformVersion":"7.1","deviceName":"Nexus"}
```

### （3）运行所有ios用例
```bash
python run_cases.py --platform=ios --ios-desired-caps={"platformVersion":"7.1","deviceName":"Nexus"}
```

### (4) 指定自己的`android`模拟器或者`ios`模拟器
```bash
python run_cases.py 
    --android-device=${android_device}
    --ios-device=${ios_device}
```