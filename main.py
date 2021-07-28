import crawler

target = "石門水庫"
# dir = r"C:\Users\user\Documents\GitHub\Reservoir_Crawler\data\Deji_Reservoir"
dir = r"C:\Users\user\Desktop\碩一\碩一下\Python practices"

crawler = crawler.Crawler(
            reservoir = target,
            file_dir = dir
        )

start_time = [2003, 1, 1]
end_time = [2020, 12, 31]

crawler.get_data(
            start_time = start_time,
            end_time = end_time
        )