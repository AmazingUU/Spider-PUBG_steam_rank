'''
玩家详细数据类
对应数据库六张表：
player_overview、radar_score、fight_behavior、survive_behavior、support_behavior、motion_behavior
'''


class Item(object):
    def set(self, detail):
        data = {}
        data.setdefault('overview', {})

        data['overview']['mode'] = detail['params']['mode']

        data['overview']['season'] = detail['params']['season']
        data['overview']['nickname'] = detail['params']['nickname']

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

        data.setdefault('radar_score', {})
        data['radar_score']['mode'] = detail['params']['mode']

        data['radar_score']['season'] = detail['params']['season']
        data['radar_score']['nickname'] = detail['params']['nickname']

        data['radar_score']['survive'] = detail['radar_score'][0]['value']
        data['radar_score']['win_ratio'] = detail['radar_score'][1]['value']
        data['radar_score']['support'] = detail['radar_score'][2]['value']
        data['radar_score']['kills'] = detail['radar_score'][3]['value']
        data['radar_score']['rating'] = detail['radar_score'][4]['value']

        data.setdefault('fight_behavior', {})
        data['fight_behavior']['mode'] = detail['params']['mode']

        data['fight_behavior']['season'] = detail['params']['season']
        data['fight_behavior']['nickname'] = detail['params']['nickname']

        data['fight_behavior']['rating'] = detail['stats'][0]['score_value']
        data['fight_behavior']['degree'] = detail['stats'][0]['score']
        data['fight_behavior']['avg_kills'] = detail['stats'][0]['overview'][0]['value']
        data['fight_behavior']['avg_kills_degree'] = detail['stats'][0]['overview'][0]['score']
        data['fight_behavior']['avg_damage'] = detail['stats'][0]['overview'][1]['value']
        data['fight_behavior']['avg_damage_degree'] = detail['stats'][0]['overview'][1]['score']
        data['fight_behavior']['avg_head_shoot'] = detail['stats'][0]['overview'][2]['value']
        data['fight_behavior']['avg_head_shoot_degree'] = detail['stats'][0]['overview'][2]['score']
        data['fight_behavior']['head_shoot_ratio'] = detail['stats'][0]['overview'][3]['value']
        data['fight_behavior']['head_shoot_ratio_degree'] = detail['stats'][0]['overview'][3]['score']
        data['fight_behavior']['max_kills'] = detail['stats'][0]['overview'][4]['value']
        data['fight_behavior']['max_continuous_kills'] = detail['stats'][0]['overview'][5]['value']
        data['fight_behavior']['max_kills_distence'] = detail['stats'][0]['overview'][6]['value']
        data['fight_behavior']['avg_road_kills'] = detail['stats'][0]['overview'][7]['value']
        data['fight_behavior']['avg_road_kills_degree'] = detail['stats'][0]['overview'][7]['score']
        data['fight_behavior']['avg_car_distory'] = detail['stats'][0]['overview'][8]['value']
        data['fight_behavior']['avg_car_distory_degree'] = detail['stats'][0]['overview'][8]['score']

        data.setdefault('survive_behavior', {})
        data['survive_behavior']['mode'] = detail['params']['mode']

        data['survive_behavior']['season'] = detail['params']['season']
        data['survive_behavior']['nickname'] = detail['params']['nickname']

        data['survive_behavior']['rating'] = detail['stats'][1]['score_value']
        data['survive_behavior']['degree'] = detail['stats'][1]['score']
        data['survive_behavior']['avg_death'] = detail['stats'][1]['overview'][0]['value']
        data['survive_behavior']['avg_death_degree'] = detail['stats'][1]['overview'][0]['score']
        data['survive_behavior']['avg_survive_time'] = detail['stats'][1]['overview'][1]['value']
        data['survive_behavior']['avg_survive_time_degree'] = detail['stats'][1]['overview'][1]['score']
        data['survive_behavior']['max_survive_time'] = detail['stats'][1]['overview'][2]['value']

        data.setdefault('support_behavior', {})
        data['support_behavior']['mode'] = detail['params']['mode']

        data['support_behavior']['season'] = detail['params']['season']
        data['support_behavior']['nickname'] = detail['params']['nickname']

        data['support_behavior']['rating'] = detail['stats'][2]['score_value']
        data['support_behavior']['degree'] = detail['stats'][2]['score']
        data['support_behavior']['avg_assist'] = detail['stats'][2]['overview'][0]['value']
        data['support_behavior']['avg_assist_degree'] = detail['stats'][2]['overview'][0]['score']
        data['support_behavior']['avg_heal'] = detail['stats'][2]['overview'][1]['value']
        data['support_behavior']['avg_heal_degree'] = detail['stats'][2]['overview'][1]['score']
        data['support_behavior']['avg_relive'] = detail['stats'][2]['overview'][2]['value']
        data['support_behavior']['avg_relive_degree'] = detail['stats'][2]['overview'][2]['score']

        data.setdefault('motion_behavior', {})
        data['motion_behavior']['mode'] = detail['params']['mode']

        data['motion_behavior']['season'] = detail['params']['season']
        data['motion_behavior']['nickname'] = detail['params']['nickname']

        data['motion_behavior']['rating'] = detail['stats'][3]['score_value']
        data['motion_behavior']['degree'] = detail['stats'][3]['score']
        data['motion_behavior']['avg_running'] = detail['stats'][3]['overview'][0]['value']
        data['motion_behavior']['avg_running_degree'] = detail['stats'][3]['overview'][0]['score']
        data['motion_behavior']['avg_train'] = detail['stats'][3]['overview'][1]['value']
        data['motion_behavior']['avg_train_degree'] = detail['stats'][3]['overview'][1]['score']
        data['motion_behavior']['avg_move'] = detail['stats'][3]['overview'][2]['value']
        data['motion_behavior']['avg_move_degree'] = detail['stats'][3]['overview'][2]['score']

        return data
