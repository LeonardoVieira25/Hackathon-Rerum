import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os


DATA_SETS_FOLDER = './dataSets/'
OUT_DTA_FOLDER = './result_files/'

def plot_df_column(df: pd.DataFrame, column_name: str):
    # y_values = df.sort_values(column_name)[column_name]
    y_values = df[column_name]
    x_values = range(len(y_values))
    plt.figure(figsize=(10, 6))  
    plt.plot(x_values, y_values)
    plt.ylabel(column_name)
    plt.show()

def list_csv_files_in_current_folder():
    subfolder_files = [f for f in os.listdir(DATA_SETS_FOLDER) if f.endswith('.csv')]
    return subfolder_files

def print_options(options):
    for i, file in enumerate(options):
        print("[ " + str(i) + " ] " + file)

def one_value_plot(df: pd.DataFrame):
    print(df.head())
    print("==< Colunas disponíveis >==")
    print_options(df.columns.values)
    column_name = df.columns.values[int(input("Selecione a coluna: "))]
    order_by = df.columns.values[int(input("Escolha a coluna para ordenação: (-1 para não ordenar)"))]
    
    if order_by != "-1":
        df = df.sort_values(by=order_by)
    
    # Configurar o estilo do seaborn
    sns.set(style="whitegrid")
    
    # Gráfico de barras
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x=column_name, y=df.index, orient='h')
    plt.xlabel(column_name)
    plt.ylabel("Índice")
    plt.title(f'Gráfico de {column_name}')
    plt.show()

def two_values_plot(df: pd.DataFrame):
    print(df.head())
    print("==< colunas disponíveis >==")
    print_options(df.columns.values)
    column_name_x = df.columns.values[int(input("Selecione a coluna do eixo x: "))]
    column_name_y = df.columns.values[int(input("Selecione a coluna do eixo y: "))]
    if column_name_x == column_name_y:
        return
    order_by = df.columns.values[int(input("Escolha a coluna para ordenação: (-1 para não ordenar)"))]
    if order_by != "-1":
        df = df.sort_values(by=order_by)
    y_values = df[column_name_y]
    x_values = df[column_name_x]
    print(df.head())
    
    sns.set()  # Configuração padrão do Seaborn

    plt.figure(figsize=(10, 6))
    # Substitui plt.scatter por sns.scatterplot para melhor apresentação
    sns.scatterplot(x=x_values, y=y_values, palette="viridis", alpha=0.7)

    plt.xlabel(column_name_x)
    plt.ylabel(column_name_y)
    plt.title(f"Gráfico de Dispersão: {column_name_x} vs {column_name_y}")
    plt.show()


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
        print(df.head())

def verifica_receita(df_columns: np.ndarray, receita: list):
    campos = df_columns
    for passo in receita: #! verifica se todos os passos possuem os requirements 
        if contains_all_elements(campos, passo.require):
            campos = np.append(campos, passo.adds)
        else:
            return type(passo), None
    return True, campos

def get_svg_encoding(file_name): #! não esta reconhecendo adequadamente 
    try:
        with open(DATA_SETS_FOLDER+file_name, 'rb') as file:
            first_4_bytes = file.read(4)
            if first_4_bytes == b'\x3C\x3F\x78\x6D':
                return "UTF-8"
            elif first_4_bytes == b'\x00\x00\xFE\xFF':
                return "UTF-32-BE"
            elif first_4_bytes == b'\xFF\xFE\x00\x00':
                return "UTF-32-LE"
            elif first_4_bytes == b'\xFE\xFF':
                return "UTF-16-BE"
            elif first_4_bytes == b'\xFF\xFE':
                return "UTF-16-LE"
            else:
                return "Unknown"
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error: {str(e)}"

def detect_csv_delimiter(filename, encoding):
    delimiters = [',', ';', '\t', '|']  # Lista de delimitadores a serem testados

    for delimiter in delimiters:
        try:
            df = pd.read_csv(DATA_SETS_FOLDER+filename, sep=delimiter, nrows=2, encoding=encoding)
            if len(df.columns) > 1:
                print(df.head())
                return delimiter
        except pd.errors.EmptyDataError:
            pass
        except pd.errors.ParserError:
            pass
    return False

