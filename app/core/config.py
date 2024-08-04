from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков QRKot'
    description: str = 'Описание из класса-конфига'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    class Config:
        env_file = '/Users/nikolai/Desktop/Dev/cat_charity_fund/.env'


settings = Settings()
