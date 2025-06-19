FROM python:3.10-slim

WORKDIR /app
COPY duplicator.py .

RUN pip install flask requests

CMD ["python", "duplicator.py"]
