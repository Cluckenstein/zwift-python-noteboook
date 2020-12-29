FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /src

ENTRYPOINT [ "python" ]

CMD [ "src/calculator.py" ]