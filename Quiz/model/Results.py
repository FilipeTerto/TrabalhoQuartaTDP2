from datetime import datetime

class Resultado:
    lista_resultados = []

    def __init__(self, usuario, pontuacao_total, total_questions, respostas_corretas, data=None):
        self.usuario = usuario
        self.pontuacao_total = pontuacao_total
        self.total_questions = total_questions
        self.respostas_corretas = respostas_corretas
        self.data = data or datetime.now()
        self.porcentagem = self.calcular_porcentagem()

    def calcular_porcentagem(self):
        if self.total_questions == 0:
            return 0
        return round((self.respostas_corretas / self.total_questions) * 100, 2)

    def salvar(self):
        Resultado.lista_resultados.append(self)
        print(f"✅ Resultado salvo: {self.usuario.nome} fez {self.porcentagem}% de acertos")

    @staticmethod
    def buscar_por_usuario(usuario):
        return [r for r in Resultado.lista_resultados if r.usuario == usuario]

    def __str__(self):
        return f"Resultado({self.usuario.nome}, {self.porcentagem}%)"