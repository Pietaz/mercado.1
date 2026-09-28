from produto import Produto
from bancodados import BancoDados


class Estoque:
    """Camada de regras de negócio do estoque.

    Produtos e categorias NÃO ficam guardados numa lista própria em memória:
    cada consulta (self.produtos, self.categorias, buscar_produto...) é
    feita direto no banco SQLite (BancoDados), que é a única fonte de
    verdade dos dados. Assim a aba Listar sempre mostra exatamente o que
    está salvo no banco, em vez de depender de uma cópia local que precisa
    ser mantida sincronizada manualmente.
    """

    def __init__(self, banco=None):
        # Por padrão conecta no banco SQLite (estoque.db); pode receber um
        # BancoDados diferente (por exemplo, um banco de teste em memória).
        self.banco = banco or BancoDados()

    @property
    def produtos(self):
        """Lista de produtos, lida diretamente do banco a cada chamada."""
        return [
            Produto(codigo, nome, preco, quantidade, categoria)
            for codigo, nome, preco, quantidade, categoria in self.banco.carregar_produtos()
        ]

    @property
    def categorias(self):
        """Lista de categorias, lida diretamente do banco a cada chamada."""
        return self.banco.carregar_categorias()

    def criar_categoria(self, nome):
        nome = nome.strip()
        if not nome:
            return False
        if nome.lower() in [c.lower() for c in self.categorias]:
            return False
        self.banco.inserir_categoria(nome)
        return True

    def buscar_produto(self, codigo):
        linha = self.banco.buscar_produto(codigo)
        if linha is None:
            return None
        codigo, nome, preco, quantidade, categoria = linha
        return Produto(codigo, nome, preco, quantidade, categoria)

    def cadastrar_produto(self, produto):
        if self.buscar_produto(produto.codigo) is not None:
            return False
        self.banco.inserir_produto(
            produto.codigo, produto.nome, produto.preco,
            produto.quantidade, produto.categoria,
        )
        return True

    def alterar_produto(self, codigo, nome, novo_preco, nova_quantidade, categoria):
        prod = self.buscar_produto(codigo)
        if prod is None:
            return False
        prod.nome = nome
        prod.categoria = categoria
        prod.atualizar_preco(novo_preco)
        prod.atualizar_quantidade(nova_quantidade)
        self.banco.atualizar_produto(
            prod.codigo, prod.nome, prod.preco, prod.quantidade, prod.categoria
        )
        return True

    def remover_produto(self, codigo):
        if self.buscar_produto(codigo) is None:
            return False
        self.banco.remover_produto(codigo)
        return True

    def calcular_quantidade_total(self):
        return sum(prod.quantidade for prod in self.produtos)