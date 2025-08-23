FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

RUN chmod +x init-scripts/run-init.sh

EXPOSE 8002

ENTRYPOINT ["init-scripts/run-init.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--log-level", "info"]