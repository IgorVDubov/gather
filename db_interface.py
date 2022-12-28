'''
Фабрика интерфейса DB
DB adapter for different SQL servers:
-MySQL
-Sqlight3

'''
# SELECT='select'
# INSERT='insert'
# UPDATE='update'
# DELETE='delete'
from consts import Consts

SELECT=Consts.SELECT
INSERT=Consts.INSERT
UPDATE=Consts.UPDATE
DELETE=Consts.DELETE

from typing import Union



class DBInterface():
    def __init__(self,dbType,dbparams) -> None:
        if dbType==Consts.MYSQL:
            from mysqlconnector import MySQLConnector
            self.connection= MySQLConnector(dbparams)
        if dbType==Consts.SQLIGHT3:
            from sqlite3_connector import Sqlight3Connector
            self.connection= Sqlight3Connector(dbparams)
    def execSQL(self,requestType:str, sql:str, params=None ):
        '''
        execute SQL request
        requestType: 'select' | 'insert' | 'updatre' | 'delete'
        sql: sql request body with %s params 
        params: tuple or list of params
        exmpl: execSQL('select','SELECT * FROM %s', ('table',))
        '''
        # print (f'execSQL: {requestType},{sql}, params:{params}')
        if requestType==SELECT:
            return self.connection.querry(sql,params)
        if requestType==INSERT:
            return self.connection.insert(sql,params)
        if requestType==UPDATE:
            return self.connection.update(sql,params)
        if requestType==DELETE:
            return self.connection.delete(sql,params)



if __name__ == '__main__':
    import globals

    db=DBInterface(Consts.MYSQL,globals.MySQLServerParams)

    result=db.execSQL(SELECT,'select * from pname')
    for rec in result:
        print(rec)

    db.execSQL(INSERT,'INSERT INTO track_2 VALUES (%s, %s, %s, %s)', (4001, '2022:10:27 19:43:50', 2, 18))
    # db.execSQL(UPDATE,'update pname set name=%s where id=%s',('test1',5))

    result=db.execSQL(SELECT,'select * from track_2')
    for rec in result:
        print(rec)
    # result=db.execSQL(DELETE,'delete from pname where id=%s',(5,))

    