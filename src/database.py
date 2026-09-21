from sqlalchemy import create_engine, text
from src.config import DB_URL

engine = create_engine(DB_URL)

DROP_AND_CREATE_TABLES_SQL = """
    SET FOREIGN_KEY_CHECKS = 0;

    DROP TABLE IF EXISTS employee_yearly_records;
    DROP TABLE IF EXISTS employees;
    DROP TABLE IF EXISTS stores;
    DROP TABLE IF EXISTS cities;
    DROP TABLE IF EXISTS job_titles;
    DROP TABLE IF EXISTS terms_types;
    DROP TABLE IF EXISTS terms_reasons;
    DROP TABLE IF EXISTS departments;
    DROP TABLE IF EXISTS business_unit;

    CREATE TABLE employees (
        id INT PRIMARY KEY,
        birthdate_key DATE,
        gender_short VARCHAR(1),
        gender_full VARCHAR(10),
        orighiredate_key DATE  
    );

    CREATE TABLE business_unit (
        business_unit_id INT PRIMARY KEY,
        business_unit_name VARCHAR(45)
    );

    CREATE TABLE departments (
        department_id INT PRIMARY KEY,
        department_name VARCHAR(45),
        business_unit_id INT,
        FOREIGN KEY (business_unit_id) REFERENCES business_unit(business_unit_id)
    );

    CREATE TABLE cities (
        id_city INT PRIMARY KEY,
        city_name VARCHAR(45)
    );

    CREATE TABLE stores (
        store_id INT PRIMARY KEY,
        store_name VARCHAR(45),
        city_id INT,
        FOREIGN KEY (city_id) REFERENCES cities(id_city)
    );

    CREATE TABLE job_titles (
        job_title_id INT PRIMARY KEY,
        job_title_name VARCHAR(45)
    );

    CREATE TABLE terms_types (
        id_term INT PRIMARY KEY,
        termtype_desc VARCHAR(45)
    );

    CREATE TABLE terms_reasons (
        termreason_id INT PRIMARY KEY,
        termreason_desc VARCHAR(45)
    );

    CREATE TABLE employee_yearly_records (
        id_employee INT,
        status_year INT,
        department_id INT,
        length_of_service FLOAT,
        status VARCHAR(45),
        store_id INT,
        job_title_id INT,
        termtype_id INT,
        termreason_id INT,
        age INT,

        PRIMARY KEY(id_employee, status_year),
        FOREIGN KEY (id_employee) REFERENCES employees(id),
        FOREIGN KEY (store_id) REFERENCES stores(store_id),
        FOREIGN KEY (job_title_id) REFERENCES job_titles(job_title_id),
        FOREIGN KEY (termtype_id) REFERENCES terms_types(id_term),
        FOREIGN KEY (termreason_id) REFERENCES terms_reasons(termreason_id),
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
    );

    SET FOREIGN_KEY_CHECKS = 1;
"""


def recreate_tables():
    try:
        with engine.connect() as connection:
            for statement in DROP_AND_CREATE_TABLES_SQL.split(";"):
                if statement.strip():
                    connection.execute(text(statement))
                    connection.commit()
        print("Таблицы успешно пересозданы с нуля.")
    except Exception as e:
        print("Ошибка при создании таблиц:", e)