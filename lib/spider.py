from datetime import datetime
from queue import Queue
from random import random, randint

import requests
from bs4 import BeautifulSoup
import threading
from lib.storge import Storge
from lib.msg import MessageType, show_message
from tqdm import tqdm
from time import sleep


class Spider:
    def __init__(self, max_work=5, db_path='lib/company.db'):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }
        self.list_max_work = threading.Semaphore(max_work)
        self.page = self.page_num_spider()
        self.company_list = Queue(maxsize=500)
        self.db_path = db_path

    def set_max_work(self, max_work):
        self.list_max_work = max_work

    def set_headers(self, headers):
        self.headers = headers

    def page_num_spider(self):
        url = 'https://www.butian.net/Reward/pub'
        data = {
            ' ajax': 1,
            'p': 1
        }
        req = requests.post(url, headers=self.headers, data=data)
        res_data = req.json()
        req.close()
        try:
            page_num = res_data['data']['count']
            return page_num
        except IndexError:
            show_message('页数获取失败', MessageType.ERROR)
            return 0

    def page_spider(self, page=1):
        sleep(randint(0, 3))
        url = 'https://www.butian.net/Reward/pub'
        data = {
            ' ajax': 1,
            'p': page
        }
        req = requests.post(url, headers=self.headers, data=data)
        try:
            res_data = req.json()
            req.close()
            list = res_data['data']['list']
            self.company_list.put(list, block=True)
            self.list_max_work.release()
            return list
        except IndexError:
            self.list_max_work.release()
            return None
        except Exception as e:
            sleep(randint(3, 5))
            self.page_spider(page)

    def domain_spider(self, company_id):
        url = f'https://www.butian.net/Loo/submit?cid={company_id}'
        req = requests.get(url, headers=self.headers)
        login_msg = "We're sorry but 奇安信｜用户登录 doesn't work properly without JavaScript enabled. Please enable it to continue."
        text = req.text
        req.close()
        if login_msg in text:
            show_message('需要登录', MessageType.ERROR)
            self.set_cookie()
            self.domain_spider(company_id)
        else:
            soup = BeautifulSoup(text, 'html.parser')
            element = soup.find('input', {'name': 'host'})
            if element:
                domain = element.get('value')
                if not domain:
                    return 'unknown'
                return domain
            return None

    def set_cookie(self):
        show_message('请输入Cookie')
        self.headers['Cookie'] = input('>>')

    def get_company_list(self, page=0):
        if page == 0:
            page = self.page
        for page in tqdm(range(1, page + 1), desc='获取公司列表中', colour='green'):
            self.list_max_work.acquire()
            threading.Thread(target=self.page_spider, args=(page,)).start()
        self.company_list.put('end')

    def get_company_domain(self):
        s = Storge(self.db_path)
        company_data = s.select_all_domain_null_data()
        for company in tqdm(company_data, desc='获取域名信息中', colour='green'):
            company_id = company['company_id']
            domain = self.domain_spider(company_id)
            if domain:
                s.update_domain_by_id(company_id, domain)

    def save_company_list(self):
        count = 0
        storge = Storge(self.db_path)
        while True:
            res = self.company_list.get(block=True)
            if res == 'end':
                break
            for item in res:
                company_id = item['company_id']
                company_name = item['company_name']
                if company_name and company_id:
                    count += 1
                    storge.insert_company(company_name, company_id)
        show_message(f'更新结束,获取到了{count}个公司', MessageType.SUCCESS)

    def start_list(self, page=0):
        threading.Thread(target=self.get_company_list, args=(page,)).start()
        threading.Thread(target=self.save_company_list).start()

    def start_domain(self):
        threading.Thread(target=self.get_company_domain).start()
