# -*- coding: utf-8 -*-
import base64
import json
import re
import sys
import uuid
import cv2


def check_json_format(raw_msg):
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


def process_request(option):
    # 如果传path和image
    data_json = {}
    if type(option).__name__ == 'str':
        if re.findall(r'([^<>/\\\|:""\*\?]+\.\w+$)', option):
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
                'base64Data': base64_data,
                "imageId": str(uuid.uuid1())
            }
            data_json = json.dumps(data_dict)

        # 如果上传json object
        elif check_json_format(option):
            data_json = option
        else:
            data_dict = {
                "base64Data": option,
                "imageId": str(uuid.uuid1())
            }
            data_json = json.dumps(data_dict)

    # 如果传byte
    if type(option).__name__ == 'bytes':
        if sys.version_info.major == 2:
            base64_data = base64.b64encode(option)
        else:
            base64_data = base64.b64encode(option).decode()
        data_dict = {
            'base64Data': base64_data,
            "imageId": str(uuid.uuid1())
        }
        data_json = json.dumps(data_dict)
    # 如果传dict
    if type(option).__name__ == 'dict':
        data_json = json.dumps(option)

    if type(option).__name__ == "numpy.ndarray":
        retval, buffer = cv2.imencode('.jpg', option)
        if sys.version_info.major == 2:
            base64_data = base64.b64encode(buffer)
        else:
            base64_data = base64.b64encode(buffer).decode()
        data_dict = {
            'base64Data': base64_data,
            "imageId": str(uuid.uuid1())
        }
        data_json = json.dumps(data_dict)

    return data_json