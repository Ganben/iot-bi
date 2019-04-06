# -*- coding: utf-8 -*-
# best for i/o sql interface for history stats

#TODO:
#sql for pin_id_4_goods
#shop for pin_ids
#chart_generator
#statistical view
import logging
import datetime

import mysql.connector
from mysql.connector import errorcode

import redis

# method example code
# sqldb = mysql.connector.connect(host='localhost',database='iotbi',user='root',password='123456')
'''
try:
  cnx = mysql.connector.connect(user='scott',
                                database='employ')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()

'''

rpool = redis.ConnectionPool(host='localhost', port=6379, db=0)
rd = redis.Redis(connection_pool=rpool)

### set up logging
logger = logging.getLogger('datamodel')
logger.setLevel(logging.DEBUG)

# fh
fh = logging.FileHandler('datamodel.log')
fh.setLevel(logging.DEBUG)
# ch
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


# sql tables
DB_NAME = 'iotbi'
TABLES = {}
TABLES['devicepinstats'] = (
    "CREATE TABLE `devicepinstats` ("
    "  `rec_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `devicepin` bigint NOT NULL,"
    "  `count` smallint NOT NULL,"
    "  PRIMARY KEY (`rec_no`)"
    ") ) ENGINE=InnoDB")

#

class PinStats:
    def __init__(self):
        # add sql conn
        # self.db = sqldb
        pass
    def save_devicecount(self, devicepin, count):
        #
        pass
        script = (
            "INSERT INTO devicepinstats "
            "(date, devicepin, count)  "
            "VALUES (%s, %s, %s)" % (int(devicepin, 16), count))
                  
        try:
            o = self.sql_execute(script)
        return o

    def sql_init(self):
        def create_database(cursor):
            try:
                cursor.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
                )
            except mysql.connector.Error as err:
                print("failed create db")
                exit(1)
        try:
            cnx = mysql.connector.connect(user='root',
            # database='iotbi',
            password='123456',
            host='localhost'
            )
            cursor = cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('db access denied')
                # return
            logger.error('db conn error')
            return
        # execute command
        try:
            cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully.".format(DB_NAME))
                cnx.database = DB_NAME
            else:
                print(err)
                exit(1)
        # 
        else:
            self.cnx = cnx
        # self.sql_init_table()

    def sql_init_table(self):
        if self.cnx is None:
            return
        cursor = self.cnx.cursor()
        for table in  TABLES:
            tablescript = TABLES[table]
            try:
                cursor.execute(tablescript)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logger.info('already exist table')
                else:
                    logger.error(err.msg)
            else:
                logger.info('table OK')
        
        cursor.close()


    def sql_close(self):
        if self.cnx is not None:
            self.cnx.close()
    
    def sql_execute(self, command):
        # 
        if self.cnx is None:
            return
        else:
            cursor = self.cnx.cursor()
        
        try:
            cursor.execute(command)
        except mysql.connector.Error as err:
            logger.error(err.msg)
            cursor.close()
            return False
        else:
            cursor.close()
            return True

def dayswap():
    # retrieve data from redis
    # then save it to sql
    while rd.llen('deviceslist') > 0:
        el = rd.lpop('deviceslist').decode('ascii')
        # loop 4 pins
        for i in range(4):
            k = '%s%s' % (el, i)
            counts = rd.get(k)
            rd.delete(k)
            # save it to sql
            #TODO
