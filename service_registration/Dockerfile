FROM python:latest

WORKDIR /usr/local/bin

RUN pip install docker
RUN pip install mysql-connector-python
RUN pip install pyyaml

COPY . .

CMD ["python", "main.py"]