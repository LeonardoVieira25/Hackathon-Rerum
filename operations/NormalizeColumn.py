# class NormalizeColumn:
#     params = [
#         "column"
#     ]
#     require = []
#     adds = []

#     def __init__(self, column):
#         self.column = column
#         self.require = [column]
#         self.adds = ["normalized_" + column]

#     def action(self, df):
#         df["normalized_" + self.column] = (df[self.column] - df[self.column].mean()) / df[self.column].std()


class NormalizeColumn:
    params = [
        "column"
    ]
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["normalized_" + self.column]
    def action(self, df):
        # Crie um objeto MinMaxScaler para normalização
        # scaler = MinMaxScaler()

        # Ajuste o scaler aos dados nas colunas especificadas
        # df["normalized_" + self.column] = scaler.fit_transform(df[self.column])
        df["normalized_" + self.column] = (df[self.column] - df[self.column].min())/(df[self.column].max() - df[self.column].min())