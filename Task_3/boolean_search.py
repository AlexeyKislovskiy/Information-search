from Task_2.lemma_helper import lemmatize_word

# Считывание инвертированного индекса в словарь
inverted_index = {}
with open("inverted_index.txt", "r", encoding='utf-8') as file:
    for line in file:
        data = line.strip().split()
        word = data[0]
        pages = [int(page) for page in data[1:]]
        inverted_index[word] = pages


# Функция для поиска документов, содержащих данное слово (или его форму)
def find_pages(word):
    lemma = lemmatize_word(word)
    if lemma not in inverted_index:
        return set()
    return set(inverted_index[lemma])


# Функция для логического NOT
def not_pages(pages):
    all_pages = set(range(1, 101))
    return all_pages - pages


# Функция для логического AND
def and_pages(pages1, pages2):
    return pages1 & pages2


# Функция для логического OR
def or_pages(pages1, pages2):
    return pages1 | pages2


# Функция, возвращающая ссылку на страницу по ее номеру
def get_url_by_number(n):
    file = open('../Task_1/index.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    return lines[n - 1].split(': ')[1].strip()


# Функция для преобразования строкового запроса в список для дальнейшей работы
def query_to_list(query):
    query_symbols = ['(', ')', '&', '|', '!']
    query = query.lower()
    query = ' ' + query + ' '
    query = query.replace('(', ' ( ')
    query = query.replace(')', ' ) ')
    # Преобразуем операторы в виде слов в символы
    query = query.replace(' and ', ' & ')
    query = query.replace(' or ', ' | ')
    query = query.replace(' not ', ' ! ')
    query = query.replace(' ', '')
    query_list = []
    word = ''
    # Операторы переносим в список как есть, а слова меняем на соответствующие им множества с номерами страниц
    for c in query:
        if c in query_symbols:
            if word:
                query_list.append(find_pages(word))
            word = ''
            query_list.append(c)
        else:
            word += c
    if word:
        query_list.append(find_pages(word))
    return query_list


# Функция для поиска документов по преобразованному списку
def find_by_query(query_list):
    # Поиск самой правой открывающейся скобки
    bracket1 = max((index for index, el in enumerate(query_list) if el == '('), default=None)
    # Если скобка есть
    if bracket1 is not None:
        # Ищем соответствующую ей закрывающуюся скобку, если ее нет, то выражение некорректно
        try:
            bracket2 = query_list.index(')', bracket1)
        except ValueError:
            return None
        # Рекурсивно вычисляем значение в скобках и вставляем в исходный лист
        result_set = find_by_query(query_list[bracket1 + 1:bracket2])
        if result_set is None:
            return None
        del query_list[bracket1:bracket2]
        query_list[bracket1] = result_set
        return find_by_query(query_list)
    # Если скобок нет, то порядок действий следующий: NOT>AND>OR
    else:
        # Проверяем, не осталось ли лишних закрывающихся скобок
        bracket = max((index for index, el in enumerate(query_list) if el == ')'), default=None)
        if bracket is not None:
            return None
        # Ищем есть ли оператор NOT
        try:
            not_symbol = query_list.index('!')
            # Может ли этот оператор стоять на данном месте
            if len(query_list) != (not_symbol + 1) and isinstance(query_list[not_symbol + 1], set):
                result_set = not_pages(query_list[not_symbol + 1])
                if result_set is None:
                    return None
                # Вставляем вычисленное значение в лист и продолжаем рекурсию
                del query_list[not_symbol]
                query_list[not_symbol] = result_set
                return find_by_query(query_list)
            else:
                return None
        except ValueError:
            # Ищем есть ли оператор AND
            try:
                and_symbol = query_list.index('&')
                # Может ли этот оператор стоять на данном месте
                if len(query_list) != (and_symbol + 1) and and_symbol != 0 and \
                        isinstance(query_list[and_symbol + 1], set) and isinstance(query_list[and_symbol - 1], set):
                    result_set = and_pages(query_list[and_symbol + 1], query_list[and_symbol - 1])
                    if result_set is None:
                        return None
                    # Вставляем вычисленное значение в лист и продолжаем рекурсию
                    del query_list[and_symbol:and_symbol + 2]
                    query_list[and_symbol - 1] = result_set
                    return find_by_query(query_list)
                else:
                    return None
            except ValueError:
                # Ищем есть ли оператор OR
                try:
                    or_symbol = query_list.index('|')
                    # Может ли этот оператор стоять на данном месте
                    if len(query_list) != (or_symbol + 1) and or_symbol != 0 and \
                            isinstance(query_list[or_symbol + 1], set) and isinstance(query_list[or_symbol - 1], set):
                        result_set = or_pages(query_list[or_symbol + 1], query_list[or_symbol - 1])
                        if result_set is None:
                            return None
                        # Вставляем вычисленное значение в лист и продолжаем рекурсию
                        del query_list[or_symbol:or_symbol + 2]
                        query_list[or_symbol - 1] = result_set
                        return find_by_query(query_list)
                    else:
                        return None
                # Случай, когда операторов больше нет. Либо ответ вычислен, либо выражение некорректно
                except ValueError:
                    if len(query_list) == 1 and isinstance(query_list[0], set):
                        return query_list[0]
                    else:
                        return None


query = input("Введите выражение для поиска: ")
# Пример выражения — (face and not (london or paper)) or turtle
pages = find_by_query(query_to_list(query))
if pages is not None:
    for page in pages:
        print(get_url_by_number(page))
else:
    print("Заданное выражение некорректно")
