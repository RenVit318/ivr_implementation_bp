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

username = os.getenv('user_name', 'sandbox') # Get right username/app-name
api_key = os.getenv('api_key', 'fake') # Right API. User-dependent

africastalking.initialize(username, api_key)

# Is this necessary if we do not have a web-interface?
@app.route('/')
def index():
    return render_template('index.html')

# I believe this is the template we need to use
# Is this automatically called if this is running with Flask?
@app.route("/voice", methods = ['GET', 'POST'])
def voice():
  # Is request automatically pushed into this function
  session_id   = request.values.get("sessionId", None)
  isActive  = request.values.get("isActive", None)
  phone_number = request.values.get("callerNumber", None)

  # Authentication check somehwere here?
  response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
  response += '<Say voice="man" playBeep="false">Please enter your account ' #Eventually replace with a voice-file from
  response += 'number followed by the hash sign</Say> </GetDigits> </Response>' #someone who speaks Nigerian ?

  dtmfDigits = request.values.get("dtmfDigits", None)
  
  # Mock code:
  # patients = load_from_files (maybe? not very secure-ish)
  # if dtmfDigits in patients['bp']:
  #   pghd = ask_for_bp() # call-and-response in function
  # elif dtmfDigits in patients['bp']:
  #   pghd = ask_for_fitbit() # call-and-response in function
  # 
  # respone = "<Response><Say voice="man" playBeep="false">Thank you for sharing your data</Say></Response>
  
  
  # From AT
  #if dtmfDigits == '1234':
  #  response = '<Response> <GetDigits timeout="30" finishOnKey="#">'
  #  response +=' <Say voice="man" playBeep="false"> Press 1 followed by a hash '
  #  response +='sign to get your account balance or 0 followed by a hash sign to'
  # response += ' quit</Say> </GetDigits></Response>'

  #elif dtmfDigits == '1':
  #  response = '<Response>'
  #  response += '<Say voice="man" playBeep="false" >Your balance is 1234 Shillings</Say>'
  #  response+= '<Reject/> </Response>'

  #elif dtmfDigits == '0':
  #  response = '<Response>'
  #  response += '<Say voice="man" playBeep="false" >Its been a pleasure, good bye </Say>'
  #  response+= '<Reject/> </Response>'

  return response


if __name__ == '__main__':
    app.run(debug=True)
