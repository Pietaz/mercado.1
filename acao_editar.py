from tkinter import messagebox

from popup_alterar import PopupAlterar


class AcaoEditar:
    """Controla o fluxo de edição de um produto pela tabela.

    Fluxo: ativar() coloca a ação em modo de espera -> o usuário clica
    numa linha da tabela -> tratar_selecao(codigo) é chamado -> confirmação
    -> se confirmado, abre o popup de edição.
    """

    def __init__(self, app, ao_atualizar):
        self.app = app
        self.estoque = app.estoque
        self.ao_atualizar = ao_atualizar  # callback chamado após salvar a edição
        self.ativo = False

    def ativar(self):
        self.ativo = True
        messagebox.showinfo(
            "Selecionar produto", "Clique na linha do produto que deseja editar."
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
            "Confirmar edição", f"Tem certeza que deseja editar '{prod.nome}'?"
        ):
            PopupAlterar(self.app, prod, ao_salvar=self.ao_atualizar)

        return True
