from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict 

app = FastAPI()

#  React 프론트엔드에서 API 호출 시 CORS 문제를 방지하기 위해 CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 어떤 곳에서 오는 요청을 허용할지 / 개발 단계에서는 "*"로 모든 도메인을 허용 실제 배포시엔 특정 주소만 허용
    allow_credentials=True,     # 쿠키나 인증 정보를 포함할지
    allow_methods=["*"],         # GET, POST 등 어떤 메소드를 허용할지
    allow_headers=["*"],         # 어떤 HTTP 헤더를 허용할지
)

# predict 관련 API를 /predict 경로로 라우팅
app.include_router(predict.router, prefix="/predict")

@app.get("/")
def root():
    return {"message": "cre-morph backend running"}

@app.get("/health")
def health():
    # 서버가 정상 동작하는지 확인하는 엔드포인트
    return {"status": "ok"}