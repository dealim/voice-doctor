# pip install google-cloud-aiplatform
import os
import json
import subprocess
import vertexai
import requests
from vertexai.language_models import TextGenerationModel
from .settings import get_secret, get_projectId

current_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("SUMMARY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("HEALTH")
# print_token = get_secret("dealimmmm") # $(gcloud auth print-access-token)
PROJ = get_projectId()

def text_summarization(
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

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        """Provide a summary with about two sentences for the following conversation:""" + text,
        **parameters,
        )

    summary = response.text

    data = f"""{{
        'documentContent': '{response.text}',
        'alternativeOutputFormat': 'FHIR_BUNDLE'
    }}"""
    # cli로 키받아오기
    print_token = subprocess.run('gcloud auth print-access-token', shell=True, capture_output=True, text=True).stdout.strip()
    print(print_token)
    header={"Authorization": f"Bearer {print_token}", \
            "Content-Type": "application/json"}
    url="https://healthcare.googleapis.com/v1/projects/applicationteam02/locations/us-central1/services/nlp:analyzeEntities"

    response = requests.post(url, data=data, headers=header)
    print(response.status_code, response.text)
    response_json = response.json()

    # 요약, 키워드 요소들만 뽑아서 json으로 저장
    filtered_entities = [mention for mention in response_json["entityMentions"] if "mentionId" in mention.keys()]
    final_output = {
        "summary": summary,
        "keywords": filtered_entities
    }

    with open(os.path.join(current_dir,'voice/health_response.json'), 'w') as f:
            json.dump(final_output, f)


if __name__ == "__main__":
    json_analyze_sentiment(current_dir + "/patient_text_request.json")
