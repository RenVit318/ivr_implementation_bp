from flask import Flask, request
import requests
from datetime import datetime
import json

app = Flask(__name__)

cardio_data = {'heart_rate': None,
               'systolic_blood_pressure': None,
               'diastolic_blood_pressure': None}

def cardio_data_collector():
    if cardio_data['heart_rate'] is None:
        with open('standard_responses/heart_rate.xml') as f:
            response = f.read()
        return response
    elif cardio_data['systolic_blood_pressure'] is None:
        with open('standard_responses/systolic_blood_pressure.xml') as f:
            response = f.read()
        return response
    elif cardio_data['diastolic_blood_pressure'] is None:
        with open('standard_responses/diastolic_blood_pressure.xml') as f:
            response = f.read()
        return response
    else:
        response = '<Response>'
        response += f'<Say>Your provided heartrate is {cardio_data["heart_rate"]}</Say>'
        response += f'<Say>Your provided systolic bloodpressure is {cardio_data["systolic_blood_pressure"]}</Say>'
        response += f'<Say>Your provided diastolic bloodpressure is {cardio_data["diastolic_blood_pressure"]}</Say>'
        response += '<GetDigits timeout="30" finishOnKey="#" callbackUrl="/submit">'
        response += '<Say>If this is correct and you want to submit, press one followed by the hash sign</Say>'
        response += '<Say>If you want to abort press two followed by the hash sign</Say>'
        response += '</GetDigits></Response>'

        return response

def send_data_to_cedar():
    cedar_url = 'https://resource.metadatacenter.org/template-instances'
    cedar_api_key = 'apiKey 62838dcb5b6359a1a93baeeef907669813ec431437b168efde17a61c254b3355'
    current_time = datetime.now()

    cedar_template = open('cedar_template.json')
    data = json.load(cedar_template)
    data['DataCollectedViaIVR']['@value'] = 'yes'
    data['Date']['@value'] = current_time.strftime('%Y-%m-%d')
    data['Pulse Number']['@value'] = cardio_data['heart_rate']
    data['Blood Pressure (Systolic)']['@value'] = cardio_data['systolic_blood_pressure']
    data['Blood Pressure (Diastolic)']['@value'] = cardio_data['diastolic_blood_pressure']
    data['schema:name'] = f'PGHD {current_time.strftime("%d/%m/%Y %H:%M:%S")}'
    cedar_template.close()

    requests.post(cedar_url, json=data, headers={'Content-Type': 'application/json',
                                                 'Accept': 'application/json',
                                                 'Authorization': cedar_api_key})

def clear_cardio_data():
    cardio_data['heart_rate'] = None
    cardio_data['systolic_blood_pressure'] = None
    cardio_data['diastolic_blood_pressure'] = None

@app.route("/pghd_handler", methods=['POST'])
def pghd_handler():
    with open('standard_responses/pghd_menu.xml') as f:
        response = f.read()
    return response


@app.route("/pghd_cardio_handler", methods=['POST'])
def pghd_cardio_handler():
    digits = request.values.get("dtmfDigits", None)
    if digits == '1':
        return cardio_data_collector()
    else:
        return '<Response><Reject/></Response>'


@app.route("/heart_rate", methods=['POST'])
def heart_rate():
    digits = request.values.get("dtmfDigits", None)
    if digits is not None:
        cardio_data['heart_rate'] = digits

    return cardio_data_collector()


@app.route("/systolic_blood_pressure", methods=['POST'])
def systolic_blood_pressure():
    digits = request.values.get("dtmfDigits", None)
    if digits is not None:
        cardio_data['systolic_blood_pressure'] = digits

    return cardio_data_collector()


@app.route("/diastolic_blood_pressure", methods=['POST'])
def diastolic_blood_pressure():
    digits = request.values.get("dtmfDigits", None)
    if digits is not None:
        cardio_data['diastolic_blood_pressure'] = digits

    return cardio_data_collector()


@app.route("/submit", methods=['POST'])
def submit():
    digits = request.values.get("dtmfDigits", None)
    if digits == '1':
        send_data_to_cedar()
        clear_cardio_data()
        return '<Response><Say>Your data has been saved, thank you for your time</Say><Reject/></Response>'
    else:
        clear_cardio_data()
        return '<Response><Reject/></Response>'


if __name__ == '__main__':
    app.run(debug=True)
