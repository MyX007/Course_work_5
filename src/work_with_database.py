from abc import ABC, abstractmethod
import psycopg2


class BaseDBManager(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_min_salary(self):
        pass

    @abstractmethod
    def get_avg_max_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_min_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_max_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword_in_name(self, keyword):
        pass

    @abstractmethod
    def get_vacancies_with_keyword_in_desc(self, keyword):
        pass


class BaseSaveToDB(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def save_vacs(self, vacs):
        pass

    def save_employers(self, employer):
        pass


class DBManager(BaseDBManager):
    """
    Менеджер базы данных
    """
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список работодателей с количеством их вакансий

        """

        self.cur.execute("SELECT employer, COUNT(*) FROM vacancies GROUP BY employer")

        return {row[0]: row[1] for row in self.cur.fetchall()}

    def get_all_vacancies(self):
        """
        Получает список всех вакансий
        """
        self.cur.execute("SELECT employer, vac_name, salary_from, salary_to, link_to_vac, description FROM vacancies")

        return self.cur.fetchall()

    def get_avg_min_salary(self):
        """
        Получает среднюю минимальную зп по всем вамкансиям
        """
        self.cur.execute("SELECT AVG(salary_from) FROM vacancies")

        return self.cur.fetchone()

    def get_avg_max_salary(self):
        """
        Получает среднюю максимальную зп по всем вамкансиям
        """
        self.cur.execute("SELECT AVG(salary_to) FROM vacancies")

        return self.cur.fetchone()

    def get_vacancies_with_higher_min_salary(self):
        """
        Получает список ваканисй, где минимальная зарплата выше средней
        """
        self.cur.execute("SELECT employer, vac_name, salary_from, salary_to, link_to_vac, description FROM vacancies "
                         "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)")

        return self.cur.fetchall()

    def get_vacancies_with_higher_max_salary(self):
        """
        Получает список ваканисй, где максимальная зарплата выше средней
        """
        self.cur.execute("SELECT employer, vac_name, salary_from, salary_to, link_to_vac, description FROM vacancies "
                         "WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)")

        return self.cur.fetchall()

    def get_vacancies_with_keyword_in_name(self, keyword):
        """
        Получает список вакансий по ключевым словам в названии
        """
        self.cur.execute(f"SELECT employer, vac_name, salary_from, salary_to, link_to_vac, description FROM vacancies "
                         f"WHERE LOWER(vac_name) LIKE %s", ('%' + keyword.lower() + '%',))

        return self.cur.fetchall()

    def get_vacancies_with_keyword_in_desc(self, keyword):
        """
        Получает список вакансий по ключевым словам в описании
        """
        self.cur.execute(f"SELECT employer, vac_name, salary_from, salary_to, link_to_vac, description FROM vacancies "
                         f"WHERE LOWER(description) LIKE %s", ('%' + keyword.lower() + '%',))

        return self.cur.fetchall()


class SaveDataToDB(BaseSaveToDB):
    """
    Класс для сохранения данных в БД
    """
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cur = self.conn.cursor()

    def save_vacs(self, vacs):
        """
        Сохраняет список вакансий
        """

        for vac in vacs:
            salary = vac['salary']
            fomated_salary = {}

            if salary is None:
                fomated_salary['salary_min'] = 0
                fomated_salary['salary_max'] = 0
                fomated_salary['currency'] = "Не указано"
            else:
                if salary is not None and vac['salary']['from'] is None:
                    fomated_salary['salary_min'] = 0
                    fomated_salary['salary_max'] = vac['salary']['to']
                    fomated_salary['currency'] = vac['salary']['currency']

                elif salary is not None and vac['salary']['to'] is None:
                    fomated_salary['salary_max'] = 0
                    fomated_salary['salary_min'] = vac['salary']['from']
                    fomated_salary['currency'] = vac['salary']['currency']
                else:
                    fomated_salary['salary_max'] = vac['salary']['to']
                    fomated_salary['salary_min'] = vac['salary']['from']
                    fomated_salary['currency'] = vac['salary']['currency']

            if vac["snippet"]["responsibility"] is None:
                vac["snippet"]["responsibility"] = "Без описания"

            self.cur.execute("INSERT INTO vacancies (vac_id, vac_name, link_to_vac, "
                             "employer, employer_id, salary_from, salary_to, currency,  description) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (int(vac["id"]), vac["name"], vac["alternate_url"], vac["employer"]["name"],
                                 int(vac["employer"]["id"]), fomated_salary['salary_min'], fomated_salary['salary_max'],
                                 fomated_salary['currency'],
                                 vac["snippet"]["responsibility"][:100]))
            self.conn.commit()

    def save_employers(self, employer):
        """
        Сохраняет список работодателей
        """
        self.cur.execute("INSERT INTO employers (employer_id, name, link, description) VALUES (%s, %s, %s, %s)",
                         (int(employer["id"]), employer["name"],
                             employer["alternate_url"], employer["description"][:100]))
        self.conn.commit()
