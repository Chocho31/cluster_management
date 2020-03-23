FROM python:latest

WORKDIR /usr/local/bin

RUN pip install docker
RUN pip install apscheduler
RUN pip install influxdb
RUN pip install pyyaml

COPY . .

CMD ["python", "main.py"]