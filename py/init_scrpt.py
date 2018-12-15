
import MySQLdb

db = MySQLdb.connect('localhost', 'root','dmitrivas','kursach')

cur = db.cursor()

cur.execute('')
db.commit()
db.close()
