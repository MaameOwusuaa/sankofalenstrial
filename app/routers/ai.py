from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import HeritageSite, User
from ..schemas import AskRequest
from ..security import get_current_user
router = APIRouter(prefix='/api/guide', tags=['Naa AI Heritage Guide'])

@router.post('/ask')
def ask_naa(payload: AskRequest, db: Session=Depends(get_db), _: User=Depends(get_current_user)):
    site = db.get(HeritageSite, payload.site_id) if payload.site_id else None
    if not settings.openai_api_key:
        context = site.name if site else 'Ghanaian heritage'
        return {'answer': f'Naa is ready to guide you about {context}. Connect OPENAI_API_KEY and OPENAI_MODEL in .env to enable the live AI integration. For production, ground answers in verified cultural sources.'}
    return {'answer': 'Naa AI integration is configured as a backend boundary. Implement your approved provider call here, using verified heritage context before sending a response.'}
