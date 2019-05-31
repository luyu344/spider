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
from se_ctrip.settings import VPS_NUMBER
import time
import requests
def run(vps_number,i):
    # vps_number = sys.argv[1]
    redis = Redisclient()
 #   ip=redis.get_ip(vps_number)
    ctr=Ctrip()
    VPS='vps_00'
 #   try:
 #       # VPS=ctr.login(vps_number+'_'+str(i))
 #       ctr.browser.get('https://accounts.ctrip.com/H5Login/Index')
 #       login_cookies=eval(redis.get_random_cookies())
 #       ctr.add_login_cookie(login_cookies)
 #       VPS=check_login(login_cookies,vps_number+'_'+str(i))
 #   except:
 #       traceback.print_exc()
  #  user_number=redis.get_account(vps_number+'_'+str(i))
  #  if user_number:
  #      try:
  #          account=user_number['username']
  #          pas=user_number['password']
  #          VPS=ctr.login(account, pas,vps_number+'_'+str(i))
  #      except:
  #          traceback.print_exc()
    client=MysqlClient()
    # ids=client.get_from_base_table()
    control=0
    while control !=1:
        dates = date_query()
        id=redis.get_one_task()
        if id:
            try:
                for date in dates:
                    if control !=1:
                        results=ctr.run(id,date,VPS)
                        # if results:
                        start_date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
                        client.delete_old(id,start_date)
                        for result in results:
                            if result==1:
                                control = 1
                                redis.back_to_task(id)
                              #  if i == 0:
                               #     client.change_ip(vps_number)
                                break
                            client.update_xc(result)


                    # else:
                    #     results = ctr.run(id, date)
                    #     start_date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
                    #     if results:
                    #         client.delete_old(id, start_date)
                    #         for result in results:
                    #             client.update_xc(result)
                    #     else:
                    #         client.delete_old(id,start_date)

            except:
                traceback.print_exc()
                for date in dates:
                    start_date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
                    client.delete_old(id,start_date)
        else:
            if vps_number=='vps_1' and i==0:
                print("更新任务队列")
                redis.add_to_task_ids()
                # os.system('ps -ef | grep chrome | grep -v grep | cut -c 9-15 | xargs kill -s 9')
                # run()
            time.sleep(2)
 #   print('更换ip.......')
    time.sleep(10)
    ctr.browser.close()
    del ctr
    client.db.close()
    run(vps_number,i)    

def main():
    for i in range(1):
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
