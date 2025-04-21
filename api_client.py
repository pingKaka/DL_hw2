# api_client.py
import requests

class LeagueStandingsFetcher:
    def __init__(self, api_url, params):
        self.api_url = api_url
        self.params= params

    def fetch_standings(self):
        try:
            response = requests.get(self.api_url, self.params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('error_code') != 0:
                raise Exception(data.get('reason', 'Unknown API error'))
                
            return {
                'title': data['result']['title'],
                'duration': data['result']['duration'],
                'ranking': data['result']['ranking']
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except KeyError as e:
            raise Exception(f"数据解析错误: 缺少必要字段 {str(e)}")


class MatchScheduleFetcher:
    def __init__(self, api_url, params):
        self.api_url = api_url
        self.params = params

    def fetch_matches(self):
        try:
            response = requests.get(self.api_url, self.params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('error_code') != 0:
                raise Exception(data.get('reason', 'Unknown API error'))
                
            return {
                'title': data['result']['title'],
                'duration': data['result']['duration'],
                'matches': data['result']['matchs']  # 注意原始数据字段是'matchs'
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"赛程请求失败: {str(e)}")
        except KeyError as e:
            raise Exception(f"赛程数据解析错误: 缺少必要字段 {str(e)}")
