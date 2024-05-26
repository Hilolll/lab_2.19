#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего варианта лабораторной работы 2.17 добавьте возможность хранения
# файла данных в домашнем каталоге пользователя. Для выполнения операций с
# файлами необходимо использовать модуль pathlib.

from pathlib import Path
import argparse
import json
import os
from datetime import datetime
import jsonschema

person_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "surname": {"type": "string"},
        "date_of_birth": {"type": "string", "format": "date"},
        "zodiac_sign": {"type": "string"}
    },
    "required": ["name", "surname", "date_of_birth", "zodiac_sign"]
}


def validate_person(person_data, schema):
    try:
        jsonschema.validate(person_data, schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Данные человека не соответствуют схеме: {e}")
        return False


def add_person(people, name, surname, date_of_birth, zodiac_sign):
    """
    Добавление нового человека в список.
    Список сортируется по знаку зодиака после добавления нового элемента.
    """
    date_of_birth = datetime.strptime(date_of_birth, '%d.%m.%Y')

    person = {
        'name': name,
        'surname': surname,
        'date_of_birth': date_of_birth,
        'zodiac_sign': zodiac_sign
    }

    people.append(person)
    people.sort(key=lambda item: item.get('zodiac_sign', ''))
    return people


def list_people(people):
    """
    Вывод таблицы людей.
    """
    line = '+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 20,
        '-' * 15,
        '-' * 13
    )
    print(line)
    print(
        '| {:^4} | {:^20} | {:^20} | {:^15} | {:^12} |'.format(
            "№",
            "Имя",
            "Фамилия",
            "Знак Зодиака",
            "Дата рождения"
        )
    )
    print(line)

    for idx, person in enumerate(people, 1):
        birth_date_str = person.get('date_of_birth').strftime('%d.%m.%Y')
        print(
            '| {:^4} | {:<20} | {:<20} | {:<15} | {:<13} |'.format(
                idx,
                person.get('name', ''),
                person.get('surname', ''),
                person.get('zodiac_sign', ''),
                birth_date_str
            )
        )

    print(line)


def select_people(people, month):
    """
    Вывести список людей, родившихся в заданном месяце.
    """
    count = 0
    for person in people:
        if person.get('date_of_birth').month == month:
            count += 1
            print('{:>4}: {} {}'.format(count, person.get(
                'name', ''), person.get('surname', '')))

    if count == 0:
        print("Люди, родившиеся в указанном месяце, не найдены.")


def save_people(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    staff_formatted = [{**person, 'date_of_birth': person.get(
        'date_of_birth').strftime('%d.%m.%Y')} for person in staff]
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        json.dump(staff_formatted, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        staff_loaded = json.load(fin)
        result_people = []
        for person in staff_loaded:
            if validate_person(person, person_schema):
                try:
                    person['date_of_birth'] = datetime.strptime(
                        person['date_of_birth'], '%d.%m.%Y')
                    result_people.append(person)
                except:
                    print(
                        f"Ошибка при разборе даты в записи, пропуск записи"
                        "{cnt}.")
            else:
                print("Неверные данные человека, пропуск записи.")
        return result_people


def main():
    # Создание основного парсера.
    parser = argparse.ArgumentParser(description="Управление списком людей")

    # Создание подпарсеров.
    subparsers = parser.add_subparsers(dest="command")

    # Создание парсера для добавления человека.
    parser_add = subparsers.add_parser('add', help="Добавить человека")
    parser_add.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )
    parser_add.add_argument("-n", "--name", help="Имя человека")
    parser_add.add_argument("-s", "--surname", help="Фамилия человека")
    parser_add.add_argument(
        "-d", "--date_of_birth", help="Дата рождения (формат ДД.ММ.ГГГГ)")
    parser_add.add_argument("-z", "--zodiac_sign", help="Знак зодиака")

    # Создание парсера для вывода списка людей.
    parser_list = subparsers.add_parser('list', help="Вывести список людей")
    parser_list.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создание парсера для выбора человека по месяцу рождения.
    parser_select = subparsers.add_parser(
        'select', help="Выбрать людей по месяцу рождения")
    parser_select.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )
    parser_select.add_argument(
        "-m", "--month", type=int, help="Месяц рождения")

    # Разбираем аргументы командной строки.
    args = parser.parse_args()

    is_dirty = False

    home_directory = Path.home()
    data_directory = home_directory / 'data'
    # Создаем каталог, если он не существует.
    data_directory.mkdir(exist_ok=True)
    filename = data_directory / args.filename

    if os.path.exists(filename):
        people = load_people(filename)
    else:
        people = []

    # Определяем, какую команду нужно выполнить.
    if args.command == 'add':
        people = add_person(people, args.name, args.surname,
                            args.date_of_birth, args.zodiac_sign)
        is_dirty = True

    elif args.command == 'list':
        list_people(people)

    elif args.command == 'select':
        select_people(people, args.month)

    if is_dirty:
        save_people(filename, people)


if __name__ == '__main__':
    main()
