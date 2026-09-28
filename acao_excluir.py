from tkinter import messagebox


class AcaoExcluir:
    """Controla o fluxo de exclusão de um produto pela tabela.

    Fluxo: ativar() coloca a ação em modo de espera -> o usuário clica
    numa linha da tabela -> tratar_selecao(codigo) é chamado -> confirmação
    -> se confirmado, remove o produto do estoque.
    """

    def __init__(self, app, ao_atualizar):
        self.app = app
        self.estoque = app.estoque
        self.ao_atualizar = ao_atualizar  # callback chamado após excluir com sucesso
        self.ativo = False

    def ativar(self):
        self.ativo = True
        messagebox.showinfo(
            "Selecionar produto", "Clique na linha do produto que deseja excluir."
        )

    def tratar_selecao(self, codigo):
        """Chamado pela aba quando uma linha é clicada.
        Retorna True se esta ação tratou o clique (estava ativa)."""
        if not self.ativo:
            return False
        self.ativo = False

        prod = self.estoque.buscar_produto(codigo)
        if prod is None:
            return True

        if messagebox.askyesno(
            "Confirmar exclusão", f"Tem certeza que deseja excluir '{prod.nome}'?"
        ):
            self.estoque.remover_produto(codigo)
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.ao_atualizar()

        return True
