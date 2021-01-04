
FROM python:3.5

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends libatlas-base-dev gfortran nginx supervisor

RUN pip3 install uwsgi

COPY ./requirements.txt /src/requirements.txt

ENV PYTHONUNBUFFERED=0
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN useradd --no-create-home nginx 
RUN usermod -G root nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY /server-conf/nginx.conf /etc/nginx/
COPY /server-conf/flask-site-nginx.conf /etc/nginx/conf.d/
COPY /server-conf/uwsgi.ini /etc/uwsgi/
COPY /server-conf/supervisord.conf /etc/



COPY . /src
WORKDIR /src

# ENTRYPOINT [ "python3" ]

# CMD [ "calculator.py" ]
CMD ["/usr/bin/supervisord"]