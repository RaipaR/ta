# Туристическое агентство

Приложение предназначено для хранения данных туристов, управления их бронированиями и генерации документов (например, договоров) на основе шаблонов Microsoft Word.

## Возможности

* хранение информации о туристах (паспортные данные, контакты, дата рождения, заметки);
* сохранение бронирований для выбранного туриста (направление, даты поездки, стоимость, описание);
* вывод списков туристов и их бронирований через командную строку;
* генерация документов Word по шаблону с автоматической подстановкой данных туриста и бронирования.

## Стек

* Python 3.11;
* SQLite для хранения данных;
* [python-docx](https://python-docx.readthedocs.io/en/latest/) для работы с шаблонами `.docx`.

## Установка

1. Создайте и активируйте виртуальное окружение (по желанию):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\\Scripts\\activate   # Windows
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Использование

Все команды доступны через модуль `tour_agency.cli`:

```bash
python -m tour_agency.cli <команда> [опции]
```

### Инициализация базы данных

```bash
python -m tour_agency.cli init-db
```

По умолчанию база данных создаётся в файле `tour_agency.db`. Можно указать другой путь через `--database path/to/file.db`.

### Добавление туриста

```bash
python -m tour_agency.cli add-tourist Иван Иванов AA1234567 \
    --phone "+7-999-000-00-00" \
    --email "ivan@example.com" \
    --date-of-birth 1985-02-14 \
    --notes "Предпочитает экскурсионные туры"
```

### Просмотр списка туристов

```bash
python -m tour_agency.cli list-tourists
```

### Добавление бронирования

```bash
python -m tour_agency.cli add-booking AA1234567 "Бали" 2024-06-01 2024-06-14 240000 \
    --description "Отель 4*, питание завтраки"
```

### Просмотр бронирований туриста

```bash
python -m tour_agency.cli list-bookings AA1234567
```

### Генерация договора

1. Подготовьте шаблон Word (формат `.docx`) с плейсхолдерами вида `{{tourist_first_name}}`, `{{booking_destination}}` и т.д. Полный список доступных полей:
   * `tourist_id`, `tourist_first_name`, `tourist_last_name`, `tourist_passport_number`, `tourist_phone`, `tourist_email`, `tourist_date_of_birth`, `tourist_notes`;
   * `booking_id`, `booking_tourist_id`, `booking_destination`, `booking_start_date`, `booking_end_date`, `booking_price`, `booking_description`.

2. Выполните команду генерации:

```bash
python -m tour_agency.cli generate-contract 1 path/to/template.docx path/to/output.docx
```

Команда подставит данные из бронирования с идентификатором `1` в шаблон и сохранит готовый документ.

## Структура проекта

```
src/
  tour_agency/
    __init__.py
    cli.py              # Командный интерфейс
    database.py         # Работа с SQLite
    document_service.py # Генерация документов
    models.py           # Модели данных
    repository.py       # Слой доступа к данным
```

## Зависимости

Список зависимостей находится в файле `requirements.txt`.
