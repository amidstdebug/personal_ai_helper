FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY stt_dev ./stt_dev
COPY stt_dev/run_server.sh /run_server.sh
RUN chmod +x /run_server.sh

ENV PYTHONPATH=/app

CMD ["python"]
