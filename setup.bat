@echo off


cd web-app
docker build -t text-app .

cd ..
cd bert-extractive-summarizer
docker build -t bert-extractive-summarizer/bert-ext-sum .

docker network create --driver bridge webapp_simplification
docker run --name text-application-prototype --network webapp_simplification -d -p 5000:5000 text-app 
docker run --name bert-extract-sum --network webapp_simplification -p 5001:5001 bert-extractive-summarizer/bert-ext-sum 

cd ..