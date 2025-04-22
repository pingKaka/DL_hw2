from data_process import StandingsApp

if __name__ == "__main__":
    # 使用示例API地址
    STANDINGS_API = "http://apis.juhe.cn/fapig/football/rank"
    SCHEDULE_API = "http://apis.juhe.cn/fapig/football/query"

    app = StandingsApp(STANDINGS_API, SCHEDULE_API)
    app.mainloop()
