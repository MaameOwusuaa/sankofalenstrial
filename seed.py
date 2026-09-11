from app.database import SessionLocal
from app.models import User, Role, Passport, HeritageSite
from app.security import hash_password
sites = [dict(name='Cape Coast Castle', region='Central Region', category='Historical Landmark', short_description='A major coastal heritage site carrying stories of Ghana, the Atlantic world and the diaspora.', story="Cape Coast Castle is one of Ghana's best-known historic coastal sites. Its spaces and collections can be used to explore the histories of the Atlantic trade, colonial rule, resistance, memory and diaspora connections. Replace this sample narrative with institutionally verified content before production.", latitude=5.1053, longitude=-1.2466, qr_code='SL-CC-001', image_url='https://images.unsplash.com/photo-1599708153386-62f8c7a9d3b2?auto=format&fit=crop&w=1200&q=80'), dict(name='Kwame Nkrumah Memorial Park', region='Greater Accra', category='National Heritage', short_description="A landmark for learning about Ghana's independence movement and national memory.", story="The memorial site provides an opportunity to explore Ghana's independence story, the Pan-African vision and the life and legacy of Kwame Nkrumah. Production content should be reviewed against authoritative sources.", latitude=5.5482, longitude=-0.1995, qr_code='SL-KN-002', image_url='https://images.unsplash.com/photo-1609946860441-a51ffcf8a6b1?auto=format&fit=crop&w=1200&q=80'), dict(name='Larabanga Mosque', region='Savannah Region', category='Architecture & Culture', short_description='An iconic earthen architectural landmark in northern Ghana.', story='Larabanga Mosque is widely recognized for its distinctive Sudanic-style earthen architecture and cultural importance. This sample record is designed to demonstrate the SankofaLens experience and should be replaced with verified community-approved content.', latitude=9.0928, longitude=-1.6945, qr_code='SL-LB-003', image_url='https://images.unsplash.com/photo-1539650116574-75c0c6d73f6e?auto=format&fit=crop&w=1200&q=80')]

def main():
    db = SessionLocal()
    if not db.query(User).filter(User.email == 'user@sankofalens.local').first():
        for email, role in [('user@sankofalens.local', Role.user), ('admin@sankofalens.local', Role.admin), ('superuser@sankofalens.local', Role.superuser)]:
            u = User(first_name=role.value.title(), last_name='Demo', email=email, hashed_password=hash_password('ChangeMe123!'), role=role)
            db.add(u)
            db.flush()
            db.add(Passport(user_id=u.id))
    if db.query(HeritageSite).count() == 0:
        for s in sites:
            db.add(HeritageSite(**s))
    db.commit()
    db.close()
    print('Seed complete')
if __name__ == '__main__':
    main()
