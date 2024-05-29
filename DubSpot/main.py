import flask
import json
from hubspot import HubSpot

api_client = HubSpot(access_token='pat-na1-efedb56d-50f0-436e-a57b-ff21b5913070')

app = flask.Flask(__name__)

@app.route("/")
def hello_world():

    contacts = api_client.crm.contacts.basic_api.get_page()

    for contact in contacts:
        print(contact.dump(contact))

if __name__ == "__main__":
  app.run(debug=True)
