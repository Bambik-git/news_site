FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYCODE = 1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ['python', 'manage.py', 'runserver']