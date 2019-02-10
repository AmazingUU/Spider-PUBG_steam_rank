'''
数据库操作类
所需表：rank_list、distribution、player_overview、radar_score、fight_behavior、survive_behavior、support_behavior、motion_behavior
建表语句：
create table if not exists rank_list(id int primary key auto_increment,ranks varchar(5),nickname varchar(30),value varchar(10),mode varchar(20),season varchar(20),category varchar(20),create_time datetime);
create table if not exists distribution(id int primary key auto_increment,start varchar(10),end varchar(10),top varchar(20),mode varchar(20),season varchar(20),category varchar(20),create_time datetime);
create table if not exists player_overview(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),rateing varchar(10),ranks varchar(5),win_times int(5),win_times_rank varchar(5),top10_times int(5),top10_times_rank varchar(5),avg_kills float(5),avg_kills_rank varchar(10),win_ratio varchar(10),win_ratio_rank varchar(10),top10_ratio varchar(10),top10_ratio_rank varchar(10),k_d float(5),k_d_rank varchar(10),create_time datetime)
create table if not exists radar_score(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),survive varchar(5),win_ratio varchar(5),support varchar(5),kills varchar(5),rating varchar(5),create_time datetime)
create table if not exists fight_behavior(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),rating varchar(5),degree varchar(5),avg_kills varchar(10),avg_kills_degree varchar(5),avg_damage varchar(10),avg_damage_degree varchar(5),avg_head_shoot varchar(5),avg_head_shoot_degree varchar(5),head_shoot_ratio varchar(10),head_shoot_ratio_degree varchar(5),max_kills int(2),max_continuous_kills int(2),max_kills_distence varchar(10),avg_road_kills varchar(5),avg_road_kills_degree varchar(5),avg_car_distory varchar(5),avg_car_distory_degree varchar(5),create_time datetime)
create table if not exists survive_behavior(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),rating varchar(5),degree varchar(5),avg_death varchar(5),avg_death_degree varchar(5),avg_survive_time varchar(10),avg_survive_time_degree varchar(5),max_survive_time varchar(10),create_time datetime)
create table if not exists support_behavior(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),rating varchar(5),degree varchar(5),avg_assist varchar(5),avg_assist_degree varchar(5),avg_heal varchar(5),avg_heal_degree varchar(5),avg_relive varchar(5),avg_relive_degree varchar(5),create_time datetime)
create table if not exists motion_behavior(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),rating varchar(5),degree varchar(5),avg_running varchar(10),avg_running_degree varchar(5),avg_train varchar(10),avg_train_degree varchar(5),avg_move varchar(10),avg_move_degree varchar(5),create_time datetime)
'''
import time

import pymysql


