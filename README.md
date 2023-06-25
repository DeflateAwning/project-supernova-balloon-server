# project-supernova-balloon-server
 Server for the Project Supernova Helium Helium Balloon

## Deployment
* Tutorial: https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application#h-dockerizing-the-application

## Main Commands
```bash

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# set env DJANGO_DEBUG=True
export DJANGE_DEBUG=True
# TODO windows version
```

## Run MariaDB Server
```bash

docker pull docker pull mariadb:10.11 # maybe optional

docker run --name mariadb_supernova -e MYSQL_ROOT_PASSWORD=SOME_PASSWORD_HERE -p 3306:3306 -d docker.io/library/mariadb:10.11

```

## Build and Run Web App
```bash
docker build -t supernova .
docker run -d -p 8020:8020 --name supernova supernova
docker run -d -p 8020:8020 -e DJANGO_DEBUG=1 --name supernova supernova # debug mode
```

## Ports
* Django listens on `0.0.0.0:8010` (in `start-server.sh`)
* Nginx listens on `0.0.0.0:8020`, and forwards requests to `127.0.0.1:8010` (in `nginx.default`)
* Docker run command connects internal and external port `8020`
