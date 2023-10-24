import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATA_SETS_FOLDER = './dataSets/'

def plot_df_column(df: pd.DataFrame, column_name: str):
    # y_values = df.sort_values(column_name)[column_name]
    y_values = df[column_name]
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

def import_operation(operations):
    mod = __import__("operations")
    for operation in operations[1:]:
        mod = getattr(mod, operation)
    return mod


class MeanColumns:
    require = []
    adds = []

    def __init__(self, column1, column2):
        self.column1 = column1
        self.column2 = column2
        self.require = [column1, column2]
        self.adds = ["mean(" + self.column1 + "," + self.column2 + ")"]
    def action(self, df):
        df["mean(" + self.column1 + "," + self.column2 + ")"] = (df[self.column1] + df[self.column2]) / 2
class MaxValue:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["max_" + column]

    def action(self, df):
        df["max_" + self.column] = df[self.column].max()
class MinValue:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["min_" + column]

    def action(self, df):
        df["min_" + self.column] = df[self.column].min()

class SquareColumn:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["square_" + column]

    def action(self, df):
        df["square_" + self.column] = df[self.column] ** 2

class LogTransform:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["log_" + column]

    def action(self, df):
        df["log_" + self.column] = df[self.column].apply(lambda x: math.log(x) if x > 0 else 0)

class NormalizeColumn:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["normalized_" + column]

    def action(self, df):
        df["normalized_" + self.column] = (df[self.column] - df[self.column].mean()) / df[self.column].std()

class FilterOutliers:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["filtered_" + column]

    def action(self, df):
        # Calcular a média e o desvio padrão da coluna
        mean = df[self.column].mean()
        std_dev = df[self.column].std()

        # Definir limites para os outliers com base no desvio padrão
        lower_bound = mean - 2 * std_dev  # 2 desvios padrão abaixo da média
        upper_bound = mean + 2 * std_dev  # 2 desvios padrão acima da média

        # Filtrar os valores que estão fora dos limites
        df["filtered_" + self.column] = df[self.column].apply(lambda x: x if lower_bound <= x <= upper_bound else mean)

class MovingAverage:
    require = []
    adds = []

    def __init__(self, column, window_size):
        self.column = column
        self.window_size = window_size
        self.require = [column]
        self.adds = ["moving_avg_" + column]

    def action(self, df):
        df["moving_avg_" + self.column] = df[self.column].rolling(window=self.window_size).mean()


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
        # AddMediaN(column_name, 10),
        SomaColunas("media_n_"+str(10),column_name),
        # MeanColumns(column_name,"in_apple_playlists"),
        # NormalizeColumn(column_name),
        # MovingAverage(column_name, 10),
        # FilterOutliers("normalized_"+column_name)
        # LogTransform(column_name),
        # MovingAverage("log_"+column_name, 10),
        ]

    # print("verifica_receita(df.columns.values, receita)")
    # print(verifica_receita(df.columns.values, receita))
    receita_state = verifica_receita(df.columns.values, receita)
    if receita_state == True:
        executa_receita(receita, df)
    else:
        print("Erro com o passo "+str(receita_state))

    while True:
        one_value_plot(df)


def load_operations():
    operations = {}
    import importlib
    operations_list = [f[:-3] for f in os.listdir("operations") if f.endswith(".py")]
    for operation in operations_list:
        module_name = f"operations.{operation}"
        module = importlib.import_module(module_name)
        class_obj = getattr(module, operation)
        operations[operation] = class_obj    
    return operations



# if __name__ == "__main__":
    #load operations
    # main()