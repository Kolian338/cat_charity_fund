import uvicorn
from fastapi import FastAPI

# Импортируем роутер.
from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

# Подключаем роутер.
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
