from fastapi import APIRouter
import requests

router = APIRouter()

@router.get('/ip')
async def get_ip():
    ip = requests.get('https://ipv4.ifconfig.me').text
    return {
        'ip': ip,
    } 