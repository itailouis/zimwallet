from flask import Request
from  datetime import  datetime
import xmltodict


class MessageRequest(Request):
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
        return "<messageRequest xmlns='http://econet.co.zw/intergration/messagingSchema'>"\
               "<transactionTime>{}</transactionTime>"\
               "<transactionID>{}</transactionID>"\
               "<sourceNumber>{}</sourceNumber>"\
               "<destinationNumber>{}</destinationNumber>"\
               "<message>{}</message>" \
               "<stage>{}</stage>" \
               "<channel>{}</channel>" \
               "</messageRequest> ".format(
            self.transactionTime, self.transactionID, self.sourceNumber, self.destinationNumber, self.message,
            self.stage, self.channel)

    def fromXML(self , xml_data):
        self.transactionTime = xmltodict.parse(xml_data)["messageRequest"]["transactionTime"];
        self.transactionTime= xmltodict.parse(xml_data)["messageRequest"]["transactionTime"];
        self.transactionID= xmltodict.parse(xml_data)["messageRequest"]["transactionID"];
        self.sourceNumber= xmltodict.parse(xml_data)["messageRequest"]["sourceNumber"];
        self.destinationNumber= xmltodict.parse(xml_data)["messageRequest"]["destinationNumber"];
        self.message= xmltodict.parse(xml_data)["messageRequest"]["message"];
        self.stage= xmltodict.parse(xml_data)["messageRequest"]["stage"];
        self.channel = xmltodict.parse(xml_data)["messageRequest"]["channel"];
        return self


    def __repr__(self):
        return 'MessageRequest(transactionTime={}, transactionID={}, sourceNumber={}, destinationNumber={},' \
               'message={}, stage={}, channel={})'.format(
            self.transactionTime, self.transactionID, self.sourceNumber, self.destinationNumber, self.message,
            self.stage, self.channel)
