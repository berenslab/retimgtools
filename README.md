# Retinal Image Annotation and Evaluation Tools

## Demo

https://retimgtools.fly.dev

## Run locally

Before running the application, place your images in the media directory. If it does not exist, create the necessary folders:

```shell
mkdir -p media/annotate media/evaluate
```

Then, add your images to the corresponding directories. The database will be populated with these images when you run the populate-*.py script.

Install dependencies and set up the environment:

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

You need to adapt the `populate-*.py` script to match your dataset.

Currently, the frontend is primitive and contains hardcoded elements as the project evolves. We plan to make it more flexible in the future, but for now, you may need to modify the templates (r`etimgann/templates/retimgann/*.html` and `retimgeval/templates/retimgeval/*.html`) to suit your data.