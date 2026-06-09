import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faz_e_conta.settings')
django.setup()

from django.contrib.auth.models import User

username = 'rodri'
password = 'nuno2013'
email = ''

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f'Superuser "{username}" criado com sucesso.')
else:
    print(f'Superuser "{username}" já existe, a ignorar.')