import requests
import time
import pandas as pd
from classes.EditalFapesp import EditalFapesp
from bs4 import BeautifulSoup

# Para FAPESP. Esse site é extremamente mal estruturado, as informações de area, modalidade e datas não estão dentro de nenhuma tag.
url = 'https://fapesp.br/chamadas/'
headers = {
    'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

numRequests=0
editais=[]

response = requests.get(url,headers=headers)
numRequests = numRequests+1
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    div_conteudo = soup.find('div', class_='accordion__item')
    for h3 in div_conteudo.find_all('h3'):
    
        a = h3.find('a')       
        edital_titulo = a.text.strip()
        edital_link = a['href']
        #print(edital_titulo,edital_link)
        edital_data_limite = ''
        edital_area = ''
        edital_modalidade = ''

        data_limite_tag = h3.next_sibling
        data_limite_text = data_limite_tag.strip()
        edital_data_limite = data_limite_text.split(":")[1].strip()

        area_tag = data_limite_tag.find_next_sibling()
        area_tag_text = area_tag.next_sibling
        area_text = area_tag_text.strip()
        edital_area=area_text.split(":")[1].strip()

        modalidade_tag = area_tag.find_next_sibling()
        modalidade_tag_text = modalidade_tag.next_sibling
        modalidade_text = modalidade_tag_text.strip()
        edital_modalidade = modalidade_text.split(":")[1].strip()

        edital =EditalFapesp(
            edital_titulo,
            edital_data_limite,
            edital_area,
            edital_modalidade,
            edital_link
        )

        editais.append(edital)

for edital in editais:
    print(edital)

print(len(editais))

# Criando o xlsx com o resultado dos queridissimos editais
data = {
    'Título': [edital.titulo for edital in editais],
    'Data Limite': [edital.data_limite for edital in editais],
    'Modalidade': [edital.modalidade for edital in editais],
    'Área': [edital.area for edital in editais],
    'Link': [edital.link for edital in editais]
}

df = pd.DataFrame(data)
excel_filename = 'editais_fapesp.xlsx'
df.to_excel(excel_filename, index=False)