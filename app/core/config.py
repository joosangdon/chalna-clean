# app/core/config.py

class Settings:
    PROJECT_NAME: str = "ChalnaClean"
    BLUR_THRESHOLD: float = 100.0
    SIMILARITY_DISTANCE: int = 20
    
    # 4주차: 보안 및 입력값 검증 설정
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 파일당 최대 10MB
    MAX_FILES_COUNT: int = 10              # 1회 최대 업로드 10장
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".webp"}
    ALLOWED_MIME_TYPES: set = {"image/jpeg", "image/png", "image/webp"}

settings = Settings()