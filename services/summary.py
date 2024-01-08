import os
from services.vertexai_text_command import text_generation
import json
from flask import current_app

current_dir = os.path.dirname(os.path.abspath(__file__))
voice_dir = os.path.join(current_dir, 'voice')

"""
텍스트 요약을 위해 
text(stt로 말이 변환된 것) 입력 -> text_generation(command:"language_code에 맞게 요약해라") -> 파일 저장하는 코드

* text_generation() : vertex ai에게 command를 주고 답변을 받음

"""
def text_summarization(
        filename: str,
        temperature: float,
        location: str,
        text: str,
        language_code : str
) -> str:
    """Summarization Example with a Large Language Model"""

    # 1. 각 언어에 따라 명령 다르게 진행 (내용은 같으나, 언어만 다름) : 단순 요약
    if language_code == "en-us":
        command = """You should be an assistant nurse so that the doctor can see the patient's questionnaire easily. The following is what the patient asks. Please summarize the article briefly about the patient's symptoms and write it in one paragraph. Write "<h3><b>Summary</b></h3>" to begin with. If the sentence entered is too short, just organize it and show it to me.: """
    elif language_code == "ja-jp":
        command = """医師が患者の問診内容を見やすいように、あなたが補助看護師になってくれます。 次の内容は患者が問診する内容です。 患者の症状と関連して文章を簡単に要約し、一つの段落で作成してください。 始まりは"<h3><b>要約</b></h3>と書いてください。もし入力された文章が短すぎるなら、そのまま整理して見せて。: """
    elif language_code == "ko-kr":
        command = """의사가 환자의 문진 내용을 보기 편하도록 너가 보조간호사가 되어줘. 다음 내용은 환자가 문진하는 내용이야. 환자의 증상과 관련해서 글을 간략하게 요약하고, 하나의 문단으로 작성해줘. 시작은 "<h3><b>요약</b></h3>"이라고 적어줘. 만약 입력된 문장이 너무 짧다면 그냥 정리해서 보여줘.: """  
    # 요약
    summary = text_generation(temperature, location, text, command)
    print(summary)
    current_app.logger.info("[text_summarization] : 요약 완료")

    # 2. 각 언어에 따라 명령 다르게 진행 (내용은 같으나, 언어만 다름) : 질병 예측
    if language_code == "en-us":
        command = """You become an assistant nurse so that the doctor can see the patient's questionnaire easily. The following is about the patient's questionnaire. If the patient's symptoms can predict the disease, tell me only three suspected diseases and why. Please write "<h3><b>Top 3 Suspected Diseases Based on Patient Symptoms</b></h3>". Organize the things that can be organized into a list using <ol><li> or <ul><li> among the html tags, and write down the <b> tag or <br> tag so that the user can easily and neatly organize them.: """
    elif language_code == "ja-jp":
        command = """医師が患者の問診内容を見やすいように、あなたが補助看護師になってくれ。 次の内容は患者が問診する内容だよ。 患者の症状が病気を予測できれば、疑いのある病気3つとその理由についてだけ言ってくれ。 始まりは「<h3><b>患者の症状に基づくトップ3疑わしい疾患</b></h3>」と書いてくれ。 リストにまとめられるものはhtmlタグの中で<ol><li>あるいは<ul><li>を利用して整理し、ユーザーが見やすくきれいに整理できるように<b>タグや<br>タグも書いてね : """
    elif language_code == "ko-kr":
        command = """의사가 환자의 문진 내용을 보기 편하도록 너가 보조간호사가 되어줘. 다음 내용은 환자가 문진하는 내용이야. 환자의 증상이 질병을 예측할 수 있으면 의심 질병 3개와 그 이유에 대해서만 말해줘. 시작은 "<h3><b>환자 증상 기반 Top 3 의심 질환</b></h3>"이라고 적어줘. 리스트로 정리될 만한 것들은 html 태그 중에서 <ol><li> 혹은 <ul><li> 이용해서 정리해주고, 사용자가 보기 편하고 깔끔하게 정리할 수 있도록 <b>태그나 <br> 태그도 써줘 : """  
    # 질병 예측
    summary_predict_disease = text_generation(temperature, location, text, command)
    print(summary_predict_disease)
    current_app.logger.info("[text_summarization] : 질병 예측 완료")

    # 3. 각 언어에 따라 명령 다르게 진행 (내용은 같으나, 언어만 다름) : 추가 질문
    if language_code == "en-us":
        command = """Make it easy for the doctor to review the patient's medical history by assisting as a nurse. The following is what the patient is documenting. Provide 10 additional questions that can help predict illnesses based on the symptoms. Start with "<h3><b>Top 10 Additional Questions for a More Definitive Diagnosis</b></h3>". Use HTML tags like <ol><li> or <ul><li> to organize the list neatly. Make it user-friendly and well-organized.: """
    elif language_code == "ja-jp":
        command = """医師が患者の問診内容を見やすくするために、あなたは看護助手としてお手伝いしてください。以下は患者が問診する内容です。患者の症状から病気を予測できるように、追加できる質問についてだけ10個教えてください。始めは「<h3><b>より確定的な診断のためのトップ10追加質問</b></h3>」と書いてください。整理されるものは<ol><li>または<ul><li>のHTMLタグを使用して整理し、ユーザーが見やすくきれいにまとめて書いてください。: """
    elif language_code == "ko-kr":
        command = """의사가 환자의 문진 내용을 보기 편하도록 너가 보조간호사가 되어줘. 다음 내용은 환자가 문진하는 내용이야. 환자의 증상이 질병을 예측할 수 있도록 추가로 할 수 있는 질문에 대해서만 10개 말해줘. 시작은 "<h3><b>환자 응답을 확장하는데 도움되는 10가지 질문</b></h3>"이라고 적어줘. 리스트로 정리될 만한 것들은 html 태그 중에서 <ol><li> 혹은 <ul><li> 이용해서 정리해주고, 사용자가 보기 편하고 깔끔하게 정리해서 써줘. : """  
    # 추가 질문
    summary_add_questions = text_generation(temperature, location, text, command)
    print(summary_add_questions)
    current_app.logger.info("[text_summarization] : 추가 질문 생성 완료")
    
    # 각 질문별 답변 따로 저장 (html 태그 포함되어서 저장되어 있음)
    final_output = {
    "summary": summary + "<br><br>" + summary_predict_disease + "<br><br>" + summary_add_questions,
    "summary_predict_disease" : summary_predict_disease,
    "summary_add_questions" : summary_add_questions,
    }

    with open(os.path.join(voice_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False)

 