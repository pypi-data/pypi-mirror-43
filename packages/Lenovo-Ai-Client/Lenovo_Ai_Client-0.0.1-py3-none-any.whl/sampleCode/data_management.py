# -*- coding: utf-8 -*-
import jsonpath
from aiClient.DataManagementClient import DataManagement


def face_library_list():
    """
    LIST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_library_list()
    return data


def face_library_get(libname):
    """
    GET
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_library_get(libname)
    return data


def face_library_create(name, description="string"):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_library_create(name,description)
    return data


def face_library_modify(libId, name, description="string"):
    """
    Put
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_library_modify(libId,name,description)
    return data


def face_library_copy(libName, name, description="string"):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_library_copy(libName,name,description)
    return data


def face_library_delete(libName):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_library_delete(libName)
    return data


def face_group_list(libname):
    """
    LIST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_group_list(libname)
    return data


def face_group_get(libname):
    """
    GET
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_group_get(libname)
    return data


def face_group_create(name, libName, description="string"):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_group_create(name, libName, description)
    return data


def face_group_modify(groupId, name, libName, description="string"):
    """
    Put
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_group_modify(groupId, name, libName, description)
    return data


def face_group_copy(groupName, libName, name, description="string"):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key,your_secret_key)
    data = data_management.face_group_copy(groupName, libName, name, description)
    return data


def face_group_delete(groupName):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"

    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.face_group_delete(groupName)
    return data


def face_person_list(groupName, pageNum=1, pageSize=30):
    """
    LIST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.face_person_list(groupName, pageNum, pageSize)
    return data


def face_person_get(personId):
    """
    GET
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.face_person_get(personId)
    return data


def face_person_create(name, localpath, personId, groupNames=[], type=0, description="string"):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data_dict = data_management.file_upload(localpath)
    extension = jsonpath.jsonpath(data_dict,'$..extension')[0]
    imageId = jsonpath.jsonpath(data_dict,'$..fileId')[0]
    path = jsonpath.jsonpath(data_dict,'$..filePath')[0]

    data = data_management.face_person_create(name, personId, extension, imageId, path, groupNames, type, description)
    return data


def face_person_modify(name, personId, localpath, groupNames=[], type=0, description="string"):

    """
    Put Update face person’s name and its descripiton.
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data_dict = data_management.file_upload(localpath)
    extension = jsonpath.jsonpath(data_dict,'$..extension')[0]
    imageId = jsonpath.jsonpath(data_dict,'$..fileId')[0]
    path = jsonpath.jsonpath(data_dict,'$..filePath')[0]
    data = data_management.face_person_modify(name, personId, extension, imageId, path, groupNames, type, description)
    return data


def face_person_add_image(localpath, personId, type=0):
    """
    POST
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data_dict = data_management.file_upload(localpath)
    extension = jsonpath.jsonpath(data_dict,'$..extension')[0]
    imageId = jsonpath.jsonpath(data_dict,'$..fileId')[0]
    path = jsonpath.jsonpath(data_dict,'$..filePath')[0]
    data = data_management.face_person_add_image(extension, imageId, path, personId, type)
    return data


def delete_person(personId):
    """
    Delete a face person 将每个组里的这个person都删除
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.face_person_delete_person(personId)
    return data


def delete_person_group(groupName, personId):
    """

    delete person from group. 从某个组里删除这个person
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.face_person_delete_person_group(groupName, personId)
    return data


def delete_person_image(imageId, personId):
    """

    delete person from group. 从某个组里删除这个person
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.face_person_delete_person_image(imageId, personId)
    return data


def file_upload(local_path):
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.file_upload(local_path)
    return data


def file_download(fileId, file_name=None, download_path="./", file_extension="jpg"):
    if not file_name:
        file_name = fileId
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    data_management = DataManagement(your_access_key, your_secret_key)
    data = data_management.download_file(fileId, file_name, download_path, file_extension)
    return data

if __name__ == '__main__':
    print(face_library_list())
    print(face_library_get("chenjie01"))
    print(face_library_create("demodemo02"))
    print(face_library_modify(100111, "str", "str"))
    print(face_library_copy("str", "stringer"))
    print(face_library_delete("str"))

    print(face_group_list("chenjie01"))
    print(face_group_get("chenjie01"))
    print(face_group_create("test02", "chenjie01"))
    print(face_group_modify(100131, "test03", "chenjie01"))
    print(face_group_copy("test03", "chenjie01", "test05", "chenjie01"))
    print(face_group_delete("test03"))

    print(face_person_list("chenjie01"))
    print(face_person_get("chichchi"))
    print(face_person_create("test101", ".\\static\\face_1.jpg", "test10111", ["chenjie03", "chenjie02"]))
    print(face_person_modify("test13", "test10", ".\\static\\face_2.jpg", ["chenjie03", "chenjie02"]))
    print(face_person_add_image( ".\\static\\face_1.jpg","testdemo"))
    print(delete_person("test10"))
    print(delete_person_group("test_name","testdemo"))
    print(delete_person_image("f225940e338d4994a25ffde5bb0932ff","test06"))
    print(file_upload(".\\static\\face_1.jpg"))
    print(file_download("e418dd82d120406789f760ff0e250f08"))