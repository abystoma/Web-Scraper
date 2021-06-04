import requests
from string import punctuation
from bs4 import BeautifulSoup
import os
from os import F_OK, access,mkdir
import string

name = []

def retrieve_page_content(url: str) -> bytes:
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    else:
        print(f"The URL returned {r.status_code}!")


def retrieve_article_text(content: bytes) -> str:

    parsed = BeautifulSoup(content, 'html.parser')
    article_body = parsed.find('div', class_='article__body')
    article_item_body = parsed.find('div', class_='article-item__body')
    article_another = parsed.find('div',class_ = 'c-article-body u-clearfix')
    article_content = article_body if article_body is not None else article_item_body
    article_content = article_another if article_another is not None else article_content
    return article_content

def fix_title(title: str) -> str:
    stripped_title = str(title).strip()
    revised_title = stripped_title.maketrans(' ', '_', string.punctuation)
    return stripped_title.translate(revised_title)

def create_folder(folder: str) -> None :
    if not access(folder, F_OK):
        mkdir(folder)
        os.chdir(folder)
        #print('The current working directory is', os.getcwd())
    else:
        print(f"Directory {folder} already exists")

def next_page(soup: str, page: int) -> str:
    n_page = soup.find_all('li',attrs={'class':'c-pagination__item'})
    for n in n_page:
        if n.get('data-page') == str(page):
            #print(f'Page Number: {page}')
            pg = n.find('a',attrs={'class':'c-pagination__link'})
            site = f"https://www.nature.com{pg.get('href')}"
            r = requests.get(site)
            #print(site)
            return BeautifulSoup(r.content, 'html.parser')

def collect_articles(soup: str, total_page: int, page_count: int, user_type: str) -> None:

    if page_count > total_page:
        return
    else:
        articles = soup.find_all('article')
        create_folder(f'Page_{page_count}')
        for article in articles:
            try:
                article_type = article.find('span', class_="c-meta__type").text.strip()
            except TypeError:
                pass
            if article_type == user_type:
                article_information = article.find("a", attrs={'data-track-action': 'view article'})
                url = f"https://www.nature.com{article_information.get('href')}"

                page_content = retrieve_page_content(url)
                parsed = BeautifulSoup(page_content, 'html.parser')
                title = article_information.text
                text = retrieve_article_text(page_content)
                new_title = fix_title(title)
                try:
                    file = open(f'{new_title}.txt', 'w',encoding='utf-8') 
                    file.write(text.text.strip())
                    #name.append(file.name)
                except AttributeError:
                    pass
        os.chdir(os.path.dirname(os.getcwd()))
        #print('The current working directory is', os.getcwd())
        page_count = page_count + 1
        collect_articles(next_page(soup,page_count), total_page, page_count, user_type)


def main() -> None:
    website = "https://www.nature.com/nature/articles"
    pages = int(input("Enter the number of pages you want to scrape: "))
    article_type = input("Enter the type of article you want to scrape: ")
    r = requests.get(website, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        collect_articles(soup, pages, 1, article_type)
        #print(name)
        print("Content saved.")
    else:
        print(f"The URL returned {r.status_code}!")

main()



