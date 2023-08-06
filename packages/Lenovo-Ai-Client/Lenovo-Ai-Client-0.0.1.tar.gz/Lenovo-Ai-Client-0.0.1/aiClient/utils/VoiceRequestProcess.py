# -*- coding: utf-8 -*-
import re
import json
import base64
import json
import sys


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


def process_request(option, rate):
    data_json = {}
    if type(option).__name__ == 'str':
        # 如果传音频文件path
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option) :
            try:
                with open(option, "rb") as f:
                    byte_data = f.read()
            except IOError:
                print("error:The file was not found or read failed")
                return
            if sys.version_info.major == 2:
                base64_data = base64.b64encode(byte_data)
            else:
                base64_data = base64.b64encode(byte_data).decode()
            data_dict = {
                'sampleRate': rate,
                "bit":16,
                "base64Data": base64_data
            }
            data_json = json.dumps(data_dict)

        # 如果上传jsonobject
        elif check_json_format(option):
            data_json = option
        else:
            data_dict = {
                'sampleRate': rate,
                "bit": 16,
                "base64Data": option
            }
            data_json = json.dumps(data_dict)

    # 如果传byte
    if type(option).__name__ == 'bytes':
        if sys.version_info.major == 2:
            base64_data = base64.b64encode(option)
        else:
            base64_data = base64.b64encode(option).decode()
        data_dict = {
            'sampleRate': rate,
            "bit": 16,
            "base64Data": base64_data
        }
        data_json = json.dumps(data_dict)

    #如果上传dict
    if type(option).__name__ == 'dict' :
        data_json = json.dumps(option)

    return data_json


def process_request_realtime(option, sessionId, index=1, finished=1):
    data_json = {}
    if type(option).__name__ == 'str':
        # 如果传音频文件path
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option) :
            try:
                with open(option, "rb") as f:
                    byte_data = f.read()
            except IOError:
                print("error:The file was not found or read failed")
                return
            if sys.version_info.major == 2:
                base64_data = base64.b64encode(byte_data)
            else:
                base64_data = base64.b64encode(byte_data).decode()
            data_dict = {
                'sessionId': sessionId,
                "index":index,
                "finished":finished,
                "base64Data": base64_data
            }
            data_json = json.dumps(data_dict)

        # 如果上传jsonobject
        elif check_json_format(option):
            data_json = option
        else:
            data_dict = {
                'sessionId': sessionId,
                "index":index,
                "finished":finished,
                "base64Data": option
            }
            data_json = json.dumps(data_dict)

    # 如果传byte
    if type(option).__name__ == 'bytes':
        if sys.version_info.major == 2:
            base64_data = base64.b64encode(option)
        else:
            base64_data = base64.b64encode(option).decode()
        data_dict = {
            'sessionId': sessionId,
            "index": index,
            "finished": finished,
            "base64Data": base64_data
        }
        data_json = json.dumps(data_dict)

    #如果上传dict
    if type(option).__name__ == 'dict' :
        data_json = json.dumps(option)

    return data_json


def process_request_long_speech(option):
    data_json = {}
    if type(option).__name__ == 'str':
        # 如果传音频文件path
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option) :
            try:
                with open(option, "rb") as f:
                    byte_data = f.read()
            except IOError:
                print("error:The file was not found or read failed")
                return
            if sys.version_info.major == 2:
                base64_data = base64.b64encode(byte_data)
            else:
                base64_data = base64.b64encode(byte_data).decode()
            data_dict = {
                "base64Data": base64_data
            }
            data_json = json.dumps(data_dict)

        # 如果上传jsonobject
        elif check_json_format(option):
            data_json = option
        else:
            data_dict = {
                "base64Data": option
            }
            data_json = json.dumps(data_dict)

    # 如果传byte
    if type(option).__name__ == 'bytes':
        if sys.version_info.major == 2:
            base64_data = base64.b64encode(option)
        else:
            base64_data = base64.b64encode(option).decode()
        data_dict = {
            "base64Data": base64_data
        }
        data_json = json.dumps(data_dict)

    #如果上传dict
    if type(option).__name__ == 'dict' :
        data_json = json.dumps(option)

    return data_json
