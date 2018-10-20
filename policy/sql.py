import pymysql.connections
from policy import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor()

class Sql:

    @classmethod
    def insert_policy(cls, department, date, name, content, overview):
        sql = "insert into policy(`department`, `date`, `name`, `content`, `overview`)values(%(department)s,%(date)s,%(name)s,%(content)s,%(overview)s)"
        value = {
            'department': department,
            'date': date,
            'name': name,
            'content': content,
            'overview': overview
        }
        cur.execute(sql, value)
        cnx.commit()


    @classmethod
    def select(cls, name):
        sql = "select exists(select 1 from policy where name = %(name)s)"
        value = {
            'name':name
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]