class SomaColunas:
    require = []
    adds = []

    def __init__(self, column1, column2):
        self.column1 = column1
        self.column2 = column2
        self.require = [column1, column2]
        self.adds = ["sum_"+self.column1+"_"+self.column2]

    def action(self, df):
        df["sum("+self.column1+","+self.column2+")"] = df[self.column1] + df[self.column2]
