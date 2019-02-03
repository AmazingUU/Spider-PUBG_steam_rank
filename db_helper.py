'''
数据库操作类
所需表：rank_list、distribution
建表语句：
create table if not exists rank_list(id int primary key auto_increment,ranks varchar(5),nickname varchar(30),value varchar(10),mode varchar(20),season varchar(20),category varchar(20),create_time datetime);
create table if not exists distribution(id int primary key auto_increment,start varchar(10),end varchar(10),top varchar(20),mode varchar(20),season varchar(20),category varchar(20),create_time datetime);
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
