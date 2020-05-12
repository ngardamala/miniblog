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

Following environment variables should be set before starting the app:
- SECRET_KEY
- DATABASE_URL
- MAIL_SERVER
- MAIL_PORT
- MAIL_USE_TLS
- MAIL_USERNAME
- MAIL_PASSWORD
- ELASTICSEARCH_URL

Configuration is set wit
