from twilio.rest import Client


class TwilioConnection(object):

    def __init__(self, params):
        self.client = Client(params["account_sid"], params["auth_token"])
        self.from_number = params["from_number"]

    def send_message(self, body, to_number, from_number=None):
        if from_number is None:
            from_number = self.from_number
        self.client.messages.create(body=body, from_=from_number, to=to_number)
