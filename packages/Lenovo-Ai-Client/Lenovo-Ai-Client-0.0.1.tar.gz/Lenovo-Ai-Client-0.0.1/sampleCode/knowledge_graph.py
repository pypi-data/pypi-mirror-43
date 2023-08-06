# -*- coding: utf-8 -*-
import json
from aiClient.KnowledgeGraphClient import KnowledgeGraph
from aiClient.utils.KgRequestProcess import check_chinese_format, check_english_format


def relationship_extraction():
    """
    Relationship Extraction
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    knowledge_graph = KnowledgeGraph(your_access_key, your_secret_key)
    path = ".\\static\\kg-chinese.txt"
    # upload path
    data = knowledge_graph.relationship_extraction(get_path(path))
    # upload string
    # data = knowledge_graph.relationship_extraction(get_string(path))
    # upload byte
    # data = knowledge_graph.relationship_extraction(get_byte(path))
    # upload dict
    # data = knowledge_graph.relationship_extraction(get_dict(path))
    # upload json
    data = knowledge_graph.relationship_extraction(get_json(path))

    return data


def entity_linking():
    """
    Entity Linking
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    knowledge_graph = KnowledgeGraph(your_access_key, your_secret_key)
    path = ".\\static\\kg-chinese.txt"
    # upload path
    data = knowledge_graph.entity_linking(get_path(path))
    # upload string
    # data = knowledge_graph.entity_linking(get_string(path))
    # upload byte
    # data = knowledge_graph.entity_linking(get_byte(path))
    # upload dict
    # data = knowledge_graph.entity_linking(get_dict(path))
    # upload json
    # data = knowledge_graph.entity_linking(get_json(path))
    return data


def movie_kg():
    """
    Movie KG
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    knowledge_graph = KnowledgeGraph(your_access_key, your_secret_key)
    path = ".\\static\\kg-movie.txt"
    # upload path
    data = knowledge_graph.movie_kg(get_path(path))
    # upload string
    # data = knowledge_graph.movie_kg(get_string(path))
    # upload byte
    # data = knowledge_graph.movie_kg(get_byte(path))
    # upload dict
    # data = knowledge_graph.movie_kg(get_dict_movie(path))
    # upload json
    # data = knowledge_graph.movie_kg(get_json(path))
    return data


def music_kg():
    """
    Movie KG
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    knowledge_graph = KnowledgeGraph(your_access_key, your_secret_key)
    path = ".\\static\\kg-music.txt"
    # upload path
    data = knowledge_graph.music_kg(get_path(path))
    # upload string
    # data = knowledge_graph.music_kg(get_string(path))
    # upload byte
    # data = knowledge_graph.music_kg(get_byte(path))
    # upload dict
    # data = knowledge_graph.music_kg(get_dict_movie(path))
    # upload json
    # data = knowledge_graph.music_kg(get_json(path))
    return data


def get_path(path):
    string_path = path
    return string_path


def get_string(path):
    with open(path, "r", encoding="utf-8") as f:
        string_data = f.read()
    return string_data


def get_byte(path):
    byte_data = get_string(path).encode()
    return byte_data


def get_dict(path):
    data_dict = {}
    string_data = get_string(path)
    if check_chinese_format(string_data):
        data_dict = {
            'data': string_data,
            "confidence": 0.5,
            "language": "Chinese"
        }
    if check_english_format(string_data):
        data_dict = {
            'data': string_data,
            "confidence": 0.5,
            "language": "English"
        }
    return data_dict


def get_dict_movie(path):
    string_data = get_string(path)
    if check_chinese_format(string_data):
        data_dict = {
            'data': string_data,
            "language": "cn-zh"
        }
    else:
        data_dict = {
            'data': string_data,
            "language": "en-us"
        }
    if check_english_format(string_data):
        data_dict = {
            'data': string_data,
            "language": "cn-zh"
        }
    else:
        data_dict = {
            'data': string_data,
            "language": "en-us"
        }
    return data_dict


def get_json(path):
    json_data = json.dumps(get_dict(path))
    return json_data


if __name__ == '__main__':
    print(relationship_extraction())
    print(entity_linking())
    print(movie_kg())
    print(music_kg())
