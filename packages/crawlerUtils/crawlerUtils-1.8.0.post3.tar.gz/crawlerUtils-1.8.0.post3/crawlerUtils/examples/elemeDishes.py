import requests
from ..captcha import recognizeCaptcha, getRequsetCaptcha, CAPTCHA_SET_PATH
from ..utils import Get, Post
from PIL import Image
import hashlib
import time
import os
import sys
import psutil
import json


__all__ = ["runElemeDishes"]


def getLocationGeohash(location=None):
    ''' 获取指定位置的经度、纬度、以及Geohash '''
    if not location:
        location = input("请输入你的地址：")

    location_headers = {
        "Referer": "https://lbs.amap.com/console/show/picker",
    }
    location_url = "https://restapi.amap.com/v3/place/text"
    location_params = {
        "s": "rsv3",
        "children": "",
        "key": "8325164e247e15eea68b59e89200988b",
        "page": "1",
        "offset": "10",
        "city": "110000",
        "language": "zh_cn",
        "callback": "jsonp_197519_",
        "platform": "JS",
        "logversion": "2.0",
        "sdkversion": "1.3",
        "appname": "https://lbs.amap.com/console/show/picker",
        "csid": "08E442FB-F19E-4A27-B2B9-73F15E44DA80",
        "keywords": location,
    }

    location_text = Get(location_url, location_headers, params=location_params).text
    begin = location_text.find("{")
    end = -1
    location_json = json.loads(location_text[begin:end])
    longitude, latitude = location_json['pois'][0]['location'].split(",")
    geohash = Get.geohashEncode(latitude, longitude)
    return longitude, latitude, geohash


def getRestaurantInformation(headers, longitude, latitude, geohash):
    ''' 获取餐馆信息 '''
    restaurant_url = "https://www.ele.me/restapi/shopping/restaurants"

    restaurant_params = {
        "extras[]": "activities",
        "geohash": geohash,
        "latitude": latitude,
        "limit": "24",
        "longitude": longitude,
        "offset": "0",
        "terminal": "web",
    }

    restaurant_json = Get(restaurant_url, headers=headers, params=restaurant_params).json
    for rest in restaurant_json:
        rest_name = rest["name"]
        rest_address = rest["address"]
        rest_business_time = rest["next_business_time"]

        print(f"餐馆名称：{rest_name}")
        print(f"餐馆地址：{rest_address}")
        print(f"营业时间：{rest_business_time}")


def inputRightCaptchaCode():
    ''' 把正确的验证码添加到训练集 '''
    captcha_image = Image.open(CAPTCHA_SET_PATH + "/captcha.jpeg")
    # process_list = []
    # for proc in psutil.process_iter():
    #     process_list.append(proc)

    captcha_image.show()
    right_captcha_code = input(
        f"\n\n请输入图片中的验证码以提高下次识别的准确性, 不认识的验证码字符请以*代替：")
    letters = [x for x in range(1, 5)]
    for i in range(len(letters)):
        letter_path = CAPTCHA_SET_PATH + \
            f"/captcha_binary___{str(letters[i])}.jpeg"
        m = hashlib.md5()
        m.update(("%s%s" % (time.time(), i)).encode("utf-8"))
        if right_captcha_code[i] != "*":
            new_path = CAPTCHA_SET_PATH + \
                f"/{right_captcha_code[i]}/" + m.hexdigest() + ".jpeg"
            os.system(f"mv '{letter_path}' '{new_path}'")
        else:
            os.system(f"rm -f '{letter_path}'")
    binary_path = CAPTCHA_SET_PATH + '/captcha_binary.jpeg'
    os.system(f"rm -f '{binary_path}'")
    image_path = CAPTCHA_SET_PATH + '/captcha.jpeg'
    os.system(f"rm -f '{image_path}'")

    # for proc in psutil.process_iter():
    #     if not proc in process_list:
    #         try:
    #             proc.kill()
    #         except Exception:
    #             pass


def mobileSendCode(headers, captcha_hash, captcha_code, telephone_number):
    ''' 输入验证码 '''
    token_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"

    token_params = {
        "captcha_hash": captcha_hash,
        "captcha_value": captcha_code,
        "mobile": telephone_number,
        "scf": "ms",
    }

    token_json = Post(token_url, headers=headers, jsons=token_params).json

    if token_json.get("validate_token"):
        validate_token = token_json["validate_token"]
        # print(f"获取到的token为：{validate_token}")
        print("验证码识别成功！")
        inputRightCaptchaCode()
        return validate_token
    elif token_json.get("message"):
        print("验证码识别错误！")
        inputRightCaptchaCode()
        sys.exit(0)


def captchaLogin(headers, telephone_number, validate_token):
    ''' 验证码登陆 '''
    captcha_login_url = "https://h5.ele.me/restapi/eus/login/login_by_mobile"

    captcha_login_params = {
        "mobile": telephone_number,
        "scf": "ms",
        "validate_code": input("请输入你手机收到的验证码："),
        "validate_token": validate_token,
    }

    res = Post(captcha_login_url, headers, jsons=captcha_login_params)
    # print(captcha_text)
    # print(session.cookies)
    if "错误" in res.text:
        print("登录失败！")
        sys.exit(0)
    else:
        print("登录成功！")
        captcha_text = res.cookiesToFile()


def getRequsetSendcode(headers, telephone_number="15201538136"):
    ''' 发送手机验证码 '''
    global SENDCODE_URL

    sendcode_params = {
        "captcha_hash": "",
        "captcha_value": "",
        "mobile": telephone_number,
        "scf": "ms",
    }

    sendcode_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"

    sendcode_json = Post(sendcode_url, headers=headers, jsons=sendcode_params).json
    if sendcode_json.get("validate_token"):
        validate_token = sendcode_json['validate_token']

    # print(session.cookies)
    # 识别验证码并登陆获取cookies
    if sendcode_json.get("name") == "NEED_CAPTCHA":
        *_, captcha_hash = getRequsetCaptcha(headers, telephone_number)
        # print(f"验证码hash：{captcha_hash}")
        captcha_code = recognizeCaptcha()
        validate_token = mobileSendCode(headers, captcha_hash, captcha_code, telephone_number)
        captchaLogin(headers, telephone_number, validate_token)
    elif sendcode_json.get("name") == "VALIDATION_TOO_BUSY":
        print("请求验证码太频繁，请稍后重试")
        sys.exit(0)
    else:
        captchaLogin(headers, telephone_number, validate_token)


def runElemeDishes(telephone_number=None):
    headers = {
        "referer": "https://h5.ele.me/login/"
    }

    Post.cookiesRead()
    if not Post.session.cookies:
        while not telephone_number:
            telephone_number = input("请输入手机号：")

        getRequsetSendcode(headers, telephone_number)

    # 获取经纬坐标以及geohash
    longitude, latitude, geohash = getLocationGeohash()
    # 获取餐馆信息
    getRestaurantInformation(headers, longitude, latitude, geohash)
