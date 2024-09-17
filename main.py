from cmd import Cmd

from lib.msg import show_message
from lib.msg import MessageType
from lib.spider import Spider
from lib.storge import Storge
from lib.ping import Ping


class SrcTool(Cmd):

    prompt = '>>'

    def __init__(self):
        super().__init__()
        self.s = Storge('lib/company.db')
        self.spider = Spider()
        self.p = Ping()
        self.init()

    def init(self):
        intro = '''                            
           .---.                       
          /. ./|                       
      .--'.  ' ;  ,---.          .---. 
     /__./ \ : | '   ,'\        /. ./| 
 .--'.  '   \\' ./   /   |    .-'-. ' | 
/___/ \ |    ' .   ; ,. :   /___/ \: | 
;   \  \;      '   | |: :.-'.. '   ' . 
 \   ;  `      '   | .; /___/ \:     ' 
  .   \    .\  |   :    .   \  ' .\    
   \   \   ' \ |\   \  / \   \   ' \ | 
    :   '  |--"  `----'   \   \  |--"  
     \   \ ;               \   \ |     
      '---"                 '---"  
    '''
        print(intro)
        self.do_show('')
        res = self.s.select_all_data()
        if len(res) == 0:
            show_message('当前没有数据，是否要进行获取数据 y/n: ')
            r = input()
            if r == 'y':
                self.do_get_company('')
            else:
                pass

    def do_get_company(self, arg):
        """获取全部页数的公司信息"""
        self.spider.start_list()

    def do_update(self, arg):
        """获取第一页的公司信息"""
        show_message('开始更新中')
        self.spider.start_list(1)

    def do_domain(self, arg):
        """获取公司域名信息"""
        show_message('准备获取域名中')
        self.spider.get_company_domain()
        show_message('获取成功', MessageType.SUCCESS)

    def do_show(self, arg):
        """显示数据"""
        company_num = len(self.s.select_all_data())
        show_message(f'目前存储公司数量 {company_num}')
        company_null_domain_num = len(self.s.select_all_domain_null_data())
        show_message(f'域名为空的公司数量 {company_null_domain_num}')
        today_company = len(self.s.select_today_data())
        show_message(f'今日获取公司数量 {today_company}')
        data = self.s.select_domain_true()
        show_message(f'有效域名{len(data)}', MessageType.SUCCESS)

    def do_info(self, arg):
        """info today：显示今天获取到的公司信息
            info domain: 导出有效域名
        """
        if arg == 'today':
            data = self.s.select_today_data()
            for item in data:
                company_name = item['company_name']
                company_domain = item['company_domain']
                show_message(f'{company_name}-----{company_domain}')
            show_message(f'今日共计 {len(data)}')
        elif arg == 'domain':
            data = self.s.select_domain_true()
            show_message('准备导出数据: domain.txt')
            f = open('domain.txt', 'a+')
            for item in data:
                f.write(item['company_domain'] + '\n')

    def do_check(self, arg):
        """检测域名有效性"""
        show_message('准备开始检测域名中')
        self.p.start_ping(self.s.select_all_domain_not_null())

    def do_help(self, arg):
        super().do_help(arg)

    def do_exit(self, arg):
        """exit"""
        print('Bye~')
        exit(-1)

    def emptyline(self):
        pass


if __name__ == '__main__':
    srctool = SrcTool()
    srctool.cmdloop()
