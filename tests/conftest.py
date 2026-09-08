# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, get_db

# Используем SQLite в памяти для тестов (быстро и изолированно)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="function")
async def db_session():
    """Фикстура для создания чистой БД и сессии на каждый тест"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Создаем таблицы в тестовой БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    TestingSessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with TestingSessionLocal() as session:
        yield session
        
    # Удаляем таблицы после завершения теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def client(db_session):
    """Фикстура асинхронного клиента, подменяющая зависимость базы данных в FastAPI"""
    async def override_get_db():
        yield db_session

    # Подменяем зависимость get_db в приложении на нашу тестовую
    app.dependency_overrides[get_db] = override_get_db
    
    # Для новых версий httpx передаем транспорт
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
    # Очищаем подмены после теста
    app.dependency_overrides.clear()
