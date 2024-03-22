import os

from Task_2.lemma_helper import extract_all_words, extract_all_lemmas
from Task_4.tf_idf import calculate_tf_for_all, calculate_idf

# Считывание всех слов и лемм
document_words = []
document_lemmas = []
for i in range(1, 101):
    document_words.append(extract_all_words(i))
    document_lemmas.append(extract_all_lemmas(i))

# Создание папок для сохранения файлов
if not os.path.exists('terms'):
    os.makedirs('terms')
if not os.path.exists('lemmas'):
    os.makedirs('lemmas')

# Вычисление tf-idf и запись их в файлы
for i in range(1, 101):
    terms_tf = calculate_tf_for_all(document_words[i - 1])
    lemmas_tf = calculate_tf_for_all(document_lemmas[i - 1])
    # Запись tf-idf для каждого термина из i документа
    with open(f'terms/term{i}.txt', 'w', encoding='utf-8') as file:
        for term, tf in terms_tf.items():
            idf = calculate_idf(term, document_words)
            tf_idf = tf * idf
            file.write(f"{term} {idf} {tf_idf}\n")
    # Запись tf-idf для каждой леммы из i документа
    with open(f'lemmas/lemma{i}.txt', 'w', encoding='utf-8') as file:
        for lemma, tf in lemmas_tf.items():
            idf = calculate_idf(lemma, document_lemmas)
            tf_idf = tf * idf
            file.write(f"{lemma} {idf} {tf_idf}\n")
