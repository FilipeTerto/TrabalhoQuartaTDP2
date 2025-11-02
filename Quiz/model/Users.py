class Usuario:
    lista_usuarios = []  # Simula uma "tabela" de usuários em memória

    def __init__(self, nome, email, senha_hash, pontuacao_total=0):
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.pontuacao_total = pontuacao_total

    def salvar(self):
        Usuario.lista_usuarios.append(self)
        print(f"✅ Usuário '{self.nome}' salvo com sucesso!")

    @staticmethod
    def buscar_por_email(email):
        for usuario in Usuario.lista_usuarios:
            if usuario.email == email:
                print(f"🔎 Usuário encontrado: {usuario.nome}")
                return usuario
        print("❌ Nenhum usuário encontrado com esse e-mail.")
        return None

    def __str__(self):
        return f"Usuário(nome={self.nome}, email={self.email}, pontuação={self.pontuacao_total})"