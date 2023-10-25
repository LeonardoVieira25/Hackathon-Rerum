class Volatility:
    params = [
        "column",
        "look_back_period",  # Número de períodos anteriores a serem considerados
        "look_forward_period",  # Número de períodos posteriores a serem considerados
    ]
    require = []
    adds = []

    def __init__(self, column, look_back_period, look_forward_period):
        self.column = column
        self.look_back_period = look_back_period
        self.look_forward_period = look_forward_period
        self.require = [column]
        self.adds = ["volatility_" + column]

    def action(self, df):
        # Função para calcular a volatilidade com base nos dados anteriores e posteriores
        def calculate_volatility(row):
            start_index = max(0, row.name - self.look_back_period)
            end_index = min(len(df) - 1, row.name + self.look_forward_period)
            selected_values = df[self.column][start_index:end_index + 1]
            return selected_values.std()

        df["volatility_" + self.column] = df.apply(calculate_volatility, axis=1)
