cd ..
poetry run alembic revision --autogenerate -m "auto"
poetry run alembic upgrade head