import pandas as pd
from src.config import DATA_PATH
from src.database import engine, recreate_tables


def run_etl():
    print("ETL-пайплайн запущен...")


    df = pd.read_csv(DATA_PATH)


    df['birthdate_key'] = pd.to_datetime(df['birthdate_key'], errors='coerce')
    df['orighiredate_key'] = pd.to_datetime(df['orighiredate_key'], errors='coerce')

    if 'length_of_service' in df.columns:
        df['length_of_service'] = pd.to_numeric(df['length_of_service'], errors='coerce').astype('Int64')

    # 3. Пересоздаем чистые таблицы в базе
    recreate_tables()

    # 4. Факторизация справочников
    df['business_unit_id'], _ = pd.factorize(df['BUSINESS_UNIT'])
    df['department_id'], _ = pd.factorize(df['department_name'])
    df['id_city'], _ = pd.factorize(df['city_name'])
    df['store_id'], _ = pd.factorize(df['store_name'])
    df['job_title_id'], _ = pd.factorize(df['job_title'])
    df['id_term'], _ = pd.factorize(df['termtype_desc'])
    df['termreason_id'], _ = pd.factorize(df['termreason_desc'])

    # 5. Заливка справочников и фактов в базу
    df[['business_unit_id', 'BUSINESS_UNIT']].drop_duplicates().rename(
        columns={'BUSINESS_UNIT': 'business_unit_name'}
    ).to_sql('business_unit', con=engine, if_exists='append', index=False)

    df[['department_id', 'department_name', 'business_unit_id']].drop_duplicates().to_sql(
        'departments', con=engine, if_exists='append', index=False
    )

    df[['id_city', 'city_name']].drop_duplicates().to_sql(
        'cities', con=engine, if_exists='append', index=False
    )

    df[['id_city', 'city_name', 'store_id', 'store_name']].drop_duplicates(subset=['store_id'])[
        ['store_id', 'store_name', 'id_city']].rename(
        columns={'id_city': 'city_id'}
    ).to_sql('stores', con=engine, if_exists='append', index=False)

    df[['job_title_id', 'job_title']].drop_duplicates().rename(
        columns={'job_title': 'job_title_name'}
    ).to_sql('job_titles', con=engine, if_exists='append', index=False)

    df[['id_term', 'termtype_desc']].drop_duplicates().to_sql(
        'terms_types', con=engine, if_exists='append', index=False)

    df[['termreason_id', 'termreason_desc']].drop_duplicates().to_sql(
        'terms_reasons', con=engine, if_exists='append', index=False)

    df[['EmployeeID', 'birthdate_key', 'gender_short', 'gender_full', 'orighiredate_key']].drop_duplicates(
        subset=['EmployeeID']).rename(
        columns={'EmployeeID': 'id'}
    ).to_sql('employees', con=engine, if_exists='append', index=False)

    records_df = df[[
        'EmployeeID', 'STATUS_YEAR', 'department_id', 'length_of_service',
        'STATUS', 'store_id', 'job_title_id', 'id_term', 'termreason_id', 'age'
    ]].rename(columns={
        'EmployeeID': 'id_employee',
        'STATUS_YEAR': 'status_year',
        'STATUS': 'status',
        'id_term': 'termtype_id'
    }).drop_duplicates(subset=['id_employee', 'status_year'])

    records_df.to_sql('employee_yearly_records', con=engine, if_exists='append', index=False)

    print("Все данные успешно обработаны и записаны в базу данных!")


if __name__ == "__main__":
    run_etl()