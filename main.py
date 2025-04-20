# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from api_client import LeagueStandingsFetcher

class StandingsApp(tk.Tk):
    def __init__(self, api_url,params):
        super().__init__()
        self.title("足球联赛积分榜")
        self.geometry("1200x700")
        
        # 初始化数据获取器
        self.fetcher = LeagueStandingsFetcher(api_url,params)
        
        # 创建界面元素
        self.create_header()
        self.create_table()
        self.create_footer()
        
        # 加载数据
        self.load_data()

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=10)
        
        self.title_label = ttk.Label(header_frame, font=('Arial', 16, 'bold'))
        self.title_label.pack()
        
        self.duration_label = ttk.Label(header_frame, font=('Arial', 12))
        self.duration_label.pack()

    def create_table(self):
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建Treeview表格
        columns = ('rank', 'team', 'wins', 'draw', 'losses', 
                 'goals', 'losing_goals', 'goal_diff', 'scores')
        
        self.tree = ttk.Treeview(
            container,
            columns=columns,
            show='headings',
            selectmode='extended',
            height=20
        )
        
        # 配置列
        column_settings = [
            ('排名', 80),
            ('球队', 150),
            ('胜/平/负', 60),
            ('进/失球', 80),
            ('已赛轮次', 80),
            ('积分', 80)
        ]
        
        for idx, (text, width) in enumerate(column_settings):
            self.tree.heading(columns[idx], text=text)
            self.tree.column(columns[idx], width=width, anchor='center')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_footer(self):
        footer_frame = ttk.Frame(self)
        footer_frame.pack(pady=5)
        
        refresh_btn = ttk.Button(
            footer_frame,
            text="刷新数据",
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def load_data(self):
        try:
            data = self.fetcher.fetch_standings()
            self.title_label.config(text=data['title'])
            self.duration_label.config(text=f"赛季：{data['duration']}")
            
            # 清空现有数据
            for i in self.tree.get_children():
                self.tree.delete(i)
            
            # 插入新数据
            for team in data['ranking']:
                self.tree.insert('', tk.END, values=(
                    team['rank_id'],
                    team['team'],
                    team['draw'],
                    team['losses'],
                    team['wins'],
                    team['goal_difference']
                ))
                
        except Exception as e:
            messagebox.showerror("错误", f"数据加载失败: {str(e)}")

    def refresh_data(self):
        self.load_data()

if __name__ == "__main__":
    # 使用示例数据（实际使用时需要替换为真实API地址）
    API_URL = "http://apis.juhe.cn/fapig/football/rank"
    PARAMS={
    'key': '3b3813a690fd85a29cacf2014be208c6',
    'type': 'yingchao',
}
    # 初始化GUI
    app = StandingsApp(API_URL,PARAMS)
    app.mainloop()
