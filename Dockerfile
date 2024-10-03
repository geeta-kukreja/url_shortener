FROM python:alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
# Run server.py when the container launches
# Run uvicorn server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]