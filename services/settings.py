import os, json

# 현재 파일의 디렉토리를 기준으로 상위 디렉토리의 경로를 구함
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 예시: 'keys/secrets.json' 파일의 경로를 상위 디렉토리 기준으로 구함
secret_file = os.path.join(parent_dir, 'keys', 'secrets.json')

try:
    with open(secret_file) as f:
        secrets = json.loads(f.read())
except Exception as e:
    print("파일 읽기 오류:", e)

def get_projectId():
    return "voicedoctor"

def get_secret(setting):
    if setting == "APIKEY_TEXT_EMOTION_ANALYSIS":
        return secrets[setting]
    elif setting == "SUMMARY":
        return os.path.join(parent_dir, 'keys', secrets[setting])
    elif setting == "HEALTH":
        return os.path.join(parent_dir, 'keys', secrets[setting])
    elif setting == "seunggu":
        return secrets[setting]
    elif setting == "STT":
        return os.path.join(parent_dir, 'keys', secrets[setting])
    elif setting == "OCR":
        return os.path.join(parent_dir, 'keys', secrets[setting])
    elif setting == "VERTEX_AI":
        return os.path.join(parent_dir, 'keys', secrets[setting])
    else:
        raise "{} 키를 찾을 수 없습니다.".format(setting)