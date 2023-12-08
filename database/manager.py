
import psycopg2

from api.hh_api import HeadHunterApi


class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(company_id),
                title VARCHAR(255),
                min_salary INTEGER,
                max_salary INTEGER,
                currency VARCHAR(10),
                url VARCHAR(255)
            )
        ''')
        self.conn.commit()

    def filling_to_database(self, data):
        for company in data:
            company_name = company.get('company_name', 'unknown company')
            vacancies = company.get('vacancies', [])

            self.cur.execute('''
                INSERT INTO companies (name) VALUES(%s)
                ON CONFLICT (name) DO NOTHING
            ''', (company_name,))

            self.cur.execute('SELECT company_id FROM companies WHERE name = %s', (company_name,))
            company_id = self.cur.fetchone()[0]

            for vacancy in vacancies:
                title = vacancy.get('name', 'unknown title')
                full_salary = vacancy.get('salary')
                currency = full_salary.get('currency') if full_salary else None
                from_salary = full_salary.get('from') if full_salary else 0
                to_salary = full_salary.get('to') if full_salary else 0
                url = vacancy.get('url', 'unknown link')

                self.cur.execute('''
                    INSERT INTO vacancies (company_id, title, min_salary, max_salary, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (company_id, title, from_salary, to_salary, currency, url))

        self.conn.commit()
        return 0

    def get_companies_and_vacancies_count(self):
        self.cur.execute('''
            SELECT companies.name, COUNT(vacancies.vacancy_id) as amount
            FROM companies
            LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
            GROUP BY companies.name;
        ''')
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute('''
            SELECT companies.name, vacancies.title, vacancies.min_salary,
            vacancies.max_salary,  vacancies.currency, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.company_id;
        ''')
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute('''
            SELECT AVG(
                    CASE
                        WHEN vacancies.min_salary IS NOT NULL THEN vacancies.min_salary
                        WHEN vacancies.max_salary IS NOT NULL THEN vacancies.max_salary
                        ELSE NULL
                    END
                )
                FROM vacancies
            ''')
        return int(self.cur.fetchone()[0])

    def get_vacancies_with_higher_salary(self):

        avg_salary = self.get_avg_salary()
        self.cur.execute('''
            SELECT companies.name, vacancies.title, vacancies.min_salary,
            vacancies.max_salary, vacancies.currency, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.company_id
            WHERE (vacancies.min_salary > %s OR vacancies.max_salary > %s)
        ''', (avg_salary, avg_salary))

        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, key_word):
        self.cur.execute('''
            SELECT companies.name, vacancies.title, vacancies.min_salary, 
            vacancies.max_salary, vacancies.currency, vacancies.url
            FROM vacancies 
            JOIN companies ON vacancies.company_id = companies.company_id
            WHERE LOWER(vacancies.title) LIKE %s
        ''', ('%' + key_word.lower() + '%',))
        return self.cur.fetchall()

    def close_conn(self):
        self.cur.close()
        self.conn.close()

