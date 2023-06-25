
FROM python:3.11-slim-bookworm

# set timezone
RUN echo "Etc/UTC" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

# set variables
ENV DJANGO_DEBUG 0

# install deps
RUN apt-get update && apt-get install nginx vim git nano pkg-config default-libmysqlclient-dev build-essential -y
# pkg-config: required for a Python mysql package
# default-libmysqlclient-dev: required for a Python mysql package
# build-essential: good to have, maybe helpful for Python mysql

# configure nginx
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/supernova
COPY requirements.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY supernova /opt/app/supernova/
WORKDIR /opt/app
RUN pip install wheel
RUN pip install -r requirements.txt
# --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]

