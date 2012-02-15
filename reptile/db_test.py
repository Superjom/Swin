import sqlite3 as sq

strr = "create table site (name CHAR);"

cx = sq.connect("./chunwei.db")
cu = cx.cursor()

cu.execute(strr)
