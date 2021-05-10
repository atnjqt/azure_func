#! /bin/sh

cd app

docker build --tag flask-bcra-app .

docker run --publish 5000:5000 -d flask-bcra-app