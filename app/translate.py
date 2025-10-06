import requests
from flask import current_app
from flask_babel import _

def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')

    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': current_app.config['MS_TRANSLATOR_REGION'],  # add this in config
        'Content-Type': 'application/json'
    }

    url = (
        'https://api.cognitive.microsofttranslator.com/translate'
        f'?api-version=3.0&from={source_language}&to={dest_language}'
    )

    r = requests.post(url, headers=auth, json=[{'Text': text}])

    if r.status_code != 200:
        return _('Error: the translation service failed.\nError code: ' + str(r.status_code))

    return r.json()[0]['translations'][0]['text']
