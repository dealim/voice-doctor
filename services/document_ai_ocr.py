from google.cloud import documentai_v1 as documentai
import os
import json
from flask import current_app
from services.vertexai_text_command import text_generation
from services.filesave import save_file
from .settings import get_secret, get_projectId
import langid

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret("OCR")

project_id = get_projectId()
location = 'us'  # Format is 'us' or 'eu'
processor_id = '3e3e9b508026de35'  # Create processor in Cloud Console

def process_document(file_path: str, mime_type: str) -> str:
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

def detect_language(text):
    """
    문자열의 언어 감지 
    (langid 라이브러리 사용 -> language, confidence가 tuple 형식으로 묶여서 return됨)
    """
    lang = langid.classify(text)[0]
    return lang

def get_ocr_json(pdf_file_name, saved_ocr_name):
    # 문진표 파일 정보
    file_path = os.path.join(current_dir, "voice", pdf_file_name)

    # 문진표 OCR 진행
    text = process_document(file_path=file_path, mime_type='application/pdf')
    print("text: ", text)

    # 문진표 언어 감지
    lang = detect_language(text)
    print("language: ", lang)

    # OCR 진행한 파일에서 특정 정보 추출
    if lang == 'en':
        doc_info_export_command = """Please compile information pertaining to \
                'NAME, DATE OF SERVICE, SEX, DATE OF BIRTH, DOCTOR, PATIENT, CHIEF COMPLAINT, ONSET OF SYMPTOMS, \
                MECHANISM OF INJURY, What makes the pain better?, What makes the pain worse?' \
                and Pair each key with its corresponding value and format it in JSON:"""
        
    elif lang == 'ja':
        doc_info_export_command = """Please compile information pertaining to \
                'NAME, DATE OF SERVICE, SEX, DATE OF BIRTH, DOCTOR, PATIENT, CHIEF COMPLAINT, ONSET OF SYMPTOMS, \
                MECHANISM OF INJURY, What makes the pain better?, What makes the pain worse?' \
                and Pair each key with its corresponding value and format it in JSON:"""
        # doc_info_export_command = """Please compile information pertaining to \
        #     "Name, DATE OF SERVICE, Date of Birth, Address (Postal Code), Phone Number, Height, Weight, Gender, Body Temperature, \
        #     What symptoms are you experiencing today?, When did these symptoms start?, \
        #     Please check the applicable symptoms, Do you have any allergies to medications or food?, \
        #     Have you had any previous illnesses?, Are you currently undergoing treatment for any illness?, Are you currently taking any medication?"
        #     and pair each key with its corresponding value and format it in JSON:"""

        # doc_info_export_command = """일본 병원 문진표를 보고, 수집할 수 있는 내용을 정리해서 KEY와 VALUE 형태인 JSON으로 정리해줘"""
        # doc_info_export_command = """일본 병원 문진표를 보고, "이름, 직업, 체온, \
        #     증상의 유무(발열, 기침, 숨쉬기 힘든지, 목구멍 통증, 콧물, 강한 나른함, 두통, 미각후각장애, 구기 구토, 설사, 기타 증상)와 증상의 발현일, \
        #     증상에 대해 약을 사용했는지(시간과 약 종류), \
        #     2주 이내의 행동과 접촉 상황(해외 여행을 갔다면 나라와 귀국일, 현외이동이라면 장소와 이동일, 회식을 했다면 장소와 날짜와 동석자와의 관계, \
        #         코로나 양성자와 접촉했다면 최종 접촉일과 접촉 내용, 양성자와의 관계), \
        #     신형 코로나 백신의 접종 상황(접종여부, 접종 횟수, 최근 접종 날짜, 최근 접종한 신형 코로나 백신 제조 업체), 기초 질환의 유무와 종류" \
        #     내용을 정리해서 KEY와 VALUE 형태인 JSON으로 정리해줘"""
    doc_info_export_result = text_generation(0.0, 'us-central1', text, doc_info_export_command)
    # print("doc_info_export_result: ", doc_info_export_result)

    # 텍스트를 JSON으로 변환
    doc_info_export_result_json = json.loads(doc_info_export_result.replace('json', '').replace("```", ''))

    # 파일 저장
    file_path = os.path.join(current_dir, "voice")
    file_name = saved_ocr_name
    file_form = "json"

    save_file(file_path, file_name, file_form, doc_info_export_result_json)