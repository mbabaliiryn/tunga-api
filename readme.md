# Tunga API and Backend [![Build Status](https://travis-ci.org/tunga-io/tunga-api.svg?branch=develop)](https://travis-ci.org/tunga-io/tunga-api)
API and Backend for tunga.io

# Installation
1. run the following commands from project root (preferably in a virtualenv)
```
pip install -r requirements.txt
python manage.py migrate
python manage.py initial_tags
python manage.py initial_tunga_settings
python manage.py initial_tunga_integration_events
```

2. Install [Redis](https://redis.io/)
3. Install [WeazyPrint](http://weasyprint.org/) (PDF generation)

# Development
1. run these commands from project root
```
python manage.py runserver
python manage.py rqworker default
python manage.py tunga_scheduler
```
2. Access the API at http://127.0.0.1:8000/api/ and the backend at http://127.0.0.1:8000/admin/ in your browser

# Testing
1. run this command from project root
```
python manage.py test

``

# Documentation
API Documentation is generated automatically at http://127.0.0.1:8000/api/docs/ using [Django REST Swagger](https://github.com/marcgibbons/django-rest-swagger)

# Deployment
Install [Ansible](https://www.ansible.com/)

## Sandbox
1. Push changes to `develop` branch
2. Run the following commands
```
cd .ansible
ansible-playbook deploy.yml -i env/sandbox
```

## Production
1. Push changes to `master` branch
2. Run the following commands
```
cd .ansible
ansible-playbook deploy.yml -i env/prod
```

connect github repo to slack
