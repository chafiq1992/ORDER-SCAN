FROM python:3.12-slim
WORKDIR /app

# --------------- dependencies ---------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------- application code -----------
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
