from google.cloud import documentai_v1 as documentai
import os

"""text_emotion_analysis.py를 실행하고 싶은 경우"""
from settings import get_projectId, get_secret

"""app.py를 실행하고 싶은 경우"""
# from .settings import get_projectId, get_secret

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(parent_dir, "keys", "applicationteam02-68f9ea71a356.json")

project_id = get_projectId()
location = 'us'  # Format is 'us' or 'eu'
processor_id = 'e9a0f80203309614'  # Create processor in Cloud Console
    
def process_document(file_path: str, mime_type: str) -> documentai.Document:
    """
    Processes a document using the Document AI API.
    """

    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = documentai_client.process_document(request=request)

        return result.document

def main():

    file_path = 'static\images\questionnaire_english.pdf'  # The local file in your current working directory
    mime_type = 'application/pdf'

    document = process_document(file_path=file_path, mime_type=mime_type)

    print("Document processing complete.")
    print(document.text)

    
main()