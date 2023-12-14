import os
import json

def save_file(file_path, file_name, file_form, data):
    """
    파일을 저장하는 함수

    Parameters:
    - file_path (str): 파일이 저장될 디렉토리 경로
    - file_name (str): 파일의 이름
    - file_form (str): 파일의 형식 (예: "json", "txt", "csv" 등)
    - data: 저장할 데이터

    Returns:
    - saved_path (str): 저장된 파일의 전체 경로
    """
    try:
        # 파일 디렉토리가 없으면 생성
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # 파일 경로 및 이름 조합
        file_path = os.path.join(file_path, f"{file_name}.{file_form}")

        # 데이터를 파일에 쓰기
        with open(file_path, 'w') as file:
            if file_form.lower() == 'json':
                # JSON 형식으로 저장
                json.dump(data, file)
            else:
                # 다른 형식에 대한 처리를 추가할 수 있습니다.
                file.write(str(data))

        return file_path

    except Exception as e:
        return f"Error: {str(e)}"



