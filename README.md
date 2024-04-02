# diningcity_watcher
监控_鼎食聚_餐厅周_餐位的空余情况

## 背景
[鼎食聚](https://www.diningcity.cn/) 

[2024春季 餐厅周](https://restaurantweek.diningcity.cn/lang/zh)
[2024春季 餐厅周 杭州](https://restaurantweek.diningcity.cn/lang/zh/cities/hangzhou/restaurants)

DiningCity鼎食聚是一个专注中高端餐厅的美食指南及预订平台，每年春季和秋季会举行餐厅周活动，提供很多高端餐厅的优惠套餐，包括北京、上海、广州、深圳、苏州、杭州、南京、成都等很多一二线城市的数百家餐厅，还有很多米其林、黑珍珠餐厅上榜。

由于活动火热，热门餐厅的位置会很快被预订完；又由于免费预定，所以很多餐位会时不时释放出来。

可以用一个监控程序来监控餐厅的位置情况，一旦有位置空余就会通知。

## 使用方法
- 2024春季，详见 2024_spring.py 代码里的注释
- 提供的方法
  - a.根据城市查询餐厅id列表
  - b.根据餐厅id/日期/午餐or晚餐，查询库存