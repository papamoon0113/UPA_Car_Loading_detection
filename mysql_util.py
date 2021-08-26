import pymysql
import pandas as pd

class Mysql:
    def __init__(self):
        self.user='b34616311e0a2b'
        self.passwd='fd4ae79f'
        self.host='us-cdbr-east-04.cleardb.com'
        self.charset='utf8'
        self.dbname = 'heroku_0633f9f5776814d'
        self.db = pymysql.connect(user=self.user,passwd=self.passwd, host=self.host, charset=self.charset, db=self.dbname)
        self.cursor = self.db.cursor()

    def set_table(self, table_name):
        self.table = table_name
        

    def get_data(self):
        sql = f"SELECT * FROM {self.table};"
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = pd.DataFrame(result)
        self.category = result.columns
        self.cursor = self.db.cursor()
        return result
    
    def input(self, arr):
        if len(arr) != len(self.category):
            print(f'{self.table}의 변수 갯수와 INPUT 변수 갯수가 다릅니다!!')
            return
        
        sql = f'INSERT INTO {self.table} ('
        for x in self.category[:-1]:
            sql= sql + str(x) + ', '
        sql = sql + str(self.category[-1]) + ') VALUES ('

        for x in arr[:-1]:
            sql = sql + "'" + str(x) + "', " 
        sql = sql + "'" + str(arr[-1]) + "');" 
        self.cursor.execute(sql)

    def input_detail(self, category, arr):
        for x in category:
            if not x in self.category:
                print('{self.table}에 포함되지 않은 변수가 있습니다! : {x}')
                return

        sql = f'INSERT INTO {self.table} ('
        for x in category[:-1]:
            sql= sql + str(x) + ', '
        sql = sql + str(category[-1]) + ') VALUES ('

        for x in arr[:-1]:
            sql = sql + "'" + str(x) + "', " 
        sql = sql + "'" + str(arr[-1]) + "');" 
        self.cursor.execute(sql)
    
    def execute(self, sql):
        self.cursor.execute(sql)

    def delete_all(self):
        sql = f"DELETE FROM {self.table};"
        self.cursor.execute(sql)

    def save(self):
        self.db.commit()

    def close(self):
        self.db.close()


