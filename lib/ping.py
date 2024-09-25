from pstats import SortKey
from token import STRING

from ping3 import ping
import threading
from tqdm import tqdm
from lib.msg import show_message, MessageType
from lib.storge import Storge


class Ping:
    def __init__(self,db_path='lib/company.db'):
        self.lock = threading.Semaphore(50)
        self.db_path = db_path

    def ping(self, item):
        domain = item['company_domain']
        company_id = item['company_id']
        res = ping(domain, size=1024, timeout=2)
        s = Storge(self.db_path)
        if res:
            s.update_check_domain(company_id, True)
        else:
            s.update_check_domain(company_id, False)
        self.lock.release()

    def start_ping(self, datas):
        for data in tqdm(datas):
            self.lock.acquire()
            threading.Thread(target=self.ping, args=(data,)).start()
        show_message('域名检测结束')
        self.show_domain()

    def show_domain(self):
        s = Storge(self.db_path)
        data = s.select_domain_true()
        show_message(f'有效域名{len(data)}', MessageType.SUCCESS)
