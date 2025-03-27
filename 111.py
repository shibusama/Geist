import mysql.connector
from ctpwrapper import MdApi


# 定义行情回调类
class MyMdApi(MdApi):
    def __init__(self, broker_id, investor_id, password, server_address, instruments):
        self.broker_id = broker_id
        self.investor_id = investor_id
        self.password = password
        self.server_address = server_address
        self.instruments = instruments
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="test"
        )
        self.cursor = self.connection.cursor()
        super().__init__()

    def OnFrontConnected(self):
        print("行情服务器连接成功")
        self.ReqUserLogin(self.broker_id, self.investor_id, self.password)

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        if pRspInfo.ErrorID == 0:
            print("登录行情服务器成功")
            self.SubscribeMarketData(self.instruments)
        else:
            print(f"登录行情服务器失败，错误码: {pRspInfo.ErrorID}, 错误信息: {pRspInfo.ErrorMsg.decode('gbk')}")

    def OnRtnDepthMarketData(self, pDepthMarketData):
        symbol = pDepthMarketData.InstrumentID.decode('gbk')
        price = pDepthMarketData.LastPrice
        insert_query = "INSERT INTO futures_market (symbol, price) VALUES (%s, %s)"
        data = (symbol, price)
        try:
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print(f"已插入数据: 符号 {symbol}, 价格 {price}")
        except mysql.connector.Error as error:
            print(f"插入数据时出错: {error}")

    def __del__(self):
        self.cursor.close()
        self.connection.close()


def create_table():
    try:
        # 连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        cursor = connection.cursor()

        # 创建期货行情表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS futures_market (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("表创建成功")
    except mysql.connector.Error as error:
        print(f"创建表时出错: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_table()

    # CTP 行情服务器地址
    server_address = "180.168.146.187:10211"
    # 经纪商 ID
    broker_id = "9999"
    # 投资者 ID
    investor_id = "212893"
    # 密码
    password = "Zc@1319119251"
    # 订阅的期货合约列表
    instruments = ["IF2312", "IC2312"]

    md_api = MyMdApi(broker_id, investor_id, password, server_address, instruments)
    md_api.Create()
    md_api.RegisterFront(server_address)
    md_api.Init()

    while True:
        pass
