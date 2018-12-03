# --encoding:utf-8--

import psycopg2
import ConfigParser
from common.commonlogger import commonlogger

config = ConfigParser.ConfigParser()
with open("config.ini", "rw") as cfgfile:
    config.readfp(cfgfile)
    name = config.get("global", "ip")
    print name

commonloggerinstance = commonlogger()
logger =commonloggerinstance.getlogger()

class mysqlhelper:
    def __init__(self):
        self.host = config.get("global", "ip")
        self.charset = config.get("global", "charset")
        self.user = config.get("global", "user")
        self.password = config.get("global", "password")
        try:
            self.conn = psycopg2.connect(host=self.host, user=self.user, passwd=self.password)
            self.conn.set_character_set(self.charset)
            self.conn.select_db(config.get("global", "defaultdb"))
            self.cursor = self.conn.cursor()
        except MySQLdb.Error as e:
            logger.error("inital db error", e)

    def query(self, sql):
        try:
            rows = self.cursor.execute(sql)
            return rows;
        except MySQLdb.Error as e:
            logger.error(e)

    def queryOnlyRow(self, sql):
        try:
            self.query(sql)
            row = {}
            result = self.cursor.fetchone()
            if result is not None:
                desc = self.cursor.description
                for i in range(0, len(result)):
                    row[desc[i][0]] = result[i]
            return row;
        except MySQLdb.Error as e:
            logger.error("query only rows error", e)

    def queryAll(self, sql):
        try:
            self.query(sql)
            result = self.cursor.fetchall()
            desc = self.cursor.description
            rows = []
            for cloumn in result:
                row = {}
                for i in range(0, len(cloumn)):
                    row[desc[i][0]] = cloumn[i]
                rows.append(row)
            return rows;
        except MySQLdb.Error as e:
            logger.error("query all error", e)

    # dataSource={"name":"汤姆克路斯".decode("gbk").encode("utf-8"),"birthday":"1992-03-12"}
    # helper.insert("users", dataSource)
    # print helper.getLastInsertRowId()
    def insert(self, tableName, pData):
        try:
            newData = {}
            for key in pData:
                newData[key] = "'""'" + pData[key] + "'"
            key = ','.join(newData.keys())
            value = ','.join(newData.values())
            sql = "insert into " + tableName + "(" + key + ") values(" + value + ")"
            self.query("set names 'utf8'")
            self.query(sql)
            self.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()
            logger.error("insert error", e)
        finally:
            self.close()


    # pData={"birthday":"2005-05-05 18:32:23"}
    # whereData={"name":"Jack Tang"}
    # helper.update("users", pData, whereData)
    def update(self, tableName, pData, whereData):
        try:
            newData = []
            keys = pData.keys()
            for i in keys:
                item = "%s=%s" % (i, "'""'" + pData[i] + "'")
                newData.append(item)
            items = ','.join(newData)
            newData2 = []
            keys = whereData.keys()
            for i in keys:
                item = "%s=%s" % (i, "'""'" + whereData[i] + "'")
                newData2.append(item)
            whereItems = " AND ".join(newData2)
            sql = "update " + tableName + " set " + items + " where " + whereItems
            self.query("set names 'utf8'")
            self.query(sql)
            self.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()
            logger.error('MySql Error: %s %s' % (e.args[0], e.args[1]))
        finally:
            self.close()

    def getLastInsertRowId(self):
        return self.cursor.lastrowid

    def getRowCount(self):
        return self.cursor.rowcount

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()