'''
Connection and SQL script funcs to MySql DB
'''
import mysql.connector
from mysql.connector import errorcode
from log_module import logger

class MySQLConnector(object):
    '''
    connection to MySQL base on 
    https://dev.mysql.com/doc/connector-python/en/
    
    '''
    def __init__(self,dbParams):
        '''
        params
        {host='localhost', port=3032, database=None, user=None, password=None}
        '''
        self.params=dbParams
        
    def connect(self):
        try:
            cnx = mysql.connector.connect(**self.params)
            if cnx.is_connected():
                return cnx
        except mysql.connector.Error as err:
            logger.error(err)
        else:
            pass#self.cnx.close()

    def connection(func):
        def makeConn(self,*args, **kwargs):
            ctx=self.connect()
            result=func(self,ctx,*args,**kwargs)
            ctx.close()
            return result
        return makeConn

    @connection
    def test(self,connection,params):  #test Querry
        cur = connection.cursor()
        #print (params)
        sql='select * from mname where id=%s'
        cur.execute(sql,tuple(params))
        result = cur.fetchall()
        cur.close()
        return result 

    @connection
    def querry(self,connection,sql:str,params:list=[]):
        '''
        base querry
        sql: sql string as "select * from ... where ..=%s and .=%s"
        params: None or list of %s..%sN params [param1,...,paramN] by order in sql
        '''
        cur = connection.cursor()
        cur.execute(sql,tuple(params))
        result = cur.fetchall()
        cur.close()
        return result 

    @connection
    def insert(self,connection,table:str,values:list):
        '''
        insert querry. 
        
        table: table name in sql string as INSERT INTO TABLE VALUES ( %s... %s )
        values:list of tuples (%s..%sN) values by order in sql [(p1,p2)...,(p1,p2)]
         
        Values nunber = table fields number!!!
        '''
        if len(values):
            valueLenngth=len(values[0])
            if values[0]:
                values = list(filter(None, values))
                sql=f'INSERT INTO {table} VALUES( {", ".join(["%s"] * valueLenngth)})'
                cur = connection.cursor()
                cur.executemany(sql,values)
                connection.commit()
                cur.close()
            else:
                logger.error(f'Empty value tuple in isert querry to table:{table}, values:{values} ')
        else:
            logger.error(f'Empty value list in isert querry to table:{table}, values:{values} ')

if __name__ == '__main__':
    import globals

    db=MySQLConnector(globals.MySQLServerParams)
    result=db.test([10018])
    for rec in result:
        print(rec)

    # import globals
    # connection = mysql.connector.connect(**globals.MySQLServerParams)

    # cursor =connection.cursor()

    # query = ("SELECT * from mname where id=%s")

    # cursor.execute(query,tuple(10021))

    # for rec in cursor:
    #     print(rec)

    # cursor.close()
    # connection.close()
  