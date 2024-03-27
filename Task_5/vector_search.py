import math
from Task_2.lemma_helper import extract_tokens, lemmatize_word
from Task_4.tf_idf import calculate_tf_for_all


# Функция для считывания инвертированного индекса
def read_inverted_index():
    inverted_index = {}
    with open('../Task_3/inverted_index.txt', 'r', encoding='utf-8') as file:
        for line in file:
            tokens = line.strip().split()
            word = tokens[0]
            docs = [int(doc) for doc in tokens[1:]]
            inverted_index[word] = docs
    return inverted_index


# Функция для считывания tf_idf документа под номером n
def read_tf_idf_for_document(n):
    tf_idfs = {}
    with open(f'../Task_4/lemmas/lemma{n}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            tokens = line.strip().split()
            word = tokens[0]
            tf_idf = tokens[2]
            tf_idfs[word] = tf_idf
    return tf_idfs


# Функция для подсчета вектора документа под номером n
def calculate_vector_for_document(n, inverted_index: dict):
    vector = {}
    for word in inverted_index.keys():
        vector[word] = 0
    tf_idfs = read_tf_idf_for_document(n)
    for word in tf_idfs.keys():
        vector[word] = float(tf_idfs[word])
    return list(vector.values())


# Функция для подсчета векторов всех документов
def calculate_vector_for_all_documents(inverted_index: dict):
    vectors = {}
    for i in range(1, 101):
        vectors[i] = calculate_vector_for_document(i, inverted_index)
    return vectors


# Функция для подсчета вектора запроса
def calculate_vector_for_query(query, inverted_index: dict):
    vector = {}
    for word in inverted_index.keys():
        vector[word] = 0
    query_lemmas = [lemmatize_word(token) for token in (extract_tokens(query))]
    tfs = calculate_tf_for_all(query_lemmas)
    for word in tfs:
        if word in inverted_index.keys():
            idf = math.log10(100 / len(inverted_index[word]))
            vector[word] = tfs[word] * idf
    return list(vector.values())


# Функция для вычисления косинусного расстояния
def cosine_similarity(vector1, vector2):
    dot_product = sum(x * y for x, y in zip(vector1, vector2))
    norm_vector1 = math.sqrt(sum(x ** 2 for x in vector1))
    norm_vector2 = math.sqrt(sum(x ** 2 for x in vector2))
    if norm_vector1 == 0 or norm_vector2 == 0:
        return 0
    return dot_product / (norm_vector1 * norm_vector2)


# Функция, возвращающая ссылку на страницу по ее номеру
def get_url_by_number(n):
    file = open('../Task_1/index.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    return lines[n - 1].split(': ')[1].strip()


# Функция для поиска топ n релевантных документов по данному запросу
def find_top_n(query, n, inverted_index, vectors):
    query_vector = calculate_vector_for_query(query, inverted_index)
    similarities = {}
    for number, vector in vectors.items():
        similarities[number] = cosine_similarity(query_vector, vector)
    sorted_similarities = {get_url_by_number(k): v for k, v in
                           sorted(similarities.items(), key=lambda item: item[1], reverse=True)}
    return list(sorted_similarities.items())[:n]
