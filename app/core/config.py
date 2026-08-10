# app/core/config.py

class Settings:
    PROJECT_NAME: str = "찰나정리 (ChalnaClean) API"
    VERSION: str = "0.1.0"
    
    # 이미지 분석 관련 설정
    BLUR_THRESHOLD: float = 100.0  # 선명도 점수가 100 미만이면 '흐림'으로 판단
    SIMILARITY_DISTANCE: int = 5   # Hamming Distance가 5 이하이면 '중복/유사'로 판단

settings = Settings()