from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, Badge, Scan, HeritageSite
from ..security import get_current_user
router = APIRouter(prefix='/api/passport', tags=['Cultural Passport'])

@router.get('')
def passport(db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    badges = db.query(Badge).filter(Badge.user_id == user.id).order_by(Badge.awarded_at.desc()).all()
    
    # Get all scans for this user
    scans = db.query(Scan).filter(Scan.user_id == user.id).order_by(Scan.scanned_at.desc()).all()
    
    # Get unique sites visited
    unique_sites = db.query(func.count(func.distinct(Scan.site_id))).filter(Scan.user_id == user.id).scalar() or 0
    
    # Get recent scans with site info
    recent_scans = db.query(Scan, HeritageSite).join(HeritageSite, Scan.site_id == HeritageSite.id).filter(Scan.user_id == user.id).order_by(Scan.scanned_at.desc()).limit(5).all()
    
    # Get all scans with site info
    all_scans = db.query(Scan, HeritageSite).join(HeritageSite, Scan.site_id == HeritageSite.id).filter(Scan.user_id == user.id).order_by(Scan.scanned_at.desc()).all()
    
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'points': user.passport.points if user.passport else 0,
        'total_badges': len(badges),
        'sites_visited': unique_sites,
        'badges': [{'name': b.name, 'description': b.description, 'awarded_at': b.awarded_at.isoformat()} for b in badges],
        'recent_stamps': [
            {
                'site_name': site.name,
                'region': site.region,
                'category': site.category,
                'image_url': site.image_url,
                'scanned_at': scan.scanned_at.isoformat()
            }
            for scan, site in recent_scans
        ],
        'all_places': [
            {
                'site_id': site.id,
                'site_name': site.name,
                'region': site.region,
                'category': site.category,
                'image_url': site.image_url,
                'short_description': site.short_description,
                'scanned_at': scan.scanned_at.isoformat()
            }
            for scan, site in all_scans
        ]
    }
