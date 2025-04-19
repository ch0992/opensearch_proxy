# app/main.py
# 이 파일은 프로젝트의 FastAPI 애플리케이션 엔트리포인트입니다.
# 전체 서비스의 라우팅, 미들웨어, 문서화, CORS 등 핵심 설정을 담당합니다.

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

# API 라우터와 환경설정 임포트
from app.api.v1.api import api_router
from app.core.config import settings

# FastAPI 앱 인스턴스 생성
# 프로젝트명과 OpenAPI 문서 경로를 환경설정에서 받아옵니다.
app = FastAPI(
    title="FileDepot",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

from app.core.middleware import log_requests
app.middleware('http')(log_requests)

from app.core.exception_handlers import global_exception_handler, http_exception_handler
from fastapi import HTTPException
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="FileDepot API 문서",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS 미들웨어 설정
# 다양한 프론트엔드/외부 서비스가 API를 호출할 수 있도록 허용합니다.
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 버전별 API 라우터 등록
# 실제 엔드포인트는 api_router에서 정의하며, 버전 prefix로 관리합니다.
app.include_router(api_router, prefix=settings.API_V1_STR)

# 루트 엔드포인트: 서비스 상태 및 문서 링크 제공
@app.get("/")
def root():
    return {
        "message": "Welcome to FileDepot",
        "documentation": "/docs",
        "redoc": "/redoc"
    }
