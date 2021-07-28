import crawler

target = "德基水庫"
dir = r"C:\Users\user\Documents\GitHub\Reservoir_Crawler\data\Deji_Reservoir"

start_time = [2003, 1, 1]
end_time = [2004, 7, 28]

crawler = crawler.Crawler(
            reservoir = target,
            file_dir = dir
        )

crawler.get_data(
            start_time = start_time,
            end_time = end_time
        )