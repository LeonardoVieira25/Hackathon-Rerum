class MaxValue:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["max_" + column]

    def action(self, df):
        df["max_" + self.column] = df[self.column].max()