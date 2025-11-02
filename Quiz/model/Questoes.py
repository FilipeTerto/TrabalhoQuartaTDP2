class Pergunta:
    lista_perguntas = []  # Simula o banco de perguntas

    def __init__(self, texto, alternativas, resposta_correta, dica=None):
        self.texto = texto
        self.alternativas = alternativas
        self.resposta_correta = resposta_correta
        self.dica = dica

    def salvar(self):
        Pergunta.lista_perguntas.append(self)
        print(f"✅ Pergunta adicionada: {self.texto}")

    def verificar_resposta(self, resposta):
        return resposta.strip().lower() == self.resposta_correta.strip().lower()

    @staticmethod
    def buscar_todas():
        return Pergunta.lista_perguntas

    def __str__(self):
        return f"Pergunta({self.texto})"