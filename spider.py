import sys
import time
from queue import Queue
from threading import Thread

import requests

from db_helper import DbHelper


def get_rank(url, params, headers):
    try:
        json = requests.get(url, params=params, headers=headers).json()
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
        print('get_rank() error,', str(e))
        data = {}
        data['result'] = 'error'
        yield data


def get_distribution(url, params, headers):
    try:
        json = requests.get(url, params=params, headers=headers).json()
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
        print('get_rank() error,', str(e))
        data = {}
        data['result'] = 'error'
        yield data

def get_Cookie(form_data,headers):
    headers['Referer'] = 'http://api.maxjia.com/'
    try:
        r = requests.post('https://api.xiaoheihe.cn/account/login/',
                     data=form_data,headers=headers).json()

        return 'pkey=' + r['result']['pkey']
    except Exception as e:
        print('get_Cookie error:',str(e))
        return None

def get_player_overview(rank,url,params,headers):
    try:
        json = requests.get(url, params=params, headers=headers).json()
        detail_list = json['result']
        for detail in detail_list:
            data = {}
            data['overview']['result'] = 'success'
            data['overview']['type'] = 'overview'

            data['overview']['mode'] = rank['mode']
            data['overview']['season'] = rank['season']
            data['overview']['nickname'] = rank['nickname']

            data['overview']['rateing'] = detail['overview'][0]['value']
            data['overview']['win_times'] = detail['overview'][1]['value']
            data['overview']['win_times_rank'] = detail['overview'][1]['rank']
            data['overview']['top10_times'] = detail['overview'][2]['value']
            data['overview']['top10_times_rank'] = detail['overview'][2]['rank']
            data['overview']['avg_kills'] = detail['overview'][3]['value']
            data['overview']['avg_kills_rank'] = detail['overview'][3]['rank']
            data['overview']['ranks'] = detail['overview'][4]['value']
            data['overview']['win_ratio'] = detail['overview'][5]['value']
            data['overview']['win_ratio_rank'] = detail['overview'][5]['rank']
            data['overview']['top10_ratio'] = detail['overview'][6]['value']
            data['overview']['top10_ratio_rank'] = detail['overview'][6]['rank']
            data['overview']['k_d'] = detail['overview'][7]['value']
            data['overview']['k_d_rank'] = detail['overview'][7]['rank']
            yield data
    except Exception as e:
        print('get_player_overview() error,', str(e))
        data = {}
        data['overview']['result'] = 'error'
        yield data

def put_into_queue(queue, url, params, headers):
    for data in get_rank(url, params, headers):
        if data['result'] == 'success':
            queue.put_nowait(data)
        elif data['result'] == 'error':
            continue
    for data in get_distribution(url, params, headers):
        if data['result'] == 'success':
            queue.put_nowait(data)
        elif data['result'] == 'error':
            continue

def get_from_queue(queue, db):
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

def put_into_queue1(queue1, url, headers):
    for rank in db.find_today_rank():
        p = {}
        p['nickname'] = rank['nickname']
        p['season'] = rank['season']
        if 'fpp' not in rank['mode']:
            p['fpp'] = '0'
            p['mode'] = rank['mode']
            for data in get_player_overview(rank,url, p, headers):
                if data['overview']['result'] == 'success':
                    queue1.put_nowait(data)
                elif data['overview']['result'] == 'error':
                    continue

def get_from_queue1(queue1, db):
    while True:
        try:
            data = queue1.get_nowait()
            if data['overview']['type'] == 'overview':
                db.save_one_data_to_overview(data['overview'])
                queue1.task_done()
            # elif data['overview']['type'] == 'distribution':
            #     db.save_one_data_to_distribution(data)
            #     queue.task_done()
        except:
            print('queue is empty wait for a while...')
            time.sleep(1)


