import os
import pymysql.connections

MYSQL_HOST = '35.240.248.27'
MYSQL_DB = 'wallet'
MYSQL_USER = 'daniel'
MYSQL_PASS = 'nihao'

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)