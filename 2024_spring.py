import time
from datetime import datetime
from typing import List, Tuple

import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://book.diningcity.asia',
    'Pragma': 'no-cache',
    'Referer': 'https://book.diningcity.asia/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    # 经过测试，下面两个参数不用也行
    # 'access-token': 'xxx',
    # 'api-key': 'xxx',
    'lang': 'zh',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'project': 'rwcn_spring_2024',
}


def fetch(
        restaurant_id: int,
        target_date_list: List[str],
        target_meal_type_tuple: Tuple = ('午餐', '晚餐'),
):
    response = requests.get(f'https://api.diningcity.asia/public/restaurants/{restaurant_id}/available_2018', params=params, headers=headers)
    d = response.json()
    data = d['data']
    for day in data:
        weekday = day['weekday']
        date_str = day['date']
        if date_str in target_date_list:
            times = day['times']
            for t in times:
                _time = t['time']
                meal_type = t['meal_type']  # lunch or dinner
                meal_type_text = t['meal_type_text']
                seats: dict = t['seats']  # {'available': [2, 4, 6], 'used': 4}
                available: List[int] = seats['available']
                used: int = seats['used']

                if meal_type_text in target_meal_type_tuple:
                    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"{time_str} 发现餐位！餐厅ID: {restaurant_id}, 日期: {date_str}, 餐别: {meal_type_text}, 库存: {available}, 已用: {used}")
                    '''
2024-04-02 21:34:30 发现餐位！餐厅ID: 2053903, 日期: 2024-04-03, 餐别: 午餐, 库存: [2, 4, 6], 已用: 4
2024-04-02 21:34:30 发现餐位！餐厅ID: 2053903, 日期: 2024-04-03, 餐别: 午餐, 库存: [2, 4, 6], 已用: 4
2024-04-02 21:34:30 发现餐位！餐厅ID: 2053903, 日期: 2024-04-03, 餐别: 晚餐, 库存: [2], 已用: 8
2024-04-02 21:34:30 发现餐位！餐厅ID: 2053903, 日期: 2024-04-03, 餐别: 晚餐, 库存: [2], 已用: 8
                    '''


if __name__ == '__main__':
    while True:
        fetch(
            restaurant_id=2053903,
            target_date_list=['2024-04-03'],
            target_meal_type_tuple=('午餐', '晚餐'),
        )
        print('sleep 60s')
        time.sleep(60)
