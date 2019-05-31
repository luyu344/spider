from selenium import  webdriver
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import re
from pyquery import PyQuery as pq
import traceback
import os
import zipfile
import datetime
from se_ctrip.db import MysqlClient
from se_ctrip.move_track import get_track
from selenium.webdriver import ActionChains
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1200,900))
display.start()


class Ctrip():

    def __init__(self):

        self.chromeOptions = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
            }}
        self.chromeOptions.add_experimental_option('prefs', prefs)
   #     self.chromeOptions.add_extension(self.get_chrome_proxy_extension(proxy='H2X613YYFK51FC3P:B14B52D0CBC69644@http-pro.abuyun.com:9010'))
 #       self.chromeOptions.add_argument('--proxy-server=http://{}:8090'.format(proxy))
        # self.chromeOptions.add_argument("--headless")
        self.chromeOptions.add_argument('--proxy-server=http://127.0.0.1:8080')
        self.chromeOptions.add_argument("log-level=3")
        self.chromeOptions.add_argument('user-agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN')
        self.chromeOptions.add_argument('--window-size=450,500')
        self.chromeOptions.add_argument("--disable-gpu")
        self.chromeOptions.add_experimental_option('excludeSwitches',['enable-automation'])
        self.chromeOptions.add_argument('--no-sandbox')
        self.chromeOptions.add_argument('--disable-dev-shm-usage')
        self.browser=webdriver.Chrome(chrome_options=self.chromeOptions)
        self.wait=WebDriverWait(self.browser,120)
        self.url='http://hotels.ctrip.com/hotel/tianjin3'
        self.num_switch=self.get_switch_value()
 #       self.browser.set_page_load_timeout(35)

    def get_switch_value(self):
        s=MysqlClient()
        result=s.get_switch()
        return result

    def add_login_cookie(self,items):
        for i in items:
            self.browser.add_cookie(i)


    def __del__(self):
        self.browser.close()

    def get_chrome_proxy_extension(self,proxy):

        CHROME_PROXY_HELPER_DIR = 'Chrome-proxy-helper'
        CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'chrome-proxy-extensions'


        m = re.compile('(.*?):(.*?)@(.*?):(.*)').search(proxy)
        if m:
            # 提取代理的各项参数
            username = m.groups()[0]
            password = m.groups()[1]
            ip = m.groups()[2]
            port = m.groups()[3]
            print(username,password,ip,port)
            # 创建一个定制Chrome代理扩展(zip文件)
            if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
                os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
            extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(proxy.replace(':', '_')))
            if not os.path.exists(extension_file_path):
                # 扩展文件不存在，创建
                zf = zipfile.ZipFile(extension_file_path, mode='w')
                zf.write(os.path.join(CHROME_PROXY_HELPER_DIR, 'manifest.json'), 'manifest.json')
                # 替换模板中的代理参数
                background_content = open(os.path.join(CHROME_PROXY_HELPER_DIR, 'background.js')).read()
                background_content = background_content.replace('%proxy_host', ip)
                background_content = background_content.replace('%proxy_port', port)
                background_content = background_content.replace('%username', username)
                background_content = background_content.replace('%password', password)
                zf.writestr('background.js', background_content)
                zf.close()
            return extension_file_path
        else:
            raise Exception('Invalid proxy format. Should be username:password@ip:port')

    def run(self,hotel_id,start,vps_number):
        url='https://m.ctrip.com/webapp/hotel/hoteldetail/{}.html?atime={}&days=1&pay=1'.format(hotel_id,start)
