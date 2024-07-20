FROM python:3.9.13

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY ./app /app
COPY .env /app/.env

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]