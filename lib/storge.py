import sqlite3
from datetime import datetime


class Storge:
    def __init__(self, db='company.db'):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.init()

    def init(self):
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            create table if not exists company(
                company_id varchar(255) primary key  not null ,
                company_name varchar(30) not null,
                company_domain varchar(255),
                create_date date default CURRENT_DATE,
                check_domain bool default False
            )
        ''')
        self.conn.commit()

    def insert_company(self, company_name, company_id, company_domain=''):
        if self.select_one_data(company_id):
            return
        sql = 'insert into company(company_name,company_id,company_domain) values (?,?,?)'
        self.cursor.execute(sql, (company_name, company_id, company_domain))
        self.conn.commit()

    def update_domain_by_id(self, company_id, domain):
        sql = 'update company set company_domain=? where company_id=?'
        self.cursor.execute(sql, (domain, company_id))
        self.conn.commit()

    def parser_data(self, result):
        if not result:
            return None
        data = {
            'company_id': result[0],
            'company_name': result[1],
            'company_domain': result[2],
            'create_date': result[3]
        }
        return data

    def select_one_data(self, company_id):
        sql = 'select * from company where company_id=?'
        self.cursor.execute(sql, (company_id,))
        result = self.cursor.fetchone()
        return self.parser_data(result)

    def select_all_data(self):
        sql = 'select * from company'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [self.parser_data(i) for i in result]

    def select_all_domain_null_data(self):
        sql = 'select * from company where company_domain=""'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [self.parser_data(i) for i in result]

    def select_all_domain_not_null(self):
        sql = 'select * from company where company_domain!=""'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [self.parser_data(i) for i in result]

    def select_today_data(self):
        sql = 'select * from company where create_date=?'
        self.cursor.execute(sql, (datetime.now().strftime('%Y-%m-%d'),))
        result = self.cursor.fetchall()
        return [self.parser_data(i) for i in result]

    def update_check_domain(self, company_id, flag):
        sql = 'update company set check_domain=? where company_id=?'
        self.cursor.execute(sql, (flag, company_id))
        self.conn.commit()

    def select_domain_true(self):
        sql = 'select * from company where check_domain=1'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [self.parser_data(i) for i in result]
