import re
import dash_bootstrap_components as dbc
from dash import html

from src.exceptions import InvalidNomenclature


def to_roman(number) -> str:
    if not (0 < number < 4000):
        raise InvalidNomenclature

    roman_numerals = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    result = ""
    for (arabic, roman) in roman_numerals:
        while number >= arabic:
            result += roman
            number -= arabic
    return result


def from_roman(roman: str) -> int:
    roman_to_arabic = {
        'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
        'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
        'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1
    }

    i = 0
    number = 0
    while i < len(roman):
        try:
            if i + 1 < len(roman) and roman[i:i + 2] in roman_to_arabic:
                number += roman_to_arabic[roman[i:i + 2]]
                i += 2
            else:
                number += roman_to_arabic[roman[i]]
                i += 1
        except KeyError:
            raise InvalidNomenclature
    return number


def parse_nomenclature(nomenclature: str):
    parts = nomenclature.split("-")
    if (
            not parts
            or not parts[0].isalpha()
            or not ('A' <= parts[0] <= 'Z' or 'a' <= parts[0] <= 'z')
    ):
        raise InvalidNomenclature

    if len(parts) == 3:
        zone, map_number, sub_part = parts
        return zone, map_number, sub_part, None
    elif len(parts) == 4:
        zone, map_number, sub_number, sub_letter = parts
        return zone, map_number, sub_number, sub_letter
    else:
        raise InvalidNomenclature


def calculate_500_000(zone, map_number, sub_number, *args, **kwargs):
    directions = {
        'lt': {'Б': (1, 0, 'В'), 'А': (1, -1, 'Г'), 'В': (0, -1, 'Б'), 'Г': (0, 0, 'А')},
        't': {'А': (1, 0, 'В'), 'Б': (1, 0, 'Г'), 'В': (0, 0, 'А'), 'Г': (0, 0, 'Б')},
        'rt': {'А': (1, 0, 'Г'), 'Б': (1, 1, 'В'), 'В': (0, 0, 'Б'), 'Г': (0, 1, 'А')},
        'l': {'А': (0, -1, 'Б'), 'Б': (0, 0, 'А'), 'В': (0, -1, 'Г'), 'Г': (0, 0, 'В')},
        'r': {'А': (0, 0, 'Б'), 'Б': (0, 1, 'А'), 'В': (0, 0, 'Г'), 'Г': (0, 1, 'В')},
        'lb': {'А': (0, -1, 'Г'), 'Б': (0, 0, 'В'), 'В': (-1, -1, 'Б'), 'Г': (-1, 0, 'А')},
        'b': {'А': (0, 0, 'В'), 'Б': (0, 0, 'Г'), 'В': (-1, 0, 'А'), 'Г': (-1, 0, 'Б')},
        'rb': {'А': (0, 0, 'Г'), 'Б': (0, 1, 'В'), 'В': (-1, 0, 'Б'), 'Г': (-1, 1, 'А')}
    }

    nomenclatures = {'m': f'{zone}-{map_number}-{sub_number}'}
    for direction in directions.keys():
        zone_change, map_change, new_sub_number = directions[direction][sub_number]

        new_zone = chr(ord(zone) + zone_change)
        new_map_number = map_number + map_change

        nomenclatures[direction] = f"{new_zone}-{new_map_number}-{new_sub_number}"
    return nomenclatures


