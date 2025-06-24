FROM python:3.12-slim
WORKDIR /app
COPY stt_dev/backend_server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY stt_dev ./stt_dev
COPY stt_dev/run_server.sh /run_server.sh
RUN chmod +x /run_server.sh
ENV PYTHONPATH=/app
CMD ["/run_server.sh", "stt_dev.backend_server.server", "8000"]

