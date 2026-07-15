FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

COPY merge-sort.py .

EXPOSE 8080

CMD ["python", "merge-sort.py"]
