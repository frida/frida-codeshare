FROM python:3.9.19

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
