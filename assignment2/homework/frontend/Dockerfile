FROM python:3.11-slim

WORKDIR /app

RUN pip install flask requests

COPY app.py /app/app.py
COPY templates /app/templates

EXPOSE 5000

CMD ["python", "app.py"]