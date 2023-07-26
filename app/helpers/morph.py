import pymorphy3
from nltk.tokenize import word_tokenize

morph = pymorphy3.MorphAnalyzer()


def morphing(tag):
    tokens = word_tokenize(tag)  # При создании тэга из нескольких слов, делим его на слова
    tokens = [word.lower() for word in tokens]  # Приводим к нижнему регистру
    words = [word for word in tokens if word.isalpha()]  # Выделяем только слова
    morphed = [morph.normal_forms(word)[0] for word in words]  # Приводим к начальной форме
    final_tag = ' '.join(morphed)  # Создаём тэг в строковом формате
    return final_tag
