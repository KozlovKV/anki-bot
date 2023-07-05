# AnkiBot
Телеграм-бот для Анки-карточек с возможностью добавления одной и той же карточки в несколько коллекций на основании алгоритма [SM-2](https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method)

## Принцип работы
Пользователь может добавлять/удалять/изменять карточки/лэйблы. К карточке он может привязать необходимый лэйбл. Запускаться тренировка будет по определённому лэйблу и проходить по принципу Анки-карточек.

Если лэйбл публичный, то по его идентификатору любой пользователь сможет проходить тренировку

*Дополнительная фича:* 
1. копирование лэйбла и связанных с ним карточек. Создаётся копия данного лэйбла и всех связей вместе с карточками, но уже с другим владельцем
2. ChatGPT - не совсем понимаю, для чего он тут нужен вообще, но во время презентации проекта его предлагали

## Tech stack
Разработка полностью на Питоне:
- API для телеграм бота ([python-telegram-bot](https://docs.python-telegram-bot.org/en/latest/index.html))
- ORM для работы с реляционной БД ([peewee](https://docs.peewee-orm.com/en/latest/index.html))

## Архитектура БД 
*`user_id` - id пользователя в Телеграм*

Сущности:
- Карточка
  - `card_id` - **PK**
  - `user_id` - **FK**
  - Сторона 1
  - Сторона 2
- Лэйбл
  - `label_id` - **PK**
  - `user_id` - **FK**
  - Название
  - Название первой стороны
  - Название второй стороны
  - `isPrivate` - если `false`, тогда по `label_id` тренироваться смогут и другие пользователи
- Цепь между лэйблом и карточкой
  - `card_id` - **PK,FK** (каскадное удаление)
  - `label_id` - **PK,FK** (каскадное удаление)
  - `isReversed` - если `false`, значит название первой стороны относится к первой стороне карточки
- Тренировочные записи
  - `card_id` - **PK, FK** (каскадное удаление)
  - `user_id` - **PK**
  - момент последнего повторения
  - через сколько дней надо провести повторение `l(n)`
  - текущий E-фактор