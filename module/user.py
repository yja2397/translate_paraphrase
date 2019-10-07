from module import db
from datetime import datetime

class memberManage():
    def __init__(self):
        self.db = db.Database()

    def login(self, id, pswd):
        sql     = "SELECT pswd FROM TS.client WHERE id = '%s'"% (id)
        data = self.db.executeOne(sql)

        if not data: # 알맞은 아이디 없음
            return 1
        elif data['pswd'] == pswd: # 로그인 완료
            return 0
        else: # 비밀번호 오류
            return 2

    def join(self, id, pswd):
        sql     = "SELECT pswd FROM TS.client WHERE id = '%s'"% (id)
        data = self.db.executeOne(sql)

        if data: # 이미 해당 아이디 있음.
            return 1
        else: # 회원가입
            sql     = "INSERT INTO TS.client(id, pswd) \
                        VALUES('%s', '%s')"% (id, pswd)
            self.db.execute(sql)

            return 0

    def insertSen(self, sentence, id):
        
        sql     = "SELECT searchCnt FROM TS.clientsearch WHERE sentence = '%s' and clientid = '%s'"% (sentence, id)
        data = self.db.executeOne(sql)

        if not data:
            sql     = "INSERT INTO TS.clientsearch(sentence, id) \
                        VALUES('%s', '%s')"% (sentence, id)
            self.db.execute(sql)

        sql     = "UPDATE TS.clientsearch \
                    SET searchCnt = searchCnt + 1 \
                    WHERE sentence='%s' and id = '%s'"% (sentence, id)
        self.db.execute(sql)

        return 'commit'
    
    def insertPara(self, clientid, paragraph, paratitle=None):
        
        now = datetime.now()
        now = '%s-%s-%s %s:%s:%s' % (now.year, now.moth, now.day, now.hour, now.minute, now.second)

        if not paratitle:
            
            paratitle = now + '에 작성된 글입니다.'
        
        sql     = "INSERT INTO TS.clientpara \
                    VALUES('%s', '%s', '%s', '%s')"% (paratitle, id, paragraph, now)
        self.db.execute(sql)

        return 'commit'


    def findSen(self, id):
        sql     = "SELECT sentence FROM TS.clientsearch WHERE id = '%s'"% (id)
        data = self.db.executeAll(sql)

        return data

    def findPara(self, id):
        sql     = "SELECT paratitle, paratime FROM TS.clientpara WHERE id = '%s'"% (id)
        data = self.db.executeAll(sql)

        return data

    def lookPara(self, id, paratime):
        sql     = "SELECT paratitle, paragraph FROM TS.clientpara WHERE id = '%s' and paratime = '%s"% (id, paratime)
        data = self.db.executeAll(sql)

        return data