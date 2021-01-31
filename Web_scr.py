import requests
from bs4 import BeautifulSoup

"""Необходимо парсить страницу со свежими статьями (вот эту) и выбирать те статьи, 
в которых встречается хотя бы одно из ключевых слов (эти слова определяем в начале скрипта). 
Поиск вести по всей доступной preview-информации (это информация, доступная непосредственно с текущей страницы). 
Вывести в консоль список подходящих статей в формате: <дата> - <заголовок> - <ссылка>."""

KEYWORDS = ['максвелла','react','дыры']  #для проверки 1-ой функции
KEYWORDS = ['теория','визуал','маршрутизатор ']   #для проверки 2-ой функции

def search_by_preview(link_):
  response = requests.get(link_)
  soup = BeautifulSoup(response.text,'html.parser')
  posts = soup.find_all('article',class_='post')
  post_list = []
  for post in posts:
    text_list = []
    text_list.append(post.text.strip().lower())
    for text in text_list:
      if any ((elem in text.split() for elem in KEYWORDS)):
        data_post = post.find('span', class_ = 'post__time').text.strip()
        link = post.find('a',class_ = 'post__title_link')
        link_link = link.attrs.get('href')
        link_text = link.text.strip()
        post_list.append(f'{data_post} - {link_text} - {link_link}')
        break
  return post_list



"""Дополнительное (необязательное) задание
Улучшить скрипт так, чтобы он анализировал не только preview-информацию статьи, но и весь текст статьи целиком.
Для этого потребуется получать страницы статей и искать по тексту внутри этой страницы."""

def full_article_search(link_):
  response = requests.get(link_)
  soup = BeautifulSoup(response.text,'html.parser')
  posts = soup.find_all('a',class_='btn btn_x-large btn_outline_blue post__habracut-btn')
  post_list = []
  for post in posts:
    link = post.attrs.get('href')
    response_link = requests.get(link)
    soup_link = BeautifulSoup(response_link.text,'html.parser')
    articles = soup_link.find_all('div',class_='post__wrapper')
    for article in articles:
      article_list = []
      article_list.append(article.text.strip().lower())
      for artic in article_list:
        if any ((elem in artic.split() for elem in KEYWORDS)):
          data_post = article.find('span', class_ = 'post__time').text.strip()
          link_text = article.find('span',class_ = 'post__title-text').text.strip()
          post_list.append(f'{data_post} - {link_text} - {link}')
  return post_list


if __name__ == '__main__':
    print(search_by_preview('https://habr.com/ru/all/'))
    print(full_article_search('https://habr.com/ru/all/'))