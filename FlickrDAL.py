import sqlite3 as db

class FlickrDAL:
    def __init__(self):
        self.is_conn_open = False
        self.__connect_()
    def __connect_(self):
        if not self.is_conn_open:
            self.conn = db.connect('flickr.db')
            self.conn.row_factory = db.Row
            self.cur = self.conn.cursor()
            self.is_conn_open = True
    def readID(self, name=None):
        if name==None:
            self.cur.execute('select name,userid from Accounts')
        else:
            self.cur.execute('select name,userid from Accounts where name=? ',(name,))
        return tuple(self.cur.fetchall())
    def insertUser(self,name):
        self.cur.execute('select name from Accounts where name=? ',(name,))
        if (len(self.cur.fetchall())==0):
            self.cur.execute('insert into Accounts (name) values(?)',(name,))
        pass
    def updateID(self,name,ID):
        self.cur.execute('select name from Accounts where name=? ',(name,))
        if (len(self.cur.fetchall())==0):
            self.cur.execute('insert into Accounts (name,userid) values(?)',(name,ID))
        else:
            self.cur.execute('update Accounts set userid=? where name=?',(ID,name))
        pass
    def __close_connection_(self):
        if self.is_conn_open:
            self.conn.commit()
            self.conn.close()
            self.is_conn_open = False
    def __del__(self):
        self.__close_connection_()

if __name__=="__main__":
    flickrDal=FlickrDAL()
    for name,id in flickrDal.readID():
        print(name,id if id!=None else "nope")
