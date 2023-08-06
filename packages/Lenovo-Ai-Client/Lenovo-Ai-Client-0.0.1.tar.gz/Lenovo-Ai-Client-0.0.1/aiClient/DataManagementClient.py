# -*- coding: utf-8 -*-
from aiClient.AiBaseClient import AiBase
from aiClient.utils.ApiUrl import AiUrl


class DataManagement(AiBase):

    def face_library_list(self, pageNum=1, pageSize=30):
        """
        faceLibraryList
        """
        face_library_list_url = AiUrl.face_library_list
        params = {
            "token": {},
            "pageNum": pageNum,
            "pageSize": pageSize,
        }

        return self._request_get(face_library_list_url, params=params)

    def face_library_get(self, libName):
        """
         faceLibraryList
        """
        face_library_list_url = AiUrl.face_library_get + libName
        params = {
            "token": {},
        }

        return self._request_get(face_library_list_url, params=params)

    def face_library_create(self, name, description="string"):
        """
         faceLibraryCreate
        """
        face_library_list_url = AiUrl.face_library_create
        params = {
            "token": {}
        }
        data = {
            "description": description,
            "name": name
        }

        return self._request_post(face_library_list_url, params=params, data=data)

    def face_library_copy(self, libName, name, description="string"):
        """
         faceLibraryList
        """
        face_library_list_url = AiUrl.face_library_copy + libName + "/copy"
        params = {
            "token": {},
        }
        data = {
            "description": description,
            "name": name
        }

        return self._request_post(face_library_list_url, params=params, data=data)

    def face_library_modify(self, libId, name, description="string"):
        """
         faceLibraryList
        """
        face_library_list_url = AiUrl.face_library_get
        params = {
            "token": {},
        }
        data = {
            "description": description,
            "libId": libId,
            "name": name
        }

        return self._request_put(face_library_list_url, params=params, data=data)

    def face_library_delete(self, libName):
        """
         faceLibraryList
        """
        face_library_list_url = AiUrl.face_library_delete + libName
        params = {
            "token": {},
        }

        return self._request_delete(face_library_list_url, params=params)

    def face_group_list(self, libname, pageNum=1, pageSize=30):
        """
        faceGroupList
        """
        face_group_list_url = AiUrl.face_group_list
        params = {
            "token": {},
            "libName":libname,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }

        return self._request_get(face_group_list_url, params=params)

    def face_group_get(self, libName):
        """
         faceGroupGET
        """
        face_group_get_url = AiUrl.face_group_get + libName
        params = {
            "token": {},
        }

        return self._request_get(face_group_get_url, params=params)

    def face_group_create(self, name, libName, description="string"):
        """
         faceGroupCreate
        """
        face_group_create_url = AiUrl.face_group_create
        params = {
            "token": {}
        }
        data = {
            "description": description,
            "libName": libName,
            "name": name
        }

        return self._request_post(face_group_create_url, params=params, data = data)

    def face_group_copy(self, groupName, libName, name, description="string"):
        """
         faceGroupyList
        """
        face_group_list_url = AiUrl.face_group_copy + groupName + "/copy"
        params = {
            "token": {},
        }
        data = {
            "description": description,
            "libName":libName,
            "name": name
        }

        return self._request_post(face_group_list_url, params=params, data= data)

    def face_group_modify(self, groupId, name, libName, description="string"):
        """
         faceGroupList
        """
        face_group_list_url = AiUrl.face_group_get
        params = {
            "token": {},
        }
        data = {
            "description": description,
            "groupId": groupId,
            "name": name,
            "libName":libName
        }

        return self._request_put(face_group_list_url, params=params, data = data)

    def face_group_delete(self, groupName):
        """
         faceGroupGroupList
        """
        face_group_list_url = AiUrl.face_group_delete + groupName
        params = {
            "token": {},
        }

        return self._request_delete(face_group_list_url, params=params)


    def face_person_list(self, groupName, pageNum=1, pageSize=30):
        """
        facePersonList
        """
        face_person_list_url = AiUrl.face_person_list
        params = {
            "token": {},
            "groupName":groupName,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }

        return self._request_get(face_person_list_url, params=params)

    def face_person_get(self, personId):
        """
         facePersonList
        """
        face_person_list_url = AiUrl.face_person_get + personId
        params = {
            "token": {},
        }

        return self._request_get(face_person_list_url, params=params)


    def face_person_create(self, name, personId, extension, imageId, path, groupNames=[], type=0, description="string"):
        """

        :param type: default 0
        :param description: description
        :param kwargs:
        :return:
        """
        """
         facePersonCreate
        """
        face_person_list_url = AiUrl.face_person_create
        params = {
            "token": {}
        }
        data = {
            "description": description,
            "groupNames": groupNames,
            "images": [
                {
                    "extension": extension,
                    "imageId": imageId,
                    "path": path,
                    "type": type
                }
            ],
            "name": name,
            "personId": personId
        }

        return self._request_post(face_person_list_url, params=params, data = data)

    def face_person_add_image(self, extension, imageId, path, personId, type=0):
        """
         facePersonList
        """
        face_person_list_url = AiUrl.face_person_copy + personId + "/images"
        params = {
            "token": {},
        }
        data = {
            "extension": extension,
            "imageId": imageId,
            "path": path,
            "type": type
        }

        return self._request_post(face_person_list_url, params=params, data= data)

    def face_person_modify(self, name, personId, extension, imageId, path, groupNames, type=0, description="string"):
        """
         facePersonList
        """
        face_person_list_url = AiUrl.face_person_get
        params = {
            "token": {},
        }
        data = {
            "description": description,
            "groupNames":groupNames,
            "images": [
                {
                    "extension": extension,
                    "imageId": imageId,
                    "path": path,
                    "type": type
                }
            ],
            "name": name,
            "personId": personId
        }
        return self._request_put(face_person_list_url, params=params, data = data)

    def face_person_delete_person(self, libName):
        """
         Delete a face person 每个组里都删除这个person
        """
        face_person_list_url = AiUrl.face_person_delete + libName
        params = {
            "token": {},
        }

        return self._request_delete(face_person_list_url, params=params)

    def face_person_delete_person_group(self, groupName, PersonId):
        """
        delete person from group. 将某个组里删除person
        """
        face_person_list_url = AiUrl.face_person_delete + PersonId + "/groups/" + groupName
        params = {
            "token": {},
        }

        return self._request_delete(face_person_list_url, params=params)

    def face_person_delete_person_image(self, imageId, PersonId):
        """

        delete images from person 从这个person删除图片
        """
        face_person_list_url = AiUrl.face_person_delete + PersonId + "/images/" + imageId
        params = {
            "token": {},
        }

        return self._request_delete(face_person_list_url, params=params)

    def file_upload(self, path):
        """

        """
        upload_url = AiUrl.file_upload
        params = {
            "token": {},
        }
        files = {'file': open(path, 'rb')}
        return self._request_post_file(upload_url, params=params, files=files)

    def download_file(self, fileId, file_name, download_path, file_extension):
        """

        """
        if not file_name:
            file_name = fileId
        download_url = AiUrl.file_download.format(fileId)
        params = {
            "token": {},
        }
        return self._request_get_file(download_url, params,
                                      download_path, file_name,
                                      file_extension)