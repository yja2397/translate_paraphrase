import db

class memberManage():
    def __init__(self):
        self.db = db.Database()

    def login(self, id, pswd):

        sql     = "SELECT pswd FROM TS.user WHERE userId = '%s'"% (id)
        data = self.db.executeOne(sql)

        if not data:
            return 1
        elif data == pswd:
            return id
        else:
            return 2

    def join(self, id, pswd):

        sql     = "SELECT pswd FROM TS.user WHERE userId = '%s'"% (id)
        data = self.db.executeOne(sql)

        if data:
            return 1
        else:
            return 0

    def findSen(self, id):
        
        sql     = "SELECT sentence FROM TS.userSen WHERE userId = '%s'"% (id)
        data = self.db.executeAll(sql)

        return data