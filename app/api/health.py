from fastapi import APIRouter

router = APIRouter()

@router.head("")
@router.get("")
def health():
    return {"status": "healthy"}

