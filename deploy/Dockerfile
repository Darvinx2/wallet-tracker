FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN adduser --system --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["python", "-m", "src.main"]