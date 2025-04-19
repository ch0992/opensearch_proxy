from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

async def global_exception_handler(request: Request, exc: Exception):
    print(f"[예외 발생] {request.method} {request.url.path} | {repr(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부 오류가 발생했습니다."}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    print(f"[HTTP 예외] {request.method} {request.url.path} | {exc.status_code} | {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