def calculate_200_000(zone, map_number, sub_number, *args, **kwargs):
    if (roman_digit := from_roman(sub_number)) > 36:
        raise InvalidNomenclature
    directions = {
        'lt': (0, 0, roman_digit - 7),
        't': (0, 0, roman_digit - 6),
        'rt': (0, 0, roman_digit - 5),
        'l': (0, 0, roman_digit - 1),
        'r': (0, 0, roman_digit + 1),
        'lb': (0, 0, roman_digit + 5),
        'b': (0, 0, roman_digit + 6),
        'rb': (0, 0, roman_digit + 7)
    }

    if 1 <= roman_digit <= 6:
        directions.update({
            'lt': (1, 0, 29 + roman_digit),
            't': (1, 0, 30 + roman_digit),
            'rt': (1, 0, 31 + roman_digit),
            'lb': (0, 0, roman_digit + 5),
            'b': (0, 0, roman_digit + 6),
            'rb': (0, 0, roman_digit + 7)
        })
        if roman_digit == 1:
            directions.update({'lt': (1, -1, 36), 'l': (0, -1, 6), 'lb': (0, -1, 12)})
        elif roman_digit == 6:
            directions.update({'rt': (1, 1, 31), 'r': (0, 1, 1), 'rb': (0, 1, 7)})
    elif 31 <= roman_digit <= 36:
        directions.update({
            'lt': (1, -1, roman_digit - 6),
            't': (0, 0, roman_digit - 6),
            'rt': (0, 0, roman_digit - 6),
            'lb': (-1, 0, roman_digit - 31),
            'b': (-1, 0, roman_digit - 30),
            'rb': (-1, 0, roman_digit - 29)
        })
        if roman_digit == 31:
            directions.update({'lt': (0, -1, 30), 'l': (0, -1, 36), 'lb': (-1, -1, 6)})
        elif roman_digit == 36:
            directions.update({'rt': (0, 1, 25), 'r': (0, 1, 31), 'rb': (-1, 1, 1)})
    elif roman_digit in (7, 13, 19, 25):
        directions.update({'lt': (0, -1, roman_digit - 1), 'l': (0, -1, roman_digit + 5)})
    elif roman_digit in (12, 18, 24, 30):
        directions.update({'rt': (0, 1, roman_digit - 11), 'r': (0, 1, roman_digit - 5)})

    nomenclatures = {'m': f'{zone}-{map_number}-{sub_number}'}
    for direction, (zone_change, map_change, new_sub_number) in directions.items():
        new_zone = chr(ord(zone) + zone_change)
        new_map_number = map_number + map_change
        nomenclatures[direction] = f"{new_zone}-{new_map_number}-{to_roman(new_sub_number)}"

    return nomenclatures


def calculate_100_000(zone, map_number, sub_number, *args, **kwargs):
    sub_number = int(sub_number)

    directions = {
        'lt': (0, 0, sub_number - 13),
        't': (0, 0, sub_number - 12),
        'rt': (0, 0, sub_number - 11),
        'l': (0, 0, sub_number - 1),
        'r': (0, 0, sub_number + 1),
        'lb': (0, 0, sub_number + 11),
        'b': (0, 0, sub_number + 12),
        'rb': (0, 0, sub_number + 13)
    }

    if 1 <= sub_number <= 12:
        directions.update({
            'lt': (1, 0, 131 + sub_number),
            't': (1, 0, 132 + sub_number),
            'rt': (1, 0, 133 + sub_number),
            'lb': (0, 0, sub_number + 11),
            'b': (0, 0, sub_number + 12),
            'rb': (0, 0, sub_number + 13)
        })
        if sub_number == 1:
            directions.update({'lt': (1, -1, 144), 'l': (0, -1, 12), 'lb': (0, -1, 24)})
        elif sub_number == 12:
            directions.update({'rt': (1, 1, 133), 'r': (0, 1, 1), 'rb': (0, 1, 13)})
    elif 133 <= sub_number <= 144:
        directions.update({
            'lt': (1, -1, sub_number - 13),
            't': (0, 0, sub_number - 12),
            'rt': (0, 0, sub_number - 11),
            'lb': (-1, 0, sub_number - 133),
            'b': (-1, 0, sub_number - 132),
            'rb': (-1, 0, sub_number - 131)
        })
        if sub_number == 133:
            directions.update({'lt': (0, -1, 132), 'l': (0, -1, 144), 'lb': (-1, -1, 12)})
        elif sub_number == 144:
            directions.update({'rt': (0, 1, 121), 'r': (0, 1, 133), 'rb': (-1, 1, 1)})
    elif sub_number % 12 == 1:
        directions.update(
            {'lt': (0, -1, sub_number - 1), 'l': (0, -1, sub_number + 11), 'lb': (0, -1, sub_number + 23)})
    elif sub_number % 12 == 0:
        directions.update({'rt': (0, 1, sub_number - 23), 'r': (0, 1, sub_number - 11), 'rb': (0, 1, sub_number + 1)})

    nomenclatures = {
        direction: f"{chr(ord(zone) + dz)}-{map_number + dm}-{new_sub}"
        for direction, (dz, dm, new_sub) in directions.items()
    }
    nomenclatures['m'] = f'{zone}-{map_number}-{sub_number}'
    return nomenclatures


