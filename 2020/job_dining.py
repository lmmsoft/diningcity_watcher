# -- coding:UTF-8
import time
from diningcity import Manager
from ding import Dingding


def do_job(pre_text):
    t = time.localtime()
    # 0-8点不运行
    if t.tm_hour <= 8:
        return
    common_date = {
        # "2020-05-15": ["dinner"],
        "2020-05-30": ["dinner", "lunch"],
        "2020-05-31": ["dinner", "lunch"],
        # "2020-05-22": ["dinner"],
        # "2020-05-23": ["dinner", "lunch"],
        # "2020-05-24": ["dinner", "lunch"],
    }
    watcher_list = [
        {
            'id': 2053903,
            'name': '牡丹中餐厅',
            'date': common_date,
        },
        {
            'id': 2054354,
            'name': '木守西溪溪隐餐厅',
            'date': common_date,
        },
        {
            'id': 2052473,
            'name': '法云安缦西餐厅"',
            'date': common_date,
        },
        {
            'id': 13887,
            'name': '西湖餐厅',
            'date': common_date,
        },
        {
            'id': 2050388,
            'name': '青岚',
            'date': common_date,
        },
        {
            'id': 2054882,
            'name': '弘·和牛烧物',
            'date': common_date,
        },
    ]
    _, text = Manager.find_availiable(watcher_list)
    if text != pre_text:
        dd = Dingding()
        dd.send_message('dining:\n' + text)
    return text


def local_sleep():
    pre_text = ''
    import time
    while True:
        pre_text = do_job(pre_text)
        t = 5 * 60
        print('sleep {} seconds'.format(t))
        time.sleep(t)


if __name__ == '__main__':
    # do_job()
    local_sleep()
