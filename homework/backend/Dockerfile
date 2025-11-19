FROM python:3.11-slim

WORKDIR /app

RUN pip install flask

COPY app.py /app/app.py

EXPOSE 5001

CMD ["python", "app.py"]