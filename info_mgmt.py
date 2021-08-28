from inventory_db import conn_mysqldb
import pandas as pd

class Info():

    def __init__(self, model, unique_num):
        self.unique_num = unique_num
        self.model = model

    def get_id(self):
        return str(self.unique_num)

    @staticmethod
    def get_area(model): # 특정 장소의 특정 차 수량 정수형 반환
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM model_info WHERE MODEL = '" + str(model) + "'"
        db_cursor.execute(sql)
        area = db_cursor.fetchone()[1]
        return area

    @staticmethod
    def get_all():  # 데이터 프레임으로 반환
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM model_info"
        db_cursor.execute(sql)
        count = pd.DataFrame(db_cursor.fetchall(), columns=['MODEL', 'AREA'])
        return count

#     @staticmethod
#     def create_table():
#         models = [['VSR', 7.632], ['AVT', 8.48625], ['AVTH', 8.48625], ['i30', 7.7903], ['IOH', 8.1354], ['IOE', 8.1354], ['IOE5', 8.76015], ['G70', 8.66725],
#                   ['G80', 9.615375], ['G90', 9.967575], ['VNU', 7.1508], ['KON', 7.569], ['KOH', 7.569], ['NKON', 7.587], ['KOE', 7.524], ['TUC', 8.63495], ['TUCH', 8.63495],
#                   ['STF', 9.0153], ['STFH', 9.0915], ['PSD', 9.0915], ['GV70', 9.0903], ['GV80', 9.766375], ['PTR', 8.9697], ['G80E', 9.634625]]
#         mysql_db = conn_mysqldb()
#         db_cursor = mysql_db.cursor()
#         for model in models:
#             sql = "INSERT INTO model_info (MODEL,AREA) VALUES ('%s', %f);" % (model[0], model[1])
#             db_cursor.execute(sql)
#             mysql_db.commit()
#
# Info.create_table()