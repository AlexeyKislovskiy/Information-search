from Task_5.vector_search import find_top_n, read_inverted_index, calculate_vector_for_all_documents

inverted_index = read_inverted_index()
vectors = calculate_vector_for_all_documents(inverted_index)
while True:
    query = input('Введите запрос для поиска\n')
    n = int(input('Введите количество документов, которые вы хотите увидеть\n'))
    print(find_top_n(query, n, inverted_index, vectors))
