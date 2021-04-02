FROM python:3.7

RUN apt-get update ;

COPY . /app
WORKDIR /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "cli.py"]