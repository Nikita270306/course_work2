from pprint import pprint

import requests


class HeadHunterApi:
    @staticmethod
    def get_vacancies() -> list:
        params = {
            'only_with_salary': 'true'}
        data = requests.get("https://api.hh.ru/vacancies", params=params).json()
        formatted_response = []

        for vacancy in data['items']:
            if vacancy['salary']['currency'] == 'BYR':
                vacancy['salary']['currency'] = 'RUR'
                if vacancy['salary']['from'] is not None:
                    vacancy['salary']['from'] = vacancy['salary']['from'] * 28
                elif vacancy['salary']['to'] is not None:
                    vacancy['salary']['to'] = vacancy['salary']['to'] * 28

            elif vacancy['salary']['currency'] == 'UZS':
                vacancy['salary']['currency'] = 'RUR'
                if vacancy['salary']['from'] is not None:
                    vacancy['salary']['from'] = int(float(vacancy['salary']['from']) * 0.0076)
                elif vacancy['salary']['to'] is not None:
                    vacancy['salary']['to'] = int(float(vacancy['salary']['to']) * 0.0076)
            elif vacancy['salary']['currency'] == 'KZT':
                continue

            company_name = vacancy.get('employer', {}).get('name', 'Не указано')
            cute_vacancy = {
                "name": vacancy.get("name", "Не указано"),
                "salary": vacancy.get("salary", "Не указано"),
                "url": vacancy.get("url", "Не указано"),
                "company_name": company_name
            }

            if len(formatted_response) == 0:
                formatted_response.append({
                    'company_name': company_name,
                    'vacancies': [cute_vacancy]
                })
            else:
                count = 0
                for comp in formatted_response:
                    if comp['company_name'] == company_name:
                        count += 1
                if count == 1:
                    for new_comp in formatted_response:
                        if new_comp['company_name'] == company_name:
                            new_comp['vacancies'].append(cute_vacancy)
                        else:
                            continue
                if count == 0:
                    formatted_response.append({
                        'company_name': company_name,
                        'vacancies': [cute_vacancy]
                    })
        return formatted_response


if __name__ == "__main__":
    pprint(HeadHunterApi().get_vacancies())
