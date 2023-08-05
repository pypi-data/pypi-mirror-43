import pymysql

CHARSET = 'utf8'
class Db(object):
    def __init__(self, ip, port, user_name, password, db_name):
        self.ip = ip
        self.port = port
        self.userName = user_name
        self.password = password
        self.dbName = db_name
        self.__connect()

    def __connect(self):
        try:
            self.connection = pymysql.connect(host=self.ip,
                                              port=self.port,
                                              user=self.userName,
                                              passwd=self.password,
                                              db=self.dbName,
                                              charset=CHARSET)
            self.cursor = self.connection.cursor()
        except Exception as e:
            self.connection = None
            print("Connect mysql error!", e)
            return

    def __del__(self):
        if self.connection:
            self.connection.close()
    def __commit(self, sqlStr):
        cursor = self.cursor
        if cursor:
            cursor.execute(sqlStr)
            self.connection.commit()
            return True
    #查询方法,不支持查询大量数据，否则耗光内存
    def select(self, sqlStr):
        try:
            cursor = self.cursor
            if cursor:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print("Excute select method error!", e)
            return None

    #插入方法
    def insert(self, sqlStr):
        try:
            self.__commit(sqlStr)
        except Exception as e:
            print("Excute insert method error!", e)
            return False
    #更新方法
    def update(self, sqlStr):
        try:
            self.__commit(sqlStr)
        except Exception as e:
            print("Excute update method error!", e)
            return False

    #删除方法
    def delete(self, sqlStr):
        try:
            self.__commit(sqlStr)
        except Exception as e:
            print("Excute delete method error!", e)
            return None


if __name__ =='__main__':
    HOST = '192.168.240.197'
    PORT = 8888
    USER = 'root'
    PASSWD = 'root'
    DB = "mall_admin"
    db = Db(HOST, PORT, USER, PASSWD, DB)
    # #正常情况
    # result = db.select("select * from sys_role")
    # print(result)
    #
    # #异常情况，表错误
    # result1 = db.select("select * from sys_role1")
    # print(result1)
    #
    # # 异常情况，字段错误
    # result2 = db.select("select column_One from sys_role")
    # print(result2)

    # 正常情况
    sql = "insert into sys_role (`role_id`, `role_name`, `role_code`, `description`, `status`, `create_time`, `create_by`, `modify_by`, `modify_time`) values ('6386818388630437124', '仓管', 'storer', '仓管', '1', '2018-10-27 13:54:28', 'luhaitao', 'luhaitao', '2018-10-27 13:54:28')"
    result3 = db.insert(sql)
    print(result3)