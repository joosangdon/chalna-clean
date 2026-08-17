# app/main.py

from fastapi import FastAPI, File, UploadFile as UF
from typing import Annotated, List
from pydantic import WithJsonSchema
from app.core.config import settings
from app.services.image_service import ImageService

# Swagger UI에서 다중 파일 선택 버튼이 정상 렌더링되도록 바이너리 스키마 지정
UploadFile = Annotated[UF, WithJsonSchema({"type": "string", "format": "binary"})]

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
async def analyze_single_photo(file: UF = File(...)):
    contents = await file.read()
    analysis_result = ImageService.analyze_image(contents, file.filename)
    analysis_result.pop("_phash_obj", None)
    return analysis_result

@app.post("/group-photos")
async def group_photos_endpoint(files: List[UploadFile] = File(...)):
    """여러 장의 사진을 업로드받아 유사 사진 그룹 및 Best Shot을 반환합니다."""
    files_data = []
    for file in files:
        contents = await file.read()
        files_data.append((file.filename, contents))
    
    result = ImageService.group_photos(files_data)
    return result