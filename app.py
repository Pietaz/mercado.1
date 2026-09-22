import customtkinter as ctk
from tkinter import messagebox

import produto as modulo_produto
import estoque as modulo_estoque
from produto import Produto
from estoque import Estoque

from aba_cadastrar import AbaCadastrar
from aba_buscar import AbaBuscar
from aba_listar import AbaListar

# Verificação: garante que os arquivos carregados são as versões novas.
if "categoria" not in Produto.__init__.__code__.co_varnames:
    raise SystemExit(
        "produto.py desatualizado (sem 'categoria'). Arquivo carregado: "
        + str(modulo_produto.__file__)
    )
if not hasattr(Estoque(), "categorias"):
    raise SystemExit(
        "estoque.py desatualizado (sem 'categorias'). Arquivo carregado: "
        + str(modulo_estoque.__file__)
    )


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AppEstoque(ctk.CTk):
    """Janela principal: cria as abas e coordena a comunicação entre elas."""

    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Estoque")
        self.geometry("950x750")

        self.estoque = Estoque()

        self.abas = ctk.CTkTabview(
            self,
            segmented_button_selected_color="#A37BD6",
            segmented_button_selected_hover_color="#8358BE",
        )
        self.abas.pack(fill="both", expand=True, padx=10, pady=10)

        tab_cadastrar = self.abas.add("Cadastrar")
        tab_buscar = self.abas.add("Consultar")
        tab_listar = self.abas.add("Listar no Estoque")

        # A ordem de criação segue a original: Cadastrar, Buscar e por
        # último Listar (que já nasce exibindo a tabela preenchida).
        self.aba_cadastrar = AbaCadastrar(tab_cadastrar, self)
        self.aba_buscar = AbaBuscar(tab_buscar, self)
        self.aba_listar = AbaListar(tab_listar, self)

    # ------------------------------------------------------------------
    # MÉTODOS COMPARTILHADOS ENTRE AS ABAS
    # ------------------------------------------------------------------
    def criar_categoria(self):
        """Abre o diálogo de nova categoria, cria no estoque e propaga
        a atualização para as abas que possuem combobox de categoria.
        Retorna o nome criado (ou None se cancelado/erro), para que a
        aba que chamou possa selecioná-lo em seu próprio combobox."""
        dialogo = ctk.CTkInputDialog(text="Nome da nova categoria:", title="Nova categoria")
        nome = dialogo.get_input()
        if not nome:  # cancelou ou deixou vazio
            return None

        if self.estoque.criar_categoria(nome):
            self.atualizar_categorias()
            return nome.strip()
        else:
            messagebox.showerror("Erro", "Categoria vazia ou já existe.")
            return None

    def atualizar_categorias(self):
        """Atualiza as opções de categoria nas comboboxes das abas."""
        self.aba_cadastrar.atualizar_categoria_values(self.estoque.categorias)
        self.aba_listar.atualizar_categoria_values(self.estoque.categorias)

    def refresh_listar(self):
        """Atualiza a tabela da aba Listar (chamado após cadastrar/alterar)."""
        self.aba_listar.acao_listar()


if __name__ == "__main__":
    app = AppEstoque()
    app.mainloop()
