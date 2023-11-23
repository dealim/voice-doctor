# pip install google-cloud-aiplatform
import os
import json
import vertexai
from vertexai.language_models import TextGenerationModel
from settings import get_secret, get_projectId
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("SUMMARY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("HEALTH")
print_token = get_secret("seunggu") # $(gcloud auth print-access-token)
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
    print(response.text)
    data = f"""{{
        'documentContent': '{response.text}',
        'alternativeOutputFormat': 'FHIR_BUNDLE'
    }}"""
    
    header={"Authorization": f"Bearer {print_token}", \
            "Content-Type": "application/json"}
    url="https://healthcare.googleapis.com/v1/projects/applicationteam02/locations/us-central1/services/nlp:analyzeEntities"
    res = requests.post(url, data=data, headers=header)
    print(res.status_code, res.text)

    return response.text


def json_analyze_sentiment(jsonfile):
    """
    Speech to text 파일을 읽고, summarize 진행
    
    Args:
        jsonfile : 감정 분석을 진행할 Speech to text를 마친 json 파일의 주소

    Returns:
        list : summarize
            하나의 화자마다 summarize로 나온 dict 결과들을 list로 묶어서 반환
    """
    # JSON 파일 읽기 예제
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
    json_analyze_sentiment("C:\\Users\\seunggu\\Desktop\\GCP-TEAM2\\services\\patient_text_request.json")
