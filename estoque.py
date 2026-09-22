class Estoque:

    def __init__(self):
        self.produtos = []
        self.categorias = ["sem categoria"]

    def criar_categoria(self, nome):
        nome = nome.strip()
        if not nome:
            return False
        if nome.lower() in [c.lower() for c in self.categorias]:
            return False
        self.categorias.append(nome)
        return True

    def buscar_produto(self, codigo):
        for prod in self.produtos:
            if prod.codigo == codigo:
                return prod
        return None

    def cadastrar_produto(self, produto):
        if self.buscar_produto(produto.codigo) is None:
            self.produtos.append(produto)
            return True
        return False

    def alterar_produto(self, codigo, novo_preco, nova_quantidade):
        prod = self.buscar_produto(codigo)
        if prod is not None:
            prod.atualizar_preco(novo_preco)
            prod.atualizar_quantidade(nova_quantidade)
            return True
        return False

    def remover_produto(self, codigo):
        prod = self.buscar_produto(codigo)
        if prod is not None:
            self.produtos.remove(prod)
            return True
        return False

    def calcular_quantidade_total(self):
        total = 0
        for prod in self.produtos:
            total += prod.quantidade
        return total