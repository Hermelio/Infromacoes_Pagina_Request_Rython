import requests
from time import sleep
from parsel import Selector
from database import create_news


# Requisito 1
def fetch(url):
    sleep(1)
    try:
        dados_html = requests.get(url, timeout=3)
    except requests.RequestException:
        return None
    else:
        if dados_html.status_code != 200:
            return None
        return dados_html.text


# Requisito 2
def scrape_noticia(html_content):
    seletor = Selector(text=html_content)
    url = seletor.css('link[rel="canonical"]::attr(href)').get()
    texto = '.tec--article__header__title#js-article-title::text'
    title = seletor.css(texto).get()
    timestamp = seletor.css('#js-article-date::attr(datetime)').get()
    texto = '.tec--author__info__link::text'
    writer = seletor.css(texto).get()
    texto = '.tec--toolbar__item::text'
    shares_count = seletor.css(texto).re_first(r'/d+') or '0'
    '''regex firts match
    https://stackoverflow.com/questions
    /38579725/return-string-with-first-match-regex'''
    comments_count = seletor.css('#js-comments-btn::attr(data-count)').get()
    summary = seletor.css('.tec--article__body p:first-child *::text').getall()
    summary_correct = ''.join(summary)
    '''concatenando strings
    https://stackoverflow.com/questions/497765/python-string-
    joinlist-on-object-array-rather-than-string-array'''
    sources = seletor.css(".z--mb-16 a::text").getall()
    categories = seletor.css("#js-categories a::text").getall()
    '''Map in python usado no source e categoria
    https://mathalope.co.uk/2017/07/01/what-is-the-equivalent-of
    -javascript-map-filter-and-reduce-functions-in-python/'''
    return{
        "url": url,
        "title": title.title() if title else "",
        "timestamp": timestamp,
        "writer": writer.strip() if writer else None,
        "shares_count": int(shares_count),
        "comments_count": int(comments_count or "0"),
        "summary": summary_correct,
        "sources": [source.strip() for source in sources],
        "categories": [category.strip() for category in categories],
    }


# Requisito 3
def scrape_novidades(html_content):
    seletor = Selector(html_content)
    meu_texto = '.tec--list__item .tec--card__title__link::attr(href)'
    minhas_urls = seletor.css(meu_texto).getall()
    return minhas_urls if minhas_urls else []


# Requisito 4
def scrape_next_page_link(html_content):
    seletor = Selector(html_content)
    meu_texto = '.tec--btn--lg::attr(href)'
    next_page = seletor.css(meu_texto).get()
    return next_page if next_page else None


# Requisito 5
# flake8: noqa: C901
def get_tech_news(amount):
    amount = int(amount)
    noticias = 0
    noticias_retornaveis = []
    global url
    conferindo = fetch(url)
    conferindo_novidade = scrape_novidades(conferindo)

    if not conferindo_novidade:
        raise Exception("Couldnt find anything in there.")
    if len(conferindo_novidade) >= amount:
        for a in conferindo_novidade:
            if noticias < amount:
                html_noticia = fetch(a)
                dict_noticia = scrape_noticia(html_noticia)
                noticias_retornaveis.append(dict_noticia)
            noticias += 1
        create_news(noticias_retornaveis)
        return noticias_retornaveis

    tamanho_url = amount - len(conferindo_novidade)

    for a in conferindo_novidade:
        html_noticia = fetch(a)
        dict_noticia = scrape_noticia(html_noticia)
        noticias_retornaveis.append(dict_noticia)
        noticias += 1

    print(noticias)
    next_page = scrape_next_page_link(conferindo)
    proxima_pagina = fetch(next_page)
    lista_proxima_pagina = scrape_novidades(proxima_pagina)

    for b in lista_proxima_pagina:
        if tamanho_url > 0:
            html_noticia = fetch(b)
            dict_noticia = scrape_noticia(html_noticia)
            noticias_retornaveis.append(dict_noticia)
            tamanho_url -= 1

    create_news(noticias_retornaveis)
    return noticias_retornaveis
