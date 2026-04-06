FROM python:3.12-slim

RUN adduser --disabled-password --no-create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 8004

ENTRYPOINT ["./entrypoint.sh"]
