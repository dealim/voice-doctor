# pip install google-cloud-aiplatform
import os
import json
from flask import current_app
import subprocess

import google.auth
import vertexai
import requests
from vertexai.preview.language_models import TextGenerationModel
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from settings import get_projectId, get_secret

current_dir = os.path.dirname(os.path.abspath(__file__))
questionnaire_dir = os.path.join(current_dir, 'questionnaire')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("HEALTH")

def text_summarization(
        filename: str,
        temperature: float,
        project_id: str,
        location: str,
        text: str,
        model_command: str
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
        model_command + text,
        **parameters,
    )
    
    with open(os.path.join(questionnaire_dir, filename), 'w') as f:
        json.dump(final_output, f)

    return response.text
    
