FROM python:3.12

WORKDIR /

RUN mkdir /saved_photos

COPY . .

ENV PYTHONPATH=/application

RUN pip install --no-cache-dir -r /application/production_requirements.txt
