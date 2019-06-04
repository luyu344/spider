import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+"."))
from se_ctrip.se import Ctrip
from se_ctrip.db import MysqlClient
import traceback
from se_ctrip.time_queue import date_query
from se_ctrip.redis_db import Redisclient
import datetime
import threading
from se_ctrip.settings import VPS_NUMBER,THREAD_NUM
import time
import requests

def run(vps_number,i):
    try:
        redis = Redisclient()
        client=MysqlClient()
        ctr=Ctrip()
        VPS=VPS_NUMBER
        try:
            # VPS=ctr.login(vps_number+'_'+str(i))
            ctr.browser.get('https://accounts.ctrip.com/H5Login/Index')
            phone_number=client.get_phone_by_vps(VPS)
            login_cookies=eval(redis.get_cookies_by_phone(phone_number))
            ctr.add_login_cookie(login_cookies)
            VPS=check_login(login_cookies,VPS)
        except:
            traceback.print_exc()
        # ids=client.get_from_base_table()
        dates = date_query()
        while 1:
            try:
                id=redis.get_one_task()
            except:
                del ctr,redis,client
                raise RuntimeError('数据库连接超时....')

            if id:
                
                for date in dates:
                    results=ctr.run(id,date,VPS)
                    start_date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
                    try:
                        client.delete_old(id,start_date)
                    except:
                        del ctr,redis,client
                        raise RuntimeError('数据库连接超时....')
                    for result in results:
                        if result==1:
                            try:
                                redis.back_to_task(id)
                            except:
                                del ctr, redis, client
                                raise RuntimeError('数据库连接超时....')

                            if i == 0:
                                #print('{}更换ip.......'.format(vps_number))
                                pass
                            break
                        try:
                            client.update_xc(result)
                        except:
                            del ctr,redis,client
                            raise RuntimeError('数据库连接超时....')


            else:
                if i == 0:
                    print("更新任务队列")
                    try:
                        redis.add_to_task_ids()
                    except:
                        del ctr,redis,client
                        raise RuntimeError('数据库连接超时....')
                    time.sleep(2)

    except:
        traceback.print_exc()
        time.sleep(3)
        run(vps_number,i)
        
def main():

    for i in range(THREAD_NUM):
        thread=threading.Thread(target=run,args=('vps_',i))
        thread.start()
        print('vps_'+'启动thread:',i)

def check_login(cookies,vps_number):
    dict = {}
    print(cookies)
    for cookie in cookies:
        dict[cookie['name']] = cookie['value']
    headers = {
        'authority': 'm.ctrip.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9'

    }
    try:
        response=requests.get('https://m.ctrip.com/webapp/h5myinfo/accounts',headers=headers, cookies=dict, timeout=8, allow_redirects=False)
        if response.status_code == 200 and '退出' in response.text:
            # print('Cookies有效')
            # print(response.text)
            return vps_number
        else:
            return ''
    except:
        traceback.print_exc()
        return ''



if __name__=='__main__':
    main()
