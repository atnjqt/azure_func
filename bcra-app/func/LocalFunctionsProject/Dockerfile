# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# SET FOR SILENT R INSTALL
ENV DEBIAN_FRONTEND=noninteractive

# R DEPENDENCIES
RUN apt update && \
    apt install -y r-base && \
    R -e "install.packages('BCRA', repos='http://cran.rstudio.com/')"

# PYTHON DEPENDENCIES
RUN pip3 install azure-functions pandas rpy2

COPY . /home/site/wwwroot