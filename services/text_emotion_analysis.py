from google.cloud import language_v2
import json

"""text_emotion_analysis.py를 실행하고 싶은 경우"""
# from settings import get_projectId, get_secret

"""app.py를 실행하고 싶은 경우"""
from .settings import get_projectId, get_secret

# SECRET KEY 가져오기 
SECRET_API_KEY = get_secret("APIKEY_TEXT_EMOTION_ANALYSIS")
PROJECT_ID = get_projectId()

def analyze_sentiment(text_content):
    """
    문자열 내에서 감정 분석

    Args:
      text_content: 한 화자의 담화 문장들
      
    return:
        dict안에 다음의 변수들이 묶어서 들어감
            int : doc_sentiment_score, doc_sentiment_magnitude
            list : text_contents, senti_scores, senti_magnitude
    """
   
    client = language_v2.LanguageServiceClient(
        client_options={"api_key": SECRET_API_KEY, "quota_project_id": PROJECT_ID}
    )

    # Available types: PLAIN_TEXT, HTML
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language_code = "en"
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
    
    # input 문장들 각각에 대한 sentiment score, manitude
    text_contents = []
    senti_scores = []
    senti_magnitudes = []
    for sentence in response.sentences:
        text_contents.append(sentence.text.content)
        senti_scores.append(sentence.sentiment.score)
        senti_magnitudes.append(sentence.sentiment.magnitude)
    
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


def json_analyze_sentiment(jsonfile):
    """
    Speech to text 파일을 읽고, analyze_sentiment 진행
    
    Args:
        jsonfile : 감정 분석을 진행할 Speech to text를 마친 json 파일의 주소

    Returns:
        list : sentiment_results
            하나의 화자마다 analyze_sentiment로 나온 dict 결과들을 list로 묶어서 반환
    """
    # JSON 파일 읽기 예제
    with open(jsonfile, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    sentiment_results = []
    # 각 문장에 대해 감정 분석 수행
    for result in json_data["results"]:
        for alternative in result["alternatives"]:
            text = alternative["transcript"]
            sentiment_results.append(analyze_sentiment(text))
    
    return sentiment_results