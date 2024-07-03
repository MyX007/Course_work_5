from abc import ABC, abstractmethod
import requests


class API(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacs(self, name, only_with_salary, area):
        pass

    @abstractmethod
    def get_employers(self):
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API hh.ru
    """
    def __init__(self, api_url='https://api.hh.ru/vacancies'):
        """
        Конструктор класса
        """
        self.api_url = api_url

    def get_vacs(self, employer_id, only_with_salary=False, area=None):
        """
        Метод для получения вакансий по заданным параметрам с сайта hh.ru.
        """

        params = {
            "employer_id": employer_id,
            "page": 0,
            "per_page": 100,
            "only_with_salary": only_with_salary,
            "area": area
        }
        response = requests.get(self.api_url, params)

        if response.status_code == 200:
            return response.json()["items"]
        else:
            return []

    def get_employers(self):
        """
        Метод для получения работодателей по заданным параметрам с сайта hh.ru.
        """
        response = requests.get(self.api_url)

        if response.status_code == 200:
            return response.json()
        else:
            return []
