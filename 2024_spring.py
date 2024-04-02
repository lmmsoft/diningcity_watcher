import json
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


def fetch_available(
        restaurant_id: int,
        target_date_list: List[str],
        target_meal_type_tuple: Tuple = ('午餐', '晚餐'),
):
    params = {
        'project': 'rwcn_spring_2024',
    }

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


def fetch_restaurant_info(restaurant_dirname: str):
    params = {
        'lang': 'zh',
    }

    response = requests.get(
        f'https://api.diningcity.asia/public/restaurants/{restaurant_dirname}/basic_info',
        params=params,
        headers=headers,
    )
    d = response.json()

    # s = json.dumps(d, indent=4, ensure_ascii=False)
    # print(s)
    '''
{
    "id": 2053903,
    "name": "浙江西子宾馆·牡丹厅",
    "dirname": "peony_chinese_restaurant_hangzhou",
    "address": "浙江省 杭州市 西湖区 南山路37号",
    "ratings_avg": 9.1,
    "lng": 120.152822,
    "lat": 30.231709,
    "localized_opening_hour_description": "11:00 - 14:00 \n17:30 - 22:00",
    "format_avg_price": "￥350",
    "cover": "https://static-assets.diningcity.asia/tx9hhny4vvzdzdmhnitvpht9oyxi?",
    "location": {
        "id": 3416,
        "name": "西湖区",
        "restaurants_count": 89
    },
    "cuisines": [
        {
            "id": 3199,
            "name": "杭帮菜",
            "dir_name": "chinese_-_hangzhou",
            "restaurants_count": 74
        }
    ]
}
    '''
    return d


def get_restaurant_id(restaurant_dirname: str):
    info_dict = fetch_restaurant_info(restaurant_dirname)
    return info_dict['id']


def fetch_restaurant_list(city_name: str):
    params = {
        'lang': 'zh',
        'api-key': 'cgecegcegcc',
        'per_page': '350',  # 上海餐厅最多，共有329家，可以一次全查出来
        'page': '1',
    }

    response = requests.get(
        f'https://api.diningcity.asia/public/extras_events/rwcn_spring_2024/cities/{city_name}/restaurants',
        params=params,
        headers=headers,
    )
    d = response.json()
    '''
[
    {
        "id": 205177662,
        "name": "Charbon by Paul Pairet",
        "address": "淮海中路999号环贸iapmL6-606号及L7-705号",
        "ratings_avg": 9.2,
        "thumb": "https://static-assets.diningcity.asia/xn4h5tdj9xlox91n0rn0i8e9n2cg?",
        "region_name": "上海",
        "meal_group_name": "A",
        "capacity_desc": "more",
        "capacity_desc_text": "预订",
        "lng": 121.458589,
        "lat": 31.21551,
        "dirname": "charbon",
        "cover": "https://static-assets.diningcity.asia/xn4h5tdj9xlox91n0rn0i8e9n2cg?",
        "avg_price": 363.0,
        "format_avg_price": "￥363",
        "michelin_stars": null,
        "reservation_type": "booking",
        "distance_to_restaurant": 0,
        "courses": [],
        "price_level": "RMB148 L - RMB298 D",
        "prices": [
            "¥148/位",
            "¥298/位"
        ],
        "detail_in_events_url": "https://restaurantweek.diningcity.cn/lang/zh/cities/shanghai/restaurants/charbon",
        "michelin_stars_text": "",
        "cuisines": [
            {
                "id": 3215,
                "name": "甜品",
                "dir_name": "desserts",
                "restaurants_count": 2726
            },
            {
                "id": 3284,
                "name": "西餐",
                "dir_name": "western",
                "restaurants_count": 1304
            }
        ],
        "tags": [],
        "locations": [
            {
                "id": 3332,
                "name": "徐汇区",
                "restaurants_count": 2253
            }
        ]
    }
]
    '''

    name_to_id = [(i['name'], i['id']) for i in d]
    s = json.dumps(name_to_id, indent=2, ensure_ascii=False)
    print(s)
    return name_to_id


if __name__ == '__main__':
    # 可以运行下面的方法，先找到餐厅 id
    restaurant_name_to_id_list = fetch_restaurant_list("shanghai")
    '''
[
  [    "九道·割烹", 205181877  ],
  [    "环球港凯悦 · 享悦中餐厅",    2054235  ],
  [    "臻萃轩中餐厅 @ 上海虹桥绿地铂瑞酒店",    205181591  ],
  [    "重庆叙山河·居民楼火锅",    205189061  ]
]
    '''

    # 用英文名查id的，暂时用不到
    # restaurant_id = get_restaurant_id("peony_chinese_restaurant_hangzhou")

    # 这里直接指定想要查询的餐厅id
    restaurant_id = 2053903  # 西子宾馆牡丹厅
    while True:
        fetch_available(
            restaurant_id=restaurant_id,
            target_date_list=['2024-04-03'],
            target_meal_type_tuple=('午餐', '晚餐'),
        )
        print('sleep 60s')
        time.sleep(60)
