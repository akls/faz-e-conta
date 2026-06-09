cd faz_e_conta
python manage.py makemigrations
python manage.py migrate
cd ..
python run.py
cd faz_e_conta
python create_superuser.py
python manage.py runserver 0.0.0.0:8000