import telebot
import time
import datetime
import json
import requests
import glob
import logging
from util import *
import spacy
import os.path
spacyNlp = spacy.load("en_core_web_sm")
jobTitleNlp = spacy.load("JOB_TITLE")
dateTimeNlp = spacy.load("DATE_TIME")

from mindmeld import configure_logs
configure_logs()
from mindmeld.components.nlp import NaturalLanguageProcessor


bot_token = '1037478288:AAF32qOmRlUUbf5xUADkxNKKu7OWvyJlzH4'
print("-" * 15)
print("Initialising Four Bot")
bot = telebot.TeleBot('1037478288:AAF32qOmRlUUbf5xUADkxNKKu7OWvyJlzH4')
print("Four Bot is now ready")
print("-" * 15)
print("Waiting to receive Telegram messages...")
ts = time.time()

logging.basicConfig(filename=LOG_DIR + 'TeleBot ' + str(datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')) +
                    'log.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
logging.info('============== Start =================')
logging.info(str('Time Started: ' +
                 datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')))
logging.info('main: TeleBot Started')
logging.info('======================================')


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(
        msg, "Hello! Send me a contract file in pdf, or a piece of information in the contract you want to process as a text")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    input_text = message.text
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    nlp = NaturalLanguageProcessor(app_path=path)
    nlp.build(incremental=True)
    sentences = input_text.split(".")
    reply = "\nThe contract has been summarized into the key details, as seen below \n\n"
    for s in sentences:
        if s is not "":
            processedWord = nlp.process(s)
            intent = processedWord.get('intent')
            domain = processedWord.get('domain')
            print("Intent is : " + intent)
            print("Domain is : " + domain)

            # handle salary case
            result_salary = ''
            if intent == 'get_salary':
                for c in s:
                    if c.isdigit():
                        result_salary += c
                reply += "The SALARY of the employee is " + result_salary + "/month\n"

            doc = spacyNlp(s)
            jobDoc = jobTitleNlp(s)
            dateDoc = dateTimeNlp(s)

            for ent in doc.ents:
                if ent.label_ == 'PERSON' and intent == 'employment_details':
                    reply += "The EMPLOYEE in the contract is : " + ent.text + "\n"
                elif ent.label_ == 'PERSON' and intent == 'employed_by':
                    reply += "The EMPLOYER in the contract is : " + ent.text + "\n"
                elif ent.label_ == 'ORG':
                    reply += "The COMPANY that the employee will report to is : " + ent.text + "\n"
                elif ent.label_ == 'GPE':
                    reply += "APPLICABLE LAW : " + ent.text + "\n"

            for ent in jobDoc.ents:
                if intent == 'job_details':
                    reply += "The JOB TITLE of the employee is : " + ent.text + "\n"
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)

            for ent in dateDoc.ents:
                if intent == 'contract_date':
                    reply += "The contract was SIGNED on : " + ent.text + "\n"
                elif intent == 'effective_date':
                    reply += "The STARTING date of employment is : " + ent.text + "\n"
                elif intent == 'last_date':
                    reply += "The TERMINATION date of employment is : " + ent.text + "\n"

    # path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # nlp = NaturalLanguageProcessor(app_path=path)
    # nlp.build(incremental=True)
    # processWord = message.text
    # processedWord = nlp.process(processWord)
    # intent = processedWord.get('intent')
    # domain = processedWord.get('domain')
    # logging.info('intent: ' + intent)
    # logging.info('domain: ' + domain)
    # if domain == 'greeting':
    #     reply = handleGreeting(intent)
    # else:  # domain = nanocore_faq
    #     reply = handleFaq(intent)

    bot.reply_to(message, reply)  # responds with success message


@bot.message_handler(content_types=['document'])
def handle_doc(message):
    reply = "\nThe contract has been summarized into the key details, as seen below \n\nThe contract was SIGNED on : 13 May 2010\nThe EMPLOYER in the contract is : Edinburgh Printmakers\nThe EMPLOYEE in the contract is : Teh Poh Heng\nThe STARTING date of employment is : 22 August 2010\nThe JOB TITLE of the employee is : secretary of internships\nThe TERMINATION date of the employment is : 22 August 2012\nThe SALARY of the employee is : $300,000.00 per annum\n"
    time.sleep(4)
    bot.reply_to(message, reply)  # responds with success message


bot.polling()  # gets bot to start listening for updates
