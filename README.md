# Flask Learning Journey
Following "The Flask Mega Tutorial" by Miguel Grinberg

Microblog App by Miguel Grinberg

## Requirement: Google App Password and MS Translator
1. It is necessary to set up gmail app password to enable the email functionality.
2. It is necessary to set up Microsoft Translation API to enable the translation functionality.

## Enable App Password for Email Functionality
1. Visit the Google Account of the email you wish to use for the sender in your Microblog App. Then navigate to **App Password**
2. Ensure **2FA** is enabled in order to create an **App Password**
3. Select a name for your App, then you will be provided with password on your screen
4. **This password must be saved** to the .env file, if you lost the password you must create another **App Password**. Copy it to the **MAIL_PASSWORD=** and set the **MAIL_USERNAME=** to the gmail account your created the password for.


## Create Microsoft Azure Translator Resource
1. Create an Azure AI Translator Resource:
Azure Subscription: You need an active Azure subscription. If you don't have one, you can create a free account.
Create Resource: In the Azure portal, search for "Translator" and create a new Translator resource. You can also create an "Azure AI Foundry" resource, which supports newer features and large language model translation.
2. Configuration: Provide necessary details like a resource group, region (Global is recommended for Translator Text API), a name for your service, and a pricing tier (start with the free tier).
Keys and Endpoint: Once the resource is deployed, navigate to its page and find the "Keys and Endpoint" section under "Resource Management." Copy your subscription key and region to <MS_TRANSLATOR_KEY> and <MS_TRANSLATOR_REGION>.

## Deploy Microblog App with Vagrant Windows 10
[Vagrant Deployment](vagrant_deployment.md)

## Deploy Microblog App with Docker WSL2 Ubuntu
[Docker Deployment](docker_deployment.md)

## Notes

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
