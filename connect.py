import pymysql
from admin import host, port, user, password, bot

connection = pymysql.connect(host = host, port = port, user = user,
                             password = password, database = 'list_del', cursorclass = pymysql.cursors.DictCursor)
cursor = connection.cursor()