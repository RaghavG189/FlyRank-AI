from fastapi import APIRouter

router = APIRouter(tags=['Meta']) #Define router object

#GET endpoint that retrieves API Data
@router.get('/')
def describe():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


#GET endpoint that returns status
@router.get('/health')
def status():
    return {"status": "ok"}


@router.get('/public/info', status_code=200)
def public_info():

    return {"message": "Welcome stranger! This info is public."}

