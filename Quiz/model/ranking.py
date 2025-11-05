class Rank:
    lista_rank = []

    def __init__(self, usuario, posicao, pontuacao_total):
        self.usuario = usuario
        self.posicao = posicao
        self.pontuacao_total = pontuacao_total

    def salvar(self):
        Rank.lista_rank.append(self)
        print(f"🏆 {self.usuario.nome} entrou no ranking na posição {self.posicao}")

    @staticmethod
    def gerar_rank():
        # Ordena usuários pela pontuação total e recria o ranking
        usuarios_ordenados = sorted(Rank.lista_rank, key=lambda r: r.pontuacao_total, reverse=True)
        for posicao, r in enumerate(usuarios_ordenados, start=1):
            r.posicao = posicao
        return usuarios_ordenados

    def __str__(self):
        return f"Rank({self.posicao}º - {self.usuario.nome}: {self.pontuacao_total} pts)"