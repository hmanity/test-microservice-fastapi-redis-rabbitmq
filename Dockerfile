FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app