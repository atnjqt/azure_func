## Building a docker flask app (LOCAL DEV)

Sample notebook here for testing --> [flask-app-testing.ipynb](./flask-app-testing.ipynb)

__________


- My dev testing looked at Python Flask app, this is ok, really we want a serverless deployment option but this was really helpful to conceptualize the project


```
docker build --tag flask-bcra-app .
docker run --publish 5000:5000 -d flask-bcra-app

../deploy.sh
```
