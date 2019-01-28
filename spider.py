import time
from queue import Queue
from threading import Thread

import requests

from db_helper import DbHelper

def get_rank(url,params,headers):
    try:
        json = requests.get(url,params=params,headers=headers).json()
        rank_list = json['result']['board']
        for rank in rank_list:
            data = {}
            data['result'] = 'success'
            data['type'] = 'rank'
            data['rank'] = rank['rank']
            data['nickname'] = rank['nickname']
            data['value'] = rank['value']
            data['mode'] = params['mode']
            data['season'] = params['season']
            data['category'] = params['category']
            # print(data)
            yield data
    except Exception as e:
        print('get_rank() error,',str(e))
        data = {}
        data['result'] = 'error'
        yield data


def get_distribution(url,params,headers):
    try:
        json = requests.get(url,params=params,headers=headers).json()
        rating_distribution_list = json['result']['rating_distribution']
        for dis in rating_distribution_list:
            data = {}
            data['result'] = 'success'
            data['type'] = 'distribution'
            data['start'] = dis['start']
            data['end'] = dis['end']
            data['top'] = dis['top']
            data['mode'] = params['mode']
            data['season'] = params['season']
            data['category'] = params['category']
            # print(data)
            yield data
    except Exception as e:
        print('get_rank() error,',str(e))
        data = {}
        data['result'] = 'error'
        yield data

def put_into_queue(queue,url,params,headers):
    for data in get_rank(url,params,headers):
        if data['result'] == 'success':
            queue.put_nowait(data)
        elif data['result'] == 'error':
            continue
    for data in get_distribution(url,params,headers):
        if data['result'] == 'success':
            queue.put_nowait(data)
        elif data['result'] == 'error':
            continue

def get_from_queue(queue,db):
    while True:
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
    mode_list = {'所有模式':'all','单人':'solo','双人':'duo','四排':'squad','第一人称单人':'solo-fpp','第一人称双人':'duo-fpp','第一人称四排':'squad-fpp'}
    season_list = {'2018第一赛季':'2018-01','2018第二赛季':'2018-02','2018第三赛季':'2018-03','2018第四赛季':'2018-04','2018第五赛季':'2018-05','2018第六赛季':'2018-06','2018第七赛季':'2018-07','2018第八赛季':'2018-08','2018第九赛季':'2018-09','2018第十赛季':'pc-2018-01','2018第十一赛季':'pc-2018-02'}
    category_lsit = {'积分':'Rating','吃鸡率':'WinRatio','场均击杀':'AvgKills','场均伤害':'AvgDamageDealt','游戏场数':'RoundsPlayed'}

    while True:
        try:
            mode = mode_list[input('请选择模式(所有模式,单人,双人,四排,第一人称单人,第一人称双人,第一人称四排):')]
            season = season_list[input('请选择赛季(2018第x赛季):')]
            category = category_lsit[input('请选择分类(积分、吃鸡率、场均击杀、场均伤害、游戏场数):')]
            break
        except:
            print('输入有误，请重新输入')

    params = {'mode':mode,'season':season,'category':category}
    # url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=10.3.3&version=1.1.52&device_id=D2AA4D4F-AC80-476C-BFE1-CBD83AB74133&heybox_id=5141514&limit=30&offset=0&mode=solo&season=pc-2018-02&category=WinRatio'
    url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/'
    headers = {
        'User-Agent': 'xiaoheihe/1.1.52 (iPhone; iOS 10.3.3; Scale/2.00)'
    }
    # print(requests.get(url,params=params,headers=headers).json())
    configs = {'host': 'localhost', 'user': 'root', 'password': 'admin', 'db': 'pubg_steam'}
    db = DbHelper()
    db.connenct(configs)

    queue = Queue()
    Thread(target=put_into_queue, args=(queue,url,params,headers), daemon=True).start()
    time.sleep(2)
    Thread(target=get_from_queue, args=(queue, db), daemon=True).start()

    queue.join()
    db.close()

# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402685&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=10fe9dc9bd15d63d7e8efbed1be202cd&limit=30&offset=0&season=2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402745&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=4f448a5e004a33f68c3750c540560b1a&limit=30&offset=0&season=pc-2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402881&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=b7205992fa31bba3f5fc396137bad193&limit=30&mode=solo&offset=0
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402912&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=363203c11f79e19cc6626fe507e70760&category=WinRatio&limit=30&mode=solo&offset=0
