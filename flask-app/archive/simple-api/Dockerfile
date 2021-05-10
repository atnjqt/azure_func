# Etienne P Jacquot - 05/09/2021

FROM python:3.8-slim as builder

#RUN pip install --user fastapi uvicorn boto3 flask
RUN pip install --user flask pandas

COPY . /src



FROM python:3.8-slim as app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /src .

ENV PATH=/root/.local:$PATH
EXPOSE 5000

#CMD ["python3", "app.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
