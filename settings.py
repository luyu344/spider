#mysql配置

MYSQL_HOST='118.25.220.202'

MYSQL_USER='root'

MYSQL_PASSWORD='86948536ZG'

MYSQL_DB='fgzhegong'


#vps编号
NO=9

#redis配置
REDIS_HOST='118.25.220.202'

REDIS_PORT=6379

REDIS_PASSWORD='889F88143FAA06BE2B579B1E0375A00F'

BASE_TABLE='ctrip:base_ids_{}'.format(NO)

TASK_TABLE='ctrip:task_ids_{}'.format(NO)



#携程数据表名
XC_TABLE='xc_price_data'


#所有酒店数据表名
HOTEL_LIST='new_hotel_list'

#抓取起止时间
START=0
END=2

RECENT=[15,30]

VPS_NUMBER='vps_{}'.format(NO)

#线程数
THREAD_NUM=2