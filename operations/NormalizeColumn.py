class NormalizeColumn:
    params = [
        "column"
    ]
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["normalized_" + column]

    def action(self, df):
        df["normalized_" + self.column] = (df[self.column] - df[self.column].mean()) / df[self.column].std()