#        if start==(datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y%m%d'):
#            url='https://m.ctrip.com/webapp/hotel/hoteldetail/{}.html?atime={}&days=3&pay=1'.format(hotel_id,start)
#            # print(url)
#        else:
#            url='https://m.ctrip.com/webapp/hotel/hoteldetail/{}.html?atime={}&days=1&pay=1'.format(hotel_id,start)
#            # print(url)
        try:
            self.browser.get(url)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'ul.dl-room-type')))
            sleep_time=random.randrange(2,5)
            time.sleep(sleep_time)
            html = self.browser.page_source
            c = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            hotelid = re.search('hoteldetail/(\d*).html', self.browser.current_url).group(1)
            start_date = re.search('atime=(\d*)', self.browser.current_url).group(1)
            start_date_1 = datetime.datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            end_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime(
                '%Y-%m-%d')
            doc = pq(html, parser='html')
            items = list(doc('li[data-ubt-key=c_hotel_inland_detail_room_basic]').items())
            items_1 = list(doc('ul.sub-romm.js_childroomlist').items())
            print('房型总数：', len(items_1), hotelid, start_date_1)
            if not len(items_1) == 0:
                for i in range(len(items_1)):
                    for one_room in items_1[i]('li[data-roomid]').items():
                        if self.num_switch:
                            if not ('仅剩' in one_room('div.room-bd div.cell-end p').text()) and not one_room(
                                    'div.room-bd div.cell-end.dl-disabled'):
                                item = {}
                                item['room_type_name'] = items[i]('div.room-bd h3').text().replace(' ', '').replace('（',
                                                                                                                    '(').replace(
                                    '）', ')').replace('代理','').replace('详情','')
                                item['start_date'] = start_date_1
                                item['end_date'] = end_date
                                item['roomname'] = one_room('div.room-bd p.room-size em').text()
                                item['breakfast'] = one_room('div.room-bd h4 em:nth-child(1)').text().replace('双早',
                                                                                                              '2').replace(
                                    '无早', '0').replace('单早', '1').replace('三早', '3').replace('四早', '4').replace('五早',
                                                                                                                '5').replace(
                                    '六早', '6').replace('八早', '8').replace('多份早餐', '7')
                                item['bed'] = one_room('div.room-bd h4 em:nth-child(2)').text().replace('大/双床',
                                                                                                        '3').replace(
                                    '大床', '1').replace('双床', '2').replace('多张床', '4').replace('单人床', '0')
                                item['pay'] = one_room('div.room-bd div.dl-btn-mod button:nth-child(2)').text().replace(
                                    '在线付', '3')
                                item['date_price'] = one_room('div.room-bd div.cell-star span.price').text().replace(
                                    '¥', '').replace('均','')
                                item['is_able'] = one_room(
                                    'div.room-bd div.dl-btn-mod button:nth-child(1)').text().replace('订完', '0').replace(
                                    '订', '1')
                                item['add_time'] = c
                                item['hotel_id'] = hotelid
                                item['room_id'] = one_room.attr('data-roomid')
                                item['login']=vps_number
                                print(item)
                                yield item
                        else:
                            if not one_room('div.room-bd div.cell-end p').text() == '仅剩1间' and not one_room(
                                    'div.room-bd div.cell-end.dl-disabled') and not one_room('div.room-bd div.cell-end p').text() == '仅剩2间':
                                item = {}
                                item['room_type_name'] = items[i]('div.room-bd h3').text().replace(' ', '').replace('（',
                                                                                                                    '(').replace(
                                    '）', ')').replace('代理','').replace('详情','')
                                item['start_date'] = start_date_1
                                item['end_date'] = end_date
                                item['roomname'] = one_room('div.room-bd p.room-size em').text()
                                item['breakfast'] = one_room('div.room-bd h4 em:nth-child(1)').text().replace('双早',
                                                                                                              '2').replace(
                                    '无早', '0').replace('单早', '1').replace('三早', '3').replace('四早', '4').replace('五早',
                                                                                                                '5').replace(
                                    '六早', '6').replace('八早', '8').replace('多份早餐', '7')
                                item['bed'] = one_room('div.room-bd h4 em:nth-child(2)').text().replace('大/双床',
                                                                                                        '3').replace(
                                    '大床', '1').replace('双床', '2').replace('多张床', '4').replace('单人床', '0')
                                item['pay'] = one_room('div.room-bd div.dl-btn-mod button:nth-child(2)').text().replace(
                                    '在线付', '3')
                                item['date_price'] = one_room('div.room-bd div.cell-star span.price').text().replace(
                                    '¥', '').replace('均','')
                                item['is_able'] = one_room(
                                    'div.room-bd div.dl-btn-mod button:nth-child(1)').text().replace('订完', '0').replace(
                                    '订', '1')
                                item['add_time'] = c
                                item['hotel_id'] = hotelid
                                item['room_id'] = one_room.attr('data-roomid')
                                item['login']=vps_number
                                print(item)
                                yield item

            if len(items) == 0:
                pattern = doc('li.recommend-item:not(.hourroom-item)')
                for p in pattern.items():
                    if not p('div.cell-star.room-column.dl-disabled') and not p('div.cell-end p').text()=='仅剩1间' and not p('div.cell-end p').text()=='仅剩2间':
                        item = {}
                        item['room_type_name'] = re.sub('\(.*\)', '', p('h3').text()).replace('代理','').replace('详情','').replace(' ', '')
                        item['start_date'] = start_date_1
                        item['end_date'] = end_date
                        item['roomname'] = ''
                        item['breakfast'] = p('p.room-size em:nth-child(2)').text().replace('双早', '2').replace('无早',
                                                                                                               '0').replace(
                            '单早', '1').replace('三早', '3').replace('四早', '4').replace('五早', '5').replace('六早',
                                                                                                        '6').replace(
                            '八早', '8').replace('多份早餐', '7')
                        item['bed'] = p('p.room-size em:nth-child(3)').text().replace('大/双床', '3').replace('大床',
                                                                                                           '1').replace(
                            '双床', '2').replace('多张床', '4').replace('单人床', '0')
                        item['pay'] = '3'
                        item['date_price'] = p('span.price').text().replace('¥', '').replace('均','')
                        item['is_able'] = p('button.dl-btn-t.js_bookButton').text().replace('订完', '0').replace('订', '1')
                        item['add_time'] = c
                        item['hotel_id'] = hotelid
                        item['room_id'] = p.attr('data-roomid')
                        item['login'] = vps_number
                        print(item)
                        yield item



        except:
            self.browser.close()
            traceback.print_exc()
            yield 1


    def login(self,account,pas,vps_number):
        self.browser.get('https://accounts.ctrip.com/H5Login/Index')
        username=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#txtUserName_login')))
        username.send_keys(account)
        password=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#txtLoginPwd_login')))
        password.send_keys(pas)
        submit=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#btnLogin')))
        submit.click()
        time.sleep(5)
        slide=self.browser.find_elements_by_css_selector('#login_slider_mask > div')
        if slide:
            width_element = self.browser.find_element_by_css_selector('div#login_slider')
            width = width_element.size
            check_code=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.cpt-drop-btn')))
            try:
               action = ActionChains(self.browser)
               Track = get_track(int(width['width'])+10)
               print(sum(Track))
               action.click_and_hold(check_code).perform()
               for distance in Track:
                   y_random = random.randrange(0, 5)
                   action.move_by_offset(distance, y_random).perform()
               action.release().perform()
               time.sleep(2)
            except:
               traceback.print_exc()
               pass

        time.sleep(20)
        if 'myctrip'  in self.browser.current_url:
            print(account,pas,'已登陆')
            return vps_number
        self.browser.save_screenshot('/root/test_/se_ctrip/images/{}.png'.format(account))
        return ''



    def parse_info(self,html):
        c = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        hotelid = re.search('hoteldetail/(\d*).html', self.browser.current_url).group(1)
        start_date = re.search('atime=(\d*)', self.browser.current_url).group(1)
        start_date_1 = datetime.datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
        end_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime(
            '%Y-%m-%d')
        doc = pq(html, parser='html')
        items = list(doc('li[data-ubt-key=c_hotel_inland_detail_room_basic]').items())
        items_1 = list(doc('ul.sub-romm.js_childroomlist').items())
        print('房型总数：', len(items_1), hotelid, start_date_1)
        if not len(items_1) == 0:
            for i in range(len(items_1)):
                for one_room in items_1[i]('li[data-roomid]').items():
                    if self.num_switch:
                        if not ('仅剩' in one_room('div.room-bd div.cell-end p').text()) and not one_room(
                                'div.room-bd div.cell-end.dl-disabled'):
                            item = {}
                            item['room_type_name'] = items[i]('div.room-bd h3').text().replace(' ', '').replace('（',
                                                                                                                '(').replace(
                                '）', ')')
                            item['start_date'] = start_date_1
                            item['end_date'] = end_date
                            item['roomname'] = one_room('div.room-bd p.room-size em').text()
                            item['breakfast'] = one_room('div.room-bd h4 em:nth-child(1)').text().replace('双早',
                                                                                                          '2').replace(
                                '无早', '0').replace('单早', '1').replace('三早', '3').replace('四早', '4').replace('五早',
                                                                                                            '5').replace(
                                '六早', '6').replace('八早', '8').replace('多份早餐', '7')
                            item['bed'] = one_room('div.room-bd h4 em:nth-child(2)').text().replace('大/双床',
                                                                                                    '3').replace(
                                '大床', '1').replace('双床', '2').replace('多张床', '4').replace('单人床', '0')
                            item['pay'] = one_room('div.room-bd div.dl-btn-mod button:nth-child(2)').text().replace(
                                '在线付', '3')
                            item['date_price'] = one_room('div.room-bd div.cell-star span.price').text().replace(
                                '¥', '')
                            item['is_able'] = one_room(
                                'div.room-bd div.dl-btn-mod button:nth-child(1)').text().replace('订完', '0').replace(
                                '订', '1')
                            item['add_time'] = c
                            item['hotel_id'] = hotelid
                            item['room_id'] = one_room.attr('data-roomid')
                            print(item)
                            yield item
                    else:
                        if not one_room('div.room-bd div.cell-end p').text() == '仅剩1间' and not one_room(
                                'div.room-bd div.cell-end.dl-disabled'):
                            item = {}
                            item['room_type_name'] = items[i]('div.room-bd h3').text().replace(' ', '').replace('（',
                                                                                                                '(').replace(
                                '）', ')')
                            item['start_date'] = start_date_1
                            item['end_date'] = end_date
                            item['roomname'] = one_room('div.room-bd p.room-size em').text()
                            item['breakfast'] = one_room('div.room-bd h4 em:nth-child(1)').text().replace('双早',
                                                                                                          '2').replace(
                                '无早', '0').replace('单早', '1').replace('三早', '3').replace('四早', '4').replace('五早',
                                                                                                            '5').replace(
                                '六早', '6').replace('八早', '8').replace('多份早餐', '7')
                            item['bed'] = one_room('div.room-bd h4 em:nth-child(2)').text().replace('大/双床',
                                                                                                    '3').replace(
                                '大床', '1').replace('双床', '2').replace('多张床', '4').replace('单人床', '0')
                            item['pay'] = one_room('div.room-bd div.dl-btn-mod button:nth-child(2)').text().replace(
                                '在线付', '3')
                            item['date_price'] = one_room('div.room-bd div.cell-star span.price').text().replace(
                                '¥', '')
                            item['is_able'] = one_room(
                                'div.room-bd div.dl-btn-mod button:nth-child(1)').text().replace('订完', '0').replace(
                                '订', '1')
                            item['add_time'] = c
                            item['hotel_id'] = hotelid
                            item['room_id'] = one_room.attr('data-roomid')
                            print(item)
                            yield item

        if len(items) == 0:
            pattern = doc('li.recommend-item:not(.hourroom-item)')
            for p in pattern.items():
                if not p('div.cell-star.room-column.dl-disabled'):
                    item = {}
                    item['room_type_name'] = re.sub('\(.*\)', '', p('h3').text())
                    item['start_date'] = start_date_1
                    item['end_date'] = end_date
                    item['roomname'] = ''
                    item['breakfast'] = p('p.room-size em:nth-child(3)').text().replace('双早', '2').replace('无早',
                                                                                                           '0').replace(
                        '单早', '1').replace('三早', '3').replace('四早', '4').replace('五早', '5').replace('六早',
                                                                                                    '6').replace(
                        '八早', '8').replace('多份早餐', '7')
                    item['bed'] = p('p.room-size em:nth-child(2)').text().replace('大/双床', '3').replace('大床',
                                                                                                       '1').replace(
                        '双床', '2').replace('多张床', '4').replace('单人床', '0')
                    item['pay'] = '3'
                    item['date_price'] = p('span.price').text().replace('¥', '')
                    item['is_able'] = p('button.dl-btn-t.js_bookButton').text().replace('订完', '0').replace('订', '1')
                    item['add_time'] = c
                    item['hotel_id'] = hotelid
                    item['room_id'] = p.attr('data-roomid')
                    print(item)
                    yield item


if __name__=="__main__":
    s=Ctrip('175.155.254.161')
    s.browser.get('https://www.baidu.com')
    time.sleep(9999)


