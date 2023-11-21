from google.cloud import language_v2
import json

def analyze_sentiment(text_content) -> None:
    """
    문자열 내에서 감정 분석
    아직 수정 중

    Args:
      text_content: The text content to analyze.
    """

    client = language_v2.LanguageServiceClient(
        client_options={"api_key": "AIzaSyC7xsFameXlL8adoNdQDtwtzHkvwqUmlLw", "quota_project_id": "appteam02"}
    )

    # text_content = 'I am so happy and joyful.'

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
    # Get overall sentiment of the input document
    print(f"Document sentiment score: {response.document_sentiment.score}")
    print(f"Document sentiment magnitude: {response.document_sentiment.magnitude}")
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(f"Sentence text: {sentence.text.content}")
        print(f"Sentence sentiment score: {sentence.sentiment.score}")
        print(f"Sentence sentiment magnitude: {sentence.sentiment.magnitude}")

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(f"Language of the text: {response.language_code}")

# JSON 파일 읽기 예제
with open('text_request.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 각 문장에 대해 감정 분석 수행
for result in json_data["results"]:
    for alternative in result["alternatives"]:
        text = alternative["transcript"]
        analyze_sentiment(text)