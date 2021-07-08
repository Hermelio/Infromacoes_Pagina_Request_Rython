from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    meus_resultados = search_news({"title": title.title()})
    return [(res["title"], res["url"]) for res in meus_resultados]


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        meus_resultados = search_news({"timestamp": {"$regex": date}})
        return [(res["title"], res["url"]) for res in meus_resultados]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    meus_resultados = search_news(
        {"sources":
            {"$regex": source, "$options": "i"}})
    return [(res["title"], res["url"]) for res in meus_resultados]


# Requisito 9
def search_by_category(category):
    meus_resultados = search_news({"categories": {
      "$regex": category, "$options": "i"
      }})
    return [(res["title"], res["url"]) for res in meus_resultados]
