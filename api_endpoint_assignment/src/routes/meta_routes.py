from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def describe():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@router.get('/health')
async def status():
    return {"status": "ok"}