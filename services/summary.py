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
    print_token = subprocess.run('gcloud auth print-access-token', shell=True, capture_output=True, text=True).stdout.strip()
    header={"Authorization": f"Bearer {print_token}", \
            "Content-Type": "application/json"}
    url="https://healthcare.googleapis.com/v1/projects/applicationteam02/locations/us-central1/services/nlp:analyzeEntities"

    response = requests.post(url, data=data, headers=header)
    response_json = response.json()
    # print(response.status_code, response.text)

    filtered_entities = [mention for mention in response_json["entityMentions"] if "mentionId" in mention.keys()]

    final_output = {
        "summary": summary,
        "keywords": filtered_entities
    }

    with open(os.path.join(current_dir,'voice/health_response.json'), 'w') as f:
            json.dump(final_output, f)

    return filtered_entities


def json_analyze_sentiment(jsonfile):

    # JSON 파일 읽기예
    with open(jsonfile, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    summarize_results = []
    # 각 문장에 대해 감정 분석 수행
    for result in json_data["results"]:
        for alternative in result["alternatives"]:
            text = alternative["transcript"]
            summarize_results.append(text_summarization(0.0, PROJ, 'us-central1', text))

    return summarize_results


if __name__ == "__main__":
    json_analyze_sentiment(current_dir + "/patient_text_request.json")
