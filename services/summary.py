# pip install google-cloud-aiplatform
import os
import json
import vertexai
from vertexai.language_models import TextGenerationModel
from .settings import get_secret, get_projectId
import requests
current_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("SUMMARY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("HEALTH")
print_token = get_secret("dealimmmm") # $(gcloud auth print-access-token)
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
        "temperature": temperature, # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256, # Token limit determines the maximum amount of text output.
        "top_p": 0.95,
        # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        """Provide a summary with about two sentences for the following conversation:""" + text,
        **parameters,
    )
    # print(response.text)
    data = f"""{{
        'documentContent': '{response.text}',
        'alternativeOutputFormat': 'FHIR_BUNDLE'
    }}"""
    
    header={"Authorization": f"Bearer {print_token}", \
            "Content-Type": "application/json"}
    url="https://healthcare.googleapis.com/v1/projects/applicationteam02/locations/us-central1/services/nlp:analyzeEntities"
    res = requests.post(url, data=data, headers=header)
    print(res)
    return response.text


def json_summary(jsonfile):

    # JSON 파일 읽기 예제
    with open(jsonfile, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    summarize_results = []
    # 요약 수행
    for result in json_data:
        transcript = result["transcript"]
        summarize_results.append(text_summarization(0.0, PROJ, 'us-central1', transcript))

    with open(current_dir + '/voice/summary.json', 'w') as json_file:
        json.dump(summarize_results, json_file, indent=4)

    print('summary.json 생성 완료')



if __name__ == "__main__":
    json_summary(current_dir + "/voice/stt.json")