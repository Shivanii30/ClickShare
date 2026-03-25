FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "clickShare.wsgi:application"]
