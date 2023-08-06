# -*- coding: utf-8 -*-
import base64
import json
import sys
from aiClient.ContextAwarenessClient import ContextAwareness


def gender_classification():
    """

    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    context_awareness = ContextAwareness(your_access_key, your_secret_key)
    # upload path
    path = ".\\static\\female.wav"
    data = context_awareness.gender_classification(get_path(path))
    # upload byte
    # data = context_awareness.gender_classification(get_byte(path))
    # upload dict
    # data = context_awareness.gender_classification(get_dict(path))
    # upload json
    # data = context_awareness.gender_classification(get_json(path))
    # upload base64
    # data = context_awareness.gender_classification(get_base64data(path))
    return data


def scene_classification():
    """

    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    context_awareness = ContextAwareness(your_access_key, your_secret_key)
    path = ".\\static\\car.wav"
    # upload path
    data = context_awareness.gender_classification(get_path(path))
    # upload byte
    # data = context_awareness.gender_classification(get_byte(path))
    # upload dict
    # data = context_awareness.gender_classification(get_dict(path))
    # upload json
    # data = context_awareness.gender_classification(get_json(path))
    # upload b64
    # data = context_awareness.gender_classification(get_base64data(path))

    return data


def ambient_detection():
    """

    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    context_awareness = ContextAwareness(your_access_key, your_secret_key)
    path = ".\\static\\ambient.wav"
    # upload path
    data = context_awareness.ambient_detection(get_path(path))
    # upload byte
    # data = context_awareness.ambient_detection(get_byte(path))
    # upload dict
    # data = context_awareness.ambient_detection(get_dict(path))
    # upload json
    # data = context_awareness.ambient_detection(get_json(path))
    # upload b64
    # data = context_awareness.ambient_detection(get_base64data(path))
    return data


def infant_crying_detection():
    """
    crying识别
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    context_awareness = ContextAwareness(your_access_key, your_secret_key)
    path = ".\\static\\cry_1.wav"
    # upload path
    data = context_awareness.infant_crying_detection(get_path(path))
    # upload byte
    # data = context_awareness.infant_crying_detection(get_byte(path))
    # upload dict
    # data = context_awareness.infant_crying_detection(get_dict(path))
    # upload json
    # data = context_awareness.infant_crying_detection(get_json(path))
    # upload base64
    # data = context_awareness.infant_crying_detection(get_base64data(path))
    return data


def get_path(path):
    """
    Convert path from file path
    """
    string_path = path
    return string_path


def get_byte(path):
    """
    Convert byte from file path
    """
    with open(path, "rb") as f:
        byte_data = f.read()
    return byte_data


def get_dict(path):
    """
    Convert to dictionary according to the file path
    """
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()
    data_dict = {
        "bit": 16,
        'base64Data': base64_data,
        "sampleRate": 8000,
        "windowSize": 2.56,
    }
    return data_dict


def get_json(path):
    """
    Convert to json according to the file path
    """
    json_data = json.dumps(get_dict(path))
    return json_data


def get_base64data(path):
    """
    Convert to base64data according to the file path
    """
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()

    return base64_data


if __name__ == '__main__':
    print(gender_classification())
    print(scene_classification())
    print(ambient_detection())
    print(infant_crying_detection())
