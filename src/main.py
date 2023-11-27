from flask import Flask, request
import requests
from datetime import datetime
import json

app = Flask(__name__)

cardio_data = {'heart_rate': None,
               'systolic_blood_pressure': None,
               'diastolic_blood_pressure': None,
               'collection_position': None,
               'collection_location': None,
               'collection_person': None}

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
    elif cardio_data['collection_position'] is None:
        with open('standard_responses/collection_position.xml') as f:
            response = f.read()
        return response
    elif cardio_data['collection_location'] is None:
        with open('standard_responses/collection_location.xml') as f:
            response = f.read()
        return response
    elif cardio_data['collection_person'] is None:
        with open('standard_responses/collection_person.xml') as f:
            response = f.read()
        return response
    else:
        response = '<Response>'
        response += f'<Say>Your provided heartrate is {cardio_data["heart_rate"]}</Say>'
        response += f'<Say>Your provided systolic bloodpressure is {cardio_data["systolic_blood_pressure"]}</Say>'
        response += f'<Say>Your provided diastolic bloodpressure is {cardio_data["diastolic_blood_pressure"]}</Say>'
        response += '<GetDigits timeout="30" finishOnKey="#" callbackUrl="/submit">'
        response += '<Say>If this is correct and you want to submit, press one followed by the hash sign. If you want to abort press two followed by the hash sign</Say>'
        response += '</GetDigits></Response>'

        return response

def send_data_to_cedar():
    cedar_url = 'https://resource.metadatacenter.org/template-instances'
    cedar_api_key = 'apiKey 62838dcb5b6359a1a93baeeef907669813ec431437b168efde17a61c254b3355'
    ontology_prefix = 'https://github.com/abdullahikawu/PGHD/tree/main/vocabularies/'
    current_time = datetime.now()

    cedar_template = open('cedar_template.json')
    data = json.load(cedar_template)
    data['PatientID']['@value'] = '1234' # TODO: Add patient ID request
    data['DataCollectedViaIVR']['@value'] = 'Yes'
    data['Date']['@value'] = current_time.strftime('%Y-%m-%d')
    data['Pulse Number']['@value'] = str(cardio_data['heart_rate'])
    data['Blood Pressure (Systolic)']['@value'] = str(cardio_data['systolic_blood_pressure'])
    data['Blood Pressure (Diastolic)']['@value'] = str(cardio_data['diastolic_blood_pressure'])
    data['CollectionPosition']['@value'] = ontology_prefix + str(cardio_data['collection_position'])
    data['CollectionLocation']['@value'] = ontology_prefix + str(cardio_data['collection_location'])
    data['CollectionPerson']['@value'] = ontology_prefix + str(cardio_data['collection_person'])
    data['schema:name'] = f'PGHD_BP {current_time.strftime("%d/%m/%Y %H:%M:%S")}'
    cedar_template.close()

    requests.post(cedar_url, json=data, headers={'Content-Type': 'application/json',
                                                 'Accept': 'application/json',
                                                 'Authorization': cedar_api_key})

def clear_cardio_data():
    cardio_data['heart_rate'] = None
    cardio_data['systolic_blood_pressure'] = None
    cardio_data['diastolic_blood_pressure'] = None
    cardio_data['collection_position'] = None
    cardio_data['collection_location'] = None
    cardio_data['collection_person'] = None

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


@app.route("/collection_position", methods=['POST']):
def collection_position():
    digits = request.values.get("dtmfDigits", None)
    if digits is not None:
        if digits == 1:
            cardio_data['collection_position'] = 'Laying'
        elif digits == 2:
            cardio_data['collection_position'] = 'Sitting'
        elif digits == 3
            cardio_data['collection_position'] = 'Standing'

    return cardio_data_collector()


@app.route("/collection_location", methods=['POST'])
def collection_location():
    digits = request.values.get("dtmfDigits", None)
    if digits is not None:
        if digits == 1:
            cardio_data['collection_location'] = 'Home'
        elif digits == 2:
            cardio_data['collection_location'] = 'Outside'

    return cardio_data_collector()


@app.route("/collection_person", methods=['POST'])
def collection_person():
    digits = request.values.get("dtmfDigits", None)
    if digits is not None:
        if digits == 1:
            cardio_data['collection_person'] = 'Patient'
        elif digits == 2:
            cardio_data['collection_person'] = 'Caregiver'
    
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
