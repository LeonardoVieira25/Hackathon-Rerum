class StdDeviation:
    params = [
        "column",
    ]
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["std_deviation_" + column]

    def action(self, df):
        df["std_deviation_" + self.column] = df[self.column].std()