def calculate_50_000(zone: str, map_number: int, sub_number: int, sub_letter: str, *args, **kwargs):
    sub_letters = {
        'lt': {'Б': 'В', 'А': 'Г', 'В': 'Б', 'Г': 'А'},
        't': {'А': 'В', 'Б': 'Г', 'В': 'А', 'Г': 'Б'},
        'rt': {'А': 'Г', 'Б': 'В', 'В': 'Б', 'Г': 'А'},
        'l': {'А': 'Б', 'Б': 'А', 'В': 'Г', 'Г': 'В'},
        'r': {'А': 'Б', 'Б': 'А', 'В': 'Г', 'Г': 'В'},
        'lb': {'А': 'Г', 'Б': 'В', 'В': 'Б', 'Г': 'А'},
        'b': {'А': 'В', 'Б': 'Г', 'В': 'А', 'Г': 'Б'},
        'rb': {'А': 'Г', 'Б': 'В', 'В': 'Б', 'Г': 'А'}
    }
    directions = {
        'lt': (0, 0, sub_number),
        't': (0, 0, sub_number),
        'rt': (0, 0, sub_number),
        'l': (0, 0, sub_number),
        'r': (0, 0, sub_number),
        'lb': (0, 0, sub_number),
        'b': (0, 0, sub_number),
        'rb': (0, 0, sub_number)
    }
    if sub_letter == 'А':
        directions.update({
            'lt': (0, 0, sub_number - 13),
            't': (0, 0, sub_number - 12),
            'rt': (0, 0, sub_number - 12),
            'l': (0, 0, sub_number - 1),
            'lb': (0, 0, sub_number - 1),
        })
    elif sub_letter == 'Б':
        directions.update({
            'lt': (0, 0, sub_number - 12),
            't': (0, 0, sub_number - 12),
            'rt': (0, 0, sub_number - 11),
            'r': (0, 0, sub_number + 1),
            'rb': (0, 0, sub_number + 1)
        })
    elif sub_letter == 'В':
        directions.update({
            'lt': (0, 0, sub_number - 1),
            'l': (0, 0, sub_number - 1),
            'lb': (0, 0, sub_number + 11),
            'b': (0, 0, sub_number + 12),
            'rb': (0, 0, sub_number + 12)
        })
    elif sub_letter == 'Г':
        directions.update({
            'rt': (0, 0, sub_number + 1),
            'r': (0, 0, sub_number + 1),
            'lb': (0, 0, sub_number + 12),
            'b': (0, 0, sub_number + 12),
            'rb': (0, 0, sub_number + 13)
        })
    else:
        raise InvalidNomenclature

    if 1 <= sub_number <= 12:
        if sub_letter in ('А', 'Б'):
            directions.update({
                'lt': (1, 0, sub_number + 131 if sub_letter == 'А' else 132),
                't': (1, 0, sub_number + 132),
                'rt': (1, 0, sub_number + 132 if sub_letter == 'А' else 133),
            })
        if sub_number == 1 and sub_letter == 'А':
            directions.update({
                'lt': (1, -1, 144),
                'l': (0, -1, 12),
                'lb': (0, -1, 12)
            })
        elif sub_number == 1 and sub_letter == 'В':
            directions.update({
                'lt': (0, -1, 12),
                'l': (0, -1, 12),
                'lb': (0, -1, 24)
            })
        elif sub_number == 12 and sub_letter == 'Б':
            directions.update({
                'rt': (1, 1, 133),
                'r': (0, 1, 1),
                'rb': (0, 1, 1)
            })
        elif sub_number == 12 and sub_letter == 'Г':
            directions.update({
                'rt': (0, 1, 1),
                'r': (0, 1, 1),
                'rb': (0, 1, 13)
            })
    elif 133 <= sub_number <= 144:
        if sub_letter in ('В', 'Г'):
            directions.update({
                'lb': (-1, 0, sub_number - 133 if sub_letter == 'В' else 132),
                'b': (-1, 0, sub_number - 132),
                'rb': (-1, 0, sub_number - 132 if sub_letter == 'В' else 131)
            })
        if sub_number == 133 and sub_letter == 'В':
            directions.update({
                'lt': (0, -1, 144),
                'l': (0, -1, 144),
                'lb': (-1, -1, 12)
            })
        elif sub_number == 133 and sub_letter == 'А':
            directions.update({
                'lt': (0, -1, 132),
                'l': (0, -1, 144),
                'lb': (0, -1, 144)
            })
        elif sub_number == 144 and sub_letter == 'Г':
            directions.update({
                'rt': (0, 1, 133),
                'r': (0, 1, 133),
                'rb': (-1, 1, 1)
            })
        elif sub_number == 144 and sub_letter == 'Б':
            directions.update({
                'rt': (0, 1, 121),
                'r': (0, 1, 133),
                'rb': (0, 1, 133)
            })
    elif (
            (sub_number % 12 == 1 and sub_letter in ('А', 'В'))
            or (sub_number == 1 and sub_letter == 'В')
            or (sub_number == 133 and sub_letter == 'A')
    ):
        directions.update({
            'lt': (0, -1, sub_number + -1 if sub_letter == 'А' else 11),
            'l': (0, -1, sub_number + 11),
            'lb': (0, -1, sub_number + 11 if sub_letter == 'А' else 23)
        })
    elif (
            (sub_number % 12 == 0 and sub_letter in ('Б', 'Г'))
            or (sub_number == 12 and sub_letter == 'Г')
            or (sub_number == 144 and sub_letter == 'Б')
    ):
        directions.update({
            'rt': (0, 1, sub_number + -23 if sub_letter == 'Б' else -11),
            'r': (0, 1, sub_number - 11),
            'rb': (0, 1, sub_number + -11 if sub_letter == 'Б' else 1)
        })

    nomenclatures = {
        direction: f"{chr(ord(zone) + dz)}-{map_number + dm}-{new_sub}-{sub_letters[direction][sub_letter]}"
        for direction, (dz, dm, new_sub) in directions.items()
    }
    nomenclatures['m'] = f"{zone}-{map_number}-{sub_number}-{sub_letter}"
    return nomenclatures


