from __future__ import annotations

import time
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.services.predictor import predict_stub


router = APIRouter(prefix="/api", tags=["predict"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 10 * 1024 * 1024 # 10MB


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    이미지 파일을 업로드 받아서
    모프 예측 결과를 반환하는 API

    현재는 실제 모델 대신 더미 응답을 반환
    """
    t0 = time.perf_counter()
    request_id = uuid.uuid4().hex[:12]

    if not file:
        raise HTTPException(status_code=400, detail="file is required")
    
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415, # 데이터 형식 불일치
            detail=f"Unsupported file type: {file.content_type}. "
                    f"Allowed: {sorted(ALLOWED_CONTENT_TYPES)}"
        )
    
    data = await file.read()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="empty file")
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail=f"file too large (max {MAX_BYTES}) bytes")
    
    # 스텁 예측
    result = predict_stub(data)

    latency_ms = int((time.perf_counter() - t0) * 1000)

    payload = {
        **result,
        "request_id": request_id,
        "latency_ms": latency_ms,
    }
    
    return JSONResponse(payload)

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