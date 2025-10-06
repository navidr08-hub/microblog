# Flask Learning Journey
Following "The Flask Mega Tutorial" by Miguel Grinberg

Microblog App by Miguel Grinberg


### Need to compare my version to Miguel's verison
- I hardcoded environment variables
- I also have different code that only works with newer api's
  - translate, email, etc.

- In order to use a real mail server and send emails, I used googlemail (gmail). In order to use gmail to send emails for logging or password reset, it is necessary to create an **App Password** (as of 2025-10-25/YYYY-MM-DD). The process is simple one can search how to set up an App-Password. Although for this use case I followed ChatGPT's instructions, to summarize the following options were used to configure the App Password:
  - Firstly it is required to enable **2FA** in order to create an **App Password**
  - You must then select a name for your App, then you will be provided with password on your screen
  - **This password must be saved** to the .env file, if you lost the password you must create another **App Password**

### Inconsistencies between my version and Miguel's version of Microblog
1. Emails:
 - **app/__init__.py:65:v16.0**
  - My verion = <my-secondary-gmail-account>
  - Miguels version = `'no-reply@' + app.config['MAIL_SERVER']`
  - Not sure if Miguel's version would work, will need to try later
2. Translate:
 - **config.py:17:v16.0**
  - My version = `MS_TRANSLATOR_REGION`
  - Miguels version = `ELASTICSEARCH_URL`
 - **app/translate.py:11:v16.0**
  - My version = `'Ocp-Apim-Subscription-Region': current_app.config['MS_TRANSLATOR_REGION']`
  - Miguels version = `'Ocp-Apim-Subscription-Region': 'westus'`
 - **app/translate.py:12:v16.0**
  - My version = `'Content-Type': 'application/json'`
  - Miguels version = `}`

### I need to document all these changes in the end

### Then I need to document how to pull down my repo and get a running and functioning app from scratch
