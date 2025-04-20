import requests
import pandas as pd

apiUrl='http://apis.juhe.cn/fapigw/air/provinces'
apiKey='a0379ff3164582de4d52c501b7747805'

requestParams = {
    'key': apiKey,
}

response = requests.get(apiUrl, params=requestParams)

print(response.json())  # 获取响应状态码
