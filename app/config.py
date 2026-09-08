# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Указываем переменные и их типы
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"  # Значение по умолчанию
    SECRET_KEY: str
    
    # Настройки для Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",            # Читать из файла .env
        env_file_encoding="utf-8",
        extra="ignore"              # Игнорировать лишние переменные в .env
    )

# Создаем синглтон настроек для импорта в другие файлы
settings = Settings()
