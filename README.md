# Retinal Image Annotation and Evaluation Tools

## Usage

```shell
pip install -r requirements.txt
python -c 'from django.core.management.utils import get_random_secret_key; print("SECRET_KEY="+get_random_secret_key())' > .env
echo "DEBUG=True" >> .env
python manage.py makemigrations
python manage.py migrate
python populate.py
python manage.py runserver
```
