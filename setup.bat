@echo off


cd web-app
docker build -t text-app .

cd ..
cd bert-extractive-summarizer
docker build -t bert-ext-sum .

cd ..
cd local-abstractive-summarizer
docker build -t local-abstractive-sum .

docker network create --driver bridge webapp_simplification
docker run --name text-application-prototype --network webapp_simplification -d -p 5000:5000 text-app 
docker run --name bert-extract-sum --network webapp_simplification -p 5001:5001 bert-ext-sum 
docker run --name local-abstract-sum --network webapp_simplification -p 5002:5002 local-abstractive-sum

cd ..