class DbHelper(object):
    def __init__(self):
        self.mutex = 0  # 锁信号
        self.db = None

    def connenct(self, configs):
        try:
            self.db = pymysql.connect(
                host=configs['host'],
                user=configs['user'],
                password=configs['password'],
                db=configs['db'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print('db connect success')
            return self.db
        except Exception as e:
            print('db connect fail,error:', str(e))
            return None

    def close(self):
        if self.db:
            self.db.close()
            print('db close')

    def save_one_data_to_rank(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into rank_list(ranks,nickname,value,mode,season,category,create_time) values(%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['rank'], data['nickname'], data['value'], data['mode'], data['season'], data['category']))
                self.db.commit()
                # self.mutex = 0  # 解锁
                print('{}\t{},{},{},{},{},{}\tinsert into rank_list'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['mode'], data['season'],
                    data['category'],
                    data['rank'], data['nickname'], data['value']))
        except Exception as e:
            print('{}\tsave rank:{}\tnickname:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['rank'], data['nickname'],
                str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_distribution(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into distribution(start,end,top,mode,season,category,create_time) values(%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['start'], data['end'], data['top'], data['mode'], data['season'], data['category']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{},{},{},{}\tinsert into distribution'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['mode'], data['season'],
                    data['category'],
                    data['start'], data['end'], data['top']))
        except Exception as e:
            print('{}\tsave distribution:{}~{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['start'], data['end'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_player_overview(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into player_overview(nickname,mode,season,rateing,ranks,' \
                      'win_times,win_times_rank,top10_times,top10_times_rank,avg_kills,' \
                      'avg_kills_rank,win_ratio,win_ratio_rank,top10_ratio,top10_ratio_rank,' \
                      'k_d,k_d_rank,create_time) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['nickname'], data['mode'], data['season'], data['rateing'], data['ranks'],
                    data['win_times'], data['win_times_rank'], data['top10_times'],
                    data['top10_times_rank'], data['avg_kills'], data['avg_kills_rank'],
                    data['win_ratio'], data['win_ratio_rank'], data['top10_ratio'],
                    data['top10_ratio_rank'], data['k_d'], data['k_d_rank']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into overview'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], data['mode'],
                    data['season']))
        except Exception as e:
            print('{}\tsave overview:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_radar_score(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into radar_score(nickname,mode,season,survive,win_ratio,' \
                      'support,kills,rating,create_time) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['nickname'], data['mode'], data['season'], data['survive'], data['win_ratio'],
                    data['support'], data['kills'], data['rating']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into radar_score'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], data['mode'],
                    data['season']))
        except Exception as e:
            print('{}\tsave radar_score:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_fight_behavior(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into fight_behavior(nickname,mode,season,rating,degree,avg_kills,avg_kills_degree,' \
                      'avg_damage,avg_damage_degree,avg_head_shoot,avg_head_shoot_degree,' \
                      'head_shoot_ratio,head_shoot_ratio_degree,max_kills,max_continuous_kills,' \
                      'max_kills_distence,avg_road_kills,avg_road_kills_degree,' \
                      'avg_car_distory,avg_car_distory_degree,create_time) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['nickname'], data['mode'], data['season'], data['rating'], data['degree'], data['avg_kills'],
                    data['avg_kills_degree'],
                    data['avg_damage'], data['avg_damage_degree'], data['avg_head_shoot'],
                    data['avg_head_shoot_degree'],
                    data['head_shoot_ratio'], data['head_shoot_ratio_degree'], data['max_kills'],
                    data['max_continuous_kills'],
                    data['max_kills_distence'], data['avg_road_kills'], data['avg_road_kills_degree'],
                    data['avg_car_distory'], data['avg_car_distory_degree']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into fight_behavior'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], data['mode'],
                    data['season']))
        except Exception as e:
            print('{}\tsave fight_behavior:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_survive_behavior(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into survive_behavior(nickname,mode,season,rating,degree,avg_death,avg_death_degree,' \
                      'avg_survive_time,avg_survive_time_degree,max_survive_time,create_time) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['nickname'], data['mode'], data['season'], data['rating'], data['degree'], data['avg_death'],
                    data['avg_death_degree'],
                    data['avg_survive_time'], data['avg_survive_time_degree'], data['max_survive_time']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into survive_behavior'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], data['mode'],
                    data['season']))
        except Exception as e:
            print('{}\tsave survive_behavior:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_support_behavior(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into support_behavior(nickname,mode,season,rating,degree,avg_assist,avg_assist_degree,' \
                      'avg_heal,avg_heal_degree,avg_relive,avg_relive_degree,create_time) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['nickname'], data['mode'], data['season'], data['rating'], data['degree'], data['avg_assist'],
                    data['avg_assist_degree'],
                    data['avg_heal'], data['avg_heal_degree'], data['avg_relive'], data['avg_relive_degree']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into support_behavior'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], data['mode'],
                    data['season']))
        except Exception as e:
            print('{}\tsave support_behavior:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_motion_behavior(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into motion_behavior(nickname,mode,season,rating,degree,avg_running,avg_running_degree,' \
                      'avg_train,avg_train_degree,avg_move,avg_move_degree,create_time) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['nickname'], data['mode'], data['season'], data['rating'], data['degree'], data['avg_running'],
                    data['avg_running_degree'],
                    data['avg_train'], data['avg_train_degree'], data['avg_move'], data['avg_move_degree']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into motion_behavior'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], data['mode'],
                    data['season']))
        except Exception as e:
            print('{}\tsave motion_behavior:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['nickname'], str(e)))
        finally:
            self.mutex = 0  # 解锁

    def find_today_rank(self):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'select nickname,mode,season from rank_list where to_days(create_time) = to_days(now())'
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except Exception as e:
            print('find_today_rank fail,error:', str(e))
            return None
        finally:
            self.mutex = 0  # 解锁
