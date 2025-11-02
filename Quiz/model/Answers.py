class Resposta:
    lista_respostas = []  # Simula o armazenamento de respostas

    def __init__(self, usuario, pergunta, resposta_enviada, correta=False):
        self.usuario = usuario
        self.pergunta = pergunta
        self.resposta_enviada = resposta_enviada
        self.correta = correta

    def salvar(self):
        Resposta.lista_respostas.append(self)
        print(f"✅ Resposta salva para o usuário {self.usuario.nome}")

    @staticmethod
    def buscar_por_usuario(usuario):
        return [r for r in Resposta.lista_respostas if r.usuario == usuario]

    def __str__(self):
        return f"Resposta(usuario={self.usuario.nome}, correta={self.correta})"