def is_numeric(value):
    return isinstance(value, (int, float, complex))

def load_operations():
    # Os operadores (funções de ação sobre o df), são carregados aqui. cada arquivo contém uma classe com o mesmo nome do arquivo
    # representando uma operação. A classe deve conter os atributos: params, require, adds e o método action.
    # operations é um dicionário que mapeia o nome da operação para a classe da operação
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
    receita_valida, colunas_validas = verifica_receita(df.columns.values, receita) # verifica se é possível adicionar a operação na receita atual
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
    
def listar_receita(receita):
    if(len(receita) == 0):
        print("A receita atual esta vazia!")
    for passo in receita:
        print(passo.__class__.__name__+": ", end=" ")
        variables = [i for i in dir(passo) if not callable(i)]
        # variables.remove(["__class__", "__delattr__", "__dict__", "__dir__", "__doc__", "__eq__", "__format__", "__ge__", "__getattribute__", "__getstate__", "__gt__", "__hash__", "__init__", "__init_subclass__", "__le__", "__lt__", "__module__", "__ne__", "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__", "__str__", "__subclasshook__", "__weakref__", "action", "adds", "params"])
        for attr in ["__class__", "__delattr__", "__dict__", "__dir__", "__doc__", "__eq__", "__format__", "__ge__", "__getattribute__", "__getstate__", "__gt__", "__hash__", "__init__", "__init_subclass__", "__le__", "__lt__", "__module__", "__ne__", "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__", "__str__", "__subclasshook__", "__weakref__", "action", "adds", "params"]:
            if attr in variables:
                variables.remove(attr)
        for param in variables:
            print(param+": "+str(passo.__dict__[param]), end=", ")
        print("")





