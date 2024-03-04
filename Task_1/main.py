import requests
import os
from lxml import html


# Функция для получения ссылок на страницы википедии про отдельные языки, получаемые с общей страницы со списком языков
def get_page_links():
    url = "https://en.wikipedia.org/wiki/Index_of_language_articles"
    page = requests.get(url)
    tree = html.fromstring(page.text)
    table_xpath = '//*[@id="mw-content-text"]/div[1]/table[3]/tbody'
    table = tree.xpath(table_xpath)
    links = table[0].xpath('.//a')
    links_set = set()
    for link in links:
        link_text = link.attrib['href']
        if link_text.startswith("/wiki/"):
            links_set.add('https://en.wikipedia.org' + link.attrib['href'])
    return links_set


# Создание папки для сохранения файлов, если её нет
if not os.path.exists('pages'):
    os.makedirs('pages')

# Получение контента по первым 100 ссылкам из множества и запись их в файлы
page_links = get_page_links()
link_number = 100
i = 1
saved_links = []
for page_link in page_links:
    content = requests.get(page_link).text
    filename = f'pages/page{i}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    saved_links.append(page_link)
    if i >= link_number:
        break
    i += 1

# Создание файла index.txt
with open('index.txt', 'w', encoding='utf-8') as index_file:
    i = 1
    for link in saved_links:
        index_file.write(f'{i}: {link}\n')
        i += 1
