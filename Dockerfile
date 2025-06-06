FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask twilio

EXPOSE 8000

CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=8000"]
