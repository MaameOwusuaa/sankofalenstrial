from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .config import settings
from .routers import auth, sites, passport, admin, ai
app = FastAPI(title=settings.app_name, version='1.0.0', description='Digital cultural heritage and tourism platform')
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(auth.router)
app.include_router(sites.router)
app.include_router(passport.router)
app.include_router(admin.router)
app.include_router(ai.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'SankofaLens'}

@app.get('/')
def root():
    return FileResponse('frontend/index.html')

@app.get('/{page}.html')
def page(page: str):
    return FileResponse(f'frontend/{page}.html')