def get_neighbor_nomenclature(zone: str, map_number: int, sub_number: str, sub_letter=None):
    if len(zone) != 1:
        raise InvalidNomenclature
    if sub_number.isalpha() and bool(re.search('[а-гА-Г]', sub_number)):
        return calculate_500_000(zone=zone, map_number=map_number, sub_number=sub_number, sub_letter=sub_letter)
    elif sub_number.isalpha() and bool(re.search('[a-zA-Z]', sub_number)):
        return calculate_200_000(zone=zone, map_number=map_number, sub_number=sub_number, sub_letter=sub_letter)
    elif sub_number.isdigit() and sub_letter is None:
        return calculate_100_000(zone=zone, map_number=map_number, sub_number=sub_number, sub_letter=sub_letter)
    elif sub_letter:
        return calculate_50_000(zone=zone, map_number=map_number, sub_number=int(sub_number), sub_letter=sub_letter)
    else:
        raise InvalidNomenclature


def get_nomenclature_table(main_nomenclature: str):
    zone, map_number, sub_part, sub_letter = parse_nomenclature(main_nomenclature)
    try:
        map_number = int(map_number)
    except ValueError:
        raise InvalidNomenclature

    neighbors = get_neighbor_nomenclature(
        zone.upper(),
        map_number,
        sub_part.upper(),
        sub_letter.upper() if sub_letter else None
    )

    table_rows = [
        html.Tr([html.Td(neighbors['lt']), html.Td(neighbors['t']), html.Td(neighbors['rt'])]),
        html.Tr([html.Td(neighbors['l']), html.Td(neighbors['m']), html.Td(neighbors['r'])]),
        html.Tr([html.Td(neighbors['lb']), html.Td(neighbors['b']), html.Td(neighbors['rb'])]),
    ]

    return dbc.Table([html.Tbody(table_rows)], bordered=True, className='mt-3')
