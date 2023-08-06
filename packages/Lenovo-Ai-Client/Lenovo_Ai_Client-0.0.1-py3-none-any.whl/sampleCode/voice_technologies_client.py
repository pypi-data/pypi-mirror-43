# -*- coding: utf-8 -*-
import base64
import json
import sys
from aiClient.VoiceTechnologiesClient import VoiceTechnologies


def automatic_speech_recognition():
    """
    Automatic Speech Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    voice_technologies = VoiceTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\test1.wav"
    # upload path
    data = voice_technologies.automatic_speech_recognition(get_path(path))
    # upload byte
    # data = voice_technologies.automatic_speech_recognition(get_byte(path))
    # upload dict
    # data = voice_technologies.automatic_speech_recognition(get_dict(path))
    # upload json
    # data = voice_technologies.automatic_speech_recognition(get_json(path))
    # upload json
    # data = voice_technologies.automatic_speech_recognition(get_base64_data(path))
    return data


def realtime_speech_recognition(sessionId):
    """
    Realtime Speech Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    voice_technologies = VoiceTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\test1.wav"
    # upload path
    data = voice_technologies.realtime_speech_recognition(get_path(path), sessionId)
    # upload byte
    # data = voice_technologies.realtime_speech_recognition(get_byte(path), sessionId)
    # upload dict
    # data = voice_technologies.realtime_speech_recognition(get_dict_realtime(path), sessionId)
    # upload json
    # data = voice_technologies.realtime_speech_recognition(get_json(path), sessionId)
    # # upload json
    # data = voice_technologies.realtime_speech_recognition(get_base64_data(path), sessionId)
    return data


def long_speech_recognition():
    """
    Long Speech Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    voice_technologies = VoiceTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\test1.wav"
    # upload path
    data = voice_technologies.long_speech_recognition(get_path(path))
    # upload byte
    # data = voice_technologies.long_speech_recognition(get_byte(path))
    # upload dict
    # data = voice_technologies.long_speech_recognition(get_dict_long(path))
    # upload json
    # data = voice_technologies.long_speech_recognition(get_json(path))
    # upload json
    # data = voice_technologies.long_speech_recognition(get_base64_data(path))
    return data


def get_path(path):
    string_path = path
    return string_path


def get_byte(path):
    with open(path, "rb") as f :
        byte_data = f.read()
    return byte_data


def get_dict(path):
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()
    data_dict = {
        'sessionId': 1,
        "index": 1,
        "finished":1,
        "base64Data": base64_data
    }
    return data_dict


def get_dict_realtime(path):
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()
    data_dict = {
        'sampleRate': 16000,
        "bit": 16,
        "base64Data": base64_data
    }
    return data_dict


def get_dict_long(path):
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()
    data_dict = {
        "base64Data": base64_data
    }
    return data_dict


def get_json(path):
    json_data = json.dumps(get_dict(path))
    return json_data


def get_base64_data(path):
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()

    return base64_data


if __name__ == '__main__':
    print(automatic_speech_recognition())
    print(realtime_speech_recognition(1))
    print(long_speech_recognition())