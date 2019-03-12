# -*- coding: utf-8 -*-
# @Author: gunjianpan
# @Date:   2019-02-28 09:47:07
# @Last Modified by:   gunjianpan
# @Last Modified time: 2019-02-28 10:57:23

import re

from proxy.getproxy import GetFreeProxy
from utils.utils import begin_time, get_html, end_time, changeCookie, changeHeaders, changeHtmlTimeout, can_retry


class southPark(object):
    """
    load download South Park url from zimuzu
    """

    def __init__(self):
        self.proxyclass = GetFreeProxy()

    def load_url(self):
        """
        load url form zimuzu
        """

        url = 'http://zmz005.com/o5itP3'
        detail = self.proxyclass.get_request_proxy(url, 0)
        total = []

        if not detail:
            print('retry')
            if can_retry(url):
                self.load_url()
            return
        season_list = detail.find_all(
            'div', class_='tab-content info-content')[1:]
        for season in season_list:
            quality_list = season.find_all('div', class_='tab-pane')
            url_body = quality_list[1] if 'APP' in quality_list[0]['id'] else quality_list[0]
            season_id = re.findall(r"\d+\.?\d*", url_body['id'])[0]
            total.append(season_id)
            if int(season_id) < 12:
                url_body = quality_list[1]

            url_list = url_body.find_all('ul', class_='down-links')
            url = [index.find_all('div', class_='copy-link')[1]['data-url']
                   for index in url_list]
            total.append('\n'.join(url) + '\n')
        with open('zimuzu/data/southPark', 'w') as f:
            f.write('\n'.join(total))
