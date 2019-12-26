# psycopg-test

This code uses Python's PosgreSQL DB library, Psycopg's connectionPool to compare the performance of multithreaded and SingleThread.  

See This Repo.  
[psycopg-test-docker-compose](https://github.com/nanaones/psycopg-test-docker-compose)


---

## Index
 1. Requirenment
 2. Install
 3. Config
 4. Logs
    - json
    - csv


---

## 1. Requirenment  

1. `postgreSQL`  
2. `python3.7`  
3. `python library`
    * python library requirenment  

    ```txt
    $ cat requirements.txt
    
    python_version >= "3.7"
    psycopg2-binary
    pytz
    configparser
    ```

## 2. Install 

`postgreSQL`  
1. [install](https://www.postgresql.org/download/)  
2. run Query in `./query/query.sql`  

`python3.7`  
 [install](https://www.python.org/downloads/)  


`install python requirements`  
```
 $ python3 install -r requirements.txt
```

## 3. Config

Watch `./config/config.ini`

---
```ini
[SQL]
INSERT = INSERT INTO public.t_test(c_test) VALUES (?);

[DB]
user=postgres
password=1234
host=localhost
port=5432
database=postgres

# Set TimeZone it based on pytz
[TIME]
timeZone=Asia/Seoul

[LOG]
logSave=True
# Set Log save path 
logSavePath=/logs/
# Set Log type
logType=json
```  


`About TimeZone`,   
You can run this code to output a list of available TimeZones.    


```python
import pytz

pytz.all_timezones
```

## 4. Logs

By default,   
*  The default save path for logs is determined by the log.logSavePath value in `./config/config.ini`.  
*  logs are stored( in `./logs` path ) as follows:  


1. json

```json

{"now" : "%Y-%m-%d %H:%M:%s+%Z", "start" : "%Y-%m-%d %H:%M:%s", "end" : "%Y-%m-%d %H:%M:%s", "time" : "%s"} \n
```

2. csv

``` csv
"%Y-%m-%d %H:%M:%s+%Z", "%Y-%m-%d %H:%M:%s", "%Y-%m-%d %H:%M:%s", "%s" \n
```

