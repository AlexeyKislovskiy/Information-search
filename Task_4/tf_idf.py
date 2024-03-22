import math


# Функция для вычисления tf данного слова в данном документе
def calculate_tf(word, document_words):
    word_count = document_words.count(word)
    return word_count / len(document_words)


# Функция для вычисления tf всех слов в данном документе
def calculate_tf_for_all(document_words):
    unique_words = list(set(document_words))
    tfs = {}
    for word in unique_words:
        tfs[word] = calculate_tf(word, document_words)
    return tfs


# Функция для вычисления idf данного слова
def calculate_idf(word, documents):
    documents_with_word = sum([1 for document in documents if word in document])
    return math.log10(len(documents) / documents_with_word)
