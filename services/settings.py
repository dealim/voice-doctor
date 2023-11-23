import os, json

# 현재 파일의 디렉토리를 기준으로 상위 디렉토리의 경로를 구함
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')

# 예시: 'keys/secrets.json' 파일의 경로를 상위 디렉토리 기준으로 구함
secret_file = os.path.join(parent_dir, 'keys', 'secrets.json')


with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_projectId():
    return "applicationteam02"


def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
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
    else:
        raise "{} 키를 찾을 수 없습니다.".format(setting)