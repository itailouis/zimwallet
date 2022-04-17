import requests
from flask import Blueprint, Response, request

from functools import wraps
import logging

from src.services.ussdSessionService import UssdSessionService
from src.models.messageRequest import MessageRequest
from src.models.messageResponse import MessageResponse

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

ussdentry = Blueprint("ussdentry", __name__, url_prefix="/ussd/econet/main")


def returns_xml(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='text/xml; charset=utf-8')

    return decorated_function


@ussdentry.post("/entry", strict_slashes=False)
@returns_xml
def main():
    messageRequest = MessageRequest().fromXML(xml_data=request.data)
    messageResponse = MessageResponse(sourceNumber=messageRequest.sourceNumber)

    session = UssdSessionService().getSession(messageRequest=messageRequest)

    if messageRequest.stage == "FIRST":
        UssdSessionService().reStartSession(messageRequest)
        messageNA = "welcome to ZimWallet \n"
        if UssdSessionService().userExist(messageRequest=messageRequest):
            messageNA += "Please Enter Pin To access your wallet "
            messageResponse.message = messageNA
            messageResponse.stage = "PENDING"
            session.menu = "pin"
            session.root_menu = "login"
            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()

        else:
            messageNA += "1 Register \n 2 View Ts & Cs"

        messageResponse.message = messageNA
        messageResponse.stage = "PENDING"
        session.menu = "registation"
        UssdSessionService().saveSession(messageRequest, session)
        return messageResponse.toXMLResponse()
    else:
        print("-------------------")
        print("---------root_menu " + session.root_menu + "--- menu  " + session.menu)
        if session.root_menu == "main" and session.menu == "registation" and messageRequest.message.isdigit() and int(
                messageRequest.message) == 1:
            messageResponse.message = "Please enter First Name"
            session.menu = "username"
            session.root_menu = "registation"

            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()
        if session.root_menu == "registation" and session.menu == "username":
            messageResponse.message = "Please enter Last Name"
            session.menu = "lastname"
            session.paramOne = messageRequest.message

            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()
        if session.root_menu == "registation" and session.menu == "lastname":
            messageResponse.message = "Please enter Nation ID No# (00-0000000X00)"
            session.menu = "nationid"
            session.paramTwo = messageRequest.message

            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()
        if session.root_menu == "registation" and session.menu == "nationid":
            messageResponse.message = "Please enter Email Address"
            session.menu = "email"
            session.paramThree = messageRequest.message

            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()
        if session.root_menu == "registation" and session.menu == "email":
            messageResponse.message = "Please your Four Digit Pin"
            session.menu = "pin"
            session.paramFour = messageRequest.message
            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()
        if session.root_menu == "registation" and session.menu == "pin":
            NAMsg = "Please Confirm \n"
            session.menu = "confirm"
            session.paramFive = messageRequest.message

            UssdSessionService().saveSession(messageRequest, session)
            session = UssdSessionService().getSession(messageRequest=messageRequest)

            NAMsg += "First Name: {} \n " \
                     "Last Name {} \n " \
                     "Nation Id {} \n " \
                     "Email {}  \n" \
                     "PIN {} \n".format(session.paramOne,
                                        session.paramTwo,
                                        session.paramThree,
                                        session.paramFour,
                                        session.paramFive,
                                        )

            messageResponse.message = NAMsg + "1 confirm \n " \
                                              "2 cancel "
            # session.menu = "confirm"
            # session.paramFive = messageRequest.message

            # UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()
        if session.root_menu == "registation" and session.menu == "confirm":
            if messageRequest.message.isdigit() and int(messageRequest.message) == 1:

                session = UssdSessionService().getSession(messageRequest=messageRequest)

                pload = {
                    "firstName": session.paramOne,
                    "lastName": session.paramTwo,
                    "mobileNumber": messageRequest.sourceNumber,
                    "email": session.paramFour,
                    "title": "NA",
                    "dateOfBirth": "NA",
                    "nationalIdNumber": session.paramThree,
                    "streetAddress": "NA",
                    "suburb": "NA",
                    "province": "NA",
                    "city": "NA",
                    "country": "NA",
                    "maritalStatus": "NA",
                    "gender": "NA",
                    "branchId": 0
                }
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post('https://zimwallet-api.herokuapp.com/api/v1/users', headers=headers,
                                         data=pload)
                print("Status Code", response.status_code)
                print("JSON Response ", response.json())

                if response.status_code == 200:
                    messageResponse.message = "Thank You for Registering \n ZImWallet"
                    session.root_menu = "main"
                    session.menu = "main"
                    pload = {
                        "customerId": 0,
                        "pinNumber": str(session.paramFour)
                    }
                    response = requests.post('https://zimwallet-api.herokuapp.com/api/v1/customer-accounts',
                                             headers=headers, data=pload)


                else:
                    messageResponse.message = "Fail To ZImWallet Please Try Again"
                    session.root_menu = "main"
                    session.menu = "main"

                UssdSessionService().reStartSession(messageRequest)


            else:
                messageResponse.message = "Your Registering for ZimWallet \n has been canceled"
                session.root_menu = "main"
                session.menu = "main"

            UssdSessionService().saveSession(messageRequest, session)
            return messageResponse.toXMLResponse()

        if session.root_menu == "main" and session.menu == "registation" and messageRequest.message.isdigit() and int(
                messageRequest.message) == 2:
            messageResponse.message = "Visit here to view Terms and Conditions"
            return messageResponse.toXMLResponse()
        else:
            pass

        if session.root_menu == "login" and session.menu == "pin":

            if UssdSessionService().isCorrect(messageRequest):
                messageResponse.message = "Main Menu:\n " \
                                          "1) Payments\n " \
                                          "2) Transfer Funds\n " \
                                          "3) Fund Wallet\n " \
                                          "4) Get Change \n " \
                                          "5) Balance Enquiry \n" \
                                          "6) Other \n " \
                                          "7) Help \n " \
                                          "8) Your Profile"
                session.menu = "home"
                session.root_menu = "main"
                messageResponse.stage = "PENDING"
                UssdSessionService().saveSession(messageRequest, session)
                return messageResponse.toXMLResponse()
            else:
                messageResponse.message = "Wrong Pin try Again"
                session.menu = "pin"
                session.root_menu = "login"
                messageResponse.stage = "PENDING"
                UssdSessionService().saveSession(messageRequest, session)
                return messageResponse.toXMLResponse()
        if session.root_menu == "main" and session.menu == "home":
            if messageRequest.message.isdigit() and int(messageRequest.message) == 1:
                messageResponse.message = "payments"
                session.menu = "payments"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 2:
                messageResponse.message = "Transfer Funds"
                session.menu = "transferFunds"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 3:
                messageResponse.message = "Fund Wallet"
                session.menu = "fundWallet"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 4:
                messageResponse.message = "Get Change"
                session.menu = "getChange"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 5:
                messageResponse.message = "Balance Enquiry"
                session.menu = "balanceEnquiry"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)

            if messageRequest.message.isdigit() and int(messageRequest.message) == 6:
                messageResponse.message = "Other Menu \n  " \
                                          "Select Option: \n" \
                                          "1) Make Donation \n " \
                                          "2) Promotions \n " \
                                          "Enter 0 for the Main menu"
                session.menu = "other"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 7:
                messageResponse.message = "Help ZimWallet\n" \
                                          "Select Option: \n " \
                                          "1) Report Transaction \n" \
                                          "2) Block/Unblock Account \n" \
                                          "3) About ZimWallet \n" \
                                          "Enter 0 for the Main "
                session.menu = "help"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 8:
                messageResponse.message = "Your Profile"
                session.menu = "yourProfile"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 0:
                messageResponse.message = "payments"
                session.menu = "main"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and messageRequest.message == "p":
                messageResponse.message = "payments"
                session.menu = "payments"
                session.root_menu = "main"
                UssdSessionService().saveSession(messageRequest, session)

            return messageResponse.toXMLResponse()
        if session.root_menu == "other" and session.menu == "main":
            if messageRequest.message.isdigit() and int(messageRequest.message) == 1:
                messageResponse.message = "Make Donation \n  " \
                                          " Select Charity: \n " \
                                          "1) Charity X \n" \
                                          "2) Charity Y \n" \
                                          "3) Charity Z \n" \
                                          "Enter p for the Previous menu \n" \
                                          " 0 for the Main menu"
                session.menu = "other"
                session.root_menu = "Donation"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 2:
                messageResponse.message = "Promotions \n  " \
                                          " Select Charity: \n " \
                                          "1) Charity X \n" \
                                          "2) Charity Y \n" \
                                          "3) Charity Z \n" \
                                          "Enter p for the Previous menu \n" \
                                          " 0 for the Main menu"
                session.menu = "other"
                session.root_menu = "Donation"
                UssdSessionService().saveSession(messageRequest, session)
        if session.root_menu == "main" and session.menu == "help":
            if messageRequest.message.isdigit() and int(messageRequest.message) == 1:
                messageResponse.message = "Report Transaction\n " \
                                          "Enter Transaction Ref No. " \
                                          "Enter p for the Previous menu " \
                                          "and 0 for the Main menu"
                session.menu = "report"
                session.root_menu = "help"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 2:
                session.menu = "Block/Unblock Account"
                session.root_menu = "help"
                UssdSessionService().saveSession(messageRequest, session)
            if messageRequest.message.isdigit() and int(messageRequest.message) == 3:
                session.menu = "About ZimWallet"
                session.root_menu = "help"
                UssdSessionService().saveSession(messageRequest, session)

            return messageResponse.toXMLResponse()
        if session.root_menu == "help" and session.menu == "report":
            messageResponse.message = " Report {}\n" \
                                      " Enter 1 to confirm or \n" \
                                      "0 to return to main menu".format(messageRequest.message)
            session.menu = "reportConfirm"
            session.root_menu = "report"
            session.paramOne = messageRequest.message
            UssdSessionService().saveSession(messageRequest, session)
        if session.root_menu == "report" and session.menu == "reportConfirm":

            if messageRequest.message.isdigit() and int(messageRequest.message) == 1:
                messageResponse.message = "Report Successful. \n" \
                                          "Our support team will contact you as soon as possible.\n" 
                                          #"Enter 0 to return to main menu"
                session.menu = "main"
                session.root_menu = "home"
                messageRequest.stage = "COMPLETE"
                # session.paramOne = messageRequest.message
                UssdSessionService().saveSession(messageRequest, session)

            if messageRequest.message.isdigit() and int(messageRequest.message) == 0:
                messageResponse.message = "Home"

                session.menu = "help"
                session.root_menu = "main"
                # session.paramOne = messageRequest.message

                UssdSessionService().saveSession(messageRequest, session)

            return messageResponse.toXMLResponse()

    return MessageResponse(sourceNumber="263772567639", message=messageRequest.message).toXMLResponse()

    # return xml_data


@ussdentry.get("/hello")
def test():
    return {"message": "hello world"}
