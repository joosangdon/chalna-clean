import requests

# 서버 주소
url = "http://127.0.0.1:8000/group-photos"

# 바탕화면에 있는 테스트 이미지 2장 준비
files = [
    ('files', ('test1.jpg', open('test1.jpg', 'rb'), 'image/jpeg')),
    ('files', ('test2.jpg', open('test2.jpg', 'rb'), 'image/jpeg'))
]

print("서버로 다중 파일 분석을 요청합니다...")
response = requests.post(url, files=files)

print(f"상태 코드: {response.status_code}")
print("응답 결과:")
print(response.json())