from fastapi import APIRouter

router = APIRouter(prefix="/dummy", tags=["dummy"])


@router.get("/")
def health_check():
    return {"status": "ok"}
