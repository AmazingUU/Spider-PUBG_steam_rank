'''
主程序
'''
import sys
import time

import requests

from db_helper import DbHelper
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Manager as ThreadManager

from items import Item

# 获取各个模式下前一百名的玩家简要信息
def get_player_leaderboards(url, params, headers):
    try:
        json = requests.get(url, params=params, headers=headers).json()
        result = json['result']
        return result
    except Exception as e:
        print('get_player_leaderboards() error:', str(e))
        return None

# 从简要信息中解析rank排名
def get_rank(result, params):
    rank_list = result['board']
    for rank in rank_list:
        data = {}
        data['rank'] = rank['rank']
        data['nickname'] = rank['nickname']
        data['value'] = rank['value']
        data['mode'] = params['mode']
        data['season'] = params['season']
        data['category'] = params['category']
        yield data

# 从简要信息中解析rank分布
def get_distribution(result, params):
    rating_distribution_list = result['rating_distribution']
    for dis in rating_distribution_list:
        data = {}
        data['start'] = dis['start']
        data['end'] = dis['end']
        data['top'] = dis['top']
        data['mode'] = params['mode']
        data['season'] = params['season']
        data['category'] = params['category']
        yield data

# 获取Cookie
def get_Cookie(form_data, headers):
    headers['Referer'] = 'http://api.maxjia.com/'
    try:
        r = requests.post('https://api.xiaoheihe.cn/account/login/',
                          data=form_data, headers=headers).json()

        return 'pkey=' + r['result']['pkey']
    except Exception as e:
        print('get_Cookie error:', str(e))
        return None

# 获取各个玩家的整体数据
def get_player_data(url, params, headers):
    try:
        json = requests.get(url, params=params, headers=headers).json()
        detail = json['result']
        return detail
    except Exception as e:
        print('get_player_data() error:', str(e))
        return None

# 从整体数据中解析出需要的数据
def get_needed_data(detail):
    item = Item().set(detail)
    yield item


def put_into_pool(queue, url, params, headers):
    detail = get_player_data(url, params, headers)
    detail['params'] = params
    queue.put_nowait(detail)


def get_from_pool(queue, db):
    while True:
        try:
            detail = queue.get_nowait()
            if detail:
                for data in get_needed_data(detail):
                    db.save_one_data_to_player_overview(data['overview'])
                    db.save_one_data_to_radar_score(data['radar_score'])
                    db.save_one_data_to_fight_behavior(data['fight_behavior'])
                    db.save_one_data_to_survive_behavior(data['survive_behavior'])
                    db.save_one_data_to_support_behavior(data['support_behavior'])
                    db.save_one_data_to_motion_behavior(data['motion_behavior'])
                queue.task_done()
            else:
                queue.task_done()
                continue
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

    # 键盘输入需要查询的模式、赛季、分类
    while True:
        try:
            mode = mode_list[input('请选择模式(单人,双人,四排,第一人称单人,第一人称双人,第一人称四排):')]
            season = season_list[input('请选择赛季(2018第x赛季):')]
            category = category_lsit[input('请选择分类(积分、吃鸡率、场均击杀、场均伤害、游戏场数):')]
            break
        except:
            print('输入有误，请重新输入')

    params = {'mode': mode, 'season': season, 'category': category}
    # url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=10.3.3&version=1.1.52&device_id=D2AA4D4F-AC80-476C-BFE1-CBD83AB74133&heybox_id=5141514&limit=30&offset=0&mode=solo&season=pc-2018-02&category=WinRatio'
    # 上面为抓包拿到的url，经过测试，其他参数可省略，只需下面的url即可
    url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/'

    headers = {
        'User-Agent': 'xiaoheihe/1.1.52 (iPhone; iOS 10.3.3; Scale/2.00)'
    }
    configs = {'host': 'localhost', 'user': 'root', 'password': 'admin', 'db': 'pubg_steam'}
    db = DbHelper()
    db.connenct(configs)

    # 获取输入参数对应模式的前一百名简要数据
    result = get_player_leaderboards(url, params, headers)
    if result:
        par = []
        for data in get_rank(result, params):# rank排名保存到数据库
            db.save_one_data_to_rank(data)
            if 'fpp' not in data['mode']:
                # 将后面爬取时需要提供的参数保存下来
                par.append({'nickname': data['nickname'], 'season': data['season'], 'mode': data['mode'], 'fpp': '0'})
            else:
                par.append({'nickname': data['nickname'], 'season': data['season'], 'mode': data['mode'], 'fpp': '1'})

        for data in get_distribution(result, params):# rank分布保存到数据库
            db.save_one_data_to_distribution(data)
    else:
        print('get_player_leaderboards fail')
        sys.exit()

    # 加密后的登录参数
    form_data = {
        'phone_num': 'M6Y3WpfSNET9W4ZwcML1tUx+jvOWtaDKwoUM3ABM+o7AXi8yZKplkUSM3u3R9cN+x4CNZ2Mo/SHFqB8nQWNt9WHEKc3iC0nSfTfbhlLJECCLpB60Cpbo7HKjE9dlY8s7kJY8bCn+xHAXEGg/2avB2SRPFLPo+Nm0JO6R07Sof4U=',
        'pwd': 'OKNkTFqOU26Adb/9IAvze4K+u6aBHpd9cvBuyRWWAifDyb48wAvLbGUHfj0ZtTvGdg3Y2k8x9EyzcvW/G36R9ukCVpa+xJFztKM8GIl1q71OPNSTx0u1+EM6JiZnGxvPWApt0coRLm64BkRBcbhgliSauUlheBBfoAIADSNlXpw='
    }

    headers['Cookie'] = get_Cookie(form_data, headers)
    if headers['Cookie'] is None:
        print('Cookie is None')
        sys.exit()

    # url = 'https://api.xiaoheihe.cn/game/pubg/get_stats_detail/?lang=zh-cn&os_type=iOS&os_version=10.3.3&_time=1548776142&version=1.1.52&device_id=D2AA4D4F-AC80-476C-BFE1-CBD83AB74133&heybox_id=5141514&hkey=06a344301cb7c6cdc1136a62c061c978&fpp=0&mode=solo&nickname=HuYaTV_15310849&region=steam&season=pc-2018-02
    # 上面为抓包拿到的url，经过测试，其他参数可省略，只需下面的url即可
    url1 = 'https://api.xiaoheihe.cn/game/pubg/get_stats_detail/?heybox_id=14909789&region=steam'
    put_thread_pool = ThreadPool(5)
    get_thread_pool = ThreadPool()
    queue = ThreadManager().Queue()  # 线程池之间通信需要用Manager().Queue()，线程间通信用Queue()
    for i in range(len(par)):
        # 利用线程池的优点在于便于控制线程数量，生产线程池中最多有五个生产线程，提高了生产效率，又不会在线程间切换花费太多时间
        put_thread_pool.apply_async(put_into_pool, (queue, url1, par[i], headers))

    time.sleep(3)  # 让生产者先生产3s，保证queue中有初始数据量

    get_thread_pool.apply_async(get_from_pool, (queue, db))

    queue.join() # 目的是阻塞主线程

    db.close()
