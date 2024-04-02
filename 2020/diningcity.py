# -- coding:UTF-8
import requests
import json
import os
from dining_model import Restaurant, Cuisines, Times

from typing import List, Dict, Any


class Storage():
    DINING_FLODER = "data/dining/"
    CITY_LIST = "data/dining/city_list.json"
    RESTAURANT_LIST = "data/dining/{city}.json"

    # HOTEL_INFO = "data/hotel/{storeNo}.json"
    # ROOM_LIST = "data/room/{storeNo}.json"
    # CALENDAR = "data/calendar/{city}.json"
    # CALENDAR_FOLDER = "data/calendar/"
    # WATCHER = 'data/watcher/{storeNo}.json'

    @classmethod
    def _save(cls, file_name: str, data: Any) -> None:
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

    @classmethod
    def _load(cls, file_name: str) -> Any:
        with open(file_name, 'r') as f:
            return json.load(f)

    @classmethod
    def save_restaurant_list(cls, city, restaurant_list=List[Restaurant]) -> None:
        # if not os.path.exists(cls.DINING_FLODER):
        #     os.mkdir(cls.DINING_FLODER)
        file_name = cls.RESTAURANT_LIST.format(city=city)
        data_js = Utils.restaurant_list_to_json(restaurant_list)
        cls._save(file_name, data_js)

    @classmethod
    def load_restaurant_list(cls, city) -> List[Restaurant]:
        file_name = cls.RESTAURANT_LIST.format(city=city)
        js_dict = cls._load(file_name)
        return Utils.restaurant_list_from_json(js_dict)

    @classmethod
    def save_watcher_result(cls,city:str,d:Dict):
        pass


class Utils:
    @classmethod
    def restaurant_list_to_json(cls, restaurant_list: List[Restaurant]) -> list:
        return Restaurant.schema().dump(restaurant_list, many=True)

    @classmethod
    def restaurant_list_from_json(cls, restaurant_list: list) -> List[Restaurant]:
        return Restaurant.schema().load(restaurant_list, many=True)

    @classmethod
    def times_list_to_json(cls, li: List[Times]) -> list:
        return Times.schema().dump(li, many=True)

    @classmethod
    def times_list_from_json(cls, li: list) -> List[Times]:
        return Times.schema().load(li, many=True)


class DiningCityCrawler():
    def get_restaurant_list_by_city(self, city='hangzhou') -> List[Restaurant]:
        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'DNT': '1',
            'Origin': 'https://restaurantweek.diningcity.cn',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://restaurantweek.diningcity.cn/lang/zh/cities/hangzhou/restaurants/results?acc=amexwebcent',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'If-None-Match': 'W/"dbd94a646991e6012bf8a8ee9cc1d34c"',
        }

        params = {
            ('lang', 'zh'),
            ('api-key', 'cgecegcegcc'),
            ('per_page', '50'),  # 杭州36个，最多上海，一次请求即可
            ('order_by', 'distance'),
            ('page', '1'),
        }

        response = requests.get(
            'https://dcapi.diningcity.cn/public/extras_events/rwcn_spring_2020/cities/{city}/restaurants'.format(city=city),
            headers=headers,
            params=params,
            verify=False
        )

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://dcapi.diningcity.cn/public/extras_events/rwcn_spring_2020/cities/hangzhou/restaurants?lang=zh&api-key=cgecegcegcc&per_page=8&order_by=distance&page=1', headers=headers)

        if response.ok:
            js = response.json()
            # dump = json.dumps(js, indent=2, ensure_ascii=False)
            # print(dump)
            # restaurant_list: List[Restaurant] = Restaurant.schema().load(js, many=True)
            restaurant_list: List[Restaurant] = Utils.restaurant_list_from_json(js)
            return restaurant_list
            # Storage.save_restaurant_list(city, restaurant_list)
        return []

        xihu_restaurant = {
            'id': 13887,
            'name': '西湖餐厅',
            'address': '灵隐路5号杭州西子湖四季酒店1楼',
            'ratings_avg': 10.0,
            'thumb': 'https://assets.diningcity.cn/restaurantpictures/2020/0ce36cbe7baff991c36ab83996c6f11e.jpg',
            'meal_group_name': 'A',
            'capacity_desc': 'more',
            'lng': 120.128119813036,
            'lat': 30.2511883714822, 'dirname': 'wl_bistro', 'cover': 'https://assets.diningcity.cn/restaurantpictures/2020/0ce36cbe7baff991c36ab83996c6f11e.jpg', 'avg_price': 600.0, 'michelin_stars': None, 'distance_to_restaurant': 0, 'courses': [],
            'price_level': 'RMB138 L - RMB288 D',
            'michelin_stars_text': '',
            'cuisines': [
                {'id': 33, 'name': '亚洲菜', 'dir_name': 'asian', 'restaurants_count': 299},
                {'id': 43, 'name': '法国菜', 'dir_name': 'french', 'restaurants_count': 2950},
                {'id': 49, 'name': '意大利菜', 'dir_name': 'italian', 'restaurants_count': 1221},
                {'id': 127, 'name': '欧菜', 'dir_name': 'european', 'restaurants_count': 302}
            ],
            'tags': [
                {'id': 10049, 'name': '携程美食林', 'icon_url': 'https://assets.diningcity.cn/tag/5e461d0f5861fa33edd0e84d88e266e7.png'},
                {'id': 10045, 'name': '特色菜单', 'icon_url': 'https://assets.diningcity.cn/tag/aa90fcc32087c22315cf4b05dd73e41e.png'}
            ],
            'locations': [
                {'id': 3416, 'name': '西湖区', 'dir_name': 'west_lake_district', 'restaurants_count': 89}
            ]}
        sample_list_res = {
            "id": 2050388,
            "name": "青岚",
            "address": "杨公堤38号曲院风荷三号门内",
            "ratings_avg": 9.2,
            "thumb": "https://assets.diningcity.cn/restaurantpictures/2017/048aa908c6fc6a32e40058868c5afd7a.jpg",
            "meal_group_name": "A",
            "capacity_desc": "no",  # 有订就是 'more', "capacity_desc": "more",
            "lng": 120.131573,
            "lat": 30.248264,
            "dirname": "id2050388_breeze",
            "cover": "https://assets.diningcity.cn/restaurantpictures/2017/048aa908c6fc6a32e40058868c5afd7a.jpg",
            "avg_price": 300.0,
            "michelin_stars": None,
            "distance_to_restaurant": 0,
            "courses": [],
            "price_level": "RMB138 L - RMB288 D",
            "michelin_stars_text": "",
            "cuisines": [
                {
                    "id": 133,
                    "name": "创意菜",
                    "dir_name": "fusion",
                    "restaurants_count": 583
                },
                {
                    "id": 3284,
                    "name": "西餐",
                    "dir_name": "western",
                    "restaurants_count": 828
                },
                {
                    "id": 3290,
                    "name": "新派料理",
                    "dir_name": "contemporary",
                    "restaurants_count": 27
                }
            ],
            "tags": [
                {
                    "id": 10052,
                    "name": "曾获奖餐厅",
                    "icon_url": "https://assets.diningcity.cn/tag/477e2c7615e5b8952695fee27bd3ac84.png"
                }
            ],
            "locations": [
                {
                    "id": 3416,
                    "name": "西湖区",
                    "dir_name": "west_lake_district",
                    "restaurants_count": 89
                }
            ]
        }

    # 只能查一天，不好用
    def get_calender_date(self, id: int = 13887, date='2020-05-15'):
        headers = {
            'Connection': 'keep-alive',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'client': '',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'access-token': '',
            'uid': '',
            'api-key': 'cgecegcegcc',
            'lang': 'zh',
            'Origin': 'https://webform.diningcity.cn',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://webform.diningcity.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        params = {
            ('project', 'rwcn_spring_2020'),
            ('access_code', 'amexwebcent'),
            ('access_password', '37998688'),
            ('selected_date', date),
        }

        response = requests.get(
            'https://dcapi.diningcity.cn/public/restaurants/{id}/available_2018'.format(id=id),
            headers=headers,
            params=params,
            verify=False,
        )

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://dcapi.diningcity.cn/public/restaurants/13887/available_2018?project=rwcn_spring_2020&access_code=amexwebcent&access_password=37998688&selected_date=2020-05-01', headers=headers)
        if response.ok:
            js = response.json()
            # dump = json.dumps(js, indent=2, ensure_ascii=False)
            # print(dump)
            times = js['data'][0]['times']
            times_list = Utils.times_list_from_json(times)
            return times_list
        return []

        sample = {
            "data": [
                {
                    "date": "2020-05-01",
                    "weekday": "friday",
                    "times": [
                        {
                            "time": "11:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "11:45",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:00",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:15",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:45",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:00",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:15",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "17:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 13
                            }
                        },
                        {
                            "time": "17:45",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 13
                            }
                        },
                        {
                            "time": "18:00",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 13
                            }
                        },
                        {
                            "time": "18:15",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 13
                            }
                        },
                        {
                            "time": "18:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 13
                            }
                        },
                        {
                            "time": "18:45",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 0
                            }
                        },
                        {
                            "time": "19:00",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 0
                            }
                        },
                        {
                            "time": "19:15",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 0
                            }
                        },
                        {
                            "time": "19:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 0
                            }
                        }
                    ]
                }
            ]
        }

    # 获取餐厅详情，没什么用
    def get_detail(self):
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'DNT': '1',
            'lang': 'zh',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'api-key': 'cgecegcegcc',
            'Content-Type': 'application/json',
            'Origin': 'https://webform.diningcity.cn',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://webform.diningcity.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'If-None-Match': 'W/"8da99fe8fbd31139e41f0814d81d6639"',
        }

        response = requests.get(
            'https://dcapi.diningcity.cn/public/restaurants/13887',
            headers=headers,
            verify=False,
        )
        if response.ok:
            js = response.json()
            dump = json.dumps(js, indent=2, ensure_ascii=False)
            print(dump)

        res = {
            "id": 13887,
            "name": "西湖餐厅",
            "dirname": "wl_bistro",
            "address": "灵隐路5号杭州西子湖四季酒店1楼",
            "phone": "0571-88298888",
            "status_name": "Basic",
            "avatar_url": "https://assets.diningcity.cn/restaurantpictures/13887_2bdf4b0e02_logo.JPG_800x800",
            "active": 8,
            "lng": 120.128119813036,
            "lat": 30.2511883714822,
            "reservation_type": 3,
            "price_class": "550-650",
            "tos": None,
            "tos_url": None,
            "learn_status": None,
            "wifi_name": None,
            "wifi_password": None,
            "privacy_policy_url": "https://diningcity.cn/zh/hangzhou/pages/privacy_policy",
            "opening_hour": "Lunch 11:30 - 14:30\nDinner 17:30 - 21:30",
            "localized_opening_hour": "11:30 - 14:30\n 17:30 - 21:30",
            "avg_price": 600.0,
            "ratings_avg": 8.866666666666667,
            "cover": "https://assets.diningcity.cn/restaurantpictures/2020/0ce36cbe7baff991c36ab83996c6f11e.jpg",
            "michelin_stars": None,
            "booking_enabled": True,
            "book_config": {},
            "website_detail_url": "https://diningcity.cn/zh/hangzhou/wl_bistro",
            "discount_enabled": True,
            "delivery_provider_phone": None,
            "enable_delivery": False,
            "is_gourmet_club_wine": False,
            "email": "wlb.han@fourseasons.com；vily.zhou@fourseasons.com",
            "max_group_size": 10,
            "region_id": 86,
            "new_system": True,
            "logo_url": "https://assets.diningcity.cn/restaurantpictures/2020/51aa5b2b9ec8177034cdcfafaed08c75.jpg_160x160",
            "wide_picture": "https://assets.diningcity.cn/restaurantwidepictures/2001100_wlbistro.jpg_730x290",
            "discount_explanation": "",
            "localized_discount_explanation": None,
            "recommends_count": 24,
            "reviews_count": 39,
            "reviews_ratings": {
                "ratings_avg": 8,
                "cuisine_avg": 8,
                "service_avg": 8,
                "atmosphere_avg": 9
            },
            "location": {
                "id": 3416,
                "name": "西湖区",
                "dir_name": "west_lake_district",
                "restaurants_count": 89
            },
            "tags": [
                {
                    "id": 9859,
                    "name": "即刻预订",
                    "icon_url": "https://assets.diningcity.cn/tag/224efa1de4a8ed36b6636c72de01a866.png"
                }
            ],
            "cuisines": [
                {
                    "id": 33,
                    "name": "亚洲菜",
                    "dir_name": "asian",
                    "restaurants_count": 298
                },
                {
                    "id": 43,
                    "name": "法国菜",
                    "dir_name": "french",
                    "restaurants_count": 2953
                },
                {
                    "id": 49,
                    "name": "意大利菜",
                    "dir_name": "italian",
                    "restaurants_count": 1222
                },
                {
                    "id": 127,
                    "name": "欧菜",
                    "dir_name": "european",
                    "restaurants_count": 302
                }
            ],
            "region": {
                "id": 86,
                "name": "杭州",
                "key_word": "hangzhou",
                "ne_lat": 30.5665162,
                "ne_lng": 120.7058943,
                "sw_lat": 29.1887571,
                "sw_lng": 118.3449335,
                "domain": "diningcity.cn",
                "global_map": False,
                "currency": "￥",
                "country_name": "china"
            },
            "account_manager": None,
            "extras": [
                {
                    "id": 3359,
                    "name": "中午套餐",
                    "dir_name": "set_lunch",
                    "restaurants_count": 81
                },
                {
                    "id": 3519,
                    "name": "全日早餐",
                    "dir_name": "all_day_breakfast",
                    "restaurants_count": 1
                },
                {
                    "id": 740,
                    "name": "户外座位",
                    "dir_name": "outdoor_seating",
                    "restaurants_count": 116
                },
                {
                    "id": 3373,
                    "name": "提供儿童设施",
                    "dir_name": "child_friendly",
                    "restaurants_count": 74
                },
                {
                    "id": 3506,
                    "name": "晚餐",
                    "dir_name": "dinner",
                    "restaurants_count": 121
                },
                {
                    "id": 3375,
                    "name": "浪漫氛围",
                    "dir_name": "romantic",
                    "restaurants_count": 238
                },
                {
                    "id": 3341,
                    "name": "酒店内的餐厅",
                    "dir_name": "hotel_restaurant",
                    "restaurants_count": 468
                }
            ],
            "landmarks": [
                {
                    "id": 195,
                    "name": "西湖北线/黄龙",
                    "dir_name": "west_lake_bei_xian_huanglong",
                    "restaurants_count": 31
                },
                {
                    "id": 2000045,
                    "name": "西湖/杨公堤",
                    "dir_name": "westlake_yanggongdi",
                    "restaurants_count": 10
                }
            ],
            "open_hour": {
                "id": 1683,
                "max_at_one_time": 10,
                "minutes_in_advance": 0,
                "off_peak_times_count": 0,
                "owner_id": 13887,
                "owner_type": "Restaurant",
                "disable_change_time": 60,
                "seats": 3,
                "time_interval": 60,
                "meal_times": []
            },
            "basic_info": {
                "localized_name": "西湖餐厅",
                "address": "灵隐路5号杭州西子湖四季酒店1楼",
                "description": "位于酒店一层，全天候供应早、午、晚餐，拥有60个座位，为客人呈献多元化的欧陆风味美食。餐厅设计别具匠心，传统的石墙，精致的地板与晶莹的餐具彼此交融。特设户外用餐区，荷塘翠竹，景致怡人，是良朋聚首、开怀畅饮的好去处。\n室内餐位：46   \n室外餐位：42\n垂询或预约请拨打86 (571) 8113 5128"
            }
        }

    # 可以拿所有日期，非常有用
    def get_calender(self, id: int = 13887) -> Dict:
        headers = {
            'Connection': 'keep-alive',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'client': '',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'access-token': '',
            'uid': '',
            'api-key': 'cgecegcegcc',
            'lang': 'zh',
            'Origin': 'https://webform.diningcity.cn',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://webform.diningcity.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'If-None-Match': 'W/"aaf237e2fc73ac13c676db198821a69b"',
        }

        params = (
            ('project', 'rwcn_spring_2020'),
            ('access_code', 'amexwebcent'),
            ('access_password', '37998688'),
        )

        response = requests.get(
            'https://dcapi.diningcity.cn/public/restaurants/{id}/available_2018'.format(id=id),
            headers=headers,
            params=params,
            verify=True,
            # cert='../data/diningcity.cer',
        )

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://dcapi.diningcity.cn/public/restaurants/13887/available_2018?project=rwcn_spring_2020&access_code=amexwebcent&access_password=37998688', headers=headers)

        if response.ok:
            js = response.json()

            # 餐厅 -> 日期 -> 午餐晚餐 -> 有位时间

            date_list = js['data']
            res_calendar_dict = {}
            for d in date_list:
                date = d['date']
                weekday = d['weekday']
                times = d['times']
                times_list = Utils.times_list_from_json(times)

                res_date = {}
                for t in times_list:
                    if t.seats.available:
                        res_date[t.meal_type] = True

                if res_date:
                    res_calendar_dict[date] = res_date

            return res_calendar_dict

        return {}

        sample = {
            "data": [
                {
                    "date": "2020-04-30",
                    "weekday": "thursday",
                    "times": [
                        {
                            "time": "11:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "11:45",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:00",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:15",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "12:45",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:00",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:15",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "17:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "17:45",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "18:00",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "18:15",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "18:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "18:45",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "19:00",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "19:15",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        },
                        {
                            "time": "19:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 2
                            }
                        }
                    ]
                },
                {
                    "date": "2020-05-01",
                    "weekday": "friday",
                    "times": [
                        {
                            "time": "11:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "13:30",
                            "meal_type": "lunch",
                            "seats": {
                                "available": [],
                                "used": 25
                            }
                        },
                        {
                            "time": "17:30",
                            "meal_type": "dinner",
                            "seats": {
                                "available": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8
                                ],
                                "used": 15
                            }
                        },
                    ]
                },
            ]}

    def save_restaurant_basic_info(self, city, restaurant_list: List[Restaurant]):
        d = {}
        for r in restaurant_list:
            d[r.name] = {
                'id': r.id,
                'district': r.locations[0].name if r.locations else 'no_district',
                'address': r.address,
            }
        Storage._save('data/dining/{city}_basic.json'.format(city=city), d)


