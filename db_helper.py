'''
数据库操作类
所需表：rank_list、distribution
建表语句：
create table if not exists rank_list(id int primary key auto_increment,ranks varchar(5),nickname varchar(30),value varchar(10),mode varchar(20),season varchar(20),category varchar(20),create_time datetime);
create table if not exists distribution(id int primary key auto_increment,start varchar(10),end varchar(10),top varchar(20),mode varchar(20),season varchar(20),category varchar(20),create_time datetime);
create table if not exists player_overview(id int primary key auto_increment,nickname varchar(30),mode varchar(20),season varchar(20),rateing varchar(10),ranks varchar(5),win_times int(5),win_times_rank varchar(5),top10_times int(5),top10_times_rank varchar(5),avg_kills float(5),avg_kills_rank varchar(10),win_ratio varchar(10),win_ratio_rank varchar(10),top10_ratio varchar(10),top10_ratio_rank varchar(10),k_d float(5),k_d_rank varchar(10),create_time datetime)
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
                print('{}\t{},{},{},{},{},{}\tinsert into rank_list'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),data['mode'], data['season'], data['category'],
                                                        data['rank'], data['nickname'], data['value']))
        except Exception as e:
            print('{}\tsave rank:{}\tnickname:{} fail,error:{}'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['rank'],data['nickname'], str(e)))
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
                    data['start'], data['end'], data['top'], data['mode'], data['season'],data['category']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{},{},{},{}\tinsert into distribution'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), data['mode'], data['season'],data['category'],
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
                    data['win_times'],data['win_times_rank'],data['top10_times'],
                    data['top10_times_rank'], data['avg_kills'], data['avg_kills_rank'],
                    data['win_ratio'],data['win_ratio_rank'],data['top10_ratio'],
                    data['top10_ratio_rank'],data['k_d'],data['k_d_rank']))
                self.db.commit()
                self.mutex = 0  # 解锁
                print('{}\t{},{},{}\tinsert into overview'.format(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),data['nickname'], data['mode'], data['season']))
        except Exception as e:
            print('{}\tsave overview:{} fail,error:{}'.format(
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
