from python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run","--host","127.0.0.1","--port","5000"]