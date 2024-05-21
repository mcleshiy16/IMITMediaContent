FROM python:3.12-alpine

WORKDIR .

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:practice_app", "--host", "0.0.0.0", "--port", "8000"]