#/usr/bin/env python
#coding=utf8

import sqlite3

conn = sqlite3.connect('firstTest.db')
print "open database successfully"
c = conn.cursor()
#c.execute('''CREATE TABLE COMPANY(
#            ID INT PRIMARY KEY NOT NULL,
#            NAME TEXT NOT NULL,
#            AGE INT NOT NULL,
#            ADDRESS CHAR(50),
#            SALARY REAL);''')
#print 'table create successfully'

#c.execute("INSERT INTO COMPANY(ID, NAME, AGE, ADDRESS, SALARY) \
#            VALUES(1, 'Paul', 32, 'California', 20000.00)")
#c.execute("INSERT INTO COMPANY(ID, NAME, AGE, ADDRESS, SALARY) \
#             VALUES(2, 'Allen', 25, 'Texas', 15000.00)")
#c.execute("INSERT INTO COMPANY(ID, NAME, AGE, ADDRESS, SALARY) \
#             VALUES(3, 'Teddy', 23, 'Norway', 20000.00);")
#c.execute("INSERT INTO COMPANY(ID, NAME, AGE, ADDRESS, SALARY) \
#             VALUES(4, 'Mark', 25, 'Rich-Mond', 65000.00);")
#conn.commit()
#cursor = c.execute("select id, name, salary from COMPANY")
#for row in cursor:
#    print "ID = ", row[0]
#    print "Name = ", row[1]
#    print "Salary = ", row[2], '\n'

#c.execute("update COMPANY set SALARY = 25000.00 where ID = 1")
#conn.commit()
#cursor = c.execute("select salary from COMPANY where ID = 1")
#for row in cursor:
#    print "salary = ", row[0]

#c.execute("delete from COMPANY where ID = 4;")
#conn.commit()
#cursor = c.execute("select * from COMPANY")
#for row in cursor:
#    print row
#print "select done"
#conn.commit()

conn.close()