'''
DB adapter for different SQL servers:
MySQL

'''
from mysql_connector import MySQLConnector
from consts import Consts

def dbInit(dbType,dbparams):
    if dbType==Consts.MYSQL:
            return MySQLConnector(dbparams)


if __name__ == '__main__':
    import globals

    db=dbInit(Consts.MYSQL,globals.MySQLServerParams)

    result=db.querry('select * from pname')
    for rec in result:
        print(rec)

    db.insert('pname',[(1,1),()])

    result=db.querry('select * from pname')
    for rec in result:
        print(rec)