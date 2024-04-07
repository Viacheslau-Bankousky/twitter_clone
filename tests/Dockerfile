FROM python:3.12

WORKDIR /

RUN mkdir /saved_photos

COPY ./application /application

COPY ./tests /tests

COPY ../README.md /

COPY ../twitter_clone_logo.jpg /

RUN pip install --no-cache-dir -r tests/testing_requirements.txt
