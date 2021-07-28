import pandas as pd
from os import listdir

class AllToOneExcel:
    
    def __init__(self, file_dir, reservoir):
        self.dir = file_dir
        self.target = reservoir
        
    def extract_year(self, file_name):
        return file_name.split('_')[1].split('.')[0]
    
    def find_target_csv(self):
        raw_file_list = listdir(self.dir)
        return [file for file in raw_file_list if file.startswith(self.target) and file.endswith('.csv')]
    
    def concat(self):
        file_list = self.find_target_csv()
        first_year = self.extract_year(file_list[0])
        last_year = self.extract_year(file_list[-1])

        df_total = None
        for file in file_list:
            df = pd.read_csv(self.dir + "\\" + file)
            if not isinstance(df_total, pd.DataFrame):
                df_total = df
            else:
                df_total = pd.concat([df_total, df])
        df_total.to_csv(self.dir + "\\" + "{}_{}~{}.csv".format(self.target, first_year, last_year), index = False)
