####################
#
# Web Application for connection between PGHD and CEDAR
# using the IVR voice service by Africa's Talking
#
# Copies from webApp.py in example dir in AT GitHub
#
####################

import os
from flask import Flask, request, render_template
from flask_restful import Resource, Api

import africastalking

app = Flask(__name__)
api = Api(app)

username = os.getenv('user_name', 'sandbox')  # Get right username/app-name
api_key = os.getenv('api_key', 'fake')  # Right API. User-dependent

africastalking.initialize(username, api_key)


# Is this necessary if we do not have a web-interface?
@app.route('/')
def index():
    return render_template('index.html')


def request_bp():
    """Function set up to request data from a digital blood pressure monitor
    RK: I don't know if this works like this but this is how I currently understand it"""

    response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
    response += '<Say voice="man" playBeep="false">Please enter your the heart '
    response += 'rate indicated by your device</Say> </GetDigits> </Response>'

    heart_rate = request.values.get("dtmfDigits", None)

    response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
    response += '<Say voice="man" playBeep="false">Please enter the top blood '
    response += 'pressure indicated by your device</Say> </GetDigits> </Response>'

    systolic_bp = request.values.get("dtmfDigits", None)

    response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
    response += '<Say voice="man" playBeep="false">Please enter the bottom blood '
    response += 'pressure indicated by your device</Say> </GetDigits> </Response>'

    diastolic_bp = request.values.get("dtmfDigits", None)

    return [heart_rate, systolic_bp, diastolic_bp]


def request_fitbit():
    """Function set up to request data from a FitBit
    TODO: Check with Sherry which data we require in this case"""
    pass


# I believe this is the template we need to use
# Is this automatically called if this is running with Flask?
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Is request automatically pushed into this function
    session_id = request.values.get("sessionId", None)
    isActive = request.values.get("isActive", None)
    phone_number = request.values.get("callerNumber", None)

    # Authentication check somehwere here?
    response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
    response += '<Say voice="man" playBeep="false">Please enter your patient '  # Eventually replace with a voice-file from
    response += 'ID followed by the hash sign</Say> </GetDigits> </Response>'  # someone who speaks Nigerian ?
    # There is no text-to-voice for the Nigerian language sadly

    # My current understanding is that calling this sends a new request to the phone?
    patient_id = request.values.get("dtmfDigits", None)

    # Something like this to route patients towards the correct response?
    # Meanwhile while this is tracking we need to somehow store all the data as well.
    # patients = load_from_files (maybe? not very secure-ish)
    if patient_id in patients['bp']:
       pghd = request_bp() # call-and-response in function
    elif patient_id in patients['bp']:
       pghd = request_fitbit() # call-and-response in function

    response = '<Response><Say voice="man" playBeep="false">Thank you for sharing your data</Say></Response>'

    return response


# From AT
# if dtmfDigits == '1234':
#  response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
#  response +=' <Say voice="man" playBeep="false"> Press 1 followed by a hash '
#  response +='sign to get your account balance or 0 followed by a hash sign to'
# response += ' quit</Say> </GetDigits></Response>'

# elif dtmfDigits == '1':
#  response = '<Response>'
#  response += '<Say voice="man" playBeep="false" >Your balance is 1234 Shillings</Say>'
#  response+= '<Reject/> </Response>'

# elif dtmfDigits == '0':
#  response = '<Response>'
#  response += '<Say voice="man" playBeep="false" >Its been a pleasure, good bye </Say>'
#  response+= '<Reject/> </Response>'


if __name__ == '__main__':
    app.run(debug=True)