def main():
    csv_files = list_csv_files_in_current_folder()
    updated_receita = False

    print("==< arquivos disponíveis >==")
    print_options(["Sair"]+csv_files)

    file_index = int(input("\nSelecione o arquivo: "))
    if file_index == 0:
        return
    else:
        file_index -= 1

    print(DATA_SETS_FOLDER + csv_files[file_index])
    encoding_detected = "latin-1"
    # encoding_detected = get_svg_encoding(csv_files[file_index])
    delimiter_detected = detect_csv_delimiter(csv_files[file_index], encoding_detected)
    print(delimiter_detected)
    print(encoding_detected)

    df = pd.read_csv(DATA_SETS_FOLDER + csv_files[file_index], encoding=encoding_detected, delimiter=delimiter_detected)
    
    operations = load_operations() # dicionário com as operações(funções) disponíveis
    receita = []
    u_input = 1

    while u_input > 0:
        print("\n==< opções >==")
        print_options([
            "Sair",
            "Visualizar gráfico com um único parâmetro",
            "Visualizar gráfico com dois parâmetros",
            "Adicionar Operações",
            "Salvar tabela",
            "Listar receita",
            "Analise de período"
        ])

        u_input = int(input())

        list_subset = []

        match u_input:
            case 0: # Sair
                continue

            case 1: # Visualizar gráfico com um único parâmetro
                receita_state, colunas_validas  = verifica_receita(df.columns.values, receita)
                if receita_state == True:
                    df_baked = df.copy()
                    if(updated_receita):
                        executa_receita(receita, df_baked)
                        updated_receita = False
                    one_value_plot(df_baked)
                else:
                    print("Erro com o passo "+str(receita_state))
                continue

            case 2: # Visualizar gráfico com dois parâmetros
                receita_state, colunas_validas  = verifica_receita(df.columns.values, receita)
                if receita_state == True:
                    df_baked = df.copy()
                    executa_receita(receita, df_baked)
                    two_values_plot(df_baked)
                else:
                    print("Erro com o passo "+str(receita_state))
                continue

            case 3: # Adicionar Operações
                novo_passo = seleciona_novo_passo(operations, receita, df)
                if novo_passo != False:
                    receita.append(novo_passo)
                    updated_receita = True
                else:
                    print("Operação incompatível com a receita atual! Verifique seus parâmetros.")

            case 4: # Salvar tabela
                out_file_name = str(input("Nome do arquivo: "))
                receita_state, colunas_validas  = verifica_receita(df.columns.values, receita)
                if receita_state == True:
                    df_baked = df.copy()
                    executa_receita(receita, df_baked)
                    order_by = df_baked.columns.values[int(input("Escolha a coluna para ordenação: (-1 para não ordenar)"))]
                    if order_by != "-1":
                        df_baked = df_baked.sort_values(by=order_by)
                    df_baked.to_csv(OUT_DTA_FOLDER + out_file_name + ".csv")
                else:
                    print("Erro com o passo "+str(receita_state))
                continue

            case 5: # Listar receita
                listar_receita(receita)

            case 6: # Analise de período
                    
                # adicionando escolha do intervalo
                meses_em_portugues = {
                'jan': 'Jan',
                'fev': 'Feb',
                'mar': 'Mar',
                'abr': 'Apr',
                'mai': 'May',
                'jun': 'Jun',
                'jul': 'Jul',
                'ago': 'Aug',
                'set': 'Sep',
                'out': 'Oct',
                'nov': 'Nov',
                'dez': 'Dec'
                }
                df['Data'] = df['Data'].str.replace('/', '-', regex=False)  # Substitua "/" por "-"
                df['Data'] = df['Data'].str[:3].map(meses_em_portugues) + df['Data'].str[3:]  # Mapeie os nomes dos meses
                df['Data'] = pd.to_datetime(df['Data'], format='%b-%y')  # Converta as datas para datetime


                print("Início do período: " + str(df['Data'].min().strftime('%b-%Y')))
                print("Fim do período: " + str(df['Data'].max().strftime('%b-%Y')))


                data_inicial_str = input("Escolha uma data de inicio (formato Oct-01):")
                data_final_str = input("Escolha uma data de fim (formato Oct-01):")

                data_inicial = pd.to_datetime(data_inicial_str, format='%b-%y')
                data_final = pd.to_datetime(data_final_str, format='%b-%y')

                subdf = df.loc[(df['Data'] >= data_inicial) & (df['Data'] <= data_final)]

                print("\n==< opções >==")
                print_options([
                    "Sair",
                    "Visualizar gráfico com um único parâmetro",
                    "Visualizar gráfico com dois parâmetros",
                ])

                internal_input = int(input())
                
                match internal_input:
                    case 0: # Sair
                        continue

                    case 1: # Visualizar gráfico com um único parâmetro
                        receita_state, colunas_validas  = verifica_receita(subdf.columns.values, receita)
                        if receita_state == True:
                            subdf_baked = subdf.copy()
                            if(updated_receita):
                                executa_receita(receita, subdf_baked)
                                updated_receita = False
                            one_value_plot(subdf_baked)
                        else:
                            print("Erro com o passo "+str(receita_state))
                        continue

                    case 2: # Visualizar gráfico com dois parâmetros
                        receita_state, colunas_validas  = verifica_receita(subdf.columns.values, receita)
                        if receita_state == True:
                            subdf_baked = subdf.copy()
                            executa_receita(receita, subdf_baked)
                            two_values_plot(subdf_baked)
                        else:
                            print("Erro com o passo "+str(receita_state))
                        continue





# def init_operator(filename):
#     delimiter, first_column = detect_csv_delimiter(filename)
#     df = pd.read_csv(DATA_SETS_FOLDER + filename, encoding='latin-1', low_memory=False, delimiter=delimiter)
#     global_df = df
# def get_operations_names():
#     return global_operations
# global_operations = 0
# global_df = 0


if __name__ == "__main__":
    # load operations
    main()



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
