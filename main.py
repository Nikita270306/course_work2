import os
from dotenv import load_dotenv

from api.hh_api import HeadHunterApi
from database.manager import DBManager

load_dotenv()

dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')


def main():
    user_key_word = input('Введите ключевое слово, по которому мы будем искать вакансии:')

    dbmanager = DBManager(dbname=dbname, user=user, password=password, host=host, port=port)

    dbmanager.create_tables()
    dbmanager.filling_to_database(HeadHunterApi.get_vacancies())

    print('Это все компании и колличесво вакансий в этих компаниях: ', dbmanager.get_companies_and_vacancies_count())
    print('Это просто все компании и информация о вакансиях в них: ', dbmanager.get_all_vacancies())
    print('Средняя зарплата по предложенным вакансиям составляет:', dbmanager.get_avg_salary())
    print('Это вакансии с зарплатой выше, чем средняя: ', dbmanager.get_vacancies_with_higher_salary())
    print('А это вакансии по вашему ключевому слову', dbmanager.get_vacancies_with_keyword(user_key_word))

    dbmanager.close_conn()


if __name__ == "__main__":
    main()
