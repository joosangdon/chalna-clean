# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from app.core.config import settings
from app.services.image_service import ImageService

app = FastAPI(title=settings.PROJECT_NAME)

@app.post("/check-blur")
async def check_blur_endpoint(file: UploadFile = File(...)):
    """단일 이미지 선명도 분석 및 블러 여부 판별 (입력값 검증 포함)"""
    contents = await file.read()
    
    # 1. 단일 파일 유효성 검증
    ImageService.validate_image_file(
        filename=file.filename,
        content_type=file.content_type,
        file_bytes=contents
    )
    
    # 2. 비즈니스 로직 실행 (함수명 및 인자 전달 순서 수정 완료!)
    result = ImageService.analyze_image(contents=contents, filename=file.filename)

    # 3. JSON 직렬화 불가 객체 제거 후 반환 (해결 코드 추가!)
    result.pop("_phash_obj", None)
    
    return result


@app.post("/group-photos")
async def group_photos_endpoint(files: list[UploadFile]): 
    """다중 이미지 그룹핑 및 Best Photo 추천 (파일 개수/포맷 검증 포함)"""
    # 1. 파일 개수 검증
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업로드된 파일이 없습니다."
        )
    if len(files) > settings.MAX_FILES_COUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"한 번에 최대 {settings.MAX_FILES_COUNT}장까지만 업로드할 수 있습니다. (요청: {len(files)}장)"
        )

    # 2. 각 파일별 유효성 검증 및 메모리 데이터 로드
    files_data = []
    for file in files:
        contents = await file.read()
        ImageService.validate_image_file(
            filename=file.filename,
            content_type=file.content_type,
            file_bytes=contents
        )
        files_data.append((file.filename, contents))

    # 3. 비즈니스 로직 실행
    result = ImageService.group_photos(files_data)
    return result