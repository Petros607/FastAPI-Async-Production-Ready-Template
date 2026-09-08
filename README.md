# TMS
Transportation Management System

uvicorn app.main:app --reload

alembic revision --autogenerate -m "Initial migration"

flake8 .

