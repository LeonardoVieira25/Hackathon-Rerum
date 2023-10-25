class FilterOutliers:
    params = [
        "column"
    ]
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
