import psycopg2
from psycopg2 import pool
from RequestsToDB import RequestsToDB
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
        connection = psycopg2.connect(user=user.replace('"',""),
                                        password=password.replace('"',""),
                                        host=host.replace('"',""),
                                        port=int(port.replace('"',"")),
                                        database=database.replace('"',""))
        cursor = connection.cursor()
        cursor.execute(_query)
        connection.commit()
        if _printing:
            print("successfully connect to PostgreSQL ")

        if _return:
            rows = cursor.fetchall()
            if len(rows)>0:
                return rows
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting PostgreSQL", error)
        
    finally:
        if (connection):
            cursor.close()
            connection.close()
            if _printing:
                print("PostgreSQL connection is closed")

@Decorator.save_resp_time
def pg_query_pool( 
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
        # TODO Try to Use [with ~ as ~:]
        
        # postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(
        #                                                      1, 
        #                                                      20,
        #                                                      user=user,
        #                                                      password=password,
        #                                                      host=host,
        #                                                      port=port,
        #                                                      database=database
        #                                                      )

        postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(
                                                             1, 
                                                             20,
                                                             user=user,
                                                             password=password,
                                                             host=host,
                                                             port=port,
                                                             database=database
                                                             )

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
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting PostgreSQL", error)
        
    finally:
        if (postgreSQL_pool):
            postgreSQL_pool.closeall
        if _printing:
            print("PostgreSQL connection pool is closed")
    