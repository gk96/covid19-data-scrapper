from sshtunnel import SSHTunnelForwarder
import pymysql
import sys

def store_to_db(dictionary, use_tunnel):
    db_port = 3306
    
    if use_tunnel:
        #ssh to server
        server = SSHTunnelForwarder(
        ('192.168.0.110', 22),
        ssh_username='pi',
        ssh_password='gk',
        remote_bind_address=('127.0.0.1', 3306)
        )
    
        server.start()
        
        db_port = server.local_bind_port
        
    # Connect to the database covid_test
    db = pymysql.connect(
    host='127.0.0.1',
    port=db_port,
    user='admin',
    password='admin',
    db='covid_test',
    cursorclass=pymysql.cursors.DictCursor
    )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    fields = (str(list(dictionary.keys()))[1:-1])
    values = (str(list(dictionary.values()))[1:-1])

    # Insert a new record
    sql = 'INSERT INTO `DistrictCounts` (' + fields + ') VALUES (' + values + ')'
    # remove single Quotes
    sql = sql.replace('\'', '')
    #print(sql)
    cursor.execute(sql)
        
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    db.commit()

    db.close()

    # Connect to the database covid19_kerala
    db = pymysql.connect(
    host='127.0.0.1',
    port=db_port,
    user='admin',
    password='admin',
    db='covid19_kerala',
    cursorclass=pymysql.cursors.DictCursor
    )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    fields = (str(list(dictionary.keys()))[1:-1])
    values = (str(list(dictionary.values()))[1:-1])

    # Insert a new record
    sql = 'INSERT INTO `district_count` (' + fields + ') VALUES (' + values + ')'
    # remove single Quotes
    sql = sql.replace('\'', '')
    
    cursor.execute(sql)
    
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    db.commit()

    # disconnect from server
    db.close()

    sys.exit(0)

