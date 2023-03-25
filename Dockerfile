from python:3-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD [ "flask", "run","--host","127.0.0.1","--port","5000"]