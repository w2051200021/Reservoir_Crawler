import os
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, timedelta
from all_to_one import AllToOneExcel

class Get:
    
    def __init__(self, url: str):
        self.session = requests.session()
        while True:
            try:
                self.response = self.session.get(url, headers = self.headers)
                break
            except:
                rand = np.random.randint(low = 10, high = 30)
                print('-------Get got caught! Take a nap for {} sec.-------'.format(rand))
                time.sleep(rand)###
               
        
    @property
    def headers(self):
        return {
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36"
        }
    @property
    def soup(self):
        return BeautifulSoup(self.response.text, "html.parser")

class Post:
    
    def __init__(self, url: str, date):
        self._get = Get(url)
        self._soup = self._get.soup
        self.session = self._get.session
        self._date = date
     
    
    def get_payload(self):
        payload = {
                "__VIEWSTATE": self._soup.find_all(id = "__VIEWSTATE")[0]["value"],
                "ctl00$cphMain$cboSearch": "所有水庫", 
                "ctl00$cphMain$ucDate$cboYear": str(self._date.year),
                "ctl00$cphMain$ucDate$cboMonth": str(self._date.month), 
                "ctl00$cphMain$ucDate$cboDay": str(self._date.day),
        }
        return payload
    
    @property    
    def post_data(self):
        while True:
            try:
                response = self.session.post(url, data = self.get_payload())
                table = pd.read_html(response.text, encoding = "utf-8")[0]
                return table
            except:
                rand = np.random.randint(low = 10, high = 30)
                print('-------Post got caught! Take a nap for {} sec.-------'.format(rand))
                time.sleep(rand)###
                self._get = Get(url)

        
class Crawler:

    def __init__(self, url: str, reservoir: str, file_dir: str):
        self.url = url
        self.target = reservoir
        self.dir = file_dir
    
    def get_data(self, start_time: str, end_time: list, concat: bool):
        if end_time == start_time:
            print("No Data!")
            return None
        
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        run = True
        temp_date = date(*start_time)
        target_condition = self.target 
        file_num = start_time[0]
        df = None
        total_timer = time.time()
        timer = time.time()
        print('Start the crawler.')
        
        while run:
            
            stop_condition = (temp_date == date(*end_time) + timedelta(days = 1)) 
            reset_condition = (temp_date.year == file_num + 1 and temp_date.month == 1 and temp_date.day == 1)
            
            if stop_condition:
                run = False 
                df = self.processing(df)
                df.to_csv(self.dir + "\\{}_{}.csv".format(self.target, file_num), index = False)
                print('Done. Total running time:', timedelta(seconds = round(time.time() - total_timer)))
            elif reset_condition:
                df = self.processing(df)
                df.to_csv(self.dir + "\\{}_{}.csv".format(self.target, file_num), index = False)
                print('Done {}. Running time:'.format(file_num), timedelta(seconds = round(time.time() - timer)))
                file_num += 1
                reset = True
                timer = time.time()

                
            post = Post(self.url, temp_date).post_data
            raw_data = post[post.iloc[:, 0] == target_condition].iloc[:, 1:-1]
            raw_data[("_", "日期")] = "{}/{}/{}".format(temp_date.year, temp_date.month, temp_date.day)
            
            if not isinstance(df, pd.DataFrame) or reset_condition:
                df = raw_data
            else:
                df = pd.concat([df, raw_data], axis = 0)   
            temp_date += timedelta(days = 1)
        
        if concat:
            
            executor = AllToOneExcel(self.dir, self.target)
            executor.concat()


    def to_hour(self, string):
        if string != '--':
            hour = string[:-2].replace("(", "-").split("-")[3]
            if len(hour) == 1:
                return "0{}:00".format(hour)
            else:
                return "{}:00".format(hour)
                
                
    def processing(self, df):
        col_names = [col[1] for col in df.columns]
        df.columns = col_names
        del df["統計時間"]
        df['水情時間'] = df['水情時間'].apply(self.to_hour)
        df.iloc[:, -2] = df.iloc[:, -2].apply(lambda x: x.replace("%", ""))
        df = pd.concat([df.iloc[:, -1], df.iloc[:, :-1]], axis = 1)
        col_names = [
                    "Date",
                    "Storage Capacity(10000m^3)",
                    "Precipitation(mm)",
                    "Inflow(10000m^3)",
                    "Outflow(10000m^3)",
                    "Water Level Difference(m)",
                    "Real-Time",
                    "Water Level(m)",
                    "Useful Storage(10000m^3)",
                    "Storage Ratio(%)"
        ]
        df.columns = col_names
        return df
        

url = "https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx"


target = "曾文水庫"
dir = "C:\\Users\\user\\Documents\\GitHub\\Reservoir_Crawler\\data\\Zengwen_Reservoir"

crawler = Crawler(
            url = url,
            reservoir = target,
            file_dir = dir
        )

crawler.get_data(
            start_time = [2003, 1, 1],
            end_time = [2021, 7, 27],
            concat = True
        )


