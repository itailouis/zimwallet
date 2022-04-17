from src.database import UssdSession, db


class UssdSessionService:

    def __init__(self):
        pass

    def reStartSession(self,messageRequest):
        session = UssdSession.query.filter(UssdSession.source == messageRequest.sourceNumber).one()
        print(session)
        if session is not None:
            pass
            #db.session.delete(session)
            #db.session.commit()

    def isCorrect(self, messageRequest):

        return True

    def getSession(self, messageRequest):
        session = UssdSession.query.filter(UssdSession.source == messageRequest.sourceNumber).one_or_none()
        print(session)

        if session == None:
            self.saveSession(messageRequest,session)

        return UssdSession.query.filter(UssdSession.source == messageRequest.sourceNumber).one_or_none()

    def saveSession(self, messageRequest,session):
        #session = UssdSession.query.filter(UssdSession.source == messageRequest.sourceNumber).one_or_none()
        print(session)
        if session is None:
            session = UssdSession.query.filter(UssdSession.source == messageRequest.sourceNumber).one_or_none()
            if session is None:
                session = UssdSession(root_menu = "main",menu = "login",source = messageRequest.sourceNumber);
                print("save data")

        else:
            print("alread saved data")
            session.root_menu = session.root_menu
            session.menu = session.menu
            session.source = messageRequest.sourceNumber
            session.message = messageRequest.message

        db.session.add(session)
        db.session.commit()

    def userExist(self, messageRequest):

        return True
