class EditalFapesp:
    def __init__(self, titulo, data_limite,area,modalidade,link):
        self.titulo = titulo
        self.area = area
        self.modalidade = modalidade
        self.data_limite = data_limite
        self.link = link

    def __str__(self):
        return f'Título: {self.titulo}\n' \
               f'Data limite: {self.data_limite}\n' \
               f'Modalidade: {self.modalidade}\n' \
               f'Area: {self.area}\n' \
               f'Link: {self.link}\n'