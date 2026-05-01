FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements /app/requirements
RUN pip install --no-cache-dir -r /app/requirements/base.txt

COPY backend/ /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
