# -*- coding: utf-8 -*-
import re
import json


def check_json_format(raw_msg):
    """
    判断字符串是不是json对象
    """
    if isinstance(raw_msg, str):  # 判断是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def check_chinese_format(raw_msg):
    """判断一个unicode是否是汉字"""
    if raw_msg >= u'\u4e00' and raw_msg <= u'\u9fa5':
        return True
    else:
        return False


def check_english_format(raw_msg):
    """判断一个unicode是否是英文字母"""
    if (raw_msg >= u'\u0041' and raw_msg <= u'\u005a') or (raw_msg >= u'\u0061' and raw_msg <= u'\u007a'):
        return True
    else:
        return False


def process_request(option, confidence):
    data_json = {}
    if type(option).__name__ == 'str':
        # 如果传text文件 path
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option):
            try:
                with open(option, "r",encoding="UTF-8") as f:
                    data = f.read()
            except IOError:
                print("error:The file was not found or read failed")
                return
            if check_chinese_format(data):
                data_dict = {
                    'data': data,
                    "confidence": confidence,
                    "language": "Chinese"
                }
                data_json = json.dumps(data_dict)
            if check_english_format(data):
                data_dict = {
                    'data': data,
                    "confidence": confidence,
                    "language": "English"
                }
                data_json = json.dumps(data_dict)
        # 如果传string message
        else:
            if check_chinese_format(option):
                data_dict = {
                    'data': option,
                    "confidence": confidence,
                    "language": "Chinese"
                }
                data_json = json.dumps(data_dict)
            if check_english_format(option):
                data_dict = {
                    'data': option,
                    "confidence": confidence,
                    "language": "English"
                }
                data_json = json.dumps(data_dict)

        # 如果上传jsonobject
        if check_json_format(option):
            data_json = option
    #如果上传byte
    if type(option).__name__ == 'bytes':
        data_str = option.decode()
        if check_chinese_format(data_str):
            data_dict = {
                'data': data_str,
                "confidence": confidence,
                "language": "Chinese"
            }
            data_json = json.dumps(data_dict)
        if check_english_format(data_str):
            data_dict = {
                'data': data_str,
                "confidence": confidence,
                "language": "English"
            }
            data_json = json.dumps(data_dict)

    #如果上传字典
    if type(option).__name__ == 'dict' :
        data_json = json.dumps(option)

    return data_json


def process_request_movie(option):
    data_json = {}
    if type(option).__name__ == 'str':
        # 如果传text文件 path
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option):
            try:
                with open(option, "r",encoding="UTF-8") as f:
                    data = f.read()
            except IOError:
                print("error:The file was not found or read failed")
                return
            if check_chinese_format(data):
                data_dict = {
                    "data": data,
                    "language": "cn-zh"
                }
                data_json = json.dumps(data_dict)
            if check_english_format(data):
                data_dict = {
                    'data': data,
                    "language": "en-us"
                }
                data_json = json.dumps(data_dict)
        # 如果传string message
        else:
            if check_chinese_format(option):
                data_dict = {
                    'data': option,
                    "language": "en-us"
                }
                data_json = json.dumps(data_dict)
            if check_english_format(option):
                data_dict = {
                    'data': option,
                    "language": "en-us"
                }
                data_json = json.dumps(data_dict)

        # 如果上传jsonobject
        if check_json_format(option):
            data_json = option
    #如果上传byte
    if type(option).__name__ == 'bytes':
        data_str = option.decode()
        if check_chinese_format(data_str):
            data_dict = {
                'data': data_str,
                "language": "Chinese"
            }
            data_json = json.dumps(data_dict)
        if check_english_format(data_str):
            data_dict = {
                'data': data_str,
                "language": "en-us"
            }
            data_json = json.dumps(data_dict)

    #如果上传字典
    if type(option).__name__ == 'dict' :
        data_json = json.dumps(option)


    return data_json
