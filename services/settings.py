import os, json

# secrets.json 파일 위치를 명시
BASE_PATH = os.environ['PYTHONPATH']
secret_file = os.path.join(BASE_PATH, 'keys\secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_projectId():
    return "appteam02"

def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "{} 키를 찾을 수 없습니다.".format(setting)
        return error_msg


