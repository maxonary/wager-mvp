from fastapi import APIRouter
import requests

router = APIRouter()

@router.get('/ip')
async def get_ip():
    ip = requests.get('https://curlmyip.org').text
    return {
        'ip': ip,
    } 