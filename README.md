# Retinal Image Annotation and Evaluation Tools

## Demo

https://retimgtools.fly.dev

## Run locally

First of all, put your images in the `media` directory. If the `media` directory does not exist, create it:

```shell
mkdir media && mkdir media/annotate && mkdir media/evaluate
```

Then, put your images into the corresponding directories. The images will be populated to the database when you run the `populate-*.py` script. Here's an example:

```shell
pip install -r requirements.txt
python -c 'from django.core.management.utils import get_random_secret_key; print("SECRET_KEY="+get_random_secret_key())' > .env
echo "DEBUG=True" >> .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python populate-evaluate-fundus.py
python manage.py runserver
```

You need to adapt the `populate-*.py` script to your own dataset.

Currently, the frontend is primitive and with many parts hard-coded as our project evolves. We will make it more flexible in the future. But for now you also need to adapt the frontend codes (`retimgann/templates/retimgann/*.html` and `retimgeval/templates/retimgeval/*.html`) according to your dataset.