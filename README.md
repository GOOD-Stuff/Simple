# README #

Веб сайт состоит из 2ух страниц: на первой странице отображаются загруженные из базы данных фотографии с их описанием; на второй - отображается форма из пары кнопок и области для ввода текста. 

Проект написан на языке python 3.5 с применением фреймворка Flask 0.10 и базы данных sqlite3. Система: Ubuntu 15.10; IDE: PyCharm 5.0.4

На linux машинах, БД располагается в папке /tmp. Содержание БД:

Имя: upld.db;

Таблица: entries;

Column:

* id - основной ключ таблицы;
* photoPath - содержит имя файла с расширением; 
* comm - содержит описание, данное к изображению;

Для инициализации БД можно воспользоваться командой:

```
#!python

from Simple import init_db
init_db()
```

или

```
#!shell

sqlite3 /tmp/upld.db < schema.sql
```


В [Downloads](https://bitbucket.org/Gustoff/simple/downloads) находятся уже готовая БД и архив с фотографиями. Папку с фотографиями и БД нужно поместить в /tmp:

Фотографии: /tmp/upload/

БД: /tmp/upld.db