# -*- coding: utf-8 -*-
import base64
import json
import re
import json
import sys


def checkJsonFormat(raw_msg):
    """
    判断字符串是不是json对象
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def process_request(option, bit, rate, windowSize):
    data_json = {}
    if type(option).__name__ == 'str':
        # 如果传text文件 path
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option):
            try:
                with open(option, "rb") as f:
                    byte_data = f.read()
            except IOError:
                print("Error: The file was not found or read failed")
                return
            if sys.version_info.major == 2:
                base64_data = base64.b64encode(byte_data)
            else:
                base64_data = base64.b64encode(byte_data).decode()
            data_dict = {
                "bit": bit,
                'base64Data': base64_data,
                "sampleRate": rate,
                "windowSize": windowSize,
            }
            data_json = json.dumps(data_dict)

        # 如果上传jsonobject
        elif checkJsonFormat(option):
            data_json = option

        else:
            data_dict = {
                "bit": bit,
                'base64Data': option,
                "sampleRate": rate,
                "windowSize": windowSize,
            }
            data_json = json.dumps(data_dict)

    # 如果上传byte
    if type(option).__name__ == 'bytes':
        if sys.version_info.major == 2:
            base64_data = base64.b64encode(option)
        else:
            base64_data = base64.b64encode(option).decode()
        data_dict = {
            "bit": bit,
            'base64Data': base64_data,
            "sampleRate": rate,
            "windowSize": windowSize,
        }
        data_json = json.dumps(data_dict)

    # 如果上传字典
    if type(option).__name__ == 'dict':
        data_json = json.dumps(option)

    return data_json
