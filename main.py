from src.work_with_api import HeadHunterAPI
from src import work_with_database
from data import config
from src import funcs

# Создание экземпляров класса и приветствие

print("Здравствуйте! Для дальнейшей работы программы необходимо ввести данные для авторизации в БД.")

login_to_db = funcs.login_to_db()

hh_vacs = HeadHunterAPI("https://api.hh.ru/vacancies")
db_vacs = work_with_database.DBManager(
    login_to_db['host'], login_to_db['name'], login_to_db['login'], login_to_db['password'])
db_saver = work_with_database.SaveDataToDB(
    login_to_db['host'], login_to_db['name'], login_to_db['login'], login_to_db['password'])

# Создание таблиц с вакансиями и работодателями
funcs.create_tables(login_to_db['host'], login_to_db['name'], login_to_db['login'], login_to_db['password'])

# Очистка таблиц от старых данных, если они имеются
funcs.clean_tables(login_to_db['host'], login_to_db['name'], login_to_db['login'], login_to_db['password'])

# Сохранение вакансий и работодателей в соответствующие таблицы в БД
for employer in config.employers_id:
    hh_employer = HeadHunterAPI(f"https://api.hh.ru/employers/{employer}")
    db_saver.save_employers(hh_employer.get_employers())

for vac in config.employers_id:
    hh_vac = HeadHunterAPI()
    db_saver.save_vacs(hh_vac.get_vacs(vac))


def main_func():
    """
    Функция интерактива с пользователем
    """
    while True:
        # Выбор основных действий для работы с программой
        functions = input("\nВыберите действие (введите номер):\n"
                          "1. Вывести на экран всех сохраненных работодателей и кол-во их вакансий \n"
                          "2. Вывести на экран список всех вакансий\n"
                          "3. Вывести на экран среднюю зарплату среди всех вакансий\n"
                          "4. Вывести на экран список вакансий с зарплатой выше средней\n"
                          "5. Поиск вакансий по ключевым словам\n"
                          "0. Завершить программу\n-> ")

        if functions == "1":
            # Вывод на экран всех сохраненных работодателей и кол-во их вакансий
            for k, v in db_vacs.get_companies_and_vacancies_count().items():
                print(f"\n{k} - {v}\n\n{'-' * 220}")
            continue
        if functions == "2":
            # Вывод на экран список всех вакансий
            funcs.format_vac_data(db_vacs.get_all_vacancies())

        elif functions == "3":
            # Вывод на экран среднюю зарплату среди всех вакансий
            min_or_max = input("Выберите действие:\n1. Вывести среднюю минимальную зарплату\n"
                               "2. Вывести среднюю максимальную зарплату\n0. Вернуться в начало\n-> ")
            if min_or_max == "1":
                # Вывод среднюю минимальную зарплату
                print(f"\n{round(db_vacs.get_avg_min_salary()[0], 2)}")
            elif min_or_max == "2":
                # Вывод среднюю максимальную зарплату
                print(f"{round(db_vacs.get_avg_max_salary()[0], 2)}")
            elif min_or_max == "0":
                # Возврат в начало программы
                continue

        elif functions == "4":
            # Вывод на экран список вакансий с зарплатой выше средней
            min_or_max = input("Выберите действие:\n1. Сортировать по минимальной зарплате\n"
                               "2. Сортировать по максимальной зарплате\n0. Вернуться в начало\n-> ")
            if min_or_max == "1":
                # Сортировка по минимальной зарплате
                funcs.format_vac_data(db_vacs.get_vacancies_with_higher_min_salary())
            elif min_or_max == "2":
                # Сортировка по максимальной зарплате
                funcs.format_vac_data(db_vacs.get_vacancies_with_higher_max_salary())
            elif min_or_max == "0":
                # Возврат в начало программы
                continue

        elif functions == "5":
            # Поиск вакансий по ключевым словам
            keyword_in = input("Выберите действие:\n1. Поиск по ключевым словам в названии\n"
                               "2. Поиск по ключевым словам в описании\n0. Вернуться в начало\n-> ")

            if keyword_in == "1":
                # Поиск по ключевым словам в названии
                vac_keyword = input("Введите ключевое слово: ")
                funcs.format_vac_data(db_vacs.get_vacancies_with_keyword_in_name(vac_keyword))
            elif keyword_in == "2":
                #
                vac_keyword = input("Введите ключевое слово: ")
                # Поиск по ключевым словам в описании
                funcs.format_vac_data(db_vacs.get_vacancies_with_keyword_in_desc(vac_keyword))
            elif keyword_in == "0":
                # Возврат в начало программы
                continue

        elif functions == "0":
            # Заваершение программы

            print("Программа успешно завершена!")
            break

        else:
            # В случае, если введено значение, не совпадающее с пунктами программы,
            # возвращает пользователся к началу программы

            continue


if __name__ == "__main__":
    main_func()
