@echo off

cd web-app
docker build -t text-app .

cd ..
cd summarization-models
docker build -t summarizers .

docker network create --driver bridge webapp_simplification
docker run --name text-application-prototype --network webapp_simplification -d -p 5000:5000 text-app 
docker run --name summarization-models --network webapp_simplification -d -p 5001:5001 summarizers

cd ..