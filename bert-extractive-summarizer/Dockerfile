FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt \
    && pip3 install bert-extractive-summarizer torch

ENV FLASK_APP=app.py

EXPOSE 5001
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
