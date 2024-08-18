FROM python:3.11-slim-bullseye 

RUN apt-get update && apt-get install -y dnsutils telnet  net-tools procps wget iputils-ping redis-tools curl 
WORKDIR /app

COPY app/ /app
COPY requirements.txt /app
COPY kubeconfig /root/.kube/config
COPY certs/  /root/.kube/certs

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]

