from fastapi import APIRouter, UploadFile, File
import uuid

router = APIRouter()


@router.post("/")
async def predict(file: UploadFile = File(...)):
    """
    이미지 파일을 업로드 받아서
    모프 예측 결과를 반환하는 API

    현재는 실제 모델 대신 더미 응답을 반환
    """
    _ = await file.read() # 파일 내용을 읽어오기. 실제로는 모델에 입력으로 사용할 수 있도록 처리
    # 나중에는 여기서:
    # 1. 이미지 전처리
    # 2. 모델 inference
    # 3. top-k 계산
    
    # 더미
    return {
        "request_id": str(uuid.uuid4()), # 고유한 요청 ID 생성
        "topk": [
            {"name": "Harlequin", "score": 0.42},
            {"name": "Flame", "score": 0.18},
            {"name": "Pinstripe", "score": 0.12},
        ],
        "unknown_score": 0.28,
    }