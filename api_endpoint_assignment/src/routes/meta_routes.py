from fastapi import APIRouter

router = APIRouter() #Define router object

#GET endpoint that retrieves API Data
@router.get('/')
async def describe():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


#GET endpoint that returns status
@router.get('/health')
async def status():
    return {"status": "ok"}