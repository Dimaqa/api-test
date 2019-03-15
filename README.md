# Тестовое задание для собеседования в Avito api4biz

Реализованы 4 POST метода и тесты для них.

- /add_product
- /add_worker
- /add_company
- /edit_responsible

 Для add_product реализовано кеширование запросов.
Edit_responsible возвращает текующий список товаров и ответственных за них в формате json. Таблица connection реализует свзять многие ко многим.

## Запуск

```Bash
docker-compose up
````

## Тесты

```Bash
cd tests
python -m unittest api-tests.py
````
