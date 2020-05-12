# Flask miniblog

Study project based on [this guide](https://habr.com/ru/post/346306/)

To run this app, please do the following:
- clone this repo
- cd to cloned folder
- make virtual environment
```
virtualenv -p python3 env
```
- activate virtual environment
```
source env/bin/activate
```
- install requirements
```
pip3 install -r requirements.txt
```
- set environment variables:
export SECRET_KEY=""
export DATABASE_URL=""
export MAIL_SERVER=""
export MAIL_PORT=""
export MAIL_USE_TLS=""
export MAIL_USERNAME=""
export MAIL_PASSWORD=""
export ELASTICSEARCH_URL=""
- set config environment variable
```
export APP_SETTINGS="config.DevelopmentConfig"
```
- run with the following command
```
./manage.py runserver
```
