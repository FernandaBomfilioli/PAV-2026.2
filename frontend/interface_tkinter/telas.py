import tkinter as tk
from tkinter import ttk, messagebox
from config import CAMPO_ID


class CadastroFrame(ttk.Frame):
    def __init__(
        self, parent, api, titulo, endpoint, campos
    ):
        super().__init__(parent, padding=12)

        self.api = api
        self.titulo = titulo
        self.endpoint = endpoint
        self.campos = campos
        self.registros = []
        self.registro_selecionado = None
        self.entradas = {}

        ttk.Label(
            self,
            text=f"Gerenciar {titulo.lower()}",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            self, text="Dados", padding=10
        )
        formulario.pack(fill="x", pady=(0, 10))

        for indice, (campo, rotulo) in enumerate(campos):
            linha, coluna = divmod(indice, 3)

            grupo = ttk.Frame(formulario)
            grupo.grid(
                row=linha,
                column=coluna,
                sticky="ew",
                padx=6,
                pady=5
            )

            ttk.Label(
                grupo, text=rotulo
            ).pack(anchor="w")

            entrada = ttk.Entry(grupo, width=24)
            entrada.pack(fill="x", pady=(3, 0))

            self.entradas[campo] = entrada
            formulario.columnconfigure(coluna, weight=1)

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=(0, 10))

        ttk.Button(
            botoes,
            text="Cadastrar",
            command=self.cadastrar
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            botoes,
            text="Atualizar",
            command=self.atualizar
        ).pack(side="left", padx=5)

        ttk.Button(
            botoes,
            text="Excluir",
            command=self.excluir
        ).pack(side="left", padx=5)

        ttk.Button(
            botoes,
            text="Limpar",
            command=self.limpar
        ).pack(side="left", padx=5)

        ttk.Button(
            botoes,
            text="Recarregar",
            command=self.carregar
        ).pack(side="right")

        area_tabela = ttk.Frame(self)
        area_tabela.pack(fill="both", expand=True)

        self.tabela = ttk.Treeview(
            area_tabela,
            show="headings",
            selectmode="browse"
        )

        barra_vertical = ttk.Scrollbar(
            area_tabela,
            orient="vertical",
            command=self.tabela.yview
        )

        barra_horizontal = ttk.Scrollbar(
            area_tabela,
            orient="horizontal",
            command=self.tabela.xview
        )

        self.tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabela.grid(
            row=0, column=0, sticky="nsew"
        )
        barra_vertical.grid(
            row=0, column=1, sticky="ns"
        )
        barra_horizontal.grid(
            row=1, column=0, sticky="ew"
        )

        area_tabela.rowconfigure(0, weight=1)
        area_tabela.columnconfigure(0, weight=1)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_registro
        )

        self.carregar()

    def obter_dados(self, validar_obrigatorios=True):
        dados = {}

        for campo, _ in self.campos:
            valor = self.entradas[campo].get().strip()

            if valor == "":
                continue

            if campo.endswith("_id") or campo == "repeticoes":
                try:
                    valor = int(valor)
                except ValueError:
                    raise ValueError(
                        f"O campo '{campo}' deve ser "
                        "um número inteiro."
                    )

            elif campo in ("carga", "peso", "altura"):
                try:
                    valor = float(valor.replace(",", "."))
                except ValueError:
                    raise ValueError(
                        f"O campo '{campo}' deve ser numérico."
                    )

            dados[campo] = valor

        obrigatorios = {
            "alunos": ["nome", "email"],
            "exercicios": ["nome"],
            "treinos": ["aluno_id"],
            "registros": [
                "treino_id",
                "exercicio_id",
                "carga",
                "repeticoes"
            ],
        }.get(self.endpoint, [])

        faltando = [
            campo
            for campo in obrigatorios
            if campo not in dados
        ]

        if validar_obrigatorios and faltando:
            raise ValueError(
                "Preencha os campos obrigatórios: "
                + ", ".join(faltando)
            )

        if not dados:
            raise ValueError(
                "Preencha os dados do formulário."
            )

        if validar_obrigatorios and self.endpoint == "registros":
            if dados.get("carga", 0) < 0:
                raise ValueError(
                    "A carga deve ser maior ou igual a zero."
                )

            if dados.get("repeticoes", 0) <= 0:
                raise ValueError(
                    "As repetições devem ser maiores que zero."
                )

        return dados

    def carregar(self):
        try:
            self.registros = self.api.listar(self.endpoint)
            self.atualizar_tabela()
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível carregar "
                f"{self.titulo.lower()}.\n\n{erro}",
                parent=self
            )

    def atualizar_tabela(self):
        self.tabela.delete(
            *self.tabela.get_children()
        )

        colunas = []

        for registro in self.registros:
            if isinstance(registro, dict):
                for chave in registro:
                    if chave not in colunas:
                        colunas.append(chave)

        if not colunas:
            colunas = [CAMPO_ID]

        self.tabela["columns"] = colunas

        for coluna in colunas:
            self.tabela.heading(
                coluna,
                text=coluna.replace("_", " ").title()
            )
            self.tabela.column(
                coluna,
                width=130,
                minwidth=80
            )

        for indice, registro in enumerate(self.registros):
            if isinstance(registro, dict):
                valores = [
                    str(registro.get(coluna, ""))
                    for coluna in colunas
                ]
            else:
                valores = [str(registro)]

            self.tabela.insert(
                "",
                "end",
                iid=str(indice),
                values=valores
            )

    def selecionar_registro(self, evento=None):
        selecao = self.tabela.selection()

        if not selecao:
            return

        try:
            registro = self.registros[int(selecao[0])]
        except (ValueError, IndexError):
            return

        if not isinstance(registro, dict):
            return

        self.registro_selecionado = registro

        for campo, _ in self.campos:
            self.entradas[campo].delete(0, "end")

            valor = registro.get(campo)

            if valor is not None:
                self.entradas[campo].insert(
                    0, str(valor)
                )

    def limpar(self):
        for entrada in self.entradas.values():
            entrada.delete(0, "end")

        self.registro_selecionado = None

        for item in self.tabela.selection():
            self.tabela.selection_remove(item)

    def cadastrar(self):
        try:
            dados = self.obter_dados()
            self.api.criar(self.endpoint, dados)

            messagebox.showinfo(
                "Sucesso",
                "Cadastro realizado.",
                parent=self
            )

            self.limpar()
            self.carregar()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao cadastrar",
                str(erro),
                parent=self
            )

    def atualizar(self):
        if not self.registro_selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um registro na tabela.",
                parent=self
            )
            return

        identificador = self.registro_selecionado.get(
            CAMPO_ID
        )

        if identificador is None:
            messagebox.showerror(
                "Erro",
                f"A API precisa retornar o campo "
                f"'{CAMPO_ID}' para atualizar.",
                parent=self
            )
            return

        try:
            dados = self.obter_dados(
                validar_obrigatorios=False
            )

            self.api.atualizar(
                self.endpoint,
                identificador,
                dados
            )

            messagebox.showinfo(
                "Sucesso",
                "Registro atualizado.",
                parent=self
            )

            self.limpar()
            self.carregar()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao atualizar",
                str(erro),
                parent=self
            )

    def excluir(self):
        if not self.registro_selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um registro na tabela.",
                parent=self
            )
            return

        identificador = self.registro_selecionado.get(
            CAMPO_ID
        )

        if identificador is None:
            messagebox.showerror(
                "Erro",
                f"A API precisa retornar o campo "
                f"'{CAMPO_ID}' para excluir.",
                parent=self
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o registro {identificador}?",
            parent=self
        )

        if not confirmar:
            return

        try:
            self.api.excluir(
                self.endpoint,
                identificador
            )

            messagebox.showinfo(
                "Sucesso",
                "Registro excluído.",
                parent=self
            )

            self.limpar()
            self.carregar()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                str(erro),
                parent=self
            )



