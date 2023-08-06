# -*- coding: utf-8 -*-
import json
from aiClient.NaturalLanguageProcessingClient import NaturalLanguageProcessing


def chinese_sentiment_analysis():
    """
    chinese Sentiment Analysis
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\NLP-sentiment.txt"
    # upload path
    data = natural_language_processing.chinese_sentiment_analysis(get_path(path))
    # upload string
    # data = natural_language_processing.chinese_sentiment_analysis(get_string(path))
    # upload byte
    # data = natural_language_processing.chinese_sentiment_analysis(get_byte(path))
    # upload dict
    # data = natural_language_processing.chinese_sentiment_analysis(get_dict(path))
    # upload json
    # data = natural_language_processing.chinese_sentiment_analysis(get_json(path))
    return data


def word_segmentation():
    """
    word Segmentation
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = natural_language_processing.word_segmentation(get_path(path))
    # upload string
    # data = natural_language_processing.word_segmentation(get_string(path))
    # upload byte
    # data = natural_language_processing.word_segmentation(get_byte(path))
    # upload dict
    # data = natural_language_processing.word_segmentation(get_dict(path))
    # upload json
    # data = natural_language_processing.word_segmentation(get_json(path))
    return data


def part_of_speech_tagging():
    """
    part Tagging
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = natural_language_processing.part_of_speech_tagging(get_path(path))
    # upload string
    # data = natural_language_processing.part_of_speech_tagging(get_string(path))
    # upload byte
    # data = natural_language_processing.part_of_speech_tagging(get_byte(path))
    # upload dict
    # data = natural_language_processing.part_of_speech_tagging(get_dict(path))
    # upload json
    # data = natural_language_processing.part_of_speech_tagging(get_json(path))
    return data


def lemmatization():
    """
    lemmatization
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = natural_language_processing.lemmatization(get_path(path))
    # upload string
    # data = natural_language_processing.lemmatization(get_string(path))
    # upload byte
    # data = natural_language_processing.lemmatization(get_byte(path))
    # # # # # upload dict
    # data = natural_language_processing.lemmatization(get_dict(path))
    # # # # upload json
    # data = natural_language_processing.lemmatization(get_json(path))
    return data


def named_entity_recognition():
    """
    named Entity Recognition
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = natural_language_processing.named_entity_recognition(get_path(path))
    # upload string
    # data = natural_language_processing.named_entity_recognition(get_string(path))
    # upload byte
    # data = natural_language_processing.named_entity_recognition(get_byte(path))
    # upload dict
    # data = natural_language_processing.named_entity_recognition(get_dict(path))
    # upload json
    # data = natural_language_processing.named_entity_recognition(get_json(path))
    return data


def parsing():
    """
    parsing
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = natural_language_processing.parsing(get_path(path))
    # upload string
    # data = natural_language_processing.parsing(get_string(path))
    # upload byte
    # data = natural_language_processing.parsing(get_byte(path))
    # upload dict
    # data = natural_language_processing.parsing(get_dict(path))
    # upload json
    # data = natural_language_processing.parsing(get_json(path))
    return data


def relationship_extraction():
    """
    relationship Extraction
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    natural_language_processing = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = natural_language_processing.relationship_extraction(get_path(path))
    # upload string
    # data = natural_language_processing.relationship_extraction(get_string(path))
    # upload byte
    # data = natural_language_processing.relationship_extraction(get_byte(path))
    # upload dict
    # data = natural_language_processing.relationship_extraction(get_dict(path))
    # upload json
    # data = natural_language_processing.relationship_extraction(get_json(path))
    return data


def coreference_resolution():
    """
    coreference Resolution
    """
    your_access_key = "1EFD41E96874F27199E162068355141F"
    your_secret_key = "F6F73EBC45BD05FF0D3C54DC5321C8D0"
    NlpClient = NaturalLanguageProcessing(your_access_key, your_secret_key)
    path = ".\\static\\Nlp-stanadford.txt"
    # upload path
    data = NlpClient.coreference_resolution(get_path(path))
    # upload string
    # data = NlpClient.coreference_resolution(get_string(path))
    # uploadbyte
    # data = NlpClient.coreference_resolution(get_byte(path))
    # upload dict
    # data = NlpClient.coreference_resolution(get_dict(path))
    # upload json
    # data = NlpClient.coreference_resolution(get_json(path))
    return data


def get_path(path):
    return path


def get_string(path):
    with open(path, "r", encoding="utf-8") as f:
        string_data = f.read()
    return string_data


def get_byte(path):
    byte_data = get_string(path).encode()
    return byte_data


def get_dict(path):
    string_data = get_string(path)

    data_dict = {
        'data': string_data,
    }

    return data_dict


def get_json(path):
    json_data = json.dumps(get_dict(path))
    return json_data


if __name__ == '__main__':
    print(chinese_sentiment_analysis())
    print(word_segmentation())
    print(part_of_speech_tagging())
    print(lemmatization())
    print(named_entity_recognition())
    print(parsing())
    print(relationship_extraction())
    print(coreference_resolution())
