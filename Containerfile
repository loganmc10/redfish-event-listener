FROM registry.access.redhat.com/ubi9/python-39:latest

WORKDIR /app

COPY listener.py

ENTRYPOINT ["python3", "/app/listener.py"]
