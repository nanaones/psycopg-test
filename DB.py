from psycopg2 import pool, DatabaseError, connect
from RequestsToDB import RequestsToDB
from Error import DBPoolThreadValueError

import Decorator

@Decorator.save_resp_time
def pg_query( _query, 
            user = RequestsToDB().config_data.get("DB", "user"), 
            password = RequestsToDB().config_data.get("DB", "password"),
            host = RequestsToDB().config_data.get("DB", "host"),
            port = RequestsToDB().config_data.get("DB", "port"),
            database = RequestsToDB().config_data.get("DB", "database"),
            _printing = False,
            _return = False,
            _save = False
             ):
    
    if _printing:
        print(user)
        print(password)
        print(host)
        print(port)
        print(database)
    try:
        with connect(user=user.replace('"',""),
                                        password=password.replace('"',""),
                                        host=host.replace('"',""),
                                        port=int(port.replace('"',"")),
                                        database=database.replace('"',"")) as connection:
            with connection.cursor() as cursor:
                cursor.execute(_query)
                connection.commit()
                if _printing:
                    print("successfully connect to PostgreSQL ")

                if _return:
                    rows = cursor.fetchall()
                    if len(rows)>0:
                        return rows
                
    except (Exception, DatabaseError) as error:
        print("Error while connecting PostgreSQL", error)
        

@Decorator.save_resp_time
def pg_query_pool( 
            _query, 
            user = RequestsToDB().config_data.get("DB", "user"), 
            password = RequestsToDB().config_data.get("DB", "password"),
            host = RequestsToDB().config_data.get("DB", "host"),
            port = RequestsToDB().config_data.get("DB", "port"),
            dbname = RequestsToDB().config_data.get("DB", "database"),
            _printing = False,
            _return = False,
            _thread = "single",
            minconn = 1
             ):

    if not _thread in ["single", "multi"]:
        raise DBPoolThreadValueError()

    if _printing:
        print(user)
        print(password)
        print(host)
        print(port)
        print(dbname)

    try:
        if _thread == "single" :
            postgreSQL_pool = pool.SimpleConnectionPool(
                                                    dsn=None, 
                                                    minconn=1, 
                                                    maxconn=20,
                                                    user=user,
                                                    password=password,
                                                    host=host,
                                                    port=port,
                                                    dbname=dbname
                                                    )

            make_connect(
                        postgreSQL_pool=postgreSQL_pool, 
                        _query=_query, 
                        _printing=_printing, 
                        _return=_return)

        elif _thread == "multi" :
            postgreSQL_pool = pool.ThreadedConnectionPool( 
                                                    dsn=None, 
                                                    minconn=minconn,
                                                    maxconn=20,
                                                    user=user,
                                                    password=password,
                                                    host=host,
                                                    port=port,
                                                    dbname=dbname
                                                    )

            run_connect(postgreSQL_pool, _query, _printing, _return, minconn=minconn)

        else: raise DBPoolThreadValueError()

    except (Exception, DatabaseError) as error:
        print("Error while connecting PostgreSQL", error)

def run_connect(postgreSQL_pool, _query, _printing, _return, minconn):
    _list = list(divide_list(_list=_query, minconn=minconn))
    [[make_connect( postgreSQL_pool=postgreSQL_pool, _query=_sub, _printing=_printing, _return=_return) for _sub in _lis ] for _lis in _list]

def make_connect(postgreSQL_pool, _query, _printing, _return):
    with postgreSQL_pool.getconn() as connection:
        with connection.cursor() as cursor:
            cursor.execute(_query)
            connection.commit()
            if _printing:
                print("successfully connect to PostgreSQL ")
            if _return:
                rows = cursor.fetchall()
                if len(rows)>0:
                    return rows
            cursor.close()
            postgreSQL_pool.putconn(connection)

def divide_list(_list=[], minconn=1): 
    for i in range(0, len(_list), minconn): 
        yield _list[i:i + minconn] 
