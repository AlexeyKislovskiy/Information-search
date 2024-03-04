from Task_2.lemma_helper import get_lemmas_from_page, get_all_lemmas

# Заполнение списка лемм для каждой страницы
lemma_list = []
for i in range(100):
    lemma_list.append(get_lemmas_from_page(i + 1))


# Функция для получения всех страниц, содержащих данную лемму
def get_all_pages_with_lemma(lemma):
    page_list = []
    n = 1
    for page in lemma_list:
        if lemma in page:
            page_list.append(n)
        n += 1
    return page_list


# Запись инвертированного индекса в файл
with open('inverted_index.txt', 'w', encoding='utf-8') as file:
    lemmas = get_all_lemmas()
    for lemma in lemmas:
        page_list = get_all_pages_with_lemma(lemma)
        file.write(f"{lemma} {' '.join(map(str, page_list))}\n")
