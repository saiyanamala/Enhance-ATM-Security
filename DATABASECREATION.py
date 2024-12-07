import sqlite3 as sql
conn=sql.connect('ATMdata.db')
conn.execute('''CREATE TABLE IMAGES(ID INT PRIMARY KEY NOT NULL,IMAGE NOT NULL ,PHONE_NO VARCHAR(10) NOT NULL);''')
conn.close()

