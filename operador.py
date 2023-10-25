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

def verifica_receita(df_columns: np.ndarray, receita: list):
    print("receita na função")
    print(receita)
    campos = df_columns
    for passo in receita: #! verifica se todos os passos possuem os requirements 
        if contains_all_elements(campos, passo.require):
            campos = np.append(campos, passo.adds)
        else:
            return type(passo)
    return True, campos

def detect_csv_delimiter(filename):
    delimiters = [',', ';', '\t', '|']  # Lista de delimitadores a serem testados

    for delimiter in delimiters:
        try:
            df = pd.read_csv("./dataSets/"+filename, sep=delimiter, nrows=1)
            if len(df.columns) > 0:
                return delimiter 
        except:
            pass
    return False  # Se nenhum delimitador for detectado

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

def seleciona_novo_passo(operations, receita, df):
    keys = list(operations.keys())
    print("Selecione uma operação")
    print_options(keys)
    op = int(input())
    params = operations[keys[op]].params
    receita_valida, colunas_validas = verifica_receita(df.columns.values, receita)
    valores_lidos = {}
    for param in params:
        valor = 0
        if param.startswith("column"):
            print_options(colunas_validas)
            valor = colunas_validas[ int( input(f"'{param}': ") ) ] #! ler colunas
        else:
            valor = int(input(f"'{param}': "))

        valores_lidos[param] = valor
    newOperation = operations[keys[op]](*valores_lidos.values())
    test_receita = receita.copy()
    test_receita.append(newOperation)
    receita_valida, colunas_validas = verifica_receita(df.columns.values, test_receita) 
    if receita_valida:
        return newOperation
    else:
        return False

def main():
    csv_files = list_csv_files_in_current_folder()
    print("==< arquivos disponíveis >==")
    print_options(csv_files)
    file_index = int(input("Selecione o arquivo: "))
    print(DATA_SETS_FOLDER + csv_files[file_index])
    delimiter, first_column = detect_csv_delimiter(csv_files[file_index])
    df = pd.read_csv(DATA_SETS_FOLDER + csv_files[file_index], encoding='latin-1', low_memory=False, delimiter=delimiter)
    
    # print("==< colunas disponíveis >==")
    # print_options(df.columns.values[1:])
    # column_name = df.columns.values[int(input("Selecione a coluna: "))]
    
# # adicionando escolha do intervalo
#     meses_em_portugues = {
#     'jan': 'Jan',
#     'fev': 'Feb',
#     'mar': 'Mar',
#     'abr': 'Apr',
#     'mai': 'May',
#     'jun': 'Jun',
#     'jul': 'Jul',
#     'ago': 'Aug',
#     'set': 'Sep',
#     'out': 'Oct',
#     'nov': 'Nov',
#     'dez': 'Dec'
# }
#     df['Data'] = df['Data'].str.replace('/', '-', regex=False)  # Substitua "/" por "-"
#     df['Data'] = df['Data'].str[:3].map(meses_em_portugues) + df['Data'].str[3:]  # Mapeie os nomes dos meses
#     df['Data'] = pd.to_datetime(df['Data'], format='%b-%y')  # Converta as datas para datetime


#     data_inicial_str = input("Escolha uma data de inicio (formato Oct-01):")
#     data_final_str = input("Escolha uma data de fim (formato Oct-01):")

#     # Converta as strings de entrada para o formato correto antes de usar pd.to_datetime
#     data_inicial = pd.to_datetime(data_inicial_str, format='%b-%y')
#     data_final = pd.to_datetime(data_final_str, format='%b-%y')

#     # Use a função .loc para selecionar as linhas dentro do intervalo.
#     linhas_no_intervalo = df.loc[(df['Data'] >= data_inicial) & (df['Data'] <= data_final)]
        
#     print(linhas_no_intervalo)
    operations = load_operations()
    global_operations = operations
    receita = []
    u_input = 1
    while u_input > 0:
        print("==< opções >==")
        print_options([
            "Sair",
            "Adicionar Operações"
        ])
        u_input = int(input())
        match u_input:
            case 0: 
                continue
            case 1:
                novo_passo = seleciona_novo_passo(operations, receita, df)
                if novo_passo != False:
                    receita.append(novo_passo)
                else:
                    print("Operação incompatível com a receita atual! Verifique seus parâmetros.")

    receita_state, colunas_validas  = verifica_receita(df.columns.values, receita)
    if receita_state == True:
        executa_receita(receita, df)
    else:
        print("Erro com o passo "+str(receita_state))

    while True:
        one_value_plot(df)

def init_operator(filename):
    delimiter, first_column = detect_csv_delimiter(filename)
    df = pd.read_csv(DATA_SETS_FOLDER + filename, encoding='latin-1', low_memory=False, delimiter=delimiter)
    global_df = df
def get_operations_names():
    return global_operations


global_operations = 0
global_df = 0
if __name__ == "__main__":
    # load operations
    main()