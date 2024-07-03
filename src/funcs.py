import psycopg2


def login_to_db():
    """
    Функция ввода данных для авторизации в БД
    Возвращает словарь с данными
    """
    login_data = {"host": input("Введите адрес базы данных: "), "name": input("Введите название базы данных: "),
                  "login": input("Введите логин: "), "password": input("Введите пароль: ")}

    return login_data


def format_vac_data(vacs):
    """
    Функция форматирования данных о вакансии для последующего вывода на экран пользователю
    """

    for vac in vacs:
        if vac[2] == 0 and vac[3] == 0:
            salary = "Не указана"
        elif vac[2] == 0 and vac[3] != 0:
            salary = f"До {vac[3]}"
        elif vac[2] != 0 and vac[3] == 0:
            salary = f"От {vac[2]}"
        else:
            salary = f"От {vac[2]} До {vac[3]}"

        print(f"\nРаботодатель: {vac[0]}\nВакансия: {vac[1]}\nЗарплата: {salary}\n"
              f"Ссылка на вакансию: {vac[4]}\n"
              f"Описание: {vac[5]}\n\n{'-' * 220}")


def clean_tables(host, database, user, password):
    with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE vacancies, employers RESTART IDENTITY")

            conn.commit()


def create_tables(host, database, user, password):
    with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
    ) as conn:
        with conn.cursor() as cur:

            cur.execute("CREATE TABLE IF NOT EXISTS vacancies (vac_id int , vac_name varchar(100) NOT NULL, "
                        "link_to_vac varchar(100) NOT NULL, employer varchar(100) NOT NULL, "
                        "employer_id int, salary_from int, salary_to int, currency varchar(15),"
                        " description varchar(100),"
                        "CONSTRAINT pk_vacancies_vac_id PRIMARY KEY (vac_id),"
                        "CONSTRAINT pk_employers_employer_id FOREIGN KEY (employer_id) "
                        "REFERENCES employers(employer_id))")

            cur.execute("CREATE TABLE IF NOT EXISTS employers (employer_id int , "
                        "name varchar(100) NOT NULL, link varchar(100) NOT NULL, "
                        "description varchar(100), "
                        "CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id))")

            conn.commit()
