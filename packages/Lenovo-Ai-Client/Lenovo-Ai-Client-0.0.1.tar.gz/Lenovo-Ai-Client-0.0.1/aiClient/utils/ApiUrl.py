# -*- coding: utf-8 -*-
class AiUrl(object):
    # sdk在线获取token接口
    Ai_online_auth_url = "https://test-api.brain.lenovo.com/online-authorize"
    #Base Pre Url
    base_url = "https://test-api.brain.lenovo.com/"
    # Nothing just a extract
    token = "?token="
    #Version
    version = "/1.6"

    # NLP Word Segmentation Url
    word_segmentation = base_url + "apicore/nlp/word-segmentation" + version + token

    # NLP Post of Speech Tagging
    part_of_speech_tagging = base_url + "apicore/nlp/part-of-speech-tagging" + version + token

    # NLP Lemmatization
    lemmatization = base_url + "apicore/nlp/lemmatization" + version + token

    # NLP Named-Entity-Recognition
    named_entity_recognition = base_url + "apicore/nlp/named-entity-recognition" + version + token

    # NLP Parsing
    parsing = base_url + "apicore/nlp/parsing" + version + token

    # NLP Relation Extration
    relationship_extraction = base_url + "apicore/nlp/relationship-extraction" + version + token

    # Nlp Conference Resolution
    conference_resolution = base_url + "apicore/nlp/coreference-resolution" + version + token

    # Nlp Chinese Sentiment Analysis
    chinese_sentiment_analysis = base_url + "apicore/nlp/sentiment-analysis" + version + token

    # Vision Technologies
    # Object Recognition
    object_recognition = base_url + "apicore/cv/object-recognition" + version + token


    # Scene Recognition
    scene_recognition = base_url + "apicore/cv/scene-recognition" + version + token

    # Face Detection
    face_detection = base_url + "apicore/cv/face-detection" + version + token

    # Face Comparison
    face_comparison = base_url + "apicore/cv/face-comparison" + version + token

    # Face Attributes Detection
    face_attributes_recognition = base_url + "apicore/cv/face-attributes-detection" + version + token

    # Photo Segmentation
    face_segmentation = base_url + "apicore/cv/face-segmentation" + "/1.7" + token

    # Photo Evaluation
    photo_evaluation = base_url + "apicore/cv/photo-evaluation" + "/1.7" + token

    # FaceIdentification
    face_identification = base_url + "apicore/cv/face-identification" + "/1.7" + token


    face_library_list = base_url + "dev-service/rest/cv/face/libraries"

    face_library_get = base_url + "dev-service/rest/cv/face/libraries/"

    face_library_create = base_url + "dev-service/rest/cv/face/libraries"

    face_library_modify = base_url + "dev-service/rest/cv/face/libraries"

    face_library_copy= base_url + "dev-service/rest/cv/face/libraries/"

    face_library_delete= base_url + "dev-service/rest/cv/face/libraries/"

    face_group_list = base_url + "dev-service/rest/cv/face/groups"

    face_group_get = base_url + "dev-service/rest/cv/face/groups/"

    face_group_create = base_url + "dev-service/rest/cv/face/groups"

    face_group_modify = base_url + "dev-service/rest/cv/face/groups"

    face_group_copy = base_url + "dev-service/rest/cv/face/groups/"

    face_group_delete = base_url + "dev-service/rest/cv/face/groups/"

    face_person_list = base_url + "dev-service/rest/cv/face/persons"

    face_person_get = base_url + "dev-service/rest/cv/face/persons/"

    face_person_create = base_url + "dev-service/rest/cv/face/persons"

    face_person_modify = base_url + "dev-service/rest/cv/face/persons"

    face_person_copy= base_url + "dev-service/rest/cv/face/persons/"

    face_person_delete= base_url + "dev-service/rest/cv/face/persons/"

    file_upload = base_url + "file/upload/file"

    file_download = base_url + "file/download/file/{}"

    # Context Awareness
    # Gender Classification
    gender_classification = base_url + "/apicore/ca/gender-detection" + version + token

    # Scene Classification
    scene_classification = base_url + "/apicore/ca/scene-classification" + version + token

    # Ambient Detection
    ambient_detection = base_url + "/apicore/ca/ambient-detection" + version + token

    # Infant Crying Detection
    infant_crying_detection = base_url + "/apicore/ca/infant-crying-detection" + version + token

    # Knowledge Graph
    # Relationship Extraction
    relationship_extraction_kg = base_url + "/apicore/kg/relationship-extraction" + version + token

    # Entity Linking
    entity_linking = base_url + "/apicore/kg/entity-linking" + version + token

    # Movie KG
    movie_KG = base_url + "/apicore/kg/movie-kg" + "/1.7" + token

    # Music KG
    music_KG = base_url + "/apicore/kg/music-kg" + "/1.7" + token

    # Voice Technology
    # automatic speech recognition
    automatic_speech_recognition = base_url + "/apicore/voice/automatic-speech-recognition" + version + token

    # Realtime Speech Recognition
    realtime_speech_recognition = base_url + "/apicore/voice/realtime-speech-recognition" + "/1.7" + token

    #long_speech_recognition
    long_speech_recognition = base_url + "/apicore/voice/speech-file-recognition" + "/1.7" + token

