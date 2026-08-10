from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import imagehash
from PIL import Image
import io

app = FastAPI(
    title="찰나정리 (ChalnaClean) API",
    description="개인정보 보호 중심의 AI 중복/저화질 사진 정리 백엔드 API",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "찰나정리(ChalnaClean) API 서버가 정상 동작 중입니다!"
    }

# 📸 단일 사진 분석 API (In-Memory 기반 처리)
@app.post("/analyze-single")
async def analyze_single_photo(file: UploadFile = File(...)):
    # 1. 업로드된 파일의 바이너리 데이터 읽기 (디스크에 저장하지 않고 메모리 상에서 처리)
    contents = await file.read()
    
    # 2. OpenCV용 이미지 변환 (Bytes -> numpy array -> cv2 image)
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # 3. 선명도(Laplacian Variance) 계산
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    
    # 4. pHash 계산 (PIL Image)
    pil_image = Image.open(io.BytesIO(contents))
    phash_val = str(imagehash.phash(pil_image))
    
    # 5. 결과 반환 (서버에 사진을 남기지 않고 연산 결과만 JSON 전달)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "focus_score": round(blur_score, 2),
        "phash": phash_val,
        "is_blurry": blur_score < 100.0  # 임계값 예시 (100 미만이면 흐림)
    }