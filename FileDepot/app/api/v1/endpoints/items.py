"""
endpoints/items.py
- Item 도메인에 대한 FastAPI 라우터/엔드포인트 정의
- 실제 서비스에서는 domain/item/models, service만 import해서 사용
"""

from fastapi import APIRouter, HTTPException, Path
from app.schemas.item import ItemCreateRequest, ItemUpdateRequest
from app.domain.item.models import Item
from app.domain.item.service import create_item, read_item, update_item, delete_item

router = APIRouter()

@router.post(
    "/items/",
    response_model=Item,
    tags=["example_items"],
    summary="아이템 생성",
    description="새로운 아이템 등록 예제 API"
)
def create(request: ItemCreateRequest):
    """
    새로운 아이템 등록 예제 API
    ---
    #### 파라미터 설명
    - name: 아이템 이름 (예: 샘플 아이템)
    - description: 아이템 설명 (예: 테스트 용도)
    """
    import uuid
    item_id = uuid.uuid4().int >> 96  # 32비트 int
    item = Item(id=item_id, name=request.name, description=request.description)
    print(f"[아이템 생성 요청] name={request.name}, description={request.description}")
    try:
        result = create_item(item)
        print(f"[아이템 생성 결과] {result}")
        return result
    except ValueError as e:
        print(f"[아이템 생성 오류] {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/items/{item_id}",
    response_model=Item,
    tags=["example_items"],
    summary="아이템 조회 (Read)",
    description="특정 아이템 정보 읽기 예제 API"
)
def read(item_id: int):
    print(f"[아이템 조회 요청] item_id={item_id}")
    try:
        result = read_item(item_id)
        print(f"[아이템 조회 결과] {result}")
        return result
    except ValueError as e:
        print(f"[아이템 조회 오류] item_id={item_id}, {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put(
    "/items/{item_id}",
    response_model=Item,
    tags=["example_items"],
    summary="아이템 수정",
    description="아이템 정보 수정 예제 API"
)
def update(
    request: ItemUpdateRequest,
    item_id: int = Path(..., description="수정할 아이템의 고유 ID (예: 1)")
):
    print(f"[아이템 수정 요청] item_id={item_id}, request={request}")
    item = Item(id=item_id, name=request.name, description=request.description)
    try:
        result = update_item(item_id, item)
        print(f"[아이템 수정 결과] {result}")
        return result
    except ValueError as e:
        print(f"[아이템 수정 오류] item_id={item_id}, {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete(
    "/items/{item_id}",
    tags=["example_items"],
    summary="아이템 삭제",
    description="아이템 정보 삭제 예제 API"
)
def delete(
    item_id: int = Path(..., description="삭제할 아이템 고유 ID (예: 1)")
):
    print(f"[아이템 삭제 요청] item_id={item_id}")
    try:
        result = delete_item(item_id)
        print(f"[아이템 삭제 결과] {result}")
        return result
    except ValueError as e:
        print(f"[아이템 삭제 오류] item_id={item_id}, {e}")
        raise HTTPException(status_code=404, detail=str(e))
