class EditalFinep:
    def __init__(self, titulo, data_publicacao, data_limite,fonte,publico_alvo,tema,link):
        self.titulo = titulo
        self.data_publicacao = data_publicacao
        self.data_limite = data_limite
        self.fonte = fonte
        self.publico_alvo = publico_alvo
        self.tema = tema
        self.link = link

    def __str__(self):
        return f'Título: {self.titulo}\n' \
               f'Data de publicação: {self.data_publicacao}\n' \
               f'Data limite: {self.data_limite}\n' \
               f'Fonte: {self.fonte}\n' \
               f'Público-alvo: {self.publico_alvo}\n' \
               f'Tema: {self.tema}\n' \
               f'Link: {self.link}\n'