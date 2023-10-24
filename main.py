import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_SETS_FOLDER = './dataSets/'

def plot_df_column(df: pd.DataFrame, column_name: str):
    y_values = df.sort_values(column_name)[column_name]
    x_values = range(len(y_values))
    plt.figure(figsize=(10, 6))  
    plt.plot(x_values, y_values)
    plt.show()

import os
def list_csv_files_in_current_folder():
    subfolder_files = [f for f in os.listdir(DATA_SETS_FOLDER) if f.endswith('.csv')]
    return subfolder_files

def print_options(options):
    for i, file in enumerate(options):
        print("[ " + str(i) + " ] " + file)


def one_value_plot(df: pd.DataFrame):
    print("==< colunas disponíveis >==")
    print_options(df.columns.values)
    column_name = df.columns.values[int(input("Selecione a coluna: "))]
    plot_df_column(df,column_name)

def media_n(series: np.ndarray):
    return np.mean(series)

def add_media_n_column(df, target_column_name, n_size):
    new_column = []
    for i in range(0,len(df)):
        if(len(df[target_column_name]) >= n_size):
            new_column.append(media_n(df[target_column_name][i:i+n_size]))
    df["media_n_"+str(n_size)] = new_column



OPTIONS = {
    "add_n_colunas": {
        "n": 0
    },
    "sum_colunas": {
        "col1": "",
        "col2": "",
    }
}

class AddMediaN:
    require = []
    adds = []

    def __init__(self, column, n_size):
        self.column = column
        self.n_size = n_size
        self.require = [column]
        self.adds = ["media_n_"+str(n_size)]

    def action(self, df):
        new_column = []
        for i in range(0,len(df)):
            if(len(df[self.column]) >= self.n_size):
                new_column.append(media_n(df[self.column][i:i+self.n_size]))
        df["media_n_"+str(self.n_size)] = new_column

class SomaColunas:
    require = []
    adds = []

    def __init__(self, column1, column2):
        self.column1 = column1
        self.column2 = column2
        self.require = [column1, column2]
        self.adds = ["sum_"+self.column1+"_"+self.column2]

    def action(self, df):
        df["sum_"+self.column1+"_"+self.column2] = df[self.column1] + df[self.column2]
        




def contains_all_elements(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    return set2.issubset(set1)
def executa_receita(receita, df):
    for passo in receita: #! efetua todas as actions da receita
        passo.action(df)
def verifica_receita(df_columns: np.ndarray, receita):
    campos = df_columns
    for passo in receita: #! verifica se todos os passos possuem os requirements 
        if contains_all_elements(campos, passo.require):
            campos = np.append(campos, passo.adds)
        else:
            return type(passo)
    return True

def main():
    csv_files = list_csv_files_in_current_folder()
    print("==< arquivos disponíveis >==")
    print_options(csv_files)
    file_index = int(input("Selecione o arquivo: "))
    df = pd.read_csv(DATA_SETS_FOLDER + csv_files[file_index], encoding='latin-1', low_memory=False)

    print("==< colunas disponíveis >==")
    print_options(df.columns.values)
    column_name = df.columns.values[int(input("Selecione a coluna: "))]
    # print(type(df[column_name].values[0]) == np.int64 or type(df[column_name].values[0]) == np.float64) #! verifica se é um número

    receita = [
        AddMediaN(column_name, 10),
        SomaColunas("media_n_"+str(10),column_name)
        ]

    # print("verifica_receita(df.columns.values, receita)")
    # print(verifica_receita(df.columns.values, receita))
    receita_state = verifica_receita(df.columns.values, receita)
    if verifica_receita(df.columns.values, receita) == True:
        executa_receita(receita, df)
    else:
        print("Erro com o passo "+str(receita_state))
    # print_options(dfb.columns.values)
    one_value_plot(df)

    # add_media_n_column(df, column_name, 10)
    # plot_df_column(df, column_name)
    

    
    





if __name__ == "__main__":
    main()