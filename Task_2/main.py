import nltk
from Task_2.lemma_helper import get_clean_text, extract_tokens, lemmatize_tokens

# Загрузка необходимых nltk модулей
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Считывание страниц и удаление HTML тегов
clean_text = ""
for i in range(100):
    clean_text += get_clean_text(i + 1)

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
