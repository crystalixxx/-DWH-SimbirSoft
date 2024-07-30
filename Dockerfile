FROM python:3.12
WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .
