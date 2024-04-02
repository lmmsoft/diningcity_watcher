from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json # https://pypi.org/project/dataclasses-json/


@dataclass_json
@dataclass
class City:
    name: str
    coverImage: str
    scenicSpotImage: str
    sort: int


@dataclass_json
@dataclass
class Cuisines:  # Location
    id: int  # 33
    name: str  # '亚洲菜'
    dir_name: str  # 'asian'
    restaurants_count: int  # 299


@dataclass_json
@dataclass
class Tag:
    id: int  # 10049
    name: str  # 携程美食林
    icon_url: str  # https://assets.diningcity.cn/tag/5e461d0f5861fa33edd0e84d88e266e7.png


@dataclass_json
@dataclass
class Restaurant:
    id: int  # 13887,
    name: str  # '西湖餐厅',
    address: str  # '灵隐路5号杭州西子湖四季酒店1楼',
    ratings_avg: float  # 10.0,
    thumb: str  # 'https://assets.diningcity.cn/restaurantpictures/2020/0ce36cbe7baff991c36ab83996c6f11e.jpg',
    meal_group_name: str  # 'A',
    capacity_desc: str  # 'more',
    lng: float  # 120.128119813036,
    lat: float  # 30.2511883714822
    dirname: str  # 'wl_bistro'
    cover: str  # 'https://assets.diningcity.cn/restaurantpictures/2020/0ce36cbe7baff991c36ab83996c6f11e.jpg'
    avg_price: float  # 600.0
    michelin_stars: Optional[str]  # todo
    distance_to_restaurant: float  # todo 0
    courses: List[Cuisines]
    michelin_stars_text: str
    price_level: str  # 'RMB138 L - RMB288 D', 'michelin_stars_text': '',
    cuisines: List[Cuisines]
    tags: List[Tag]
    locations: List[Cuisines]


@dataclass_json
@dataclass
class Seats:
    available: List[int]
    used: int  # 25


@dataclass_json
@dataclass
class Times:
    time: str  # '11:30'
    meal_type: str  # 'lunch'
    seats: Seats
