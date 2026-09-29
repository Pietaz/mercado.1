class BuscaProdutos:
    """Encapsula a lógica de busca de produtos no estoque."""

    def __init__(self, estoque):
        self.estoque = estoque

    def buscar(self, codigo=None, nome=None, categoria=None):
        """
        Retorna lista de produtos que atendem aos filtros.

        - codigo: match exato (int ou None)
        - nome: substring case-insensitive (str ou None)
        - categoria: match exato (str ou None)
        """
        resultados = []
        nome_lower = nome.lower() if nome else None

        for p in self.estoque.produtos:
            if codigo is not None and p.codigo != codigo:
                continue
            if nome_lower and nome_lower not in p.nome.lower():
                continue
            if categoria is not None and p.categoria != categoria:
                continue
            resultados.append(p)

        return resultados

    @staticmethod
    def parse_codigo(texto):
        """
        Converte texto em int. Retorna (codigo, erro).
        erro é uma string com mensagem, ou None se OK.
        """
        texto = (texto or "").strip()
        if not texto:
            return None, None
        try:
            return int(texto), None
        except ValueError:
            return None, "Digite um código numérico válido."