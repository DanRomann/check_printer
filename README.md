# check_printer

## Запуск
Для запуска предварительно требуется выполнить следующие команды
```
pip install -r requierments.txt
docker-compose up --build
python manage.py migrate
python manage.py rqworker default
python manage.py runserver
```

## Админка
Для входа в админку требуется создать пользователя
```
python manage.py createsuperuser
```
