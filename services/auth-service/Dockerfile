FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x init-scripts/run-init.sh

ENV PYTHONPATH=/app

EXPOSE 8001

ENTRYPOINT ["init-scripts/run-init.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]