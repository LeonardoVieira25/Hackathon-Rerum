import tkinter as tk
from tkinter import filedialog, ttk

import os
import shutil
# from operador import get_operations_names
# from operador import init_operator


def mover_arquivo(arquivo_origem):
    diretorio_destino = os.path.join(os.getcwd(), "dataSets")
    # Verifique se a subpasta existe, e se não, crie-a
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Determine o nome do arquivo de destino
    nome_arquivo_destino = os.path.join(diretorio_destino, os.path.basename(arquivo_origem))

    # Mova o arquivo para a subpasta
    shutil.move(arquivo_origem, nome_arquivo_destino)

# def escolher_arquivo():
#     arquivo_selecionado = filedialog.askopenfilename()
#     if arquivo_selecionado:
#         # Chame sua função e passe o caminho do arquivo como argumento
#         print(arquivo_selecionado)

# def import_file(janela, select_file):
#     def busca_arquivo():
#         arquivo_selecionado = filedialog.askopenfilename()
#         mover_arquivo(arquivo_selecionado)
#         select_file()
#         fileEntry.delete(0, tk.END)
#         fileEntry.insert(0, arquivo_selecionado)

#     tk.Label(janela, text = "Escolha seu arquivo .csv:").grid(column=0, row=0)
#     fileEntry = tk.Entry(  janela, width=40)
#     fileEntry.grid(column=1, row=0)

#     fileButton = tk.Button(  janela, text="Buscar", command=busca_arquivo)
#     fileButton.grid(column=2, row=0)

# def select_file(janela, arquivos_disponiveis):
#     botoes = []
#     for i, texto in enumerate(arquivos_disponiveis):
#         botao = tk.Button(janela, text=texto, command=lambda t=texto: acao_do_botao(t))
#         botao.grid(row=i, column=0, padx=10, pady=5)
#         botoes.append(botao)

class Interface:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Hackaton")

        # Obtém a largura e altura da janela principal
        largura_janela = 500
        altura_janela = 300

        # Obtém a largura e altura da tela
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        # Calcula as coordenadas X e Y para centralizar a janela
        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2

        # Define a geometria da janela para centralizá-la
        self.janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        tk.Label(self.janela, text = "Escolha seu arquivo .csv:").grid(column=0, row=0)
        self.fileEntry = tk.Entry(self.janela, width=40)
        self.fileEntry.grid(column=1, row=0)

        self.fileButton = tk.Button(self.janela, text="Buscar", command=self.acao_botao)
        self.fileButton.grid(column=2, row=0)


        # Cria uma ComboBox com dados pré-definidos

        tk.Label(self.janela, text="Escolha a operação a ser realizada:").grid(column=0, row=1)
        self.dados_combobox = ["Média", "Opção 2", "Opção 3", "Opção 4"]
        # self.dados_combobox = [] + [get_operations_names()]
        self.combobox = ttk.Combobox(self.janela, values=self.dados_combobox)
        self.combobox.grid(column=1, row=1)
        self.combobox.set(self.dados_combobox[0])
        self.combobox.bind("<<ComboboxSelected>>", self.rastrear_selecao)
        self.generateButton = tk.Button(self.janela, text="Gerar")
        self.generateButton.grid(column=2, row=1)

        # Cria um Canvas com barra de rolagem
        self.canvas = tk.Canvas(self.janela, width=450, height=100)
        self.canvas.grid(column=0, row=2, columnspan=3)

        self.frame_checkbox = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_checkbox, anchor="nw")

        # Adiciona a barra de rolagem vertical
        scrollbar = ttk.Scrollbar(self.janela, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(column=3, row=2, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

    def acao_botao(self):
        # Abre uma janela de seleção de arquivo
        arquivo_selecionado = filedialog.askopenfilename()
        mover_arquivo(arquivo_selecionado)
        self.fileEntry.delete(0, tk.END)
        self.fileEntry.insert(0, arquivo_selecionado)

    def rastrear_selecao(self, event):
        # Obtém o valor atualmente selecionado na ComboBox
        opcao_selecionada = self.combobox.get()

        if opcao_selecionada == "Média":
            self.media(["teste1", "teste2", "teste3", "teste4", "teste5", "teste6", "teste7"])
        else:
            tk.Label(text="erro").grid()   # Oculta o Label para outras opções

    def media(self, array):
        self.array_itens = array  # Armazena o array para uso posterior

        # Remove as caixas de seleção existentes
        for checkbox in self.frame_checkbox.winfo_children():
            checkbox.destroy()

        # Adiciona caixas de seleção para cada item no array
        for i, item in enumerate(array):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.frame_checkbox, text=item, variable=var)
            checkbox.grid(row=i, sticky="w")

        # Atualiza a região rolável do canvas
        self.frame_checkbox.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    #def generate(self):


def main():
    # Cria uma instância da janela principal
    janela_principal = tk.Tk()

    # Cria uma instância da classe TelaInterclasse
    tela = Interface(janela_principal)

    # Inicia o loop principal
    janela_principal.mainloop()

if __name__ == "__main__":
    main()