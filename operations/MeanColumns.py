class MeanColumns:
    params = [
        "column1",
        "column2"
    ]
    require = []
    adds = []

    def __init__(self, column1, column2):
        self.column1 = column1
        self.column2 = column2
        self.require = [column1, column2]
        self.adds = ["mean(" + self.column1 + "," + self.column2 + ")"]
        # print("mean(" + self.column1 + "," + self.column2 + ")")
    def action(self, df):
        df["mean(" + self.column1 + "," + self.column2 + ")"] = (df[self.column1] + df[self.column2]) / 2
