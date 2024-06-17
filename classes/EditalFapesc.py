class EditalFapesc:
    def __init__(self, titulo, resumo,link):
        self.titulo = titulo
        self.resumo = resumo
        self.link = link

    def __str__(self):
        return f'Título: {self.titulo}\n' \
               f'Resumo: {self.resumo}\n' \
               f'Link: {self.link}\n'