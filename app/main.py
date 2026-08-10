# app/main.py

from fastapi import FastAPI, File, UploadFile
from app.core.config import settings
from app.services.image_service import ImageService

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="개인정보 보호 중심의 AI 중복/저화질 사진 정리 백엔드 API",
    version=settings.VERSION
)

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": f"{settings.PROJECT_NAME} 서버가 정상 동작 중입니다!"
    }

@app.post("/analyze-single")
async def analyze_single_photo(file: UploadFile = File(...)):
    # 1. 파일 데이터 읽기
    contents = await file.read()
    
    # 2. 이미지 서비스로 연산 위임 (Clean Architecture)
    analysis_result = ImageService.analyze_image(contents)
    
    # 3. 최종 결과 조합 반환
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        **analysis_result
    }