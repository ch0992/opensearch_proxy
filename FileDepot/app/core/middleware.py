import time
import asyncio
from fastapi import Request

async def log_requests(request: Request, call_next):

    start_time = time.time()
    try:
        body = await request.body()
        body_str = body.decode('utf-8') if body else ''
    except Exception:
        body = b''
        body_str = '[body 읽기 실패]'
    print(f"[요청] {request.method} {request.url.path} | Body: {body_str}")

    # body 복원: downstream에서 또 읽을 수 있도록 패치
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}
    request._receive = receive

    response = await call_next(request)
    duration = time.time() - start_time
    print(f"[응답] {request.method} {request.url.path} | Status: {response.status_code} | 처리시간: {duration:.2f}s")
    return response
