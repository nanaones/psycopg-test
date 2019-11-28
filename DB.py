import psycopg2
from psycopg2 import pool, DatabaseError
from RequestsToDB import RequestsToDB
import Decorator
from Error import DBPoolThreadValueError

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
        with psycopg2.connect(user=user.replace('"',""),
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
            _thread = "single"
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
        postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(dsn=None, 
                                                minconn=1, 
                                                maxconn=20,
                                                user=user,
                                                password=password,
                                                host=host,
                                                port=port,
                                                dbname=dbname
                                                )

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
            
    except (Exception, DatabaseError) as error:
        print("Error while connecting PostgreSQL", error)
    
@Decorator.save_resp_time
def pg_query_pool_with( 
            _query, 
            user = RequestsToDB().config_data.get("DB", "user"), 
            password = RequestsToDB().config_data.get("DB", "password"),
            host = RequestsToDB().config_data.get("DB", "host"),
            port = RequestsToDB().config_data.get("DB", "port"),
            database = RequestsToDB().config_data.get("DB", "database"),
            _printing = False,
            _return = False
             ):
    postgreSQL_pool = False

    if _printing:
        print(user)
        print(password)
        print(host)
        print(port)
        print(database)
    try:
        with psycopg2.pool.SimpleConnectionPool(
                                                1, 
                                                20,
                                                user=user,
                                                password=password,
                                                host=host,
                                                port=port,
                                                database=database
                                                ) as postgreSQL_pool:

            connection  = postgreSQL_pool.getconn()
            cursor = connection.cursor()
            cursor.execute(_query)
            connection.commit()
            
            if _printing:
                print("successfully connect to PostgreSQL ")
                if(postgreSQL_pool):
                    print("Connection pool created successfully")
            if _return:
                rows = cursor.fetchall()
                if len(rows)>0:
                    return rows
                
            cursor.close()
            connection.close()
                
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting PostgreSQL", error)
            
