import tkinter as tk
from tkinter import ttk, messagebox
from api_client import LeagueStandingsFetcher,MatchScheduleFetcher

class MatchDialog(tk.Toplevel):
    def __init__(self, parent, team_name, matches):
        super().__init__(parent)
        self.title(f"{team_name} 比赛详情")
        self.geometry("800x400")
        
        # 创建表格容器
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建Treeview
        columns = ('date', 'week', 'status', 'team1', 'score', 'team2')
        self.tree = ttk.Treeview(
            container,
            columns=columns,
            show='headings',
            height=15
        )
        
        # 配置列
        column_settings = [
            ('日期', 100),
            ('星期', 60),
            ('状态', 80),
            ('主队', 120),
            ('比分', 80),
            ('客队', 120)
        ]
        
        for idx, (text, width) in enumerate(column_settings):
            self.tree.heading(columns[idx], text=text)
            self.tree.column(columns[idx], width=width, anchor='center')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 插入数据
        for match in matches:
            self.tree.insert('', tk.END, values=(
                match['date'],
                match['week'],
                match['status_text'],
                match['team1'],
                f"{match['team1_score']} - {match['team2_score']}",
                match['team2']
            ))

class pra(ttk.Frame):
    def create_header(self,parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(pady=10)
        
        self.title_label = ttk.Label(header_frame, font=('Arial', 16, 'bold'))
        self.title_label.pack()

    def create_table(self,parent):
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建Treeview表格
        columns = ('rank', 'team', 'WDL', 'G/LG', 'Turn', 'scores')
        
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
        
        self.tree.bind("<Double-1>", self.on_team_click)

    def create_footer(self,parent):
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(pady=5)
        
        refresh_btn = ttk.Button(
            footer_frame,
            text="刷新数据",
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

    def refresh_data(self):
        self.load_data()

    def load_data(self, standings_fetcher, schedule_fetcher):
        try:
            # 获取积分榜数据
            standings_data = standings_fetcher.fetch_standings()
            self.title_label.config(text=standings_data['title'])
            
            # 清空现有数据
            for i in self.tree.get_children():
                self.tree.delete(i)
            
            # 插入新数据
            for team in standings_data['ranking']:
                self.tree.insert('', tk.END, values=(
                    team['rank_id'],
                    team['team'],
                    team['draw'],
                    team['losses'],
                    team['wins'],
                    team['goal_difference']
                ))
            
            # 获取赛程数据
            schedule_data = schedule_fetcher.fetch_matches()
            self.matches_data = self.process_matches(schedule_data['matches'])
            
        except Exception as e:
            messagebox.showerror("错误", f"数据加载失败: {str(e)}")

    def process_matches(self, raw_matches):
        processed = []
        for day in raw_matches:
            for match in day['list']:
                processed.append({
                    'date': day['date'],
                    'week': day['week'],
                    'status_text': match['status_text'],
                    'team1': match['team1'],
                    'team2': match['team2'],
                    'team1_score': match['team1_score'],
                    'team2_score': match['team2_score']
                })
        return processed

    def on_team_click(self, event):
        # 获取点击的球队名称
        
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        column = self.tree.identify_column(event.x)
        if column != "#2":  # 球队列是第二列
            return
            
        item = self.tree.selection()[0]
        team_name = self.tree.item(item, "values")[1]
        
        # 查找相关比赛
        related_matches = [
            m for m in self.matches_data 
            if m['team1'] == team_name or m['team2'] == team_name
        ]
        
        if not related_matches:
            messagebox.showinfo("提示", f"{team_name} 暂无比赛数据")
            return
            
        # 显示详情窗口
        MatchDialog(self,team_name, related_matches)


class StandingsApp(tk.Tk):
    def __init__(self, standings_url, schedule_url):
        super().__init__()
        self.title("足球联赛积分榜")
        self.geometry("1200x700")
        
        # 创建主容器
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        #生成不同联赛的排行表
        League=[("英超","yingchao"),("西甲","xijia"),("德甲","dejia"),("意甲","yijia"),("法甲","fajia")]
        for i, (cn,en) in enumerate(League):
            s=pra() #创建新表格实例
            self.create_standings_tab(cn, s)
            params={
            'key': '3b3813a690fd85a29cacf2014be208c6',
            'type': en,
        }
            self.standings_fetcher = LeagueStandingsFetcher(standings_url, params)
            self.schedule_fetcher = MatchScheduleFetcher(schedule_url, params)
            self.matches_data = None
            # 加载数据
            s.load_data(self.standings_fetcher,self.schedule_fetcher)


    def create_standings_tab(self, text, pra0):
        """创建积分榜标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=text)
        
        pra0.create_header(tab)
        pra0.create_table(tab)
        pra0.create_footer(tab)