class AnalisesFrame(ttk.Frame):
    def __init__(self, parent, api):
        super().__init__(parent, padding=14)
        self.api = api

        estilo = ttk.Style()
        estilo.configure("Indicador.TLabel", font=("Arial", 9), foreground="#555555")
        estilo.configure("ValorIndicador.TLabel", font=("Arial", 18, "bold"), foreground="#285783")
        estilo.configure("TituloAnalise.TLabel", font=("Arial", 15, "bold"), foreground="#285783")
        estilo.configure("Treeview", rowheight=28, font=("Arial", 10))
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        ttk.Label(
            self,
            text="Análises de desempenho",
            style="TituloAnalise.TLabel"
        ).pack(anchor="w", pady=(0, 4))

        ttk.Label(
            self,
            text="Consulte o volume dos treinos, compare períodos e acompanhe a frequência dos alunos."
        ).pack(anchor="w", pady=(0, 12))

        consultas = ttk.LabelFrame(self, text="Consultar análise", padding=10)
        consultas.pack(fill="x", pady=(0, 10))

        linha1 = ttk.Frame(consultas)
        linha1.pack(fill="x", pady=4)

        ttk.Label(linha1, text="ID do treino:").pack(side="left")
        self.id_treino = ttk.Entry(linha1, width=10)
        self.id_treino.pack(side="left", padx=(6, 12))
        ttk.Button(
            linha1, text="Consultar volume", command=self.volume_treino
        ).pack(side="left")

        linha2 = ttk.Frame(consultas)
        linha2.pack(fill="x", pady=6)

        ttk.Label(linha2, text="ID do aluno:").pack(side="left")
        self.id_aluno = ttk.Entry(linha2, width=9)
        self.id_aluno.pack(side="left", padx=6)
        ttk.Label(linha2, text="ID do exercício:").pack(side="left", padx=(10, 0))
        self.id_exercicio = ttk.Entry(linha2, width=9)
        self.id_exercicio.pack(side="left", padx=6)

        ttk.Button(
            linha2, text="Comparar períodos", command=self.comparacao
        ).pack(side="left", padx=(8, 4))
        ttk.Button(
            linha2, text="Consultar frequência", command=self.frequencia
        ).pack(side="left", padx=4)

        datas_frame = ttk.LabelFrame(
            self, text="Filtros de data opcionais (AAAA-MM-DD)", padding=8
        )
        datas_frame.pack(fill="x", pady=(0, 10))

        self.datas = {}
        campos_datas = [
            ("data_inicio_1", "Início período 1"),
            ("data_fim_1", "Fim período 1"),
            ("data_inicio_2", "Início período 2"),
            ("data_fim_2", "Fim período 2"),
            ("data_inicio", "Início frequência"),
            ("data_fim", "Fim frequência"),
        ]

        for indice, (campo, rotulo) in enumerate(campos_datas):
            grupo = ttk.Frame(datas_frame)
            grupo.grid(
                row=indice // 3, column=indice % 3,
                sticky="ew", padx=5, pady=4
            )
            ttk.Label(grupo, text=rotulo).pack(anchor="w")
            entrada = ttk.Entry(grupo)
            entrada.pack(fill="x", pady=(3, 0))
            self.datas[campo] = entrada

        for coluna in range(3):
            datas_frame.columnconfigure(coluna, weight=1)

        # Contêiner dos resultados com rolagem vertical.
        self.resultados = ttk.LabelFrame(self, text="Resultado da análise", padding=6)
        self.resultados.pack(fill="both", expand=True)

        self.canvas_resultados = tk.Canvas(
            self.resultados, highlightthickness=0, borderwidth=0
        )
        self.barra_resultados = ttk.Scrollbar(
            self.resultados, orient="vertical", command=self.canvas_resultados.yview
        )
        self.canvas_resultados.configure(
            yscrollcommand=self.barra_resultados.set
        )
        self.barra_resultados.pack(side="right", fill="y")
        self.canvas_resultados.pack(side="left", fill="both", expand=True)

        self.conteudo_resultados = ttk.Frame(self.canvas_resultados, padding=6)
        self.janela_resultados = self.canvas_resultados.create_window(
            (0, 0), window=self.conteudo_resultados, anchor="nw"
        )
        self.conteudo_resultados.bind("<Configure>", self.atualizar_area_rolagem)
        self.canvas_resultados.bind("<Configure>", self.redimensionar_conteudo)
        self.canvas_resultados.bind("<Enter>", self.ativar_rolagem_mouse)
        self.canvas_resultados.bind("<Leave>", self.desativar_rolagem_mouse)

        self.mensagem_inicial = ttk.Label(
            self.conteudo_resultados,
            text="Selecione uma consulta para visualizar os resultados.",
            font=("Arial", 11), foreground="#666666"
        )
        self.mensagem_inicial.pack(anchor="center", pady=30)

    def atualizar_area_rolagem(self, evento=None):
        self.canvas_resultados.configure(
            scrollregion=self.canvas_resultados.bbox("all")
        )

    def redimensionar_conteudo(self, evento):
        self.canvas_resultados.itemconfigure(
            self.janela_resultados, width=evento.width
        )

    def ativar_rolagem_mouse(self, evento=None):
        self.canvas_resultados.bind_all("<MouseWheel>", self.rolar_com_mouse)

    def desativar_rolagem_mouse(self, evento=None):
        self.canvas_resultados.unbind_all("<MouseWheel>")

    def rolar_com_mouse(self, evento):
        self.canvas_resultados.yview_scroll(
            int(-1 * (evento.delta / 120)), "units"
        )

    def limpar_resultado(self):
        for widget in self.conteudo_resultados.winfo_children():
            widget.destroy()

    @staticmethod
    def formatar_nome(chave):
        nomes = {
            "treino_id": "ID do treino",
            "aluno_id": "ID do aluno",
            "exercicio_id": "ID do exercício",
            "data_treino": "Data do treino",
            "quantidade_registros": "Exercícios registrados",
            "quantidade_treinos": "Treinos realizados",
            "volume_total": "Volume total",
            "carga_media": "Carga média",
            "carga_maxima": "Carga máxima",
            "repeticoes_total": "Total de repetições",
            "variacao_volume_percentual": "Variação do volume",
            "tendencia": "Tendência",
            "data_inicio": "Data inicial",
            "data_fim": "Data final",
            "datas": "Datas dos treinos",
            "detalhes": "Detalhes dos exercícios",
            "registros": "Registros",
            "periodo_1": "Período 1",
            "periodo_2": "Período 2",
        }
        return nomes.get(chave, chave.replace("_", " ").capitalize())

    @staticmethod
    def formatar_valor(chave, valor):
        if valor is None:
            return "Não informado"
        if isinstance(valor, bool):
            return "Sim" if valor else "Não"
        if isinstance(valor, float):
            if "percentual" in chave or "variacao" in chave:
                return f"{valor:+.2f}%"
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if isinstance(valor, list):
            return ", ".join(str(item) for item in valor)
        if isinstance(valor, dict):
            return ""
        return str(valor)

    def criar_cartao(self, pai, titulo, valor):
        cartao = ttk.LabelFrame(pai, text=titulo, padding=(12, 10))
        cartao.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        ttk.Label(
            cartao, text=valor, style="ValorIndicador.TLabel", wraplength=190
        ).pack(anchor="w", pady=(3, 0))

    def criar_tabela(self, pai, registros, titulo=None):
        if not isinstance(registros, list) or not registros:
            return
        registros_dict = [item for item in registros if isinstance(item, dict)]
        if not registros_dict:
            return

        if titulo:
            ttk.Label(
                pai, text=titulo, font=("Arial", 11, "bold")
            ).pack(anchor="w", pady=(12, 6))

        colunas = []
        for registro in registros_dict:
            for chave, valor in registro.items():
                if not isinstance(valor, (dict, list)) and chave not in colunas:
                    colunas.append(chave)
        if not colunas:
            return

        area = ttk.Frame(pai)
        area.pack(fill="x", expand=True, pady=(0, 5))
        tabela = ttk.Treeview(
            area, columns=colunas, show="headings",
            height=min(len(registros_dict), 7)
        )
        barra_y = ttk.Scrollbar(area, orient="vertical", command=tabela.yview)
        barra_x = ttk.Scrollbar(area, orient="horizontal", command=tabela.xview)
        tabela.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)

        for coluna in colunas:
            tabela.heading(coluna, text=self.formatar_nome(coluna))
            tabela.column(coluna, width=135, minwidth=90, anchor="center")

        for registro in registros_dict:
            valores = [
                self.formatar_valor(coluna, registro.get(coluna, ""))
                for coluna in colunas
            ]
            tabela.insert("", "end", values=valores)

        tabela.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)

    def renderizar_resultado(self, titulo, resultado):
        self.limpar_resultado()
        pai = self.conteudo_resultados

        ttk.Label(
            pai, text=titulo, style="TituloAnalise.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        if not isinstance(resultado, dict):
            ttk.Label(pai, text=str(resultado), wraplength=750).pack(anchor="w")
            self.atualizar_area_rolagem()
            return

        indicadores = ttk.Frame(pai)
        indicadores.pack(fill="x", pady=(0, 8))

        chaves_destaque = [
            ("volume_total", "Volume total"),
            ("quantidade_registros", "Exercícios registrados"),
            ("quantidade_treinos", "Treinos realizados"),
            ("carga_media", "Carga média"),
            ("carga_maxima", "Carga máxima"),
            ("repeticoes_total", "Total de repetições"),
            ("variacao_volume_percentual", "Variação do volume"),
        ]
        exibidos = set()
        for chave, rotulo in chaves_destaque:
            if chave in resultado and not isinstance(resultado[chave], (dict, list)):
                valor = self.formatar_valor(chave, resultado[chave])
                if chave == "volume_total" or chave in ("carga_media", "carga_maxima"):
                    valor += " kg"
                self.criar_cartao(indicadores, rotulo, valor)
                exibidos.add(chave)

        linhas_info = [
            (chave, valor) for chave, valor in resultado.items()
            if chave not in exibidos and not isinstance(valor, (dict, list))
        ]
        if linhas_info:
            informacoes = ttk.LabelFrame(pai, text="Informações gerais", padding=8)
            informacoes.pack(fill="x", pady=(0, 8))
            for chave, valor in linhas_info:
                linha = ttk.Frame(informacoes)
                linha.pack(fill="x", pady=2)
                ttk.Label(
                    linha, text=f"{self.formatar_nome(chave)}:",
                    font=("Arial", 10, "bold"), width=25
                ).pack(side="left", anchor="w")
                texto = self.formatar_valor(chave, valor)
                if chave == "tendencia":
                    texto = texto.replace("_", " ").capitalize()
                ttk.Label(linha, text=texto, wraplength=600).pack(side="left", anchor="w")

        for chave, valor in resultado.items():
            if isinstance(valor, list):
                if valor and all(isinstance(item, dict) for item in valor):
                    self.criar_tabela(pai, valor, self.formatar_nome(chave))
                elif valor:
                    ttk.Label(
                        pai,
                        text=f"{self.formatar_nome(chave)}: " + ", ".join(str(item) for item in valor),
                        wraplength=750
                    ).pack(anchor="w", pady=4)
            elif isinstance(valor, dict):
                grupo = ttk.LabelFrame(pai, text=self.formatar_nome(chave), padding=8)
                grupo.pack(fill="x", pady=5)
                for subchave, subvalor in valor.items():
                    if not isinstance(subvalor, (dict, list)):
                        linha = ttk.Frame(grupo)
                        linha.pack(fill="x", pady=2)
                        ttk.Label(
                            linha, text=f"{self.formatar_nome(subchave)}:", width=25
                        ).pack(side="left")
                        ttk.Label(
                            linha, text=self.formatar_valor(subchave, subvalor)
                        ).pack(side="left")
                    elif isinstance(subvalor, list):
                        self.criar_tabela(grupo, subvalor, self.formatar_nome(subchave))

        if not resultado:
            ttk.Label(pai, text="A API não retornou dados para esta consulta.").pack(anchor="w")

        self.atualizar_area_rolagem()

    def mostrar_resultado(self, titulo, funcao):
        try:
            resultado = funcao()
            self.renderizar_resultado(titulo, resultado)
        except Exception as erro:
            messagebox.showerror("Erro na análise", str(erro), parent=self)

    def volume_treino(self):
        treino = self.id_treino.get().strip()
        if not treino.isdigit():
            messagebox.showwarning("Validação", "Informe um ID de treino numérico.", parent=self)
            return
        self.mostrar_resultado(
            f"Resumo do treino #{treino}",
            lambda: self.api.consultar_analise(f"analise/volume-treino/{treino}")
        )

    def parametros_datas(self, campos, parametros):
        from datetime import date
        valores = {campo: self.datas[campo].get().strip() for campo in campos}

        for campo, valor in valores.items():
            if valor:
                try:
                    date.fromisoformat(valor)
                except ValueError:
                    raise ValueError(
                        f"A data de '{campo}' deve estar no formato AAAA-MM-DD."
                    )
                parametros[campo] = valor

        pares = [
            ("data_inicio_1", "data_fim_1", "O início do período 1 deve ser anterior ao fim."),
            ("data_inicio_2", "data_fim_2", "O início do período 2 deve ser anterior ao fim."),
            ("data_inicio", "data_fim", "A data inicial deve ser anterior à data final."),
        ]
        for inicio, fim, mensagem in pares:
            if valores.get(inicio) and valores.get(fim) and valores[inicio] > valores[fim]:
                raise ValueError(mensagem)
        return parametros

    def comparacao(self):
        aluno = self.id_aluno.get().strip()
        exercicio = self.id_exercicio.get().strip()
        if not aluno.isdigit() or not exercicio.isdigit():
            messagebox.showwarning(
                "Validação", "Informe IDs numéricos de aluno e exercício.", parent=self
            )
            return

        def consultar():
            parametros = {"aluno_id": aluno, "exercicio_id": exercicio}
            parametros = self.parametros_datas(
                ["data_inicio_1", "data_fim_1", "data_inicio_2", "data_fim_2"],
                parametros
            )
            return self.api.consultar_analise("analise/comparacao", parametros)

        self.mostrar_resultado("Comparação de desempenho", consultar)

    def frequencia(self):
        aluno = self.id_aluno.get().strip()
        if not aluno.isdigit():
            messagebox.showwarning(
                "Validação", "Informe um ID de aluno numérico.", parent=self
            )
            return

        def consultar():
            parametros = self.parametros_datas(
                ["data_inicio", "data_fim"], {"aluno_id": aluno}
            )
            return self.api.consultar_analise("analise/frequencia", parametros)

        self.mostrar_resultado("Frequência de treinos", consultar)
