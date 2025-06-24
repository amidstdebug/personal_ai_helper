FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY stt_dev ./stt_dev

ENV PYTHONPATH=/app

CMD ["python"]
