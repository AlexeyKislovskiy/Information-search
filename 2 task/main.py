import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import requests
from bs4 import BeautifulSoup

# Загрузка необходимых nltk модулей
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Загрузка списка стоп-слов, чтобы удалить ненужные союзы, предлоги
stop_words = set(stopwords.words('english'))


# Функция, проверяющая, что в строке содержатся только символы английского алфавита
def only_english_letters(string):
    match = re.match("^[A-Za-z]*$", string)
    return match is not None


# Функция для извлечения токенов из текста
def extract_tokens(text):
    tokens = word_tokenize(text.lower())
    # Удаление мусорных токенов и токенов из списка стоп-слов (союзы, предлоги)
    cleaned_tokens = [token for token in tokens if
                      only_english_letters(token) and len(token) > 2 and token not in stop_words]
    return list(set(cleaned_tokens))


# Функция для лемматизации токенов
def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = {}
    for token in tokens:
        lemma = lemmatizer.lemmatize(token)
        if lemma not in lemmatized_tokens:
            lemmatized_tokens[lemma] = []
        lemmatized_tokens[lemma].append(token)
    return lemmatized_tokens


def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


# Считывание страниц и удаление HTML тегов
clean_text = ""
for i in range(100):
    html_text = read_file(f'../1 task/pages/page{i + 1}.txt')
    clean_text += BeautifulSoup(html_text, "lxml").get_text(separator=" ")

# Извлечение токенов
extracted_tokens = extract_tokens(clean_text)

# Лемматизация токенов
lemmatized_tokens = lemmatize_tokens(extracted_tokens)

# Запись токенов в файл
with open('tokens.txt', 'w', encoding='utf-8') as file:
    for token in extracted_tokens:
        file.write(f"{token}\n")

# Запись лемматизированных токенов в файл
with open('lemmatized_tokens.txt', 'w', encoding='utf-8') as file:
    for lemma, tokens_list in lemmatized_tokens.items():
        file.write(f"{lemma} {' '.join(tokens_list)}\n")
