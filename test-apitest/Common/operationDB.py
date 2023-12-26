from Config import ReadConfig
import pymysql

from Common import Log


class operationDB:

    global host, user, password, port, db, config
    readconfig = ReadConfig.readconfig()
    host = readconfig.get_DATABASE("host")
    port = readconfig.get_DATABASE("port")
    user = readconfig.get_DATABASE("user")
    password = readconfig.get_DATABASE("password")
    db = readconfig.get_DATABASE("database")
    config = {
        'host': str(host),
        'port': int(port),
        'user': user,
        'password': password,
        'db': db
    }
    #实例初始化
    def __init__(self):
        self.logger = Log.log('sql_log').logger
        # self.db = readconfig.get_DATABASE("database")
        self.connect=None #pymysql.connect(**config)
        self.cursor=None #self.connect.cursor(pymysql.cursors.DictCursor)
        # connectdb = pymysql.Connect(host=host,port=port,user=user,password=password,db='see')




#设置连接的database库
    def set_db(self,database='tmc_services'):
        db = database
#连接DB
    def connection_db(self):
        try:
            self.connect = pymysql.connect(**config)
            self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)
        except ConnectionError:
            self.logger.error("数据库连接失败")


#执行sql

    def exe_sql(self,exesql):
        self.connection_db()
        count = self.cursor.execute(exesql)
        self.connect.commit()
        return count


#返回全部数据
    def get_all(self):
        result=self.cursor.fetchall()
        return  result

#返回单条数据
    def get_one(self):
        result=self.cursor.fetchone()
        return result

#关闭DB
    def colse_db(self):
        self.connect.close()



if __name__ == "__main__":
    con =operationDB()
    con_db = con.exe_sql('select * from train_task')
    sul=con.get_one()
    print(con_db)
    print(sul)