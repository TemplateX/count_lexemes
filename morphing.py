import re
import pymorphy2
from morph_excel import lemmas_to_excel


def count_morphed_usages(filename: str, file_id: str):
    """
    :param file_id: uuid background task. Используется в названии файла
    :param filename: Путь до файла с текстом
    :return: Ничего
    """
    unique_lemmas = set()
    lemmas_strings = []

    with open(filename, "r", encoding="utf-8") as f:
        morph = pymorphy2.MorphAnalyzer()
        for line in f:
            line = line.strip()
            if line != "":
                line = re.sub(r"[^a-zA-Zа-яА-ЯёЁ-]", " ", line).split()
                temp = []
                for i in line:
                    first_similar = morph.parse(i)[0]
                    temp.append(first_similar.normal_form)
                lemmas_strings.append(temp)
                unique_lemmas.update(set(temp))

    lemmas_count_dict = dict()

    for uniq in unique_lemmas:
        lemmas_count_dict[uniq] = []
        for string in lemmas_strings:
            if uniq in string:
                lemmas_count_dict[uniq] += [string.count(uniq)]
            else:
                lemmas_count_dict[uniq] += [0]
        lemmas_count_dict[uniq] += [sum(lemmas_count_dict[uniq])]

    lemmas_to_excel(lemmas_count_dict, file_id)
    print(f"Закончили разбор{file_id}")