class Manager:
    @staticmethod
    def find_availiable(watcher_list):
        restaurant_list = Storage.load_restaurant_list('hangzhou')

        crawler = DiningCityCrawler()

        watcher_result = []
        for w in watcher_list:
            calender = crawler.get_calender(w['id'])
            if calender:
                res_list = []
                for dt_str, lunch_dinner_list in w['date'].items():
                    res_dates = []
                    if dt_str in calender:
                        l_d_l = calender[dt_str]
                        for i in l_d_l:
                            if i in lunch_dinner_list:
                                res_dates.append(i)
                    if res_dates:
                        res_list.append((dt_str, res_dates))
                r = [re for re in restaurant_list if re.id == w['id']][0]

                watcher_result.append({
                    'name': r.name,
                    'district': r.locations[0].name if r.locations else 'no_district',
                    'address': r.address,
                    'available': res_list,
                })

        # text = json.dumps(watcher_result, ensure_ascii=False, indent=4, sort_keys=True)
        text_list = []
        for w in watcher_result:
            text_list.append('【{}】【{}】 {}'.format(w['district'], w['name'], w['address']))
            for dt_str, lunch_dinner_list in w['available']:
                text_list.append('{} {}'.format(dt_str, lunch_dinner_list))

        return watcher_result, '\n'.join(text_list)

    @staticmethod
    def find_all():
        crawler = DiningCityCrawler()
        city = 'hangzhou'
        restaurant_list = crawler.get_restaurant_list_by_city(city)
        if restaurant_list:
            Storage.save_restaurant_list(city, restaurant_list)

            crawler.save_restaurant_basic_info(city, restaurant_list)

            calender_list = []
            for r in restaurant_list:
                print('get_calender for {} {}'.format(r.id, r.name))
                calender = crawler.get_calender(r.id)
                if calender:
                    calender_list.append({
                        'name': r.name,
                        'district': r.locations[0].name if r.locations else 'no_district',
                        'address': r.address,
                        'available': calender,
                    })

            Storage._save('data/dining/{city}_calender.json'.format(city=city), calender_list)


if __name__ == '__main__':
    crawler = DiningCityCrawler()
    # crawler.get_restaurant_list_by_city()
    # crawler.get_calender_date()
    # crawler.get_detail()
    crawler.get_calender()
