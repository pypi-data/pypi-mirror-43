| WARNING: This project is not maintained anymore. |
| --- |

# Django Manifest

A kickstarter for Django Web Framework projects.

Tested with Django 2.1.7

## Quick Start

Run in shell:

```
$ virtualenv my_env
$ source my_env/bin/activate
(my_env)$ pip install django-manifest
(my_env)$ django-admin startproject my_site . --template=path/to/manifest/project/template
(my_env)$ pip install --upgrade -r my_site/requirements.txt
(my_env)$ python manage.py migrate
(my_env)$ python manage.py runserver
```