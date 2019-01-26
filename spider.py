import time
from queue import Queue
from threading import Thread

import requests

from db_helper import DbHelper


def get_rank(url,headers):
    json = requests.get(url,headers=headers).json()
    rank_list = json['result']['board']
    for rank in rank_list:
        data = {}
        data['type'] = 'rank'
        data['rank'] = rank['rank']
        data['nickname'] = rank['nickname']
        data['value'] = rank['value']
        # print(data)
        yield data

def get_distribution(url,headers):
    json = requests.get(url,headers=headers).json()
    rating_distribution_list = json['result']['rating_distribution']
    for dis in rating_distribution_list:
        data = {}
        data['type'] = 'distribution'
        data['start'] = dis['start']
        data['end'] = dis['end']
        data['top'] = dis['top']
        # print(data)
        yield data

def put_into_queue(queue,url,headers):
    for data in get_rank(url,headers):
        queue.put_nowait(data)
    for data in get_distribution(url,headers):
        queue.put_nowait(data)

def get_from_queue(queue,db):
    try:
        data = queue.get_nowait()
        if data['type'] == 'rank':
            db.save_one_data_to_rank(data)
            queue.task_done()
        elif data['type'] == 'distribution':
            db.save_one_data_to_distribution(data)
            queue.task_done()
    except:
        print('queue is empty wait for a while...')
        time.sleep(1)

if __name__ == '__main__':
    url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548401877&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=c1aa1c85ada7b8afee362867c291bc84&limit=30&offset=0'
    headers = {
        'User-Agent': 'xiaoheihe/1.1.52 (iPhone; iOS 12.1.2; Scale/2.00)'
    }

    configs = {'host': 'localhost', 'user': 'root', 'password': 'admin', 'db': 'pubg_steam'}
    db = DbHelper()
    db.connenct(configs)

    queue = Queue()
    Thread(target=put_into_queue, args=(queue,url,headers)).start()
    time.sleep(2)
    Thread(target=get_from_queue, args=(queue, db)).start()

    queue.join()
    db.close()
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402685&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=10fe9dc9bd15d63d7e8efbed1be202cd&limit=30&offset=0&season=2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402745&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=4f448a5e004a33f68c3750c540560b1a&limit=30&offset=0&season=pc-2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402881&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=b7205992fa31bba3f5fc396137bad193&limit=30&mode=solo&offset=0
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402912&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=363203c11f79e19cc6626fe507e70760&category=WinRatio&limit=30&mode=solo&offset=0
