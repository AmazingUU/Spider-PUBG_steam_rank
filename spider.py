import requests

url = 'https://api.xiaoheihe.cn/game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548401877&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=c1aa1c85ada7b8afee362867c291bc84&limit=30&offset=0'
headers = {
    'User-Agent': 'xiaoheihe/1.1.52 (iPhone; iOS 12.1.2; Scale/2.00)'
}
json = requests.get(url,headers=headers).json()
rank_list = json['result']['board']
ranks = []
for rank in rank_list:
    data = {}
    data['rank'] = rank['rank']
    data['nickname'] = rank['nickname']
    data['value'] = rank['value']
    print(data)
    ranks.append(data)
rating_distribution_list = json['result']['rating_distribution']
distributions = []
for dis in rating_distribution_list:
    data = {}
    data['range'] = dis['start'] + '~' + dis['end']
    data['top'] = dis['top']
    print(data)
    distributions.append(data)

# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402685&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=10fe9dc9bd15d63d7e8efbed1be202cd&limit=30&offset=0&season=2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402745&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=4f448a5e004a33f68c3750c540560b1a&limit=30&offset=0&season=pc-2018-02
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402881&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=b7205992fa31bba3f5fc396137bad193&limit=30&mode=solo&offset=0
# /game/pubg/get_player_leaderboards/?lang=zh-cn&os_type=iOS&os_version=12.1.2&_time=1548402912&version=1.1.52&device_id=6635D9A6-4C84-43E9-953F-BF4304E19324&heybox_id=5141514&hkey=363203c11f79e19cc6626fe507e70760&category=WinRatio&limit=30&mode=solo&offset=0
