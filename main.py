import crawler

url = "https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx"
target = "德基水庫"
dir = r"C:\Users\user\Documents\GitHub\Reservoir_Crawler\data\Deji_Reservoir"

crawler = crawler.Crawler(
            url = url,
            reservoir = target,
            file_dir = dir
        )

crawler.get_data(
            start_time = [2008, 1, 1],
            end_time = [2021, 7, 28]
        )