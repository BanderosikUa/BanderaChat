FROM python:3.11-alpine3.16

RUN mkdir app
WORKDIR /app

RUN apk add --no-cache \
    python3-dev \
    libpq \
    gcc g++ \
    cargo


ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000", "--reload-dir", "/app/src"]
