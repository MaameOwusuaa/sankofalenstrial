from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Role, HeritageSite, Scan, AuditLog
from ..security import require_roles
router = APIRouter(prefix='/api/admin', tags=['Administration'])

@router.get('/dashboard')
def dashboard(db: Session=Depends(get_db), _: User=Depends(require_roles(Role.admin, Role.superuser))):
    return {'users': db.query(User).count(), 'sites': db.query(HeritageSite).count(), 'scans': db.query(Scan).count()}

@router.get('/users')
def users(db: Session=Depends(get_db), _: User=Depends(require_roles(Role.superuser))):
    return [{'id': u.id, 'name': f'{u.first_name} {u.last_name}', 'email': u.email, 'role': u.role.value, 'active': u.is_active} for u in db.query(User).order_by(User.id.desc()).all()]

@router.patch('/users/{user_id}/role')
def change_role(user_id: int, role: Role, db: Session=Depends(get_db), actor: User=Depends(require_roles(Role.superuser))):
    user = db.get(User, user_id)
    if not user:
        return {'error': 'User not found'}
    user.role = role
    db.add(AuditLog(user_id=actor.id, action='change_role', details=f'user={user_id}, role={role.value}'))
    db.commit()
    return {'message': 'Role updated'}
