FROM python:3.8-slim-buster

WORKDIR /app
ENV PYTHONPATH=/app


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest httpx pytest-asyncio

# Commande pour exécuter les tests
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




