"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests

URL = 'https://sroehl.ddns.net:5000/api/'


# --------------- Helpers that build all of the responses ----------------------

def build_speech_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': response
    }


def no_access_token_response():
    response = {'outputSpeech':
                    {'type': 'PlainText',
                     'text': 'You must have a Baby Journal account to use this skill.  ' +
                             'Please use Alexa app to link your Amazon account with your Baby Journal account'
                },
                'card': {
                    'type': 'LinkAccount'
                },
                'shouldEndSession': True
                }
    return build_response({}, response)



# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speech_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speech_response(
        card_title, speech_output, None, should_end_session))


def add_diaper(intent, session, access_token):
    if 'diaper_type' in intent['slots'] and 'diaper_load' in intent['slots']:
        diaper_type = intent['slots']['diaper_type']['value']
        diaper_load = intent['slots']['diaper_load']['value']
        payload = {'size': diaper_load, 'type': diaper_type}
        headers = {'Authorization': access_token}
        r = requests.post(URL + 'diaper', json=payload, headers=headers, verify=False)
        if r.status_code == requests.codes.ok:
            response_json = r.json()
            speech_output = "Successfully added a " + response_json['diaper_size'] + " " \
                            + response_json['diaper_type'] + " diaper"
        else:
            speech_output = 'Failed to add diaper'
        print(speech_output)
        return build_response({}, build_speech_response(intent['name'], speech_output, '', True))


def add_bottle(intent, session, access_token):
    if 'amount' in intent['slots']:
        amount = int(intent['slots']['amount']['value'])
        payload = {'amount': amount}
        headers = {'Authorization': access_token}
        r = requests.post(URL + 'bottle', json=payload, headers=headers, verify=False)
        if r.status_code == requests.codes.ok:
            response_json = r.json()
            speech_output = "Successfully added a " + str(response_json['amount']) + " ounce bottle"
        else:
            speech_output = 'Failed to add bottle'
        return build_response({}, build_speech_response(intent['name'], speech_output, '', True))


def get_inventory_diaper(intent, session, access_token):
    diaper_size = None
    if 'diaper_size' in intent['slots']:
        diaper_size = intent['slots']['diaper_size']['value']
    headers = {'Authorization': access_token}
    r = requests.get(URL + 'inventory/diaper', headers=headers)
    if r.status_code == requests.codes.ok:
        response_json = r.json()
        if diaper_size is None:
            speech_output = "You have "
            for key in response_json:
                speech_output + str(response_json[key]) + " size " + str(key) + " diapers left, "
        else:
            speech_output = "You have " + str(response_json[diaper_size]) + " size " + diaper_size + " diapers left"
    else:
        speech_output = "Failed to get inventory of diapers"
    return build_response({}, build_speech_response(intent['name'], speech_output, '', True))


def add_inventory_diaper(intent, session, access_token):
    if 'diaper_size' in intent['slots'] and 'amount' in intent['slots']:
        diaper_size = int(intent['slots']['diaper_size']['value'])
        amount = int(intent['slots']['amount']['value'])
        payload = {'size': diaper_size, 'amount': amount}
        headers = {'Authorization': access_token}
        r = requests.post(URL + 'inventory/diaper', json=payload, headers=headers, verify=False)
        if r.status_code == requests.codes.ok:
            response_json = r.json()
            speech_output = "You now have " + str(response_json['amount']) + " size " \
                            + str(response_json['size']) + " diapers left"
        else:
            speech_output = 'Failed to add diapers to inventory'
        return build_response({}, build_speech_response(intent['name'], speech_output, '', True))


def add_inventory_bottle(intent, session, access_token):
    if 'amount' in intent['slots']:
        amount = int(intent['slots']['amount']['value'])
        headers = {'Authorization': access_token}
        payload = {'amount': amount}
        r = requests.post(URL + 'inventory/bottle', json=payload, headers=headers, verify=False)
        if r.status_code == requests.codes.ok:
            response_json = r.json()
            speech_output = "You now have " + str(response_json['amount']) + " " \
                            + "ounces of formula left"
        else:
            speech_output = 'Failed to add formula to inventory'
        return build_response({}, build_speech_response(intent['name'], speech_output, '', True))


def get_inventory_bottle(intent, session, access_token):
    headers = {'Authorization': access_token}
    r = requests.get(URL + 'inventory/bottle', headers=headers)
    if r.status_code == requests.codes.ok:
        response_json = r.json()
        speech_output = "You have " + str(response_json['amount']) + " ounces of formula left"
    else:
        speech_output = "Failed to get inventory of formula"
    return build_response({}, build_speech_response(intent['name'], speech_output, '', True))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session, access_token):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AddDiaper":
        return add_diaper(intent, session, access_token)
    elif intent_name == 'AddBottle':
        return add_bottle(intent, session, access_token)
    elif intent_name == 'GetInventoryDiaper':
        return get_inventory_diaper(intent, session, access_token)
    elif intent_name == 'GetInventoryBottle':
        return get_inventory_bottle(intent, session, access_token)
    elif intent_name == 'AddInventoryDiaper':
        return add_inventory_diaper(intent, session, access_token)
    elif intent_name == 'AddInventoryBottle':
        return add_inventory_bottle(intent, session, access_token)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if 'accessToken' in event['session']['user']:
        access_token = event['session']['user']['accessToken']
    else:
        return no_access_token_response()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], access_token)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
