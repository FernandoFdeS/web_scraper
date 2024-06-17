import requests
import pandas as pd
from classes.EditalFapesc import EditalFapesc
from bs4 import BeautifulSoup

# Para FAPESC (Investigar o motivo do request ser dolorasemente lento)
url = 'https://fapesc.sc.gov.br/category/chamadas-abertas'
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


numRequests=0
editais=[]
flag=True

while(flag):
    response = requests.get(url,headers=headers)
    numRequests = numRequests+1
    if response.status_code == 200:
        print("response")
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        div_conteudo = soup.find('div', class_='page-content')
        div_itens = div_conteudo.find_all('article', class_='post')
        for item in div_itens:
            a = item.find('a')
            p = item.find('p')
            edital_titulo = a.text.strip()
            edital_link = a['href']
            edital_resumo = p.text.strip()
            edital = EditalFapesc(edital_titulo,edital_resumo,edital_link)
            editais.append(edital)

        # Pegando proximo link
        nav_previous = soup.select_one('nav.pagination div.nav-previous a')
        if nav_previous:
            url = nav_previous['href']
        else:
            flag = False

print("Requests: "+str(requests))
# Para visualizar melhor o que a gente pegou do site até o momento vamos criar um xlsx simples
data = {
    'Título': [edital.titulo for edital in editais],
    'Resumo': [edital.resumo for edital in editais],
    'Link': [edital.link for edital in editais]
}

df = pd.DataFrame(data)
excel_filename = 'editais_fapesc.xlsx'
df.to_excel(excel_filename, index=False)
