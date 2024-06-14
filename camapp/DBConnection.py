import mysql.connector

class Db:

    def __init__(self):

        self.cnx = mysql.connector.connect(host="localhost", user="root", password="", database="examhall")
        self.cur = self.cnx.cursor(dictionary=True)


    def select(self, q):
        self.cur.execute(q)
        return self.cur.fetchall()

    def selectOne(self, q):
        self.cur.execute(q)
        return self.cur.fetchone()


    def insert(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.lastrowid

    def update(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.rowcount

    def delete(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.rowcount



    def instoreport(self,title,report):

        qry="INSERT INTO `myapp_report` (`report`,`time`,`date`,`title`) VALUES ('"+report+"',CURTIME(),CURDATE(),'"+title+"')"
        self.insert(qry)

        import pyttsx3

        engine = pyttsx3.init()
        engine.say(title+ ". "+ report  )
        engine.runAndWait()






