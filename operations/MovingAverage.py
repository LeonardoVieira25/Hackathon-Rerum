class MovingAverage:
    params = [
        "column",
        "window_size"
    ]
    require = []
    adds = []

    def __init__(self, column, window_size):
        self.column = column
        self.window_size = window_size
        self.require = [column]
        self.adds = ["moving_avg_"+ str(window_size) + "_" + column]
    def action(self, df):
        df["moving_avg_" + self.column] = df[self.column].rolling(window=self.window_size).mean()
