<H3>Запуск проекта</H3>

Добавить в файл <b>.env</b> следующие переменные:
<ul>
<li> <b>TG_TOKEN</b> - токен телеграм-бота
<li> <b>YANDEX_API_KEY</b> - ключ для работы с <a href="https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html">API Геокодера</a>
</li>
</ul>

Запуск сервера: <b>docker-compose up</b>

Добавить суперпользователя: <b>docker-compose exec admin python manage.py createsuperuser</b>

Панель администратора будет доступна по адресу <a href="http://localhost">localhost</a>

После запуска приложения, автоматически будут созданы две группы для администраторов(Group 1 и Group 2), у которых различаются права доступа

<H3>To do</H3>
<li> Добавить логирование
<li> Добавить обработку ошибок