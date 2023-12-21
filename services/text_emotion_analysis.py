from google.cloud import language_v2
import json
import os

"""text_emotion_analysis.py를 실행하고 싶은 경우"""
# from settings import get_projectId, get_secret

"""app.py를 실행하고 싶은 경우"""
from .settings import get_projectId, get_secret

# SECRET KEY 가져오기 
SECRET_API_KEY = get_secret("APIKEY_TEXT_EMOTION_ANALYSIS")
PROJECT_ID = get_projectId()

# 현재 폴더 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))

def analyze_sentiment(text_content, stt_language_code):
    """
    문자열 내에서 감정 분석

    Args:
      text_content: 한 화자의 담화 문장들
      language_code: 문자열이 어느 나라 말인지 코드
      
    return:
        dict안에 다음의 변수들이 묶어서 들어감
            int : doc_sentiment_score, doc_sentiment_magnitude
            list : text_contents, senti_scores, senti_magnitude
    """
    print("text_content: ", text_content)
    client = language_v2.LanguageServiceClient(
        client_options={"api_key": SECRET_API_KEY, "quota_project_id": PROJECT_ID}
    )

    # Available types: PLAIN_TEXT, HTML
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    stt_language_codes = {"en-us":"en", "ko-kr":"ko", "ja-jp":"ja"}
    language_code = stt_language_codes[stt_language_code]

    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    # See https://cloud.google.com/natural-language/docs/reference/rest/v2/EncodingType.
    encoding_type = language_v2.EncodingType.UTF8

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    # input 문장들의 종합적인 sentiment score, manitude
    doc_sentiment_score = response.document_sentiment.score
    doc_sentiment_magnitude = response.document_sentiment.magnitude

    # input 문장들 각각에 대한 sentiment score, magnitude
    text_contents = []
    senti_scores = []
    senti_magnitudes = []
    for sentence in response.sentences:
        text_contents.append(sentence.text.content)
        senti_scores.append(round(sentence.sentiment.score,3))
        senti_magnitudes.append(round(sentence.sentiment.magnitude,3))

    # json 형식으로 묶어서 return
    sentiment_result = {
        "doc_sentiment_score" : doc_sentiment_score,
        "doc_sentiment_magnitude" : doc_sentiment_magnitude,
        "text_contents" : text_contents,
        "senti_scores" : senti_scores,
        "senti_magnitudes" : senti_magnitudes
    }

    """
    # input 문장들의 종합적인 sentiment score, manitude
    print("="*50)
    print(f"전체 감정 score: {doc_sentiment_score}")
    print(f"전체 감정 magnitude: {doc_sentiment_magnitude}")
    print("="*50)
    
    # input 문장들 각각에 대한 sentiment score, manitude
    for sentence in response.sentences:
        print(f"문장: {sentence.text.content}")
        print(f"감정 score: {sentence.sentiment.score}")
        print(f"감정 magnitude: {sentence.sentiment.magnitude}")
        print()

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(f"언어: {response.language_code}")
    """

    return sentiment_result


import json

def json_analyze_sentiment(jsonfile):
    """
    Speech to text 파일을 읽고, analyze_sentiment 진행

    Args:
        jsonfile : 감정 분석을 진행할 Speech to text를 마친 json 파일의 주소

    Returns:
        list : sentiment_results
            "transcript" 필드의 값들에 대한 감정 분석 결과를 list로 묶어서 반환
    """
    sentiment_results = []

    # JSON 파일 읽기
    with open(jsonfile, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    for result in json_data:
        transcript = result["transcript"]
        stt_language_code = result["language_code"]
        sentiment_result = analyze_sentiment(transcript, stt_language_code)
        sentiment_results.append(sentiment_result)

    return sentiment_results


# 환자용 JSON 파일 읽기 & 각 문장에 대해 감정 분석 수행
def get_json_sentiment(jsonfile, filename):
    patient = json_analyze_sentiment(jsonfile)

    with open(os.path.join(current_dir, 'voice', filename), 'w', encoding='utf-8') as f:
        json.dump(patient[0], f, ensure_ascii=False)