if __name__ == '__main__':
    mode_list = {'单人': 'solo', '双人': 'duo', '四排': 'squad', '第一人称单人': 'solo-fpp', '第一人称双人': 'duo-fpp',
                 '第一人称四排': 'squad-fpp'}
    season_list = {'2018第一赛季': '2018-01', '2018第二赛季': '2018-02', '2018第三赛季': '2018-03', '2018第四赛季': '2018-04',
                   '2018第五赛季': '2018-05', '2018第六赛季': '2018-06', '2018第七赛季': '2018-07', '2018第八赛季': '2018-08',
                   '2018第九赛季': '2018-09', '2018第十赛季': 'pc-2018-01', '2018第十一赛季': 'pc-2018-02'}
    category_lsit = {'积分': 'Rating', '吃鸡率': 'WinRatio', '场均击杀': 'AvgKills', '场均伤害': 'AvgDamageDealt',
                     '游戏场数': 'RoundsPlayed'}

    # while True:
    #     try:
    #         mode = mode_list[input('请选择模式(单人,双人,四排,第一人称单人,第一人称双人,第一人称四排):')]
    #         season = season_list[input('请选择赛季(2018第x赛季):')]
    #         category = category_lsit[input('请选择分类(积分、吃鸡率、场均击杀、场均伤害、游戏场数):')]
    #         break
    #     except:
    #         print('输入有误，请重新输入')
    #
    # params = {'mode': mode, 'season': season, 'category': category}
    # # url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=10.3.3&version=1.1.52&device_id=D2AA4D4F-AC80-476C-BFE1-CBD83AB74133&heybox_id=5141514&limit=30&offset=0&mode=solo&season=pc-2018-02&category=WinRatio'
    # url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/'
    headers = {
        'User-Agent': 'xiaoheihe/1.1.52 (iPhone; iOS 10.3.3; Scale/2.00)'
    }
    # print(requests.get(url,params=params,headers=headers).json())
    configs = {'host': 'localhost', 'user': 'root', 'password': 'admin', 'db': 'pubg_steam'}
    db = DbHelper()
    db.connenct(configs)

    # queue = Queue()
    # Thread(target=put_into_queue, args=(queue, url, params, headers), daemon=True).start()
    # time.sleep(10)
    # Thread(target=get_from_queue, args=(queue, db), daemon=True).start()
    #
    # queue.join()

    # for rank in db.find_today_rank():
    #     print(rank)

    # headers['Referer'] = 'http://api.maxjia.com/'

    # headers = {
    #     'User-Agent': 'xiaoheihe/1.1.52 (iPhone; iOS 10.3.3; Scale/2.00)',
    #     'Referer':'http://api.maxjia.com/',
    #     'Cookie':'pkey=MTU0OTE3NzI0OS42N18xNDkwOTc4OXFqbXJvZ2xjeXNpaGZvcms__'
    # }
    form_data = {
        'phone_num':'M6Y3WpfSNET9W4ZwcML1tUx+jvOWtaDKwoUM3ABM+o7AXi8yZKplkUSM3u3R9cN+x4CNZ2Mo/SHFqB8nQWNt9WHEKc3iC0nSfTfbhlLJECCLpB60Cpbo7HKjE9dlY8s7kJY8bCn+xHAXEGg/2avB2SRPFLPo+Nm0JO6R07Sof4U=',
        'pwd':'OKNkTFqOU26Adb/9IAvze4K+u6aBHpd9cvBuyRWWAifDyb48wAvLbGUHfj0ZtTvGdg3Y2k8x9EyzcvW/G36R9ukCVpa+xJFztKM8GIl1q71OPNSTx0u1+EM6JiZnGxvPWApt0coRLm64BkRBcbhgliSauUlheBBfoAIADSNlXpw='
    }

    # r = requests.post('https://api.xiaoheihe.cn/account/login/',
    #                  data=form_data,headers=headers).json()
    #
    # headers['Cookie'] = 'pkey=' + r['result']['pkey']
    headers['Cookie'] = get_Cookie(form_data,headers)
    if headers['Cookie'] is None:
        print('Cookie is None')
        sys.exit()

    url1 = 'https://api.xiaoheihe.cn/game/pubg/get_stats_detail/?heybox_id=14909789&region=steam'
    queue1 = Queue()
    Thread(target=put_into_queue1, args=(queue1, url1, headers), daemon=True).start()
    time.sleep(600)
    Thread(target=get_from_queue1, args=(queue1, db), daemon=True).start()

    queue1.join()

    # for rank in db.find_today_rank():
    #     p = {}
    #     p['nickname'] = rank['nickname']
    #     p['season'] = rank['season']
    #     if 'fpp' not in rank['mode']:
    #         p['fpp'] = '0'
    #         p['mode'] = rank['mode']
    #         # r = requests.get('https://api.xiaoheihe.cn/game/pubg/get_stats_detail/?heybox_id=14909789&fpp=0&mode=duo&nickname=HuYaTV-17044129&region=steam&season=pc-2018-02',
    #         res = requests.get('https://api.xiaoheihe.cn/game/pubg/get_stats_detail/?heybox_id=14909789&region=steam',
    #                          params=p,headers=headers).json()['result']
    #         # print(res)
    #         overview = {}
    #         overview['mode'] = rank['mode']
    #         overview['season'] = rank['season']
    #         overview['nickname'] = rank['nickname']
    #
    #         overview['rateing'] = res['overview'][0]['value']
    #         overview['win_times'] = res['overview'][1]['value']
    #         overview['win_times_rank'] = res['overview'][1]['rank']
    #         overview['top10_times'] = res['overview'][2]['value']
    #         overview['top10_times_rank'] = res['overview'][2]['rank']
    #         overview['avg_kills'] = res['overview'][3]['value']
    #         overview['avg_kills_rank'] = res['overview'][3]['rank']
    #         overview['ranks'] = res['overview'][4]['value']
    #         overview['win_ratio'] = res['overview'][5]['value']
    #         overview['win_ratio_rank'] = res['overview'][5]['rank']
    #         overview['top10_ratio'] = res['overview'][6]['value']
    #         overview['top10_ratio_rank'] = res['overview'][6]['rank']
    #         overview['k_d'] = res['overview'][7]['value']
    #         overview['k_d_rank'] = res['overview'][7]['rank']
    #
    #         db.save_one_data_to_player_overview(overview)


    db.close()

# https://www.cnblogs.com/cdwp8/p/4355819.html

# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402685&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=10fe9dc9bd15d63d7e8efbed1be202cd&limit=30&offset=0&season=2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402745&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=4f448a5e004a33f68c3750c540560b1a&limit=30&offset=0&season=pc-2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402881&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=b7205992fa31bba3f5fc396137bad193&limit=30&mode=solo&offset=0
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402912&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=363203c11f79e19cc6626fe507e70760&category=WinRatio&limit=30&mode=solo&offset=0

# /game/pubg/get_stats_detail/?lang=zh-cn&os_type=iOS&os_version=10.3.3&_time=1548776142&version=1.1.52&device_id=D2AA4D4F-AC80-476C-BFE1-CBD83AB74133&heybox_id=5141514&hkey=06a344301cb7c6cdc1136a62c061c978&fpp=0&mode=solo&nickname=HuYaTV_15310849&region=steam&season=pc-2018-02
# http://api.maxjia.com/
# https://api.xiaoheihe.cn/
