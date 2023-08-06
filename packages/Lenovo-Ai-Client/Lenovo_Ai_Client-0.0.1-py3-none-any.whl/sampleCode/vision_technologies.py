# -*- coding: utf-8 -*-
import base64
import json
import sys
from aiClient.VisionTechnologiesClient import VisionTechnologies


def face_detection():
    """
    Face Detection
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\face_1.jpg"
    # upload path
    data = vision_technologies.face_detection(get_path(path))
    # upload byte
    # data = vision_technologies.face_detection(get_byte(path))
    # upload dict
    # data = vision_technologies.face_detection(get_dict(path))
    # upload json
    # data = vision_technologies.face_detection(get_json(path))
    # upload base64data
    # data = vision_technologies.face_detection(get_base64data(path))

    return data


def face_attribute_recognition():
    """
    Face Attributes Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\face_1.jpg"
    # upload path
    data = vision_technologies.face_attribute_recognition(get_path(path))
    # # uploadbyte
    # data = vision_technologies.face_attribute_recognition(get_byte(path))
    # # upload dict
    # data = vision_technologies.face_attribute_recognition(get_dict(path))
    # upload json
    # data = vision_technologies.face_attribute_recognition(get_json(path))
    # # upload base64data
    # data = vision_technologies.face_attribute_recognition(get_base64data(path))
    return data


def face_comparision():
    """

    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\face_1.jpg"
    # upload path
    data = vision_technologies.face_comparision(get_path(path), get_path(path))
    # upload byte
    # data = vision_technologies.face_comparision(get_byte(path), get_byte(path))
    # upload dict
    # data = vision_technologies.face_comparision(get_dict(path), get_dict(path))
    # upload json
    # data = vision_technologies.face_comparision(get_json(path), get_json(path))
    # upload base64data
    # data = vision_technologies.face_comparision(get_base64data(path), get_base64data(path))
    return data


def photo_evaluation():
    """

    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\face_1.jpg"
    # upload path
    data = vision_technologies.photo_evaluation(get_path(path))
    # upload byte
    # data = vision_technologies.photo_evaluation(get_byte(path))
    # upload dict
    # data = vision_technologies.photo_evaluation(get_dict(path))
    # upload json
    # data = vision_technologies.photo_evaluation(get_json(path))
    # upload base64data
    # data = vision_technologies.photo_evaluation(get_base64data(path))
    return data


def face_segmentation():
    """

    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\face_1.jpg"
    # upload path
    data = vision_technologies.face_segmentation(get_path(path))
    # upload byte
    # data = vision_technologies.face_segmentation(get_byte(path))
    # upload dict
    # data = vision_technologies.face_segmentation(get_dict(path))
    # upload json
    # data = vision_technologies.face_segmentation(get_json(path))
    # upload base64data
    # data = vision_technologies.face_segmentation(get_base64data(path))
    return data


def face_identification(groupNames, format="jpg"):
    """
    
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\timg.jpg"
    # upload path
    data = vision_technologies.face_identification(get_path(path), groupNames, format)
    # upload byte
    # data = vision_technologies.face_identification(get_byte(path), groupNames, format)
    # upload dict
    # data = vision_technologies.face_identification(get_dict(path), groupNames, format)
    # upload json
    # data = vision_technologies.face_identification(get_json(path), groupNames, format)
    # upload base64data
    # data = vision_technologies.face_identification(get_base64data(path), groupNames, format)
    return data


def object_recognition():
    """
    Object Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    vision_technologies = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\ImgRecognition_animal.jpg"
    # upload path
    data = vision_technologies.object_recognition(get_path(path))
    # upload byte
    # data = vision_technologies.object_recognition(get_byte(path))
    # upload dict
    # data = vision_technologies.object_recognition(get_dict(path))
    # upload json
    # data = vision_technologies.object_recognition(get_json(path))
    # upload base64data
    # data = vision_technologies.object_recognition(get_base64data(path))
    return data


def scene_recognition():
    """
    Scene Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    VisionClient = VisionTechnologies(your_access_key, your_secret_key)
    path = ".\\static\\ImgRecognition_animal.jpg"
    # upload path
    data = VisionClient.scene_recognition(get_path(path))
    # upload byte
    # data = VisionClient.scene_recognition(get_byte(path))
    # upload dict
    # data = VisionClient.scene_recognition(get_dict(path))
    # upload json
    # data = VisionClient.scene_recognition(get_json(path))
    # upload base64data
    # data = VisionClient.scene_recognition(get_base64data(path))
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
        'base64Data': base64_data
    }
    return data_dict


def get_json(path):
    json_data = json.dumps(get_dict(path))
    return json_data


def get_base64data(path):
    if sys.version_info.major == 2:
        base64_data = base64.b64encode(get_byte(path))
    else:
        base64_data = base64.b64encode(get_byte(path)).decode()

    return base64_data


if __name__ == '__main__':
    print(face_detection())
    print(face_attribute_recognition())
    print(face_comparision())
    print(face_segmentation())
    print(photo_evaluation())
    print(face_identification("chenjie02"))
    print(object_recognition())
    print((scene_recognition()))