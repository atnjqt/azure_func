# syntax=docker/dockerfile:1

# Etienne P Jacquot 05/09/2021
# Multistaged build from AWS example

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install --user flask

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

#ENV PATH=/root/.local:$PATH
#EXPOSE 5000

#CMD ["python3", "api.py"]
#CMD ["python3", "app.py"]
