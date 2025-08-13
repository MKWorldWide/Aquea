
FROM python:3.12-slim
WORKDIR /app

# Install gateway deps
COPY services/gateway/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install local adapter as editable
COPY libs/nesshash-adapter /tmp/nesshash-adapter
RUN pip install -e /tmp/nesshash-adapter

# Copy gateway source
COPY services/gateway/ .

ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
