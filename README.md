# Task
Требования:
- [x] Для комнат должны быть поля: номер/название, стоимость за сутки, количество
мест.
- [x] Пользователи должны уметь фильтровать и сортировать комнаты по цене, по
количеству мест.
- [x] Пользователи должны уметь искать свободные комнаты в заданном временном
интервале.
- [x] Пользователи должны уметь забронировать свободную комнату.
- [x] Суперюзер должен уметь добавлять/удалять/редактировать комнаты и
редактировать записи о бронях через админ панель Django.
- [x] Брони могут быть отменены как самим юзером, так и суперюзером.
- [x] Пользователи должны уметь регистрироваться и авторизовываться (логиниться).
- [x] Чтобы забронировать комнату пользователи должны быть авторизованными.
Просматривать комнаты можно без логина. Авторизованные пользователи должны
видеть свои брони.

- [x] Автотесты;
- [x] Аннотации типов;
- [x] Линтер;
- [x] Автоформатирование кода;
- [x] Документация к API;
- [x] Инструкция по запуску приложения.

# Запуск(docker)
1. Реализовано развертывание приложения с помощью докера, для этого небходимо установить docker desktop и запустить его.
2. После запуска докера прописать
 ```docker-compose build```
3. Дождаться билда проекта и прописать
```docker-compose up -d```
4. Перейти на страницу
```http://127.0.0.1:8000/swagger/```
# Запуск (не докер)
1. Клонировать репозиторий
2. Из корневой директории проекта прописать
```pip install -r requirements.txt```
3. Поменять ENV файл на свои данные (postgreSQL)
4. Создать миграции
`python hotel/manage.py makemigrations
6. Мигрировать
`python hotel/manage.py migrate
7. Загрузить фикстуры из корневой директории проекта прописать
```python hotel/manage.py loaddata hotel/fixtures.json```
# Описание
1. Реализованы все пункты задания. Касаемо бронирования -> запрос get /reservation/ выводит все брони зарегестрированого пользователя, либо все существующие брони, если пользователь админ.
2. Get запрос к комнатам позволяет фильтровать, сортировать и выводит свободные комнаты по датам.
3. Отмена броней реализована, как delete запрос, то есть удаляет бронь, пользователь может удалить только свою бронь.
4. Тесты реализованы для эндпоинтов, тестирует весь функционал, который поставлен в требованиях.
5. Созданы фикстуры, которые автоматически подгрузятся, если запуск через докер, для автоматического заполнения БД. Супер юзер создан логин: 123 пароль: 123
