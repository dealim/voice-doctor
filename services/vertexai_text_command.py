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

def text_generation(
        temperature: float,
        location: str,
        text: str,
        model_command: str,
) -> str:
    """Summarization Example with a Large Language Model"""
    
    # 같은 이름의 다른 환경 변수와 중복 시, 에러나기 때문에 함수 안으로 이동
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("HEALTH")
    
    vertexai.init(project=get_projectId(), location=location)
    
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,
        # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison")
    
    response = model.predict(
        model_command + text,
        **parameters,
    )

    # text generation 완료
    summary = response.text
    current_app.logger.info("text generation 완료")
    return summary