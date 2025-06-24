FROM python:3.12-slim
WORKDIR /app
COPY stt_dev/telegram_server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY stt_dev ./stt_dev
ENV PYTHONPATH=/app
CMD ["python", "-m", "stt_dev.telegram_server.server"]

