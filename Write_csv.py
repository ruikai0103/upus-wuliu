from pandas import DataFrame


class Write_csv:
    def __init__(self):
        self.to_csv = ""
        self.mode = "a"
        self.header = False
        self.index = False
        self.value_title = [['单号', '状态', '签收时间', '签收物流', '开始时间', '开始物流', '第二时间', '第二物流', ]]

    def write_excel(self, *args):
        value = [*args]
        data_df = DataFrame(value)
        data_df.to_csv(self.to_csv, index=self.index, mode=self.mode, header=self.header)

    def create_csv(self):
        data_df = DataFrame(self.value_title)
        data_df.to_csv(self.to_csv, index=self.index, mode=self.mode, header=self.header)
