from flask import Response
from  datetime import  datetime


class MessageResponse(Response):
    default_mimetype = 'application/xml'

    def __init__(self, transactionTime=datetime.now().isoformat(), transactionID="", sourceNumber="", destinationNumber="727", message=" ",
                 stage="", channel="USSD"):
        self.transactionTime = transactionTime
        self.transactionID = sourceNumber if transactionID == "" else transactionID
        self.sourceNumber = sourceNumber
        self.destinationNumber = destinationNumber
        self.message = message
        self.stage = "FIRST" if stage == "" else stage
        self.channel = channel
        #return super(MessageRequest, self).__init__(response )

    def toXMLResponse(self):
        return "<messageResponse xmlns='http://econet.co.zw/intergration/messagingSchema'>"\
               "<transactionTime>{}</transactionTime>"\
               "<transactionID>{}</transactionID>"\
               "<sourceNumber>{}</sourceNumber>"\
               "<destinationNumber>{}</destinationNumber>"\
               "<message>{}</message>" \
               "<stage>{}</stage>" \
               "<channel>{}</channel>" \
               "</messageResponse> ".format(
            self.transactionTime, self.transactionID, self.sourceNumber, self.destinationNumber, self.message,
            self.stage, self.channel)




    def __repr__(self):
        return 'messageResponse(transactionTime={}, transactionID={}, sourceNumber={}, destinationNumber={},' \
               'message={}, stage={}, channel={})'.format(
            self.transactionTime, self.transactionID, self.sourceNumber, self.destinationNumber, self.message,
            self.stage, self.channel)
