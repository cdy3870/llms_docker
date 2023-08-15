FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY mapping.pkl ./mapping.pkl

RUN pip install --no-cache-dir -r requirements.txt

COPY fast_api_test.py ./

CMD ["uvicorn", "fast_api_test:app", "--host", "0.0.0.0", "--port", "80"]
