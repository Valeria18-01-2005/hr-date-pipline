ETL для загрузки и преобразования данных из csv

CSV -> Python ETL -> MySQL Data Warehouse

## Technologies

- Python 3.12
- pandas
- SQLAlchemy
- PyMySQL
- MySQL 8.0
- Docker
- Docker Compose

## Project structure

```text
hr-date-pipline/
│
├── data/
│   └── MFG10YearTerminationData.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── etl.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

ETL-пайплайн выполняет следующие шаги:

1. Загружает HR-данные из CSV-файла.
2. Приводит даты и числовые значения к нужным типам.
3. Пересоздаёт таблицы в MySQL.
4. Формирует идентификаторы для справочных таблиц.
5. Загружает справочные данные в MySQL.
6. Загружает основные записи сотрудников в таблицу employee_yearly_records.

В базе данных создаются 9 таблиц:

employees
business_unit
departments
cities
stores
job_titles
terms_types
terms_reasons
employee_yearly_records

## КАК ЗАПУСТИТЬ ПРОЕКТ

### 1. Клонировать репозиторий

```bash
git clone git@github.com:Valeria18-01-2005/hr-date-pipline.git
cd hr-date-pipline
```

### 2. Создать файл .env

Скопировать файл .env.example:

```bash
cp .env.example .env
```

При необходимости изменить значения в .env.

Пример:

```env
MYSQL_ROOT_PASSWORD=change_me
MYSQL_DATABASE=hr_analytics_dwh
MYSQL_PORT=3307
```

### 3. Запустить Docker Compose

```bash
docker compose up --build
```

Docker автоматически:

- запускает MySQL 8.0;
- создаёт базу данных hr_analytics_dwh;
- ждёт готовности MySQL;
- собирает Python-контейнер;
- устанавливает зависимости из requirements.txt;
- запускает ETL-пайплайн;
- загружает данные из CSV в MySQL.

При успешном выполнении ETL завершится с кодом 0.

### 4. Запуск в фоновом режиме

```bash
docker compose up -d
```

Проверить состояние контейнеров:

```bash
docker compose ps -a
```

### 5. Остановка проекта

```bash
docker compose down
```

Для удаления вместе с данными MySQL:

```bash
docker compose down -v
```

После запуска данные из CSV загружаются в MySQL Data Warehouse.

В текущем наборе данных в таблицу employee_yearly_records загружается 49 648 записей.