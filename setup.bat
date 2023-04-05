@echo off
docker build -t text-app .
docker run --name text-application-prototype -d -p 5000:5000 text-app