FROM ubuntu:latest

# SET FOR SILENT R INSTALL
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL PYTHON AND R FOR UBUNTU
RUN apt-get update && apt-get install -y build-essential r-base python3 python3-pip python3-setuptools python3-dev

WORKDIR /app

# PYTHON DEPENDENCIES
RUN pip3 install flask pandas rpy2

# R DEPENDENCIES
RUN Rscript -e "install.packages('BCRA')"

COPY . /app
EXPOSE 5000

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "app.py"]
