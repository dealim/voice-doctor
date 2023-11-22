#pip install google-cloud-aiplatform
import os
import vertexai
from vertexai.language_models import TextGenerationModel
from settings import get_secret

def text_summarization(
    temperature: float,
    project_id: str,
    location: str,
) -> str:
    """Summarization Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        """Provide a summary with about two sentences for the following conversation:""" + 
        """Um-hum . Yeah. Hello , good morning . Good
          morning . So , tell me what's going on . Uh , sure , so , um , I
          woke up probably three or four days ago , which , uh , wheezing and short of breath .
          Okay , any cough or chest pain ? I cough infrequently , but no ,
          uh , chest pain . Have you been exposed to anyone with covid ?
          Uh , no , and I also took a test , which was negative . Uh , is it getting
          worse , or better ? Uh , it has been getting a lot worse
""",
        **parameters,
    )
    print(f"Response from Model: {response.text}")

    return response.text

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("SUMMARY")
    text_summarization(0.0, 'applicationteam02', 'us-central1')