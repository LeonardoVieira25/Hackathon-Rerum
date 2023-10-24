class LogTransform:
    require = []
    adds = []

    def __init__(self, column):
        self.column = column
        self.require = [column]
        self.adds = ["log_" + column]

    def action(self, df):
        df["log_" + self.column] = df[self.column].apply(lambda x: math.log(x) if x > 0 else 0)
