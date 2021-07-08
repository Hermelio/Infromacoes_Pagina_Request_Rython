import sys
from scraper import get_tech_news
from analyzer.search_engine import (
  search_by_title,
  search_by_date,
  search_by_source,
  search_by_category
)
from analyzer.ratings import top_5_categories, top_5_news


# Requisito 12
# flake8: noqa: C901
def analyzer_menu():
    while True:
        print("Selecione uma das opções a seguir:")
        print(' 0 - Popular banco;')
        print(' 1 - Buscar notícias por título;')
        print(' 2 - Buscar notícias por data;')
        print(' 3 - Buscar notícias por fonte;')
        print(' 4 - Buscar notícias por categoria;')
        print(' 5 - Listar top 5 noticias;')
        print(' 6 - Listar top 5 categorias;')
        print(' 7 - Sair.')
        entrada = input()

        if entrada == '0':
            print('Digite quantas notícias serão buscadas:')
            quantidade_noticias = input()
            get_tech_news(int(quantidade_noticias))
        elif entrada == '1':
            print('Digite o título:')
            titulo = input()
            print(search_by_title(titulo))
        elif entrada == '2':
            print('Digite a data no formato aaaa-mm-dd:')
            data = input()
            print(search_by_date(data))
        elif entrada == '3':
            print('Digite a fonte:')
            fonte = input()
            print(search_by_source(fonte))
        elif entrada == '4':
            print('Digite a categoria:')
            categoria = input()
            print(search_by_category(categoria))
        elif entrada == '5':
            print(top_5_news())
        elif entrada == '6':
            print(top_5_categories())
        elif entrada == '7':
            print('Encerrando script')
            break
        else:
            sys.stderr.write('Opção inválida\n')
        print()
        print("Aperte Enter para voltar para o menu")
        input()


if __name__ == "__main__":
    analyzer_menu()
