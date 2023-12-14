# pip install google-cloud-aiplatform
import os
import json
from flask import current_app
import subprocess

import google.auth
import vertexai
import requests
from vertexai.preview.language_models import TextGenerationModel
from .settings import get_secret, get_projectId
from google.auth.transport.requests import Request
from google.oauth2 import service_account

current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir, 'voice')
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("SUMMARY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("HEALTH")
PROJ = get_projectId()


def text_summarization(
        filename: str,
        temperature: float,
        project_id: str,
        location: str,
        text: str,
) -> str:
    """Summarization Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,
        # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        """Provide a summary for the following conversation in three sentences:""" + text,
        **parameters,
    )

    # 요약 완료
    summary = response.text
    current_app.logger.info("[text_summarization] : 요약 완료")
    print("summary:\n", summary)

    # 필요한 스코프 지정
    scopes = ['https://www.googleapis.com/auth/cloud-platform']

    # 서비스 계정을 사용하여 인증 정보 생성
    credentials = service_account.Credentials.from_service_account_file(
        get_secret("HEALTH"),
        scopes=scopes
    )

    # 기존 로직을 유지하면서 credentials 객체를 사용하여 헤더 설정
    credentials.refresh(Request())
    header = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }

    # print_token = subprocess.run('gcloud auth print-access-token', shell=True, capture_output=True, text=True).stdout.strip()
    # header={"Authorization": f"Bearer {print_token}", "Content-Type": "application/json"}

    # 데이터 및 URL 설정
    data = f"""{{
        "documentContent": "{response.text}",
        "alternativeOutputFormat": "FHIR_BUNDLE"
    }}"""
    url = "https://healthcare.googleapis.com/v1/projects/applicationteam02/locations/us-central1/services/nlp:analyzeEntities"

    # Healthcare API 요청
    response = requests.post(url, data=data, headers=header)
    current_app.logger.info("Healthcare API 응답 코드 : " + str(response.status_code))

    # 요약, 키워드 요소들만 뽑아서 json으로 저장
    print("response_json:\n", response_json)
    response_json = response.json()

    # entityMentions 키의 존재 여부 확인
    if "entityMentions" in response_json:
        filtered_entities = [mention for mention in response_json["entityMentions"] if "mentionId" in mention.keys()]
    else:
        filtered_entities = []

    final_output = {
        "summary": summary,
        "keywords": filtered_entities
    }

    with open(os.path.join(voice_dir, filename), 'w') as f:
        json.dump(final_output, f)

if __name__ == "__main__":
    text_summarization(current_dir + "/patient_text_request.json")
