# api_yamdb 

api_yamdb 

 

## Описание проекта: 

Проект api_yamdb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. Произведению может быть присвоен жанр (Genre). Произведениям можно поставить оценку из которой будет сформирован их рейтинг и написать отзыв.  

В целях упрощения работы через github actions производится автоматическая провека стиля (flake8), пуш на Dockerhub, deploy на сервере (яндекс облако (проверка функционирования http://130.193.54.207/redoc/). 

 

Это командный проект. Мой участок работы: отзывы и комментарии, рейтинги  (модели, представления,  эндпойнты, определение прав доступа для запросов). Соавторов можно увидеть в конце файла. 

 

 

## Как запустить: 

 

Клонировать репозиторий: 

 

``` 

git clone https://github.com/vladimirramozin/api_yamdb.git 

 

``` 

 

Перейти в него в командной строке: 

 

``` 

cd api_yamdb 

``` 

 

Cоздать и активировать виртуальное окружение: 

 

``` 

python3 -m venv env 

source env/bin/activate 

``` 

 

Установить pip и далее зависимости из файла requirements.txt: 

 

``` 

python3 -m pip install --upgrade pip 

pip install -r requirements.txt 

``` 

 

Перейти в папку проекта: 

 

``` 

cd api_yamdb 

``` 

 

Выполнить миграции: 

 

``` 

python3 manage.py migrate 

``` 

 

Завести тестового суперпользователя admin с паролем admin: 

 

``` 

python3 manage.py createsuperuser 

> admin 

>                 (на запрос email) 

> admin 

> admin           (повтор пароля) 

> y               (ответ на вопрос что пароль слишком простой)  

``` 

 

Запустить проект: 

 

``` 

python3 manage.py runserver 

``` 

## Системные требования: 

requests==2.26.0, 

django==2.2.16, 

djangorestframework==3.12.4, 

PyJWT==1.7.0, 

pytest==6.2.4, 

pytest-django==4.3.0, 

pytest-pythonpath==0.7.3, 

djangorestframework-simplejwt==4.3.0, 

django-filter==21.1 

 

### Над проектом также работали: Владимир Макаров https://github.com/vovamkr, Игорь Батулин https://github.com/IgorGIT 

 

[![Actions Status](https://github.com/vladimirramozin/yamdb_final/workflows/actions/badge.svg)](https://github.com/vladimirramozin/yamdb_final/actions) 

 
