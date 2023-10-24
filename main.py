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

def import_operation(operations):
    mod = __import__("operations")
    for operation in operations[1:]:
        mod = getattr(mod, operation)
    return mod


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

def detect_csv_delimiter(filename):
    delimiters = [',', ';', '\t', '|']  # Lista de delimitadores a serem testados

    for delimiter in delimiters:
        try:
            df = pd.read_csv("./dataSets/"+filename, sep=delimiter, nrows=1)
            print("delimiter")
            print(delimiter)
            return delimiter, df.columns[0] if len(df.columns) > 0 else None
        except:
            pass
    return None, None  # Se nenhum delimitador for detectado

def is_numeric(value):
    return isinstance(value, (int, float, complex))

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

def main():
    csv_files = list_csv_files_in_current_folder()
    print("==< arquivos disponíveis >==")
    print_options(csv_files)
    file_index = int(input("Selecione o arquivo: "))
    print(DATA_SETS_FOLDER + csv_files[file_index])
    delimiter, first_column = detect_csv_delimiter(csv_files[file_index])
    df = pd.read_csv(DATA_SETS_FOLDER + csv_files[file_index], encoding='latin-1', low_memory=False, delimiter=delimiter)
    
    print("==< colunas disponíveis >==")
    print_options(df.columns.values[1:])
    column_name = df.columns.values[int(input("Selecione a coluna: "))]
    
    operations = load_operations()
    receita = [
        operations["FilterOutliers"](column_name)
        # AddMediaN(column_name, 10),
        # SomaColunas("media_n_"+str(10),column_name),
        # MeanColumns(column_name,"in_apple_playlists"),
        # NormalizeColumn(column_name),
        # MovingAverage(column_name, 10),
        # FilterOutliers("normalized_"+column_name)
        # LogTransform(column_name),
        # MovingAverage("log_"+column_name, 10),
        ]

    receita_state = verifica_receita(df.columns.values, receita)
    if receita_state == True:
        executa_receita(receita, df)
    else:
        print("Erro com o passo "+str(receita_state))

    while True:
        one_value_plot(df)






if __name__ == "__main__":
    # load operations
    main()