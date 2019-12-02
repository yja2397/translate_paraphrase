from module import db
from datetime import datetime

class memberManage():
    def __init__(self):
        self.db = db.Database()

    def login(self, userid, pswd):
        sql     = "SELECT pswd FROM TS.client WHERE id = '%s'"% (userid)
        data = self.db.executeOne(sql)
        self.db.commit()

        if not data: # 알맞은 아이디 없음
            return 1
        elif data['pswd'] == pswd: # 로그인 완료
            return 0
        else: # 비밀번호 오류
            return 2

    def join(self, userid, pswd):
        sql     = "SELECT pswd FROM TS.client WHERE id = '%s'"% (userid)
        data = self.db.executeOne(sql)
        self.db.commit()

        if data: # 이미 해당 아이디 있음.
            return 1
        else: # 회원가입
            sql     = "INSERT INTO TS.client(id, pswd) \
                        VALUES('%s', '%s')"% (userid, pswd)
            self.db.execute(sql)
            self.db.commit()

            return 0

    def insertSen(self, sentence, userid):
        
        sql     = "SELECT searchCnt FROM TS.clientsearch WHERE sentence = '%s' and clientid = '%s'"% (sentence, userid)
        data = self.db.executeOne(sql)
        self.db.commit()

        if not data:
            sql     = "INSERT INTO TS.clientsearch(sentence, clientid) \
                        VALUES('%s', '%s')"% (sentence, userid)

            self.db.execute(sql)
            self.db.commit()

        sql     = "UPDATE TS.clientsearch \
                    SET searchCnt = searchCnt + 1 \
                    WHERE sentence='%s' and clientid = '%s'"% (sentence, userid)
        self.db.execute(sql)
        self.db.commit()

        sql     = "UPDATE TS.client \
                    SET searchCnt = searchCnt + 1 \
                    WHERE id = '%s'"% (userid)
        self.db.execute(sql)
        self.db.commit()

        return 'commit'
    
    def insertPara(self, userid, paragraph, paratitle=None):

        paragraph = paragraph.replace("'", "''")
        
        now = datetime.now()
        now = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

        if not paratitle:
            
            paratitle = now + '에 작성된 글입니다.'
        
        sql     = "INSERT INTO TS.clientpara \
                    VALUES('%s', '%s', '%s', '%s')"% (paratitle, userid, paragraph, now)

        self.db.execute(sql)
        self.db.commit()
        
        sql     = "UPDATE TS.client \
                    SET parCnt = parCnt + 1 \
                    WHERE id = '%s'"% (userid)
        self.db.execute(sql)
        self.db.commit()

        return 'commit'


    def findSen(self, userid):
        sql     = "SELECT sentence, searchCnt FROM TS.clientsearch WHERE clientid = '%s'"% (userid)
        data = self.db.executeAll(sql)
        self.db.commit()

        return data

    def findPara(self, userid):
        sql     = "SELECT paratitle, paratime FROM TS.clientpara WHERE clientid = '%s'"% (userid)
        data = self.db.executeAll(sql)
        self.db.commit()

        return data

    def lookPara(self, userid, paratime):
        sql     = "SELECT paratitle, paragraph FROM TS.clientpara WHERE clientid = '%s' and paratime = '%s'"% (userid, paratime)
        data = self.db.executeAll(sql)
        self.db.commit()

        return data

    def deleteSen(self, userid, deleteSen):
        if deleteSen:
            for sen in deleteSen:
                sql = "DELETE FROM TS.clientsearch WHERE clientid = '%s' AND sentence = '%s'"% (userid, sen)
                self.db.execute(sql)
                self.db.commit()
        
        return ""
    
    def deletePara(self, userid, deleteSen):
        if deleteSen:
            for sen in deleteSen:
                sql = "DELETE FROM TS.clientpara WHERE clientid = '%s' AND paratime = '%s'"% (userid, sen)
                self.db.execute(sql)
                self.db.commit()
        
        return ""

if __name__ == "__main__":
    user = memberManage()
    data = user.findSen("admin")

    for i in data:
        print(i['sentence'])
        print(i['searchCnt'])