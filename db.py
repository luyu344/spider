import pymysql
import random
import re
import traceback
from se_ctrip.settings import MYSQL_DB,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER,XC_TABLE,HOTEL_LIST
import traceback
import time

class MysqlClient():

    def __init__(self):
        self.db=pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB,use_unicode=True,charset='utf8')
        self.cursor=self.db.cursor()


    def get_from_base_table(self):
        """
        获取基础表酒店id
        :return:
        """
        sql='select distinct hotel_id from {}'.format(HOTEL_LIST)
        self.cursor.execute(sql)
        results=self.cursor.fetchall()
        lists=[]
        for i in results:
            lists.append(i[0])
        print(len(lists),lists)
        return lists

    def update_xc(self,item):
        if '钟点' not in item['roomname'] and '起订' not in item['roomname']:
            values = ','.join(['%s'] * len(item))
            keys = ','.join(item.keys())
            sql = 'INSERT INTO {}({}) VALUES({}) on duplicate key update date_price={},add_time="{}",pay="{}",is_able="{}",breakfast="{}"  '.format(XC_TABLE, keys, values,item['date_price'], item['add_time'], item['pay'], item['is_able'],item['breakfast'])
            try:
                self.db.ping(reconnect=True)
                self.cursor.execute(sql,tuple(item.values()))
                # self.db.commit()
                print('写入成功')
            except:
                traceback.print_exc()
                print('写入失败')
                self.db.rollback()





    def delete_old(self,id,start_date):
        """删除某天某酒店数据"""
        sql='delete from {} where hotel_id={} and start_date="{}" '.format(XC_TABLE,id,start_date)
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def offlineHotel(self,id,start_date):
        """携程数据写入前先下线所有房型"""
        c = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql='update {} set is_able="0",add_time="{}" where hotel_id={} and start_date="{}" '.format(XC_TABLE,c,id,start_date)
        try:
            # print("下线成功")
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            # print('下线失败')
            self.db.rollback()


    def get_base_table_info(self):
        sql='select * from {}'.format('price_rate_1')
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        # print(len(results),results)
        # items=[]
        # for i in results:
        #     items.append(i[1:])
        # print(items)
        print(results)
        return results
    def add_to_base_table(self,item):
        # sql='insert into {}(hotel_name,hotel_id,fg_hotel_id,room_type,bed_type,fg_room_type,fg_real_hotel_id,fg_room_type_id,good_id,fg_real_hotel_outer_id,fg_room_type_outer_id) select hotel_name,hotel_id,fg_hotel_id,room_type,bed_type,fg_room_type,fg_real_hotel_id,fg_room_type_id,good_id,fg_real_hotel_outer_id,fg_room_type_outer_id from {}'.format(HOTEL_LIST,'new_hotel_list_1')
        sql='insert into price_rate(fg_hid,rate) values({},"{}")'.format(item[0],item[1])

        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            self.db.commit()
            print('w')
        except:
            traceback.print_exc()
            self.db.rollback()

    def __del__(self):
        self.db.close()

    def get_switch(self):
        sql='select rate from price_rate where fg_hid=2'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result[0].replace(' ','')=='1':
            return True
        else:
            return False
        # return lists
    def change_ip(self,vps_number):
        sql='update VPS set status="1" where number="{}"'.format(vps_number)
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            traceback.print_exc()
            self.db.rollback()

    def check_ip_status(self,vps_number):
        sql='select status from VPS where number="{}"'.format(vps_number)
        self.cursor.execute(sql)
        result=self.cursor.fetchone()
        return result[0]

    def get_phone_by_vps(self,vps_number):
        sql='select user from ctrip_account where vps_name="{}" '.format(vps_number)
        self.cursor.execute(sql)
        results=self.cursor.fetchall()
        result=random.choice(results)
        # print(result)
        return  result[0]

if __name__=="__main__":


    s=MysqlClient()
    # s.get_from_base_table()
    s.get_phone_by_vps('vps_1')
    # items=s.get_base_table_info()
    # # s.add_to_base_table()
    # for i in items:
    #     s.add_to_base_table(i)
