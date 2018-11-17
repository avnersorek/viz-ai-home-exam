FROM python:3-slim

RUN apt-get update
# We need gcc to install Pillow
RUN apt-get -y install gcc

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "src/app.py" ]
