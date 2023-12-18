import langid

def detect_language(text):
    lang, confidence = langid.classify(text)
    return lang, confidence

# 테스트 문자열
sample_text = "안녕하세요. 이것은 테스트입니다."

# 언어 감지 함수 호출
detected_language, confidence = detect_language(sample_text)

# 결과 출력
print(f"Detected Language: {detected_language}")
print(f"Confidence: {confidence}")