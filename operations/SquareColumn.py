class SquareColumn:
    params = [
        "column"
    ]
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["square_" + column]

    def action(self, df):
        df["square_" + self.column] = df[self.column] ** 2
