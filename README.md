# README #

Веб сайт состоит из 2ух страниц: на первой странице отображаются загруженные из базы данных фотографии с их описанием; на второй - отображается форма из пары кнопок и области для ввода текста. 

Проект написан на языке python 3.5 с применением фреймворка Flask 0.10 и базы данных sqlite3. Система: Ubuntu 15.10; IDE: PyCharm 5.0.4

Для инициализации БД можно воспользоваться командой:
from Simple import init_db
init_db()
или 
sqlite3 /upld.db < schema.sql

В Downloads находится уже готовая БД и архив с фотографиями. 