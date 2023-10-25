class MinValue:
    params = [
        "column",
    ]
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["min_" + column]

    def action(self, df):
        df["min_" + self.column] = df[self.column].min()
