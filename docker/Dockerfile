FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R nobody:nogroup /app && \
    chmod -R 755 /app

USER nobody

ENV FLASK_APP=wsgi.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ping || exit 1

CMD ["gunicorn", "--config", "app/config/gunicorn.py", "wsgi:app"] 