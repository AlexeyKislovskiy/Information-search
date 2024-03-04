from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup


# Функция, проверяющая, что в строке содержатся только символы английского алфавита
def only_english_letters(string):
    match = re.match("^[A-Za-z]*$", string)
    return match is not None


# Функция для извлечения токенов из текста
def extract_tokens(text):
    # Загрузка списка стоп-слов, чтобы удалить ненужные союзы, предлоги
    stop_words = set(stopwords.words('english'))

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


# Функция для чтения содержимого файла
def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


# Функция для извлечения чистого текста без HTML тегов из страницы под номером n
def get_clean_text(n):
    html_text = read_file(f'../Task_1/pages/page{n}.txt')
    return BeautifulSoup(html_text, "lxml").get_text(separator=" ")


# Функция, возвращающая леммы из страницы с номером n
def get_lemmas_from_page(n):
    clean_text = get_clean_text(n)
    extracted_tokens = extract_tokens(clean_text)
    return lemmatize_tokens(extracted_tokens)


# Функция для получения всех лемм из файла
def get_all_lemmas():
    file = open('../Task_2/lemmatized_tokens.txt', 'r', encoding='utf-8')
    lemmas = file.readlines()
    return [lemma.split(' ', 1)[0] for lemma in lemmas]


# Функция для лематизации слова
def lemmatize_word(word):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word.lower())
