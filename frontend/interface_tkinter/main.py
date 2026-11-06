import tkinter as tk
from tkinter import ttk

from config import API_URL
from api_client import APIClient
from telas import CadastroFrame, AnalisesFrame


class SistemaAcademia(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(
            "Sistema de Análise de Desempenho em Academia"
        )
        self.geometry("950x620")
        self.minsize(800, 500)
        self.configure(bg="#f3f5f7")

        self.api = APIClient(API_URL)

        self.configurar_estilo()
        self.criar_cabecalho()
        self.criar_abas()

    def configurar_estilo(self):
        estilo = ttk.Style(self)

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "TNotebook.Tab",
            padding=(12, 7),
            font=("Arial", 10)
        )
        estilo.configure(
            "Treeview",
            rowheight=25,
            font=("Arial", 10)
        )
        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )
        estilo.configure(
            "TButton",
            padding=5,
            font=("Arial", 9)
        )

    def criar_cabecalho(self):
        cabecalho = tk.Frame(
            self, bg="#315f91", height=70
        )
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text="Sistema de Análise de Desempenho em Academia",
            bg="#315f91",
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=18, pady=(12, 2))

        tk.Label(
            cabecalho,
            text="Interface gráfica acadêmica",
            bg="#315f91",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w", padx=19)

    def criar_abas(self):
        abas = ttk.Notebook(self)
        abas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        entidades = [
            (
                "Alunos",
                "alunos",
                [
                    ("nome", "Nome"),
                    ("email", "E-mail"),
                    ("data_nascimento", "Nascimento (AAAA-MM-DD)"),
                    ("peso", "Peso (kg)"),
                    ("altura", "Altura (m)"),
                    ("objetivo", "Objetivo"),
                ]
            ),
            (
                "Exercícios",
                "exercicios",
                [
                    ("nome", "Nome"),
                    ("grupo_muscular", "Grupo muscular"),
                    ("descricao", "Descrição"),
                ]
            ),
            (
                "Treinos",
                "treinos",
                [
                    ("aluno_id", "ID do aluno"),
                    ("data_treino", "Data (AAAA-MM-DD)"),
                    ("observacao", "Observação"),
                ]
            ),
            (
                "Registros",
                "registros",
                [
                    ("treino_id", "ID do treino"),
                    ("exercicio_id", "ID do exercício"),
                    ("carga", "Carga"),
                    ("repeticoes", "Repetições"),
                ]
            ),
        ]

        for titulo, endpoint, campos in entidades:
            tela = CadastroFrame(
                abas,
                self.api,
                titulo,
                endpoint,
                campos
            )
            abas.add(tela, text=titulo)

        abas.add(
            AnalisesFrame(abas, self.api),
            text="Análises"
        )


if __name__ == "__main__":
    app = SistemaAcademia()
    app.mainloop()
