from google.cloud import documentai_v1 as documentai
import os
from summary_copy import text_summarization

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
    resource_name = documentai_client.processor_path(
        project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = documentai_client.process_document(request=request)

        return result.document.text

def main():

    # 문진표 파일 정보 
    mime_type = 'application/pdf'
    filename = "questionnaire_english.pdf"
    fileleftname = filename.rsplit('.')[0]
    file_path = os.path.join(parent_dir, "static", "images", filename)

    # 문진표 OCR
    text = process_document(file_path=file_path, mime_type=mime_type)
    print("OCR완료: \n",text)
    
    # OCR 진행한 파일에서 특정 정보 추출
    model_command = """Please compile information pertaining to \
            'NAME, DATE OF SERVICE, DATE OF BIRTH, DOCTOR, PATIENT, CHIEF COMPLAINT, ONSET OF SYMPTOMS, \
            MECHANISM OF INJURY, What makes the pain better?, What makes the pain worse?' and present it."""

    ## ocr 진행한 text 받아서 [파일이름]_ocr_result.json 으로 변환
    file_ocr_result = fileleftname + '_ocr_result.json'
    text_summarization(file_ocr_result, 0.0, 'applicationteam02', 'us-central1', text, model_command)
    print("OCR에서 정보 추출 완료")
    
main()