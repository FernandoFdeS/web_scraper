import requests
import time
import pandas as pd
from classes.EditalFinep import EditalFinep
from bs4 import BeautifulSoup

# Para FINEP, futuramente estruturar melhor, dividir em classes de acordo com o orgão de fomento.
baseUrl =  'http://www.finep.gov.br'
url = 'https://www.finep.gov.br/chamadas-publicas?situacao=aberta&start='
headers = {
    'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

pg = 0 # Index usado pra navegar nas paginas do site da FINEP (vai após o 'start=' na url)
numRequests=0
editais=[]
flag=True

# Loop
while(flag):
    response = requests.get(url+str(pg),headers=headers)
    numRequests = numRequests+1
    print(url+str(pg),numRequests)
    pg = pg+10
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        div_conteudo = soup.find('div', id='conteudoChamada')

        divs_item = div_conteudo.find_all('div', class_='item') # Pegando apenas a div onde temos os editais
        if divs_item: # Existem editais nessa página, seguimos o scraping
            for div_item in divs_item:
                edital_data_publicacao = ''
                edital_prazo = 'Fluxo contínuo'
                edital_fonte = ''
                edital_publico_alvo = ''
                edital_tema = ''

                html_data_publicacao=div_item.find('div',class_='data_pub')
                if html_data_publicacao:
                    edital_data_publicacao = html_data_publicacao.find('span').text.strip()

                html_prazo=div_item.find('div',class_='prazo')
                if html_prazo:
                    edital_prazo = html_prazo.find('span').text.strip()
                
                html_fonte=div_item.find('div',class_='fonte')
                if html_fonte:
                    edital_fonte = html_fonte.find('span').text.strip()

                html_publico_alvo=div_item.find('div',class_='publico')
                if html_publico_alvo:
                    edital_publico_alvo = html_publico_alvo.find('span').text.strip()
                
                html_tema=div_item.find('div',class_='tema')
                if html_tema:
                    edital_tema = html_tema.find('span').text.strip()

                h3 = div_item.find('h3')
                a = h3.find('a')
                edital_titulo = a.text.strip()
                edital_link = a['href']

                edital = EditalFinep(
                    edital_titulo,
                    edital_data_publicacao,
                    edital_prazo,
                    edital_fonte,
                    edital_publico_alvo,
                    edital_tema,
                    baseUrl+edital_link
                )

                editais.append(edital)
        else: # Não tem mais editais, paramos tudo.
            print("Acabaram os editais!")
            flag=False
            break
  
    else:
        print(f'Erro ao acessar a página: {response.status_code}')

print("Quantidade de editais: "+str(len(editais)))
print("Requests: "+ str(numRequests))

# Para visualizar melhor o que a gente pegou do site até o momento vamos criar um xlsx simples
data = {
    'Título': [edital.titulo for edital in editais],
    'Data de Publicação': [edital.data_publicacao for edital in editais],
    'Data Limite': [edital.data_limite for edital in editais],
    'Fonte': [edital.fonte for edital in editais],
    'Público-alvo': [edital.publico_alvo for edital in editais],
    'Tema': [edital.tema for edital in editais],
    'Link': [edital.link for edital in editais]
}

df = pd.DataFrame(data)
excel_filename = 'editais_finep.xlsx'
df.to_excel(excel_filename, index=False)