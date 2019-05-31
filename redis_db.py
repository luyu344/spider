import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+"."))
import redis
from se_ctrip.settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,BASE_TABLE,TASK_TABLE
import random

class Redisclient():

    def __init__(self):
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    def add_all_id(self,items):
        for num,i in enumerate(items):
            print('添加：',i)

            self.db.rpush('x_base_ids',i)
        return

    def add_to_task_ids(self):

        result=self.db.lrange(BASE_TABLE,0,-1)
        for i in result:
            self.db.rpush(TASK_TABLE,i)

    def get_one_task(self):
        result=self.db.lpop(TASK_TABLE)

        return result
    def add_account(self,keyname,user):
        self.db.hset('ctrip_account',keyname,user)

    def get_ip(self,vps_number):
        result=self.db.hget('adsl_proxy',vps_number)
        print(result)
        return result

    def back_to_task(self,id):
        self.db.rpush(TASK_TABLE,id)

    def get_account(self,keyname):
        result =self.db.hget('ctrip_account',keyname)
        if result:
            return eval(result)
        else:
            return None
    def get_random_ctrip_account(self):
        all=self.db.smembers('all_ctrip_account')
        a=random.sample(all,45)
        keysname=[]
        for n in range(3):
            keysname+=['vps_'+str(j)+'_'+str(n) for j in range(1,24)]
        final=random.sample(keysname,45)
        result=zip(final,a)
        self.db.delete('ctrip_account')
        for key,value in result:
            self.add_account(key,value)
    def get_random_cookies(self):
        result=random.choice(self.db.hvals('cookies:ctrip'))
        # print(result)
        return result
if __name__=='__main__':
    s=Redisclient()
    s.get_random_ctrip_account()
