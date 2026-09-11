from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io

import qrcode
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models import HeritageSite, Scan, User, Role, Badge
from ..schemas import SiteCreate, SiteOut
from ..security import get_current_user, require_roles
router = APIRouter(prefix='/api/sites', tags=['Heritage Sites'])

@router.get('', response_model=list[SiteOut])
def list_sites(q: str | None=None, region: str | None=None, category: str | None=None, db: Session=Depends(get_db)):
    query = db.query(HeritageSite).filter(HeritageSite.is_published.is_(True))
    if q:
        query = query.filter(or_(HeritageSite.name.ilike(f'%{q}%'), HeritageSite.story.ilike(f'%{q}%')))
    if region:
        query = query.filter(HeritageSite.region == region)
    if category:
        query = query.filter(HeritageSite.category == category)
    return query.order_by(HeritageSite.name).all()

@router.get('/{site_id}', response_model=SiteOut)
def get_site(site_id: int, db: Session=Depends(get_db)):
    site = db.get(HeritageSite, site_id)
    if not site or not site.is_published:
        raise HTTPException(404, 'Heritage site not found')
    return site

@router.post('', response_model=SiteOut, status_code=201)
def create_site(payload: SiteCreate, db: Session=Depends(get_db), _: User=Depends(require_roles(Role.admin, Role.superuser))):
    site = HeritageSite(**payload.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site

@router.put('/{site_id}', response_model=SiteOut)
def update_site(site_id: int, payload: SiteCreate, db: Session=Depends(get_db), _: User=Depends(require_roles(Role.admin, Role.superuser))):
    site = db.get(HeritageSite, site_id)
    if not site:
        raise HTTPException(404, 'Heritage site not found')
    for k, v in payload.model_dump().items():
        setattr(site, k, v)
    db.commit()
    db.refresh(site)
    return site

@router.post('/{site_id}/scan')
def scan_site(site_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    site = db.get(HeritageSite, site_id)
    if not site:
        raise HTTPException(404, 'Heritage site not found')
    db.add(Scan(user_id=user.id, site_id=site.id))
    passport = user.passport
    passport.points += 10
    if passport.points >= 50 and (not db.query(Badge).filter(Badge.user_id == user.id, Badge.name == 'Heritage Explorer').first()):
        db.add(Badge(user_id=user.id, name='Heritage Explorer', description='Completed five heritage interactions.'))
    db.commit()
    return {'message': 'Experience recorded', 'points': passport.points}

@router.get('/{site_id}/qr')
def qr_image(site_id: int, db: Session=Depends(get_db)):
    site = db.get(HeritageSite, site_id)
    if not site:
        raise HTTPException(404, 'Heritage site not found')
    img = qrcode.make(f'/experience/{site.qr_code}')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')
