import customtkinter as ctk
from tkinter import ttk

from helpers import formatar_preco, TODAS
from acao_editar import AcaoEditar
from acao_excluir import AcaoExcluir


class AbaListar:
    """Aba de listagem, busca, edição e exclusão de produtos em estoque."""

    def __init__(self, aba, app):
        self.app = app
        self.estoque = app.estoque
        self.linha_hover = None  # item da tabela que está sob o mouse no momento

        # Cada ação cuida do próprio fluxo de seleção + confirmação
        self.acao_editar = AcaoEditar(self.app, ao_atualizar=self.acao_listar)
        self.acao_excluir = AcaoExcluir(self.app, ao_atualizar=self.acao_listar)

        self._montar(aba)
        self.acao_listar()

    def _montar(self, aba):
        # Barra superior: Buscar | Categoria | Editar | Excluir
        frame_filtro = ctk.CTkFrame(aba, fg_color="transparent")
        frame_filtro.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(frame_filtro, text="Buscar:").pack(side="left", padx=(0, 8))
        self.ent_busca = ctk.CTkEntry(frame_filtro, width=180, placeholder_text="Código ou nome")
        self.ent_busca.pack(side="left", padx=(0, 15))
        self.ent_busca.bind("<KeyRelease>", self.acao_listar)

        ctk.CTkLabel(frame_filtro, text="Categoria:").pack(side="left", padx=(0, 8))
        self.cmb_filtro = ctk.CTkComboBox(
            frame_filtro,
            values=[TODAS] + self.estoque.categorias,
            state="readonly",
            width=180,
            command=self.acao_listar,
        )
        self.cmb_filtro.set(TODAS)
        self.cmb_filtro.pack(side="left", padx=(0, 15))

        self.btn_editar = ctk.CTkButton(
            frame_filtro, text="Editar Produto", width=130,
            fg_color="#A37BD6", hover_color="#8358BE",
            command=self.acao_editar.ativar,
        )
        self.btn_editar.pack(side="left", padx=(0, 8))

        self.btn_excluir = ctk.CTkButton(
            frame_filtro, text="Excluir Produto", width=130,
            fg_color="#C0392B", hover_color="#922B21",
            command=self.acao_excluir.ativar,
        )
        self.btn_excluir.pack(side="left")

        # Estilo do Treeview para combinar com o tema escuro
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=32,
            borderwidth=0,
            font=("Arial", 12),
        )
        estilo.configure(
            "Treeview.Heading",
            background="#3a3a3a",
            foreground="white",
            relief="flat",
            font=("Arial", 12, "bold"),
        )
        estilo.map("Treeview", background=[("selected", "#1f6aa5")])

        frame_tabela = ctk.CTkFrame(aba)
        frame_tabela.pack(fill="both", expand=True)

        colunas = ("codigo", "nome", "categoria", "preco", "quantidade")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        # Títulos e conteúdo das células centralizados
        self.tabela.heading("codigo", text="Código", anchor="center")
        self.tabela.heading("nome", text="Nome", anchor="center")
        self.tabela.heading("categoria", text="Categoria", anchor="center")
        self.tabela.heading("preco", text="Preço (R$)", anchor="center")
        self.tabela.heading("quantidade", text="Quantidade", anchor="center")

        self.tabela.column("codigo", width=90, anchor="center")
        self.tabela.column("nome", width=300, anchor="center")
        self.tabela.column("categoria", width=160, anchor="center")
        self.tabela.column("preco", width=120, anchor="center")
        self.tabela.column("quantidade", width=110, anchor="center")

        # Tag usada para escurecer a linha sob o cursor do mouse
        self.tabela.tag_configure("hover", background="#1e1e1e")

        barra = ctk.CTkScrollbar(frame_tabela, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        # Clique em uma linha: repassa para a ação (editar/excluir) ativa
        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar_produto)

        # Escurece a linha sob o cursor para indicar qual produto será selecionado
        self.tabela.bind("<Motion>", self.ao_passar_mouse)
        self.tabela.bind("<Leave>", self.ao_sair_mouse)

        self.lbl_contagem = ctk.CTkLabel(aba, text="")
        self.lbl_contagem.pack(pady=(8, 0))

        btn_atualizar = ctk.CTkButton(
            aba, text="Atualizar Lista", command=self.acao_listar,
            fg_color="#A37BD6", hover_color="#8358BE",
        )
        btn_atualizar.pack(pady=10)

    def atualizar_categoria_values(self, categorias):
        """Chamado pelo App quando a lista de categorias muda em qualquer aba."""
        self.cmb_filtro.configure(values=[TODAS] + categorias)

    def acao_listar(self, _=None):
        # O parâmetro "_" recebe o valor/evento enviado pelo combobox ou
        # pela tecla digitada na busca, e é ignorado.
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        filtro_categoria = self.cmb_filtro.get()
        texto_busca = self.ent_busca.get().strip().lower()
        exibidos = 0

        for p in self.estoque.produtos:
            if filtro_categoria != TODAS and p.categoria != filtro_categoria:
                continue
            if texto_busca and texto_busca not in p.nome.lower() and texto_busca not in str(p.codigo):
                continue
            self.tabela.insert(
                "", "end",
                values=(p.codigo, p.nome, p.categoria, formatar_preco(p.preco), p.quantidade),
            )
            exibidos += 1

        self.lbl_contagem.configure(text=f"Exibindo {exibidos} produto(s)")

    # ------------------------------------------------------------------
    # EFEITO DE HOVER (escurece a linha sob o cursor)
    # ------------------------------------------------------------------
    def ao_passar_mouse(self, evento):
        item = self.tabela.identify_row(evento.y)

        if item == self.linha_hover:
            return  # mouse continua na mesma linha, nada a fazer

        if self.linha_hover is not None and self.tabela.exists(self.linha_hover):
            self.tabela.item(self.linha_hover, tags=())

        if item:
            self.tabela.item(item, tags=("hover",))

        self.linha_hover = item or None

    def ao_sair_mouse(self, _evento):
        if self.linha_hover is not None and self.tabela.exists(self.linha_hover):
            self.tabela.item(self.linha_hover, tags=())
        self.linha_hover = None

    # ------------------------------------------------------------------
    # CLIQUE NA TABELA: repassa para a ação (editar/excluir) que estiver ativa
    # ------------------------------------------------------------------
    def ao_selecionar_produto(self, _evento):
        selecionados = self.tabela.selection()
        if not selecionados:
            return
        item_id = selecionados[0]
        valores = self.tabela.item(item_id, "values")
        codigo = int(valores[0])
        self.tabela.selection_remove(item_id)

        # Cada ação sabe se está ativa; só uma delas trata o clique por vez.
        if self.acao_editar.tratar_selecao(codigo):
            return
        self.acao_excluir.tratar_selecao(codigo)