# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch.py process_one_video.py create_storage_account.py run_all.py config.py .

ENTRYPOINT ["python", "run_all.py"]
