FROM python:3.9.13

WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Noto Sans 폰트 설치
RUN wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSans-hinted.zip \
    && unzip NotoSans-hinted.zip -d /usr/share/fonts \
    && fc-cache -f -v \
    && rm NotoSans-hinted.zip
    
COPY requirements.txt /app/requirements.txt
COPY ./app /app
COPY .env /app/.env

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]