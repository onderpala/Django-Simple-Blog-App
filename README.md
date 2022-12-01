
# Overview

A simple blog application built upon Django(4.1.3) for self-educational purposes.

Features;

* Automatically converts uploaded images to WebP format.
* "Popular Posts" widget (via [django-hitcount](https://github.com/thornomad/django-hitcount)).
* RichTextUploading Field from [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor).


This code has written with the perspective of "fat models slim views" model*.

## Requirements

 * Python 3.10.2
 * PostgreSQL (Environment variables are in "./config/.env")
 
## Installation

Install Django-Simple-Blog application via terminal

```bash
  pip install -r requirements.txt
```
Edit "./config/.env" file according to your PostgreSQL settings.
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## Optimizations

I redesigned Post model's save method in order to convert all uploaded images to .WebP format.

## Lessons Learned

 * [django-hitcount](https://github.com/thornomad/django-hitcount) Simple usage.
 * [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor) RichTextUploadingField usage and workflow.
 * If you dont recylce unused images, nobody is there for them. [django-cleanup](https://github.com/un1t/django-cleanup).
 * How to convert an image into .webp format using [Pillow](https://github.com/python-pillow/Pillow).
 * How to edit image while uploading.
 * How to create custom template tag.