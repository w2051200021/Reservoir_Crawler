# Reservoir_Crawler
以Python實作網路爬蟲，抓取[台灣地區主要水庫蓄水量報告表](https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx)資料。該網站提供全臺各地水庫數據，包含水庫基本數據、每日蓄水統計、即時水情資料。此專案目的為方便使用者取得特定水庫的長時間的每日資料，例如：2010/1/1~2020/12/31。

![alt 文字](https://github.com/w2051200021/Reservoir_Crawler/blob/main/description/figure_1.PNG "網站示意圖")

### 使用說明
1. Import the package, input your target reservoir, file directory and instantiate 'Crawler' class. For example,
```Python
import crawler

target = "石門水庫" 
dir = r"C:\Users\user\Documents\GitHub\Reservoir_Crawler\data\Shimen_Reservoir"

crawler = crawler.Crawler(
            reservoir = target,
            file_dir = dir
        )
```

2. Input the time interval and start the crawler.
```Python
start_time = [2010, 1, 1] # year/month/day
end_time = [2020, 12, 31]

crawler.get_data(
            start_time = start_time,
            end_time = end_time
        )
```


