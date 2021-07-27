import pandas as pd
from os import listdir

class AllToOneExcel:
    
    def __init__(self, file_dir, reservoir):
        self.dir = file_dir
        self.target = reservoir
        
    def extract(self, file_name):
        return file_name.split('_')[1].split('.')[0]

    def concat(self):
        file_list = listdir(self.dir)
        first_year = self.extract(file_list[0])
        last_year = self.extract(file_list[-1])

        df_total = None
        for file in file_list:
            df = pd.read_csv(self.dir + "\\" + file)
            if not isinstance(df_total, pd.DataFrame):
                df_total = df
            else:
                df_total = pd.concat([df_total, df])
        df_total.to_csv(self.dir + "\\" + "{}_{}~{}.csv".format(self.target, first_year, last_year), index = False)

# dir = "C:\\Users\\user\\Documents\\GitHub\\Reservoir_Crawler\\data\\Shimen_reservoir"
# test = AllToOneExcel(dir, "石門水庫")
# test.concat()
    
    
